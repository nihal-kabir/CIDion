# Agentic AI Project

A complete end-to-end agentic AI system that demonstrates AI agent capabilities with tool calling, task planning, memory management, and a web interface.

## Features

- **AI Agent**: LLM-powered agent with reasoning and tool calling
- **Tool System**: Extensible tools for file operations, web search, calculations
- **Memory Management**: Persistent conversation and task memory
- **Task Planning**: Multi-step task breakdown and execution
- **Web Interface**: Clean, responsive frontend for agent interaction
- **API Backend**: FastAPI-based REST API

## Architecture

```
├── src/
│   ├── agent/          # Core AI agent logic
│   ├── tools/          # Tool implementations
│   ├── memory/         # Memory management
│   ├── api/            # FastAPI backend
│   └── frontend/       # Web interface
├── tests/              # Test suite
├── data/               # Data storage
└── docs/               # Documentation
```

## Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment Setup**
   ```bash
   cp .env.example .env
   # Edit .env with your OpenAI API key
   ```

3. **Run the Application**
   ```bash
   python -m src.main
   ```

4. **Access Web Interface**
   Open http://localhost:8000 in your browser

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

- `OPENAI_API_KEY`: Your OpenAI API key
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
