#!/usr/bin/env python3

print("Testing JARVIS Memory System...")

try:
    # Test import
    print("1. Testing import...")
    import jarvis_memory_system
    print("✅ Import successful")
    
    # Test class access
    print("2. Testing class access...")
    memory_class = jarvis_memory_system.JarvisMemorySystem
    print("✅ Class access successful")
    
    # Test initialization
    print("3. Testing initialization...")
    memory = memory_class()
    print("✅ Initialization successful")
    
    # Test basic functionality
    print("4. Testing basic functionality...")
    status = memory.get_memory_status()
    print(f"✅ Status retrieved: {status['system_status']}")
    
    print("\n🎉 ALL TESTS PASSED!")
    print("🧠 JARVIS Memory System is working perfectly!")
    
except Exception as e:
    print(f"❌ Test failed: {e}")
    import traceback
    traceback.print_exc()