from typing import Dict, Any
from .base_agent import BaseAgent
import json
import re


class NotesAgent(BaseAgent):
    def __init__(self, db_client=None):
        super().__init__(name="NotesAgent")
        self.db = db_client
    
    async def process(self, note_request: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle note creation, retrieval, and organization
        """
        
        # Determine note intent
        intent_prompt = f"""
        Determine what the user wants to do with notes:
        {note_request}
        
        Return JSON with:
        - action: "create", "search", "organize", "delete"
        - content: (for create)
        - tags: (for organizing)
        - query: (for search)
        """
        
        intent = await self.think(intent_prompt)
        parsed = self._parse_json(intent)
        
        action = parsed.get("action", "create")
        
        if action == "create":
            note_id = "note_123"
            if self.db:
                note = await self.db.create_note({
                    "content": parsed.get("content"),
                    "tags": parsed.get("tags", []),
                    "user_id": context.get("user_id")
                })
                note_id = note.get("id")
            return {"status": "created", "note_id": note_id}
        
        elif action == "search":
            results = []
            if self.db:
                results = await self.db.search_notes(
                    query=parsed.get("query"),
                    user_id=context.get("user_id")
                )
            return {"status": "success", "results": results}
        
        return {"status": "processed"}
    
    def _parse_json(self, text: str) -> Dict[str, Any]:
        try:
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except json.JSONDecodeError:
            pass
        return {"action": "create", "content": ""}
