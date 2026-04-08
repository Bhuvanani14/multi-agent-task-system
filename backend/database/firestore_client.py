from typing import Dict, Any, List
import uuid
from datetime import datetime


class FirestoreClient:
    """Mock Firestore client for testing"""
    
    def __init__(self, project_id: str = None):
        self.project_id = project_id
        self.data = {
            "tasks": {},
            "events": {},
            "notes": {},
            "workflow_executions": {}
        }
    
    # Task operations
    async def create_task(self, task_data: Dict[str, Any]) -> str:
        task_id = str(uuid.uuid4())
        self.data["tasks"][task_id] = {
            **task_data,
            "id": task_id,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        return task_id
    
    async def get_tasks(self, user_id: str, status: str = None) -> List[Dict[str, Any]]:
        tasks = [t for t in self.data["tasks"].values() if t.get("user_id") == user_id]
        if status:
            tasks = [t for t in tasks if t.get("status") == status]
        return tasks
    
    async def update_task(self, task_id: str, updates: Dict[str, Any]) -> None:
        if task_id in self.data["tasks"]:
            self.data["tasks"][task_id].update(updates)
            self.data["tasks"][task_id]["updated_at"] = datetime.now().isoformat()
    
    # Event operations
    async def create_event(self, event_data: Dict[str, Any]) -> str:
        event_id = str(uuid.uuid4())
        self.data["events"][event_id] = {
            **event_data,
            "id": event_id,
            "created_at": datetime.now().isoformat()
        }
        return event_id
    
    async def get_events(self, user_id: str) -> List[Dict[str, Any]]:
        return [e for e in self.data["events"].values() if e.get("user_id") == user_id]
    
    # Note operations
    async def create_note(self, note_data: Dict[str, Any]) -> Dict[str, Any]:
        note_id = str(uuid.uuid4())
        note = {
            **note_data,
            "id": note_id,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        self.data["notes"][note_id] = note
        return note
    
    async def search_notes(self, query: str, user_id: str) -> List[Dict[str, Any]]:
        notes = [n for n in self.data["notes"].values() if n.get("user_id") == user_id]
        results = [n for n in notes if query.lower() in n.get("content", "").lower() 
                   or query.lower() in [t.lower() for t in n.get("tags", [])]]
        return results
    
    # Workflow execution logging
    async def log_workflow(self, workflow_data: Dict[str, Any]) -> str:
        execution_id = str(uuid.uuid4())
        self.data["workflow_executions"][execution_id] = {
            **workflow_data,
            "id": execution_id,
            "created_at": datetime.now().isoformat()
        }
        return execution_id
