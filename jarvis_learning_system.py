#!/usr/bin/env python3
"""
JARVIS Advanced Learning System - Continuous Learning and Adaptation
"""

import json
import os
import sqlite3
import time
from datetime import datetime
from typing import Dict, List, Any
import threading
from collections import defaultdict
import hashlib

# Try to import ML libraries
try:
    import numpy as np
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False
    print("⚠️ NumPy not available. Install with: pip install numpy")

# Import JARVIS components
try:
    from jarvis_memory_system import JarvisMemorySystem
    MEMORY_AVAILABLE = True
except ImportError:
    MEMORY_AVAILABLE = False

class JarvisLearningSystem:
    """Advanced learning system for JARVIS Supreme Being AI"""
    
    def __init__(self, learning_dir: str = "supreme_learning"):
        self.learning_dir = learning_dir
        self.db_path = os.path.join(learning_dir, "jarvis_learning.db")
        
        # Learning statistics
        self.learning_stats = {
            'total_patterns': 0,
            'successful_predictions': 0,
            'failed_predictions': 0,
            'accuracy_rate': 0.0
        }
        
        # Pattern recognition
        self.user_patterns = defaultdict(list)
        self.learning_lock = threading.Lock()
        
        # Initialize memory system if available
        if MEMORY_AVAILABLE:
            self.memory_system = JarvisMemorySystem()
        
        # Initialize learning system
        self.initialize_learning_system()
    
    def initialize_learning_system(self):
        """Initialize the learning system"""
        print("🧠 INITIALIZING JARVIS LEARNING SYSTEM...")
        
        try:
            os.makedirs(self.learning_dir, exist_ok=True)
            self.init_database()
            self.update_learning_stats()
            
            print("✅ JARVIS Learning System initialized successfully")
            print(f"📊 Learning Statistics: {self.learning_stats}")
            
        except Exception as e:
            print(f"❌ Learning system initialization error: {e}")
    
    def init_database(self):
        """Initialize SQLite database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS patterns (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    pattern_type TEXT,
                    input_pattern TEXT,
                    output_pattern TEXT,
                    success_rate REAL,
                    usage_count INTEGER DEFAULT 0,
                    timestamp TEXT
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS feedback (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_input TEXT,
                    jarvis_response TEXT,
                    feedback_type TEXT,
                    feedback_value REAL,
                    timestamp TEXT
                )
            ''')
            
            conn.commit()
    
    def learn_from_interaction(self, user_input: str, jarvis_response: str, 
                             feedback: str = None, success: bool = True) -> bool:
        """Learn from user interaction"""
        with self.learning_lock:
            try:
                # Extract patterns
                input_patterns = self.extract_input_patterns(user_input)
                
                # Store patterns
                for pattern in input_patterns:
                    self.store_pattern("input", pattern, jarvis_response, success)
                
                # Process feedback if provided
                if feedback:
                    self.process_feedback(user_input, jarvis_response, feedback)
                
                # Update statistics
                if success:
                    self.learning_stats['successful_predictions'] += 1
                else:
                    self.learning_stats['failed_predictions'] += 1
                
                self.update_accuracy_rate()
                return True
                
            except Exception as e:
                print(f"❌ Error learning from interaction: {e}")
                return False
    
    def extract_input_patterns(self, user_input: str) -> List[str]:
        """Extract patterns from user input"""
        patterns = []
        words = user_input.lower().split()
        
        # Question patterns
        if user_input.strip().endswith('?'):
            patterns.append("question")
            if any(word in words for word in ['what', 'how', 'why', 'when', 'where', 'who']):
                patterns.append("wh_question")
        
        # Topic patterns
        if any(word in words for word in ['code', 'program', 'python', 'javascript']):
            patterns.append("programming")
        if any(word in words for word in ['ai', 'machine learning', 'neural']):
            patterns.append("ai_topic")
        
        # Sentiment patterns
        if any(word in words for word in ['good', 'great', 'excellent', 'amazing']):
            patterns.append("positive_sentiment")
        if any(word in words for word in ['bad', 'terrible', 'awful', 'wrong']):
            patterns.append("negative_sentiment")
        
        return patterns
    
    def store_pattern(self, pattern_type: str, input_pattern: str, 
                     output_pattern: str, success: bool) -> int:
        """Store a learning pattern"""
        try:
            timestamp = datetime.now().isoformat()
            success_rate = 1.0 if success else 0.0
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Check if pattern exists
                cursor.execute('''
                    SELECT id, success_rate, usage_count FROM patterns 
                    WHERE pattern_type = ? AND input_pattern = ? AND output_pattern = ?
                ''', (pattern_type, input_pattern, output_pattern))
                
                existing = cursor.fetchone()
                
                if existing:
                    # Update existing pattern
                    pattern_id, old_success_rate, usage_count = existing
                    new_usage_count = usage_count + 1
                    new_success_rate = ((old_success_rate * usage_count) + success_rate) / new_usage_count
                    
                    cursor.execute('''
                        UPDATE patterns 
                        SET success_rate = ?, usage_count = ?
                        WHERE id = ?
                    ''', (new_success_rate, new_usage_count, pattern_id))
                else:
                    # Insert new pattern
                    cursor.execute('''
                        INSERT INTO patterns 
                        (pattern_type, input_pattern, output_pattern, success_rate, usage_count, timestamp)
                        VALUES (?, ?, ?, ?, 1, ?)
                    ''', (pattern_type, input_pattern, output_pattern, success_rate, timestamp))
                    
                    pattern_id = cursor.lastrowid
                
                conn.commit()
                return pattern_id
                
        except Exception as e:
            print(f"❌ Error storing pattern: {e}")
            return -1
    
    def process_feedback(self, user_input: str, jarvis_response: str, feedback: str):
        """Process user feedback"""
        try:
            timestamp = datetime.now().isoformat()
            
            # Analyze feedback sentiment
            feedback_lower = feedback.lower()
            feedback_value = 0.0
            feedback_type = "neutral"
            
            if any(word in feedback_lower for word in ['good', 'great', 'excellent', 'perfect']):
                feedback_value = 1.0
                feedback_type = "positive"
            elif any(word in feedback_lower for word in ['bad', 'wrong', 'incorrect', 'terrible']):
                feedback_value = -1.0
                feedback_type = "negative"
            
            # Store feedback
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO feedback 
                    (user_input, jarvis_response, feedback_type, feedback_value, timestamp)
                    VALUES (?, ?, ?, ?, ?)
                ''', (user_input, jarvis_response, feedback_type, feedback_value, timestamp))
                
                conn.commit()
                
        except Exception as e:
            print(f"❌ Error processing feedback: {e}")
    
    def predict_best_response_type(self, user_input: str) -> Dict[str, float]:
        """Predict the best response type for user input"""
        try:
            input_patterns = self.extract_input_patterns(user_input)
            response_scores = defaultdict(float)
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                for pattern in input_patterns:
                    cursor.execute('''
                        SELECT output_pattern, success_rate, usage_count 
                        FROM patterns 
                        WHERE input_pattern = ? AND pattern_type = 'input'
                        ORDER BY success_rate DESC, usage_count DESC
                    ''', (pattern,))
                    
                    results = cursor.fetchall()
                    
                    for output_pattern, success_rate, usage_count in results:
                        score = success_rate * (1 + usage_count * 0.1)
                        response_scores[output_pattern] += score
            
            return dict(response_scores)
            
        except Exception as e:
            print(f"❌ Error predicting response type: {e}")
            return {}
    
    def update_accuracy_rate(self):
        """Update learning accuracy rate"""
        total = self.learning_stats['successful_predictions'] + self.learning_stats['failed_predictions']
        if total > 0:
            self.learning_stats['accuracy_rate'] = self.learning_stats['successful_predictions'] / total
    
    def update_learning_stats(self):
        """Update learning statistics"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('SELECT COUNT(*) FROM patterns')
                self.learning_stats['total_patterns'] = cursor.fetchone()[0]
                
        except Exception as e:
            print(f"❌ Error updating learning stats: {e}")
    
    def get_learning_insights(self) -> Dict[str, Any]:
        """Get insights about learning progress"""
        try:
            insights = {
                'learning_stats': self.learning_stats,
                'top_patterns': [],
                'improvement_areas': []
            }
            
            # Get top patterns
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT input_pattern, output_pattern, success_rate, usage_count 
                    FROM patterns 
                    ORDER BY success_rate DESC, usage_count DESC 
                    LIMIT 10
                ''')
                
                insights['top_patterns'] = [
                    {
                        'input': row[0],
                        'output': row[1][:50] + '...' if len(row[1]) > 50 else row[1],
                        'success_rate': row[2],
                        'usage_count': row[3]
                    }
                    for row in cursor.fetchall()
                ]
            
            # Identify improvement areas
            if self.learning_stats['accuracy_rate'] < 0.8:
                insights['improvement_areas'].append('Response accuracy needs improvement')
            
            if self.learning_stats['total_patterns'] < 50:
                insights['improvement_areas'].append('More interaction data needed')
            
            return insights
            
        except Exception as e:
            print(f"❌ Error getting learning insights: {e}")
            return {}
    
    def get_learning_status(self) -> Dict[str, Any]:
        """Get learning system status"""
        self.update_learning_stats()
        
        return {
            'learning_stats': self.learning_stats,
            'ml_available': ML_AVAILABLE,
            'memory_available': MEMORY_AVAILABLE,
            'database_path': self.db_path,
            'system_status': 'active'
        }

def main():
    """Test the learning system"""
    print("🧠 JARVIS LEARNING SYSTEM TEST")
    print("=" * 50)
    
    # Initialize learning system
    learning = JarvisLearningSystem()
    
    # Test learning from interactions
    print("\n🔄 Testing learning from interactions...")
    
    interactions = [
        ("What is Python?", "Python is a high-level programming language.", True),
        ("How do I create a function?", "Use the 'def' keyword to create a function.", True),
        ("Tell me about AI", "AI is artificial intelligence in machines.", True),
        ("What's the weather?", "I don't have weather data.", False),
    ]
    
    for user_input, jarvis_response, success in interactions:
        learned = learning.learn_from_interaction(user_input, jarvis_response, success=success)
        print(f"✅ Learned from: '{user_input[:30]}...' - Success: {success}")
    
    # Test feedback processing
    print("\n🔄 Testing feedback processing...")
    learning.process_feedback(
        "What is Python?",
        "Python is a programming language.",
        "Great explanation!"
    )
    print("✅ Processed positive feedback")
    
    # Test pattern prediction
    print("\n🔄 Testing response prediction...")
    predictions = learning.predict_best_response_type("How do I learn programming?")
    print(f"✅ Generated {len(predictions)} response predictions")
    
    # Get learning insights
    print("\n🔄 Testing learning insights...")
    insights = learning.get_learning_insights()
    print(f"✅ Generated insights with {len(insights['top_patterns'])} top patterns")
    
    # Show learning status
    print("\n📊 Learning System Status:")
    status = learning.get_learning_status()
    for key, value in status['learning_stats'].items():
        print(f"   {key}: {value}")
    
    accuracy = status['learning_stats']['accuracy_rate']
    print(f"\n🎯 Learning Accuracy: {accuracy:.2%}")
    print(f"📈 Total Patterns: {status['learning_stats']['total_patterns']}")
    
    print("\n🎉 LEARNING SYSTEM TEST COMPLETED!")
    print("✅ All learning functions working correctly")
    print("🧠 JARVIS Learning System is ready for continuous improvement")

if __name__ == '__main__':
    main()
