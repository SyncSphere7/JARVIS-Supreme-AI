#!/usr/bin/env python3
"""
Install advanced dependencies for Jarvis ML and Web Automation capabilities.
"""
import subprocess
import sys
import os
from pathlib import Path

def install_package(package):
    """Install a package using pip."""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ Installed {package}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install {package}: {e}")
        return False

def install_ml_dependencies():
    """Install machine learning dependencies."""
    print("📊 Installing Machine Learning Dependencies...")
    
    ml_packages = [
        "scikit-learn>=1.3.0",
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "matplotlib>=3.7.0",
        "seaborn>=0.12.0",
        "joblib>=1.3.0",
        "torch>=2.0.0",
        "tensorflow>=2.13.0",
        "transformers>=4.30.0",
        "datasets>=2.14.0",
        "accelerate>=0.20.0"
    ]
    
    success_count = 0
    for package in ml_packages:
        if install_package(package):
            success_count += 1
    
    print(f"📊 ML Dependencies: {success_count}/{len(ml_packages)} installed successfully")
    return success_count == len(ml_packages)

def install_web_automation_dependencies():
    """Install web automation dependencies."""
    print("🌐 Installing Web Automation Dependencies...")
    
    web_packages = [
        "selenium>=4.15.0",
        "undetected-chromedriver>=3.5.0",
        "beautifulsoup4>=4.12.0",
        "requests>=2.31.0",
        "aiohttp>=3.8.0",
        "playwright>=1.40.0",
        "pyautogui>=0.9.54",
        "opencv-python>=4.8.0",
        "pillow>=10.0.0",
        "pytesseract>=0.3.10"
    ]
    
    success_count = 0
    for package in web_packages:
        if install_package(package):
            success_count += 1
    
    print(f"🌐 Web Automation Dependencies: {success_count}/{len(web_packages)} installed successfully")
    
    # Install Playwright browsers
    try:
        print("🎭 Installing Playwright browsers...")
        subprocess.check_call([sys.executable, "-m", "playwright", "install"])
        print("✅ Playwright browsers installed")
    except:
        print("⚠️ Playwright browser installation failed (optional)")
    
    return success_count >= len(web_packages) * 0.8  # 80% success rate

def install_additional_dependencies():
    """Install additional useful dependencies."""
    print("🔧 Installing Additional Dependencies...")
    
    additional_packages = [
        "psutil>=5.9.0",
        "python-dotenv>=1.0.0",
        "cryptography>=41.0.0",
        "paramiko>=3.3.0",
        "schedule>=1.2.0",
        "watchdog>=3.0.0",
        "rich>=13.5.0",
        "typer>=0.9.0",
        "fastapi>=0.103.0",
        "uvicorn>=0.23.0",
        # Output formatting dependencies
        "reportlab>=4.0.0",
        "python-docx>=0.8.11",
        "openpyxl>=3.1.0",
        "pdfkit>=1.0.0",
        "weasyprint>=60.0"
    ]
    
    success_count = 0
    for package in additional_packages:
        if install_package(package):
            success_count += 1
    
    print(f"🔧 Additional Dependencies: {success_count}/{len(additional_packages)} installed successfully")
    return success_count >= len(additional_packages) * 0.8

def setup_chrome_driver():
    """Setup Chrome driver for web automation."""
    try:
        print("🚗 Setting up Chrome driver...")
        
        # Check if Chrome is installed
        chrome_paths = [
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",  # macOS
            "/usr/bin/google-chrome",  # Linux
            "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"  # Windows
        ]
        
        chrome_found = False
        for path in chrome_paths:
            if os.path.exists(path):
                chrome_found = True
                break
        
        if not chrome_found:
            print("⚠️ Google Chrome not found. Please install Chrome for web automation.")
            return False
        
        # Test undetected-chromedriver
        try:
            import undetected_chromedriver as uc
            driver = uc.Chrome(headless=True)
            driver.quit()
            print("✅ Chrome driver setup successful")
            return True
        except Exception as e:
            print(f"⚠️ Chrome driver test failed: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Chrome driver setup failed: {e}")
        return False

def create_ml_directories():
    """Create necessary directories for ML models."""
    try:
        directories = [
            "ml_models",
            "datasets",
            "logs",
            "temp",
            "cache"
        ]
        
        for directory in directories:
            Path(directory).mkdir(exist_ok=True)
            print(f"📁 Created directory: {directory}")
        
        return True
    except Exception as e:
        print(f"❌ Failed to create directories: {e}")
        return False

def test_installations():
    """Test if installations were successful."""
    print("\n🧪 Testing Installations...")
    
    tests = {
        "Machine Learning": [
            "import sklearn",
            "import pandas",
            "import numpy",
            "import torch",
            "import tensorflow"
        ],
        "Web Automation": [
            "import selenium",
            "import undetected_chromedriver",
            "import requests",
            "from bs4 import BeautifulSoup"
        ],
        "Additional": [
            "import psutil",
            "from dotenv import load_dotenv",
            "import cryptography"
        ]
    }
    
    results = {}
    
    for category, imports in tests.items():
        success_count = 0
        for import_test in imports:
            try:
                exec(import_test)
                success_count += 1
            except ImportError:
                pass
        
        results[category] = f"{success_count}/{len(imports)}"
        print(f"✅ {category}: {results[category]} imports successful")
    
    return results

def main():
    """Main installation function."""
    print("🚀" + "=" * 60 + "🚀")
    print("🔥    JARVIS ADVANCED CAPABILITIES INSTALLER    🔥")
    print("🚀" + "=" * 60 + "🚀")
    print("")
    
    # Check Python version
    if sys.version_info < (3.8):
        print("❌ Python 3.8+ required")
        return False
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Install dependencies
    ml_success = install_ml_dependencies()
    web_success = install_web_automation_dependencies()
    additional_success = install_additional_dependencies()
    
    # Setup Chrome driver
    chrome_success = setup_chrome_driver()
    
    # Create directories
    dir_success = create_ml_directories()
    
    # Test installations
    test_results = test_installations()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 INSTALLATION SUMMARY:")
    print("=" * 60)
    print(f"🤖 Machine Learning: {'✅' if ml_success else '❌'}")
    print(f"🌐 Web Automation: {'✅' if web_success else '❌'}")
    print(f"🔧 Additional Tools: {'✅' if additional_success else '❌'}")
    print(f"🚗 Chrome Driver: {'✅' if chrome_success else '❌'}")
    print(f"📁 Directories: {'✅' if dir_success else '❌'}")
    
    print("\n📋 Test Results:")
    for category, result in test_results.items():
        print(f"   {category}: {result}")
    
    overall_success = ml_success and web_success and additional_success
    
    if overall_success:
        print("\n🎉 INSTALLATION COMPLETE!")
        print("🚀 Jarvis now has advanced ML and Web Automation capabilities!")
        print("\nTry these commands:")
        print("   python main.py --cli")
        print("   > automl")
        print("   > create api account")
        print("   > shop online")
    else:
        print("\n⚠️ INSTALLATION PARTIALLY COMPLETE")
        print("Some dependencies failed to install. Jarvis will work with reduced functionality.")
        print("Try running: pip install --upgrade pip")
        print("Then re-run this installer.")
    
    return overall_success

if __name__ == "__main__":
    main()
