"""
Task Agent - Manages tasks and to-do lists (persisted in the database)
"""
from typing import Dict, Any
from datetime import datetime
from .base_agent import BaseAgent, logger
from database import get_session, Task


class TaskAgent(BaseAgent):
    """Agent specialized in task management. Backed by the `tasks` DB table."""

    def __init__(self):
        super().__init__(
            name="Task Agent",
            description="Manages tasks, to-do lists, and reminders"
        )

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

    @staticmethod
    def _serialize(task: Task) -> Dict[str, Any]:
        return {
            "id": task.id,
            "title": task.title,
            "completed": task.is_complete,
            "created_at": task.created_at.isoformat() if task.created_at else None,
            "completed_at": task.completed_at.isoformat() if task.completed_at else None,
        }

    async def _add_task(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Add a new task, persisted to the DB"""
        self.update_status("active", "Adding new task")

        title = context.get("title", "New Task")
        thread_id = context.get("thread_id", "default")

        with get_session() as db:
            new_task = Task(thread_id=thread_id, title=title)
            db.add(new_task)
            db.flush()  # populate new_task.id before commit
            serialized = self._serialize(new_task)

        return {
            "success": True,
            "agent": self.name,
            "action": "add_task",
            "task": serialized,
            "message": f"Added task: {title}"
        }

    async def _complete_task(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Mark a task as completed"""
        self.update_status("active", "Completing task")

        task_id = context.get("task_id")

        with get_session() as db:
            task = db.query(Task).filter(Task.id == task_id).first()
            if not task:
                return {
                    "success": False,
                    "agent": self.name,
                    "action": "complete_task",
                    "message": "Task not found"
                }
            task.is_complete = True
            task.completed_at = datetime.utcnow()
            db.flush()
            serialized = self._serialize(task)

        return {
            "success": True,
            "agent": self.name,
            "action": "complete_task",
            "task": serialized,
            "message": f"Task completed: {serialized['title']}"
        }

    async def _list_tasks(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """List tasks for the current thread"""
        self.update_status("active", "Listing tasks")

        show_completed = context.get("show_completed", False)
        thread_id = context.get("thread_id", "default")

        with get_session() as db:
            query = db.query(Task).filter(Task.thread_id == thread_id)
            if not show_completed:
                query = query.filter(Task.is_complete.is_(False))
            tasks = [self._serialize(t) for t in query.order_by(Task.created_at.desc()).all()]

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

        with get_session() as db:
            task = db.query(Task).filter(Task.id == task_id).first()
            if not task:
                return {
                    "success": False,
                    "agent": self.name,
                    "action": "delete_task",
                    "message": "Task not found"
                }
            serialized = self._serialize(task)
            db.delete(task)

        return {
            "success": True,
            "agent": self.name,
            "action": "delete_task",
            "task": serialized,
            "message": f"Task deleted: {serialized['title']}"
        }
