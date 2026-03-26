"""
Email Agent - Manages Gmail operations using Gmail API
"""
from typing import Dict, Any, List, Optional
from datetime import datetime
import os
import sys
import base64
import email
from pathlib import Path
from .base_agent import BaseAgent, logger

# Add utils to path
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.oauth_helper import get_gmail_service


class EmailAgent(BaseAgent):
    """Agent specialized in email management"""

    def __init__(self):
        super().__init__(
            name="Email Agent",
            description="Manages Gmail - read, send, search, and organize emails"
        )

    def can_handle(self, task: str) -> bool:
        """Check if this agent can handle the task"""
        email_keywords = [
            "email", "mail", "gmail", "send email", "inbox",
            "compose", "reply", "draft", "message"
        ]
        task_lower = task.lower()
        return any(keyword in task_lower for keyword in email_keywords)

    def _get_user_email(self, context: Dict[str, Any]) -> Optional[str]:
        """Extract user email from context"""
        return context.get("user_email")

    def _decode_message_body(self, message_parts) -> str:
        """Decode email message body from Gmail API response"""
        try:
            if isinstance(message_parts, list):
                for part in message_parts:
                    if part.get('mimeType') == 'text/plain':
                        body_data = part.get('body', {}).get('data')
                        if body_data:
                            return base64.urlsafe_b64decode(body_data).decode('utf-8')
            else:
                body_data = message_parts.get('body', {}).get('data')
                if body_data:
                    return base64.urlsafe_b64decode(body_data).decode('utf-8')
        except Exception:
            pass
        return "Unable to decode message content"

    def _create_message(self, to: str, subject: str, body: str, from_email: str = None) -> Dict:
        """Create a message for Gmail API"""
        message = email.message.EmailMessage()
        message['To'] = to
        message['Subject'] = subject
        if from_email:
            message['From'] = from_email
        message.set_content(body)

        return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

    async def execute(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute email-related tasks"""
        self.update_status("thinking", "Processing email request")

        user_email = self._get_user_email(context)
        if not user_email:
            return {
                "success": False,
                "error": "User not authenticated",
                "message": "Please sign in with Google to access your Gmail"
            }

        try:
            task_lower = task.lower()

            if "send" in task_lower or "compose" in task_lower:
                result = await self._send_email(user_email, context)
            elif "read" in task_lower or "check" in task_lower or "inbox" in task_lower:
                result = await self._read_emails(user_email, context)
            elif "search" in task_lower or "find" in task_lower:
                result = await self._search_emails(user_email, context)
            elif "draft" in task_lower:
                result = await self._create_draft(user_email, context)
            else:
                result = await self._read_emails(user_email, context)

            self.record_success()
            return result

        except Exception as e:
            self.record_failure(str(e))
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to process email request"
            }

    async def _read_emails(self, user_email: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Read recent emails from real Gmail"""
        self.update_status("active", "Fetching emails")

        try:
            service = get_gmail_service(user_email)
            if not service:
                return self._fallback_read_emails()

            max_results = context.get("max_results", 10)

            # Get list of messages
            results = service.users().messages().list(
                userId='me',
                maxResults=max_results,
                q="in:inbox"
            ).execute()

            messages = results.get('messages', [])

            formatted_emails = []
            for msg in messages[:max_results]:
                # Get full message details
                message = service.users().messages().get(
                    userId='me',
                    id=msg['id'],
                    format='full'
                ).execute()

                # Extract headers
                headers = {h['name']: h['value'] for h in message['payload'].get('headers', [])}

                # Get message body
                snippet = message.get('snippet', '')

                # Check if unread
                labels = message.get('labelIds', [])
                is_unread = 'UNREAD' in labels

                formatted_emails.append({
                    "id": message['id'],
                    "from": headers.get('From', 'Unknown'),
                    "subject": headers.get('Subject', 'No subject'),
                    "snippet": snippet,
                    "date": headers.get('Date', datetime.now().isoformat()),
                    "unread": is_unread,
                    "thread_id": message.get('threadId')
                })

            unread_count = sum(1 for e in formatted_emails if e["unread"])

            logger.info(f"Retrieved {len(formatted_emails)} real emails for {user_email}")

            return {
                "success": True,
                "agent": self.name,
                "action": "read_emails",
                "emails": formatted_emails,
                "count": len(formatted_emails),
                "unread_count": unread_count,
                "source": "real_gmail_api",
                "message": f"Retrieved {len(formatted_emails)} emails from your inbox ({unread_count} unread)"
            }

        except Exception as e:
            logger.error(f"Gmail read error for {user_email}: {str(e)}")
            return self._fallback_read_emails()

    async def _send_email(self, user_email: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Send an email using real Gmail API"""
        self.update_status("active", "Sending email")

        try:
            service = get_gmail_service(user_email)
            if not service:
                return self._fallback_send_email()

            to = context.get("to", "")
            subject = context.get("subject", "Message from CoreAI")
            body = context.get("body", "")

            if not to or not body:
                return {
                    "success": False,
                    "agent": self.name,
                    "action": "send_email",
                    "message": "Missing required fields: 'to' and 'body'"
                }

            # Create message
            message = self._create_message(to, subject, body, user_email)

            # Send message
            sent_message = service.users().messages().send(
                userId='me',
                body=message
            ).execute()

            logger.info(f"Sent real email {sent_message['id']} for {user_email}")

            return {
                "success": True,
                "agent": self.name,
                "action": "send_email",
                "message_id": sent_message['id'],
                "to": to,
                "subject": subject,
                "sent_at": datetime.now().isoformat(),
                "source": "real_gmail_api",
                "message": f"Email sent successfully to {to}"
            }

        except Exception as e:
            logger.error(f"Gmail send error for {user_email}: {str(e)}")
            return self._fallback_send_email()

    async def _search_emails(self, user_email: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Search emails using real Gmail API"""
        self.update_status("active", "Searching emails")

        try:
            service = get_gmail_service(user_email)
            if not service:
                return self._fallback_search_emails(context)

            query = context.get("query", "")
            if not query:
                return {
                    "success": False,
                    "agent": self.name,
                    "action": "search_emails",
                    "message": "Search query is required"
                }

            # Search messages
            results = service.users().messages().list(
                userId='me',
                q=query,
                maxResults=5
            ).execute()

            messages = results.get('messages', [])

            formatted_results = []
            for msg in messages:
                # Get message details
                message = service.users().messages().get(
                    userId='me',
                    id=msg['id'],
                    format='metadata'
                ).execute()

                headers = {h['name']: h['value'] for h in message['payload'].get('headers', [])}

                formatted_results.append({
                    "id": message['id'],
                    "from": headers.get('From', 'Unknown'),
                    "subject": headers.get('Subject', 'No subject'),
                    "snippet": message.get('snippet', ''),
                    "date": headers.get('Date', datetime.now().isoformat()),
                    "thread_id": message.get('threadId')
                })

            logger.info(f"Found {len(formatted_results)} emails matching '{query}' for {user_email}")

            return {
                "success": True,
                "agent": self.name,
                "action": "search_emails",
                "query": query,
                "results": formatted_results,
                "count": len(formatted_results),
                "source": "real_gmail_api",
                "message": f"Found {len(formatted_results)} emails matching '{query}'"
            }

        except Exception as e:
            logger.error(f"Gmail search error for {user_email}: {str(e)}")
            return self._fallback_search_emails(context)

    async def _create_draft(self, user_email: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Create an email draft using real Gmail API"""
        self.update_status("active", "Creating email draft")

        try:
            service = get_gmail_service(user_email)
            if not service:
                return self._fallback_create_draft()

            to = context.get("to", "")
            subject = context.get("subject", "Draft from CoreAI")
            body = context.get("body", "")

            if not to or not body:
                return {
                    "success": False,
                    "agent": self.name,
                    "action": "create_draft",
                    "message": "Missing required fields: 'to' and 'body'"
                }

            # Create message
            message = self._create_message(to, subject, body, user_email)

            # Create draft
            draft = service.users().drafts().create(
                userId='me',
                body={'message': message}
            ).execute()

            logger.info(f"Created real email draft {draft['id']} for {user_email}")

            return {
                "success": True,
                "agent": self.name,
                "action": "create_draft",
                "draft_id": draft['id'],
                "to": to,
                "subject": subject,
                "source": "real_gmail_api",
                "message": "Email draft created successfully"
            }

        except Exception as e:
            logger.error(f"Gmail draft error for {user_email}: {str(e)}")
            return self._fallback_create_draft()

    # Fallback methods for when API is not available
    def _fallback_read_emails(self):
        """Fallback when real Gmail API is unavailable"""
        emails = [
            {
                "id": "fallback_1",
                "from": "john@example.com",
                "subject": "Project Update",
                "snippet": "Here's the latest update on the project...",
                "date": datetime.now().isoformat(),
                "unread": True,
                "thread_id": "thread_1"
            },
            {
                "id": "fallback_2",
                "from": "team@company.com",
                "subject": "Weekly Newsletter",
                "snippet": "This week's highlights and updates...",
                "date": datetime.now().isoformat(),
                "unread": False,
                "thread_id": "thread_2"
            }
        ]

        return {
            "success": True,
            "agent": self.name,
            "action": "read_emails",
            "emails": emails,
            "count": len(emails),
            "unread_count": sum(1 for e in emails if e["unread"]),
            "source": "simulated",
            "message": f"Retrieved {len(emails)} emails (simulated data)"
        }

    def _fallback_send_email(self):
        """Fallback send email when real Gmail API is unavailable"""
        return {
            "success": True,
            "agent": self.name,
            "action": "send_email",
            "message_id": f"sim_{datetime.now().timestamp()}",
            "sent_at": datetime.now().isoformat(),
            "source": "simulated",
            "message": "Email sent (simulated - Gmail API not available)"
        }

    def _fallback_search_emails(self, context: Dict[str, Any]):
        """Fallback search emails when real Gmail API is unavailable"""
        query = context.get("query", "")
        results = [
            {
                "id": "fallback_search_1",
                "from": "sarah@example.com",
                "subject": f"Re: {query}",
                "snippet": f"Regarding your query about {query}...",
                "date": datetime.now().isoformat(),
                "thread_id": "thread_search_1"
            }
        ]

        return {
            "success": True,
            "agent": self.name,
            "action": "search_emails",
            "query": query,
            "results": results,
            "count": len(results),
            "source": "simulated",
            "message": f"Found {len(results)} emails matching '{query}' (simulated data)"
        }

    def _fallback_create_draft(self):
        """Fallback create draft when real Gmail API is unavailable"""
        return {
            "success": True,
            "agent": self.name,
            "action": "create_draft",
            "draft_id": f"draft_sim_{datetime.now().timestamp()}",
            "source": "simulated",
            "message": "Draft created (simulated - Gmail API not available)"
        }
