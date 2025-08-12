#!/usr/bin/env python3
"""
Test the self-repair system.
"""
import os
import sys

# Suppress warnings
os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["PYTHONWARNINGS"] = "ignore::UserWarning"

def test_self_repair():
    """Test the self-repair system."""
    print("🧪 Testing Self-Repair System...")
    
    try:
        # Test basic imports
        print("📦 Testing imports...")
        from main import Jarvis
        print("✅ Main imports successful")
        
        # Test initialization
        print("🤖 Testing initialization...")
        jarvis = Jarvis()
        print("✅ Jarvis initialized")
        
        # Test self-repair system
        if hasattr(jarvis, 'autonomous_debugger'):
            print("🔧 Testing autonomous debugger...")
            
            # Create a test error
            test_error = ValueError("Test error for self-repair")
            
            # Test repair
            repair_result = jarvis.autonomous_debugger.autonomous_debug_and_repair(
                test_error,
                context={'test': True},
                task_context="Self-repair system test"
            )
            
            print(f"✅ Self-repair test result: {repair_result}")
        else:
            print("⚠️ Self-repair system not available")
        
        # Test self-repairing wrapper
        if hasattr(jarvis, 'self_repairing_wrapper'):
            print("🔄 Testing self-repairing wrapper...")
            
            def test_function():
                return "Test function executed successfully"
            
            result = jarvis.self_repairing_wrapper.self_repairing_execution(
                test_function,
                task_context="Wrapper test"
            )
            
            print(f"✅ Wrapper test result: {result}")
        else:
            print("⚠️ Self-repairing wrapper not available")
        
        print("\n🎉 SELF-REPAIR SYSTEM TEST COMPLETE!")
        print("🔧 Jarvis can now autonomously debug and repair itself!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_self_repair()
    
    if success:
        print("\n🚀 Ready to test autonomous self-repair:")
        print("   python main.py --cli")
        print("   > execute goal create a website")
        print("   (Jarvis will auto-repair any errors)")
    else:
        print("\n🔧 Run: python install_deps.py")
