"""
Unit tests for Consciousness Matrix
"""
import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.supreme_consciousness.consciousness.consciousness_matrix import ConsciousnessMatrixImpl
from core.supreme_consciousness.data_models import ConsciousnessState


class MockBrain:
    """Mock brain for testing"""
    def think(self, prompt, max_tokens=200):
        return "Mock response for consciousness testing"


class TestConsciousnessMatrix(unittest.TestCase):
    
    def setUp(self):
        self.brain = MockBrain()
        self.consciousness = ConsciousnessMatrixImpl(self.brain)
        self.consciousness.initialize()
    
    def test_initialization(self):
        """Test consciousness matrix initialization"""
        self.assertTrue(self.consciousness.initialize())
        self.assertIsInstance(self.consciousness.consciousness_state, ConsciousnessState)
        self.assertGreater(self.consciousness.consciousness_state.awareness_level, 0)
        self.assertIn('problem_solving', self.consciousness.consciousness_state.capability_matrix)
    
    def test_evolve_capabilities(self):
        """Test capability evolution"""
        initial_capabilities = dict(self.consciousness.consciousness_state.capability_matrix)
        
        # Trigger evolution
        evolved_state = self.consciousness.evolve_capabilities()
        
        self.assertIsInstance(evolved_state, ConsciousnessState)
        self.assertGreater(len(evolved_state.evolution_history), 0)
        
        # Check that some capabilities may have evolved
        final_capabilities = evolved_state.capability_matrix
        self.assertEqual(len(initial_capabilities), len(final_capabilities))
    
    def test_self_reflect(self):
        """Test self-reflection functionality"""
        performance_data = {
            'problem_solving': 0.7,
            'pattern_recognition': 0.8,
            'creative_thinking': 0.4,
            'logical_reasoning': 0.9
        }
        
        reflection = self.consciousness.self_reflect(performance_data)
        
        self.assertIn('reflection_timestamp', reflection)
        self.assertIn('performance_analysis', reflection)
        self.assertIn('improvement_recommendations', reflection)
        self.assertIn('consciousness_level', reflection)
        
        # Check performance analysis structure
        analysis = reflection['performance_analysis']
        self.assertIn('strengths', analysis)
        self.assertIn('weaknesses', analysis)
        self.assertIn('overall_score', analysis)
    
    def test_adapt_strategies(self):
        """Test strategy adaptation"""
        environmental_changes = {
            'complexity_increase': 0.8,
            'performance_pressure': 'high',
            'user_behavior_change': 0.6
        }
        
        initial_strategies = len(self.consciousness.adaptation_strategies)
        
        self.consciousness.adapt_strategies(environmental_changes)
        
        # Should have created new strategies
        self.assertGreaterEqual(len(self.consciousness.adaptation_strategies), initial_strategies)
        
        # Check environmental context was updated
        self.assertIn('last_adaptation', self.consciousness.consciousness_state.environmental_context)
    
    def test_generate_insights(self):
        """Test insight generation"""
        data_streams = [
            {'metric_a': 0.8, 'metric_b': 0.6, 'category': 'type1'},
            {'metric_a': 0.9, 'metric_b': 0.7, 'category': 'type1'},
            {'metric_a': 0.7, 'metric_b': 0.5, 'category': 'type2'},
            {'metric_a': 0.85, 'metric_b': 0.65, 'category': 'type1'}
        ]
        
        insights = self.consciousness.generate_insights(data_streams)
        
        self.assertIsInstance(insights, list)
        self.assertGreater(len(insights), 0)
        
        # Should generate meaningful insights
        for insight in insights:
            self.assertIsInstance(insight, str)
            self.assertGreater(len(insight), 10)  # Should be descriptive
    
    def test_consciousness_state_tracking(self):
        """Test consciousness state tracking"""
        state = self.consciousness.get_consciousness_state()
        
        self.assertIn('awareness_level', state)
        self.assertIn('learning_rate', state)
        self.assertIn('capabilities', state)
        self.assertIn('current_goals', state)
        self.assertIn('performance_metrics', state)
        
        # Values should be within expected ranges
        self.assertTrue(0 <= state['awareness_level'] <= 1)
        self.assertTrue(0 <= state['learning_rate'] <= 1)
    
    def test_goal_setting(self):
        """Test goal setting functionality"""
        new_goals = ['improve_efficiency', 'enhance_creativity', 'optimize_performance']
        
        self.consciousness.set_goals(new_goals)
        
        self.assertEqual(self.consciousness.consciousness_state.current_goals, new_goals)
    
    def test_learning_history_management(self):
        """Test learning history management"""
        # Add some learning history
        for i in range(150):  # More than the keep_recent limit
            self.consciousness.learning_history.append({
                'timestamp': f'2024-01-{i:02d}',
                'data': f'test_data_{i}'
            })
        
        initial_count = len(self.consciousness.learning_history)
        self.consciousness.clear_learning_history(keep_recent=100)
        
        self.assertEqual(len(self.consciousness.learning_history), 100)
        self.assertLess(len(self.consciousness.learning_history), initial_count)
    
    def test_pattern_identification(self):
        """Test pattern identification in data"""
        data_streams = [
            {'success_rate': 0.8, 'response_time': 1.2},
            {'success_rate': 0.85, 'response_time': 1.1},
            {'success_rate': 0.9, 'response_time': 1.0},
            {'success_rate': 0.75, 'response_time': 1.3}
        ]
        
        patterns = self.consciousness._identify_patterns(data_streams)
        
        self.assertIn('frequency', patterns)
        self.assertIn('numerical', patterns)
        
        # Check numerical patterns
        numerical = patterns['numerical']
        if 'success_rate' in numerical:
            self.assertIn('mean', numerical['success_rate'])
            self.assertIn('trend', numerical['success_rate'])
    
    def test_improvement_strategy_generation(self):
        """Test improvement strategy generation"""
        poor_performance = {
            'problem_solving': 0.3,
            'creative_thinking': 0.4,
            'emotional_intelligence': 0.2
        }
        
        strategies = self.consciousness._generate_improvement_strategies(poor_performance)
        
        self.assertIsInstance(strategies, list)
        self.assertGreater(len(strategies), 0)
        
        # Should contain actionable strategies
        for strategy in strategies:
            self.assertIsInstance(strategy, str)
            self.assertGreater(len(strategy), 20)  # Should be descriptive
    
    def test_performance_metrics_tracking(self):
        """Test performance metrics are properly tracked"""
        initial_evolution_cycles = self.consciousness.performance_metrics['evolution_cycles']
        initial_insights = self.consciousness.performance_metrics['insights_generated']
        
        # Trigger evolution and insight generation
        self.consciousness.evolve_capabilities()
        self.consciousness.generate_insights([{'test': 'data'}])
        
        # Metrics should be updated
        self.assertGreater(
            self.consciousness.performance_metrics['evolution_cycles'], 
            initial_evolution_cycles
        )
        self.assertGreater(
            self.consciousness.performance_metrics['insights_generated'], 
            initial_insights
        )


if __name__ == '__main__':
    unittest.main()