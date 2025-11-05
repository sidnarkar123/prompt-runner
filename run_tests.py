#!/usr/bin/env python
"""
Quick test runner script for Streamlit Prompt Runner
"""
import sys
import subprocess


def run_tests(args=None):
    """Run pytest with specified arguments"""
    cmd = ["pytest"]
    
    if args:
        cmd.extend(args)
    else:
        # Default: run all tests with coverage
        cmd.extend([
            "-v",
            "--cov=.",
            "--cov-report=term-missing",
            "--cov-report=html"
        ])
    
    print(f"Running: {' '.join(cmd)}")
    print("=" * 60)
    
    result = subprocess.run(cmd)
    return result.returncode


def main():
    """Main entry point"""
    # Parse command line arguments
    args = sys.argv[1:]
    
    # Show help
    if "-h" in args or "--help" in args:
        print("""
Streamlit Prompt Runner - Test Runner

Usage:
    python run_tests.py              # Run all tests with coverage
    python run_tests.py -v           # Run with verbose output
    python run_tests.py -k mcp       # Run only MCP tests
    python run_tests.py --lf         # Run last failed tests
    python run_tests.py tests/test_mcp.py  # Run specific file

Examples:
    python run_tests.py -v --cov-report=html
    python run_tests.py tests/test_geometry.py -v
    python run_tests.py -k "test_calculator" -v
        """)
        return 0
    
    # Run tests
    exit_code = run_tests(args)
    
    # Summary
    print("\n" + "=" * 60)
    if exit_code == 0:
        print("✅ All tests passed!")
        print("📊 Coverage report: htmlcov/index.html")
    else:
        print("❌ Some tests failed!")
    print("=" * 60)
    
    return exit_code


if __name__ == "__main__":
    sys.exit(main())

