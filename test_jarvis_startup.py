#!/usr/bin/env python3
"""
Test Jarvis startup without problematic components
"""

import os
import sys

# Set environment variables to avoid issues
os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["GOOGLE_API_KEY"] = "AIzaSyCK9TgGvQsHoHcvwbT8JEKmxqAPZFRuQMU"

def test_basic_startup():
    """Test basic Jarvis components without problematic ones"""
    print("🧪 Testing Jarvis Basic Startup...")
    
    try:
        # Test brain import
        print("1. Testing brain import...")
        import brain
        print("✅ Brain imported successfully")
        
        # Test basic thinking
        print("2. Testing basic thinking...")
        response = brain.think("Hello, who created you?")
        print(f"✅ Brain response: {response[:100]}...")
        
        # Test hybrid uncensored system
        print("3. Testing hybrid uncensored system...")
        from core.llm.hybrid_uncensored import hybrid_uncensored
        response = hybrid_uncensored.uncensored_think("Test uncensored system", 'jailbreak')
        print(f"✅ Uncensored response: {response[:100]}...")
        
        # Test command manager
        print("4. Testing command manager...")
        from core.brain.command_manager import CommandManager
        cm = CommandManager()
        print("✅ Command manager created")
        
        print("\n🎉 BASIC COMPONENTS WORKING!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_minimal_jarvis():
    """Test minimal Jarvis without Supreme Consciousness"""
    print("\n🧪 Testing Minimal Jarvis...")
    
    try:
        # Import main but don't initialize problematic components
        print("1. Testing main import...")
        
        # We'll create a minimal version
        from core.brain.brain import Brain
        from core.brain.command_manager import CommandManager
        
        print("✅ Core components imported")
        
        # Test basic functionality
        brain = Brain(backend="cloud")
        cm = CommandManager()
        
        print("✅ Minimal Jarvis components working")
        return True
        
    except Exception as e:
        print(f"❌ Minimal test failed: {e}")
        return False

if __name__ == "__main__":
    basic_success = test_basic_startup()
    minimal_success = test_minimal_jarvis()
    
    if basic_success and minimal_success:
        print("\n🚀 JARVIS CORE SYSTEMS ARE WORKING!")
        print("💡 The issue is likely in Supreme Consciousness or web components")
        print("🔧 Recommendation: Start with minimal mode first")
    else:
        print("\n❌ CORE SYSTEMS HAVE ISSUES")
        print("🔧 Need to fix basic components first")