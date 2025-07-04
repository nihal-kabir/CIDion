#!/usr/bin/env python3
"""
Simple test to verify the project setup.
"""
import sys
import os

def test_imports():
    """Test if all required modules can be imported."""
    print("🧪 Testing Project Setup")
    print("=" * 30)
    
    # Add current directory to path
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    try:
        print("✅ Testing basic imports...")
        import fastapi
        import uvicorn
        import openai
        import pydantic
        import aiofiles
        import requests
        import sqlite3
        print("✅ All basic dependencies imported successfully")
        
        print("✅ Testing project modules...")
        from src.tools import create_tool_manager
        from src.memory import ConversationMemory
        from src.agent import Agent
        print("✅ All project modules imported successfully")
        
        print("✅ Testing tool manager...")
        tool_manager = create_tool_manager()
        print(f"✅ Tool manager created with {len(tool_manager.tools)} tools")
        
        print("✅ Testing memory system...")
        memory = ConversationMemory("test.db")
        print("✅ Memory system initialized")
        
        # Clean up test db
        if os.path.exists("test.db"):
            os.remove("test.db")
        
        print("\\n🎉 All tests passed! Project is ready to run.")
        print("\\nTo start the server:")
        print("python -m src.main")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please check that all dependencies are installed:")
        print("pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1)
