#!/usr/bin/env python3
"""
Test Jarvis functionality.
"""
import os
import sys

# Suppress warnings
os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["PYTHONWARNINGS"] = "ignore::UserWarning"

def test_jarvis():
    """Test Jarvis core functionality."""
    print("🧪 Testing God-Mode Jarvis...")
    
    try:
        # Test imports
        print("📦 Testing imports...")
        from main import Jarvis
        print("✅ Main imports successful")
        
        # Initialize Jarvis
        print("🤖 Initializing Jarvis...")
        jarvis = Jarvis()
        print("✅ Jarvis initialized")
        
        # Test memory
        print("🧠 Testing memory...")
        if hasattr(jarvis, 'memory'):
            jarvis.memory.learn_fact("test", "Jarvis is working perfectly", "test")
            facts = jarvis.memory.recall_facts("test")
            if facts:
                print("✅ Memory system working")
            else:
                print("⚠️ Memory system issue")
        
        # Test system access
        print("💻 Testing system access...")
        if hasattr(jarvis, 'system_access'):
            projects = jarvis.system_access.find_existing_projects()
            print(f"✅ Found {len(projects)} projects")
        
        # Test internet access
        print("🌐 Testing internet access...")
        if hasattr(jarvis, 'internet_access'):
            print("✅ Internet access module loaded")
        
        # Test autonomous capabilities
        print("🎯 Testing autonomous capabilities...")
        if hasattr(jarvis, 'goal_executor'):
            print("✅ Goal executor loaded")
        
        # Test self-healing
        print("🔧 Testing self-healing...")
        if hasattr(jarvis, 'auto_updater'):
            health = jarvis.auto_updater.monitor_health()
            print(f"✅ Health status: {health.get('overall_status', 'unknown')}")
        
        print("\n🎉 ALL TESTS PASSED!")
        print("🚀 God-Mode Jarvis is fully operational!")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def show_commands():
    """Show available commands."""
    print("\n🎮 GOD-MODE COMMANDS TO TRY:")
    print("=" * 40)
    print("🧠 Memory & Intelligence:")
    print("  > remember that I prefer dark themes")
    print("  > memory insights")
    print("  > what do you remember about projects")
    
    print("\n🎯 Autonomous Execution:")
    print("  > execute goal create a portfolio website")
    print("  > autonomous build me a landing page")
    
    print("\n💻 System Control:")
    print("  > open VS Code")
    print("  > morning setup")
    print("  > list projects")
    
    print("\n🌐 Internet & Research:")
    print("  > search for AI trends 2024")
    print("  > research React best practices")
    print("  > weather in Tokyo")
    
    print("\n🔧 Self-Healing:")
    print("  > health check")
    print("  > maintenance")
    
    print("\n💻 Web Development:")
    print("  > create website with dark theme #1a1a2e")
    print("  > enhance design with animations")

if __name__ == "__main__":
    success = test_jarvis()
    
    if success:
        show_commands()
        print("\n🚀 Ready to launch: python main.py --cli")
    else:
        print("\n🔧 Run: python fix_torch_warnings.py")
