"""
Conversation memory management for the agent.
"""
import json
import os
import aiofiles
from typing import List, Dict, Any, Optional
from datetime import datetime
import sqlite3
import aiosqlite

class ConversationMemory:
    """Manages conversation history and context."""
    
    def __init__(self, db_path: str = "data/conversations.db"):
        """Initialize conversation memory with SQLite backend."""
        self.db_path = db_path
        self._ensure_db_exists()
    
    def _ensure_db_exists(self):
        """Ensure the database and tables exist."""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        # Create tables if they don't exist
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                metadata TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS session_metadata (
                session_id TEXT PRIMARY KEY,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                last_activity DATETIME DEFAULT CURRENT_TIMESTAMP,
                title TEXT,
                summary TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    async def add_message(self, session_id: str, role: str, content: str, metadata: Optional[Dict] = None):
        """Add a message to the conversation history."""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "INSERT INTO conversations (session_id, role, content, metadata) VALUES (?, ?, ?, ?)",
                (session_id, role, content, json.dumps(metadata) if metadata else None)
            )
            
            # Update session metadata
            await db.execute(
                """INSERT OR REPLACE INTO session_metadata 
                   (session_id, created_at, last_activity) 
                   VALUES (?, COALESCE((SELECT created_at FROM session_metadata WHERE session_id = ?), CURRENT_TIMESTAMP), CURRENT_TIMESTAMP)""",
                (session_id, session_id)
            )
            
            await db.commit()
    
    async def get_conversation_history(self, session_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Get conversation history for a session."""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                """SELECT role, content, timestamp, metadata 
                   FROM conversations 
                   WHERE session_id = ? 
                   ORDER BY timestamp DESC 
                   LIMIT ?""",
                (session_id, limit)
            )
            
            rows = await cursor.fetchall()
            
            history = []
            for row in rows:
                history.append({
                    "role": row[0],
                    "content": row[1],
                    "timestamp": row[2],
                    "metadata": json.loads(row[3]) if row[3] else None
                })
            
            return list(reversed(history))  # Return in chronological order
    
    async def get_recent_sessions(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent conversation sessions."""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                """SELECT session_id, created_at, last_activity, title, summary
                   FROM session_metadata 
                   ORDER BY last_activity DESC 
                   LIMIT ?""",
                (limit,)
            )
            
            rows = await cursor.fetchall()
            
            sessions = []
            for row in rows:
                sessions.append({
                    "session_id": row[0],
                    "created_at": row[1],
                    "last_activity": row[2],
                    "title": row[3],
                    "summary": row[4]
                })
            
            return sessions
    
    async def update_session_title(self, session_id: str, title: str):
        """Update the title for a session."""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "UPDATE session_metadata SET title = ? WHERE session_id = ?",
                (title, session_id)
            )
            await db.commit()
    
    async def update_session_summary(self, session_id: str, summary: str):
        """Update the summary for a session."""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "UPDATE session_metadata SET summary = ? WHERE session_id = ?",
                (summary, session_id)
            )
            await db.commit()
    
    async def clear_session(self, session_id: str):
        """Clear conversation history for a session."""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("DELETE FROM conversations WHERE session_id = ?", (session_id,))
            await db.execute("DELETE FROM session_metadata WHERE session_id = ?", (session_id,))
            await db.commit()
    
    async def get_session_stats(self, session_id: str) -> Dict[str, Any]:
        """Get statistics for a session."""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                """SELECT COUNT(*) as message_count,
                          MIN(timestamp) as first_message,
                          MAX(timestamp) as last_message
                   FROM conversations 
                   WHERE session_id = ?""",
                (session_id,)
            )
            
            row = await cursor.fetchone()
            
            return {
                "message_count": row[0],
                "first_message": row[1],
                "last_message": row[2]
            }
