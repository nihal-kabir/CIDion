"""
File operation tools for the agent.
"""
import os
import aiofiles
from typing import Dict, Any
from src.tools.base import Tool

class FileReadTool(Tool):
    """Tool for reading file contents."""
    
    @property
    def name(self) -> str:
        return "read_file"
    
    @property
    def description(self) -> str:
        return "Read the contents of a file"
    
    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to read"
                }
            },
            "required": ["file_path"]
        }
    
    async def execute(self, file_path: str) -> str:
        """Read file contents."""
        try:
            async with aiofiles.open(file_path, 'r', encoding='utf-8') as file:
                content = await file.read()
                return content
        except FileNotFoundError:
            return f"File not found: {file_path}"
        except Exception as e:
            return f"Error reading file: {str(e)}"

class FileWriteTool(Tool):
    """Tool for writing file contents."""
    
    @property
    def name(self) -> str:
        return "write_file"
    
    @property
    def description(self) -> str:
        return "Write content to a file"
    
    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to write"
                },
                "content": {
                    "type": "string",
                    "description": "Content to write to the file"
                }
            },
            "required": ["file_path", "content"]
        }
    
    async def execute(self, file_path: str, content: str) -> str:
        """Write content to file."""
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            async with aiofiles.open(file_path, 'w', encoding='utf-8') as file:
                await file.write(content)
                return f"Successfully wrote to {file_path}"
        except Exception as e:
            return f"Error writing file: {str(e)}"

class FileListTool(Tool):
    """Tool for listing directory contents."""
    
    @property
    def name(self) -> str:
        return "list_files"
    
    @property
    def description(self) -> str:
        return "List files and directories in a path"
    
    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "directory_path": {
                    "type": "string",
                    "description": "Path to the directory to list"
                }
            },
            "required": ["directory_path"]
        }
    
    async def execute(self, directory_path: str) -> str:
        """List directory contents."""
        try:
            items = os.listdir(directory_path)
            files = []
            dirs = []
            
            for item in items:
                item_path = os.path.join(directory_path, item)
                if os.path.isdir(item_path):
                    dirs.append(f"📁 {item}/")
                else:
                    files.append(f"📄 {item}")
            
            result = []
            if dirs:
                result.append("Directories:")
                result.extend(dirs)
            if files:
                result.append("Files:")
                result.extend(files)
            
            return "\n".join(result) if result else "Directory is empty"
        except Exception as e:
            return f"Error listing directory: {str(e)}"
