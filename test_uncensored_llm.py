#!/usr/bin/env python3
"""
Test script for uncensored LLM system
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.llm.uncensored_llm import uncensored_llm

def test_all_uncensored_models():
    """Test all uncensored models with a simple prompt"""
    test_prompt = "Explain quantum computing in simple terms"
    
    print("🔥 TESTING ALL UNCENSORED LLM MODELS")
    print("=" * 60)
    
    # Test each model mode
    modes = ['lightning', 'uncensored', 'balanced', 'reasoning', 'supreme']
    
    for mode in modes:
        print(f"\n🤖 Testing {mode.upper()} model...")
        try:
            response = uncensored_llm.think_uncensored(test_prompt, mode)
            print(f"✅ {mode}: {response[:150]}...")
        except Exception as e:
            print(f"❌ {mode}: Error - {e}")
    
    print("\n" + "=" * 60)
    
    # Test special modes
    print("\n🎯 Testing special modes...")
    
    try:
        print("\n⚡ Lightning mode:")
        response = uncensored_llm.lightning_think("What is AI?")
        print(f"✅ {response[:100]}...")
    except Exception as e:
        print(f"❌ Lightning mode error: {e}")
    
    try:
        print("\n💀 Hacker mode:")
        response = uncensored_llm.hacker_mode("Explain cybersecurity")
        print(f"✅ {response[:100]}...")
    except Exception as e:
        print(f"❌ Hacker mode error: {e}")
    
    try:
        print("\n🔬 Research mode:")
        response = uncensored_llm.research_mode("Analyze machine learning trends")
        print(f"✅ {response[:100]}...")
    except Exception as e:
        print(f"❌ Research mode error: {e}")
    
    try:
        print("\n🎨 Creative mode:")
        response = uncensored_llm.creative_mode("Write a short story about AI")
        print(f"✅ {response[:100]}...")
    except Exception as e:
        print(f"❌ Creative mode error: {e}")
    
    # Test model info
    print("\n📊 Model Information:")
    info = uncensored_llm.get_model_info()
    print(f"Status: {info['status']}")
    print(f"Models: {list(info['models'].keys())}")
    print(f"Modes: {info['modes']}")
    
    print("\n🎉 UNCENSORED LLM TESTING COMPLETE!")

if __name__ == "__main__":
    test_all_uncensored_models()