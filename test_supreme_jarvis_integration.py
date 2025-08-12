#!/usr/bin/env python3
"""
Test Supreme Jarvis integration
"""
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from supreme_jarvis import SupremeJarvis


def test_supreme_jarvis():
    """Test Supreme Jarvis initialization and basic functionality"""
    print("🧪 Testing Supreme Jarvis Integration...")
    
    try:
        # Initialize Supreme Jarvis
        print("1. Initializing Supreme Jarvis...")
        supreme_jarvis = SupremeJarvis()
        
        # Check if Supreme Consciousness is active
        print(f"2. Supreme Consciousness active: {supreme_jarvis.supreme_mode_active}")
        
        if supreme_jarvis.supreme_mode_active:
            print("3. Testing Supreme Consciousness status...")
            status = supreme_jarvis.supreme_consciousness.get_supreme_status()
            print(f"   - Components: {len(status['components'])}")
            print(f"   - Active: {status['active']}")
            
            # Test components
            components = status['components']
            for name, info in components.items():
                print(f"   - {name}: {info['status']}")
        
        # Test basic brain functionality
        print("4. Testing basic brain functionality...")
        response = supreme_jarvis.brain.think("What is 2+2?", max_tokens=50)
        print(f"   Brain response: {response[:100]}...")
        
        # Cleanup
        print("5. Shutting down...")
        supreme_jarvis.shutdown()
        
        print("✅ Supreme Jarvis integration test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Supreme Jarvis integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_supreme_jarvis()
    sys.exit(0 if success else 1)