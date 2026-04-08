from typing import Dict, Any
from .base_agent import BaseAgent
from datetime import datetime, timedelta
import json
import re


class ScheduleAgent(BaseAgent):
    def __init__(self, db_client=None, calendar_tool=None):
        super().__init__(name="ScheduleAgent")
        self.db = db_client
        self.calendar = calendar_tool
    
    async def process(self, schedule_request: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle scheduling requests - create events, find time slots, send invitations
        """
        
        # Understand scheduling intent
        intent_prompt = f"""
        Understand this scheduling request:
        {schedule_request}
        
        Extract:
        - Event name
        - Proposed time/date
        - Duration (default 1 hour)
        - Attendees
        - Location (if mentioned)
        
        Respond in JSON format.
        """
        
        event_details = await self.think(intent_prompt)
        parsed = self._parse_json(event_details)
        
        # Create calendar event
        event_id = "event_123"
        event = {"id": event_id, **parsed}
        
        if self.calendar:
            event = await self.calendar.create_event(parsed)
        
        if self.db:
            await self.db.create_event(event)
        
        return {
            "status": "scheduled",
            "event_id": event.get("id"),
            "details": event,
            "message": f"Event '{parsed.get('name', 'Event')}' scheduled"
        }
    
    async def find_free_slots(self, duration_minutes: int = 60) -> Dict[str, Any]:
        """Find free time slots for scheduling"""
        if self.calendar:
            free_slots = await self.calendar.get_free_slots(duration_minutes)
            return {"free_slots": free_slots}
        return {"free_slots": []}
    
    def _parse_json(self, text: str) -> Dict[str, Any]:
        try:
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except json.JSONDecodeError:
            pass
        return {"name": "Event", "time": "TBD", "duration": 60}
