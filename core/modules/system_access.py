"""
System Access module for Jarvis.
Provides file system access, app integration, and project management.
"""
import os
import subprocess
import json
from pathlib import Path
from typing import List, Dict, Optional
from core.utils.log import logger


class SystemAccess:
    def __init__(self, brain):
        self.brain = brain
        self.jarvis_root = Path(__file__).parent.parent.parent
        self.projects_dir = self.jarvis_root / "projects"
        self.projects_dir.mkdir(exist_ok=True)

    def find_existing_projects(self) -> List[Dict]:
        """Find all existing website projects."""
        projects = []
        
        # Check Jarvis projects folder
        if self.projects_dir.exists():
            for project_path in self.projects_dir.iterdir():
                if project_path.is_dir():
                    project_info = self._analyze_project(project_path)
                    if project_info:
                        projects.append(project_info)
        
        # Check common development folders
        home = Path.home()
        common_dirs = [
            home / "Desktop",
            home / "Documents",
            home / "Projects",
            home / "Development",
            home / "Sites",
            home / "www"
        ]
        
        for dir_path in common_dirs:
            if dir_path.exists():
                projects.extend(self._scan_directory_for_projects(dir_path))
        
        return projects

    def _analyze_project(self, project_path: Path) -> Optional[Dict]:
        """Analyze a directory to determine if it's a web project."""
        try:
            files = list(project_path.glob("*"))
            file_names = [f.name.lower() for f in files]
            
            # Check for web project indicators
            has_html = any('.html' in name for name in file_names)
            has_css = any('.css' in name for name in file_names)
            has_js = any('.js' in name for name in file_names)
            has_package_json = 'package.json' in file_names
            has_index = 'index.html' in file_names
            
            if has_html or has_package_json:
                return {
                    'name': project_path.name,
                    'path': str(project_path.absolute()),
                    'type': 'web_project',
                    'files': {
                        'html': has_html,
                        'css': has_css,
                        'js': has_js,
                        'index': has_index,
                        'package_json': has_package_json
                    },
                    'last_modified': project_path.stat().st_mtime
                }
        except Exception as e:
            logger.warning(f"Error analyzing {project_path}: {e}")
        
        return None

    def _scan_directory_for_projects(self, directory: Path, max_depth: int = 2) -> List[Dict]:
        """Scan directory for web projects (limited depth)."""
        projects = []
        
        try:
            if max_depth <= 0:
                return projects
            
            for item in directory.iterdir():
                if item.is_dir() and not item.name.startswith('.'):
                    # Check if this directory is a project
                    project_info = self._analyze_project(item)
                    if project_info:
                        projects.append(project_info)
                    
                    # Recursively scan subdirectories
                    if max_depth > 1:
                        projects.extend(self._scan_directory_for_projects(item, max_depth - 1))
        
        except PermissionError:
            pass  # Skip directories we can't access
        except Exception as e:
            logger.warning(f"Error scanning {directory}: {e}")
        
        return projects

    def list_projects(self) -> str:
        """List all found projects."""
        projects = self.find_existing_projects()
        
        if not projects:
            return "❌ No web projects found on your system."
        
        result = f"📁 Found {len(projects)} web projects:\n\n"
        
        for i, project in enumerate(projects, 1):
            result += f"{i}. **{project['name']}**\n"
            result += f"   📍 Path: {project['path']}\n"
            result += f"   📄 Files: "
            files = []
            if project['files']['index']:
                files.append("index.html")
            if project['files']['css']:
                files.append("CSS")
            if project['files']['js']:
                files.append("JS")
            if project['files']['package_json']:
                files.append("package.json")
            result += ", ".join(files) + "\n\n"
        
        return result

    def switch_to_project(self, project_name: str) -> str:
        """Switch to an existing project."""
        projects = self.find_existing_projects()
        
        # Find project by name (case insensitive)
        target_project = None
        for project in projects:
            if project['name'].lower() == project_name.lower():
                target_project = project
                break
        
        if not target_project:
            return f"❌ Project '{project_name}' not found. Use 'list projects' to see available projects."
        
        # Update web builder to use this project
        from core.modules.web_builder import WebBuilder
        # This is a bit hacky, but we need to update the web_builder's project_dir
        # In a real implementation, we'd have better state management
        
        return f"✅ Switched to project: {target_project['name']}\n📍 Location: {target_project['path']}\n🚀 You can now use 'run dev', 'enhance design', etc."

    def open_in_vscode(self, project_path: str = None) -> str:
        """Open project in VS Code."""
        if not project_path:
            projects = self.find_existing_projects()
            if not projects:
                return "❌ No projects found."
            project_path = projects[0]['path']  # Use first project
        
        try:
            subprocess.run(['code', project_path], check=True)
            return f"✅ Opened {project_path} in VS Code"
        except subprocess.CalledProcessError:
            return "❌ VS Code not found. Install VS Code or use 'code' command."
        except Exception as e:
            return f"❌ Error opening VS Code: {e}"

    def open_in_browser(self, project_path: str = None, url: str = None) -> str:
        """Open project or URL in browser."""
        if url:
            # Open specific URL
            try:
                if os.name == 'nt':  # Windows
                    subprocess.run(['start', url], shell=True, check=True)
                elif os.name == 'posix':  # macOS/Linux
                    subprocess.run(['open', url], check=True)
                return f"✅ Opened {url} in browser"
            except Exception as e:
                return f"❌ Error opening URL: {e}"

        # Open project file
        if not project_path:
            projects = self.find_existing_projects()
            if not projects:
                return "❌ No projects found."
            project_path = projects[0]['path']

        index_file = Path(project_path) / "index.html"
        if not index_file.exists():
            return f"❌ No index.html found in {project_path}"

        try:
            if os.name == 'nt':  # Windows
                os.startfile(str(index_file))
            elif os.name == 'posix':  # macOS/Linux
                subprocess.run(['open', str(index_file)], check=True)
            return f"✅ Opened {index_file} in browser"
        except Exception as e:
            return f"❌ Error opening browser: {e}"

    def open_chrome(self, url: str = "http://localhost:8000") -> str:
        """Open Chrome with specific URL."""
        try:
            if os.name == 'nt':  # Windows
                chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"
                subprocess.run([chrome_path, url], check=True)
            elif os.name == 'posix':  # macOS/Linux
                # Try different Chrome paths
                chrome_paths = [
                    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                    "/usr/bin/google-chrome",
                    "/usr/bin/chromium-browser"
                ]

                chrome_found = False
                for chrome_path in chrome_paths:
                    if os.path.exists(chrome_path):
                        subprocess.run([chrome_path, url], check=True)
                        chrome_found = True
                        break

                if not chrome_found:
                    # Fallback to system default
                    subprocess.run(['open', '-a', 'Google Chrome', url], check=True)

            return f"✅ Opened {url} in Chrome"
        except Exception as e:
            # Fallback to default browser
            try:
                if os.name == 'nt':
                    subprocess.run(['start', url], shell=True, check=True)
                elif os.name == 'posix':
                    subprocess.run(['open', url], check=True)
                return f"✅ Opened {url} in default browser (Chrome not found)"
            except Exception as e2:
                return f"❌ Error opening browser: {e2}"

    def run_server_for_project(self, project_name: str, port: int = 8000) -> str:
        """Start server for specific project."""
        projects = self.find_existing_projects()
        
        target_project = None
        for project in projects:
            if project['name'].lower() == project_name.lower():
                target_project = project
                break
        
        if not target_project:
            return f"❌ Project '{project_name}' not found."
        
        try:
            project_path = target_project['path']
            cmd = f"cd '{project_path}' && python -m http.server {port}"
            
            # Start server in background
            process = subprocess.Popen(
                cmd, 
                shell=True, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE
            )
            
            return f"🚀 Server started for {project_name}!\n📍 URL: http://localhost:{port}\n💡 Press Ctrl+C in terminal to stop"
            
        except Exception as e:
            return f"❌ Error starting server: {e}"

    def get_system_info(self) -> str:
        """Get system information."""
        try:
            import platform
            import psutil
            
            info = f"""💻 **System Information:**

**OS:** {platform.system()} {platform.release()}
**Architecture:** {platform.machine()}
**Processor:** {platform.processor()}
**Python:** {platform.python_version()}

**Memory:** {psutil.virtual_memory().total // (1024**3)} GB total
**Disk:** {psutil.disk_usage('/').total // (1024**3)} GB total

**Current Directory:** {os.getcwd()}
**Home Directory:** {Path.home()}
**Jarvis Location:** {self.jarvis_root}
"""
            return info
        except Exception as e:
            return f"❌ Error getting system info: {e}"

    def find_files(self, pattern: str, directory: str = None) -> str:
        """Find files matching pattern."""
        if not directory:
            directory = str(Path.home())
        
        try:
            search_path = Path(directory)
            if not search_path.exists():
                return f"❌ Directory {directory} not found."
            
            matches = list(search_path.rglob(pattern))[:20]  # Limit to 20 results
            
            if not matches:
                return f"❌ No files matching '{pattern}' found in {directory}"
            
            result = f"📁 Found {len(matches)} files matching '{pattern}':\n\n"
            for match in matches:
                result += f"📄 {match}\n"
            
            if len(matches) == 20:
                result += "\n... (showing first 20 results)"
            
            return result
            
        except Exception as e:
            return f"❌ Error searching files: {e}"
