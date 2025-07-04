#!/usr/bin/env python3
"""
Security Check Script for CIDion AI

This script helps verify that your installation is secure and API keys are protected.
"""

import os
import sys
from pathlib import Path

def check_gitignore():
    """Check if .gitignore exists and contains important exclusions."""
    gitignore_path = Path('.gitignore')
    
    if not gitignore_path.exists():
        return False, "❌ No .gitignore file found"
    
    with open(gitignore_path, 'r') as f:
        content = f.read()
    
    required_patterns = ['.env', '__pycache__/', '*.log']
    missing = [pattern for pattern in required_patterns if pattern not in content]
    
    if missing:
        return False, f"❌ .gitignore missing patterns: {', '.join(missing)}"
    
    return True, "✅ .gitignore properly configured"

def check_env_files():
    """Check .env and .env.example setup."""
    env_path = Path('.env')
    env_example_path = Path('.env.example')
    
    issues = []
    
    if not env_example_path.exists():
        issues.append("❌ No .env.example file found")
    
    if not env_path.exists():
        issues.append("⚠️  No .env file found - you need to create one")
    else:
        # Check if .env is tracked by git
        try:
            import subprocess
            result = subprocess.run(['git', 'ls-files', '.env'], 
                                  capture_output=True, text=True)
            if result.stdout.strip():
                issues.append("🚨 CRITICAL: .env file is tracked by git!")
        except:
            pass  # Git not available or not a git repo
    
    if not issues:
        return True, "✅ Environment files properly configured"
    else:
        return False, '\n'.join(issues)

def check_api_key():
    """Check if API key is configured."""
    api_key = os.environ.get('GEMINI_API_KEY')
    
    if not api_key:
        # Try loading from .env file
        env_path = Path('.env')
        if env_path.exists():
            with open(env_path, 'r') as f:
                for line in f:
                    if line.startswith('GEMINI_API_KEY='):
                        api_key = line.split('=', 1)[1].strip()
                        break
    
    if not api_key or api_key == 'your_gemini_api_key_here':
        return False, "❌ GEMINI_API_KEY not configured"
    
    if len(api_key) < 20:
        return False, "❌ GEMINI_API_KEY appears invalid (too short)"
    
    return True, "✅ GEMINI_API_KEY configured"

def main():
    """Run all security checks."""
    print("🔒 CIDion AI Security Check")
    print("=" * 40)
    
    checks = [
        ("Git Ignore", check_gitignore),
        ("Environment Files", check_env_files),
        ("API Key", check_api_key),
    ]
    
    all_passed = True
    
    for name, check_func in checks:
        try:
            passed, message = check_func()
            print(f"\n{name}:")
            print(f"  {message}")
            if not passed:
                all_passed = False
        except Exception as e:
            print(f"\n{name}:")
            print(f"  ❌ Error during check: {e}")
            all_passed = False
    
    print("\n" + "=" * 40)
    if all_passed:
        print("🎉 All security checks passed!")
        print("Your CIDion AI installation appears secure.")
    else:
        print("⚠️  Some security issues detected.")
        print("Please review the issues above and fix them.")
        print("See SECURITY.md for detailed guidance.")
    
    print("\n📚 For more information:")
    print("  - README.md - Setup instructions")
    print("  - SECURITY.md - Security guidelines")
    print("  - DEPLOY.md - Deployment guide")
    
    return 0 if all_passed else 1

if __name__ == '__main__':
    sys.exit(main())
