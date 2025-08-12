#!/usr/bin/env python3
"""
Quick test to check if the syntax error is fixed.
"""
import sys
import os

# Suppress warnings
os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["PYTHONWARNINGS"] = "ignore::UserWarning"

def test_imports():
    """Test if all imports work."""
    try:
        print("🧪 Testing imports...")
        
        # Test the problematic import
        print("📦 Testing goal_executor import...")
        from core.autonomous.goal_executor import GoalExecutor
        print("✅ goal_executor imported successfully!")
        
        # Test main import
        print("📦 Testing main import...")
        from main import Jarvis
        print("✅ main imported successfully!")
        
        # Test initialization
        print("🤖 Testing Jarvis initialization...")
        jarvis = Jarvis()
        print("✅ Jarvis initialized successfully!")
        
        print("\n🎉 ALL TESTS PASSED!")
        print("🚀 Jarvis is ready to run!")
        print("Try: python main.py --cli")
        
        return True
        
    except SyntaxError as e:
        print(f"❌ SYNTAX ERROR: {e}")
        print(f"📍 File: {e.filename}, Line: {e.lineno}")
        return False
        
    except ImportError as e:
        print(f"❌ IMPORT ERROR: {e}")
        return False
        
    except Exception as e:
        print(f"❌ OTHER ERROR: {type(e).__name__}: {e}")
        return False

if __name__ == "__main__":
    print("🔧 QUICK SYNTAX AND IMPORT TEST")
    print("=" * 40)
    
    success = test_imports()
    
    if success:
        print("\n✅ Everything is working!")
    else:
        print("\n❌ Issues found - need manual fix")
