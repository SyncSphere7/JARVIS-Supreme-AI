#!/usr/bin/env python3
"""
Setup script for the Supreme Autonomous Coding Agent.
Installs dependencies and configures the system for maximum performance.
"""
import os
import subprocess
import sys
from pathlib import Path

def install_dependencies():
    """Install all required dependencies for the Supreme Coding Agent."""
    
    print("🚀 Installing Supreme Coding Agent Dependencies")
    print("=" * 60)
    
    # Core dependencies
    core_deps = [
        "google-generativeai>=0.8.0",  # Gemini AI
        "openai>=1.0.0",               # OpenAI API
        "aiohttp>=3.9.0",              # Async HTTP
        "asyncio",                     # Async support
        "beautifulsoup4>=4.12.0",      # Web scraping
        "requests>=2.31.0",            # HTTP requests
        "pandas>=2.0.0",               # Data processing
        "numpy>=1.24.0",               # Numerical computing
        "pydantic>=2.5.0",             # Data validation
        "fastapi>=0.104.0",            # API framework
        "uvicorn>=0.24.0",             # ASGI server
        "sqlalchemy>=2.0.0",           # Database ORM
        "alembic>=1.13.0",             # Database migrations
        "python-multipart>=0.0.6",     # File uploads
        "python-jose[cryptography]>=3.3.0",  # JWT tokens
        "passlib[bcrypt]>=1.7.4",      # Password hashing
        "python-dotenv>=1.0.0",        # Environment variables
    ]
    
    # Code quality and formatting
    quality_deps = [
        "black>=23.0.0",               # Code formatting
        "autopep8>=2.0.0",             # PEP8 formatting
        "pylint>=3.0.0",               # Code linting
        "mypy>=1.7.0",                 # Type checking
        "isort>=5.12.0",               # Import sorting
    ]
    
    # Testing dependencies
    testing_deps = [
        "pytest>=7.4.0",              # Testing framework
        "pytest-asyncio>=0.21.0",     # Async testing
        "pytest-cov>=4.1.0",          # Coverage reporting
        "httpx>=0.25.0",               # Async HTTP client for testing
    ]
    
    # Development tools
    dev_deps = [
        "jupyter>=1.0.0",             # Notebooks
        "ipython>=8.17.0",            # Interactive Python
        "rich>=13.7.0",               # Rich terminal output
        "typer>=0.9.0",               # CLI framework
    ]
    
    # Optional advanced dependencies
    advanced_deps = [
        "selenium>=4.15.0",           # Web automation
        "playwright>=1.40.0",        # Modern web automation
        "docker>=6.1.0",             # Docker integration
        "kubernetes>=28.1.0",        # Kubernetes integration
        "redis>=5.0.0",              # Redis client
        "celery>=5.3.0",             # Task queue
        "flower>=2.0.0",             # Celery monitoring
    ]
    
    all_deps = core_deps + quality_deps + testing_deps + dev_deps
    
    print("📦 Installing core dependencies...")
    for dep in core_deps:
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", dep], 
                         check=True, capture_output=True)
            print(f"✅ {dep}")
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install {dep}")
    
    print("\n🔧 Installing development tools...")
    for dep in quality_deps + testing_deps + dev_deps:
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", dep], 
                         check=True, capture_output=True)
            print(f"✅ {dep}")
        except subprocess.CalledProcessError:
            print(f"⚠️ Optional: {dep} (failed)")
    
    print("\n🚀 Installing advanced dependencies (optional)...")
    for dep in advanced_deps:
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", dep], 
                         check=True, capture_output=True)
            print(f"✅ {dep}")
        except subprocess.CalledProcessError:
            print(f"⚠️ Optional: {dep} (failed)")

def setup_environment():
    """Setup environment configuration."""
    
    print("\n🔧 Setting up environment configuration...")
    
    # Create .env file if it doesn't exist
    env_file = Path(".env")
    if not env_file.exists():
        env_content = """# Supreme Coding Agent Configuration

# AI APIs
GEMINI_API_KEY=your-gemini-api-key-here
OPENAI_API_KEY=your-openai-api-key-here

# Database
DATABASE_URL=postgresql://user:password@localhost/jarvis_db

# Authentication
SECRET_KEY=your-super-secret-key-here
JWT_SECRET=your-jwt-secret-here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Third-party Integrations
STRIPE_SECRET_KEY=your-stripe-secret-key
STRIPE_WEBHOOK_SECRET=your-stripe-webhook-secret
FIREBASE_CONFIG=your-firebase-config-json
AUTH0_DOMAIN=your-auth0-domain
AUTH0_CLIENT_ID=your-auth0-client-id
AUTH0_CLIENT_SECRET=your-auth0-client-secret

# Development
DEBUG=true
LOG_LEVEL=INFO
ENVIRONMENT=development

# Performance
MAX_WORKERS=4
CACHE_TTL=3600
RATE_LIMIT_PER_MINUTE=100

# Features
ENABLE_AUTONOMOUS_MODE=true
ENABLE_SELF_IMPROVEMENT=true
ENABLE_ADVANCED_FEATURES=true
"""
        
        with open(env_file, 'w') as f:
            f.write(env_content)
        
        print("✅ Created .env configuration file")
    else:
        print("✅ .env file already exists")

def create_project_structure():
    """Create necessary project directories."""
    
    print("\n📁 Creating project structure...")
    
    directories = [
        "supreme_projects",
        "coding_projects", 
        "logs",
        "cache",
        "temp",
        "backups",
        "exports",
        "templates",
        "plugins"
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ {directory}/")

def setup_git_hooks():
    """Setup Git hooks for code quality."""
    
    print("\n🔗 Setting up Git hooks...")
    
    git_dir = Path(".git")
    if git_dir.exists():
        hooks_dir = git_dir / "hooks"
        hooks_dir.mkdir(exist_ok=True)
        
        # Pre-commit hook
        pre_commit_hook = hooks_dir / "pre-commit"
        hook_content = """#!/bin/bash
# Supreme Coding Agent Pre-commit Hook

echo "🔍 Running code quality checks..."

# Run Black formatter
black --check . || {
    echo "❌ Code formatting issues found. Run 'black .' to fix."
    exit 1
}

# Run tests
pytest tests/ || {
    echo "❌ Tests failed. Fix issues before committing."
    exit 1
}

echo "✅ All checks passed!"
"""
        
        with open(pre_commit_hook, 'w') as f:
            f.write(hook_content)
        
        # Make executable
        os.chmod(pre_commit_hook, 0o755)
        print("✅ Git pre-commit hook installed")
    else:
        print("⚠️ Not a Git repository - skipping Git hooks")

def test_installation():
    """Test the installation."""
    
    print("\n🧪 Testing installation...")
    
    try:
        # Test core imports
        import google.generativeai
        print("✅ Gemini AI SDK")
        
        import openai
        print("✅ OpenAI SDK")
        
        import aiohttp
        print("✅ Async HTTP")
        
        import fastapi
        print("✅ FastAPI")
        
        import sqlalchemy
        print("✅ SQLAlchemy")
        
        # Test Jarvis modules
        from core.modules.supreme_coding_agent import SupremeCodingAgent
        print("✅ Supreme Coding Agent")
        
        from core.modules.autonomous_app_builder import AutonomousAppBuilder
        print("✅ Autonomous App Builder")
        
        print("\n🎉 Installation test successful!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def display_next_steps():
    """Display next steps for the user."""
    
    print("\n🎯 NEXT STEPS")
    print("=" * 40)
    print("1. Set up your API keys in .env file:")
    print("   - Get Gemini API key: https://makersuite.google.com/app/apikey")
    print("   - Get OpenAI API key: https://platform.openai.com/api-keys")
    print("")
    print("2. Test the Supreme Coding Agent:")
    print("   python main.py --cli")
    print("   > build app a social media platform with real-time chat")
    print("")
    print("3. Try advanced features:")
    print("   > enhance app [add AI-powered recommendations]")
    print("   > deploy app [to production]")
    print("   > add integration [stripe for payments]")
    print("")
    print("4. Explore capabilities:")
    print("   - Full-stack web applications")
    print("   - iOS and Android mobile apps")
    print("   - Advanced integrations (Stripe, Firebase, OpenAI)")
    print("   - Autonomous debugging and optimization")
    print("   - Production-ready deployment")
    print("")
    print("🚀 Your Supreme Coding Agent is ready to build anything!")

def main():
    """Main setup function."""
    
    print("🚀 SUPREME AUTONOMOUS CODING AGENT SETUP")
    print("=" * 60)
    print("Setting up the most advanced AI coding system ever created...")
    print("")
    
    try:
        # Install dependencies
        install_dependencies()
        
        # Setup environment
        setup_environment()
        
        # Create project structure
        create_project_structure()
        
        # Setup Git hooks
        setup_git_hooks()
        
        # Test installation
        if test_installation():
            print("\n✅ SETUP COMPLETED SUCCESSFULLY!")
            display_next_steps()
        else:
            print("\n❌ Setup completed with some issues. Check the errors above.")
            
    except KeyboardInterrupt:
        print("\n❌ Setup interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
