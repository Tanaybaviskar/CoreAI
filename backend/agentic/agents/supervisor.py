"""
Supervisor Agent - Coordinates all specialized agents
"""
from typing import Dict, Any, List, Optional
from datetime import datetime
import asyncio
import sys
from pathlib import Path
from .base_agent import BaseAgent, logger
from .calendar_agent import CalendarAgent
from .meeting_agent import MeetingAgent
from .email_agent import EmailAgent
from .info_agents import WeatherAgent, NewsAgent
from .task_agent import TaskAgent

# Add utils to path
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.gemini_client import get_gemini_client


class SupervisorAgent:
    """
    Supervisor agent that coordinates multiple specialized agents.
    Uses a hierarchical approach where the supervisor delegates tasks
    to the most appropriate specialized agent.
    """

    def __init__(self):
        self.name = "Supervisor"
        self.agents: List[BaseAgent] = [
            CalendarAgent(),
            MeetingAgent(),
            EmailAgent(),
            WeatherAgent(),
            NewsAgent(),
            TaskAgent(),
        ]
        self.conversation_history: List[Dict[str, Any]] = []
        self.gemini = get_gemini_client()

    async def process_request(self, user_message: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Process user request by:
        1. Using LLM to classify query intent
        2. Determining if an agent is needed or if it's conversational
        3. Coordinating execution appropriately
        4. Returning consolidated response
        """
        if context is None:
            context = {}

        logger.info(f"[Supervisor] Processing request: {user_message}")

        # Record conversation
        self.conversation_history.append({
            "timestamp": datetime.now().isoformat(),
            "role": "user",
            "content": user_message
        })

        # Use LLM to classify query intent
        agent_names = [agent.name for agent in self.agents]
        classification = self.gemini.classify_query_intent(user_message, agent_names)

        logger.info(f"[Supervisor] Classification: {classification}")

        # If it's a general query (no agent needed), handle conversationally
        if not classification["needs_agent"]:
            result = await self._handle_general_query(user_message, context)
        else:
            # Find capable agents based on both LLM classification and agent's own can_handle
            capable_agents = []
            for agent in self.agents:
                if agent.can_handle(user_message):
                    capable_agents.append(agent)
                    logger.info(f"[Supervisor] Agent {agent.name} can handle this request")

            if not capable_agents:
                # LLM thinks we need an agent but none matched - still handle conversationally
                logger.info("[Supervisor] No agent matched, falling back to conversational response")
                result = await self._handle_general_query(user_message, context)
            elif len(capable_agents) == 1:
                # Single agent can handle it
                result = await self._execute_single_agent(capable_agents[0], user_message, context)
            else:
                # Multiple agents might be needed (complex task)
                result = await self._execute_complex_task(capable_agents, user_message, context)

        # Record response
        self.conversation_history.append({
            "timestamp": datetime.now().isoformat(),
            "role": "assistant",
            "content": result
        })

        return result

    async def _execute_single_agent(self, agent: BaseAgent, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute task with a single agent"""
        logger.info(f"[Supervisor] Delegating to {agent.name}")

        try:
            result = await agent.execute(task, context)
            return {
                "success": True,
                "agent": agent.name,
                "result": result,
                "message": result.get("message", "Task completed"),
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"[Supervisor] Error with {agent.name}: {str(e)}")
            return {
                "success": False,
                "agent": agent.name,
                "error": str(e),
                "message": f"Failed to complete task with {agent.name}",
                "timestamp": datetime.now().isoformat()
            }

    async def _execute_complex_task(self, agents: List[BaseAgent], task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute complex task that might require multiple agents.
        Example: "Schedule a meeting" requires both Calendar and Meeting agents
        """
        logger.info(f"[Supervisor] Complex task detected, coordinating {len(agents)} agents")

        # Special case: Calendar + Meeting coordination
        if any(isinstance(a, CalendarAgent) for a in agents) and any(isinstance(a, MeetingAgent) for a in agents):
            return await self._coordinate_meeting_scheduling(agents, task, context)

        # For other cases, execute in sequence
        results = []
        for agent in agents:
            try:
                result = await agent.execute(task, context)
                results.append(result)
            except Exception as e:
                logger.error(f"[Supervisor] Error with {agent.name}: {str(e)}")

        return {
            "success": True,
            "agents": [a.name for a in agents],
            "results": results,
            "message": "Complex task completed with multiple agents",
            "timestamp": datetime.now().isoformat()
        }

    async def _coordinate_meeting_scheduling(self, agents: List[BaseAgent], task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Coordinate meeting scheduling:
        1. Calendar Agent checks availability
        2. Meeting Agent creates Google Meet link
        3. Calendar Agent books the time slot
        """
        logger.info("[Supervisor] Coordinating meeting scheduling workflow")

        calendar_agent = next((a for a in agents if isinstance(a, CalendarAgent)), None)
        meeting_agent = next((a for a in agents if isinstance(a, MeetingAgent)), None)

        if not calendar_agent or not meeting_agent:
            return {"success": False, "message": "Required agents not available"}

        workflow_steps = []

        # Step 1: Check calendar availability
        logger.info("[Supervisor] Step 1: Checking calendar availability")
        availability = await calendar_agent.execute("check availability", context)
        workflow_steps.append({
            "step": 1,
            "agent": calendar_agent.name,
            "action": "check_availability",
            "result": availability
        })

        if not availability.get("success"):
            return {
                "success": False,
                "workflow": workflow_steps,
                "message": "Failed to check calendar availability"
            }

        # Step 2: Create Google Meet link
        logger.info("[Supervisor] Step 2: Creating Google Meet link")
        meeting_result = await meeting_agent.execute("create meeting", context)
        workflow_steps.append({
            "step": 2,
            "agent": meeting_agent.name,
            "action": "create_meeting",
            "result": meeting_result
        })

        # Step 3: Book the time slot in calendar
        if meeting_result.get("success"):
            logger.info("[Supervisor] Step 3: Booking calendar slot")
            booking_context = {
                **context,
                "meeting_link": meeting_result.get("meeting_link"),
                "meeting_id": meeting_result.get("meeting_id")
            }
            booking = await calendar_agent.execute("create event", booking_context)
            workflow_steps.append({
                "step": 3,
                "agent": calendar_agent.name,
                "action": "book_slot",
                "result": booking
            })

        # Compile final response
        return {
            "success": True,
            "workflow": "meeting_scheduling",
            "steps": workflow_steps,
            "meeting_link": meeting_result.get("meeting_link"),
            "event_id": booking.get("event_id") if 'booking' in locals() else None,
            "message": "Successfully coordinated meeting scheduling across agents",
            "timestamp": datetime.now().isoformat()
        }

    async def _handle_general_query(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle general queries using Gemini LLM for conversation"""
        logger.info("[Supervisor] Handling as general conversational query")

        try:
            # Get user ID for chat history
            user_id = context.get('user_email', 'default')

            # Get conversational response from Gemini
            response_text = self.gemini.chat(query, context, user_id)

            return {
                "success": True,
                "agent": "CoreAI Assistant",
                "message": response_text,
                "type": "conversational",
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"[Supervisor] Error in general query handling: {str(e)}")
            return {
                "success": False,
                "agent": "Supervisor",
                "message": f"I apologize, but I encountered an error: {str(e)}. Please try again.",
                "timestamp": datetime.now().isoformat()
            }

    def get_all_agents_status(self) -> List[Dict[str, Any]]:
        """Get status of all agents"""
        return [agent.get_info() for agent in self.agents]

    def get_agent_by_name(self, name: str) -> Optional[BaseAgent]:
        """Get specific agent by name"""
        for agent in self.agents:
            if agent.name.lower() == name.lower():
                return agent
        return None
