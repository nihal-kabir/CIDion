"""
Base classes for the tool system.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)

class Tool(ABC):
    """Base class for all tools."""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Return the tool name."""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Return the tool description."""
        pass
    
    @property
    @abstractmethod
    def parameters(self) -> Dict[str, Any]:
        """Return the tool parameters schema."""
        pass
    
    @abstractmethod
    async def execute(self, **kwargs) -> Any:
        """Execute the tool with given parameters."""
        pass

class ToolManager:
    """Manages all available tools."""
    
    def __init__(self):
        """Initialize the tool manager."""
        self.tools: Dict[str, Tool] = {}
    
    def register_tool(self, tool: Tool) -> None:
        """Register a new tool."""
        self.tools[tool.name] = tool
        logger.info(f"Registered tool: {tool.name}")
    
    def get_tools_description(self) -> str:
        """Get a description of all available tools."""
        descriptions = []
        for tool in self.tools.values():
            descriptions.append(f"- {tool.name}: {tool.description}")
        return "\n".join(descriptions)
    
    async def execute_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Any:
        """Execute a tool by name with given parameters."""
        if tool_name not in self.tools:
            raise ValueError(f"Tool '{tool_name}' not found")
        
        tool = self.tools[tool_name]
        logger.info(f"Executing tool: {tool_name}")
        
        try:
            result = await tool.execute(**parameters)
            logger.info(f"Tool {tool_name} executed successfully")
            return result
        except Exception as e:
            logger.error(f"Error executing tool {tool_name}: {e}")
            raise
    
    def list_tools(self) -> List[str]:
        """List all available tool names."""
        return list(self.tools.keys())
