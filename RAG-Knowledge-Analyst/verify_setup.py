#!/usr/bin/env python3
"""
Project Verification Script - Checks if all components are properly set up
"""

import os
import sys
from pathlib import Path

def check_files():
    """Check if all required files exist"""
    required_files = [
        'app.py',
        'rag_pipeline.py',
        'utils.py',
        'requirements.txt',
        'README.md',
        '.env.example',
        '.gitignore',
        'QUICKSTART.md',
        'CONFIG.md'
    ]
    
    print("📋 Checking Files...")
    print("-" * 50)
    
    all_good = True
    for file in required_files:
        exists = os.path.exists(file)
        status = "✅" if exists else "❌"
        print(f"{status} {file}")
        if not exists:
            all_good = False
    
    return all_good

def check_directories():
    """Check if required directories exist"""
    directories = ['data', 'vectorstore']
    
    print("\n📁 Checking Directories...")
    print("-" * 50)
    
    for dir in directories:
        exists = os.path.exists(dir)
        if not exists:
            os.makedirs(dir)
        print(f"✅ {dir}/")
    
    return True

def check_python_imports():
    """Check if all required Python modules can be imported"""
    required_packages = [
        'streamlit',
        'langchain',
        'langchain_community',
        'langchain_groq',
        'pypdf',
        'faiss',
        'sentence_transformers',
        'dotenv'
    ]
    
    print("\n🐍 Checking Python Imports...")
    print("-" * 50)
    
    missing = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}")
            missing.append(package)
    
    return len(missing) == 0

def check_env_file():
    """Check if .env file exists and has API key"""
    print("\n🔐 Checking Environment Configuration...")
    print("-" * 50)
    
    if not os.path.exists('.env'):
        print("❌ .env file not found")
        print("   → Copy .env.example to .env")
        print("   → Add your GROQ_API_KEY")
        return False
    
    print("✅ .env file exists")
    
    # Check if API key is set
    with open('.env', 'r') as f:
        content = f.read()
        if 'GROQ_API_KEY=' in content and 'your_groq_api_key_here' not in content:
            print("✅ GROQ_API_KEY appears to be configured")
            return True
        else:
            print("⚠️  GROQ_API_KEY not properly configured")
            print("   → Edit .env and add your actual key")
            return False

def check_file_syntax():
    """Check Python files for syntax errors"""
    print("\n✨ Checking Python Syntax...")
    print("-" * 50)
    
    python_files = ['app.py', 'rag_pipeline.py', 'utils.py']
    all_good = True
    
    for file in python_files:
        try:
            with open(file, 'r') as f:
                compile(f.read(), file, 'exec')
            print(f"✅ {file}")
        except SyntaxError as e:
            print(f"❌ {file}: {e}")
            all_good = False
    
    return all_good

def main():
    """Run all checks"""
    print("\n" + "="*50)
    print("🔍 RAG Knowledge Analyst - Project Verification")
    print("="*50 + "\n")
    
    results = {
        'Files': check_files(),
        'Directories': check_directories(),
        'Environment': check_env_file(),
        'Syntax': check_file_syntax(),
    }
    
    print("\n🐍 Checking Python Imports...")
    print("-" * 50)
    print("⚠️  Skipping import check - install dependencies first with:")
    print("   pip install -r requirements.txt")
    
    print("\n" + "="*50)
    print("📊 Verification Summary")
    print("="*50)
    
    for check, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {check}")
    
    all_passed = all(results.values())
    
    print("\n" + "="*50)
    if all_passed:
        print("✅ All checks passed!")
        print("\nNext steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Verify GROQ_API_KEY in .env")
        print("3. Run: streamlit run app.py")
    else:
        print("⚠️  Some checks failed. Please fix the issues above.")
        print("   See README.md for troubleshooting")
    print("="*50 + "\n")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
