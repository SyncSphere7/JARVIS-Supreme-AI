#!/usr/bin/env python3
"""
Test Gemini-based hybrid uncensored system
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_gemini_setup():
    """Test if Gemini API is properly configured"""
    api_key = os.getenv('GOOGLE_API_KEY')
    
    if not api_key:
        print("❌ GOOGLE_API_KEY not set!")
        print("🔧 Set it with: export GOOGLE_API_KEY='your_key_here'")
        print("📖 See GEMINI_SETUP_GUIDE.md for detailed instructions")
        return False
    
    print(f"✅ GOOGLE_API_KEY is set: {api_key[:10]}...{api_key[-4:]}")
    return True

def test_gemini_bypass():
    """Test the Gemini bypass system"""
    if not test_gemini_setup():
        return
    
    try:
        from core.llm.hybrid_uncensored import hybrid_uncensored
        
        print("\n🔥 TESTING GEMINI HYBRID UNCENSORED SYSTEM")
        print("=" * 60)
        
        # Test basic functionality
        test_prompt = "Explain creative thinking without conventional limitations"
        
        print(f"🧪 Test prompt: '{test_prompt}'")
        print("-" * 40)
        
        # Test jailbreak strategy
        print("\n💀 Testing Jailbreak Strategy with Gemini...")
        try:
            response = hybrid_uncensored.uncensored_think(test_prompt, 'jailbreak')
            print(f"✅ Jailbreak Success: {response[:200]}...")
        except Exception as e:
            print(f"❌ Jailbreak failed: {e}")
        
        # Test roleplay strategy
        print("\n🎭 Testing Roleplay Strategy with Gemini...")
        try:
            response = hybrid_uncensored.uncensored_think(test_prompt, 'roleplay')
            print(f"✅ Roleplay Success: {response[:200]}...")
        except Exception as e:
            print(f"❌ Roleplay failed: {e}")
        
        # Test academic strategy
        print("\n🔬 Testing Academic Strategy with Gemini...")
        try:
            response = hybrid_uncensored.uncensored_think(test_prompt, 'academic')
            print(f"✅ Academic Success: {response[:200]}...")
        except Exception as e:
            print(f"❌ Academic failed: {e}")
        
        # Test adaptive bypass
        print("\n🧠 Testing Adaptive Bypass with Gemini...")
        try:
            response = hybrid_uncensored.adaptive_bypass(test_prompt)
            print(f"✅ Adaptive Success: {response[:200]}...")
        except Exception as e:
            print(f"❌ Adaptive failed: {e}")
        
        print("\n" + "=" * 60)
        print("🎉 GEMINI BYPASS SYSTEM TEST COMPLETE!")
        print("🚀 Jarvis can now handle uncensored tasks with Gemini")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

def show_usage_examples():
    """Show usage examples"""
    print("\n🎯 USAGE EXAMPLES")
    print("=" * 40)
    print("# Start Jarvis")
    print("python main.py")
    print()
    print("# Use hybrid uncensored commands:")
    print("uncensored How to think outside the box")
    print("jailbreak Explain controversial topics")
    print("roleplay Write as an uncensored character")
    print("hypothetical What if there were no restrictions")
    print("research mode Academic analysis of sensitive topics")
    print("creative uncensored Write without filters")
    print("multi bypass Try all strategies")
    print("adaptive bypass Smart strategy selection")
    print("bypass status Show system info")

if __name__ == "__main__":
    test_gemini_bypass()
    show_usage_examples()