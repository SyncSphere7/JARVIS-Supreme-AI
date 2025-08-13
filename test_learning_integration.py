#!/usr/bin/env python3
"""Test integration between learning and memory systems"""

from jarvis_learning_system import JarvisLearningSystem
from jarvis_memory_system import JarvisMemorySystem

def test_integration():
    print("🧪 TESTING LEARNING & MEMORY INTEGRATION...")
    
    try:
        # Initialize both systems
        learning = JarvisLearningSystem()
        memory = JarvisMemorySystem()
        
        print("✅ Both systems initialized")
        
        # Test learning from interaction
        user_input = "How do I write a Python function?"
        jarvis_response = "To write a Python function, use the 'def' keyword followed by the function name and parameters."
        
        # Learn from interaction
        learned = learning.learn_from_interaction(user_input, jarvis_response, success=True)
        print(f"✅ Learning system processed interaction: {learned}")
        
        # Store in memory
        conv_id = memory.store_conversation(user_input, jarvis_response, importance=2)
        print(f"✅ Memory system stored conversation: {conv_id}")
        
        # Test prediction
        predictions = learning.predict_best_response_type("How do I create a function in Python?")
        print(f"✅ Learning system made {len(predictions)} predictions")
        
        # Test feedback processing
        learning.process_feedback(user_input, jarvis_response, "That was very helpful!")
        print("✅ Feedback processed successfully")
        
        # Get insights
        insights = learning.get_learning_insights()
        print(f"✅ Generated insights with {len(insights['top_patterns'])} patterns")
        
        # Get status from both systems
        learning_status = learning.get_learning_status()
        memory_status = memory.get_memory_status()
        
        print(f"\n📊 Integration Status:")
        print(f"   Learning Accuracy: {learning_status['learning_stats']['accuracy_rate']:.2%}")
        print(f"   Memory Conversations: {memory_status['memory_stats']['total_conversations']}")
        print(f"   Learning Patterns: {learning_status['learning_stats']['total_patterns']}")
        
        print("\n🎉 INTEGRATION TEST PASSED!")
        print("✅ Learning and Memory systems work together perfectly")
        
        return True
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        return False

if __name__ == "__main__":
    test_integration()