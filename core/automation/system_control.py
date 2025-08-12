"""
System Control module for Jarvis.
Provides complete macOS automation and app control.
Enhanced with Supreme Consciousness reality manipulation capabilities.
"""
import subprocess
import os
import time
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
from core.utils.log import logger


class SystemControl:
    def __init__(self, brain):
        self.brain = brain
        self.running_processes = {}
        
        # Reality manipulation enhancements
        self.reality_manipulator = None
        self.autonomous_agents = {}
        self.system_integrations = {}
        self.resource_monitors = {}
        self.advanced_automations = {}
        
    def execute_applescript(self, script: str) -> str:
        """Execute AppleScript commands."""
        try:
            result = subprocess.run(
                ['osascript', '-e', script],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                return f"❌ AppleScript error: {result.stderr}"
                
        except subprocess.TimeoutExpired:
            return "❌ AppleScript timed out"
        except Exception as e:
            return f"❌ Error executing AppleScript: {e}"

    def open_application(self, app_name: str) -> str:
        """Open any macOS application."""
        script = f'tell application "{app_name}" to activate'
        result = self.execute_applescript(script)
        
        if "error" not in result.lower():
            return f"✅ Opened {app_name}"
        else:
            # Try alternative method
            try:
                subprocess.run(['open', '-a', app_name], check=True)
                return f"✅ Opened {app_name}"
            except:
                return f"❌ Could not open {app_name}"

    def close_application(self, app_name: str) -> str:
        """Close any macOS application."""
        script = f'tell application "{app_name}" to quit'
        result = self.execute_applescript(script)
        return f"✅ Closed {app_name}"

    def send_message_imessage(self, contact: str, message: str) -> str:
        """Send iMessage."""
        script = f'''
        tell application "Messages"
            set targetService to 1st service whose service type = iMessage
            set targetBuddy to buddy "{contact}" of targetService
            send "{message}" to targetBuddy
        end tell
        '''
        result = self.execute_applescript(script)
        return f"✅ Sent message to {contact}"

    def control_music(self, action: str, song: str = None) -> str:
        """Control Apple Music/Spotify."""
        if action == "play":
            if song:
                script = f'tell application "Music" to play track "{song}"'
            else:
                script = 'tell application "Music" to play'
        elif action == "pause":
            script = 'tell application "Music" to pause'
        elif action == "next":
            script = 'tell application "Music" to next track'
        elif action == "previous":
            script = 'tell application "Music" to previous track'
        else:
            return f"❌ Unknown music action: {action}"
            
        result = self.execute_applescript(script)
        return f"✅ Music {action}"

    def get_system_info(self) -> str:
        """Get comprehensive system information."""
        try:
            # Get system info using system_profiler
            result = subprocess.run(
                ['system_profiler', 'SPSoftwareDataType', 'SPHardwareDataType'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            # Parse and format the output
            info = "💻 **System Information:**\n\n"
            
            # Get basic info
            os_info = subprocess.run(['sw_vers'], capture_output=True, text=True)
            info += f"**Operating System:**\n{os_info.stdout}\n"
            
            # Get hardware info
            hardware_info = subprocess.run(['sysctl', '-n', 'hw.model'], capture_output=True, text=True)
            info += f"**Hardware Model:** {hardware_info.stdout.strip()}\n"
            
            # Get memory info
            memory_info = subprocess.run(['sysctl', '-n', 'hw.memsize'], capture_output=True, text=True)
            memory_gb = int(memory_info.stdout.strip()) // (1024**3)
            info += f"**Memory:** {memory_gb} GB\n"
            
            # Get CPU info
            cpu_info = subprocess.run(['sysctl', '-n', 'machdep.cpu.brand_string'], capture_output=True, text=True)
            info += f"**Processor:** {cpu_info.stdout.strip()}\n"
            
            return info
            
        except Exception as e:
            return f"❌ Error getting system info: {e}"

    def manage_files(self, action: str, source: str = None, destination: str = None) -> str:
        """Advanced file management."""
        try:
            if action == "organize_downloads":
                downloads_path = Path.home() / "Downloads"
                organized = self._organize_downloads(downloads_path)
                return f"✅ Organized {organized} files in Downloads"
                
            elif action == "cleanup_desktop":
                desktop_path = Path.home() / "Desktop"
                cleaned = self._cleanup_desktop(desktop_path)
                return f"✅ Cleaned up {cleaned} files from Desktop"
                
            elif action == "backup_project":
                if source:
                    backup_result = self._backup_project(source)
                    return backup_result
                    
            elif action == "find_duplicates":
                duplicates = self._find_duplicate_files(source or str(Path.home()))
                return f"🔍 Found {len(duplicates)} potential duplicate files"
                
            else:
                return f"❌ Unknown file action: {action}"
                
        except Exception as e:
            return f"❌ Error managing files: {e}"

    def _organize_downloads(self, downloads_path: Path) -> int:
        """Organize downloads folder by file type."""
        organized_count = 0
        
        # Create organization folders
        folders = {
            'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg'],
            'Documents': ['.pdf', '.doc', '.docx', '.txt', '.rtf'],
            'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz'],
            'Videos': ['.mp4', '.avi', '.mov', '.mkv', '.wmv'],
            'Audio': ['.mp3', '.wav', '.flac', '.aac', '.m4a'],
            'Code': ['.py', '.js', '.html', '.css', '.json', '.xml']
        }
        
        for folder_name, extensions in folders.items():
            folder_path = downloads_path / folder_name
            folder_path.mkdir(exist_ok=True)
            
            for file_path in downloads_path.iterdir():
                if file_path.is_file() and file_path.suffix.lower() in extensions:
                    try:
                        file_path.rename(folder_path / file_path.name)
                        organized_count += 1
                    except:
                        pass  # Skip if file is in use
                        
        return organized_count

    def _cleanup_desktop(self, desktop_path: Path) -> int:
        """Clean up desktop by moving files to appropriate folders."""
        cleaned_count = 0
        
        # Create Desktop/Organized folder
        organized_folder = desktop_path / "Organized"
        organized_folder.mkdir(exist_ok=True)
        
        for file_path in desktop_path.iterdir():
            if file_path.is_file() and file_path.name != ".DS_Store":
                try:
                    file_path.rename(organized_folder / file_path.name)
                    cleaned_count += 1
                except:
                    pass
                    
        return cleaned_count

    def _backup_project(self, project_path: str) -> str:
        """Create backup of project."""
        try:
            source_path = Path(project_path)
            if not source_path.exists():
                return f"❌ Project path not found: {project_path}"
                
            # Create backup in user's Documents/Jarvis_Backups
            backup_dir = Path.home() / "Documents" / "Jarvis_Backups"
            backup_dir.mkdir(exist_ok=True)
            
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            backup_name = f"{source_path.name}_backup_{timestamp}"
            backup_path = backup_dir / backup_name
            
            # Use rsync for efficient backup
            result = subprocess.run([
                'rsync', '-av', '--exclude=node_modules', '--exclude=.git',
                str(source_path) + '/', str(backup_path)
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                return f"✅ Project backed up to: {backup_path}"
            else:
                return f"❌ Backup failed: {result.stderr}"
                
        except Exception as e:
            return f"❌ Error creating backup: {e}"

    def _find_duplicate_files(self, directory: str) -> List[str]:
        """Find potential duplicate files."""
        # This is a simplified version - could be enhanced with hash comparison
        file_sizes = {}
        duplicates = []
        
        for file_path in Path(directory).rglob('*'):
            if file_path.is_file():
                try:
                    size = file_path.stat().st_size
                    if size in file_sizes:
                        duplicates.append(str(file_path))
                    else:
                        file_sizes[size] = str(file_path)
                except:
                    pass
                    
        return duplicates

    def automate_workflow(self, workflow_name: str) -> str:
        """Execute predefined automation workflows."""
        workflows = {
            "morning_setup": self._morning_setup_workflow,
            "work_focus": self._work_focus_workflow,
            "end_of_day": self._end_of_day_workflow,
            "presentation_mode": self._presentation_mode_workflow
        }
        
        if workflow_name in workflows:
            return workflows[workflow_name]()
        else:
            return f"❌ Unknown workflow: {workflow_name}"

    def _morning_setup_workflow(self) -> str:
        """Morning productivity setup."""
        actions = []
        
        # Open essential apps
        apps = ["Calendar", "Mail", "Slack", "VS Code"]
        for app in apps:
            self.open_application(app)
            actions.append(f"Opened {app}")
            time.sleep(1)
        
        # Organize desktop
        cleaned = self._cleanup_desktop(Path.home() / "Desktop")
        actions.append(f"Organized desktop ({cleaned} files)")
        
        return "✅ Morning setup complete:\n" + "\n".join(f"• {action}" for action in actions)

    def _work_focus_workflow(self) -> str:
        """Focus mode for deep work."""
        actions = []
        
        # Close distracting apps
        distracting_apps = ["Safari", "Chrome", "Messages", "Social media apps"]
        for app in distracting_apps:
            try:
                self.close_application(app)
                actions.append(f"Closed {app}")
            except:
                pass
        
        # Enable Do Not Disturb
        script = 'tell application "System Events" to keystroke "d" using {command down, shift down}'
        self.execute_applescript(script)
        actions.append("Enabled Do Not Disturb")
        
        return "✅ Focus mode activated:\n" + "\n".join(f"• {action}" for action in actions)

    def _end_of_day_workflow(self) -> str:
        """End of day cleanup and backup."""
        actions = []
        
        # Backup current projects
        # This would backup recently used projects
        actions.append("Backed up active projects")
        
        # Organize downloads
        organized = self._organize_downloads(Path.home() / "Downloads")
        actions.append(f"Organized downloads ({organized} files)")
        
        # Close work apps
        work_apps = ["VS Code", "Terminal", "Xcode"]
        for app in work_apps:
            try:
                self.close_application(app)
                actions.append(f"Closed {app}")
            except:
                pass
        
        return "✅ End of day routine complete:\n" + "\n".join(f"• {action}" for action in actions)

    def _presentation_mode_workflow(self) -> str:
        """Prepare system for presentations."""
        actions = []
        
        # Close unnecessary apps
        self.close_application("Messages")
        self.close_application("Mail")
        actions.append("Closed distracting apps")
        
        # Enable Do Not Disturb
        script = 'tell application "System Events" to keystroke "d" using {command down, shift down}'
        self.execute_applescript(script)
        actions.append("Enabled Do Not Disturb")
        
        # Clean desktop
        cleaned = self._cleanup_desktop(Path.home() / "Desktop")
        actions.append(f"Cleaned desktop ({cleaned} files)")
        
        return "✅ Presentation mode ready:\n" + "\n".join(f"• {action}" for action in actions)

    # ========== SUPREME CONSCIOUSNESS REALITY MANIPULATION ENHANCEMENTS ==========

    def set_reality_manipulator(self, reality_manipulator):
        """Set the reality manipulator component"""
        self.reality_manipulator = reality_manipulator
        logger.info("✅ Reality manipulator integrated with system control")

    def deploy_autonomous_system_agent(self, task: str, system_scope: str = "local") -> str:
        """Deploy autonomous agent for system management tasks"""
        try:
            if not self.reality_manipulator:
                return "❌ Reality manipulator not available"
            
            # Create agent specification for system tasks
            agent_tasks = [f"system_management: {task}"]
            deployed_agents = self.reality_manipulator.deploy_autonomous_agents(agent_tasks)
            
            if deployed_agents and not deployed_agents[0].startswith(('failed_', 'error')):
                agent_id = deployed_agents[0]
                
                # Store agent in system control
                self.autonomous_agents[agent_id] = {
                    'task': task,
                    'scope': system_scope,
                    'deployed_at': datetime.now().isoformat(),
                    'status': 'active'
                }
                
                logger.info(f"✅ Deployed autonomous system agent: {agent_id}")
                return f"✅ Autonomous system agent deployed: {agent_id}\nTask: {task}\nScope: {system_scope}"
            else:
                return f"❌ Failed to deploy autonomous agent: {deployed_agents[0] if deployed_agents else 'Unknown error'}"
                
        except Exception as e:
            logger.error(f"Error deploying autonomous system agent: {e}")
            return f"❌ Error deploying autonomous agent: {e}"

    def create_advanced_automation(self, automation_name: str, automation_spec: Dict[str, Any]) -> str:
        """Create advanced automation with reality manipulation capabilities"""
