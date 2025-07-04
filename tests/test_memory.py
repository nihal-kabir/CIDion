"""
Test the memory system.
"""
import pytest
from src.memory import ConversationMemory

@pytest.mark.asyncio
async def test_conversation_memory(temp_db):
    """Test conversation memory functionality."""
    memory = temp_db
    session_id = "test_session"
    
    # Add messages
    await memory.add_message(session_id, "user", "Hello")
    await memory.add_message(session_id, "assistant", "Hi there!")
    
    # Get history
    history = await memory.get_conversation_history(session_id)
    
    assert len(history) == 2
    assert history[0]["role"] == "user"
    assert history[0]["content"] == "Hello"
    assert history[1]["role"] == "assistant"
    assert history[1]["content"] == "Hi there!"

@pytest.mark.asyncio
async def test_session_management(temp_db):
    """Test session management."""
    memory = temp_db
    session_id = "test_session"
    
    # Add a message to create session
    await memory.add_message(session_id, "user", "Test message")
    
    # Update session title
    await memory.update_session_title(session_id, "Test Session")
    
    # Get recent sessions
    sessions = await memory.get_recent_sessions()
    
    assert len(sessions) >= 1
    assert any(s["session_id"] == session_id for s in sessions)

@pytest.mark.asyncio
async def test_session_stats(temp_db):
    """Test session statistics."""
    memory = temp_db
    session_id = "test_session"
    
    # Add multiple messages
    await memory.add_message(session_id, "user", "Message 1")
    await memory.add_message(session_id, "assistant", "Response 1")
    await memory.add_message(session_id, "user", "Message 2")
    
    # Get stats
    stats = await memory.get_session_stats(session_id)
    
    assert stats["message_count"] == 3
    assert stats["first_message"] is not None
    assert stats["last_message"] is not None
