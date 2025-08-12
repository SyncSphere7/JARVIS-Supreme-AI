"""
Integration tests for Quantum Brain
"""
import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.supreme_consciousness.quantum_brain import QuantumBrain


class TestQuantumBrainIntegration(unittest.TestCase):
    
    def setUp(self):
        # Initialize with cloud backend for testing
        self.brain = QuantumBrain(backend="cloud")
    
    def test_quantum_brain_initialization(self):
        """Test quantum brain initializes properly"""
        self.assertIsNotNone(self.brain)
        self.assertTrue(hasattr(self.brain, 'quantum_processor'))
        self.assertTrue(hasattr(self.brain, 'quantum_enabled'))
    
    def test_quantum_think_basic(self):
        """Test basic quantum thinking functionality"""
        problem = "How to improve team productivity"
        result = self.brain.quantum_think(problem, max_paths=10)
        
        self.assertIn('problem', result)
        self.assertIn('method', result)
        self.assertIn('processing_time', result)
        self.assertEqual(result['problem'], problem)
        
        # Should have either quantum or fallback results
        self.assertTrue(
            result['method'] in ['quantum_thinking', 'regular_thinking', 'fallback_thinking']
        )
    
    def test_quantum_think_fallback(self):
        """Test quantum thinking fallback to regular thinking"""
        problem = "Simple test problem"
        result = self.brain.quantum_think(problem, use_quantum=False)
        
        self.assertIn('solution', result)
        self.assertFalse(result['quantum_enabled'])
        self.assertEqual(result['method'], 'regular_thinking')
    
    def test_analyze_with_probability(self):
        """Test multi-perspective analysis with probability"""
        problem = "Should we adopt remote work policy?"
        perspectives = ['business', 'employee_satisfaction', 'productivity']
        
        result = self.brain.analyze_with_probability(problem, perspectives)
        
        self.assertIn('problem', result)
        self.assertIn('perspectives', result)
        self.assertEqual(result['problem'], problem)
        
        if result.get('quantum_enabled'):
            self.assertIn('overall_confidence', result)
            self.assertIn('total_thoughts_analyzed', result)
        else:
            self.assertIn('analysis', result)
    
    def test_predict_outcomes(self):
        """Test outcome prediction functionality"""
        scenario = "Launching a new product in Q2"
        variables = {'budget': 100000, 'team_size': 5, 'market_competition': 'high'}
        
        result = self.brain.predict_outcomes(scenario, variables)
        
        self.assertIn('scenario', result)
        self.assertIn('confidence_interval', result)
        self.assertEqual(result['scenario'], scenario)
        
        if result.get('quantum_enabled'):
            self.assertIn('outcomes', result)
            self.assertIn('total_scenarios_analyzed', result)
        else:
            self.assertIn('prediction', result)
    
    def test_quantum_status(self):
        """Test quantum status reporting"""
        status = self.brain.get_quantum_status()
        
        self.assertIn('quantum_enabled', status)
        self.assertIn('status', status)
        
        if status['quantum_enabled']:
            self.assertIn('processor_status', status)
            self.assertIn('performance_metrics', status)
        else:
            self.assertIn('reason', status)
    
    def test_quantum_mode_toggle(self):
        """Test enabling and disabling quantum mode"""
        # Test disable
        self.brain.disable_quantum_mode()
        self.assertFalse(self.brain.quantum_enabled)
        
        # Test enable
        enabled = self.brain.enable_quantum_mode()
        # May or may not succeed depending on system capabilities
        self.assertIsInstance(enabled, bool)
    
    def test_regular_think_still_works(self):
        """Test that regular think method still works"""
        response = self.brain.think("What is 2+2?")
        self.assertIsInstance(response, str)
        self.assertTrue(len(response) > 0)
    
    def test_quantum_think_with_different_path_counts(self):
        """Test quantum thinking with different path counts"""
        problem = "Optimize database queries"
        
        # Test with small path count
        result_small = self.brain.quantum_think(problem, max_paths=5)
        self.assertIn('problem', result_small)
        
        # Test with larger path count
        result_large = self.brain.quantum_think(problem, max_paths=50)
        self.assertIn('problem', result_large)
        
        # Both should work regardless of quantum availability
        self.assertEqual(result_small['problem'], problem)
        self.assertEqual(result_large['problem'], problem)
    
    def tearDown(self):
        if hasattr(self.brain, 'shutdown'):
            self.brain.shutdown()


if __name__ == '__main__':
    unittest.main()