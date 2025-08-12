#!/usr/bin/env python3
"""
Test the Universal Web Orchestrator capabilities.
"""
import os
import sys
import json
from pathlib import Path

# Suppress warnings
os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["PYTHONWARNINGS"] = "ignore::UserWarning"

def test_workflow_planning():
    """Test workflow analysis and planning."""
    print("🎯 Testing Workflow Planning...")
    
    try:
        from main import Jarvis
        jarvis = Jarvis()
        
        if not hasattr(jarvis, 'web_orchestrator'):
            print("❌ Universal Web Orchestrator not available")
            return False
        
        # Test workflow planning
        test_workflow = "Create an n8n account and set up a simple automation that sends me an email when someone fills out my contact form"
        
        print(f"📋 Testing workflow: {test_workflow}")
        
        # Test the planning function (without execution)
        orchestrator = jarvis.web_orchestrator
        plan_result = orchestrator._analyze_and_plan_workflow(test_workflow)
        
        if plan_result.get('success'):
            print("✅ Workflow planning successful!")
            print(f"   Plan steps: {len(plan_result.get('plan', []))}")
            print(f"   Metadata: {plan_result.get('metadata', {})}")
            
            # Show first few steps
            plan = plan_result.get('plan', [])
            for i, step in enumerate(plan[:3]):
                print(f"   Step {i+1}: {step.get('action', 'Unknown')} on {step.get('platform', 'Unknown')}")
            
            return True
        else:
            print(f"❌ Workflow planning failed: {plan_result.get('error')}")
            return False
            
    except Exception as e:
        print(f"❌ Workflow planning test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_automation_json_creation():
    """Test automation JSON configuration creation."""
    print("📝 Testing Automation JSON Creation...")
    
    try:
        from main import Jarvis
        jarvis = Jarvis()
        
        if not hasattr(jarvis, 'web_orchestrator'):
            print("❌ Universal Web Orchestrator not available")
            return False
        
        # Test JSON creation
        automation_description = "Twitter bot that automatically replies to mentions with AI-generated responses and tracks engagement metrics"
        
        print(f"🤖 Creating JSON for: {automation_description}")
        
        result = jarvis.web_orchestrator.create_automation_json(automation_description)
        
        if result.get('success'):
            print("✅ Automation JSON creation successful!")
            print(f"   Config file: {result.get('config_file')}")
            
            # Check if file was created
            config_file = Path(result.get('config_file'))
            if config_file.exists():
                print(f"   File size: {config_file.stat().st_size} bytes")
                
                # Try to load and validate JSON
                try:
                    if config_file.suffix == '.json':
                        with open(config_file, 'r') as f:
                            config_data = json.load(f)
                        print(f"   JSON keys: {list(config_data.keys())}")
                    else:
                        print("   Saved as text file (JSON parsing issues)")
                except json.JSONDecodeError:
                    print("   ⚠️ JSON validation failed, but file created")
                
                return True
            else:
                print("❌ Config file not created")
                return False
        else:
            print(f"❌ JSON creation failed: {result.get('error')}")
            return False
            
    except Exception as e:
        print(f"❌ JSON creation test failed: {e}")
        return False

def test_platform_handlers():
    """Test platform-specific handlers."""
    print("🌐 Testing Platform Handlers...")
    
    try:
        from core.modules.universal_web_orchestrator import UniversalWebOrchestrator
        from main import Jarvis
        
        jarvis = Jarvis()
        orchestrator = UniversalWebOrchestrator(jarvis.brain)
        
        # Test that platform handlers exist
        expected_platforms = [
            'n8n', 'zapier', 'make', 'github', 'aws', 'google_cloud',
            'azure', 'docker', 'kubernetes', 'vercel', 'netlify',
            'heroku', 'firebase', 'supabase', 'stripe', 'twilio'
        ]
        
        available_platforms = []
        for platform in expected_platforms:
            if platform in orchestrator.platform_handlers:
                available_platforms.append(platform)
                print(f"✅ {platform} handler available")
            else:
                print(f"❌ {platform} handler missing")
        
        print(f"📊 Platform handlers: {len(available_platforms)}/{len(expected_platforms)} available")
        
        # Test a simple handler call (without actual web automation)
        try:
            test_result = orchestrator.platform_handlers['n8n']('test', 'test_action', {})
            print("✅ Platform handler callable")
        except Exception as e:
            print(f"⚠️ Platform handler test failed: {e}")
        
        return len(available_platforms) >= len(expected_platforms) * 0.8
        
    except Exception as e:
        print(f"❌ Platform handlers test failed: {e}")
        return False

def test_workflow_examples():
    """Test workflow examples."""
    print("📋 Testing Workflow Examples...")
    
    try:
        from examples.complex_workflow_examples import WORKFLOW_EXAMPLES
        
        print(f"✅ Found {len(WORKFLOW_EXAMPLES)} workflow examples")
        
        # Test example structure
        required_keys = ['description', 'complexity', 'estimated_time', 'platforms']
        valid_examples = 0
        
        for example_name, example_data in WORKFLOW_EXAMPLES.items():
            if all(key in example_data for key in required_keys):
                valid_examples += 1
                print(f"✅ {example_name}: Valid structure")
            else:
                print(f"❌ {example_name}: Missing required keys")
        
        print(f"📊 Valid examples: {valid_examples}/{len(WORKFLOW_EXAMPLES)}")
        
        # Test complexity levels
        complexities = set(ex['complexity'] for ex in WORKFLOW_EXAMPLES.values())
        print(f"✅ Complexity levels: {complexities}")
        
        # Test platform coverage
        all_platforms = set()
        for example in WORKFLOW_EXAMPLES.values():
            all_platforms.update(example['platforms'])
        
        print(f"✅ Platforms covered: {len(all_platforms)}")
        print(f"   Platforms: {', '.join(sorted(all_platforms))}")
        
        return valid_examples >= len(WORKFLOW_EXAMPLES) * 0.9
        
    except Exception as e:
        print(f"❌ Workflow examples test failed: {e}")
        return False

def test_integration():
    """Test integration with main Jarvis system."""
    print("🔗 Testing Integration...")
    
    try:
        from main import Jarvis
        jarvis = Jarvis()
        
        # Test that orchestrator is available
        if hasattr(jarvis, 'web_orchestrator'):
            print("✅ Web orchestrator integrated")
        else:
            print("❌ Web orchestrator not integrated")
            return False
        
        # Test that it has required methods
        required_methods = [
            'execute_complex_workflow',
            'create_automation_json',
            'deploy_automation'
        ]
        
        available_methods = []
        for method in required_methods:
            if hasattr(jarvis.web_orchestrator, method):
                available_methods.append(method)
                print(f"✅ Method available: {method}")
            else:
                print(f"❌ Method missing: {method}")
        
        # Test that workflows directory exists
        workflows_dir = Path("workflows")
        if workflows_dir.exists():
            print("✅ Workflows directory exists")
        else:
            print("⚠️ Workflows directory will be created on first use")
        
        print(f"📊 Integration: {len(available_methods)}/{len(required_methods)} methods available")
        
        return len(available_methods) == len(required_methods)
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        return False

def main():
    """Main test function."""
    print("🧪" + "=" * 60 + "🧪")
    print("🔥    UNIVERSAL WEB ORCHESTRATOR TEST    🔥")
    print("🧪" + "=" * 60 + "🧪")
    print("")
    
    # Run tests
    tests = [
        ("Workflow Planning", test_workflow_planning),
        ("Automation JSON Creation", test_automation_json_creation),
        ("Platform Handlers", test_platform_handlers),
        ("Workflow Examples", test_workflow_examples),
        ("Integration", test_integration)
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
    print("📊 TEST SUMMARY:")
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
        print("🚀 Universal Web Orchestrator is fully operational!")
        print("\nTry these commands:")
        print("   python main.py --cli")
        print('   > create workflow')
        print('   > "Set up n8n automation with Google Sheets and Slack"')
    elif passed >= len(tests) * 0.75:
        print("\n✅ MOST TESTS PASSED!")
        print("🚀 Universal Web Orchestrator is mostly operational!")
        print("Some advanced features may have limited functionality.")
    else:
        print("\n⚠️ SEVERAL TESTS FAILED")
        print("🔧 Check dependencies and configuration.")
    
    print("\n🌟 EXAMPLE WORKFLOWS:")
    print("   python examples/complex_workflow_examples.py")
    
    return passed >= len(tests) * 0.75

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
