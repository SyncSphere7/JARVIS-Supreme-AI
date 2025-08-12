"""
Unit tests for Quantum Processor
"""
import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.supreme_consciousness.quantum.quantum_processor import QuantumProcessorImpl
from core.supreme_consciousness.data_models import QuantumThought


class MockBrain:
    """Mock brain for testing"""
    def think(self, prompt, max_tokens=200):
        return "Step 1: Analyze problem\nStep 2: Design solution\nStep 3: Implement\nStep 4: Test\nStep 5: Deploy"


class TestQuantumProcessor(unittest.TestCase):
    
    def setUp(self):
        self.brain = MockBrain()
        self.processor = QuantumProcessorImpl(self.brain)
        self.processor.initialize()
    
    def test_initialization(self):
        """Test quantum processor initialization"""
        self.assertTrue(self.processor.initialize())
        self.assertIn('thoughts_processed', self.processor.performance_metrics)
        self.assertEqual(self.processor.name, "QuantumProcessor")
    
    def test_process_quantum_thoughts(self):
        """Test quantum thought generation"""
        problem = "How to optimize database performance"
        thoughts = self.processor.process_quantum_thoughts(problem, max_paths=10)
        
        self.assertEqual(len(thoughts), 10)
        self.assertIsInstance(thoughts[0], QuantumThought)
        self.assertEqual(thoughts[0].problem_context, problem)
        self.assertTrue(0 <= thoughts[0].probability_score <= 1)
        self.assertTrue(0 <= thoughts[0].confidence_level <= 1)
    
    def test_evaluate_scenarios(self):
        """Test scenario evaluation"""
        scenarios = [
            {'id': 'scenario1', 'feasibility': 0.8, 'efficiency': 0.6},
            {'id': 'scenario2', 'feasibility': 0.6, 'efficiency': 0.9},
            {'id': 'scenario3', 'feasibility': 0.9, 'efficiency': 0.7}
        ]
        
        criteria = {'feasibility': 0.6, 'efficiency': 0.4}
        evaluated = self.processor.evaluate_scenarios(scenarios, criteria)
        
        self.assertEqual(len(evaluated), 3)
        self.assertIn('evaluation_score', evaluated[0])
        # Should be sorted by score (highest first)
        self.assertGreaterEqual(evaluated[0]['evaluation_score'], evaluated[1]['evaluation_score'])
    
    def test_synthesize_solutions(self):
        """Test solution synthesis"""
        thoughts = self.processor.process_quantum_thoughts("Test problem", max_paths=5)
        synthesized = self.processor.synthesize_solutions(thoughts)
        
        self.assertIsInstance(synthesized, QuantumThought)
        self.assertTrue(len(synthesized.solution_path) > 0)
        self.assertTrue(synthesized.probability_score > 0)
        self.assertTrue(synthesized.confidence_level > 0)
    
    def test_calculate_probabilities(self):
        """Test probability calculations"""
        outcomes = [
            {'id': 'success', 'weight': 0.7, 'description': 'Success'},
            {'id': 'failure', 'weight': 0.3, 'description': 'Failure'}
        ]
        
        probabilities = self.processor.calculate_probabilities(outcomes)
        
        self.assertIn('success', probabilities)
        self.assertIn('failure', probabilities)
        self.assertAlmostEqual(
            probabilities['success']['probability'] + probabilities['failure']['probability'], 
            1.0, 
            places=2
        )
    
    def test_quantum_think(self):
        """Test high-level quantum thinking"""
        result = self.processor.quantum_think("How to build a web application", max_paths=20)
        
        self.assertIn('problem', result)
        self.assertIn('total_thoughts_generated', result)
        self.assertIn('best_solution', result)
        self.assertIn('outcome_probabilities', result)
        self.assertEqual(result['total_thoughts_generated'], 20)
        self.assertTrue(result['quantum_advantage'])  # Should be True for 20 paths
    
    def test_performance_metrics(self):
        """Test performance metrics tracking"""
        initial_processed = self.processor.performance_metrics['thoughts_processed']
        
        self.processor.process_quantum_thoughts("Test problem", max_paths=5)
        
        self.assertGreater(
            self.processor.performance_metrics['thoughts_processed'], 
            initial_processed
        )
        self.assertGreater(self.processor.performance_metrics['success_rate'], 0)
    
    def tearDown(self):
        self.processor.shutdown()


if __name__ == '__main__':
    unittest.main()