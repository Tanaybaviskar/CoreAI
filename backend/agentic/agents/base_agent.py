"""
Base Agent class that all specialized agents inherit from.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """Base class for all specialized agents"""

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.status = "idle"  # idle, active, thinking, error
        self.last_action = "Ready"
        self.success_count = 0
        self.failure_count = 0
        self.created_at = datetime.now()

    @abstractmethod
    async def execute(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the agent's primary task.

        Args:
            task: The task description
            context: Additional context and parameters

        Returns:
            Dict containing the result and any metadata
        """
        pass

    @abstractmethod
    def can_handle(self, task: str) -> bool:
        """
        Determine if this agent can handle the given task.

        Args:
            task: The task description

        Returns:
            Boolean indicating if the agent can handle this task
        """
        pass

    def update_status(self, status: str, action: Optional[str] = None):
        """Update agent status and last action"""
        self.status = status
        if action:
            self.last_action = action
        logger.info(f"[{self.name}] Status: {status} - {self.last_action}")

    def record_success(self):
        """Record a successful execution"""
        self.success_count += 1
        self.update_status("idle", "Task completed successfully")

    def record_failure(self, error: str):
        """Record a failed execution"""
        self.failure_count += 1
        self.update_status("error", f"Error: {error}")

    def get_success_rate(self) -> float:
        """Calculate success rate percentage"""
        total = self.success_count + self.failure_count
        if total == 0:
            return 100.0
        return round((self.success_count / total) * 100, 1)

    def get_info(self) -> Dict[str, Any]:
        """Get agent information"""
        return {
            "name": self.name,
            "description": self.description,
            "status": self.status,
            "last_action": self.last_action,
            "success_rate": self.get_success_rate(),
            "total_tasks": self.success_count + self.failure_count
        }
