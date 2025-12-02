#!/usr/bin/env python3
"""
Test Runner utama untuk menjalankan semua unit tests
Memenuhi kompetensi J.620100.033.02
"""
import unittest
import sys
import os
from datetime import datetime

def run_all_tests():
    """Jalankan semua test suites"""
    
    print("=" * 70)
    print("UNIT TESTING SYSTEM - RESTORAN PEMESANAN APP")
    print(f"Test Execution Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    # Discover semua test
    test_loader = unittest.TestLoader()
    
    # Test suites
    test_suites = [
        test_loader.loadTestsFromName('tests.test_model'),
        test_loader.loadTestsFromName('tests.test_database'),
        test_loader.loadTestsFromName('tests.test_integration'),
    ]
    
    # Combine semua suites
    complete_suite = unittest.TestSuite(test_suites)
    
    # Test runner dengan report detail
    test_runner = unittest.TextTestRunner(
        verbosity=2,
        failfast=False,  # Jangan berhenti di test pertama yang gagal
        buffer=True      # Capture output selama test
    )
    
    # Jalankan tests
    print("\n" + "="*70)
    print("EXECUTING TESTS...")
    print("="*70 + "\n")
    
    result = test_runner.run(complete_suite)
    
    # Print summary
    print("\n" + "="*70)
    print("TEST EXECUTION SUMMARY")
    print("="*70)
    print(f"Total Tests Run   : {result.testsRun}")
    print(f"Tests Passed      : {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Tests Failed      : {len(result.failures)}")
    print(f"Tests with Errors : {len(result.errors)}")
    print(f"Success Rate      : {(result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100:.1f}%")
    
    # Print failures jika ada
    if result.failures:
        print("\n" + "="*70)
        print("FAILED TESTS:")
        print("="*70)
        for test, traceback in result.failures:
            print(f"\n❌ {test}")
            print("-" * 50)
            print(traceback)
    
    # Print errors jika ada
    if result.errors:
        print("\n" + "="*70)
        print("TESTS WITH ERRORS:")
        print("="*70)
        for test, traceback in result.errors:
            print(f"\n⚠️ {test}")
            print("-" * 50)
            print(traceback)
    
    # Return exit code
    return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    # Add current directory to Python path
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    # Run tests
    exit_code = run_all_tests()
    
    print("\n" + "="*70)
    if exit_code == 0:
        print("🎉 ALL TESTS PASSED SUCCESSFULLY!")
    else:
        print("❌ SOME TESTS FAILED!")
    print("="*70)
    
    sys.exit(exit_code)