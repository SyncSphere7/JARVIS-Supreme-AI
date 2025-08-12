#!/usr/bin/env python3
"""
Comprehensive test for all Jarvis capabilities.
Tests smart routing, web scraping, output formatting, and integration.
"""
import os
import sys
from pathlib import Path

# Suppress warnings
os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["PYTHONWARNINGS"] = "ignore::UserWarning"

def test_smart_command_routing():
    """Test smart command parsing and routing."""
    print("🧠 Testing Smart Command Routing...")
    
    try:
        from main import Jarvis
        jarvis = Jarvis()
        
        if not hasattr(jarvis, 'command_parser'):
            print("❌ Command parser not available")
            return False
        
        # Test various command types
        test_commands = [
            # Website analysis
            ("analyze website https://example.com", "website_analysis"),
            ("do an analysis of this site https://google.com", "website_analysis"),
            
            # Web scraping
            ("scrape data from https://github.com", "web_scraping"),
            ("extract content from https://reddit.com", "web_scraping"),
            
            # Website creation
            ("create a website for my business", "website_creation"),
            ("build me a portfolio site", "website_creation"),
            
            # Automation
            ("automate my social media posting", "automation_workflow"),
            ("create workflow for email notifications", "automation_workflow"),
            
            # ML training
            ("train a model with my data", "ml_training"),
            ("automl pipeline", "ml_training"),
            
            # API creation
            ("create api account for Meta", "api_creation"),
            ("setup Twitter API", "api_creation"),
        ]
        
        correct_detections = 0
        
        for command, expected_intent in test_commands:
            parsed = jarvis.command_parser.parse_command(command)
            detected_intent = parsed.get('intent')
            confidence = parsed.get('confidence')
            
            print(f"🧪 '{command[:50]}...'")
            print(f"   Expected: {expected_intent}")
            print(f"   Detected: {detected_intent} (confidence: {confidence})")
            
            if detected_intent == expected_intent:
                correct_detections += 1
                print("   ✅ Correct")
            else:
                print("   ❌ Incorrect")
        
        accuracy = (correct_detections / len(test_commands)) * 100
        print(f"📊 Command routing accuracy: {accuracy:.1f}% ({correct_detections}/{len(test_commands)})")
        
        return accuracy >= 80  # 80% accuracy threshold
        
    except Exception as e:
        print(f"❌ Smart routing test failed: {e}")
        return False

def test_web_scraper():
    """Test web scraping capabilities."""
    print("🕷️ Testing Web Scraper...")
    
    try:
        from main import Jarvis
        jarvis = Jarvis()
        
        if not hasattr(jarvis, 'web_scraper'):
            print("❌ Web scraper not available")
            return False
        
        # Test with a simple, reliable website
        test_url = "https://httpbin.org/html"
        print(f"🔍 Testing scraping: {test_url}")
        
        result = jarvis.web_scraper.scrape_website(test_url)
        
        if result.get('success'):
            print("✅ Web scraping successful!")
            
            # Check result structure
            required_keys = ['metadata', 'data', 'links', 'text_analysis']
            available_keys = []
            
            for key in required_keys:
                if key in result:
                    available_keys.append(key)
                    print(f"✅ {key} data available")
                else:
                    print(f"❌ {key} data missing")
            
            # Check metadata
            metadata = result.get('metadata', {})
            if metadata:
                print(f"📊 Scraped items: {metadata.get('total_items', 0)}")
                print(f"🔗 Links found: {len(result.get('links', []))}")
                print(f"📄 Text analysis: {result.get('text_analysis', {}).get('word_count', 0)} words")
            
            return len(available_keys) >= 3  # At least 3 components should work
        else:
            print(f"❌ Web scraping failed: {result.get('error')}")
            return False
            
    except Exception as e:
        print(f"❌ Web scraper test failed: {e}")
        return False

def test_output_formatter():
    """Test multi-format output capabilities."""
    print("📄 Testing Output Formatter...")
    
    try:
        from main import Jarvis
        jarvis = Jarvis()
        
        if not hasattr(jarvis, 'output_formatter'):
            print("❌ Output formatter not available")
            return False
        
        # Test data
        test_data = {
            'title': 'Test Report',
            'metadata': {
                'created': '2024-01-01',
                'type': 'test',
                'version': '1.0'
            },
            'data': {
                'items': [
                    {'name': 'Item 1', 'value': 100, 'category': 'A'},
                    {'name': 'Item 2', 'value': 200, 'category': 'B'},
                    {'name': 'Item 3', 'value': 150, 'category': 'A'}
                ],
                'summary': {
                    'total_items': 3,
                    'total_value': 450
                }
            }
        }
        
        # Test available formats
        available_formats = jarvis.output_formatter.get_available_formats()
        print(f"📋 Available formats: {available_formats}")
        
        # Test export to available formats
        test_formats = ['json', 'csv', 'txt', 'html']
        # Only test formats that are available
        test_formats = [fmt for fmt in test_formats if fmt in available_formats]
        
        if not test_formats:
            print("⚠️ No basic formats available for testing")
            return False
        
        print(f"🧪 Testing export to: {test_formats}")
        
        result = jarvis.output_formatter.export_data(
            test_data, 
            'test_export', 
            test_formats
        )
        
        if result.get('success'):
            print("✅ Export successful!")
            
            exported_files = result.get('exported_files', {})
            for format_type, file_path in exported_files.items():
                if Path(file_path).exists():
                    file_size = Path(file_path).stat().st_size
                    print(f"✅ {format_type.upper()}: {file_path} ({file_size} bytes)")
                else:
                    print(f"❌ {format_type.upper()}: File not created")
            
            return len(exported_files) >= 2  # At least 2 formats should work
        else:
            print(f"❌ Export failed: {result.get('error')}")
            return False
            
    except Exception as e:
        print(f"❌ Output formatter test failed: {e}")
        return False

def test_integration():
    """Test integration between all components."""
    print("🔗 Testing System Integration...")
    
    try:
        from main import Jarvis
        jarvis = Jarvis()
        
        # Test that all advanced modules are available
        required_modules = [
            'command_parser',
            'website_analyzer', 
            'web_scraper',
            'web_orchestrator',
            'ml_capabilities',
            'output_formatter'
        ]
        
        available_modules = []
        for module in required_modules:
            if hasattr(jarvis, module):
                available_modules.append(module)
                print(f"✅ {module} available")
            else:
                print(f"❌ {module} missing")
        
        # Test that directories are created
        expected_dirs = ['exports', 'scraped_data', 'workflows', 'website_analyses']
        created_dirs = []
        
        for dir_name in expected_dirs:
            if Path(dir_name).exists():
                created_dirs.append(dir_name)
                print(f"✅ Directory exists: {dir_name}")
            else:
                print(f"⚠️ Directory will be created on first use: {dir_name}")
        
        print(f"📊 Integration: {len(available_modules)}/{len(required_modules)} modules available")
        
        return len(available_modules) >= len(required_modules) * 0.8  # 80% of modules should be available
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        return False

def test_end_to_end_workflow():
    """Test a complete end-to-end workflow."""
    print("🎯 Testing End-to-End Workflow...")
    
    try:
        from main import Jarvis
        jarvis = Jarvis()
        
        # Simulate a complete workflow: analyze website -> export results
        test_url = "https://example.com"
        
        print(f"🔍 Step 1: Analyzing website {test_url}")
        
        # Test website analysis
        if hasattr(jarvis, 'website_analyzer'):
            analysis_result = jarvis.website_analyzer.analyze_website(test_url, deep_analysis=False)
            
            if analysis_result.get('success'):
                print("✅ Website analysis completed")
                
                # Test export of analysis results
                if hasattr(jarvis, 'output_formatter'):
                    print("📄 Step 2: Exporting analysis results")
                    
                    export_result = jarvis.output_formatter.export_data(
                        analysis_result,
                        'end_to_end_test',
                        ['json', 'txt']
                    )
                    
                    if export_result.get('success'):
                        print("✅ Export completed")
                        print(f"📁 Files created: {list(export_result['exported_files'].keys())}")
                        return True
                    else:
                        print(f"❌ Export failed: {export_result.get('error')}")
                        return False
                else:
                    print("⚠️ Output formatter not available, but analysis worked")
                    return True
            else:
                print(f"❌ Website analysis failed: {analysis_result.get('error')}")
                return False
        else:
            print("❌ Website analyzer not available")
            return False
            
    except Exception as e:
        print(f"❌ End-to-end test failed: {e}")
        return False

def main():
    """Main test function."""
    print("🧪" + "=" * 60 + "🧪")
    print("🔥    COMPREHENSIVE JARVIS SYSTEM TEST    🔥")
    print("🧪" + "=" * 60 + "🧪")
    print("")
    
    # Run tests
    tests = [
        ("Smart Command Routing", test_smart_command_routing),
        ("Web Scraper", test_web_scraper),
        ("Output Formatter", test_output_formatter),
        ("System Integration", test_integration),
        ("End-to-End Workflow", test_end_to_end_workflow)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results[test_name] = False
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 COMPREHENSIVE TEST SUMMARY:")
    print("=" * 60)
    
    passed = 0
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("\n🎉 ALL TESTS PASSED!")
        print("🚀 Jarvis comprehensive system is fully operational!")
        print("\n🎯 READY FOR PRODUCTION USE!")
        print("\nTry these commands:")
        print("   python main.py --cli")
        print("   > analyze website https://example.com")
        print("   > scrape data from https://github.com")
        print("   > automate social media posting")
    elif passed >= len(tests) * 0.8:
        print("\n✅ MOST TESTS PASSED!")
        print("🚀 Jarvis system is mostly operational!")
        print("Some advanced features may have limited functionality.")
    else:
        print("\n⚠️ SEVERAL TESTS FAILED")
        print("🔧 Check dependencies and configuration.")
        print("Run: python install_advanced_deps.py")
    
    print("\n💡 EXAMPLE COMMANDS:")
    print("   analyze website https://syncsphereofficial.com")
    print("   scrape data from https://news.ycombinator.com")
    print("   create workflow for email automation")
    print("   train model with customer_data.csv")
    
    return passed >= len(tests) * 0.8

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
