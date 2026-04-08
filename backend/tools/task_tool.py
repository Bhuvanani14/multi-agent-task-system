from typing import Dict, Any, List

TASK_TOOL_SCHEMA = {
    "name": "tasks",
    "description": "Create, list, update, and manage tasks",
    "inputSchema": {
        "type": "object",
        "properties": {
            "method": {
                "type": "string",
                "enum": ["create_task", "list_tasks", "update_task", "complete_task"]
            },
            "title": {"type": "string"},
            "description": {"type": "string"},
            "priority": {"type": "string", "enum": ["low", "medium", "high"]},
            "due_date": {"type": "string", "format": "date"},
            "task_id": {"type": "string"}
        }
    }
}


class TaskTool:
    """Handles task management operations"""
    
    def __init__(self):
        self.tasks = []
    
    async def create_task(self, title: str, description: str = "", priority: str = "medium", 
                         due_date: str = None) -> Dict[str, Any]:
        """Create new task"""
        task = {
            "id": f"task_{len(self.tasks)}",
            "title": title,
            "description": description,
            "priority": priority,
            "due_date": due_date,
            "status": "open"
        }
        self.tasks.append(task)
        return task
    
    async def list_tasks(self, status: str = None, priority: str = None) -> List[Dict[str, Any]]:
        """List tasks with filters"""
        result = self.tasks
        if status:
            result = [t for t in result if t.get("status") == status]
        if priority:
            result = [t for t in result if t.get("priority") == priority]
        return result
    
    async def update_task(self, task_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update task"""
        for task in self.tasks:
            if task.get("id") == task_id:
                task.update(updates)
                return task
        return {"error": "Task not found"}
    
    async def complete_task(self, task_id: str) -> Dict[str, str]:
        """Mark task as complete"""
        for task in self.tasks:
            if task.get("id") == task_id:
                task["status"] = "completed"
                return {"status": "completed", "task_id": task_id}
        return {"error": "Task not found"}
