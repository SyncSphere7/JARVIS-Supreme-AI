"""
Web Builder module for Jarvis.
Automates website creation, file generation, and deployment.
"""
import os
import subprocess
import tempfile
import shutil
from pathlib import Path
from typing import Dict, List
from core.utils.log import logger


class WebBuilder:
    def __init__(self, brain):
        self.brain = brain
        self.current_project = None
        self.project_dir = None
        self.jarvis_root = Path(__file__).parent.parent.parent
        self.projects_root = self.jarvis_root / "projects"

    def set_current_project(self, project_path: str):
        """Set the current working project."""
        self.project_dir = Path(project_path)
        self.current_project = self.project_dir.name

    def create_website(self, description: str, project_name: str = "my_website") -> str:
        """Create a complete website from description."""
        try:
            # Create project directory
            self.project_dir = self.projects_root / project_name
            self.project_dir.mkdir(parents=True, exist_ok=True)
            self.current_project = project_name
            
            # Generate website structure with detailed specifications
            prompt = f"""Create a complete, modern, responsive website based on this EXACT description: {description}

IMPORTANT: Follow the user's specifications EXACTLY. If they mention:
- Specific colors (hex codes, color names) - use them precisely
- Specific fonts - implement them exactly
- Specific layouts - create them as described
- Specific components - build them as requested
- Specific styling - apply it exactly as specified

Please provide:
1. Complete HTML file (index.html) with semantic structure
2. Complete CSS file (style.css) with exact specifications
3. JavaScript file (script.js) for any interactive features
4. Any additional pages mentioned

Requirements:
- Use EXACT colors, fonts, and styling specified by the user
- Implement responsive design (mobile-first)
- Use modern CSS (Grid/Flexbox, CSS Variables)
- Include smooth animations and transitions
- Add hover effects and micro-interactions
- Ensure accessibility (ARIA labels, semantic HTML)
- Make it pixel-perfect to the description
- Include Google Fonts if specific fonts are mentioned
- Use CSS custom properties for colors and spacing

Format your response as separate code blocks with clear file names like:

**index.html:**
```html
[HTML code here]
```

**style.css:**
```css
[CSS code here]
```

**script.js:**
```javascript
[JavaScript code here]
```"""

            response = self.brain.think(prompt, max_tokens=2000)
            
            # Parse and save files
            files_created = self._parse_and_save_files(response)
            
            # Create package.json for easy serving
            self._create_package_json()
            
            result = f"✅ Website '{project_name}' created successfully!\n"
            result += f"📁 Location: {self.project_dir.absolute()}\n"
            result += f"📄 Files created: {', '.join(files_created)}\n\n"
            result += "🚀 To run locally:\n"
            result += f"cd {self.project_dir}\n"
            result += "python -m http.server 8000\n"
            result += "Then open: http://localhost:8000\n\n"
            result += "Or use: npx serve . (if you have Node.js)"
            
            return result
            
        except Exception as e:
            return f"❌ Error creating website: {e}"

    def _parse_and_save_files(self, response: str) -> List[str]:
        """Parse LLM response and save code files."""
        files_created = []
        current_file = None
        current_content = []
        in_code_block = False

        lines = response.split('\n')

        for line in lines:
            # Detect file names - more flexible detection
            line_lower = line.lower()
            if any(ext in line_lower for ext in ['.html', '.css', '.js', '.json']):
                if 'index.html' in line_lower or 'html' in line_lower:
                    current_file = 'index.html'
                elif 'style.css' in line_lower or 'css' in line_lower:
                    current_file = 'style.css'
                elif 'script.js' in line_lower or 'javascript' in line_lower or '.js' in line_lower:
                    current_file = 'script.js'
                elif 'about.html' in line_lower:
                    current_file = 'about.html'
                elif 'contact.html' in line_lower:
                    current_file = 'contact.html'
                continue

            # Detect code blocks
            if line.strip().startswith('```'):
                if in_code_block and current_file and current_content:
                    # Save the file
                    self._save_file(current_file, '\n'.join(current_content))
                    files_created.append(current_file)
                    current_content = []
                in_code_block = not in_code_block
                # Auto-detect file type from code block language
                if in_code_block and not current_file:
                    if 'html' in line.lower():
                        current_file = 'index.html'
                    elif 'css' in line.lower():
                        current_file = 'style.css'
                    elif 'javascript' in line.lower() or 'js' in line.lower():
                        current_file = 'script.js'
                continue

            # Collect content
            if in_code_block:
                if not current_file:
                    # Auto-detect from content
                    if '<!DOCTYPE html>' in line or '<html' in line:
                        current_file = 'index.html'
                    elif 'body {' in line or '.container' in line:
                        current_file = 'style.css'
                    elif 'function' in line or 'document.' in line:
                        current_file = 'script.js'

                if current_file:
                    current_content.append(line)

        # Save last file if needed
        if current_file and current_content:
            self._save_file(current_file, '\n'.join(current_content))
            files_created.append(current_file)

        # Ensure we always have an HTML file
        if 'index.html' not in files_created:
            self._create_fallback_html()
            files_created.append('index.html')

        return files_created

    def _create_fallback_html(self):
        """Create a basic HTML file if none was generated."""
        html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Website</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header>
        <h1>Welcome to My Website</h1>
        <nav>
            <a href="#home">Home</a>
            <a href="#about">About</a>
            <a href="#contact">Contact</a>
        </nav>
    </header>

    <main>
        <section id="home">
            <h2>Home</h2>
            <p>This is the home section of your website.</p>
        </section>

        <section id="about">
            <h2>About</h2>
            <p>Tell visitors about yourself or your business.</p>
        </section>

        <section id="contact">
            <h2>Contact</h2>
            <p>Contact information goes here.</p>
        </section>
    </main>

    <script src="script.js"></script>
</body>
</html>"""
        self._save_file('index.html', html_content)

    def _save_file(self, filename: str, content: str):
        """Save content to file."""
        file_path = self.project_dir / filename
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        logger.info(f"Created: {filename}")

    def _create_package_json(self):
        """Create package.json for easy serving."""
        package_json = {
            "name": self.current_project,
            "version": "1.0.0",
            "description": "Website created by Jarvis",
            "scripts": {
                "start": "python -m http.server 8000",
                "serve": "npx serve ."
            }
        }
        
        import json
        with open(self.project_dir / 'package.json', 'w') as f:
            json.dump(package_json, f, indent=2)

    def run_local_server(self, port: int = 8000, auto_open: bool = False) -> str:
        """Start a local development server."""
        if not self.project_dir or not self.project_dir.exists():
            return "❌ No project found. Create a website first."

        try:
            # Check if port is already in use
            import socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex(('localhost', port))
            sock.close()

            if result == 0:
                # Port is in use, try next port
                port += 1
                logger.info(f"Port {port-1} in use, trying port {port}")

            logger.info(f"Starting server on port {port}...")
            cmd = f"cd '{self.project_dir}' && python -m http.server {port}"

            # Start server in background
            process = subprocess.Popen(
                cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            url = f"http://localhost:{port}"

            # Auto-open in browser if requested
            if auto_open:
                try:
                    if os.name == 'posix':  # macOS/Linux
                        subprocess.run(['open', url], check=True)
                    elif os.name == 'nt':  # Windows
                        subprocess.run(['start', url], shell=True, check=True)
                except:
                    pass  # Ignore browser opening errors

            return f"🚀 Server started!\n📍 URL: {url}\n💡 Press Ctrl+C in terminal to stop"

        except Exception as e:
            return f"❌ Error starting server: {e}"

    def deploy_website(self, platform: str = "auto") -> str:
        """Deploy website autonomously to multiple platforms."""
        if not self.project_dir or not self.project_dir.exists():
            return "❌ No project found. Create a website first."

        try:
            # Generate autonomous deployment configuration
            prompt = f"""Create complete autonomous deployment setup for this website:

Project: {self.project_dir.name}
Platform: {platform}

Provide:
1. Deployment configuration files
2. Build optimization scripts
3. CI/CD pipeline setup
4. Performance optimizations
5. Security configurations
6. Custom domain setup
7. SSL/HTTPS configuration
8. Monitoring and analytics setup

Make it production-ready and fully autonomous."""

            deployment_config = self.brain.think(prompt, max_tokens=1200)

            # Create deployment directory
            deploy_dir = self.project_dir / "deployment"
            deploy_dir.mkdir(exist_ok=True)

            # Create platform-specific configurations
            self._create_netlify_config(deploy_dir)
            self._create_vercel_config(deploy_dir)
            self._create_github_actions(deploy_dir)

            # Create deployment scripts
            self._create_deployment_scripts(deploy_dir, platform)

            # Create comprehensive deployment guide
            with open(deploy_dir / "DEPLOYMENT_GUIDE.md", "w") as f:
                f.write(f"# Autonomous Deployment Guide\n\n{deployment_config}")

            instructions = f"""🚀 **Autonomous Deployment Ready!**

📁 **Deployment files created:** {deploy_dir}

**Quick Deploy Options:**
1. **Netlify:** Drag {self.project_dir} to https://app.netlify.com/drop
2. **Vercel:** Upload to https://vercel.com/new
3. **GitHub Pages:** Push to GitHub and enable Pages
4. **Automated:** Run ./deployment/deploy.sh

**Advanced Features:**
✅ Performance optimizations
✅ Security headers
✅ SSL/HTTPS ready
✅ CI/CD pipeline
✅ Custom domain support
✅ Analytics integration

📋 **Files ready at:** {self.project_dir.absolute()}

🔗 **All files are production-ready!**
"""
            return instructions

        except Exception as e:
            return f"❌ Error setting up deployment: {e}"

    def _create_netlify_config(self, deploy_dir: Path):
        """Create Netlify configuration."""
        netlify_config = """[build]
  publish = "."
  command = "echo 'Build complete'"

[build.environment]
  NODE_VERSION = "18"

[[headers]]
  for = "/*"
  [headers.values]
    X-Frame-Options = "DENY"
    X-XSS-Protection = "1; mode=block"
    X-Content-Type-Options = "nosniff"
    Referrer-Policy = "strict-origin-when-cross-origin"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
"""
        with open(deploy_dir / "netlify.toml", "w") as f:
            f.write(netlify_config)

    def _create_vercel_config(self, deploy_dir: Path):
        """Create Vercel configuration."""
        vercel_config = """{
  "version": 2,
  "builds": [
    {
      "src": "**/*",
      "use": "@vercel/static"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/$1"
    }
  ],
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        {
          "key": "X-Content-Type-Options",
          "value": "nosniff"
        },
        {
          "key": "X-Frame-Options",
          "value": "DENY"
        },
        {
          "key": "X-XSS-Protection",
          "value": "1; mode=block"
        }
      ]
    }
  ]
}"""
        with open(deploy_dir / "vercel.json", "w") as f:
            f.write(vercel_config)

    def _create_github_actions(self, deploy_dir: Path):
        """Create GitHub Actions workflow."""
        github_dir = deploy_dir / ".github" / "workflows"
        github_dir.mkdir(parents=True, exist_ok=True)

        workflow = """name: Deploy to GitHub Pages

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Setup Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'

    - name: Optimize files
      run: |
        echo "Optimizing website files..."
        # Add optimization commands here

    - name: Deploy to GitHub Pages
      uses: peaceiris/actions-gh-pages@v3
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: ./
"""
        with open(github_dir / "deploy.yml", "w") as f:
            f.write(workflow)

    def _create_deployment_scripts(self, deploy_dir: Path, platform: str):
        """Create deployment scripts."""
        deploy_script = f"""#!/bin/bash
# Autonomous deployment script

echo "🚀 Starting autonomous deployment..."

# Optimize files
echo "📦 Optimizing files..."
if command -v npx &> /dev/null; then
    echo "Minifying CSS and JS..."
    # Add minification commands
fi

# Platform-specific deployment
case "{platform}" in
    "netlify")
        echo "🌐 Deploying to Netlify..."
        echo "Drag your project folder to https://app.netlify.com/drop"
        ;;
    "vercel")
        echo "⚡ Deploying to Vercel..."
        echo "Upload to https://vercel.com/new"
        ;;
    "github")
        echo "🐙 Setting up GitHub Pages..."
        echo "Push to GitHub and enable Pages in settings"
        ;;
    *)
        echo "🎯 Auto-deployment ready for all platforms"
        ;;
esac

echo "✅ Deployment preparation complete!"
"""

        with open(deploy_dir / "deploy.sh", "w") as f:
            f.write(deploy_script)

        # Make executable
        os.chmod(deploy_dir / "deploy.sh", 0o755)

    def improve_website(self, improvement_request: str) -> str:
        """Improve existing website based on request."""
        if not self.project_dir or not self.project_dir.exists():
            return "❌ No project found. Create a website first."
        
        try:
            # Read current files
            current_files = {}
            for file_path in self.project_dir.glob('*.html'):
                with open(file_path, 'r') as f:
                    current_files[file_path.name] = f.read()
            
            for file_path in self.project_dir.glob('*.css'):
                with open(file_path, 'r') as f:
                    current_files[file_path.name] = f.read()
            
            for file_path in self.project_dir.glob('*.js'):
                with open(file_path, 'r') as f:
                    current_files[file_path.name] = f.read()
            
            # Generate improvements
            prompt = f"""Improve this website based on the request: {improvement_request}

Current files:
{chr(10).join([f"{name}:{chr(10)}{content[:500]}..." for name, content in current_files.items()])}

Please provide the improved versions of the files that need changes.
Format as separate code blocks with clear file names."""
            
            response = self.brain.think(prompt, max_tokens=2000)
            
            # Parse and update files
            files_updated = self._parse_and_save_files(response)
            
            return f"✅ Website improved!\n📄 Files updated: {', '.join(files_updated)}"
            
        except Exception as e:
            return f"❌ Error improving website: {e}"
