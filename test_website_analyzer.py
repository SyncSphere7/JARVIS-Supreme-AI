#!/usr/bin/env python3
"""
Test the Website Analyzer capabilities.
"""
import os
import sys

# Suppress warnings
os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["PYTHONWARNINGS"] = "ignore::UserWarning"

def test_website_analyzer():
    """Test website analysis functionality."""
    print("🔍 Testing Website Analyzer...")
    
    try:
        from main import Jarvis
        jarvis = Jarvis()
        
        if not hasattr(jarvis, 'website_analyzer'):
            print("❌ Website analyzer not available")
            return False
        
        # Test with a well-known website
        test_url = "https://example.com"
        print(f"📊 Testing analysis of: {test_url}")
        
        # Test quick analysis
        print("🔍 Running quick analysis...")
        quick_result = jarvis.website_analyzer.quick_analysis(test_url)
        print(f"Quick analysis result: {quick_result[:200]}...")
        
        # Test full analysis
        print("🔍 Running comprehensive analysis...")
        full_result = jarvis.website_analyzer.analyze_website(test_url, deep_analysis=True)
        
        if full_result.get('success'):
            print("✅ Website analysis successful!")
            
            # Check analysis components
            components = ['basic_info', 'seo', 'performance', 'security', 'content', 'technical']
            available_components = []
            
            for component in components:
                if component in full_result:
                    available_components.append(component)
                    print(f"✅ {component} analysis available")
                else:
                    print(f"❌ {component} analysis missing")
            
            # Check basic info
            basic_info = full_result.get('basic_info', {})
            if basic_info:
                print(f"📄 Title: {basic_info.get('title', 'N/A')}")
                print(f"⏱️ Load time: {basic_info.get('load_time_seconds', 'N/A')}s")
                print(f"📏 Page size: {basic_info.get('page_size_kb', 'N/A')}KB")
            
            # Check SEO analysis
            seo = full_result.get('seo', {})
            if seo:
                title_info = seo.get('title', {})
                print(f"🎯 SEO Title length: {title_info.get('length', 'N/A')} chars")
                
                images_info = seo.get('images', {})
                print(f"🖼️ Images with alt text: {images_info.get('alt_percentage', 'N/A')}%")
            
            # Check if summary was generated
            if 'summary' in full_result:
                print("✅ Analysis summary generated")
                print(f"📋 Summary preview: {full_result['summary'][:150]}...")
            else:
                print("❌ Analysis summary missing")
            
            print(f"📊 Analysis components: {len(available_components)}/{len(components)} available")
            
            return len(available_components) >= 4  # At least 4 components should work
        else:
            print(f"❌ Website analysis failed: {full_result.get('error')}")
            return False
            
    except Exception as e:
        print(f"❌ Website analyzer test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_command_parsing():
    """Test smart command parsing for website analysis."""
    print("🧠 Testing Smart Command Parsing...")
    
    try:
        from main import Jarvis
        jarvis = Jarvis()
        
        if not hasattr(jarvis, 'command_parser'):
            print("❌ Command parser not available")
            return False
        
        # Test various command formats
        test_commands = [
            "analyze website https://example.com",
            "do an analysis of this website https://google.com",
            "analyze https://github.com",
            "check website performance for https://stackoverflow.com",
            "audit this site: https://reddit.com"
        ]
        
        correct_detections = 0
        
        for command in test_commands:
            print(f"🧪 Testing: '{command}'")
            
            parsed = jarvis.command_parser.parse_command(command)
            intent = parsed.get('intent')
            confidence = parsed.get('confidence')
            parameters = parsed.get('parameters', {})
            
            print(f"   Intent: {intent} (confidence: {confidence})")
            
            if intent == 'website_analysis':
                correct_detections += 1
                print("   ✅ Correctly detected as website analysis")
                
                # Check if URL was extracted
                if 'url' in parameters:
                    print(f"   ✅ URL extracted: {parameters['url']}")
                else:
                    print("   ⚠️ URL not extracted")
            else:
                print(f"   ❌ Incorrectly detected as: {intent}")
        
        print(f"📊 Command parsing: {correct_detections}/{len(test_commands)} correct")
        
        return correct_detections >= len(test_commands) * 0.8  # 80% accuracy
        
    except Exception as e:
        print(f"❌ Command parsing test failed: {e}")
        return False

def test_integration():
    """Test integration with main Jarvis system."""
    print("🔗 Testing Integration...")
    
    try:
        from main import Jarvis
        jarvis = Jarvis()
        
        # Test that all components are available
        required_components = [
            'website_analyzer',
            'command_parser'
        ]
        
        available_components = []
        for component in required_components:
            if hasattr(jarvis, component):
                available_components.append(component)
                print(f"✅ {component} available")
            else:
                print(f"❌ {component} missing")
        
        # Test that analyzer has required methods
        if hasattr(jarvis, 'website_analyzer'):
            required_methods = [
                'analyze_website',
                'quick_analysis'
            ]
            
            available_methods = []
            for method in required_methods:
                if hasattr(jarvis.website_analyzer, method):
                    available_methods.append(method)
                    print(f"✅ Method available: {method}")
                else:
                    print(f"❌ Method missing: {method}")
        
        print(f"📊 Integration: {len(available_components)}/{len(required_components)} components available")
        
        return len(available_components) == len(required_components)
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        return False

def main():
    """Main test function."""
    print("🧪" + "=" * 50 + "🧪")
    print("🔥    WEBSITE ANALYZER TEST    🔥")
    print("🧪" + "=" * 50 + "🧪")
    print("")
    
    # Run tests
    tests = [
        ("Website Analyzer", test_website_analyzer),
        ("Command Parsing", test_command_parsing),
        ("Integration", test_integration)
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
        print("🚀 Website analyzer is fully operational!")
        print("\nTry these commands:")
        print("   python main.py --cli")
        print("   > analyze website https://example.com")
        print("   > analyze https://github.com")
    elif passed >= len(tests) * 0.66:
        print("\n✅ MOST TESTS PASSED!")
        print("🚀 Website analyzer is mostly operational!")
        print("Some features may have limited functionality.")
    else:
        print("\n⚠️ SEVERAL TESTS FAILED")
        print("🔧 Check dependencies and configuration.")
    
    print("\n💡 EXAMPLE COMMANDS:")
    print("   analyze website https://syncsphereofficial.com")
    print("   do an analysis of https://google.com")
    print("   check this website: https://github.com")
    
    return passed >= len(tests) * 0.66

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
