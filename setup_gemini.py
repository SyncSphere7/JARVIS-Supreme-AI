#!/usr/bin/env python3
"""
Setup script for Gemini API integration.
"""
import os
from pathlib import Path

def setup_gemini_api():
    """Setup Gemini API key."""
    print("🔧 Setting up Gemini API for Jarvis")
    print("=" * 50)
    
    # Check if .env file exists
    env_file = Path(".env")
    
    print("To use Gemini AI with Jarvis, you need a Google AI API key.")
    print("Get your free API key at: https://makersuite.google.com/app/apikey")
    print("")
    
    api_key = input("Enter your Gemini API key (or press Enter to skip): ").strip()
    
    if not api_key:
        print("⚠️ Skipping Gemini setup. You can set it up later.")
        return False
    
    # Read existing .env file or create new one
    env_content = ""
    if env_file.exists():
        with open(env_file, 'r') as f:
            env_content = f.read()
    
    # Check if GEMINI_API_KEY already exists
    if "GEMINI_API_KEY" in env_content:
        # Replace existing key
        lines = env_content.split('\n')
        new_lines = []
        for line in lines:
            if line.startswith('GEMINI_API_KEY='):
                new_lines.append(f'GEMINI_API_KEY={api_key}')
            else:
                new_lines.append(line)
        env_content = '\n'.join(new_lines)
    else:
        # Add new key
        if env_content and not env_content.endswith('\n'):
            env_content += '\n'
        env_content += f'GEMINI_API_KEY={api_key}\n'
    
    # Write .env file
    with open(env_file, 'w') as f:
        f.write(env_content)
    
    print("✅ Gemini API key saved to .env file")
    print("🚀 Jarvis will now use Gemini AI for enhanced responses!")
    
    return True

def test_gemini_connection():
    """Test Gemini API connection."""
    print("\n🧪 Testing Gemini connection...")
    
    try:
        import google.generativeai as genai
        
        # Load API key from environment
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            print("❌ No API key found. Run setup first.")
            return False
        
        # Configure and test
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Simple test
        response = model.generate_content("Say hello and confirm you're working!")
        
        print("✅ Gemini connection successful!")
        print(f"🤖 Response: {response.text}")
        
        return True
        
    except ImportError:
        print("❌ Google AI library not installed. Run: pip install google-generativeai")
        return False
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

def main():
    """Main setup function."""
    print("🚀 Jarvis Gemini AI Setup")
    print("=" * 30)
    
    # Setup API key
    if setup_gemini_api():
        # Load environment variables
        from dotenv import load_dotenv
        load_dotenv()
        
        # Test connection
        test_gemini_connection()
    
    print("\n🎯 Next steps:")
    print("1. Run: python main.py --cli")
    print("2. Try: generate code for a calculator")
    print("3. Try: debug code [paste your code]")
    print("4. Try: analyze website https://example.com")

if __name__ == "__main__":
    main()
