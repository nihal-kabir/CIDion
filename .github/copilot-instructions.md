# Copilot Instructions for Agentic AI Project

<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

## Project Overview
This is an end-to-end agentic AI project that demonstrates:
- AI agent with tool calling capabilities
- Task planning and execution
- Memory management
- Web interface for interaction
- Multiple tools (file ops, web search, calculator)

## Code Style Guidelines
- Use Python type hints throughout
- Follow PEP 8 style guidelines
- Use async/await for I/O operations
- Implement proper error handling
- Add comprehensive docstrings
- Use dependency injection for better testability

## Architecture Patterns
- Agent-based architecture with tool calling
- Repository pattern for data access
- Factory pattern for tool creation
- Observer pattern for event handling
- Dependency injection for loose coupling

## Key Components
- `Agent`: Main AI agent with planning and execution
- `ToolManager`: Manages available tools
- `Memory`: Persistent storage for conversations and tasks
- `WebAPI`: FastAPI backend for web interface
- `Frontend`: Simple HTML/JS interface
