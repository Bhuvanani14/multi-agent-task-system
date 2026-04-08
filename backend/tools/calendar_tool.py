from typing import Dict, Any, List
from datetime import datetime, timedelta

CALENDAR_TOOL_SCHEMA = {
    "name": "calendar",
    "description": "Manage calendar events, find free slots, schedule meetings",
    "inputSchema": {
        "type": "object",
        "properties": {
            "method": {
                "type": "string",
                "enum": ["create_event", "list_events", "find_free_slots", "delete_event"]
            },
            "event_name": {"type": "string"},
            "start_time": {"type": "string", "format": "datetime"},
            "end_time": {"type": "string", "format": "datetime"},
            "attendees": {"type": "array", "items": {"type": "string"}},
            "duration_minutes": {"type": "integer"}
        }
    }
}


class CalendarTool:
    """Handles calendar operations"""
    
    def __init__(self):
        self.events = []
    
    async def create_event(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create calendar event"""
        event = {
            "id": f"event_{len(self.events)}",
            "name": event_data.get("event_name"),
            "start_time": event_data.get("start_time"),
            "end_time": event_data.get("end_time"),
            "attendees": event_data.get("attendees", []),
            "created_at": datetime.now().isoformat()
        }
        self.events.append(event)
        return event
    
    async def list_events(self, start_date: str = None, end_date: str = None) -> List[Dict[str, Any]]:
        """List calendar events"""
        return self.events
    
    async def find_free_slots(self, duration_minutes: int = 60) -> List[Dict[str, str]]:
        """Find free time slots"""
        now = datetime.now()
        slots = []
        for i in range(1, 5):
            slot_start = now + timedelta(hours=i*2)
            slot_end = slot_start + timedelta(minutes=duration_minutes)
            slots.append({
                "start": slot_start.isoformat(),
                "end": slot_end.isoformat()
            })
        return slots
    
    async def delete_event(self, event_id: str) -> Dict[str, str]:
        """Delete calendar event"""
        self.events = [e for e in self.events if e.get("id") != event_id]
        return {"status": "deleted", "event_id": event_id}
