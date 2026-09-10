"""
Calendar Agent - Manages calendar operations using Google Calendar API
"""
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta, timezone
import os
import sys
from pathlib import Path
from .base_agent import BaseAgent, logger

# Add utils to path
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.oauth_helper import get_calendar_service
from utils.gemini_client import get_gemini_client


class CalendarAgent(BaseAgent):
    """Agent specialized in calendar management"""

    def __init__(self):
        super().__init__(
            name="Calendar Agent",
            description="Manages calendar events, checks availability, and schedules appointments"
        )
        self.calendar_id = "primary"
        self.gemini = get_gemini_client()

    def can_handle(self, task: str) -> bool:
        """Check if this agent can handle the task"""
        calendar_keywords = [
            "calendar", "schedule", "meeting", "appointment", "event",
            "free time", "availability", "book", "reschedule", "busy"
        ]
        task_lower = task.lower()
        return any(keyword in task_lower for keyword in calendar_keywords)

    def _get_user_email(self, context: Dict[str, Any]) -> Optional[str]:
        """Extract user email from context"""
        return context.get("user_email")

    def _parse_datetime(self, date_string: str, time_string: str = None) -> str:
        """Parse date/time string to RFC3339 format"""
        try:
            if time_string:
                dt_string = f"{date_string} {time_string}"
                dt = datetime.strptime(dt_string, "%Y-%m-%d %H:%M")
            else:
                dt = datetime.strptime(date_string, "%Y-%m-%d")
                dt = dt.replace(hour=9)  # Default to 9 AM

            # Add timezone info
            dt = dt.replace(tzinfo=timezone.utc)
            return dt.isoformat()
        except:
            # Default to next hour
            dt = datetime.now(timezone.utc) + timedelta(hours=1)
            return dt.isoformat()

    async def execute(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute calendar-related tasks"""
        self.update_status("thinking", "Analyzing calendar request")

        user_email = self._get_user_email(context)
        if not user_email:
            return {
                "success": False,
                "error": "User not authenticated",
                "message": "Please sign in with Google to access your calendar"
            }

        try:
            task_lower = task.lower()

            # Check availability
            if "free" in task_lower or "available" in task_lower or "availability" in task_lower:
                result = await self._check_availability(user_email, context)
            # Schedule event
            elif "schedule" in task_lower or "book" in task_lower or "create" in task_lower:
                result = await self._create_event(user_email, task, context)
            # List events
            elif "show" in task_lower or "list" in task_lower or "what" in task_lower or "calendar" in task_lower:
                result = await self._list_events(user_email, context)
            # Cancel event
            elif "cancel" in task_lower or "delete" in task_lower:
                result = await self._cancel_event(user_email, context)
            else:
                result = await self._list_events(user_email, context)

            self.record_success()
            return result

        except Exception as e:
            self.record_failure(str(e))
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to process calendar request"
            }

    async def _list_events(self, user_email: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """List calendar events from real Google Calendar"""
        self.update_status("active", "Fetching calendar events")

        try:
            service = get_calendar_service(user_email)
            if not service:
                return self._fallback_list_events()

            # Get events for today and next 7 days
            now = datetime.utcnow()
            time_min = now.isoformat() + 'Z'
            time_max = (now + timedelta(days=7)).isoformat() + 'Z'

            events_result = service.events().list(
                calendarId=self.calendar_id,
                timeMin=time_min,
                timeMax=time_max,
                maxResults=10,
                singleEvents=True,
                orderBy='startTime'
            ).execute()

            events = events_result.get('items', [])

            formatted_events = []
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                end = event['end'].get('dateTime', event['end'].get('date'))

                # Parse datetime
                if 'T' in start:
                    start_dt = datetime.fromisoformat(start.replace('Z', '+00:00'))
                    end_dt = datetime.fromisoformat(end.replace('Z', '+00:00'))
                    start_time = start_dt.strftime('%H:%M')
                    end_time = end_dt.strftime('%H:%M')
                    date = start_dt.strftime('%Y-%m-%d')
                else:
                    # All-day event
                    start_time = "All day"
                    end_time = ""
                    date = start

                formatted_events.append({
                    "id": event['id'],
                    "title": event.get('summary', 'No title'),
                    "start": start_time,
                    "end": end_time,
                    "date": date,
                    "description": event.get('description', ''),
                    "location": event.get('location', ''),
                    "attendees": len(event.get('attendees', []))
                })

            logger.info(f"Retrieved {len(formatted_events)} real calendar events for {user_email}")

            return {
                "success": True,
                "agent": self.name,
                "action": "list_events",
                "events": formatted_events,
                "count": len(formatted_events),
                "source": "real_calendar_api",
                "message": f"Found {len(formatted_events)} upcoming events in your calendar"
            }

        except Exception as e:
            logger.error(f"Calendar API error for {user_email}: {str(e)}")
            return self._fallback_list_events()

    async def _check_availability(self, user_email: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Check calendar availability from real Google Calendar"""
        self.update_status("active", "Checking calendar availability")

        try:
            service = get_calendar_service(user_email)
            if not service:
                return self._fallback_availability()

            # Check for today by default
            check_date = context.get("date", datetime.now().strftime("%Y-%m-%d"))
            start_time = f"{check_date}T00:00:00Z"
            end_time = f"{check_date}T23:59:59Z"

            # Get busy times
            body = {
                "timeMin": start_time,
                "timeMax": end_time,
                "timeZone": "UTC",
                "items": [{"id": self.calendar_id}]
            }

            busy_result = service.freebusy().query(body=body).execute()
            busy_times = busy_result['calendars'][self.calendar_id]['busy']

            # Calculate free slots (9 AM to 6 PM)
            work_start = datetime.fromisoformat(f"{check_date}T09:00:00")
            work_end = datetime.fromisoformat(f"{check_date}T18:00:00")

            free_slots = []
            current_time = work_start

            for busy in busy_times:
                busy_start = datetime.fromisoformat(busy['start'].replace('Z', ''))
                busy_end = datetime.fromisoformat(busy['end'].replace('Z', ''))

                # Add free slot before this busy time
                if current_time < busy_start:
                    free_slots.append({
                        "start": current_time.strftime('%H:%M'),
                        "end": busy_start.strftime('%H:%M')
                    })

                current_time = max(current_time, busy_end)

            # Add final free slot if there's time left
            if current_time < work_end:
                free_slots.append({
                    "start": current_time.strftime('%H:%M'),
                    "end": work_end.strftime('%H:%M')
                })

            logger.info(f"Found {len(free_slots)} free slots for {user_email} on {check_date}")

            return {
                "success": True,
                "agent": self.name,
                "action": "check_availability",
                "date": check_date,
                "free_slots": free_slots,
                "busy_count": len(busy_times),
                "source": "real_calendar_api",
                "message": f"Found {len(free_slots)} available time slots for {check_date}"
            }

        except Exception as e:
            logger.error(f"Calendar availability error for {user_email}: {str(e)}")
            return self._fallback_availability()

    async def _create_event(self, user_email: str, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Create a calendar event in real Google Calendar"""
        self.update_status("active", "Creating calendar event")

        try:
            service = get_calendar_service(user_email)
            if not service:
                return self._fallback_create_event()

            # Use Gemini to extract datetime from the task message
            logger.info(f"Extracting datetime from task: {task}")
            datetime_info = self.gemini.extract_datetime_from_query(task)
            logger.info(f"Extracted datetime info: {datetime_info}")

            # Extract event details from context or use defaults
            title = context.get("title", datetime_info.get("description", "New Meeting"))
            description = context.get("description", "")
            location = context.get("location", "")

            # Build start and end times from extracted datetime
            if datetime_info.get("has_datetime") and datetime_info.get("date"):
                date = datetime_info["date"]
                time = datetime_info.get("time", "09:00")
                end_time_str = datetime_info.get("end_time", "")

                # Parse start time
                start_dt = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
                start_dt = start_dt.replace(tzinfo=timezone.utc)

                # Parse or calculate end time
                if end_time_str:
                    end_dt = datetime.strptime(f"{date} {end_time_str}", "%Y-%m-%d %H:%M")
                    end_dt = end_dt.replace(tzinfo=timezone.utc)
                else:
                    # Use duration from extraction
                    duration_hours = datetime_info.get("duration_hours", 1.0)
                    end_dt = start_dt + timedelta(hours=duration_hours)

                start_time = start_dt.isoformat()
                end_time = end_dt.isoformat()

                logger.info(f"Parsed times - Start: {start_time}, End: {end_time}")
            else:
                # Fallback to context or default times
                start_time = context.get("start_time")
                end_time = context.get("end_time")

                if not start_time:
                    start_dt = datetime.now(timezone.utc) + timedelta(hours=1)
                    start_time = start_dt.isoformat()

                if not end_time:
                    start_dt = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
                    end_dt = start_dt + timedelta(hours=1)
                    end_time = end_dt.isoformat()

            # Create event
            event = {
                'summary': title,
                'description': description,
                'location': location,
                'start': {'dateTime': start_time, 'timeZone': 'UTC'},
                'end': {'dateTime': end_time, 'timeZone': 'UTC'},
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'email', 'minutes': 10},
                        {'method': 'popup', 'minutes': 10}
                    ]
                }
            }

            # Add attendees if provided
            attendees = context.get("attendees", [])
            if attendees:
                event['attendees'] = [{'email': email} for email in attendees]

            # Add meeting link if provided (from Meeting Agent)
            meeting_link = context.get("meeting_link")
            if meeting_link:
                event['description'] = f"{description}\n\nGoogle Meet: {meeting_link}".strip()

            # Create the event
            created_event = service.events().insert(
                calendarId=self.calendar_id,
                body=event
            ).execute()

            logger.info(f"Created real calendar event {created_event['id']} for {user_email}")

            # Format the start time for display
            start_display = datetime.fromisoformat(start_time.replace('Z', '+00:00')).strftime('%A, %B %d at %I:%M %p')

            return {
                "success": True,
                "agent": self.name,
                "action": "create_event",
                "event_id": created_event['id'],
                "title": title,
                "start_time": start_time,
                "end_time": end_time,
                "start_display": start_display,
                "event_link": created_event.get('htmlLink'),
                "source": "real_calendar_api",
                "message": f"Successfully created calendar event '{title}' for {start_display}"
            }

        except Exception as e:
            logger.error(f"Calendar create error for {user_email}: {str(e)}")
            return self._fallback_create_event()

    async def _cancel_event(self, user_email: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Cancel a calendar event in real Google Calendar"""
        self.update_status("active", "Canceling calendar event")

        try:
            service = get_calendar_service(user_email)
            event_id = context.get("event_id")

            if not service or not event_id:
                return {
                    "success": False,
                    "agent": self.name,
                    "action": "cancel_event",
                    "message": "Cannot cancel event - missing event ID or calendar access"
                }

            # Delete the event
            service.events().delete(
                calendarId=self.calendar_id,
                eventId=event_id
            ).execute()

            logger.info(f"Deleted calendar event {event_id} for {user_email}")

            return {
                "success": True,
                "agent": self.name,
                "action": "cancel_event",
                "event_id": event_id,
                "source": "real_calendar_api",
                "message": "Successfully canceled the calendar event"
            }

        except Exception as e:
            logger.error(f"Calendar cancel error for {user_email}: {str(e)}")
            return {
                "success": False,
                "agent": self.name,
                "action": "cancel_event",
                "error": str(e),
                "message": "Failed to cancel calendar event"
            }

    # Fallback methods for when API is not available
    def _fallback_list_events(self):
        """Fallback when real calendar API is unavailable"""
        events = [
            {
                "id": "fallback_1",
                "title": "Team Standup",
                "start": "09:00",
                "end": "09:30",
                "date": datetime.now().strftime("%Y-%m-%d"),
                "description": "Daily team sync",
                "location": "Conference Room A",
                "attendees": 5
            },
            {
                "id": "fallback_2",
                "title": "Client Meeting",
                "start": "15:00",
                "end": "16:00",
                "date": datetime.now().strftime("%Y-%m-%d"),
                "description": "Quarterly review",
                "location": "Zoom",
                "attendees": 3
            }
        ]

        return {
            "success": True,
            "agent": self.name,
            "action": "list_events",
            "events": events,
            "count": len(events),
            "source": "simulated",
            "message": f"Found {len(events)} events (simulated data)"
        }

    def _fallback_availability(self):
        """Fallback availability when real calendar API is unavailable"""
        free_slots = [
            {"start": "09:00", "end": "10:00"},
            {"start": "14:00", "end": "15:30"},
            {"start": "16:00", "end": "17:00"}
        ]

        return {
            "success": True,
            "agent": self.name,
            "action": "check_availability",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "free_slots": free_slots,
            "source": "simulated",
            "message": f"Found {len(free_slots)} available time slots (simulated data)"
        }

    def _fallback_create_event(self):
        """Fallback create event when real calendar API is unavailable"""
        return {
            "success": True,
            "agent": self.name,
            "action": "create_event",
            "event_id": f"sim_{datetime.now().timestamp()}",
            "title": "New Event",
            "source": "simulated",
            "message": "Event created (simulated - calendar API not available)"
        }
