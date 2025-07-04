"""
Tools package initialization.
"""
from .base import Tool, ToolManager
from .file_ops import FileReadTool, FileWriteTool, FileListTool
from .web_tools import WebSearchTool, WebScrapeTool
from .calculator import CalculatorTool

def create_tool_manager() -> ToolManager:
    """Create and configure a tool manager with all available tools."""
    manager = ToolManager()
    
    # Register file operation tools
    manager.register_tool(FileReadTool())
    manager.register_tool(FileWriteTool())
    manager.register_tool(FileListTool())
    
    # Register web tools
    manager.register_tool(WebSearchTool())
    manager.register_tool(WebScrapeTool())
    
    # Register calculator tool
    manager.register_tool(CalculatorTool())
    
    return manager

__all__ = [
    "Tool", 
    "ToolManager", 
    "create_tool_manager",
    "FileReadTool", 
    "FileWriteTool", 
    "FileListTool",
    "WebSearchTool", 
    "WebScrapeTool",
    "CalculatorTool"
]
