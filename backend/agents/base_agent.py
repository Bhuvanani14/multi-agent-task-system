from abc import ABC, abstractmethod
from typing import Any, Dict, List
from pydantic import BaseModel
import json


class AgentMessage(BaseModel):
    role: str  # "user", "assistant", "system"
    content: str


class BaseAgent(ABC):
    def __init__(self, name: str, model: str = "claude-3-5-sonnet-20241022"):
        self.name = name
        self.model = model
        self.conversation_history: List[AgentMessage] = []
    
    @abstractmethod
    async def process(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process task and return results"""
        pass
    
    async def think(self, prompt: str) -> str:
        """Use Claude to reason about task"""
        try:
            from anthropic import Anthropic
            client = Anthropic()
            
            messages = [{"role": msg.role, "content": msg.content} 
                       for msg in self.conversation_history]
            messages.append({"role": "user", "content": prompt})
            
            response = client.messages.create(
                model=self.model,
                max_tokens=2048,
                messages=messages
            )
            
            result = response.content[0].text
            self.conversation_history.append(AgentMessage(role="user", content=prompt))
            self.conversation_history.append(AgentMessage(role="assistant", content=result))
            
            return result
        except Exception as e:
            # Mock response if Anthropic API is not available
            return f"Mock response: Processed '{prompt[:50]}...'"
    
    def add_tool_result(self, result: str):
        """Add tool execution result to conversation"""
        self.conversation_history.append(
            AgentMessage(role="user", content=f"Tool result: {result}")
        )
    
    def clear_history(self):
        """Reset conversation for new workflow"""
        self.conversation_history = []
