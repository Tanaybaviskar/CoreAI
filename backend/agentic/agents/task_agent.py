"""
Task Agent - Manages tasks and to-do lists
"""
from typing import Dict, Any, List
from datetime import datetime
import os
from .base_agent import BaseAgent, logger


class TaskAgent(BaseAgent):
    """Agent specialized in task management"""

    def __init__(self):
        super().__init__(
            name="Task Agent",
            description="Manages tasks, to-do lists, and reminders"
        )
        # Store tasks in memory (in real implementation, use database)
        self.tasks: List[Dict[str, Any]] = []

    def can_handle(self, task: str) -> bool:
        """Check if this agent can handle the task"""
        task_keywords = [
            "task", "todo", "to-do", "reminder", "checklist",
            "add task", "complete task", "list tasks"
        ]
        task_lower = task.lower()
        return any(keyword in task_lower for keyword in task_keywords)

    async def execute(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute task-related operations"""
        self.update_status("thinking", "Processing task request")

        try:
            task_lower = task.lower()

            if "add" in task_lower or "create" in task_lower:
                result = await self._add_task(context)
            elif "complete" in task_lower or "done" in task_lower or "finish" in task_lower:
                result = await self._complete_task(context)
            elif "list" in task_lower or "show" in task_lower:
                result = await self._list_tasks(context)
            elif "delete" in task_lower or "remove" in task_lower:
                result = await self._delete_task(context)
            else:
                result = await self._list_tasks(context)

            self.record_success()
            return result

        except Exception as e:
            self.record_failure(str(e))
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to process task request"
            }

    async def _add_task(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Add a new task"""
        self.update_status("active", "Adding new task")

        title = context.get("title", "New Task")
        description = context.get("description", "")
        priority = context.get("priority", "medium")
        due_date = context.get("due_date")

        new_task = {
            "id": f"task_{len(self.tasks) + 1}",
            "title": title,
            "description": description,
            "priority": priority,
            "due_date": due_date,
            "completed": False,
            "created_at": datetime.now().isoformat()
        }

        self.tasks.append(new_task)

        return {
            "success": True,
            "agent": self.name,
            "action": "add_task",
            "task": new_task,
            "message": f"Added task: {title}"
        }

    async def _complete_task(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Mark a task as completed"""
        self.update_status("active", "Completing task")

        task_id = context.get("task_id")

        for task in self.tasks:
            if task["id"] == task_id:
                task["completed"] = True
                task["completed_at"] = datetime.now().isoformat()
                return {
                    "success": True,
                    "agent": self.name,
                    "action": "complete_task",
                    "task": task,
                    "message": f"Task completed: {task['title']}"
                }

        return {
            "success": False,
            "agent": self.name,
            "action": "complete_task",
            "message": "Task not found"
        }

    async def _list_tasks(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """List all tasks"""
        self.update_status("active", "Listing tasks")

        show_completed = context.get("show_completed", False)

        if show_completed:
            tasks = self.tasks
        else:
            tasks = [t for t in self.tasks if not t["completed"]]

        # Add some default tasks if empty
        if not tasks:
            tasks = [
                {
                    "id": "task_1",
                    "title": "Review project documentation",
                    "priority": "high",
                    "completed": False,
                    "created_at": datetime.now().isoformat()
                },
                {
                    "id": "task_2",
                    "title": "Prepare presentation slides",
                    "priority": "medium",
                    "completed": False,
                    "created_at": datetime.now().isoformat()
                }
            ]

        return {
            "success": True,
            "agent": self.name,
            "action": "list_tasks",
            "tasks": tasks,
            "total": len(tasks),
            "message": f"You have {len(tasks)} {'pending ' if not show_completed else ''}tasks"
        }

    async def _delete_task(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Delete a task"""
        self.update_status("active", "Deleting task")

        task_id = context.get("task_id")

        for i, task in enumerate(self.tasks):
            if task["id"] == task_id:
                deleted_task = self.tasks.pop(i)
                return {
                    "success": True,
                    "agent": self.name,
                    "action": "delete_task",
                    "task": deleted_task,
                    "message": f"Task deleted: {deleted_task['title']}"
                }

        return {
            "success": False,
            "agent": self.name,
            "action": "delete_task",
            "message": "Task not found"
        }
