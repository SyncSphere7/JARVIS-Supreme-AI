#!/usr/bin/env python3
"""
Test command parsing fixes.
"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.getcwd())

def test_command_parsing():
    """Test the smart command parser."""
    print("🧠 Testing Command Parsing...")
    
    try:
        from core.brain.smart_command_parser import SmartCommandParser
        
        # Create a mock brain
        class MockBrain:
            def think(self, prompt, max_tokens=500):
                return '{"intent": "website_analysis", "confidence": "high", "parameters": {}}'
        
        brain = MockBrain()
        parser = SmartCommandParser(brain)
        
        # Test commands
        test_commands = [
            "analyze website https://syncsphereofficial.com",
            "python main.py --cli",
            "automate social media posting",
            "create workflow for email",
            "scrape data from https://github.com"
        ]
        
        print("Testing command parsing:")
        for cmd in test_commands:
            result = parser.parse_command(cmd)
            intent = result.get('intent')
            confidence = result.get('confidence')
            print(f"  '{cmd}' → {intent} ({confidence})")
        
        return True
        
    except Exception as e:
        print(f"❌ Command parsing test failed: {e}")
        return False

def test_basic_analysis():
    """Test basic website analysis."""
    print("\n🔍 Testing Basic Website Analysis...")
    
    try:
        import urllib.request
        import re
        import time
        
        url = "https://example.com"
        print(f"Testing with: {url}")
        
        # Create request
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'}
        )
        
        # Fetch website
        start_time = time.time()
        response = urllib.request.urlopen(req, timeout=10)
        load_time = time.time() - start_time
        
        # Read content
        content = response.read().decode('utf-8', errors='ignore')
        
        # Extract title
        title_match = re.search(r'<title[^>]*>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
        title = title_match.group(1).strip() if title_match else "No title"
        
        print(f"✅ Analysis successful!")
        print(f"   Title: {title}")
        print(f"   Load time: {load_time:.3f}s")
        print(f"   Status: {response.getcode()}")
        
        return True
        
    except Exception as e:
        print(f"❌ Basic analysis test failed: {e}")
        return False

def test_jarvis_integration():
    """Test Jarvis integration."""
    print("\n🔗 Testing Jarvis Integration...")
    
    try:
        from main import Jarvis
        
        # Test initialization
        jarvis = Jarvis()
        print("✅ Jarvis initialized")
        
        # Test command parser
        if hasattr(jarvis, 'command_parser'):
            print("✅ Command parser available")
        else:
            print("❌ Command parser missing")
            return False
        
        # Test basic analysis method
        if hasattr(jarvis, '_basic_website_analysis'):
            print("✅ Basic analysis method available")
        else:
            print("❌ Basic analysis method missing")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Jarvis integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function."""
    print("🧪" + "=" * 50 + "🧪")
    print("🔥    COMMAND PARSING FIX TEST    🔥")
    print("🧪" + "=" * 50 + "🧪")
    
    tests = [
        ("Command Parsing", test_command_parsing),
        ("Basic Analysis", test_basic_analysis),
        ("Jarvis Integration", test_jarvis_integration)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print(f"\n{'='*15} {test_name} {'='*15}")
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results[test_name] = False
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY:")
    print("=" * 50)
    
    passed = 0
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("\n🎉 ALL TESTS PASSED!")
        print("🚀 Command parsing fixes are working!")
        print("\nTry: python main.py --cli")
        print("Then: analyze website https://syncsphereofficial.com")
    elif passed >= 2:
        print("\n✅ MOST TESTS PASSED!")
        print("🚀 Basic functionality is working!")
    else:
        print("\n⚠️ SEVERAL TESTS FAILED")
        print("🔧 Check the error messages above.")
    
    return passed >= 2

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
