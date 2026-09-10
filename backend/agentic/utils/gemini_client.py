"""
Gemini LLM Client - for conversational AI and intent classification
Using the new google.genai package (google.generativeai is deprecated)
"""
import os
import logging
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)

# Try to import new Gemini package
GEMINI_AVAILABLE = False
genai = None

try:
    from google import genai as google_genai
    genai = google_genai
    GEMINI_AVAILABLE = True
    logger.info("Using new google.genai package")
except ImportError:
    try:
        import google.generativeai as old_genai
        genai = old_genai
        GEMINI_AVAILABLE = True
        logger.info("Falling back to deprecated google.generativeai package")
    except ImportError:
        logger.warning("No Gemini package available")

# Model configuration - use 'gemini-flash-latest' for free tier compatibility
MODEL_NAME = os.getenv('AI_MODEL', 'gemini-flash-latest')
TEMPERATURE = float(os.getenv('AI_TEMPERATURE', '0.7'))
MAX_TOKENS = int(os.getenv('AI_MAX_TOKENS', '4000'))


class GeminiClient:
    """Client for Gemini LLM interactions"""

    def __init__(self):
        self.client = None
        self.model_name = MODEL_NAME
        self.chat_sessions: Dict[str, Any] = {}

        # Get API key from environment
        from dotenv import load_dotenv
        load_dotenv()

        api_key = os.getenv('GOOGLE_API_KEY')

        if not api_key:
            logger.error("No GOOGLE_API_KEY found in environment")
            return

        try:
            # Try new google.genai package first
            from google import genai as new_genai
            self.client = new_genai.Client(api_key=api_key)
            self.use_new_api = True
            logger.info(f"Gemini client initialized with new API, model: {self.model_name}")
        except Exception as e:
            logger.warning(f"New API failed: {e}, trying old API")
            try:
                import google.generativeai as old_genai
                old_genai.configure(api_key=api_key)
                self.client = old_genai.GenerativeModel(self.model_name)
                self.use_new_api = False
                logger.info(f"Gemini client initialized with old API, model: {self.model_name}")
            except Exception as e2:
                logger.error(f"Both APIs failed: {e2}")
                self.client = None

    def _generate(self, prompt: str) -> str:
        """Generate content using whichever API is available"""
        if self.client is None:
            return "AI model not available. Please check your GOOGLE_API_KEY configuration."

        try:
            if self.use_new_api:
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=prompt
                )
                return response.text
            else:
                response = self.client.generate_content(prompt)
                return response.text
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Generation error: {error_msg}")
            if "404" in error_msg:
                return f"Model '{self.model_name}' not found. Please update AI_MODEL in your .env file."
            elif "429" in error_msg:
                return "API quota exceeded. Please check your Google AI billing/quota."
            elif "401" in error_msg or "403" in error_msg:
                return "Invalid API key. Please check your GOOGLE_API_KEY in .env file."
            return f"Error: {error_msg[:100]}"

    def classify_query_intent(self, query: str, available_agents: List[str]) -> Dict[str, Any]:
        """
        Classify user query to determine if it needs an agent or can be handled conversationally.
        """
        # Use simple keyword-based classification as fallback
        action_keywords = {
            'calendar': ['calendar', 'schedule', 'meeting', 'appointment', 'event', 'book', 'reschedule'],
            'email': ['email', 'mail', 'inbox', 'send', 'compose', 'reply'],
            'weather': ['weather', 'temperature', 'forecast', 'rain', 'sunny', 'cold', 'hot'],
            'news': ['news', 'headlines', 'latest', 'happening'],
            'task': ['task', 'todo', 'reminder', 'to-do', 'to do'],
            'meeting': ['meet', 'google meet', 'video call', 'conference']
        }

        query_lower = query.lower()

        # Check for action keywords
        needs_agent = False
        matched_agents = []

        for agent_type, keywords in action_keywords.items():
            if any(kw in query_lower for kw in keywords):
                needs_agent = True
                matched_agents.append(agent_type)

        # If no agent keywords found, it's conversational
        if not needs_agent:
            return {
                "needs_agent": False,
                "agent_types": [],
                "confidence": 0.9,
                "reasoning": "General conversational query"
            }

        return {
            "needs_agent": True,
            "agent_types": matched_agents,
            "confidence": 0.85,
            "reasoning": f"Detected action keywords for: {', '.join(matched_agents)}"
        }

    def chat(self, query: str, context: Optional[Dict[str, Any]] = None, user_id: str = "default") -> str:
        """Have a conversational interaction with the LLM."""
        if self.client is None:
            return self._fallback_response(query)

        system_prompt = """You are CoreAI, a helpful and friendly AI assistant. You are part of a multi-agent system that can help with:
- Calendar management and scheduling
- Email handling
- Weather information
- News updates
- Task management
- Google Meet meetings

For general questions, explanations, calculations, or conversation - respond directly and helpfully.
Keep responses concise but friendly. Use markdown formatting when appropriate."""

        full_prompt = f"{system_prompt}\n\nUser: {query}\n\nAssistant:"

        response = self._generate(full_prompt)

        # If API failed, use fallback
        if response.startswith("API quota exceeded") or response.startswith("Error:") or response.startswith("Model '"):
            return self._fallback_response(query)

        return response

    def _fallback_response(self, query: str) -> str:
        """Provide basic responses when Gemini API is not available"""
        query_lower = query.lower().strip()

        # Greetings
        if any(g in query_lower for g in ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening']):
            return "Hello! I'm CoreAI, your personal assistant. I can help you with:\n\n- **Calendar** - Schedule meetings, check availability\n- **Email** - Read and manage your emails\n- **Weather** - Get weather forecasts\n- **News** - Get latest headlines\n- **Tasks** - Manage your to-do list\n\nWhat would you like to do?"

        # How are you
        if 'how are you' in query_lower:
            return "I'm doing well, thank you for asking! I'm here and ready to help. What can I do for you today?"

        # What can you do
        if any(p in query_lower for p in ['what can you do', 'help me', 'capabilities', 'what do you do']):
            return """I'm CoreAI, your multi-agent assistant! Here's what I can help with:

### 📅 Calendar
- Schedule meetings and appointments
- Check your availability
- View upcoming events

### 📧 Email
- Read your inbox
- Send emails
- Search for specific messages

### 🌤️ Weather
- Current conditions
- Forecasts

### 📰 News
- Latest headlines
- Topic-specific news

### ✅ Tasks
- Create and manage to-do items
- Set reminders

Just ask me something like "Show my calendar" or "What's the weather?"!"""

        # Simple math
        if any(op in query_lower for op in ['+', '-', '*', '/', 'plus', 'minus', 'times', 'divided']):
            try:
                # Simple calculator
                import re
                query_clean = query_lower.replace('what is', '').replace('calculate', '').replace('?', '')
                query_clean = query_clean.replace('plus', '+').replace('minus', '-').replace('times', '*').replace('divided by', '/')
                numbers = re.findall(r'[\d\+\-\*\/\.\s\(\)]+', query_clean)
                if numbers:
                    result = eval(numbers[0].strip())
                    return f"The answer is **{result}**"
            except:
                pass

        # Default response
        return """I understand you're asking something, but I'm currently running in limited mode.

You can try asking me to:
- "Show my calendar"
- "Check my emails"
- "What's the weather?"
- "Show latest news"
- "Schedule a meeting for tomorrow at 3pm"

Or I can help if you enable full AI capabilities by setting up your Google AI API quota at [Google AI Studio](https://ai.google.dev)."""

    def extract_datetime_from_query(self, query: str, reference_date: Optional[str] = None) -> Dict[str, Any]:
        """Extract date and time information from natural language query."""
        from datetime import datetime, timedelta

        now = datetime.now()
        query_lower = query.lower()

        result = {
            "has_datetime": False,
            "date": "",
            "time": "09:00",
            "end_time": "10:00",
            "duration_hours": 1.0,
            "description": "Meeting",
            "confidence": 0.7
        }

        # Simple day parsing
        if "tomorrow" in query_lower:
            target_date = now + timedelta(days=1)
            result["has_datetime"] = True
            result["date"] = target_date.strftime("%Y-%m-%d")
        elif "today" in query_lower:
            result["has_datetime"] = True
            result["date"] = now.strftime("%Y-%m-%d")
        elif "next" in query_lower:
            # Parse "next Monday", "next Saturday", etc.
            days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
            for i, day in enumerate(days):
                if day in query_lower:
                    current_day = now.weekday()
                    days_ahead = i - current_day
                    if days_ahead <= 0:
                        days_ahead += 7
                    target_date = now + timedelta(days=days_ahead)
                    result["has_datetime"] = True
                    result["date"] = target_date.strftime("%Y-%m-%d")
                    break

        # Simple time parsing
        if "morning" in query_lower:
            result["time"] = "09:00"
            result["end_time"] = "10:00"
        elif "afternoon" in query_lower:
            result["time"] = "14:00"
            result["end_time"] = "15:00"
        elif "evening" in query_lower:
            result["time"] = "18:00"
            result["end_time"] = "19:00"

        # Try to find specific times like "3pm", "10am", "15:00"
        import re
        time_patterns = [
            r'(\d{1,2})\s*(?::|\.)?(\d{2})?\s*(am|pm)',
            r'(\d{1,2})\s*(am|pm)',
            r'at\s+(\d{1,2}):(\d{2})',
        ]

        for pattern in time_patterns:
            match = re.search(pattern, query_lower)
            if match:
                groups = match.groups()
                hour = int(groups[0])
                minute = int(groups[1]) if groups[1] and groups[1].isdigit() else 0

                # Handle AM/PM
                if len(groups) > 1 and groups[-1] in ['pm', 'am']:
                    if groups[-1] == 'pm' and hour < 12:
                        hour += 12
                    elif groups[-1] == 'am' and hour == 12:
                        hour = 0

                result["time"] = f"{hour:02d}:{minute:02d}"
                result["end_time"] = f"{(hour + 1) % 24:02d}:{minute:02d}"
                result["has_datetime"] = True
                break

        # Extract description
        desc_patterns = [
            r'(?:schedule|book|create)\s+(?:a\s+)?(.+?)(?:\s+(?:for|on|at|tomorrow|today|next))',
            r'(?:meeting|call|appointment)\s+(?:with|about|for)\s+(.+?)(?:\s+(?:on|at|tomorrow))?$',
        ]

        for pattern in desc_patterns:
            match = re.search(pattern, query_lower)
            if match:
                result["description"] = match.group(1).strip().title()
                break

        return result

    def clear_chat_history(self, user_id: str = "default"):
        """Clear chat history for a user"""
        if user_id in self.chat_sessions:
            del self.chat_sessions[user_id]


# Global instance
_gemini_client = None

def get_gemini_client() -> GeminiClient:
    """Get the global Gemini client instance"""
    global _gemini_client
    if _gemini_client is None:
        _gemini_client = GeminiClient()
    return _gemini_client
