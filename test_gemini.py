"""
Test script to verify Gemini API integration.
"""
import os
import sys
import asyncio
from dotenv import load_dotenv

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

load_dotenv()

from src.agent.core import Agent
from src.tools import create_tool_manager
from src.memory.conversation import ConversationMemory

async def test_gemini():
    """Test Gemini API integration."""
    
    print("🧪 Testing Gemini API Integration...")
    
    # Get API key
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ GEMINI_API_KEY not found in environment!")
        return False
    
    print("✅ API key found")
    
    try:
        # Initialize components
        tool_manager = create_tool_manager()
        memory = ConversationMemory()
        agent = Agent(api_key=api_key, tool_manager=tool_manager, memory=memory)
        
        print("✅ Agent initialized")
        
        # Test simple conversation
        test_message = "Hello! Can you help me calculate 15 + 27?"
        session_id = "test-session"
        
        print(f"🤖 Testing with message: {test_message}")
        
        response = await agent.process_message(test_message, session_id)
        
        print("✅ Response received:")
        print(f"📝 Content: {response['content']}")
        print(f"🔧 Tools used: {len(response['tools_used'])}")
        print(f"📋 Steps: {len(response['execution_steps'])}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_gemini())
    if success:
        print("\n🎉 Gemini integration test passed!")
    else:
        print("\n💥 Gemini integration test failed!")
        sys.exit(1)
