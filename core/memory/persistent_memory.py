"""
Persistent Memory System for Jarvis.
Provides long-term memory, learning, and context awareness across sessions.
"""
import json
import sqlite3
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
from core.utils.log import logger


class PersistentMemory:
    def __init__(self, brain):
        self.brain = brain
        self.jarvis_root = Path(__file__).parent.parent.parent
        self.memory_dir = self.jarvis_root / "memory"
        self.memory_dir.mkdir(exist_ok=True)
        
        # Initialize databases
        self.conversation_db = self.memory_dir / "conversations.db"
        self.knowledge_db = self.memory_dir / "knowledge.db"
        self.preferences_db = self.memory_dir / "preferences.db"
        
        self._init_databases()
        self.session_id = self._generate_session_id()
        
    def _init_databases(self):
        """Initialize all memory databases."""
        # Conversations database
        with sqlite3.connect(self.conversation_db) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT,
                    timestamp DATETIME,
                    user_input TEXT,
                    jarvis_response TEXT,
                    context TEXT,
                    sentiment REAL,
                    importance INTEGER
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS sessions (
                    session_id TEXT PRIMARY KEY,
                    start_time DATETIME,
                    end_time DATETIME,
                    total_interactions INTEGER,
                    session_summary TEXT
                )
            """)
        
        # Knowledge database
        with sqlite3.connect(self.knowledge_db) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS facts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    topic TEXT,
                    fact TEXT,
                    source TEXT,
                    confidence REAL,
                    timestamp DATETIME,
                    last_accessed DATETIME
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS learned_patterns (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    pattern_type TEXT,
                    pattern_data TEXT,
                    frequency INTEGER,
                    last_seen DATETIME
                )
            """)
        
        # Preferences database
        with sqlite3.connect(self.preferences_db) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS user_preferences (
                    key TEXT PRIMARY KEY,
                    value TEXT,
                    category TEXT,
                    last_updated DATETIME
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS project_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    project_name TEXT,
                    project_path TEXT,
                    last_accessed DATETIME,
                    access_count INTEGER,
                    project_type TEXT,
                    notes TEXT
                )
            """)

    def _generate_session_id(self) -> str:
        """Generate unique session ID."""
        timestamp = datetime.now().isoformat()
        return hashlib.md5(timestamp.encode()).hexdigest()[:12]

    def remember_conversation(self, user_input: str, jarvis_response: str, context: Dict = None):
        """Store conversation in memory."""
        try:
            # Analyze sentiment and importance
            sentiment = self._analyze_sentiment(user_input)
            importance = self._calculate_importance(user_input, context)
            
            with sqlite3.connect(self.conversation_db) as conn:
                conn.execute("""
                    INSERT INTO conversations 
                    (session_id, timestamp, user_input, jarvis_response, context, sentiment, importance)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    self.session_id,
                    datetime.now(),
                    user_input,
                    jarvis_response,
                    json.dumps(context or {}),
                    sentiment,
                    importance
                ))
                
        except Exception as e:
            logger.error(f"Error storing conversation: {e}")

    def learn_fact(self, topic: str, fact: str, source: str = "user", confidence: float = 0.8):
        """Learn and store a new fact."""
        try:
            with sqlite3.connect(self.knowledge_db) as conn:
                conn.execute("""
                    INSERT OR REPLACE INTO facts 
                    (topic, fact, source, confidence, timestamp, last_accessed)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (topic, fact, source, confidence, datetime.now(), datetime.now()))
                
        except Exception as e:
            logger.error(f"Error storing fact: {e}")

    def recall_facts(self, topic: str, limit: int = 5) -> List[Dict]:
        """Recall facts about a topic."""
        try:
            with sqlite3.connect(self.knowledge_db) as conn:
                cursor = conn.execute("""
                    SELECT fact, source, confidence, timestamp 
                    FROM facts 
                    WHERE topic LIKE ? 
                    ORDER BY confidence DESC, last_accessed DESC 
                    LIMIT ?
                """, (f"%{topic}%", limit))
                
                facts = []
                for row in cursor.fetchall():
                    facts.append({
                        'fact': row[0],
                        'source': row[1],
                        'confidence': row[2],
                        'timestamp': row[3]
                    })
                
                # Update last_accessed
                conn.execute("""
                    UPDATE facts 
                    SET last_accessed = ? 
                    WHERE topic LIKE ?
                """, (datetime.now(), f"%{topic}%"))
                
                return facts
                
        except Exception as e:
            logger.error(f"Error recalling facts: {e}")
            return []

    def get_conversation_context(self, lookback_minutes: int = 30) -> str:
        """Get recent conversation context."""
        try:
            cutoff_time = datetime.now() - timedelta(minutes=lookback_minutes)
            
            with sqlite3.connect(self.conversation_db) as conn:
                cursor = conn.execute("""
                    SELECT user_input, jarvis_response, timestamp 
                    FROM conversations 
                    WHERE session_id = ? AND timestamp > ?
                    ORDER BY timestamp DESC 
                    LIMIT 10
                """, (self.session_id, cutoff_time))
                
                context = "Recent conversation context:\n"
                for row in cursor.fetchall():
                    context += f"User: {row[0]}\nJarvis: {row[1]}\n---\n"
                
                return context
                
        except Exception as e:
            logger.error(f"Error getting context: {e}")
            return ""

    def save_preference(self, key: str, value: Any, category: str = "general"):
        """Save user preference."""
        try:
            with sqlite3.connect(self.preferences_db) as conn:
                conn.execute("""
                    INSERT OR REPLACE INTO user_preferences 
                    (key, value, category, last_updated)
                    VALUES (?, ?, ?, ?)
                """, (key, json.dumps(value), category, datetime.now()))
                
        except Exception as e:
            logger.error(f"Error saving preference: {e}")

    def get_preference(self, key: str, default: Any = None) -> Any:
        """Get user preference."""
        try:
            with sqlite3.connect(self.preferences_db) as conn:
                cursor = conn.execute("""
                    SELECT value FROM user_preferences WHERE key = ?
                """, (key,))
                
                row = cursor.fetchone()
                if row:
                    return json.loads(row[0])
                return default
                
        except Exception as e:
            logger.error(f"Error getting preference: {e}")
            return default

    def track_project_usage(self, project_name: str, project_path: str, project_type: str = "web"):
        """Track project usage for learning user patterns."""
        try:
            with sqlite3.connect(self.preferences_db) as conn:
                # Check if project exists
                cursor = conn.execute("""
                    SELECT access_count FROM project_history 
                    WHERE project_name = ? AND project_path = ?
                """, (project_name, project_path))
                
                row = cursor.fetchone()
                if row:
                    # Update existing
                    conn.execute("""
                        UPDATE project_history 
                        SET last_accessed = ?, access_count = access_count + 1
                        WHERE project_name = ? AND project_path = ?
                    """, (datetime.now(), project_name, project_path))
                else:
                    # Insert new
                    conn.execute("""
                        INSERT INTO project_history 
                        (project_name, project_path, last_accessed, access_count, project_type)
                        VALUES (?, ?, ?, 1, ?)
                    """, (project_name, project_path, datetime.now(), project_type))
                    
        except Exception as e:
            logger.error(f"Error tracking project: {e}")

    def get_frequently_used_projects(self, limit: int = 5) -> List[Dict]:
        """Get most frequently used projects."""
        try:
            with sqlite3.connect(self.preferences_db) as conn:
                cursor = conn.execute("""
                    SELECT project_name, project_path, access_count, last_accessed, project_type
                    FROM project_history 
                    ORDER BY access_count DESC, last_accessed DESC 
                    LIMIT ?
                """, (limit,))
                
                projects = []
                for row in cursor.fetchall():
                    projects.append({
                        'name': row[0],
                        'path': row[1],
                        'access_count': row[2],
                        'last_accessed': row[3],
                        'type': row[4]
                    })
                
                return projects
                
        except Exception as e:
            logger.error(f"Error getting frequent projects: {e}")
            return []

    def _analyze_sentiment(self, text: str) -> float:
        """Analyze sentiment of user input."""
        # Simple sentiment analysis - could be enhanced with ML
        positive_words = ['good', 'great', 'awesome', 'perfect', 'excellent', 'love', 'like']
        negative_words = ['bad', 'terrible', 'awful', 'hate', 'dislike', 'wrong', 'error']
        
        text_lower = text.lower()
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count + negative_count == 0:
            return 0.0  # Neutral
        
        return (positive_count - negative_count) / (positive_count + negative_count)

    def _calculate_importance(self, user_input: str, context: Dict = None) -> int:
        """Calculate importance of interaction (1-10)."""
        importance = 5  # Base importance
        
        # Increase importance for certain keywords
        high_importance_keywords = ['error', 'bug', 'fix', 'urgent', 'important', 'critical']
        medium_importance_keywords = ['create', 'build', 'deploy', 'enhance', 'improve']
        
        text_lower = user_input.lower()
        
        for keyword in high_importance_keywords:
            if keyword in text_lower:
                importance += 2
                
        for keyword in medium_importance_keywords:
            if keyword in text_lower:
                importance += 1
        
        # Cap at 10
        return min(importance, 10)

    def generate_insights(self) -> str:
        """Generate insights about user patterns and preferences."""
        try:
            insights = "🧠 **Memory Insights:**\n\n"
            
            # Most used projects
            frequent_projects = self.get_frequently_used_projects(3)
            if frequent_projects:
                insights += "**Most Used Projects:**\n"
                for project in frequent_projects:
                    insights += f"• {project['name']} ({project['access_count']} times)\n"
                insights += "\n"
            
            # Recent activity summary
            with sqlite3.connect(self.conversation_db) as conn:
                cursor = conn.execute("""
                    SELECT COUNT(*) FROM conversations 
                    WHERE timestamp > datetime('now', '-24 hours')
                """)
                daily_interactions = cursor.fetchone()[0]
                
                cursor = conn.execute("""
                    SELECT AVG(sentiment) FROM conversations 
                    WHERE timestamp > datetime('now', '-7 days')
                """)
                avg_sentiment = cursor.fetchone()[0] or 0
                
            insights += f"**Recent Activity:**\n"
            insights += f"• {daily_interactions} interactions today\n"
            insights += f"• Average sentiment: {'Positive' if avg_sentiment > 0.1 else 'Negative' if avg_sentiment < -0.1 else 'Neutral'}\n\n"
            
            # Learning summary
            with sqlite3.connect(self.knowledge_db) as conn:
                cursor = conn.execute("SELECT COUNT(*) FROM facts")
                fact_count = cursor.fetchone()[0]
                
            insights += f"**Knowledge Base:**\n"
            insights += f"• {fact_count} facts learned\n"
            
            return insights
            
        except Exception as e:
            logger.error(f"Error generating insights: {e}")
            return "Unable to generate insights at this time."
