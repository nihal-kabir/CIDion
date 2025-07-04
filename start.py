#!/usr/bin/env python3
"""
Simple startup script for the Agentic AI system.
"""
import os
import sys
import subprocess

def check_dependencies():
    """Check if all required dependencies are installed."""
    try:
        import fastapi
        import uvicorn
        import openai
        import aiofiles
        import aiosqlite
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        return False

def install_dependencies():
    """Install dependencies from requirements.txt."""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def create_env_file():
    """Create .env file if it doesn't exist."""
    if not os.path.exists(".env"):
        print("📝 Creating .env file...")
        with open(".env", "w") as f:
            f.write("# Environment Configuration\n")
            f.write("OPENAI_API_KEY=your_openai_api_key_here\n")
            f.write("LOG_LEVEL=INFO\n")
            f.write("HOST=localhost\n")
            f.write("PORT=8000\n")
        print("✅ Created .env file. Please add your OpenAI API key!")
        return False
    return True

def main():
    """Main startup function."""
    print("🚀 Starting Agentic AI System...")
    print("=" * 50)
    
    # Check if dependencies are installed
    if not check_dependencies():
        if not install_dependencies():
            sys.exit(1)
    
    # Check environment configuration
    if not create_env_file():
        print("\n⚠️  Please edit the .env file and add your OpenAI API key!")
        print("Then run this script again to start the server.")
        sys.exit(1)
    
    # Check if OpenAI API key is set
    from dotenv import load_dotenv
    load_dotenv()
    
    if not os.getenv("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY") == "your_openai_api_key_here":
        print("\n⚠️  Please set your OpenAI API key in the .env file!")
        print("OPENAI_API_KEY=your_actual_api_key_here")
        sys.exit(1)
    
    # Start the server
    print("\n🎯 Starting server...")
    try:
        from src.main import main as start_server
        start_server()
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
