#!/usr/bin/env python3
"""
Test syntax of all Jarvis files.
"""
import ast
import sys
from pathlib import Path

def test_file_syntax(file_path):
    """Test syntax of a single file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        ast.parse(content)
        print(f"✅ {file_path}")
        return True
    except SyntaxError as e:
        print(f"❌ {file_path}: {e}")
        return False
    except Exception as e:
        print(f"⚠️ {file_path}: {e}")
        return False

def main():
    """Test all Python files."""
    files_to_test = [
        "main.py",
        "core/autonomous/goal_executor.py",
        "core/brain/brain.py",
        "core/modules/web_builder.py"
    ]
    
    print("🧪 Testing syntax of all files...")
    
    all_good = True
    for file_path in files_to_test:
        if Path(file_path).exists():
            if not test_file_syntax(file_path):
                all_good = False
        else:
            print(f"⚠️ File not found: {file_path}")
    
    if all_good:
        print("\n🎉 All syntax tests passed!")
        print("🚀 Try: python main.py --cli")
    else:
        print("\n❌ Some syntax errors found")
    
    return all_good

if __name__ == "__main__":
    main()
