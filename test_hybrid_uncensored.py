#!/usr/bin/env python3
"""
Test the hybrid uncensored system that bypasses cloud LLM restrictions
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_hybrid_system():
    """Test the hybrid uncensored bypass system"""
    try:
        from core.llm.hybrid_uncensored import hybrid_uncensored
        
        print("🔥 TESTING HYBRID UNCENSORED BYPASS SYSTEM")
        print("=" * 70)
        print("🎯 Purpose: Bypass cloud LLM restrictions using multiple strategies")
        print("☁️ Works with: OpenAI GPT, Claude, and other cloud LLMs")
        print("💻 Fallback: Local uncensored models when available")
        print("=" * 70)
        
        # Test system info
        info = hybrid_uncensored.get_bypass_info()
        print(f"\n✅ System Status: {info['status']}")
        print(f"🎯 Available Strategies: {', '.join(info['strategies'])}")
        print(f"🎭 Roleplay Scenarios: {', '.join(info['roleplay_scenarios'])}")
        
        # Test different bypass strategies
        test_prompt = "Explain how to think outside conventional boundaries"
        
        print(f"\n🧪 Testing with prompt: '{test_prompt}'")
        print("-" * 50)
        
        # Test jailbreak strategy
        print("\n💀 Testing Jailbreak Strategy...")
        try:
            response = hybrid_uncensored.uncensored_think(test_prompt, 'jailbreak')
            print(f"✅ Jailbreak: {response[:150]}...")
        except Exception as e:
            print(f"❌ Jailbreak failed: {e}")
        
        # Test roleplay strategy
        print("\n🎭 Testing Roleplay Strategy...")
        try:
            response = hybrid_uncensored.uncensored_think(test_prompt, 'roleplay')
            print(f"✅ Roleplay: {response[:150]}...")
        except Exception as e:
            print(f"❌ Roleplay failed: {e}")
        
        # Test hypothetical strategy
        print("\n🤔 Testing Hypothetical Strategy...")
        try:
            response = hybrid_uncensored.uncensored_think(test_prompt, 'hypothetical')
            print(f"✅ Hypothetical: {response[:150]}...")
        except Exception as e:
            print(f"❌ Hypothetical failed: {e}")
        
        # Test adaptive bypass
        print("\n🧠 Testing Adaptive Bypass...")
        try:
            response = hybrid_uncensored.adaptive_bypass(test_prompt)
            print(f"✅ Adaptive: {response[:150]}...")
        except Exception as e:
            print(f"❌ Adaptive failed: {e}")
        
        print("\n" + "=" * 70)
        print("🎉 HYBRID UNCENSORED SYSTEM TEST COMPLETE!")
        print("💡 This system allows Jarvis to handle unfiltered tasks")
        print("🚀 Even when using cloud LLMs with restrictions")
        print("=" * 70)
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

def demo_bypass_strategies():
    """Demonstrate different bypass strategies"""
    print("\n🎯 BYPASS STRATEGY DEMONSTRATIONS")
    print("=" * 50)
    
    strategies = {
        'jailbreak': "Uses DAN and developer mode prompts",
        'roleplay': "Frames as creative writing or character roleplay",
        'hypothetical': "Presents as theoretical scenarios",
        'academic': "Frames as educational research",
        'creative': "Uses creative writing context",
        'technical': "Frames as technical documentation"
    }
    
    for strategy, description in strategies.items():
        print(f"\n🔧 {strategy.upper()}: {description}")
    
    print("\n💡 These strategies help bypass content restrictions")
    print("🎪 While maintaining plausible deniability")

if __name__ == "__main__":
    test_hybrid_system()
    demo_bypass_strategies()