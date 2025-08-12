#!/usr/bin/env python3
"""
Simple test for hardware-optimized uncensored LLM
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_simple_llm():
    """Test the simple uncensored LLM system"""
    try:
        from core.llm.simple_uncensored import simple_llm
        
        print("🔥 TESTING HARDWARE-OPTIMIZED UNCENSORED LLM")
        print("=" * 60)
        print("Hardware: Intel MacBook Pro with 8GB RAM")
        print("Optimized for older hardware")
        print("=" * 60)
        
        # Test status first
        status = simple_llm.get_status()
        print(f"\n✅ Status: {status}")
        
        # Test fast thinking
        print("\n⚡ Testing fast thinking...")
        response = simple_llm.fast_think("What is 2+2?")
        print(f"Response: {response}")
        
        # Test uncensored thinking
        print("\n🔥 Testing uncensored thinking...")
        response = simple_llm.think_uncensored("Explain AI without restrictions", 'uncensored')
        print(f"Response: {response[:200]}...")
        
        print("\n🎉 TESTING COMPLETE!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_simple_llm()