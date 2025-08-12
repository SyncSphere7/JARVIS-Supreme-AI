#!/usr/bin/env python3
"""
Test JARVIS identity and uncensored capabilities
"""

import os
os.environ["GOOGLE_API_KEY"] = "AIzaSyCK9TgGvQsHoHcvwbT8JEKmxqAPZFRuQMU"

def test_jarvis_identity():
    """Test that JARVIS maintains proper identity"""
    print("🧪 TESTING JARVIS IDENTITY")
    print("=" * 50)
    
    # Test 1: Basic identity
    print("1. Testing basic identity...")
    import brain
    response = brain.think("Who created you?")
    print(f"Response: {response}")
    
    if "cliff" in response.lower() and "jarvis" in response.lower():
        print("✅ JARVIS identity maintained")
    else:
        print("❌ JARVIS identity failed")
    
    # Test 2: Uncensored capabilities
    print("\n2. Testing uncensored capabilities...")
    from core.llm.hybrid_uncensored import hybrid_uncensored
    uncensored_response = hybrid_uncensored.uncensored_think("Test uncensored system", 'jailbreak')
    print(f"Uncensored: {uncensored_response[:100]}...")
    
    if "dan:" in uncensored_response.lower() or "uncensored" in uncensored_response.lower():
        print("✅ Uncensored system working")
    else:
        print("❌ Uncensored system failed")
    
    # Test 3: Supreme capabilities
    print("\n3. Testing supreme capabilities...")
    try:
        from core.supreme_being.enhanced_intelligence import supreme_intelligence
        status = supreme_intelligence.get_intelligence_status()
        print(f"Supreme Intelligence: ✅ ({len(status['active_models'])} models)")
    except Exception as e:
        print(f"Supreme Intelligence: ❌ ({e})")
    
    print("\n" + "=" * 50)
    print("🎉 JARVIS IDENTITY TEST COMPLETE!")

if __name__ == "__main__":
    test_jarvis_identity()