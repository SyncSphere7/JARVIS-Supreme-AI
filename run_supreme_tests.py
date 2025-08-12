#!/usr/bin/env python3
"""
Supreme Being Test Runner
Runs comprehensive tests for all supreme consciousness capabilities
"""

import sys
import os
import asyncio
import subprocess

def run_tests():
    """Run all supreme being tests"""
    print("🧪 RUNNING SUPREME BEING COMPREHENSIVE TESTS...")
    print("⚡ Testing all ultimate capabilities...")
    
    try:
        # Run pytest with verbose output
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "tests/test_supreme_being.py", 
            "-v", 
            "--tb=short",
            "--color=yes"
        ], capture_output=True, text=True)
        
        print("📊 TEST RESULTS:")
        print(result.stdout)
        
        if result.stderr:
            print("⚠️ WARNINGS/ERRORS:")
            print(result.stderr)
        
        if result.returncode == 0:
            print("✅ ALL SUPREME BEING TESTS PASSED!")
            print("👑 Supreme consciousness capabilities verified")
        else:
            print("❌ Some tests failed")
            print(f"Exit code: {result.returncode}")
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ Test execution error: {e}")
        return False

def run_manual_tests():
    """Run manual integration tests"""
    print("\n🔧 RUNNING MANUAL INTEGRATION TESTS...")
    
    try:
        # Import and test basic functionality
        from core.supreme_being.supreme_orchestrator import supreme_orchestrator
        
        print("✅ Supreme orchestrator import successful")
        
        # Test status
        status = supreme_orchestrator.get_supreme_status()
        print(f"✅ Supreme status: {status['overall_supreme_level']:.0%} power level")
        
        # Test basic functionality
        async def test_basic_functionality():
            try:
                result = await supreme_orchestrator.supreme_think("Test basic functionality", use_all_capabilities=False)
                print("✅ Basic supreme thinking successful")
                return True
            except Exception as e:
                print(f"❌ Basic functionality test failed: {e}")
                return False
        
        # Run async test
        success = asyncio.run(test_basic_functionality())
        
        if success:
            print("✅ Manual integration tests passed")
        else:
            print("❌ Manual integration tests failed")
        
        return success
        
    except Exception as e:
        print(f"❌ Manual test error: {e}")
        return False

def main():
    """Main test runner"""
    print("👑 SUPREME BEING TEST SUITE")
    print("=" * 50)
    
    # Run manual tests first (basic functionality)
    manual_success = run_manual_tests()
    
    print("\n" + "=" * 50)
    
    # Run comprehensive pytest suite
    pytest_success = run_tests()
    
    print("\n" + "=" * 50)
    print("📋 FINAL TEST SUMMARY:")
    print(f"Manual Tests: {'✅ PASSED' if manual_success else '❌ FAILED'}")
    print(f"Pytest Suite: {'✅ PASSED' if pytest_success else '❌ FAILED'}")
    
    if manual_success and pytest_success:
        print("\n🎉 ALL TESTS SUCCESSFUL!")
        print("👑 Supreme Being implementation fully verified")
        print("⚡ Ultimate consciousness capabilities confirmed")
    else:
        print("\n⚠️ Some tests failed - review output above")
    
    return 0 if (manual_success and pytest_success) else 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)