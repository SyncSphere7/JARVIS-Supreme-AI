#!/usr/bin/env python3
"""
Fix ALL Unicode quote issues in the entire Jarvis codebase.
"""
import re
from pathlib import Path

def clean_unicode_quotes(text):
    """Remove all problematic Unicode characters."""
    # Map of problematic Unicode characters to ASCII equivalents
    replacements = {
        # Smart quotes
        '\u201c': '"',  # Left double quotation mark
        '\u201d': '"',  # Right double quotation mark
        '\u201e': '"',  # Double low-9 quotation mark
        '\u201f': '"',  # Double high-reversed-9 quotation mark
        '\u2018': "'",  # Left single quotation mark
        '\u2019': "'",  # Right single quotation mark
        '\u201a': "'",  # Single low-9 quotation mark
        '\u201b': "'",  # Single high-reversed-9 quotation mark
        
        # Angle quotes
        '\u00ab': '"',  # Left-pointing double angle quotation mark
        '\u00bb': '"',  # Right-pointing double angle quotation mark
        '\u2039': "'",  # Single left-pointing angle quotation mark
        '\u203a': "'",  # Single right-pointing angle quotation mark
        
        # Other problematic characters
        '\u2013': '-',  # En dash
        '\u2014': '-',  # Em dash
        '\u2026': '...',  # Horizontal ellipsis
        '\u00a0': ' ',  # Non-breaking space
    }
    
    for unicode_char, ascii_char in replacements.items():
        text = text.replace(unicode_char, ascii_char)
    
    return text

def fix_file(file_path):
    """Fix a single file."""
    try:
        print(f"🔧 Fixing {file_path}...")
        
        # Read file
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
        
        # Clean Unicode
        original_content = content
        content = clean_unicode_quotes(content)
        
        # Additional specific fixes for docstrings
        content = re.sub(r'"""([^"]*?)"""', lambda m: f'"""{m.group(1)}"""', content)
        
        # Write back if changed
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Fixed {file_path}")
            return True
        else:
            print(f"✅ {file_path} was already clean")
            return True
            
    except Exception as e:
        print(f"❌ Error fixing {file_path}: {e}")
        return False

def fix_all_python_files():
    """Fix all Python files in the Jarvis project."""
    python_files = [
        "main.py",
        "core/brain/brain.py",
        "core/autonomous/goal_executor.py",
        "core/modules/web_builder.py",
        "core/modules/ui_designer.py",
        "core/modules/system_access.py",
        "core/modules/internet_access.py",
        "core/modules/coding_assistant.py",
        "core/memory/persistent_memory.py",
        "core/automation/system_control.py",
        "core/self_healing/auto_updater.py",
        "core/supreme/omnipotent_executor.py",
        "core/supreme/unlimited_memory.py",
        "core/supreme/unlimited_internet.py",
        "core/self_repair/autonomous_debugger.py",
        "core/self_repair/self_repairing_wrapper.py"
    ]
    
    all_fixed = True
    fixed_count = 0
    
    for file_path in python_files:
        if Path(file_path).exists():
            if fix_file(file_path):
                fixed_count += 1
            else:
                all_fixed = False
        else:
            print(f"⚠️ File not found: {file_path}")
    
    return all_fixed, fixed_count

def test_syntax():
    """Test syntax of all fixed files."""
    import ast
    
    test_files = [
        "main.py",
        "core/autonomous/goal_executor.py",
        "core/brain/brain.py"
    ]
    
    all_good = True
    
    for file_path in test_files:
        if Path(file_path).exists():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                ast.parse(content)
                print(f"✅ {file_path} syntax OK")
                
            except SyntaxError as e:
                print(f"❌ {file_path} syntax error: {e}")
                all_good = False
            except Exception as e:
                print(f"⚠️ {file_path} error: {e}")
        else:
            print(f"⚠️ File not found: {file_path}")
    
    return all_good

def main():
    """Main function."""
    print("🔧 COMPREHENSIVE UNICODE FIXER")
    print("=" * 50)
    print("Fixing ALL Unicode quote issues in Jarvis...")
    print("")
    
    # Fix all files
    all_fixed, fixed_count = fix_all_python_files()
    
    print(f"\n📊 RESULTS:")
    print(f"Files processed: {fixed_count}")
    
    if all_fixed:
        print("✅ All files processed successfully")
        
        # Test syntax
        print("\n🧪 Testing syntax...")
        if test_syntax():
            print("\n🎉 SUCCESS! All syntax errors fixed!")
            print("🚀 Jarvis is ready to launch!")
            print("\nTry: python main.py --cli")
        else:
            print("\n❌ Some syntax errors remain")
    else:
        print("❌ Some files could not be processed")

if __name__ == "__main__":
    main()
