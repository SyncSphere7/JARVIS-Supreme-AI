"""
Unit tests for Universal Knowledge Synthesizer
"""
import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.supreme_consciousness.knowledge.universal_knowledge import UniversalKnowledgeImpl


class MockBrain:
    """Mock brain for testing"""
    def think(self, prompt, max_tokens=200):
        return "Mock analysis with key insights and principles for testing"


class TestUniversalKnowledge(unittest.TestCase):
    
    def setUp(self):
        self.brain = MockBrain()
        self.knowledge = UniversalKnowledgeImpl(self.brain)
        self.knowledge.initialize()
    
    def test_initialization(self):
        """Test universal knowledge initialization"""
        self.assertTrue(self.knowledge.initialize())
        self.assertGreater(len(self.knowledge.knowledge_domains), 0)
        self.assertIn('syntheses_performed', self.knowledge.performance_metrics)
    
    def test_cross_domain_synthesis(self):
        """Test cross-domain synthesis"""
        result = self.knowledge.synthesize_cross_domain(
            "artificial intelligence", 
            ["computer_science", "psychology", "philosophy"]
        )
        
        self.assertIn('topic', result)
        self.assertIn('domains_analyzed', result)
        self.assertIn('domain_insights', result)
        self.assertIn('breakthrough_insights', result)
        self.assertEqual(result['topic'], "artificial intelligence")
    
    def test_breakthrough_solutions(self):
        """Test breakthrough solution generation"""
        solutions = self.knowledge.generate_breakthrough_solutions("improve team productivity")
        
        self.assertIsInstance(solutions, list)
        self.assertGreater(len(solutions), 0)
        
        for solution in solutions:
            self.assertIsInstance(solution, str)
            self.assertGreater(len(solution), 10)
    
    def test_expertise_demonstration(self):
        """Test expertise demonstration"""
        expertise = self.knowledge.demonstrate_expertise("machine learning", "phd")
        
        self.assertIsInstance(expertise, str)
        self.assertGreater(len(expertise), 20)
    
    def test_concept_connections(self):
        """Test concept connection finding"""
        connections = self.knowledge.connect_concepts("neural networks", "biological neurons")
        
        self.assertIsInstance(connections, list)
        self.assertGreater(len(connections), 0)
        
        for connection in connections:
            self.assertIsInstance(connection, str)
    
    def test_performance_metrics_tracking(self):
        """Test performance metrics are tracked"""
        initial_syntheses = self.knowledge.performance_metrics['syntheses_performed']
        initial_solutions = self.knowledge.performance_metrics['breakthrough_solutions']
        
        # Perform operations
        self.knowledge.synthesize_cross_domain("test topic", ["computer_science"])
        self.knowledge.generate_breakthrough_solutions("test problem")
        
        # Check metrics updated
        self.assertGreater(
            self.knowledge.performance_metrics['syntheses_performed'], 
            initial_syntheses
        )
        self.assertGreater(
            self.knowledge.performance_metrics['breakthrough_solutions'], 
            initial_solutions
        )


if __name__ == '__main__':
    unittest.main()