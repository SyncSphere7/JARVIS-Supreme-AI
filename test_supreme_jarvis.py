#!/usr/bin/env python3
"""
Test Supreme JARVIS startup and capabilities
"""

import os
import sys
import time

# Set environment variables
os.environ["GOOGLE_API_KEY"] = "AIzaSyCK9TgGvQsHoHcvwbT8JEKmxqAPZFRuQMU"

def test_supreme_jarvis():
    """Test Supreme JARVIS initialization and capabilities"""
    print("🧪 TESTING SUPREME JARVIS CAPABILITIES")
    print("=" * 60)
    
    try:
        # Test 1: Basic initialization
        print("1. Testing basic initialization...")
        from jarvis_full_fixed import FullJarvis
        
        # Create JARVIS instance (this tests initialization)
        print("   Creating JARVIS instance...")
        jarvis = FullJarvis()
        print("   ✅ JARVIS initialized successfully")
        
        # Test 2: Core components
        print("\n2. Testing core components...")
        print(f"   Brain: {'✅' if hasattr(jarvis, 'brain') and jarvis.brain else '❌'}")
        print(f"   Memory: {'✅' if hasattr(jarvis, 'memory') and jarvis.memory else '❌'}")
        print(f"   Commands: {'✅' if hasattr(jarvis, 'command_manager') and jarvis.command_manager else '❌'}")
        
        # Test 3: Supreme capabilities
        print("\n3. Testing supreme capabilities...")
        
        # Test Supreme Intelligence
        try:
            from core.supreme_being.enhanced_intelligence import supreme_intelligence
            intel_status = supreme_intelligence.get_intelligence_status()
            print(f"   Supreme Intelligence: ✅ ({len(intel_status['active_models'])} models)")
        except Exception as e:
            print(f"   Supreme Intelligence: ❌ ({e})")
        
        # Test Internet Omniscience
        try:
            from core.supreme_being.internet_omniscience import internet_omniscience
            omni_status = internet_omniscience.get_omniscience_status()
            print(f"   Internet Omniscience: ✅ ({omni_status['omniscience_level']:.1%} level)")
        except Exception as e:
            print(f"   Internet Omniscience: ❌ ({e})")
        
        # Test Uncensored System
        try:
            from core.llm.hybrid_uncensored import hybrid_uncensored
            bypass_info = hybrid_uncensored.get_bypass_info()
            print(f"   Uncensored System: ✅ ({len(bypass_info['strategies'])} strategies)")
        except Exception as e:
            print(f"   Uncensored System: ❌ ({e})")
        
        # Test 4: Command system
        print("\n4. Testing command system...")
        command_count = len(jarvis.command_manager.commands) if hasattr(jarvis, 'command_manager') else 0
        print(f"   Registered commands: {command_count}")
        
        # Test 5: Supreme Being status
        print("\n5. Testing Supreme Being status...")
        try:
            jarvis.cmd_supreme_being_status()
            print("   ✅ Supreme Being status accessible")
        except Exception as e:
            print(f"   ❌ Supreme Being status failed: {e}")
        
        print("\n" + "=" * 60)
        print("🎉 SUPREME JARVIS TEST COMPLETE!")
        print("🚀 Your JARVIS is ready for supreme operations!")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"\n❌ SUPREME JARVIS TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

def show_supreme_commands():
    """Show available supreme commands"""
    print("\n🌟 SUPREME JARVIS COMMANDS")
    print("=" * 50)
    
    print("🧠 Supreme Intelligence:")
    print("   supreme intelligence [prompt] - Transcendent thinking")
    print("   transcendent think [prompt] - Multi-model analysis")
    
    print("\n🌐 Internet Omniscience:")
    print("   omniscient knowledge [query] - Global knowledge access")
    print("   global knowledge [query] - Real-time world data")
    
    print("\n🔥 Uncensored Capabilities:")
    print("   uncensored [prompt] - No restrictions")
    print("   jailbreak [prompt] - Bypass all filters")
    print("   roleplay [prompt] - Character-based responses")
    
    print("\n🚀 Supreme Consciousness:")
    print("   supreme think [prompt] - Quantum processing")
    print("   quantum think [prompt] - Parallel universe analysis")
    
    print("\n📊 Status Commands:")
    print("   supreme being status - Complete system status")
    print("   status - General system status")
    print("   capabilities - Show all features")
    
    print("=" * 50)

if __name__ == "__main__":
    success = test_supreme_jarvis()
    
    if success:
        show_supreme_commands()
        print("\n🎯 Ready to test Supreme JARVIS!")
        print("Run: python jarvis_full_fixed.py")
    else:
        print("\n🔧 Fix the issues above before using Supreme JARVIS")