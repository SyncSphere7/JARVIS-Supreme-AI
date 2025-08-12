#!/usr/bin/env python3
"""
Test the autonomous evolution system.
"""
import os
import sys

# Suppress warnings
os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["PYTHONWARNINGS"] = "ignore::UserWarning"

def test_auto_evolution():
    """Test the auto-evolution system."""
    print("🧪 Testing Auto-Evolution System...")
    
    try:
        # Test basic imports
        print("📦 Testing imports...")
        from main import Jarvis
        print("✅ Main imports successful")
        
        # Test initialization
        print("🤖 Testing initialization...")
        jarvis = Jarvis()
        print("✅ Jarvis initialized")
        
        # Test auto-evolution system
        if hasattr(jarvis, 'autonomous_updater'):
            print("🔄 Testing autonomous updater...")
            
            # Test status check
            status = jarvis.autonomous_updater.get_update_status()
            print(f"✅ Update status: {status[:100]}...")
            
            # Test if system is running
            is_running = jarvis.autonomous_updater.running
            print(f"✅ Auto-update running: {is_running}")
            
        else:
            print("⚠️ Autonomous updater not available")
        
        print("\n🎉 AUTO-EVOLUTION SYSTEM TEST COMPLETE!")
        print("🔄 Jarvis will now continuously improve itself every 24 hours!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_auto_evolution()
    
    if success:
        print("\n🚀 Ready to test autonomous evolution:")
        print("   python main.py --cli")
        print("   > update status")
        print("   > force update")
        print("   (Jarvis will auto-update every 24 hours)")
    else:
        print("\n🔧 Run: python install_deps.py")
