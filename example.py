"""
Example usage of the Agentic AI system.
"""
import asyncio
import os
from src.agent import Agent
from src.tools import create_tool_manager
from src.memory import ConversationMemory

async def main():
    """Example of using the agent programmatically."""
    print("🤖 Agentic AI Example")
    print("=" * 50)
    
    # Initialize components
    tool_manager = create_tool_manager()
    memory = ConversationMemory()
    
    # Initialize agent (you need to set OPENAI_API_KEY in .env)
    api_key = os.getenv("OPENAI_API_KEY", "dummy-key")
    agent = Agent(api_key=api_key, tool_manager=tool_manager, memory=memory)
    
    # Example session
    session_id = "example_session"
    
    # Example interactions
    examples = [
        "Calculate the square root of 144",
        "What is 15 * 23 + 7?",
        "Search for the latest news about artificial intelligence",
        "Create a simple Python script that prints 'Hello, World!'",
    ]
    
    print("Running example interactions:")
    print("-" * 30)
    
    for i, message in enumerate(examples, 1):
        print(f"\\n{i}. User: {message}")
        
        try:
            response = await agent.process_message(message, session_id)
            print(f"   Agent: {response['content']}")
            
            if response.get('tools_used'):
                tools = [tool['name'] for tool in response['tools_used']]
                print(f"   Tools used: {', '.join(tools)}")
                
        except Exception as e:
            print(f"   Error: {e}")
    
    print(f"\\n✅ Example completed!")
    print("\\nTo start the web server, run: python -m src.main")

if __name__ == "__main__":
    asyncio.run(main())
