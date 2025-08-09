from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
import logging
from datetime import datetime

from app.llm.ollama_client import OllamaClient
from app.tools.registry import tool_manager

logger = logging.getLogger(__name__)

class AgentMessage(BaseModel):
    role: str  # "user", "assistant", "system", "tool"
    content: str
    metadata: Dict[str, Any] = {}
    timestamp: datetime = None
    
    def __init__(self, **data):
        super().__init__(**data)
        if self.timestamp is None:
            self.timestamp = datetime.now()

class AgentResponse(BaseModel):
    content: str
    tool_calls: List[Dict[str, Any]] = []
    metadata: Dict[str, Any] = {}
    confidence: float = 0.0

class BaseAgent(ABC):
    """Base class for all agents"""
    
    def __init__(self, name: str, system_prompt: str):
        self.name = name
        self.system_prompt = system_prompt
        self.llm_client = OllamaClient()
        self.memory: List[AgentMessage] = []
        
    def add_message(self, role: str, content: str, metadata: Dict[str, Any] = None):
        """Add a message to memory"""
        self.memory.append(AgentMessage(
            role=role,
            content=content,
            metadata=metadata or {}
        ))
        
    def get_context(self, limit: int = 10) -> List[Dict[str, str]]:
        """Get recent context for LLM"""
        return [
            {"role": msg.role, "content": msg.content}
            for msg in self.memory[-limit:]
        ]
    
    async def think(self, prompt: str, context: Dict[str, Any] = None) -> AgentResponse:
        """Process input and generate response"""
        self.add_message("user", prompt, context)
        
        messages = [
            {"role": "system", "content": self.system_prompt},
            *self.get_context()
        ]
        
        try:
            response = await self.llm_client.chat(messages)
            content = response.get("message", {}).get("content", "")
            
            # Parse tool calls if present
            tool_calls = self._parse_tool_calls(content)
            
            agent_response = AgentResponse(
                content=content,
                tool_calls=tool_calls,
                confidence=0.8  # Could be enhanced with confidence scoring
            )
            
            self.add_message("assistant", content, {"tool_calls": tool_calls})
            return agent_response
            
        except Exception as e:
            logger.error(f"Agent thinking error: {e}")
            return AgentResponse(
                content=f"I encountered an error: {str(e)}",
                confidence=0.0
            )
    
    def _parse_tool_calls(self, content: str) -> List[Dict[str, Any]]:
        """Parse tool calls from agent response"""
        # Simple parsing - could be enhanced with JSON parsing
        tool_calls = []
        
        # Look for tool call patterns
        import re
        tool_pattern = r'@(\w+)\((.*?)\)'
        matches = re.findall(tool_pattern, content)
        
        for tool_name, params_str in matches:
            try:
                # Try to parse parameters as JSON
                params = {}
                if params_str.strip():
                    params = eval(params_str)  # Safe for controlled input
                tool_calls.append({
                    "tool": tool_name,
                    "parameters": params
                })
            except:
                pass
                
        return tool_calls
    
    @abstractmethod
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process input and return results"""
        pass
