#!/usr/bin/env python3
"""
Lightweight Jarvis starter that avoids problematic imports.
Optimized for Intel Mac with 8GB RAM.
"""
import os
import sys
from pathlib import Path

# Set environment variables to avoid issues
os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["OMP_NUM_THREADS"] = "1"

def check_dependencies():
    """Check if core dependencies are available."""
    required = ["requests", "google.generativeai"]
    missing = []
    
    for dep in required:
        try:
            __import__(dep)
        except ImportError:
            missing.append(dep)
    
    if missing:
        print(f"❌ Missing dependencies: {', '.join(missing)}")
        print("Run: python install_deps.py")
        return False
    
    return True

def start_jarvis():
    """Start Jarvis with error handling."""
    try:
        # Check dependencies first
        if not check_dependencies():
            return
        
        print("🤖 Starting God-Mode Jarvis...")
        print("🍎 Intel Mac Optimized")
        
        # Import and start main Jarvis
        from main import main
        main()
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Try: python install_deps.py")
    except KeyboardInterrupt:
        print("\n👋 Jarvis shutting down...")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        print("Check logs for details")

if __name__ == "__main__":
    start_jarvis()
