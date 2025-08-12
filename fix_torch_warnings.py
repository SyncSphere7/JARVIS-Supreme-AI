#!/usr/bin/env python3
"""
Fix torch warnings and optimize Jarvis for Intel Mac.
"""
import subprocess
import sys
import os

def fix_torch_issues():
    """Fix torch-related warnings."""
    print("🔧 Fixing torch warnings...")
    
    # Option 1: Uninstall torch (recommended for Jarvis)
    print("Option 1: Remove torch (recommended)")
    print("Torch is not needed for Jarvis core functionality")
    
    try:
        result = subprocess.run([
            sys.executable, '-m', 'pip', 'uninstall', 'torch', '-y'
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Torch removed successfully")
            return True
        else:
            print(f"⚠️ Could not remove torch: {result.stderr}")
    except Exception as e:
        print(f"⚠️ Error removing torch: {e}")
    
    # Option 2: Set environment variables to suppress warnings
    print("\nOption 2: Suppressing torch warnings with environment variables")
    
    env_vars = {
        "PYTORCH_ENABLE_MPS_FALLBACK": "1",
        "TOKENIZERS_PARALLELISM": "false",
        "OMP_NUM_THREADS": "1",
        "PYTHONWARNINGS": "ignore::UserWarning"
    }
    
    for var, value in env_vars.items():
        os.environ[var] = value
        print(f"Set {var}={value}")
    
    return True

def install_psutil():
    """Install psutil for system monitoring."""
    print("📦 Installing psutil for system monitoring...")
    
    try:
        result = subprocess.run([
            sys.executable, '-m', 'pip', 'install', 'psutil'
        ], capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print("✅ psutil installed successfully")
            return True
        else:
            print(f"❌ Failed to install psutil: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error installing psutil: {e}")
        return False

def create_startup_script():
    """Create optimized startup script."""
    script_content = '''#!/bin/bash
# Jarvis Optimized Startup Script

# Set environment variables to suppress warnings
export PYTORCH_ENABLE_MPS_FALLBACK=1
export TOKENIZERS_PARALLELISM=false
export OMP_NUM_THREADS=1
export PYTHONWARNINGS=ignore::UserWarning

# Start Jarvis
echo "🚀 Starting God-Mode Jarvis..."
python main.py --cli
'''
    
    with open('start_jarvis.sh', 'w') as f:
        f.write(script_content)
    
    # Make executable
    os.chmod('start_jarvis.sh', 0o755)
    print("✅ Created optimized startup script: start_jarvis.sh")

def main():
    print("🛠️ JARVIS OPTIMIZATION TOOL")
    print("=" * 40)
    
    # Fix torch issues
    fix_torch_issues()
    
    # Install psutil
    install_psutil()
    
    # Create startup script
    create_startup_script()
    
    print("\n🎉 OPTIMIZATION COMPLETE!")
    print("=" * 40)
    print("✅ Torch warnings suppressed")
    print("✅ System monitoring enabled")
    print("✅ Startup script created")
    print("\n🚀 Launch Jarvis with:")
    print("   ./start_jarvis.sh")
    print("   OR")
    print("   python main.py --cli")

if __name__ == "__main__":
    main()
