"""
Tests for Quantum Processing capabilities
"""
import unittest
import asyncio
from unittest.mock import Mock, patch
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from core.supreme_consciousness.quantum.quantum_processor import QuantumProcessorImpl
from core.supreme_consciousness.data_models import QuantumThought


class TestQuantumProcessing(unittest.TestCase):
    """Test suite for Quantum Processing capabilities"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.mock_brain = Mock()
        self.mock_brain.think.return_value = "Test quantum response"
        self.quantum_processor = QuantumProcessorImpl(self.mock_brain)
        
    def test_initialization(self):
        """Test quantum processor initialization"""
        self.assertIsNotNone(self.quantum_processor)
        self.assertEqual(self.quantum_processor.name, "QuantumProcessor")
        self.assertFalse(self.quantum_processor.active)
        
    def test_quantum_processor_initialize(self):
        """Test quantum processor initialization process"""
        result = self.quantum_processor.initialize()
        self.assertTrue(result)
        self.assertTrue(self.quantum_processor.active)
        
    def test_parallel_solution_generation(self):
        """Test parallel solution path generation"""
        # Initialize the processor
        self.quantum_processor.initialize()
        
        problem = "How to optimize system performance"
        max_paths = 10
        
        # Mock the brain response for quantum thinking
        self.mock_brain.think.return_value = """
        Solution paths:
        1. Optimize memory usage
        2. Improve CPU utilization
        3. Enhance disk I/O
        4. Network optimization
        5. Cache optimization
        """
        
        thoughts = self.quantum_processor.process_quantum_thoughts(problem, max_paths)
        
        # Verify results
        self.assertIsInstance(thoughts, list)
        self.assertGreater(len(thoughts), 0)
        self.assertLessEqual(len(thoughts), max_paths)
        
        # Check that each thought is a QuantumThought instance
        for thought in thoughts:
            self.assertIsInstance(thought, QuantumThought)
            self.assertEqual(thought.problem_context, problem)
            self.assertGreaterEqual(thought.confidence_level, 0.0)
            self.assertLessEqual(thought.confidence_level, 1.0)
    
    def test_scenario_evaluation(self):
        """Test scenario evaluation with weighted outcomes"""
        self.quantum_processor.initialize()
        
        scenarios = [
            {'name': 'scenario_1', 'description': 'High performance approach', 'complexity': 0.8},
            {'name': 'scenario_2', 'description': 'Balanced approach', 'complexity': 0.5},
            {'name': 'scenario_3', 'description': 'Simple approach', 'complexity': 0.2}
        ]
        
        criteria = {
            'performance': 0.4,
            'complexity': 0.3,
            'reliability': 0.3
        }
        
        evaluated_scenarios = self.quantum_processor.evaluate_scenarios(scenarios, criteria)
        
        # Verify results
        self.assertIsInstance(evaluated_scenarios, list)
        self.assertEqual(len(evaluated_scenarios), len(scenarios))
        
        # Check that each scenario has evaluation scores
        for scenario in evaluated_scenarios:
            self.assertIn('evaluation_score', scenario)
            self.assertIn('weighted_score', scenario)
            self.assertGreaterEqual(scenario['evaluation_score'], 0.0)
            self.assertLessEqual(scenario['evaluation_score'], 1.0)
    
    def test_solution_synthesis(self):
        """Test synthesis of multiple solution paths"""
        self.quantum_processor.initialize()
        
        # Create test quantum thoughts
        thoughts = [
            QuantumThought(
                problem_context="test problem",
                solution_path=["step1", "step2", "step3"],
                confidence_level=0.8,
                probability_score=0.7
            ),
            QuantumThought(
                problem_context="test problem",
                solution_path=["stepA", "stepB", "stepC"],
                confidence_level=0.6,
                probability_score=0.8
            ),
            QuantumThought(
                problem_context="test problem",
                solution_path=["option1", "option2"],
                confidence_level=0.9,
                probability_score=0.6
            )
        ]
        
        synthesized_solution = self.quantum_processor.synthesize_solutions(thoughts)
        
        # Verify results
        self.assertIsInstance(synthesized_solution, QuantumThought)
        self.assertEqual(synthesized_solution.problem_context, "test problem")
        self.assertGreater(len(synthesized_solution.solution_path), 0)
        self.assertGreaterEqual(synthesized_solution.confidence_level, 0.0)
        self.assertLessEqual(synthesized_solution.confidence_level, 1.0)
    
    def test_probability_calculation(self):
        """Test probability-weighted recommendations"""
        self.quantum_processor.initialize()
        
        outcomes = [
            {'outcome': 'success', 'likelihood': 0.7, 'impact': 0.9},
            {'outcome': 'partial_success', 'likelihood': 0.2, 'impact': 0.6},
            {'outcome': 'failure', 'likelihood': 0.1, 'impact': 0.1}
        ]
        
        probabilities = self.quantum_processor.calculate_probabilities(outcomes)
        
        # Verify results
        self.assertIsInstance(probabilities, dict)
        self.assertIn('weighted_probabilities', probabilities)
        self.assertIn('recommendation', probabilities)
        self.assertIn('confidence', probabilities)
        
        # Check probability values
        weighted_probs = probabilities['weighted_probabilities']
        for outcome_name, prob in weighted_probs.items():
            self.assertGreaterEqual(prob, 0.0)
            self.assertLessEqual(prob, 1.0)
    
    def test_quantum_advantage_detection(self):
        """Test detection of quantum processing advantage"""
        self.quantum_processor.initialize()
        
        # Test with complex problem that should benefit from quantum processing
        complex_problem = "Optimize multi-dimensional resource allocation across distributed systems with dynamic constraints"
        
        result = self.quantum_processor.quantum_think(complex_problem, max_paths=100)
        
        # Verify quantum advantage is detected for complex problems
        self.assertIsInstance(result, dict)
        self.assertIn('quantum_advantage', result)
        self.assertIn('best_solution', result)
        self.assertIn('processing_time', result)
        
        # For complex problems, quantum advantage should be detected
        if result.get('quantum_advantage'):
            self.assertGreater(result.get('parallel_paths_generated', 0), 10)
    
    def test_performance_metrics(self):
        """Test quantum processing performance metrics"""
        self.quantum_processor.initialize()
        
        # Perform several quantum operations
        problems = [
            "Simple optimization problem",
            "Complex multi-variable problem",
            "Resource allocation challenge"
        ]
        
        for problem in problems:
            self.quantum_processor.quantum_think(problem, max_paths=20)
        
        # Check performance metrics
        metrics = self.quantum_processor.performance_metrics
        self.assertIn('quantum_operations', metrics)
        self.assertIn('average_processing_time', metrics)
        self.assertIn('quantum_advantage_rate', metrics)
        
        # Verify metrics are reasonable
        self.assertGreaterEqual(metrics['quantum_operations'], len(problems))
        self.assertGreaterEqual(metrics['average_processing_time'], 0.0)
        self.assertGreaterEqual(metrics['quantum_advantage_rate'], 0.0)
        self.assertLessEqual(metrics['quantum_advantage_rate'], 1.0)
    
    def test_error_handling(self):
        """Test error handling in quantum processing"""
        self.quantum_processor.initialize()
        
        # Test with invalid input
        result = self.quantum_processor.process_quantum_thoughts("", 0)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)
        
        # Test with brain error
        self.mock_brain.think.side_effect = Exception("Brain error")
        
        result = self.quantum_processor.quantum_think("test problem")
        self.assertIsInstance(result, dict)
        self.assertIn('error', result)
    
    def test_quantum_coherence(self):
        """Test quantum coherence in solution paths"""
        self.quantum_processor.initialize()
        
        problem = "Design coherent system architecture"
        
        # Generate multiple solution paths
        thoughts = self.quantum_processor.process_quantum_thoughts(problem, max_paths=50)
        
        # Check for coherence in solutions
        if len(thoughts) > 1:
            # All thoughts should have the same problem context
            for thought in thoughts:
                self.assertEqual(thought.problem_context, problem)
            
            # Solutions should have reasonable confidence levels
            avg_confidence = sum(t.confidence_level for t in thoughts) / len(thoughts)
            self.assertGreaterEqual(avg_confidence, 0.3)  # Reasonable minimum confidence


class TestQuantumProcessingIntegration(unittest.TestCase):
    """Integration tests for Quantum Processing with other components"""
    
    def setUp(self):
        """Set up integration test fixtures"""
        self.mock_brain = Mock()
        self.mock_brain.think.return_value = "Integration test response"
        
    def test_brain_integration(self):
        """Test integration with Brain component"""
        quantum_processor = QuantumProcessorImpl(self.mock_brain)
        quantum_processor.initialize()
        
        # Test that quantum processor uses brain for thinking
        result = quantum_processor.quantum_think("test problem")
        
        # Verify brain was called
        self.mock_brain.think.assert_called()
        self.assertIsInstance(result, dict)
    
    def test_memory_integration(self):
        """Test integration with memory systems"""
        quantum_processor = QuantumProcessorImpl(self.mock_brain)
        quantum_processor.initialize()
        
        # Generate thoughts that should be memorable
        problem = "Important strategic decision"
        thoughts = quantum_processor.process_quantum_thoughts(problem, max_paths=10)
        
        # Verify thoughts contain memory-relevant information
        for thought in thoughts:
            self.assertIsNotNone(thought.created_at)
            self.assertIsNotNone(thought.thought_id)
            self.assertEqual(thought.problem_context, problem)


if __name__ == '__main__':
    unittest.main()
