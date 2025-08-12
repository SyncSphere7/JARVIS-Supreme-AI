#!/usr/bin/env python3
"""
Ultimate syntax fixer - removes all problematic characters.
"""
import re
from pathlib import Path

def fix_goal_executor():
    """Fix the goal_executor.py file completely."""
    file_path = Path("core/autonomous/goal_executor.py")
    
    if not file_path.exists():
        print("❌ File not found")
        return False
    
    try:
        # Read the file as bytes to see exactly what's there
        with open(file_path, 'rb') as f:
            content_bytes = f.read()
        
        # Decode and clean
        content = content_bytes.decode('utf-8', errors='replace')
        
        # Replace all problematic quote characters
        content = content.replace('"', '"')  # Left double quotation mark
        content = content.replace('"', '"')  # Right double quotation mark
        content = content.replace(''', "'")  # Left single quotation mark
        content = content.replace(''', "'")  # Right single quotation mark
        content = content.replace('‚', "'")  # Single low-9 quotation mark
        content = content.replace('„', '"')  # Double low-9 quotation mark
        content = content.replace('‹', "'")  # Single left-pointing angle quotation mark
        content = content.replace('›', "'")  # Single right-pointing angle quotation mark
        content = content.replace('«', '"')  # Left-pointing double angle quotation mark
        content = content.replace('»', '"')  # Right-pointing double angle quotation mark
        
        # Fix the specific problematic line
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if 'Execute plan autonomously without user intervention' in line:
                lines[i] = '        """Execute plan autonomously without user intervention."""'
                print(f"✅ Fixed line {i+1}")
                break
        
        # Write back as clean UTF-8
        content = '\n'.join(lines)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ File cleaned and saved")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

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
        return False

def main():
    """Main function."""
    print("🔧 ULTIMATE SYNTAX FIXER")
    print("=" * 30)
    
    if fix_goal_executor():
        if test_syntax():
            print("\n🎉 SUCCESS! Syntax error fixed!")
            print("🚀 Try: python main.py --cli")
        else:
            print("\n❌ Syntax still broken")
    else:
        print("\n❌ Could not fix file")

if __name__ == "__main__":
    main()
