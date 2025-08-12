#!/usr/bin/env python3
"""
Intelligent dependency installer for Jarvis.
Optimized for Intel Mac - avoids problematic packages.
"""
import subprocess
import sys
import os

def run_cmd(cmd, description=""):
    """Run command with better error handling."""
    print(f"📦 {description or cmd}")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True, timeout=120)
        print(f"✅ Success")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed: {e.stderr}")
        return False
    except subprocess.TimeoutExpired:
        print(f"⏱️ Timeout")
        return False

def main():
    print("🤖 JARVIS OPTIMIZED INSTALLER")
    print("=" * 40)
    print("🍎 Intel Mac Optimized - Avoiding Heavy Dependencies")

    # LIGHTWEIGHT CORE DEPENDENCIES ONLY
    deps = [
        ("pip install --upgrade pip", "Upgrading pip"),
        ("pip install psutil", "System monitoring"),
        ("pip install google-generativeai", "Gemini API (Primary)"),
        ("pip install openai", "OpenAI API (Fallback)"),
        ("pip install requests", "HTTP requests"),
        ("pip install python-dotenv", "Environment variables"),
        ("pip install beautifulsoup4", "Web scraping"),
        ("pip install lxml", "XML parsing"),
    ]

    # OPTIONAL AUDIO (Skip if problematic)
    optional_deps = [
        ("pip install SpeechRecognition", "Voice recognition"),
        ("pip install pyttsx3", "Text-to-speech"),
    ]

    print("\n📦 Installing Core Dependencies...")
    failed_core = []
    for cmd, desc in deps:
        if not run_cmd(cmd, desc):
            failed_core.append(desc)

    print("\n🔧 Installing Optional Dependencies...")
    failed_optional = []
    for cmd, desc in optional_deps:
        if not run_cmd(cmd, desc):
            failed_optional.append(desc)

    # AVOID THESE HEAVY PACKAGES
    print("\n🚫 Avoiding Heavy Dependencies:")
    avoid_packages = ["torch", "tensorflow", "transformers", "numpy", "whisper"]
    for pkg in avoid_packages:
        print(f"❌ Skipping {pkg} (causes issues on Intel Mac)")

    # SUMMARY
    print("\n" + "=" * 40)
    if not failed_core:
        print("🎉 CORE INSTALLATION SUCCESSFUL!")
    else:
        print(f"⚠️ Core failures: {', '.join(failed_core)}")

    if failed_optional:
        print(f"⚠️ Optional failures: {', '.join(failed_optional)}")

    print("\n📋 Next Steps:")
    print("1. Add API keys to .env file")
    print("2. Test: python main.py --cli")
    print("3. If issues persist, restart terminal")

    print("\n🚀 Ready for God-Mode Jarvis!")

if __name__ == "__main__":
    main()
