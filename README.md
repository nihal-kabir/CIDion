# CIDion AI - Intelligent Assistant with Tool Calling

A complete end-to-end agentic AI system powered by Google Gemini API that demonstrates AI agent capabilities with tool calling, task planning, memory management, and a clean web interface.

## 🚀 Features

- **🤖 AI Agent**: Gemini-1.5-flash powered agent with reasoning and tool calling
- **🛠️ Tool System**: Extensible tools for file operations, web search, calculations
- **🧠 Memory Management**: Persistent conversation and task memory with SQLite
- **📋 Task Planning**: Multi-step task breakdown and execution
- **🌐 Web Interface**: Clean, responsive frontend for agent interaction
- **📡 API Backend**: FastAPI-based REST API with full documentation
- **🔧 Debug Mode**: Optional transparency into agent's thinking process

## 🏗️ Architecture

```
copilot/
├── src/
│   ├── agent/          # Core AI agent logic with Gemini integration
│   ├── tools/          # Tool implementations (6 tools available)
│   ├── memory/         # SQLite-based conversation memory
│   ├── api/            # FastAPI backend with web interface
│   └── main.py         # Application entry point
├── .env                # Environment configuration
├── requirements.txt    # Python dependencies
├── start.sh/.bat       # Easy startup scripts
└── test_gemini.py      # Integration tests
```

## 🛠️ Available Tools

1. **📊 Calculator** - Mathematical expressions and calculations
2. **🔍 Web Search** - DuckDuckGo search integration
3. **🌐 Web Scraping** - Extract content from webpages
4. **📖 File Read** - Read file contents
5. **✏️ File Write** - Write content to files
6. **📁 File List** - Directory and file listing

## ⚡ Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Environment Setup
```bash
cp .env.example .env
# Edit .env with your Gemini API key
```

Your `.env` file should contain:
```env
GEMINI_API_KEY=your_gemini_api_key_here
LOG_LEVEL=INFO
HOST=localhost
PORT=8000
```

### 3. Start the Application

**Option A: Simple startup**
```bash
python -m uvicorn src.api.app:create_app --factory --host localhost --port 8000 --reload
```

**Option B: Use startup scripts**
```bash
./start.sh        # Linux/Mac
start.bat         # Windows
```

**Option C: Python script**
```bash
python run.py
```

### 4. Access the Application
- **🌐 Web Interface**: http://localhost:8000
- **📚 API Documentation**: http://localhost:8000/docs
- **❤️ Health Check**: http://localhost:8000/api/health

## 💬 Usage Examples

### Via Web Interface
1. Open http://localhost:8000 in your browser
2. Type your question: *"Calculate 15 * 27 and explain the result"*
3. Watch CIDion plan and execute using available tools
4. Toggle "Debug Mode" to see internal reasoning (optional)

### Via API
```bash
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Search for the latest AI news and summarize the top 3 articles"
  }'
```

### Python Integration
```python
import requests

response = requests.post("http://localhost:8000/api/chat", json={
    "message": "List files in the current directory and read any README file"
})

result = response.json()
print(result["response"])
```

## 🧪 Testing

### Run Integration Test
```bash
python test_gemini.py
```

### Expected Output
```
🧪 Testing Gemini API Integration...
✅ API key found
✅ Agent initialized
🤖 Testing with message: Hello! Can you help me calculate 15 + 27?
✅ Response received:
📝 Content: The calculation 15 + 27 equals 42...
🔧 Tools used: 13
📋 Steps: 13
🎉 Gemini integration test passed!
```

### Run Unit Tests
```bash
pytest tests/
```

## 🔧 Configuration

### Environment Variables
Set these in your `.env` file:

| Variable | Description | Default |
|----------|-------------|---------|
| `GEMINI_API_KEY` | Your Google Gemini API key | Required |
| `LOG_LEVEL` | Logging level (DEBUG, INFO, WARNING, ERROR) | INFO |
| `HOST` | Server host address | localhost |
| `PORT` | Server port number | 8000 |
| `DATABASE_URL` | SQLite database path | sqlite:///data/agent.db |

### Getting Gemini API Key
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the key to your `.env` file

## 🎮 How It Works

1. **User Input**: Send a message via web interface or API
2. **Planning**: CIDion analyzes the request and creates a step-by-step plan
3. **Tool Selection**: Automatically determines which tools are needed
4. **Execution**: Runs tools in sequence and gathers results
5. **Response**: Provides a comprehensive answer based on tool outputs
6. **Memory**: Stores conversation for context in future interactions

## 🔍 Debug Mode

CIDion includes an optional debug mode that shows:
- 🧠 **Thinking Process**: Step-by-step reasoning
- 🔧 **Tools Used**: Which tools were called and with what parameters
- 📋 **Execution Steps**: Detailed breakdown of actions taken

Toggle debug mode in the web interface to see behind-the-scenes operations.

## 🔌 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Web interface |
| `/api/chat` | POST | Send message to CIDion |
| `/api/sessions` | GET | Get conversation history |
| `/api/health` | GET | System health check |
| `/docs` | GET | Interactive API documentation |

## 🛡️ Error Handling

CIDion includes robust error handling:
- **API Failures**: Graceful degradation when tools fail
- **Invalid Input**: Clear error messages for malformed requests
- **Network Issues**: Retry logic for external API calls
- **Memory Errors**: Automatic database recovery

## 🚀 Performance

- **Response Time**: Typically 2-5 seconds for complex multi-tool queries
- **Concurrency**: Supports multiple simultaneous users
- **Memory Usage**: Efficient SQLite-based conversation storage
- **Scalability**: Ready for production deployment

## 🔄 Recent Updates

- ✅ **v1.0.0**: Initial release with Gemini integration
- ✅ **Clean UI**: Removed verbose debug output by default
- ✅ **Debug Toggle**: Optional transparency mode
- ✅ **Tool Optimization**: Improved tool selection and execution
- ✅ **Error Recovery**: Better handling of API failures

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if needed
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details.

## 🆘 Troubleshooting

### Common Issues

**"GEMINI_API_KEY not found"**
- Ensure your `.env` file exists and contains the API key
- Check the key is valid at Google AI Studio

**"Module not found" errors**
- Run `pip install -r requirements.txt`
- Ensure you're in the project root directory

**Server won't start**
- Check if port 8000 is already in use
- Try a different port: `--port 8001`

**Tools not working**
- Check internet connection for web search
- Verify file permissions for file operations
- Enable debug mode to see detailed error messages

### Getting Help

- 📧 Check the logs for detailed error messages
- 🔧 Enable debug mode in the web interface
- 📚 Review the API documentation at `/docs`
- 🧪 Run the test suite to verify installation

---

**CIDion AI** - Your intelligent assistant that thinks, plans, and acts! 🤖✨
