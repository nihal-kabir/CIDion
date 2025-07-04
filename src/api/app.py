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
        title="CIDion",
        description="AI assistant with tool calling capabilities",
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
    
    # Get configuration from environment
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        logger.warning("GEMINI_API_KEY not found. Set it in environment variables for full functionality.")
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
            <title>CIDion</title>
            <link rel="preconnect" href="https://fonts.googleapis.com">
            <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
            <link href="https://fonts.googleapis.com/css2?family=Roboto+Serif:wght@400;700;900&display=swap" rel="stylesheet">
            <style>
                * {
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }
                
                body {
                    font-family: 'Arial', 'Helvetica', sans-serif;
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
                    font-size: 42px;
                    font-weight: 900;
                    margin-bottom: 12px;
                    font-family: 'Roboto Serif', serif;
                }
                
                .header p {
                    opacity: 0.95;
                    font-size: 22px;
                    font-weight: 700;
                    font-family: 'Roboto Serif', serif;
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
                
                .welcome-box {
                    background: #f8f9fa;
                    border: 1px solid #e9ecef;
                    border-radius: 15px;
                    padding: 20px;
                    margin: 20px auto 30px auto;
                    max-width: 500px;
                    text-align: center;
                    font-family: 'Trebuchet MS', sans-serif;
                    color: #6c757d;
                    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
                }
                
                .message {
                    margin-bottom: 15px;
                    padding: 12px 16px;
                    border-radius: 12px;
                    max-width: 80%;
                    word-wrap: break-word;
                    font-family: 'Trebuchet MS', sans-serif;
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
                    font-family: 'Arial', 'Helvetica', sans-serif;
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
                    font-family: 'Arial', 'Helvetica', sans-serif;
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
                    <h1>🤖 CIDion</h1>
                    <p>Bol bsdk, kya chahiye tereko?</p>
                </div>
                
                <div class="chat-area">
                    <div class="welcome-box">
                        👋 Hello! I'm your AI assistant with access to various tools. I can help you with:
                        <br>• File operations (read, write, list)
                        <br>• Web search and scraping
                        <br>• Mathematical calculations
                        <br>• Planning and executing complex tasks
                        <br><br>What can I help you with?
                    </div>
                    
                    <div class="messages" id="messages">
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
                        
                        if (!response.ok) {
                            throw new Error(`HTTP error! status: ${response.status}`);
                        }
                        
                        const data = await response.json();
                        sessionId = data.session_id;
                        
                        // ONLY show the clean agent response (no debug functionality)
                        const agentDiv = document.createElement('div');
                        agentDiv.className = 'message agent-message';
                        agentDiv.innerHTML = data.response.replace(/\\n/g, '<br>');
                        messagesDiv.appendChild(agentDiv);
                        
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
