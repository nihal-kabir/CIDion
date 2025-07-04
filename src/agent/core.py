"""
Core AI Agent implementation with reasoning and tool calling capabilities.
"""
import json
import logging
from typing import List, Dict, Any, Optional
import google.generativeai as genai
from pydantic import BaseModel

from src.tools.base import Tool, ToolManager
from src.memory.conversation import ConversationMemory

logger = logging.getLogger(__name__)

class Task(BaseModel):
    """Represents a task with steps and status."""
    id: str
    description: str
    steps: List[str]
    completed_steps: List[str] = []
    status: str = "pending"  # pending, in_progress, completed, failed
    result: Optional[str] = None

class Agent:
    """
    Main AI Agent with planning, reasoning, and tool execution capabilities.
    """
    
    def __init__(self, api_key: str, tool_manager: ToolManager, memory: ConversationMemory):
        """Initialize the agent with tools and memory."""
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        self.tool_manager = tool_manager
        self.memory = memory
        
    async def process_message(self, message: str, session_id: str) -> Dict[str, Any]:
        """
        Process a user message and execute any necessary actions.
        
        Args:
            message: The user's message
            session_id: Unique session identifier
            
        Returns:
            Dict containing the response and execution details
        """
        try:
            # Store user message in memory
            await self.memory.add_message(session_id, "user", message)
            
            # Get conversation history
            history = await self.memory.get_conversation_history(session_id)
            
            # Plan and execute
            response = await self._plan_and_execute(message, history)
            
            # Store agent response in memory
            await self.memory.add_message(session_id, "assistant", response["content"])
            
            return response
            
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            error_response = {
                "content": f"I encountered an error: {str(e)}",
                "thought_process": ["Error occurred during processing"],
                "tools_used": [],
                "execution_steps": []
            }
            await self.memory.add_message(session_id, "assistant", error_response["content"])
            return error_response
    
    async def _plan_and_execute(self, message: str, history: List[Dict]) -> Dict[str, Any]:
        """
        Plan the approach and execute the necessary steps.
        """
        # First, analyze the message and create a plan
        plan_prompt = self._create_planning_prompt(message, history)
        
        try:
            planning_response = self.model.generate_content(plan_prompt)
            plan_content = planning_response.text
            logger.info(f"Agent plan: {plan_content}")
        except Exception as e:
            logger.error(f"Error generating plan: {e}")
            plan_content = "Simple plan: Address the user's request directly."
        
        # Parse the plan and determine if tools are needed
        execution_response = await self._execute_with_tools(message, history, plan_content)
        
        return execution_response
    
    async def _execute_with_tools(self, message: str, history: List[Dict], plan: str) -> Dict[str, Any]:
        """
        Execute the plan using available tools.
        """
        # Get available tools
        tools_description = self.tool_manager.get_tools_description()
        
        # Create execution prompt with tools
        execution_prompt = self._create_execution_prompt(message, history, plan, tools_description)
        
        # Build conversation context
        conversation_context = ""
        for msg in history[-5:]:  # Last 5 messages for context
            conversation_context += f"{msg['role']}: {msg['content']}\n"
        
        full_prompt = f"{execution_prompt}\n\nConversation context:\n{conversation_context}\n\nUser: {message}"
        
        tools_used = []
        execution_steps = []
        
        try:
            # Generate initial response
            response = self.model.generate_content(full_prompt)
            initial_response = response.text
            
            # Check if the response suggests using tools
            response_lower = initial_response.lower()
            final_content = initial_response
            
            # Simple tool detection based on keywords
            if any(keyword in response_lower for keyword in ['calculate', 'math', 'compute']):
                # Try to extract calculation from response
                import re
                math_patterns = re.findall(r'[\d+\-*/().\s]+', initial_response)
                for pattern in math_patterns:
                    if any(op in pattern for op in ['+', '-', '*', '/', '(']):
                        try:
                            result = await self.tool_manager.execute_tool('calculate', {'expression': pattern.strip()})
                            tools_used.append({
                                "name": "calculate",
                                "args": {"expression": pattern.strip()},
                                "result": result
                            })
                            execution_steps.append("Used calculator tool")
                            final_content += f"\n\nCalculation result: {result}"
                        except:
                            pass
            
            if any(keyword in response_lower for keyword in ['search', 'find', 'look up']):
                # Extract search query
                search_query = message
                if len(search_query) > 100:
                    search_query = search_query[:100]
                try:
                    result = await self.tool_manager.execute_tool('web_search', {'query': search_query})
                    tools_used.append({
                        "name": "web_search",
                        "args": {"query": search_query},
                        "result": result
                    })
                    execution_steps.append("Used web search tool")
                    final_content += f"\n\nSearch results: {result}"
                except:
                    pass
            
            if any(keyword in response_lower for keyword in ['read', 'file', 'open']):
                # Look for file paths in the message
                import re
                file_patterns = re.findall(r'[^\s]+\.[a-zA-Z]{1,5}', message)
                for file_path in file_patterns:
                    try:
                        result = await self.tool_manager.execute_tool('read_file', {'file_path': file_path})
                        tools_used.append({
                            "name": "read_file",
                            "args": {"file_path": file_path},
                            "result": result
                        })
                        execution_steps.append("Used file read tool")
                        final_content += f"\n\nFile content: {result}"
                    except:
                        pass
            
            # If tools were used, generate a final response incorporating the results
            if tools_used:
                tool_results = "\n".join([f"Tool {tool['name']}: {tool['result']}" for tool in tools_used])
                final_prompt = f"Based on the original question: {message}\nAnd these tool results:\n{tool_results}\n\nProvide a comprehensive final answer:"
                
                try:
                    final_response = self.model.generate_content(final_prompt)
                    final_content = final_response.text
                except:
                    pass  # Keep the original response if final generation fails
            
        except Exception as e:
            logger.error(f"Error in execution: {e}")
            final_content = f"I encountered an error while processing your request: {str(e)}"
        
        return {
            "content": final_content,
            "thought_process": plan.split('\n'),
            "tools_used": tools_used,
            "execution_steps": execution_steps
        }
    
    def _create_planning_prompt(self, message: str, history: List[Dict]) -> str:
        """Create the planning prompt for the agent."""
        recent_context = ""
        if history:
            recent_messages = history[-3:]  # Last 3 messages for context
            recent_context = "\\nRecent conversation context:\\n"
            for msg in recent_messages:
                recent_context += f"{msg['role']}: {msg['content'][:100]}...\\n"
        
        return f"""You are an intelligent AI agent with access to various tools. Your task is to analyze the user's request and create a clear plan of action.

Available tools: {self.tool_manager.get_tools_description()}

{recent_context}

User's request: {message}

Create a step-by-step plan to address this request. Consider:
1. What information do you need?
2. Which tools might be helpful?
3. What's the logical sequence of actions?
4. How will you present the final result?

Provide a clear, numbered plan."""
    
    def _create_execution_prompt(self, message: str, history: List[Dict], plan: str, tools_desc: str) -> str:
        """Create the execution prompt with tools context."""
        context_info = ""
        if history:
            context_info = "\\nYou have access to the conversation history for context."
        
        return f"""You are an intelligent AI agent executing a plan to help the user.

Your plan:
{plan}

Available tools:
{tools_desc}

User's original request: {message}
{context_info}

Instructions:
1. Follow your plan step by step
2. Use tools when they can provide value
3. Be thorough but efficient
4. Provide clear explanations of your actions
5. Give a comprehensive final answer

Execute your plan now to address the user's request."""
