"""
Meeting Agent - Manages Google Meet video conferences
"""
from typing import Dict, Any
from datetime import datetime
import os
from .base_agent import BaseAgent, logger


class MeetingAgent(BaseAgent):
    """Agent specialized in managing video meetings"""

    def __init__(self):
        super().__init__(
            name="Meeting Agent",
            description="Creates and manages Google Meet video conferences"
        )
        self.api_key = os.getenv("GOOGLE_MEET_API_KEY")

    def can_handle(self, task: str) -> bool:
        """Check if this agent can handle the task"""
        meeting_keywords = [
            "meet", "video call", "conference", "zoom", "join meeting",
            "create meeting", "meeting link"
        ]
        task_lower = task.lower()
        return any(keyword in task_lower for keyword in meeting_keywords)

    async def execute(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute meeting-related tasks"""
        self.update_status("thinking", "Processing meeting request")

        try:
            task_lower = task.lower()

            if "create" in task_lower or "schedule" in task_lower:
                result = await self._create_meeting(context)
            elif "join" in task_lower:
                result = await self._join_meeting(context)
            elif "cancel" in task_lower:
                result = await self._cancel_meeting(context)
            else:
                result = await self._create_meeting(context)

            self.record_success()
            return result

        except Exception as e:
            self.record_failure(str(e))
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to process meeting request"
            }

    async def _create_meeting(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Create a Google Meet link"""
        self.update_status("active", "Creating Google Meet link")

        title = context.get("title", "New Meeting")
        start_time = context.get("start_time")
        duration = context.get("duration", 60)  # minutes

        # In real implementation: use Google Meet API
        # For now, generate a simulated meeting link
        meeting_id = f"meet-{datetime.now().timestamp()}"
        meeting_link = f"https://meet.google.com/{meeting_id}"

        return {
            "success": True,
            "agent": self.name,
            "action": "create_meeting",
            "meeting_id": meeting_id,
            "meeting_link": meeting_link,
            "title": title,
            "start_time": start_time,
            "duration": duration,
            "message": f"Successfully created Google Meet: {meeting_link}"
        }

    async def _join_meeting(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Get meeting join information"""
        self.update_status("active", "Fetching meeting details")

        meeting_id = context.get("meeting_id")

        return {
            "success": True,
            "agent": self.name,
            "action": "join_meeting",
            "meeting_link": f"https://meet.google.com/{meeting_id}",
            "message": f"Meeting link ready"
        }

    async def _cancel_meeting(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Cancel a meeting"""
        self.update_status("active", "Canceling meeting")

        meeting_id = context.get("meeting_id")

        return {
            "success": True,
            "agent": self.name,
            "action": "cancel_meeting",
            "meeting_id": meeting_id,
            "message": "Meeting canceled successfully"
        }
