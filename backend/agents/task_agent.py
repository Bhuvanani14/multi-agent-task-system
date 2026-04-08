from typing import Dict, Any
from .base_agent import BaseAgent
import json
import re


class TaskAgent(BaseAgent):
    def __init__(self, db_client=None):
        super().__init__(name="TaskAgent")
        self.db = db_client
    
    async def process(self, task_description: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle task creation, updating, completion tracking
        """
        
        # Parse task details
        parse_prompt = f"""
        Parse this task description and extract:
        - Task title
        - Description
        - Priority (high/medium/low)
        - Due date (if mentioned)
        - Sub-tasks (if any)
        
        Description: {task_description}
        
        Respond in JSON format with keys: title, description, priority, due_date, subtasks
        """
        
        task_details = await self.think(parse_prompt)
        parsed = self._parse_json(task_details)
        
        # Create in database if available
        task_id = "task_123"
        if self.db:
            task_id = await self.db.create_task(parsed)
        
        return {
            "status": "created",
            "task_id": task_id,
            "details": parsed,
            "message": f"Task '{parsed.get('title', 'New Task')}' created successfully"
        }
    
    async def list_tasks(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """List all tasks with filters"""
        if self.db:
            tasks = await self.db.get_tasks(
                user_id=context.get("user_id"),
                status=context.get("status")
            )
            return {"tasks": tasks, "count": len(tasks)}
        return {"tasks": [], "count": 0}
    
    async def update_task(self, task_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update existing task"""
        if self.db:
            await self.db.update_task(task_id, updates)
        return {"status": "updated", "task_id": task_id}
    
    def _parse_json(self, text: str) -> Dict[str, Any]:
        try:
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except json.JSONDecodeError:
            pass
        return {"title": "Task", "description": "", "priority": "medium", "subtasks": []}
