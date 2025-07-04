# Ag## Features

- **AI Agent**: Gemini-powered agent with reasoning and tool calling
- **Tool System**: Extensible tools for file operations, web search, calculations
- **Memory Management**: Persistent conversation and task memory
- **Task Planning**: Multi-step task breakdown and execution
- **Web Interface**: Clean, responsive frontend for agent interaction
- **API Backend**: FastAPI-based REST API Project

A complete end-to-end agentic AI system that demonstrates AI agent capabilities with tool calling, task planning, memory management, and a web interface.

## Features

- **🤖 AI Agent**: LLM-powered agent with reasoning and tool calling
- **🔧 Tool System**: Extensible tools for file operations, web search, calculations
- **💾 Memory Management**: Persistent conversation and task memory
- **📋 Task Planning**: Multi-step task breakdown and execution
- **🌐 Web Interface**: Clean, responsive frontend for agent interaction
- **⚡ API Backend**: FastAPI-based REST API

## Quick Start

### Option 1: Automated Setup (Recommended)
```bash
# Run the setup script
python setup.py

# Edit .env file with your OpenAI API key
# OPENAI_API_KEY=your_api_key_here

# Start the server
python -m src.main
```

### Option 2: Manual Setup
1. **Install Dependencies**
   ```bash
   pip install fastapi uvicorn openai pydantic python-multipart aiofiles requests beautifulsoup4 python-dotenv jinja2 aiosqlite
   ```

2. **Environment Setup**
   ```bash
   cp .env.example .env
   # Edit .env with your Gemini API key
   ```

3. **Run the Application**
   ```bash
   python -m src.main
   ```

4. **Access Web Interface**
   Open http://localhost:8000 in your browser

## Project Structure

```
├── src/
│   ├── agent/          # Core AI agent logic
│   │   ├── core.py     # Main agent implementation
│   │   └── __init__.py
│   ├── tools/          # Tool implementations
│   │   ├── base.py     # Tool framework
│   │   ├── file_ops.py # File operations
│   │   ├── web_tools.py # Web search & scraping
│   │   ├── calculator.py # Mathematical calculations
│   │   └── __init__.py
│   ├── memory/         # Memory management
│   │   ├── conversation.py # Conversation storage
│   │   └── __init__.py
│   ├── api/            # FastAPI backend
│   │   ├── app.py      # Main API application
│   │   └── __init__.py
│   ├── config.py       # Configuration settings
│   └── main.py         # Application entry point
├── tests/              # Test suite
├── data/               # Data storage
├── docs/               # Documentation
├── .github/            # GitHub/Copilot configuration
├── .vscode/            # VS Code configuration
├── requirements.txt    # Python dependencies
├── setup.py           # Setup script
├── example.py         # Usage examples
└── README.md          # This file
```

## Usage

### Via Web Interface
1. Navigate to http://localhost:8000
2. Enter your task or question
3. Watch the agent plan and execute using available tools

### Via API
```python
import requests

response = requests.post("http://localhost:8000/api/chat", json={
    "message": "Search for the latest AI news and summarize the top 3 articles"
})
```

## Configuration

Set these environment variables in `.env`:

- `GEMINI_API_KEY`: Your Google Gemini API key
- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)
- `HOST`: Server host (default: localhost)
- `PORT`: Server port (default: 8000)

## Available Tools

- **File Operations**: Read, write, search files
- **Web Search**: Search and scrape web content
- **Calculator**: Mathematical calculations
- **Memory**: Store and retrieve information
- **Task Planner**: Break down complex tasks

## Development

### Running Tests
```bash
pytest tests/
```

### Code Style
```bash
black src/
flake8 src/
mypy src/
```

## License

MIT License - see LICENSE file for details
