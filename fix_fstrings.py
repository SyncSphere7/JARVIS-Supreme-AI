#!/usr/bin/env python3
"""
Fix all problematic f-strings in goal_executor.py
"""
import re
from pathlib import Path

def fix_multiline_fstrings():
    """Fix all multiline f-strings in goal_executor.py"""
    file_path = Path("core/autonomous/goal_executor.py")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace all multiline f-strings with single line versions
    # Pattern: f"""...""" (multiline)
    
    # Fix pattern 1: f"""...""" spanning multiple lines
    def replace_multiline_fstring(match):
        fstring_content = match.group(1)
        # Replace newlines with \n and quotes with proper escaping
        fixed_content = fstring_content.replace('\n', '\\n').replace('"', '\\"')
        return f'f"{fixed_content}"'
    
    # Find and replace multiline f-strings
    pattern = r'f"""(.*?)"""'
    content = re.sub(pattern, replace_multiline_fstring, content, flags=re.DOTALL)
    
    # Also fix any remaining triple quotes in f-strings
    content = re.sub(r'f"""([^"]*?)"""', r'f"\1"', content)
    
    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Fixed all multiline f-strings")

def test_syntax():
    """Test if syntax is now correct."""
    try:
        import ast
        with open("core/autonomous/goal_executor.py", 'r') as f:
            content = f.read()
        
        ast.parse(content)
        print("✅ Syntax is now correct!")
        return True
        
    except SyntaxError as e:
        print(f"❌ Syntax still broken: {e}")
        print(f"Line {e.lineno}: {e.text}")
        return False

def main():
    """Main function."""
    print("🔧 FIXING ALL F-STRINGS")
    print("=" * 30)
    
    fix_multiline_fstrings()
    
    if test_syntax():
        print("\n🎉 SUCCESS! All f-string errors fixed!")
        print("🚀 Try: python main.py --cli")
    else:
        print("\n❌ Some syntax errors remain")

if __name__ == "__main__":
    main()
