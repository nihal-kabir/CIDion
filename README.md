# CIDion AI - Intelligent Assistant with Tool Calling

**🌟 Live Demo: [https://cidion-bol-bsdk.onrender.com](https://cidion-bol-bsdk.onrender.com)**

A complete end-to-end agentic AI system powered by Google Gemini API that demonstrates AI agent capabilities with tool calling, task planning, memory management, and a clean web interface.

## 🚀 Features

- **🤖 AI Agent**: Gemini-1.5-flash powered agent with reasoning and tool calling
- **🛠️ Tool System**: 6 extensible tools for file operations, web search, calculations
- **🧠 Memory Management**: Persistent conversation and task memory with SQLite
- **📋 Task Planning**: Multi-step task breakdown and execution
- **🌐 Web Interface**: Clean, responsive frontend with modern design
- **📡 API Backend**: FastAPI-based REST API with full documentation
- **☁️ Cloud Ready**: Deployed on Render.com with public access
- **🎨 Custom UI**: Professional interface with Roboto Serif fonts and clean messaging

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
├── Dockerfile          # Container configuration
├── Procfile           # Deployment configuration
├── render.yaml        # Render.com deployment config
└── DEPLOY.md          # Deployment guide
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
PORT=8001
```

### ⚠️ Security Important

**🔒 API Key Protection**
- Your `.env` file contains sensitive information (API keys)
- The `.env` file is automatically excluded from git commits via `.gitignore`
- **Never commit API keys to git repositories**
- Use `.env.example` as a template for others

**🎯 Getting Your Gemini API Key**
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key and paste it in your `.env` file

**🚨 If you accidentally commit API keys:**
1. Immediately revoke the key at Google AI Studio
2. Generate a new API key
3. Update your `.env` file with the new key
4. Consider using `git filter-branch` to remove from history

### 3. Start the Application

**Option A: Simple startup**
```bash
python -m uvicorn src.api.app:create_app --factory --host localhost --port 8001 --reload
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
- **🌐 Live Demo**: https://cidion-bol-bsdk.onrender.com
- **🏠 Local Web Interface**: http://localhost:8001
- **📚 API Documentation**: http://localhost:8001/docs
- **❤️ Health Check**: http://localhost:8001/api/health

## 💬 Usage Examples

### Via Live Demo
1. Visit [https://cidion-bol-bsdk.onrender.com](https://cidion-bol-bsdk.onrender.com)
2. Wait 30-60 seconds for initial load (free tier limitation)
3. Type your question: *"Calculate 25 * 17 and explain the result"*
4. Watch CIDion respond with clean, professional answers

### Via Local Installation
1. Open http://localhost:8001 in your browser
2. Type your question: *"Search for latest AI news"*
3. Watch CIDion plan and execute using available tools

### Via API
```bash
curl -X POST "https://cidion-bol-bsdk.onrender.com/api/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Search for the latest AI news and summarize the top 3 articles"
  }'
```

### Python Integration
```python
import requests

response = requests.post("https://cidion-bol-bsdk.onrender.com/api/chat", json={
    "message": "List files in the current directory and read any README file"
})

result = response.json()
print(result["response"])
```

## 🌐 Live Deployment

**Public URL**: [https://cidion-bol-bsdk.onrender.com](https://cidion-bol-bsdk.onrender.com)

### Deployment Features:
- ✅ **Free hosting** on Render.com
- ✅ **Public access** - share with anyone
- ✅ **Auto-deployment** from GitHub
- ✅ **HTTPS enabled** by default
- ✅ **Global CDN** for fast access

### Important Notes:
- **Cold Start**: First request may take 30-60 seconds (free tier)
- **Sleep Mode**: App sleeps after 15 minutes of inactivity
- **Wake Up**: Subsequent requests wake the app automatically

## 🚀 Deploy Your Own

Want to deploy your own version? Check out our [deployment guide](DEPLOY.md) for step-by-step instructions for:

- **Render.com** (recommended)
- **Railway.app**
- **Fly.io**
- **Vercel**

All deployment files are included in this repository!
    "message": "Search for the latest AI news and summarize the top 3 articles"
  }'
```

### Python Integration
```python
import requests

response = requests.post("http://localhost:8001/api/chat", json={
    "message": "List files in the current directory and read any README file"
})

result = response.json()
print(result["response"])
```

## 🧪 Testing

### Live Demo Test
Visit [https://cidion-bol-bsdk.onrender.com](https://cidion-bol-bsdk.onrender.com) and try:
- "Calculate 25 * 17"
- "Search for latest AI news"
- "Help me with Python coding"

### Local Integration Test
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
🔧 Tools used: 1
📋 Steps: 1
🎉 Gemini integration test passed!
```

### Run Unit Tests
```bash
pytest tests/
```

## 🔧 Configuration

### Environment Variables
Set these in your `.env` file for local development:

| Variable | Description | Default |
|----------|-------------|---------|
| `GEMINI_API_KEY` | Your Google Gemini API key | Required |
| `LOG_LEVEL` | Logging level (DEBUG, INFO, WARNING, ERROR) | INFO |
| `HOST` | Server host address | localhost |
| `PORT` | Server port number | 8001 |
| `DATABASE_URL` | SQLite database path | sqlite:///data/agent.db |

### Getting Gemini API Key
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the key to your `.env` file (for local) or deployment platform

## 🎮 How It Works

1. **User Input**: Send a message via web interface or API
2. **AI Processing**: CIDion (Gemini-powered) analyzes the request
3. **Tool Selection**: Automatically determines which tools are needed
4. **Execution**: Runs tools and gathers results
5. **Clean Response**: Provides a professional answer (no debug clutter)
6. **Memory**: Stores conversation for context in future interactions

## 🎨 User Interface

CIDion features a modern, clean interface with:
- **Custom Branding**: "Bol bsdk, kya chahiye tereko?" heading
- **Professional Fonts**: Roboto Serif for headings, Trebuchet MS for chat
- **Responsive Design**: Works on desktop and mobile
- **Clean Messaging**: Only shows AI responses (no debug info by default)
- **Welcome Box**: Centered introduction with available capabilities

## 🔌 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Web interface |
| `/api/chat` | POST | Send message to CIDion |
| `/api/sessions` | GET | Get conversation history |
| `/api/health` | GET | System health check |
| `/docs` | GET | Interactive API documentation |

**Live API**: All endpoints available at https://cidion-bol-bsdk.onrender.com

## 🛡️ Error Handling

CIDion includes robust error handling:
- **API Failures**: Graceful degradation when tools fail
- **Invalid Input**: Clear error messages for malformed requests
- **Network Issues**: Retry logic for external API calls
- **Memory Errors**: Automatic database recovery
- **Deployment Issues**: Health checks and monitoring

## 🚀 Performance

- **Response Time**: 2-5 seconds for complex queries
- **Concurrency**: Supports multiple simultaneous users
- **Memory Usage**: Efficient SQLite-based storage
- **Scalability**: Production-ready deployment
- **Global Access**: Available worldwide via Render.com

## 🔄 Recent Updates

- ✅ **v1.0.0**: Initial release with Gemini integration
- ✅ **v1.1.0**: Clean UI with professional fonts and branding
- ✅ **v1.2.0**: Live deployment on Render.com
- ✅ **v1.3.0**: Optimized user experience (no debug clutter)
- ✅ **v1.4.0**: Mobile-responsive design and performance improvements
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

**Live Demo Not Loading**
- Wait 30-60 seconds for the free tier to wake up
- Try refreshing the page
- Check [https://cidion-bol-bsdk.onrender.com/api/health](https://cidion-bol-bsdk.onrender.com/api/health)

**Local Setup Issues**

**"GEMINI_API_KEY not found"**
- Ensure your `.env` file exists and contains the API key
- Check the key is valid at Google AI Studio

**"Module not found" errors**
- Run `pip install -r requirements.txt`
- Ensure you're in the project root directory

**Server won't start locally**
- Check if port 8001 is already in use
- Try a different port: `--port 8002`

**Tools not working**
- Check internet connection for web search
- Verify file permissions for file operations
- Ensure Gemini API key is valid and has sufficient quota

### Getting Help

- 📧 Check the logs for detailed error messages
- 🧪 Run the test suite to verify installation: `python test_gemini.py`
- 📚 Review the API documentation at `/docs`
- 🌐 Try the live demo first: [https://cidion-bol-bsdk.onrender.com](https://cidion-bol-bsdk.onrender.com)

### Deployment Issues

- Check [DEPLOY.md](DEPLOY.md) for detailed deployment instructions
- Verify environment variables are set correctly on your platform
- Monitor the deployment logs for specific error messages

---

**CIDion AI** - Your intelligent assistant that thinks, plans, and acts! 🤖✨

**🌟 Try it now: [https://cidion-bol-bsdk.onrender.com](https://cidion-bol-bsdk.onrender.com)**
