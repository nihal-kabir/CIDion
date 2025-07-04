"""
Test configuration and fixtures.
"""
import pytest
import asyncio
import os
import tempfile
from src.tools import create_tool_manager
from src.memory import ConversationMemory

@pytest.fixture
def tool_manager():
    """Create a tool manager for testing."""
    return create_tool_manager()

@pytest.fixture
def temp_db():
    """Create a temporary database for testing."""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
        db_path = f.name
    
    memory = ConversationMemory(db_path)
    yield memory
    
    # Cleanup
    os.unlink(db_path)

@pytest.fixture
def event_loop():
    """Create an event loop for async tests."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()
