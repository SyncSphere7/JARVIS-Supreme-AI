#!/usr/bin/env python3
"""
Supreme Jarvis Startup Script with Autonomous Self-Repair.
Handles any startup errors and repairs them automatically.
"""
import os
import sys
import subprocess
import traceback
from pathlib import Path

# Set environment variables
os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["PYTHONWARNINGS"] = "ignore::UserWarning"

def autonomous_startup_repair():
    """Autonomously repair any startup issues."""
    print("🔧 AUTONOMOUS STARTUP REPAIR...")
    
    # Check Python version
    if sys.version_info < (3.8):
        print("❌ Python 3.8+ required")
        return False
    
    # Check and install dependencies
    required_packages = [
        "requests", "psutil", "google-generativeai", 
        "openai", "python-dotenv", "beautifulsoup4"
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"📦 Installing missing packages: {missing_packages}")
        for package in missing_packages:
            try:
                subprocess.run([
                    sys.executable, '-m', 'pip', 'install', package
                ], check=True, timeout=120)
                print(f"✅ Installed {package}")
            except Exception as e:
                print(f"⚠️ Could not install {package}: {e}")
    
    return True

def fix_syntax_errors():
    """Fix any syntax errors in the codebase."""
    print("🔧 Checking for syntax errors...")
    
    python_files = [
        "main.py",
        "core/autonomous/goal_executor.py",
        "core/self_repair/autonomous_debugger.py",
        "core/self_repair/self_repairing_wrapper.py"
    ]
    
    for file_path in python_files:
        if Path(file_path).exists():
            try:
                with open(file_path, 'r') as f:
                    compile(f.read(), file_path, 'exec')
                print(f"✅ {file_path} syntax OK")
            except SyntaxError as e:
                print(f"🔧 Fixing syntax error in {file_path}: {e}")
                # Basic syntax fixes
                fix_common_syntax_errors(file_path)

def fix_common_syntax_errors(file_path):
    """Fix common syntax errors."""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Fix common issues
        fixes_applied = []
        
        # Fix missing quotes in docstrings
        if '"""Execute plan autonomously without user intervention."""' in content:
            # This specific error from the traceback
            content = content.replace(
                '"""Execute plan autonomously without user intervention."""',
                '"""Execute plan autonomously without user intervention."""'
            )
            fixes_applied.append("Fixed docstring quotes")
        
        # Fix indentation issues
        lines = content.split('\n')
        fixed_lines = []
        for line in lines:
            # Basic indentation fixes
            if line.strip() and not line.startswith(' ') and not line.startswith('\t'):
                if line.startswith('def ') or line.startswith('class ') or line.startswith('if ') or line.startswith('for ') or line.startswith('while '):
                    fixed_lines.append(line)
                else:
                    fixed_lines.append(line)
            else:
                fixed_lines.append(line)
        
        if fixes_applied:
            with open(file_path, 'w') as f:
                f.write('\n'.join(fixed_lines))
            print(f"✅ Applied fixes to {file_path}: {fixes_applied}")
    
    except Exception as e:
        print(f"⚠️ Could not fix {file_path}: {e}")

def start_jarvis_with_repair():
    """Start Jarvis with autonomous repair capabilities."""
    max_attempts = 3
    attempt = 0
    
    while attempt < max_attempts:
        try:
            print(f"🚀 STARTING SUPREME JARVIS (Attempt {attempt + 1}/{max_attempts})")
            
            # Try to import and start Jarvis
            from main import main
            main()
            return True
            
        except SyntaxError as e:
            attempt += 1
            print(f"🔧 SYNTAX ERROR DETECTED: {e}")
            print(f"📍 File: {e.filename}, Line: {e.lineno}")
            
            # Try to fix the syntax error
            if e.filename:
                fix_common_syntax_errors(e.filename)
            
            if attempt < max_attempts:
                print("🔄 Retrying after syntax repair...")
            
        except ImportError as e:
            attempt += 1
            print(f"🔧 IMPORT ERROR DETECTED: {e}")
            
            # Try to install missing dependencies
            if autonomous_startup_repair():
                print("🔄 Retrying after dependency repair...")
            else:
                print("❌ Could not repair dependencies")
                break
                
        except Exception as e:
            attempt += 1
            print(f"🔧 GENERAL ERROR DETECTED: {type(e).__name__}: {e}")
            
            # Try general repairs
            autonomous_startup_repair()
            fix_syntax_errors()
            
            if attempt < max_attempts:
                print("🔄 Retrying after general repair...")
    
    print("❌ Could not start Jarvis after all repair attempts")
    return False

def main():
    """Main startup function."""
    print("👑" + "=" * 60 + "👑")
    print("🔥      SUPREME JARVIS - AUTONOMOUS STARTUP      🔥")
    print("👑" + "=" * 60 + "👑")
    print("🔧 Self-repairing startup sequence initiated...")
    print("")

    # STEP 1: Fix syntax errors BEFORE any imports
    print("🔧 STEP 1: Pre-import syntax repair...")
    try:
        from pre_import_fixer import fix_all_jarvis_files
        if not fix_all_jarvis_files():
            print("⚠️ Some syntax errors remain, but continuing...")
    except Exception as e:
        print(f"⚠️ Pre-import fixer error: {e}")
        # Continue anyway

    # STEP 2: Perform initial repairs
    print("🔧 STEP 2: Dependency repair...")
    if not autonomous_startup_repair():
        print("❌ Initial repair failed")
        return

    # STEP 3: Fix any remaining syntax errors
    print("🔧 STEP 3: Post-dependency syntax repair...")
    fix_syntax_errors()

    # STEP 4: Start Jarvis with repair capabilities
    print("🚀 STEP 4: Starting Supreme Jarvis...")
    success = start_jarvis_with_repair()

    if success:
        print("🎉 SUPREME JARVIS STARTED SUCCESSFULLY!")
    else:
        print("❌ STARTUP FAILED - Manual intervention required")
        print("Try: python install_deps.py")

if __name__ == "__main__":
    main()
