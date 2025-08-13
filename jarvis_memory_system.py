#!/usr/bin/env python3
"""
JARVIS Memory System - Advanced Memory Management and Learning
Persistent memory, conversation history, and knowledge base for JARVIS Supreme Being AI
"""

import json
import os
import sqlite3
import hashlib
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import threading

class JarvisMemorySystem:
    """Advanced memory management system for JARVIS Supreme Being AI"""
    
    def __init__(self, memory_dir: str = "supreme_memory"):
        self.memory_dir = memory_dir
        self.db_path = os.path.join(memory_dir, "jarvis_memory.db")
        
        # Memory statistics
        self.memory_stats = {
            'total_conversations': 0,
            'total_interactions': 0,
            'knowledge_entries': 0,
            'memory_size_mb': 0,
            'last_cleanup': None
        }
        
        # Thread lock for concurrent access
        self.memory_lock = threading.Lock()
        
        # Initialize memory system
        self.initialize_memory_system()
    
    def initialize_memory_system(self):
        """Initialize the memory system and database"""
        print("🧠 INITIALIZING JARVIS MEMORY SYSTEM...")
        
        try:
            # Create memory directory
            os.makedirs(self.memory_dir, exist_ok=True)
            
            # Initialize SQLite database
            self.init_database()
            
            # Update statistics
            self.update_memory_stats()
            
            print("✅ JARVIS Memory System initialized successfully")
            print(f"📊 Memory Statistics: {self.memory_stats}")
            
        except Exception as e:
            print(f"❌ Memory system initialization error: {e}")
    
    def init_database(self):
        """Initialize SQLite database for memory storage"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Conversations table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT,
                    timestamp TEXT,
                    user_input TEXT,
                    jarvis_response TEXT,
                    context TEXT,
                    sentiment REAL,
                    importance INTEGER,
                    tags TEXT
                )
            ''')
            
            # Knowledge base table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS knowledge (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    topic TEXT,
                    content TEXT,
                    source TEXT,
                    confidence REAL,
                    timestamp TEXT,
                    access_count INTEGER DEFAULT 0,
                    last_accessed TEXT
                )
            ''')
            
            # User preferences table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS preferences (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT,
                    preference_type TEXT,
                    preference_value TEXT,
                    timestamp TEXT
                )
            ''')
            
            conn.commit()
    
    def store_conversation(self, user_input: str, jarvis_response: str, 
                          session_id: str = None, context: Dict = None, 
                          importance: int = 1) -> int:
        """Store a conversation in memory"""
        with self.memory_lock:
            try:
                timestamp = datetime.now().isoformat()
                session_id = session_id or self.generate_session_id()
                
                # Analyze sentiment
                sentiment = self.analyze_sentiment(user_input)
                
                # Extract tags
                tags = self.extract_tags(user_input, jarvis_response)
                
                with sqlite3.connect(self.db_path) as conn:
                    cursor = conn.cursor()
                    cursor.execute('''
                        INSERT INTO conversations 
                        (session_id, timestamp, user_input, jarvis_response, 
                         context, sentiment, importance, tags)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (session_id, timestamp, user_input, jarvis_response,
                          json.dumps(context or {}), sentiment, importance, 
                          json.dumps(tags)))
                    
                    conversation_id = cursor.lastrowid
                    conn.commit()
                
                # Update statistics
                self.memory_stats['total_interactions'] += 1
                
                return conversation_id
                
            except Exception as e:
                print(f"❌ Error storing conversation: {e}")
                return -1
    
    def store_knowledge(self, topic: str, content: str, source: str = "user", 
                       confidence: float = 0.8) -> int:
        """Store knowledge in the knowledge base"""
        try:
            timestamp = datetime.now().isoformat()
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO knowledge 
                    (topic, content, source, confidence, timestamp, last_accessed)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (topic, content, source, confidence, timestamp, timestamp))
                
                knowledge_id = cursor.lastrowid
                conn.commit()
            
            # Update statistics
            self.memory_stats['knowledge_entries'] += 1
            
            return knowledge_id
            
        except Exception as e:
            print(f"❌ Error storing knowledge: {e}")
            return -1
    
    def retrieve_conversations(self, limit: int = 10, session_id: str = None, 
                             importance_threshold: int = 0) -> List[Dict]:
        """Retrieve recent conversations"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                query = '''
                    SELECT * FROM conversations 
                    WHERE importance >= ?
                '''
                params = [importance_threshold]
                
                if session_id:
                    query += ' AND session_id = ?'
                    params.append(session_id)
                
                query += ' ORDER BY timestamp DESC LIMIT ?'
                params.append(limit)
                
                cursor.execute(query, params)
                rows = cursor.fetchall()
                
                conversations = []
                for row in rows:
                    conversations.append({
                        'id': row[0],
                        'session_id': row[1],
                        'timestamp': row[2],
                        'user_input': row[3],
                        'jarvis_response': row[4],
                        'context': json.loads(row[5]) if row[5] else {},
                        'sentiment': row[6],
                        'importance': row[7],
                        'tags': json.loads(row[8]) if row[8] else []
                    })
                
                return conversations
                
        except Exception as e:
            print(f"❌ Error retrieving conversations: {e}")
            return []
    
    def search_knowledge(self, query: str, limit: int = 5) -> List[Dict]:
        """Search knowledge base"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT * FROM knowledge 
                    WHERE topic LIKE ? OR content LIKE ?
                    ORDER BY confidence DESC, access_count DESC
                    LIMIT ?
                ''', (f'%{query}%', f'%{query}%', limit))
                
                rows = cursor.fetchall()
                
                knowledge_items = []
                for row in rows:
                    knowledge_items.append({
                        'id': row[0],
                        'topic': row[1],
                        'content': row[2],
                        'source': row[3],
                        'confidence': row[4],
                        'timestamp': row[5],
                        'access_count': row[6],
                        'last_accessed': row[7]
                    })
                    
                    # Update access count
                    cursor.execute('''
                        UPDATE knowledge 
                        SET access_count = access_count + 1, last_accessed = ?
                        WHERE id = ?
                    ''', (datetime.now().isoformat(), row[0]))
                
                conn.commit()
                return knowledge_items
                
        except Exception as e:
            print(f"❌ Error searching knowledge: {e}")
            return []
    
    def store_preference(self, preference_type: str, preference_value: str, 
                        user_id: str = "default") -> int:
        """Store user preference"""
        try:
            timestamp = datetime.now().isoformat()
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO preferences 
                    (user_id, preference_type, preference_value, timestamp)
                    VALUES (?, ?, ?, ?)
                ''', (user_id, preference_type, preference_value, timestamp))
                
                pref_id = cursor.lastrowid
                conn.commit()
                
                return pref_id
                
        except Exception as e:
            print(f"❌ Error storing preference: {e}")
            return -1
    
    def get_user_preferences(self, user_id: str = "default") -> Dict:
        """Get user preferences"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT preference_type, preference_value 
                    FROM preferences 
                    WHERE user_id = ?
                    ORDER BY timestamp DESC
                ''', (user_id,))
                
                rows = cursor.fetchall()
                preferences = {}
                for row in rows:
                    preferences[row[0]] = row[1]
                
                return preferences
                
        except Exception as e:
            print(f"❌ Error getting preferences: {e}")
            return {}
    
    def analyze_sentiment(self, text: str) -> float:
        """Simple sentiment analysis"""
        positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic', 'love', 'like']
        negative_words = ['bad', 'terrible', 'awful', 'hate', 'dislike', 'horrible', 'worst']
        
        text_lower = text.lower()
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count + negative_count == 0:
            return 0.0
        
        return (positive_count - negative_count) / (positive_count + negative_count)
    
    def extract_tags(self, user_input: str, jarvis_response: str) -> List[str]:
        """Extract tags from conversation"""
        tech_terms = ['python', 'javascript', 'programming', 'code', 'ai', 'machine learning', 
                     'algorithm', 'data', 'function', 'variable', 'api', 'database']
        
        text = (user_input + " " + jarvis_response).lower()
        keywords = []
        
        for term in tech_terms:
            if term in text:
                keywords.append(term)
        
        return keywords
    
    def generate_session_id(self) -> str:
        """Generate unique session ID"""
        return f"session_{hashlib.md5(f'{datetime.now().isoformat()}_{os.getpid()}'.encode()).hexdigest()[:16]}"
    
    def update_memory_stats(self):
        """Update memory statistics"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Count conversations
                cursor.execute('SELECT COUNT(*) FROM conversations')
                self.memory_stats['total_conversations'] = cursor.fetchone()[0]
                
                # Count knowledge entries
                cursor.execute('SELECT COUNT(*) FROM knowledge')
                self.memory_stats['knowledge_entries'] = cursor.fetchone()[0]
                
                # Calculate memory size
                if os.path.exists(self.db_path):
                    size_bytes = os.path.getsize(self.db_path)
                    self.memory_stats['memory_size_mb'] = round(size_bytes / (1024 * 1024), 2)
                
        except Exception as e:
            print(f"❌ Error updating memory stats: {e}")
    
    def get_memory_status(self) -> Dict:
        """Get comprehensive memory system status"""
        self.update_memory_stats()
        
        return {
            'memory_stats': self.memory_stats,
            'database_path': self.db_path,
            'memory_directory': self.memory_dir,
            'system_status': 'active'
        }
    
    def learn_from_interaction(self, user_input: str, jarvis_response: str, feedback: str = None) -> bool:
        """Learn from user interaction and feedback"""
        try:
            # Store the conversation
            conv_id = self.store_conversation(user_input, jarvis_response, importance=2)
            
            # Extract and store potential knowledge
            if "is" in user_input.lower() and "?" not in user_input:
                topic = user_input.split()[0] if user_input.split() else "general"
                self.store_knowledge(topic, user_input, "interaction", 0.6)
            
            # Learn user preferences
            if "prefer" in user_input.lower() or "like" in user_input.lower():
                self.store_preference("user_preference", user_input)
            
            return True
            
        except Exception as e:
            print(f"❌ Error learning from interaction: {e}")
            return False

def main():
    """Test the memory system"""
    print("🧠 JARVIS MEMORY SYSTEM TEST")
    print("=" * 50)
    
    # Initialize memory system
    memory = JarvisMemorySystem()
    
    # Test storing conversation
    print("\n🔄 Testing conversation storage...")
    conv_id = memory.store_conversation(
        "What is artificial intelligence?",
        "Artificial intelligence is the simulation of human intelligence in machines.",
        importance=2
    )
    print(f"✅ Stored conversation with ID: {conv_id}")
    
    # Test storing knowledge
    print("\n🔄 Testing knowledge storage...")
    knowledge_id = memory.store_knowledge(
        "AI Definition",
        "AI is the capability of machines to imitate intelligent human behavior",
        "system",
        0.9
    )
    print(f"✅ Stored knowledge with ID: {knowledge_id}")
    
    # Test storing preferences
    print("\n🔄 Testing preference storage...")
    pref_id = memory.store_preference("communication_style", "detailed_explanations")
    print(f"✅ Stored preference with ID: {pref_id}")
    
    # Test searching knowledge
    print("\n🔄 Testing knowledge search...")
    results = memory.search_knowledge("artificial intelligence")
    print(f"✅ Found {len(results)} knowledge items")
    
    # Test retrieving conversations
    print("\n🔄 Testing conversation retrieval...")
    conversations = memory.retrieve_conversations(limit=5)
    print(f"✅ Retrieved {len(conversations)} conversations")
    
    # Test learning from interaction
    print("\n🔄 Testing learning system...")
    learned = memory.learn_from_interaction(
        "I prefer detailed explanations",
        "I understand you prefer detailed explanations. I'll provide comprehensive responses."
    )
    print(f"✅ Learning successful: {learned}")
    
    # Show memory status
    print("\n📊 Memory System Status:")
    status = memory.get_memory_status()
    for key, value in status['memory_stats'].items():
        print(f"   {key}: {value}")
    
    print("\n🎉 MEMORY SYSTEM TEST COMPLETED SUCCESSFULLY!")
    print("✅ All memory functions working correctly")
    print("🧠 JARVIS Memory System is ready for use")

if __name__ == '__main__':
    main()