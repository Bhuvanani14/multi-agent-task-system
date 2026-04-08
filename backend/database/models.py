from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class Task(BaseModel):
    id: Optional[str] = None
    user_id: str
    title: str
    description: str
    priority: str  # low, medium, high
    status: str = "open"  # open, in_progress, completed
    due_date: Optional[datetime] = None
    tags: List[str] = []
    created_at: datetime = None
    updated_at: datetime = None
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }


class Event(BaseModel):
    id: Optional[str] = None
    user_id: str
    name: str
    description: str
    start_time: datetime
    end_time: datetime
    attendees: List[str] = []
    location: Optional[str] = None
    created_at: datetime = None


class Note(BaseModel):
    id: Optional[str] = None
    user_id: str
    content: str
    tags: List[str] = []
    created_at: datetime = None
    updated_at: datetime = None


class WorkflowExecution(BaseModel):
    id: Optional[str] = None
    user_id: str
    user_request: str
    agents_used: List[str]
    execution_log: List[dict]
    results: dict
    created_at: datetime = None
