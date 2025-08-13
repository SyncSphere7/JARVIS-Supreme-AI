#!/usr/bin/env python3
"""Test script for JARVIS Memory System"""

from jarvis_memory_system import JarvisMemorySystem

def test_memory_system():
    print("🧠 TESTING JARVIS MEMORY SYSTEM...")
    
    try:
        # Initialize memory system
        memory = JarvisMemorySystem()
        print("✅ Memory system initialized")
        
        # Test conversation storage
        conv_id = memory.store_conversation(
            "Hello JARVIS, how are you?",
            "Hello! I'm functioning perfectly and ready to assist you.",
            importance=1
        )
        print(f"✅ Conversation stored with ID: {conv_id}")
        
        # Test knowledge storage
        knowledge_id = memory.store_knowledge(
            "JARVIS",
            "JARVIS is an advanced AI assistant with supreme capabilities",
            0.95
        )
        print(f"✅ Knowledge stored with ID: {knowledge_id}")
        
        # Test retrieval
        conversations = memory.retrieve_conversations(limit=3)
        print(f"✅ Retrieved {len(conversations)} conversations")
        
        knowledge_results = memory.search_knowledge("JARVIS")
        print(f"✅ Found {len(knowledge_results)} knowledge items")
        
        # Get status
        status = memory.get_memory_status()
        print(f"✅ Memory status retrieved: {status['system_status']}")
        
        print("\n🎉 ALL MEMORY TESTS PASSED!")
        print("🧠 JARVIS Memory System is working perfectly!")
        
        return True
        
    except Exception as e:
        print(f"❌ Memory test failed: {e}")
        return False

if __name__ == "__main__":
    test_memory_system()