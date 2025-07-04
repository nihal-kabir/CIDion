"""
Core AI Agent implementation with reasoning and tool calling capabilities.
"""
import json
import logging
from typing import List, Dict, Any, Optional
from openai import OpenAI
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
        self.client = OpenAI(api_key=api_key)
        self.tool_manager = tool_manager
        self.memory = memory
        self.model = "gpt-4-turbo-preview"
        
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
        
        planning_response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "system", "content": plan_prompt}],
            temperature=0.1
        )
        
        plan_content = planning_response.choices[0].message.content
        logger.info(f"Agent plan: {plan_content}")
        
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
        
        # Prepare tools for OpenAI function calling
        openai_tools = self._prepare_openai_tools()
        
        messages = [
            {"role": "system", "content": execution_prompt},
            {"role": "user", "content": message}
        ]
        
        # Add recent history for context
        for msg in history[-5:]:  # Last 5 messages for context
            messages.insert(-1, {"role": msg["role"], "content": msg["content"]})
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=openai_tools,
            tool_choice="auto",
            temperature=0.2
        )
        
        message_obj = response.choices[0].message
        tools_used = []
        execution_steps = []
        
        # Handle tool calls
        if message_obj.tool_calls:
            for tool_call in message_obj.tool_calls:
                tool_name = tool_call.function.name
                tool_args = json.loads(tool_call.function.arguments)
                
                logger.info(f"Executing tool: {tool_name} with args: {tool_args}")
                execution_steps.append(f"Using {tool_name} tool")
                
                # Execute the tool
                tool_result = await self.tool_manager.execute_tool(tool_name, tool_args)
                tools_used.append({
                    "name": tool_name,
                    "args": tool_args,
                    "result": tool_result
                })
                
                # Add tool result to messages for final response
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(tool_result)
                })
            
            # Get final response after tool execution
            final_response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.3
            )
            
            final_content = final_response.choices[0].message.content
        else:
            final_content = message_obj.content
        
        return {
            "content": final_content,
            "thought_process": plan.split('\n'),
            "tools_used": tools_used,
            "execution_steps": execution_steps
        }
    
    def _create_planning_prompt(self, message: str, history: List[Dict]) -> str:
        """Create the planning prompt for the agent."""
        return f"""You are an intelligent AI agent with access to various tools. Your task is to analyze the user's request and create a clear plan of action.

Available tools: {self.tool_manager.get_tools_description()}

User's request: {message}

Create a step-by-step plan to address this request. Consider:
1. What information do you need?
2. Which tools might be helpful?
3. What's the logical sequence of actions?
4. How will you present the final result?

Provide a clear, numbered plan."""
    
    def _create_execution_prompt(self, message: str, history: List[Dict], plan: str, tools_desc: str) -> str:
        """Create the execution prompt with tools context."""
        return f"""You are an intelligent AI agent executing a plan to help the user.

Your plan:
{plan}

Available tools:
{tools_desc}

Instructions:
1. Follow your plan step by step
2. Use tools when they can provide value
3. Be thorough but efficient
4. Provide clear explanations of your actions
5. Give a comprehensive final answer

Execute your plan now to address the user's request."""
    
    def _prepare_openai_tools(self) -> List[Dict]:
        """Prepare tools in OpenAI function calling format."""
        tools = []
        for tool_name, tool in self.tool_manager.tools.items():
            tools.append({
                "type": "function",
                "function": {
                    "name": tool_name,
                    "description": tool.description,
                    "parameters": tool.parameters
                }
            })
        return tools
