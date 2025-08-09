import importlib
import inspect
import logging
from pathlib import Path
from typing import List, Type
from app.tools.base_tool import BaseTool, ToolRegistry

logger = logging.getLogger(__name__)

class ToolManager:
    """Manages dynamic tool discovery and registration"""
    
    def __init__(self):
        self.registry = ToolRegistry()
        self._discover_tools()
    
    def _discover_tools(self):
        """Automatically discover and register tools from the tools directory"""
        tools_dir = Path(__file__).parent
        
        # Find all Python files in tools directory
        for tool_file in tools_dir.rglob("*.py"):
            if tool_file.name.startswith("_") or tool_file.name == "base_tool.py":
                continue
            
            try:
                # Import the module
                module_name = tool_file.stem
                relative_path = tool_file.parent.relative_to(tools_dir)
                
                if str(relative_path) == ".":
                    module_path = f"app.tools.{module_name}"
                else:
                    module_path = f"app.tools.{'.'.join(relative_path.parts)}.{module_name}"
                
                module = importlib.import_module(module_path)
                
                # Find all classes that inherit from BaseTool
                for name, obj in inspect.getmembers(module):
                    if (inspect.isclass(obj) and 
                        issubclass(obj, BaseTool) and 
                        obj != BaseTool):
                        
                        tool_instance = obj()
                        self.registry.register(tool_instance)
                        logger.info(f"Registered tool: {tool_instance.metadata.name}")
                        
            except Exception as e:
                logger.warning(f"Failed to load tool from {tool_file}: {e}")
    
    def get_registry(self) -> ToolRegistry:
        """Get the tool registry"""
        return self.registry
    
    def list_available_tools(self) -> List[dict]:
        """List all available tools with their metadata"""
        return [
            {
                "name": tool.metadata.name,
                "description": tool.metadata.description,
                "parameters": tool.metadata.parameters,
                "examples": tool.metadata.examples
            }
            for tool in self.registry._tools.values()
        ]

# Global tool manager instance
tool_manager = ToolManager()
