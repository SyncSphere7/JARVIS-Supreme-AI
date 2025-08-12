"""
Tests for Consciousness Evolution capabilities
"""
import unittest
from unittest.mock import Mock, patch
import sys
import os
from datetime import datetime

# Add the project root to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from core.supreme_consciousness.consciousness.consciousness_matrix import ConsciousnessMatrixImpl
from core.supreme_consciousness.data_models import ConsciousnessState


class TestConsciousnessEvolution(unittest.TestCase):
    """Test suite for Consciousness Evolution capabilities"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.mock_brain = Mock()
        self.mock_brain.think.return_value = "Consciousness evolution response"
        self.consciousness_matrix = ConsciousnessMatrixImpl(self.mock_brain)
        
    def test_initialization(self):
        """Test consciousness matrix initialization"""
        self.assertIsNotNone(self.consciousness_matrix)
        self.assertEqual(self.consciousness_matrix.name, "ConsciousnessMatrix")
        self.assertFalse(self.consciousness_matrix.active)
        
    def test_consciousness_matrix_initialize(self):
        """Test consciousness matrix initialization process"""
        result = self.consciousness_matrix.initialize()
        self.assertTrue(result)
        self.assertTrue(self.consciousness_matrix.active)
        
    def test_autonomous_capability_development(self):
        """Test autonomous development of new capabilities"""
        self.consciousness_matrix.initialize()
        
        # Mock brain response for capability evolution
        self.mock_brain.think.return_value = """
        New capabilities developed:
        1. Enhanced pattern recognition
        2. Improved decision making
        3. Advanced problem solving
        4. Better resource optimization
        """
        
        evolved_state = self.consciousness_matrix.evolve_capabilities()
        
        # Verify evolution occurred
        self.assertIsInstance(evolved_state, ConsciousnessState)
        self.assertGreater(evolved_state.awareness_level, 0.0)
        self.assertLessEqual(evolved_state.awareness_level, 1.0)
        self.assertGreater(len(evolved_state.evolution_history), 0)
        
        # Check that capabilities were updated
        self.assertGreater(len(evolved_state.capability_matrix), 0)
        
    def test_self_reflection_analysis(self):
        """Test self-reflection and performance analysis"""
        self.consciousness_matrix.initialize()
        
        # Provide performance data for reflection
        performance_data = {
            'problem_solving': 0.8,
            'pattern_recognition': 0.7,
            'decision_making': 0.9,
            'learning_rate': 0.6,
            'adaptation_speed': 0.75
        }
        
        reflection_result = self.consciousness_matrix.self_reflect(performance_data)
        
        # Verify reflection results
        self.assertIsInstance(reflection_result, dict)
        self.assertIn('self_assessment', reflection_result)
        self.assertIn('improvement_areas', reflection_result)
        self.assertIn('strengths', reflection_result)
        self.assertIn('evolution_recommendations', reflection_result)
        
        # Check that performance data was processed
        self.assertIsInstance(reflection_result['improvement_areas'], list)
        self.assertIsInstance(reflection_result['strengths'], list)


if __name__ == '__main__':
    unittest.main()