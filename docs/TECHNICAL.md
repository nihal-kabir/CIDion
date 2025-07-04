# Agentic AI System - Technical Documentation

## Architecture Overview

The Agentic AI system is built with a modular, extensible architecture that demonstrates key concepts in AI agent development:

### Core Components

#### 1. Agent (`src/agent/core.py`)
The main AI agent that orchestrates reasoning, planning, and execution:
- **Planning**: Analyzes user requests and creates step-by-step plans
- **Tool Integration**: Seamlessly calls available tools when needed
- **Memory Management**: Maintains conversation context and history
- **Error Handling**: Robust error handling and recovery

#### 2. Tool System (`src/tools/`)
Extensible tool framework with multiple implementations:
- **Base Framework**: Abstract tool interface for easy extension
- **File Operations**: Read, write, and list files
- **Web Tools**: Search and scrape web content
- **Calculator**: Safe mathematical expression evaluation
- **Tool Manager**: Centralized tool registration and execution

#### 3. Memory System (`src/memory/`)
Persistent conversation and session management:
- **SQLite Backend**: Reliable local storage
- **Session Management**: Track multiple conversation sessions
- **History Retrieval**: Context-aware conversation history
- **Metadata Support**: Extensible session and message metadata

#### 4. Web API (`src/api/`)
FastAPI-based REST API with modern web interface:
- **RESTful Endpoints**: Clean API design
- **Real-time Chat**: Interactive web interface
- **Session Management**: Persistent conversation sessions
- **Health Monitoring**: System status and diagnostics

## Key Features

### 🧠 Intelligent Planning
The agent analyzes requests and creates detailed execution plans before taking action, ensuring logical and efficient task completion.

### 🔧 Tool Calling
Seamless integration with external tools through OpenAI's function calling API, allowing the agent to:
- Perform calculations
- Read and write files
- Search the web
- Access real-time information

### 💾 Memory Management
Persistent conversation history with:
- Session-based organization
- Metadata tracking
- Efficient retrieval
- Context preservation

### 🌐 Web Interface
Modern, responsive web interface featuring:
- Real-time chat interaction
- Thought process visualization
- Tool usage tracking
- Clean, intuitive design

## Getting Started

### Prerequisites
- Python 3.8 or higher
- OpenAI API key

### Quick Setup
1. **Clone and Setup**:
   ```bash
   python setup.py
   ```

2. **Configure Environment**:
   Edit `.env` file and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

3. **Run the Server**:
   ```bash
   python -m src.main
   ```

4. **Access Web Interface**:
   Open http://localhost:8000

### Development Mode
Use VS Code's integrated debugging:
- Press F5 to start in debug mode
- Use the "Run Agentic AI Server" configuration

## API Usage

### Chat Endpoint
```python
import requests

response = requests.post("http://localhost:8000/api/chat", json={
    "message": "Calculate the square root of 144 and then search for information about mathematics",
    "session_id": "optional_session_id"
})
```

### Health Check
```python
response = requests.get("http://localhost:8000/api/health")
print(response.json())  # Shows available tools and system status
```

## Extending the System

### Adding New Tools
1. Create a new tool class inheriting from `Tool`:
   ```python
   from src.tools.base import Tool
   
   class MyCustomTool(Tool):
       @property
       def name(self) -> str:
           return "my_custom_tool"
       
       # Implement required methods...
   ```

2. Register in tool manager:
   ```python
   # In src/tools/__init__.py
   manager.register_tool(MyCustomTool())
   ```

### Customizing the Agent
The agent behavior can be customized by:
- Modifying prompt templates
- Adjusting model parameters
- Adding new planning strategies
- Implementing custom memory strategies

## Configuration

Key configuration options in `src/config.py`:
- **Model Selection**: Choose different OpenAI models
- **Memory Settings**: Adjust conversation history limits
- **Tool Configuration**: Enable/disable specific tools
- **API Settings**: Host, port, and security settings

## Testing

Run the test suite:
```bash
pytest tests/
```

Test coverage includes:
- Tool functionality
- Memory operations
- Agent behavior
- API endpoints

## Deployment

For production deployment:
1. Set up environment variables
2. Configure database backend
3. Use production WSGI server
4. Implement security measures
5. Set up monitoring and logging

## Security Considerations

- **API Key Management**: Store securely, never commit to version control
- **Input Validation**: All user inputs are validated
- **Safe Execution**: Calculator uses AST parsing for safe evaluation
- **Rate Limiting**: Implement rate limiting in production
- **Error Handling**: Sensitive information is not exposed in error messages

## Performance Notes

- **Memory Usage**: SQLite provides efficient local storage
- **Tool Execution**: Tools run asynchronously for better performance
- **Caching**: Consider implementing response caching for production
- **Scaling**: Design supports horizontal scaling with external databases

## Troubleshooting

### Common Issues
1. **Import Errors**: Ensure all dependencies are installed
2. **API Key Issues**: Verify OpenAI API key is set correctly
3. **Port Conflicts**: Change port in configuration if 8000 is occupied
4. **Database Issues**: Check file permissions for SQLite database

### Debug Mode
Enable debug logging by setting `LOG_LEVEL=DEBUG` in `.env` file.

## Contributing

The codebase follows:
- **PEP 8** style guidelines
- **Type hints** throughout
- **Comprehensive docstrings**
- **Async/await** for I/O operations
- **Dependency injection** for testability

## License

MIT License - see LICENSE file for details.
