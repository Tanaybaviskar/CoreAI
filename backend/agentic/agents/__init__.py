"""
Agent package - Multi-agent system for CoreAI
"""
from .base_agent import BaseAgent
from .calendar_agent import CalendarAgent
from .meeting_agent import MeetingAgent
from .email_agent import EmailAgent
from .info_agents import WeatherAgent, NewsAgent
from .task_agent import TaskAgent
from .supervisor import SupervisorAgent

__all__ = [
    'BaseAgent',
    'CalendarAgent',
    'MeetingAgent',
    'EmailAgent',
    'WeatherAgent',
    'NewsAgent',
    'TaskAgent',
    'SupervisorAgent',
]
