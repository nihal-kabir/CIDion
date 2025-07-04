# 🚀 Agentic AI System Setup Guide

## Quick Start

1. **Set up your OpenAI API Key:**
   ```bash
   # Edit the .env file that was created
   OPENAI_API_KEY=your_actual_openai_api_key_here
   ```

2. **Run the application:**
   ```bash
   python start.py
   ```

3. **Access the web interface:**
   - Open your browser and go to: http://localhost:8000
   - Start chatting with your AI agent!

## Manual Setup (Alternative)

If you prefer to set up manually:

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Create environment file:**
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   ```

3. **Run the server:**
   ```bash
   python -m src.main
   ```

## Using VS Code

1. **Open the project in VS Code**
2. **Run tasks:**
   - Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
   - Type "Tasks: Run Task"
   - Select "Run Agentic AI Server"

3. **Debug the application:**
   - Press `F5` to start debugging
   - Choose "Run Agentic AI Server"

## Features Demonstration

### 1. Calculator Tool
```
Ask: "Calculate the square root of 144"
Result: AI will use the calculator tool to compute sqrt(144) = 12.0
```

### 2. Web Search Tool
```
Ask: "Search for the latest news about artificial intelligence"
Result: AI will search the web and provide summaries
```

### 3. File Operations
```
Ask: "Create a file called 'hello.txt' with the content 'Hello World'"
Result: AI will use file tools to create and write to the file
```

### 4. Complex Tasks
```
Ask: "Search for Python best practices, summarize the top 3 points, and save them to a file"
Result: AI will:
1. Search the web for Python best practices
2. Analyze and summarize the findings
3. Create a file with the summary
```

## API Endpoints

- `GET /` - Web interface
- `POST /api/chat` - Send messages to the agent
- `GET /api/tools` - List available tools
- `GET /api/sessions` - Get conversation sessions
- `GET /health` - Health check

## Development

### Running Tests
```bash
python -m pytest tests/ -v
```

### Code Formatting
```bash
black src/ tests/
```

### Linting
```bash
flake8 src/ tests/
```

### Type Checking
```bash
mypy src/
```

## Troubleshooting

### Common Issues

1. **"OpenAI API key not set" error:**
   - Make sure you've added your API key to the `.env` file
   - Verify the key is correct and has sufficient credits

2. **Import errors:**
   - Make sure all dependencies are installed: `pip install -r requirements.txt`
   - Check that you're in the correct directory

3. **Port already in use:**
   - Change the PORT in `.env` file to a different number (e.g., 8001)

### Getting Help

- Check the logs in the terminal for detailed error messages
- Ensure your OpenAI API key is valid and has credits
- Make sure Python 3.8+ is installed

## Architecture Overview

```
src/
├── agent/          # AI agent core logic
├── tools/          # Tool implementations
├── memory/         # Conversation memory
├── api/            # FastAPI backend
└── frontend/       # Web interface
```

## Next Steps

1. **Customize Tools:** Add your own tools in `src/tools/`
2. **Enhance UI:** Modify `src/frontend/index.html`
3. **Add Features:** Extend the agent capabilities
4. **Deploy:** Consider deploying to cloud platforms

Happy coding! 🎉
