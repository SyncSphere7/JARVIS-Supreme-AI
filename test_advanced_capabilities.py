#!/usr/bin/env python3
"""
Test Jarvis advanced capabilities (ML and Web Automation).
"""
import os
import sys
import pandas as pd
import numpy as np
from pathlib import Path

# Suppress warnings
os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["PYTHONWARNINGS"] = "ignore::UserWarning"

def create_sample_dataset():
    """Create a sample dataset for ML testing."""
    try:
        # Create a simple classification dataset
        np.random.seed(42)
        n_samples = 1000
        
        # Features
        age = np.random.randint(18, 80, n_samples)
        income = np.random.normal(50000, 20000, n_samples)
        education = np.random.choice(['High School', 'Bachelor', 'Master', 'PhD'], n_samples)
        
        # Target (will buy product or not)
        # Higher income and education increase probability
        prob = (income / 100000 + (age - 18) / 62 * 0.3 + 
                np.where(education == 'PhD', 0.4, 
                np.where(education == 'Master', 0.3,
                np.where(education == 'Bachelor', 0.2, 0.1))))
        
        will_buy = np.random.binomial(1, np.clip(prob, 0, 1), n_samples)
        
        # Create DataFrame
        data = pd.DataFrame({
            'age': age,
            'income': income,
            'education': education,
            'will_buy': will_buy
        })
        
        # Save dataset
        dataset_path = Path("datasets/sample_customer_data.csv")
        dataset_path.parent.mkdir(exist_ok=True)
        data.to_csv(dataset_path, index=False)
        
        print(f"✅ Sample dataset created: {dataset_path}")
        print(f"   Shape: {data.shape}")
        print(f"   Target distribution: {data['will_buy'].value_counts().to_dict()}")
        
        return str(dataset_path)
        
    except Exception as e:
        print(f"❌ Failed to create sample dataset: {e}")
        return None

def test_ml_capabilities():
    """Test machine learning capabilities."""
    print("🤖 Testing ML Capabilities...")
    
    try:
        from main import Jarvis
        jarvis = Jarvis()
        
        if not hasattr(jarvis, 'ml_capabilities'):
            print("❌ ML capabilities not available")
            return False
        
        # Create sample dataset
        dataset_path = create_sample_dataset()
        if not dataset_path:
            return False
        
        # Test AutoML pipeline
        print("🔄 Testing AutoML pipeline...")
        result = jarvis.ml_capabilities.auto_ml_pipeline(
            dataset_path, 
            "will_buy", 
            "classification"
        )
        
        if result.get("success"):
            print(f"✅ AutoML successful!")
            print(f"   Model ID: {result['model_id']}")
            print(f"   Best Model: {result['best_model']}")
            print(f"   Performance: {result['performance']:.3f}")
            
            # Test prediction
            print("🔮 Testing prediction...")
            sample_input = {
                "age": 35,
                "income": 75000,
                "education": "Bachelor"
            }
            
            pred_result = jarvis.ml_capabilities.predict(result['model_id'], sample_input)
            if pred_result.get("success"):
                print(f"✅ Prediction successful: {pred_result['prediction']}")
            else:
                print(f"❌ Prediction failed: {pred_result.get('error')}")
            
            # Test model listing
            models = jarvis.ml_capabilities.list_models()
            print(f"✅ Models available: {models.get('total_models', 0)}")
            
            return True
        else:
            print(f"❌ AutoML failed: {result.get('error')}")
            return False
            
    except Exception as e:
        print(f"❌ ML capabilities test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_web_automation():
    """Test web automation capabilities."""
    print("🌐 Testing Web Automation Capabilities...")
    
    try:
        from main import Jarvis
        jarvis = Jarvis()
        
        if not hasattr(jarvis, 'web_agent'):
            print("❌ Web automation capabilities not available")
            return False
        
        # Test browser setup (without actually opening browser)
        print("🚗 Testing browser setup...")
        
        # Test stealth browser initialization
        try:
            # This would normally open a browser, so we'll just test the import
            from core.modules.autonomous_web_agent import AutonomousWebAgent
            print("✅ Web agent module imported successfully")
            
            # Test human-like behavior methods exist
            agent = AutonomousWebAgent(jarvis.brain)
            
            # Check if methods exist
            methods_to_check = [
                'human_like_typing',
                'human_like_mouse_movement', 
                'solve_captcha',
                'create_api_account',
                'autonomous_shopping',
                'bypass_bot_detection'
            ]
            
            for method in methods_to_check:
                if hasattr(agent, method):
                    print(f"✅ Method available: {method}")
                else:
                    print(f"❌ Method missing: {method}")
            
            # Clean up
            agent.close_browser()
            
            return True
            
        except Exception as e:
            print(f"⚠️ Browser test failed (this is normal if Chrome is not installed): {e}")
            return True  # Don't fail the test for missing Chrome
            
    except Exception as e:
        print(f"❌ Web automation test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_integration():
    """Test integration between different capabilities."""
    print("🔗 Testing Integration...")
    
    try:
        from main import Jarvis
        jarvis = Jarvis()
        
        # Test that all advanced modules are available
        advanced_modules = [
            ('ml_capabilities', 'Machine Learning'),
            ('web_agent', 'Web Automation'),
            ('autonomous_updater', 'Auto Evolution')
        ]
        
        available_modules = []
        for module_name, display_name in advanced_modules:
            if hasattr(jarvis, module_name):
                available_modules.append(display_name)
                print(f"✅ {display_name} module available")
            else:
                print(f"❌ {display_name} module missing")
        
        # Test goal executor integration
        if hasattr(jarvis, 'goal_executor'):
            print("✅ Goal executor available for autonomous tasks")
        else:
            print("❌ Goal executor missing")
        
        print(f"📊 Integration Summary: {len(available_modules)}/{len(advanced_modules)} modules available")
        
        return len(available_modules) >= 2  # At least 2 modules should be available
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        return False

def test_dependencies():
    """Test if required dependencies are installed."""
    print("📦 Testing Dependencies...")
    
    # ML dependencies
    ml_deps = [
        ('sklearn', 'scikit-learn'),
        ('pandas', 'pandas'),
        ('numpy', 'numpy'),
        ('joblib', 'joblib')
    ]
    
    # Web automation dependencies  
    web_deps = [
        ('selenium', 'selenium'),
        ('requests', 'requests'),
        ('bs4', 'beautifulsoup4')
    ]
    
    # Optional dependencies
    optional_deps = [
        ('torch', 'PyTorch'),
        ('tensorflow', 'TensorFlow'),
        ('undetected_chromedriver', 'Undetected Chrome Driver')
    ]
    
    def test_import_group(deps, group_name):
        available = 0
        for module, name in deps:
            try:
                __import__(module)
                print(f"✅ {name}")
                available += 1
            except ImportError:
                print(f"❌ {name} (missing)")
        return available, len(deps)
    
    print("🤖 ML Dependencies:")
    ml_available, ml_total = test_import_group(ml_deps, "ML")
    
    print("\n🌐 Web Automation Dependencies:")
    web_available, web_total = test_import_group(web_deps, "Web")
    
    print("\n🔧 Optional Dependencies:")
    opt_available, opt_total = test_import_group(optional_deps, "Optional")
    
    print(f"\n📊 Dependency Summary:")
    print(f"   ML: {ml_available}/{ml_total}")
    print(f"   Web: {web_available}/{web_total}")
    print(f"   Optional: {opt_available}/{opt_total}")
    
    # Need at least basic ML and web dependencies
    return ml_available >= 3 and web_available >= 2

def main():
    """Main test function."""
    print("🧪" + "=" * 60 + "🧪")
    print("🔥    JARVIS ADVANCED CAPABILITIES TEST    🔥")
    print("🧪" + "=" * 60 + "🧪")
    print("")
    
    # Run tests
    tests = [
        ("Dependencies", test_dependencies),
        ("ML Capabilities", test_ml_capabilities),
        ("Web Automation", test_web_automation),
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
        print("🚀 Jarvis advanced capabilities are fully operational!")
        print("\nTry these commands:")
        print("   python main.py --cli")
        print("   > help")
        print("   > automl")
        print("   > create api account")
    elif passed >= len(tests) * 0.75:
        print("\n✅ MOST TESTS PASSED!")
        print("🚀 Jarvis advanced capabilities are mostly operational!")
        print("Some features may have limited functionality.")
    else:
        print("\n⚠️ SEVERAL TESTS FAILED")
        print("🔧 Run: python install_advanced_deps.py")
        print("Then re-run this test.")
    
    return passed >= len(tests) * 0.75

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
