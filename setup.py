#!/usr/bin/env python3
"""
Setup script for the Agentic AI project.
"""
import os
import sys
import subprocess
from pathlib import Path

def main():
    """Setup the project environment."""
    print("🚀 Setting up Agentic AI Project")
    print("=" * 40)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required!")
        sys.exit(1)
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Create .env file if it doesn't exist
    env_file = Path(".env")
    if not env_file.exists():
        print("📝 Creating .env file from template...")
        example_env = Path(".env.example")
        if example_env.exists():
            env_file.write_text(example_env.read_text())
            print("✅ .env file created")
            print("⚠️  Please edit .env and add your OpenAI API key!")
        else:
            print("❌ .env.example not found")
    
    # Create data directory
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    print("✅ Data directory created")
    
    # Install dependencies
    print("📦 Installing dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True)
        print("✅ Dependencies installed")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        sys.exit(1)
    
    print("\\n🎉 Setup complete!")
    print("\\nNext steps:")
    print("1. Edit .env file and add your OpenAI API key")
    print("2. Run the server: python -m src.main")
    print("3. Open http://localhost:8000 in your browser")
    print("\\nOr run the example: python example.py")

if __name__ == "__main__":
    main()
