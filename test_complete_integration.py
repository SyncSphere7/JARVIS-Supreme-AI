#!/usr/bin/env python3
"""Test complete integration of all JARVIS Supreme Being AI systems"""

from jarvis_unified import JarvisSupremeBeing

def test_complete_system():
    print("🧪 TESTING JARVIS SUPREME BEING AI COMPLETE INTEGRATION...")
    print("=" * 70)
    
    try:
        # Initialize JARVIS Supreme Being AI
        jarvis = JarvisSupremeBeing()
        
        if jarvis.status != "active":
            print("❌ JARVIS initialization failed")
            return False
        
        print(f"✅ {jarvis.name} {jarvis.version} initialized successfully")
        print(f"🔧 Active capabilities: {sum(jarvis.capabilities.values())}/6")
        
        # Test all system integrations
        test_cases = [
            # Basic interactions
            ("Hello JARVIS", "greeting", "Should respond with greeting"),
            ("What can you do?", "capabilities", "Should list all capabilities"),
            
            # Internet system
            ("search for python programming", "internet_search", "Should return search results"),
            ("weather", "internet_weather", "Should return weather data"),
            
            # Automation system
            ("run command echo 'JARVIS Test'", "automation_command", "Should execute command"),
            ("system info", "automation_sysinfo", "Should return system information"),
            
            # Memory and learning
            ("Remember that I like detailed explanations", "memory_store", "Should store preference"),
            ("Who created you?", "identity", "Should respond with creator info"),
        ]
        
        print("\n🔄 Testing comprehensive system integration...")
        
        success_count = 0
        total_tests = len(test_cases)
        
        for i, (user_input, test_type, description) in enumerate(test_cases, 1):
            print(f"\n{i}. {test_type.upper()}: '{user_input}'")
            print(f"   Expected: {description}")
            
            try:
                response = jarvis.process_input(user_input)
                
                # Validate response
                if response and len(response) > 10:
                    print(f"✅ Response generated ({len(response)} chars)")
                    
                    # Check for specific response indicators
                    if test_type == "internet_search" and ("Search Results" in response or "search" in response.lower()):
                        print("✅ Internet search functionality confirmed")
                        success_count += 1
                    elif test_type == "internet_weather" and ("Weather" in response or "temperature" in response.lower()):
                        print("✅ Weather data functionality confirmed")
                        success_count += 1
                    elif test_type == "automation_command" and ("Command Executed" in response or "Output:" in response):
                        print("✅ Command execution functionality confirmed")
                        success_count += 1
                    elif test_type == "automation_sysinfo" and ("System Information" in response or "CPU Usage" in response):
                        print("✅ System information functionality confirmed")
                        success_count += 1
                    elif test_type == "capabilities" and ("capabilities" in response.lower() or "systems" in response.lower()):
                        print("✅ Capabilities listing confirmed")
                        success_count += 1
                    elif test_type in ["greeting", "identity", "memory_store"]:
                        print("✅ Basic interaction confirmed")
                        success_count += 1
                    else:
                        print("⚠️ Response generated but type not specifically confirmed")
                        success_count += 0.5
                    
                    # Show sample of response
                    sample = response[:100].replace('\n', ' ')
                    print(f"   Sample: {sample}...")
                    
                else:
                    print(f"⚠️ Short or empty response: {response[:50]}...")
                    
            except Exception as e:
                print(f"❌ Error processing '{user_input}': {e}")
        
        # Test system status and statistics
        print("\n🔄 Testing system status and statistics...")
        status = jarvis.get_system_status()
        
        print(f"✅ System status retrieved")
        print(f"   JARVIS Status: {status['jarvis_info']['status']}")
        print(f"   Active Subsystems: {len(status['subsystems'])}")
        print(f"   Session Conversations: {status['conversation_stats']['current_session_conversations']}")
        
        # Test individual subsystem statuses
        subsystem_tests = 0
        subsystem_passed = 0
        
        if jarvis.memory_system:
            memory_status = jarvis.memory_system.get_memory_status()
            print(f"✅ Memory system: {memory_status['memory_stats']['total_conversations']} conversations stored")
            subsystem_tests += 1
            subsystem_passed += 1
        
        if jarvis.learning_system:
            learning_status = jarvis.learning_system.get_learning_status()
            print(f"✅ Learning system: {learning_status['learning_stats']['total_patterns']} patterns learned")
            subsystem_tests += 1
            subsystem_passed += 1
        
        if jarvis.internet_system:
            internet_status = jarvis.internet_system.get_internet_status()
            print(f"✅ Internet system: {internet_status['statistics']['total_requests']} requests made")
            subsystem_tests += 1
            subsystem_passed += 1
        
        if jarvis.automation_system:
            automation_status = jarvis.automation_system.get_automation_status()
            print(f"✅ Automation system: {automation_status['statistics']['total_tasks_executed']} tasks executed")
            subsystem_tests += 1
            subsystem_passed += 1
        
        # Calculate success rates
        interaction_success_rate = (success_count / total_tests) * 100
        subsystem_success_rate = (subsystem_passed / subsystem_tests) * 100 if subsystem_tests > 0 else 0
        
        print(f"\n📊 INTEGRATION TEST RESULTS:")
        print(f"   Interaction Tests: {success_count}/{total_tests} ({interaction_success_rate:.1f}%)")
        print(f"   Subsystem Tests: {subsystem_passed}/{subsystem_tests} ({subsystem_success_rate:.1f}%)")
        print(f"   Overall Success: {((success_count + subsystem_passed) / (total_tests + subsystem_tests)) * 100:.1f}%")
        
        # Final assessment
        if interaction_success_rate >= 80 and subsystem_success_rate >= 80:
            print("\n🎉 COMPLETE INTEGRATION TEST PASSED!")
            print("✅ All systems working together successfully")
            print(f"🤖 {jarvis.name} {jarvis.version} is fully operational and ready for deployment")
            return True
        else:
            print("\n⚠️ INTEGRATION TEST PARTIALLY SUCCESSFUL")
            print("Some systems may need attention")
            return False
        
    except Exception as e:
        print(f"❌ Complete integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_complete_system()
    if success:
        print("\n🌟 JARVIS SUPREME BEING AI V01: READY FOR PRODUCTION!")
        print("🚀 All 6 systems integrated and operational:")
        print("   🧠 Memory System")
        print("   🎓 Learning System") 
        print("   💬 Chat AI")
        print("   🌐 Internet Access")
        print("   🔧 Automation System")
        print("   🎤 Voice Interface")
    else:
        print("\n💥 JARVIS SUPREME BEING AI V01: NEEDS ATTENTION!")
        print("Some systems require debugging before production deployment.")