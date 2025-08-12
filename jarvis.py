#!/usr/bin/env python3
"""
Ultimate Jarvis Launcher with Pre-Import Self-Repair.
This launcher ALWAYS fixes syntax errors before attempting to start Jarvis.
"""
import os
import sys
import subprocess
from pathlib import Path

# Set environment variables immediately
os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["PYTHONWARNINGS"] = "ignore::UserWarning"

def emergency_syntax_fix():
    """Emergency syntax fix for the most common issues."""
    print("🚨 EMERGENCY SYNTAX REPAIR...")

    # Fix the specific syntax error we know about
    goal_executor_file = Path("core/autonomous/goal_executor.py")
    if goal_executor_file.exists():
        try:
            with open(goal_executor_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Fix the specific quote issue - check for problematic quotes
            original_content = content

            # Replace smart quotes with regular quotes
            content = content.replace('"', '"').replace('"', '"')
            content = content.replace(''', "'").replace(''', "'")

            if content != original_content:
                with open(goal_executor_file, 'w', encoding='utf-8') as f:
                    f.write(content)

                print("✅ Fixed goal_executor.py syntax error")
                return True
        except Exception as e:
            print(f"❌ Emergency fix failed: {e}")

    return False

def install_missing_dependencies():
    """Install any missing dependencies."""
    print("📦 Checking dependencies...")

    required = ["requests", "psutil", "google-generativeai", "openai", "python-dotenv"]
    missing = []

    for package in required:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing.append(package)

    if missing:
        print(f"📦 Installing: {missing}")
        for package in missing:
            try:
                subprocess.run([
                    sys.executable, '-m', 'pip', 'install', package
                ], check=True, timeout=120)
                print(f"✅ Installed {package}")
            except Exception as e:
                print(f"⚠️ Could not install {package}: {e}")

def launch_jarvis():
    """Launch Jarvis with maximum error handling."""
    max_attempts = 3

    for attempt in range(max_attempts):
        try:
            print(f"🚀 LAUNCHING JARVIS (Attempt {attempt + 1}/{max_attempts})")

            # Try to import and run main
            from main import main
            main()
            return True

        except SyntaxError as e:
            print(f"🔧 SYNTAX ERROR: {e}")
            print(f"📍 File: {e.filename}, Line: {e.lineno}")

            # Try emergency fix
            if emergency_syntax_fix():
                print("🔄 Retrying after emergency fix...")
                continue
            else:
                print("❌ Could not fix syntax error")
                break

        except ImportError as e:
            print(f"🔧 IMPORT ERROR: {e}")
            install_missing_dependencies()
            print("🔄 Retrying after dependency installation...")
            continue

        except Exception as e:
            print(f"🔧 GENERAL ERROR: {type(e).__name__}: {e}")

            if attempt < max_attempts - 1:
                print("🔄 Retrying...")
                continue
            else:
                print("❌ All attempts failed")
                break

    return False

def main():
    """Main launcher function."""
    print("👑" + "=" * 50 + "👑")
    print("🔥    ULTIMATE JARVIS LAUNCHER    🔥")
    print("👑" + "=" * 50 + "👑")
    print("🔧 Self-repairing launch sequence...")
    print("")

    # Step 1: Emergency syntax fix
    emergency_syntax_fix()

    # Step 2: Install dependencies
    install_missing_dependencies()

    # Step 3: Launch Jarvis
    success = launch_jarvis()

    if success:
        print("🎉 JARVIS LAUNCHED SUCCESSFULLY!")
    else:
        print("❌ LAUNCH FAILED")
        print("🔧 Try manual fixes:")
        print("   python pre_import_fixer.py")
        print("   python install_deps.py")
        print("   python main.py --cli")

if __name__ == "__main__":
    main()