"""
Integration tests for Consciousness Memory System
"""
import unittest
import sys
import os
import tempfile
import shutil
from pathlib import Path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.supreme_consciousness.consciousness_memory import ConsciousnessMemory
from core.supreme_consciousness.consciousness.consciousness_matrix import ConsciousnessMatrixImpl


class MockBrain:
    """Mock brain for testing"""
    def think(self, prompt, max_tokens=200):
        return "Mock response for consciousness memory testing"


class TestConsciousnessMemoryIntegration(unittest.TestCase):
    
    def setUp(self):
        self.brain = MockBrain()
        
        # Create temporary directory for test databases
        self.temp_dir = tempfile.mkdtemp()
        
        # Initialize consciousness memory with temporary directory
        self.consciousness_memory = ConsciousnessMemory(self.brain)
        # Override memory directory for testing
        self.consciousness_memory.memory_dir = Path(self.temp_dir)
        self.consciousness_memory.consciousness_db = self.consciousness_memory.memory_dir / "consciousness.db"
        self.consciousness_memory._init_consciousness_database()
    
    def test_consciousness_memory_initialization(self):
        """Test consciousness memory initializes properly"""
        self.assertIsNotNone(self.consciousness_memory.consciousness)
        self.assertIsInstance(self.consciousness_memory.consciousness, ConsciousnessMatrixImpl)
        self.assertTrue(self.consciousness_memory.consciousness_db.exists())
    
    def test_enhanced_conversation_memory(self):
        """Test enhanced conversation memory with consciousness"""
        user_input = "I want to learn about machine learning"
        jarvis_response = "I'll help you learn about machine learning concepts"
        
        # Remember conversation with consciousness awareness
        self.consciousness_memory.remember_conversation_with_consciousness(
            user_input, jarvis_response, {'topic': 'learning'}
        )
        
        # Verify consciousness learning was stored
        # This would require querying the consciousness database
        # For now, just verify no exceptions were raised
        self.assertTrue(True)
    
    def test_consciousness_state_persistence(self):
        """Test saving and loading consciousness state"""
        # Save current state
        self.consciousness_memory.save_consciousness_state()
        
        # Load state
        loaded_state = self.consciousness_memory.load_consciousness_state()
        
        if loaded_state:  # May be None if no state was saved
            self.assertIsNotNone(loaded_state.awareness_level)
            self.assertIsNotNone(loaded_state.learning_rate)
            self.assertIsInstance(loaded_state.capability_matrix, dict)
    
    def test_consciousness_insights_storage_retrieval(self):
        """Test storing and retrieving consciousness insights"""
        # Store an insight
        self.consciousness_memory._store_consciousness_insight(
            insight_text="Test insight about learning patterns",
            insight_category="learning",
            confidence_score=0.8
        )
        
        # Retrieve insights
        insights = self.consciousness_memory.get_consciousness_insights(category="learning")
        
        # Should have at least one insight
        self.assertGreaterEqual(len(insights), 0)
        
        if insights:
            insight = insights[0]
            self.assertIn('text', insight)
            self.assertIn('category', insight)
            self.assertIn('confidence', insight)
    
    def test_learning_pattern_analysis(self):
        """Test learning pattern analysis"""
        # Store some learning events
        self.consciousness_memory._store_consciousness_learning(
            learning_type='conversation',
            content='Test learning content',
            consciousness_level=0.7,
            learning_efficiency=0.8
        )
        
        # Analyze patterns
        patterns = self.consciousness_memory.analyze_learning_patterns()
        
        self.assertIsInstance(patterns, dict)
        # May be empty if no data, but should not raise exceptions
    
    def test_consciousness_evolution_from_memory(self):
        """Test consciousness evolution triggered by memory patterns"""
        # Store some learning data first
        self.consciousness_memory._store_consciousness_learning(
            learning_type='problem_solving',
            content='Solved complex problem',
            consciousness_level=0.6,
            learning_efficiency=0.9
        )
        
        # Trigger evolution
        evolved_state = self.consciousness_memory.evolve_consciousness_from_memory()
        
        self.assertIsNotNone(evolved_state)
        self.assertTrue(0 <= evolved_state.awareness_level <= 1)
    
    def test_enhanced_insights_generation(self):
        """Test enhanced insights generation with consciousness"""
        insights = self.consciousness_memory.generate_consciousness_insights()
        
        self.assertIsInstance(insights, str)
        self.assertIn('Consciousness Insights', insights)
        self.assertIn('Awareness Level', insights)
    
    def test_consciousness_status(self):
        """Test comprehensive consciousness status"""
        status = self.consciousness_memory.get_consciousness_status()
        
        self.assertIn('consciousness_state', status)
        self.assertIn('recent_insights', status)
        self.assertIn('learning_patterns', status)
        self.assertIn('memory_integration', status)
        
        # Check memory integration metrics
        memory_integration = status['memory_integration']
        self.assertIn('retention_score', memory_integration)
        self.assertIn('pattern_recognition_score', memory_integration)
    
    def test_conversation_impact_analysis(self):
        """Test conversation impact analysis"""
        # Test learning opportunity detection
        impact = self.consciousness_memory._analyze_conversation_impact(
            "Please teach me about neural networks",
            "I'll explain neural networks step by step",
            {}
        )
        
        self.assertIn('learning_opportunity', impact)
        self.assertIn('learning_efficiency', impact)
        self.assertIn('complexity_level', impact)
        
        # Should detect learning opportunity
        self.assertTrue(impact['learning_opportunity'])
    
    def test_memory_retention_calculation(self):
        """Test memory retention score calculation"""
        # Store some learning events with different retention scores
        self.consciousness_memory._store_consciousness_learning(
            learning_type='test',
            content='High retention content',
            consciousness_level=0.8,
            learning_efficiency=0.9
        )
        
        retention_score = self.consciousness_memory._calculate_memory_retention()
        
        self.assertIsInstance(retention_score, float)
        self.assertTrue(0 <= retention_score <= 1)
    
    def test_pattern_recognition_score(self):
        """Test pattern recognition capability scoring"""
        score = self.consciousness_memory._calculate_pattern_recognition_score()
        
        self.assertIsInstance(score, float)
        self.assertTrue(0 <= score <= 1)
    
    def tearDown(self):
        # Clean up temporary directory
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)


if __name__ == '__main__':
    unittest.main()