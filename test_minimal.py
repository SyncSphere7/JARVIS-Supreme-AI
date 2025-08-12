#!/usr/bin/env python3
"""
Minimal test to identify dependency issues.
"""
import sys
import os

print("🧪 Testing Jarvis Dependencies...")
print(f"Python: {sys.version}")
print(f"Platform: {sys.platform}")

# Test core imports
tests = [
    ("os", "Built-in OS module"),
    ("sys", "Built-in sys module"),
    ("pathlib", "Path handling"),
    ("json", "JSON handling"),
    ("sqlite3", "Database"),
    ("subprocess", "Process management"),
    ("requests", "HTTP requests"),
    ("psutil", "System monitoring"),
    ("google.generativeai", "Gemini API"),
    ("openai", "OpenAI API"),
]

passed = 0
failed = 0

for module, description in tests:
    try:
        __import__(module)
        print(f"✅ {description}")
        passed += 1
    except ImportError as e:
        print(f"❌ {description}: {e}")
        failed += 1

print(f"\n📊 Results: {passed} passed, {failed} failed")

if failed == 0:
    print("🎉 All dependencies available!")
    print("Try: python main.py --cli")
else:
    print("⚠️ Some dependencies missing")
    print("Install with: pip install psutil google-generativeai openai requests")

# Test basic functionality
try:
    print("\n🧠 Testing Brain module...")
    from core.brain.brain import Brain
    brain = Brain()
    print("✅ Brain module works!")
except Exception as e:
    print(f"❌ Brain module failed: {e}")

print("\n🏁 Test complete!")
