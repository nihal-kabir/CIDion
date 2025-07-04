"""
Main entry point for the Agentic AI application.
"""
import os
import sys
import uvicorn
from dotenv import load_dotenv

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.api.app import create_app

def main():
    """Main function to start the application."""
    # Load environment variables
    load_dotenv()
    
    # Create the FastAPI app
    app = create_app()
    
    # Get configuration from environment
    host = os.getenv("HOST", "localhost")
    port = int(os.getenv("PORT", 8000))
    
    print(f"🚀 Starting Agentic AI Server on http://{host}:{port}")
    print("📱 Web Interface: http://localhost:8000")
    print("📚 API Docs: http://localhost:8000/docs")
    
    # Start the server
    uvicorn.run(
        app,
        host=host,
        port=port,
        reload=True,
        log_level=os.getenv("LOG_LEVEL", "info").lower()
    )

if __name__ == "__main__":
    main()
