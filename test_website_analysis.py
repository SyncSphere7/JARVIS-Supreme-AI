#!/usr/bin/env python3
"""
Test website analysis functionality.
"""
import urllib.request
import urllib.parse
import json
import re
import time
from datetime import datetime

def test_simple_analysis():
    """Test simple website analysis."""
    print("🔍 Testing Simple Website Analysis...")
    
    url = "https://example.com"
    print(f"📊 Analyzing: {url}")
    
    try:
        # Create request with headers
        req = urllib.request.Request(
            url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            }
        )
        
        # Fetch the website
        start_time = time.time()
        response = urllib.request.urlopen(req, timeout=30)
        load_time = time.time() - start_time
        
        # Read content
        content = response.read().decode('utf-8', errors='ignore')
        
        # Extract title
        title_match = re.search(r'<title[^>]*>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
        title = title_match.group(1).strip() if title_match else "No title found"
        title = re.sub(r'\s+', ' ', title)
        
        # Extract meta description
        desc_match = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\']([^"\']*)["\']', content, re.IGNORECASE)
        description = desc_match.group(1).strip() if desc_match else "No description found"
        
        # Basic metrics
        page_size = len(content.encode('utf-8'))
        status_code = response.getcode()
        
        # Count elements
        images_count = len(re.findall(r'<img[^>]*>', content, re.IGNORECASE))
        links_count = len(re.findall(r'<a[^>]*href[^>]*>', content, re.IGNORECASE))
        
        # Results
        result = {
            'url': url,
            'title': title,
            'description': description,
            'status_code': status_code,
            'load_time': round(load_time, 3),
            'page_size_kb': round(page_size / 1024, 2),
            'images_count': images_count,
            'links_count': links_count
        }
        
        print("✅ Analysis successful!")
        print(f"📄 Title: {title}")
        print(f"⏱️ Load Time: {load_time:.3f}s")
        print(f"📏 Page Size: {page_size/1024:.2f}KB")
        print(f"🖼️ Images: {images_count}")
        print(f"🔗 Links: {links_count}")
        
        return True
        
    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        return False

def test_jarvis_integration():
    """Test Jarvis integration."""
    print("\n🔗 Testing Jarvis Integration...")
    
    try:
        # Test imports
        import sys
        import os
        
        # Add current directory to path
        sys.path.insert(0, os.getcwd())
        
        from core.modules.simple_website_analyzer import SimpleWebsiteAnalyzer
        print("✅ SimpleWebsiteAnalyzer import successful")
        
        # Create a mock brain
        class MockBrain:
            def think(self, prompt, max_tokens=500):
                return "This is a mock AI response for testing purposes."
        
        brain = MockBrain()
        analyzer = SimpleWebsiteAnalyzer(brain)
        print("✅ SimpleWebsiteAnalyzer initialized")
        
        # Test analysis
        result = analyzer.analyze_website("https://example.com", deep_analysis=False)
        
        if result.get('success'):
            print("✅ Website analysis successful!")
            print(f"📊 Title: {result.get('basic_info', {}).get('title', 'N/A')}")
            return True
        else:
            print(f"❌ Website analysis failed: {result.get('error')}")
            return False
            
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function."""
    print("🧪" + "=" * 50 + "🧪")
    print("🔥    WEBSITE ANALYSIS TEST    🔥")
    print("🧪" + "=" * 50 + "🧪")
    
    tests = [
        ("Simple Analysis", test_simple_analysis),
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
        print("🚀 Website analysis is working!")
        print("\nTry: python main.py --cli")
        print("Then: analyze website https://example.com")
    else:
        print("\n⚠️ SOME TESTS FAILED")
        print("🔧 Check the error messages above.")
    
    return passed == len(tests)

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
