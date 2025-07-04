#!/bin/bash

# Agentic AI Startup Script
# This script starts the Agentic AI server

echo "🚀 Starting Agentic AI Server..."
echo "📍 Location: $(pwd)"
echo "🐍 Python: $(python --version)"
echo ""

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found!"
    echo "📝 Creating .env from example..."
    cp .env.example .env
    echo "✅ .env file created. Please edit it with your API keys."
    echo ""
fi

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv .venv
    echo "✅ Virtual environment created."
fi

# Activate virtual environment
if [ -f ".venv/Scripts/activate" ]; then
    echo "🔧 Activating virtual environment (Windows)..."
    source .venv/Scripts/activate
elif [ -f ".venv/bin/activate" ]; then
    echo "🔧 Activating virtual environment (Unix)..."
    source .venv/bin/activate
fi

# Install requirements
echo "📦 Installing requirements..."
pip install -r requirements.txt

echo ""
echo "🚀 Starting server..."
echo "📱 Web Interface: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo "🔧 Press Ctrl+C to stop"
echo "=" * 50

# Start the server
python -m uvicorn src.api.app:create_app --factory --host localhost --port 8000 --reload
