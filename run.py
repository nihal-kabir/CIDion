"""
Startup script for the Agentic AI application.
Run this from the project root directory.
"""
import os
import sys
import subprocess

def main():
    """Main startup function."""
    # Ensure we're in the project root
    project_root = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_root)
    
    # Add project root to Python path
    sys.path.insert(0, project_root)
    
    print("🚀 Starting Agentic AI Server...")
    print("📱 Web Interface: http://localhost:8000")
    print("📚 API Docs: http://localhost:8000/docs")
    print("🔧 Press Ctrl+C to stop")
    print("-" * 50)
    
    try:
        # Run with uvicorn
        subprocess.run([
            "uvicorn", 
            "src.api.app:create_app",
            "--factory",
            "--host", "localhost",
            "--port", "8000",
            "--reload"
        ], check=True)
    except KeyboardInterrupt:
        print("\n✅ Server stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error starting server: {e}")
        return 1
    except FileNotFoundError:
        print("❌ uvicorn not found. Please install requirements:")
        print("pip install -r requirements.txt")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
