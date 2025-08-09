from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)

class ToolResult(BaseModel):
    success: bool
    data: Any = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = {}

class ToolMetadata(BaseModel):
    name: str
    description: str
    parameters: Dict[str, Any]
    required: List[str]
    examples: List[str] = []

class BaseTool(ABC):
    """Base class for all tools"""
    
    def __init__(self):
        self.metadata = self._get_metadata()
    
    @abstractmethod
    def _get_metadata(self) -> ToolMetadata:
        """Return tool metadata for dynamic discovery"""
        pass
    
    @abstractmethod
    async def execute(self, parameters: Dict[str, Any]) -> ToolResult:
        """Execute the tool with given parameters"""
        pass
    
    def validate_parameters(self, parameters: Dict[str, Any]) -> bool:
        """Validate required parameters"""
        required = self.metadata.required
        return all(param in parameters for param in required)
    
    def get_usage_examples(self) -> List[str]:
        """Return usage examples"""
        return self.metadata.examples

class ToolRegistry:
    """Registry for dynamic tool discovery and management"""
    
    def __init__(self):
        self._tools: Dict[str, BaseTool] = {}
    
    def register(self, tool: BaseTool):
        """Register a new tool"""
        self._tools[tool.metadata.name] = tool
    
    def get_tool(self, name: str) -> Optional[BaseTool]:
        """Get tool by name"""
        return self._tools.get(name)
    
    def list_tools(self) -> List[ToolMetadata]:
        """List all available tools"""
        return [tool.metadata for tool in self._tools.values()]
    
    def search_tools(self, query: str) -> List[ToolMetadata]:
        """Search tools by description or name"""
        query = query.lower()
        return [
            tool.metadata for tool in self._tools.values()
            if query in tool.metadata.name.lower() or query in tool.metadata.description.lower()
        ]
