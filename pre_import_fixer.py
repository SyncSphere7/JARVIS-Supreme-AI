#!/usr/bin/env python3
"""
Pre-Import Syntax Fixer for Jarvis.
Fixes syntax errors BEFORE imports happen.
"""
import ast
import re
import sys
from pathlib import Path


def fix_syntax_errors_in_file(file_path: str) -> bool:
    """Fix syntax errors in a specific file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Try to parse the file
        try:
            ast.parse(content)
            return True  # No syntax errors
        except SyntaxError as e:
            print(f"🔧 Fixing syntax error in {file_path}: {e}")
            
            # Apply common fixes
            fixed_content = apply_common_syntax_fixes(content, e)
            
            # Test if fix worked
            try:
                ast.parse(fixed_content)
                # Write the fixed content
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(fixed_content)
                print(f"✅ Fixed syntax error in {file_path}")
                return True
            except SyntaxError:
                print(f"❌ Could not fix syntax error in {file_path}")
                return False
                
    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")
        return False


def apply_common_syntax_fixes(content: str, error: SyntaxError) -> str:
    """Apply common syntax fixes."""
    lines = content.split('\n')
    
    if error.lineno and error.lineno <= len(lines):
        line_idx = error.lineno - 1
        problematic_line = lines[line_idx]
        
        # Fix common quote issues
        if 'invalid syntax' in str(error) and '"""' in problematic_line:
            # Fix smart quotes or encoding issues
            fixed_line = problematic_line.replace('"', '"').replace('"', '"')
            fixed_line = fixed_line.replace(''', "'").replace(''', "'")
            lines[line_idx] = fixed_line
            
        # Fix indentation issues
        elif 'IndentationError' in str(error) or 'unexpected indent' in str(error):
            # Fix indentation
            if line_idx > 0:
                prev_line = lines[line_idx - 1]
                if prev_line.strip().endswith(':'):
                    # Should be indented
                    lines[line_idx] = '    ' + problematic_line.lstrip()
                else:
                    # Should match previous line indentation
                    prev_indent = len(prev_line) - len(prev_line.lstrip())
                    lines[line_idx] = ' ' * prev_indent + problematic_line.lstrip()
        
        # Fix missing colons
        elif 'invalid syntax' in str(error) and any(keyword in problematic_line for keyword in ['def ', 'class ', 'if ', 'for ', 'while ', 'try', 'except', 'else', 'elif']):
            if not problematic_line.rstrip().endswith(':'):
                lines[line_idx] = problematic_line.rstrip() + ':'
        
        # Fix unclosed parentheses/brackets
        elif 'EOF while scanning' in str(error) or 'unexpected EOF' in str(error):
            # Count unclosed brackets
            open_parens = content.count('(') - content.count(')')
            open_brackets = content.count('[') - content.count(']')
            open_braces = content.count('{') - content.count('}')
            
            if open_parens > 0:
                lines.append(')' * open_parens)
            if open_brackets > 0:
                lines.append(']' * open_brackets)
            if open_braces > 0:
                lines.append('}' * open_braces)
    
    return '\n'.join(lines)


def fix_all_jarvis_files() -> bool:
    """Fix syntax errors in all Jarvis Python files."""
    jarvis_files = [
        'main.py',
        'core/brain/brain.py',
        'core/autonomous/goal_executor.py',
        'core/modules/web_builder.py',
        'core/modules/ui_designer.py',
        'core/modules/system_access.py',
        'core/modules/internet_access.py',
        'core/modules/coding_assistant.py',
        'core/memory/persistent_memory.py',
        'core/automation/system_control.py',
        'core/self_healing/auto_updater.py',
        'core/supreme/omnipotent_executor.py',
        'core/supreme/unlimited_memory.py',
        'core/supreme/unlimited_internet.py',
        'core/self_repair/autonomous_debugger.py',
        'core/self_repair/self_repairing_wrapper.py'
    ]
    
    all_fixed = True
    
    for file_path in jarvis_files:
        if Path(file_path).exists():
            if not fix_syntax_errors_in_file(file_path):
                all_fixed = False
        else:
            print(f"⚠️ File not found: {file_path}")
    
    return all_fixed


def main():
    """Main function to fix all syntax errors."""
    print("🔧 PRE-IMPORT SYNTAX FIXER")
    print("=" * 40)
    
    if fix_all_jarvis_files():
        print("✅ All syntax errors fixed!")
        print("🚀 Ready to start Jarvis")
        return True
    else:
        print("❌ Some syntax errors could not be fixed")
        return False


if __name__ == "__main__":
    success = main()
    if success:
        print("\nTry: python main.py --cli")
    else:
        print("\nManual intervention required")
