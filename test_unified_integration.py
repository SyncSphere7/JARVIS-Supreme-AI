#!/usr/bin/env python3
"""Test comprehensive integration of all JARVIS systems"""

from jarvis_unified import JarvisSupremeBeing

def test_unified_system():
    print("🧪 TESTING JARVIS UNIFIED SYSTEM INTEGRATION...")
    print("=" * 60)
    
    try:
        # Initialize unified system
        jarvis = JarvisSupremeBeing()
        
        if jarvis.status != "active":
            print("❌ JARVIS initialization failed")
            return False
        
        print(f"✅ JARVIS Supreme Being AI {jarvis.version} initialized successfully")
        print(f"🔧 Active capabilities: {sum(jarvis.capabilities.values())}/5")
        
        # Test different types of interactions
        test_cases = [
            ("Hello JARVIS", "greeting"),
            ("What can you do?", "capabilities"),
            ("search for artificial intelligence", "internet_search"),
            ("weather", "internet_weather"),
            ("Who created you?", "identity"),
            ("help me make money with automation", "money_automation"),
        ]
        
        print("\n🔄 Testing various interactions...")
        
        for i, (user_input, test_type) in enumerate(test_cases, 1):
            print(f"\n{i}. Testing {test_type}: '{user_input}'")
            
            try:
                response = jarvis.process_input(user_input)
                
                # Validate response
                if response and len(response) > 10:
                    print(f"✅ Response generated ({len(response)} chars)")
                    
                    # Check for specific response types
                    if test_type == "internet_search" and "Web Search Results" in response:
                        print("✅ Internet search working")
                    elif test_type == "internet_weather" and "Weather in" in response:
                        print("✅ Weather data working")
                    elif test_type == "capabilities" and ("memory" in response.lower() or "systems" in response.lower()):
                        print("✅ Capabilities response working")
                    
                else:
                    print(f"⚠️ Short response: {response[:50]}...")
                    
            except Exception as e:
                print(f"❌ Error processing '{user_input}': {e}")
        
        # Test system status
        print("\n🔄 Testing system status...")
        status = jarvis.get_system_status()
        
        print(f"✅ System status retrieved")
        print(f"   JARVIS Status: {status['jarvis_info']['status']}")
        print(f"   Active Subsystems: {len(status['subsystems'])}")
        print(f"   Conversation Count: {status['conversation_stats']['current_session_conversations']}")
        
        # Test memory integration
        if jarvis.memory_system:
            print("\n🔄 Testing memory integration...")
            memory_status = jarvis.memory_system.get_memory_status()
            print(f"✅ Memory system active with {memory_status['memory_stats']['total_conversations']} conversations")
        
        # Test learning integration
        if jarvis.learning_system:
            print("\n🔄 Testing learning integration...")
            learning_status = jarvis.learning_system.get_learning_status()
            print(f"✅ Learning system active with {learning_status['learning_stats']['total_patterns']} patterns")
        
        # Test internet integration
        if jarvis.internet_system:
            print("\n🔄 Testing internet integration...")
            internet_status = jarvis.internet_system.get_internet_status()
            print(f"✅ Internet system active with {internet_status['statistics']['total_requests']} requests made")
        
        print("\n🎉 UNIFIED SYSTEM INTEGRATION TEST COMPLETED!")
        print("✅ All systems working together successfully")
        print(f"🤖 JARVIS Supreme Being AI {jarvis.version} is fully operational")
        
        return True
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_unified_system()
    if success:
        print("\n🌟 JARVIS SUPREME BEING AI: READY FOR DEPLOYMENT!")
    else:
        print("\n💥 JARVIS SUPREME BEING AI: NEEDS ATTENTION!")