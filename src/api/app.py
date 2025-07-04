"""
FastAPI application for the CIDion AI system.
"""
import os
import uuid
from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import logging
from dotenv import load_dotenv

from src.agent import Agent
from src.tools import create_tool_manager
from src.memory import ConversationMemory

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChatMessage(BaseModel):
    """Chat message model."""
    message: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    """Chat response model."""
    response: str
    session_id: str
    thought_process: List[str]
    tools_used: List[Dict[str, Any]]
    execution_steps: List[str]

class SessionInfo(BaseModel):
    """Session information model."""
    session_id: str
    created_at: str
    last_activity: str
    title: Optional[str] = None
    summary: Optional[str] = None

def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="CIDion AI System",
        description="An intelligent AI agent with tool calling capabilities",
        version="1.0.0"
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Initialize components
    tool_manager = create_tool_manager()
    memory = ConversationMemory()
    
    # Get Gemini API key
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        logger.warning("GEMINI_API_KEY not found. Set it in .env file for full functionality.")
        api_key = "dummy-key"  # For testing without Gemini
    
    agent = Agent(api_key=api_key, tool_manager=tool_manager, memory=memory)
    
    @app.get("/", response_class=HTMLResponse)
    async def root():
        """Serve the main web interface."""
        html_content = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>CIDion AI Assistant</title>
            <style>
                * {
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }
                
                body {
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    padding: 20px;
                }
                
                .container {
                    background: white;
                    border-radius: 20px;
                    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
                    width: 100%;
                    max-width: 1000px;
                    height: 750px;
                    display: flex;
                    flex-direction: column;
                    overflow: hidden;
                }
                
                .header {
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 20px;
                    text-align: center;
                }
                
                .header h1 {
                    font-size: 24px;
                    margin-bottom: 5px;
                }
                
                .header p {
                    opacity: 0.9;
                    font-size: 14px;
                }
                
                .chat-area {
                    flex: 1;
                    display: flex;
                    flex-direction: column;
                    padding: 20px;
                    overflow: hidden;
                }
                
                .messages {
                    flex: 1;
                    overflow-y: auto;
                    margin-bottom: 20px;
                    padding-right: 10px;
                }
                
                .message {
                    margin-bottom: 15px;
                    padding: 12px 16px;
                    border-radius: 12px;
                    max-width: 80%;
                    word-wrap: break-word;
                }
                
                .user-message {
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    margin-left: auto;
                }
                
                .agent-message {
                    background: #f5f5f5;
                    color: #333;
                }
                
                .debug-info {
                    background: #fff3e0;
                    color: #f57c00;
                    font-size: 12px;
                    margin: 5px 0;
                    padding: 8px 12px;
                    border-radius: 8px;
                    border-left: 3px solid #ff9800;
                    opacity: 0.8;
                }
                
                .input-area {
                    display: flex;
                    gap: 10px;
                }
                
                .input-area input {
                    flex: 1;
                    padding: 12px 16px;
                    border: 2px solid #e0e0e0;
                    border-radius: 25px;
                    font-size: 14px;
                    outline: none;
                    transition: border-color 0.3s;
                }
                
                .input-area input:focus {
                    border-color: #667eea;
                }
                
                .input-area button {
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    border: none;
                    padding: 12px 24px;
                    border-radius: 25px;
                    cursor: pointer;
                    font-size: 14px;
                    font-weight: 600;
                    transition: transform 0.2s;
                }
                
                .input-area button:hover {
                    transform: translateY(-2px);
                }
                
                .input-area button:disabled {
                    opacity: 0.6;
                    transform: none;
                    cursor: not-allowed;
                }
                
                .loading {
                    display: inline-block;
                    width: 20px;
                    height: 20px;
                    border: 3px solid #f3f3f3;
                    border-top: 3px solid #667eea;
                    border-radius: 50%;
                    animation: spin 1s linear infinite;
                }
                
                @keyframes spin {
                    0% { transform: rotate(0deg); }
                    100% { transform: rotate(360deg); }
                }
                
                .status {
                    text-align: center;
                    padding: 10px;
                    font-size: 12px;
                    color: #666;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🤖 CIDion AI Assistant</h1>
                    <p>Your intelligent assistant with tool calling capabilities</p>
                    <div style="margin-top: 10px;">
                        <label style="font-size: 12px; cursor: pointer;">
                            <input type="checkbox" id="debugMode" style="margin-right: 5px;"> Debug Mode
                        </label>
                    </div>
                </div>
                
                <div class="chat-area">
                    <div class="messages" id="messages">
                        <div class="agent-message">
                            👋 Hello! I'm your AI assistant with access to various tools. I can help you with:
                            <br>• File operations (read, write, list)
                            <br>• Web search and scraping
                            <br>• Mathematical calculations
                            <br>• Planning and executing complex tasks
                            <br><br>What would you like me to help you with today?
                        </div>
                    </div>
                    
                    <div class="input-area">
                        <input type="text" id="messageInput" placeholder="Ask me anything..." onkeypress="handleKeyPress(event)">
                        <button onclick="sendMessage()" id="sendButton">Send</button>
                    </div>
                </div>
                
                <div class="status" id="status">Ready</div>
            </div>
            
            <script>
                let sessionId = null;
                
                function handleKeyPress(event) {
                    if (event.key === 'Enter') {
                        sendMessage();
                    }
                }
                
                async function sendMessage() {
                    const input = document.getElementById('messageInput');
                    const message = input.value.trim();
                    
                    if (!message) return;
                    
                    const messagesDiv = document.getElementById('messages');
                    const sendButton = document.getElementById('sendButton');
                    const status = document.getElementById('status');
                    
                    // Add user message to chat
                    const userDiv = document.createElement('div');
                    userDiv.className = 'message user-message';
                    userDiv.textContent = message;
                    messagesDiv.appendChild(userDiv);
                    
                    // Clear input and disable button
                    input.value = '';
                    sendButton.disabled = true;
                    sendButton.innerHTML = '<div class="loading"></div>';
                    status.textContent = 'Processing...';
                    
                    // Scroll to bottom
                    messagesDiv.scrollTop = messagesDiv.scrollHeight;
                    
                    try {
                        const response = await fetch('/api/chat', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                            },
                            body: JSON.stringify({
                                message: message,
                                session_id: sessionId
                            })
                        });
                        
                        const data = await response.json();
                        sessionId = data.session_id;
                        
                        // Check if debug mode is enabled
                        const debugMode = document.getElementById('debugMode').checked;
                        
                        // Add agent response first (clean, main response)
                        const agentDiv = document.createElement('div');
                        agentDiv.className = 'message agent-message';
                        agentDiv.innerHTML = data.response.replace(/\\n/g, '<br>');
                        messagesDiv.appendChild(agentDiv);
                        
                        // Show debug information ONLY if debug mode is enabled
                        if (debugMode) {
                            if (data.thought_process && data.thought_process.length > 0) {
                                const thinkingDiv = document.createElement('div');
                                thinkingDiv.className = 'debug-info';
                                thinkingDiv.innerHTML = '<strong>🧠 Thinking:</strong><br>' + data.thought_process.join('<br>');
                                messagesDiv.appendChild(thinkingDiv);
                            }
                            
                            if (data.tools_used && data.tools_used.length > 0) {
                                const toolsDiv = document.createElement('div');
                                toolsDiv.className = 'debug-info';
                                const toolsList = data.tools_used.map(tool => `🔧 ${tool.name}`).join(', ');
                                toolsDiv.innerHTML = '<strong>Tools used:</strong> ' + toolsList;
                                messagesDiv.appendChild(toolsDiv);
                            }
                        }
                        
                        status.textContent = 'Ready';
                        
                    } catch (error) {
                        const errorDiv = document.createElement('div');
                        errorDiv.className = 'message agent-message';
                        errorDiv.textContent = 'Sorry, I encountered an error: ' + error.message;
                        messagesDiv.appendChild(errorDiv);
                        
                        status.textContent = 'Error occurred';
                    }
                    
                    // Re-enable button
                    sendButton.disabled = false;
                    sendButton.textContent = 'Send';
                    
                    // Scroll to bottom
                    messagesDiv.scrollTop = messagesDiv.scrollHeight;
                    
                    // Focus input
                    input.focus();
                }
                
                // Focus input on load
                document.getElementById('messageInput').focus();
            </script>
        </body>
        </html>
        """
        return HTMLResponse(content=html_content)
    
    @app.post("/api/chat", response_model=ChatResponse)
    async def chat(message: ChatMessage):
        """Handle chat messages from the user."""
        try:
            # Generate session ID if not provided
            session_id = message.session_id or str(uuid.uuid4())
            
            # Process the message with the agent
            result = await agent.process_message(message.message, session_id)
            
            return ChatResponse(
                response=result["content"],
                session_id=session_id,
                thought_process=result.get("thought_process", []),
                tools_used=result.get("tools_used", []),
                execution_steps=result.get("execution_steps", [])
            )
            
        except Exception as e:
            logger.error(f"Error in chat endpoint: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.get("/api/sessions", response_model=List[SessionInfo])
    async def get_sessions():
        """Get recent conversation sessions."""
        try:
            sessions = await memory.get_recent_sessions()
            return [
                SessionInfo(
                    session_id=session["session_id"],
                    created_at=session["created_at"],
                    last_activity=session["last_activity"],
                    title=session["title"],
                    summary=session["summary"]
                )
                for session in sessions
            ]
        except Exception as e:
            logger.error(f"Error getting sessions: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.get("/api/health")
    async def health_check():
        """Health check endpoint."""
        return {
            "status": "healthy",
            "tools_available": len(tool_manager.tools),
            "tool_names": list(tool_manager.tools.keys())
        }
    
    return app
