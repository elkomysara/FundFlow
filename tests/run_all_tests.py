"""
Complete Test Suite Runner
Executes all tests systematically and provides comprehensive report
"""

import subprocess
import sys
import time
import os

def run_test_script(script_name, description):
    """Run a test script and capture results"""
    print(f"\n{'='*80}")
    print(f"🧪 {description}")
    print(f"{'='*80}")
    
    script_path = os.path.join('tests', script_name)
    start_time = time.time()
    
    try:
        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        elapsed = time.time() - start_time
        
        # Print output
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        success = result.returncode == 0
        return {
            "name": description,
            "success": success,
            "time": elapsed,
            "returncode": result.returncode
        }
        
    except subprocess.TimeoutExpired:
        print("❌ Test timed out after 5 minutes")
        return {"name": description, "success": False, "time": 300, "returncode": -1}
    except Exception as e:
        print(f"❌ Test execution failed: {str(e)}")
        return {"name": description, "success": False, "time": 0, "returncode": -2}

def main():
    print("🚀 ImaraFund Complete AI Testing Suite")
    print("="*80)
    print("Systematic validation of AI prompt integration")
    print("Expected duration: 5-10 minutes")
    print("="*80)
    
    # Test suite in order of complexity
    test_suite = [
        ("test_ai_direct.py", "Direct AI Prompt Testing"),
        ("test_integration_complete.py", "Full Integration Testing"),
        ("test_gemini_unit.py", "Unit Testing Framework")
    ]
    
    results = []
    total_start = time.time()
    
    for script_name, description in test_suite:
        result = run_test_script(script_name, description)
        results.append(result)
        
        # Brief pause between test suites
        if result != results[-1]:  # Not the last test
            time.sleep(2)
    
    total_elapsed = time.time() - total_start
    
    # Generate comprehensive report
    print("\n" + "="*80)
    print("📊 FINAL AI TESTING REPORT")
    print("="*80)
    
    for result in results:
        status = "✅ PASSED" if result['success'] else "❌ FAILED"
        print(f"{status} {result['name']} ({result['time']:.1f}s)")
    
    passed = sum(1 for r in results if r['success'])
    total = len(results)
    
    print(f"\nSummary: {passed}/{total} test suites passed")
    print(f"Total execution time: {total_elapsed:.1f}s")
    
    # Provide actionable feedback
    if passed == total:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ Your AI integration is fully operational")
        print("✅ Prompts are generating quality advice")
        print("✅ System performance is acceptable")
        return 0
    elif passed >= 2:
        print("\n⚠️ MOSTLY SUCCESSFUL")
        print("✅ Core AI functionality is working")
        print("⚠️ Some tests failed - review specific issues")
        return 1
    else:
        print("\n❌ CRITICAL ISSUES DETECTED")
        print("❌ AI integration needs immediate attention")
        print("❌ Review API keys, model availability, and configuration")
        return 2

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
