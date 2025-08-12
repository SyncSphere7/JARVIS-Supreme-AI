"""
Simple test for Quantum Brain functionality
"""
import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.supreme_consciousness.quantum_brain import QuantumBrain


class TestQuantumBrainSimple(unittest.TestCase):
    
    def setUp(self):
        self.brain = QuantumBrain(backend="cloud")
    
    def test_basic_functionality(self):
        """Test basic quantum brain functionality"""
        # Test regular thinking still works
        response = self.brain.think("What is 2+2?", max_tokens=50)
        self.assertIsInstance(response, str)
        self.assertTrue(len(response) > 0)
        
        # Test quantum status
        status = self.brain.get_quantum_status()
        self.assertIn('quantum_enabled', status)
        
        # Test quantum thinking with fallback
        result = self.brain.quantum_think("Simple problem", max_paths=5, use_quantum=False)
        self.assertIn('method', result)
        self.assertEqual(result['method'], 'regular_thinking')
    
    def test_quantum_mode_toggle(self):
        """Test quantum mode can be toggled"""
        # Disable quantum mode
        self.brain.disable_quantum_mode()
        self.assertFalse(self.brain.quantum_enabled)
        
        # Try to enable (may not work but shouldn't crash)
        try:
            enabled = self.brain.enable_quantum_mode()
            self.assertIsInstance(enabled, bool)
        except Exception as e:
            self.fail(f"Enable quantum mode raised exception: {e}")
    
    def tearDown(self):
        if hasattr(self.brain, 'shutdown'):
            self.brain.shutdown()


if __name__ == '__main__':
    unittest.main()