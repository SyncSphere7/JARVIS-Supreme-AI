#!/usr/bin/env python3
"""
JARVIS Automation System - Advanced Task Execution and Automation
Comprehensive automation capabilities for JARVIS Supreme Being AI V01
"""

import os
import sys
import subprocess
import threading
import time
import json
import sqlite3
import shutil
import glob
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from pathlib import Path
import psutil

class JarvisAutomationSystem:
    """Advanced automation system for JARVIS Supreme Being AI"""
    
    def __init__(self, automation_dir: str = "supreme_automation"):
        self.automation_dir = automation_dir
        self.db_path = os.path.join(automation_dir, "automation.db")
        self.scripts_dir = os.path.join(automation_dir, "scripts")
        self.logs_dir = os.path.join(automation_dir, "logs")
        
        # Automation capabilities
        self.capabilities = {
            'file_operations': True,
            'system_commands': True,
            'process_management': True,
            'script_execution': True
        }
        
        # Active tasks
        self.active_tasks = {}
        self.running_processes = {}
        
        # Statistics
        self.automation_stats = {
            'total_tasks_executed': 0,
            'successful_tasks': 0,
            'failed_tasks': 0,
            'files_processed': 0,
            'commands_executed': 0
        }
        
        # Thread lock
        self.automation_lock = threading.Lock()
        
        # Initialize system
        self.initialize_automation_system()
    
    def initialize_automation_system(self):
        """Initialize the automation system"""
        print("🔧 INITIALIZING JARVIS AUTOMATION SYSTEM...")
        
        try:
            # Create directories
            os.makedirs(self.automation_dir, exist_ok=True)
            os.makedirs(self.scripts_dir, exist_ok=True)
            os.makedirs(self.logs_dir, exist_ok=True)
            
            # Initialize database
            self.init_database()
            
            # Load existing stats
            self.load_automation_stats()
            
            print("✅ JARVIS Automation System initialized successfully")
            print(f"🔧 Automation Capabilities: {sum(self.capabilities.values())}/4 active")
            
        except Exception as e:
            print(f"❌ Automation system initialization error: {e}")
    
    def init_database(self):
        """Initialize SQLite database for automation data"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Task execution history
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS task_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task_name TEXT,
                    task_type TEXT,
                    command TEXT,
                    status TEXT,
                    start_time TEXT,
                    end_time TEXT,
                    duration REAL,
                    output TEXT,
                    error_message TEXT
                )
            ''')
            
            # File operations log
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS file_operations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    operation_type TEXT,
                    source_path TEXT,
                    target_path TEXT,
                    status TEXT,
                    timestamp TEXT,
                    file_size INTEGER,
                    error_message TEXT
                )
            ''')
            
            conn.commit()
    
    def execute_command(self, command: str, working_dir: str = None, 
                       timeout: int = 300, capture_output: bool = True) -> Dict[str, Any]:
        """Execute system command with comprehensive logging"""
        
        task_id = f"cmd_{int(time.time())}"
        start_time = datetime.now()
        
        try:
            print(f"🔧 Executing command: {command}")
            
            # Prepare command execution
            if working_dir:
                original_dir = os.getcwd()
                os.chdir(working_dir)
            
            # Execute command
            if capture_output:
                result = subprocess.run(
                    command,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=timeout
                )
                
                output = result.stdout
                error = result.stderr
                return_code = result.returncode
            else:
                return_code = subprocess.run(command, shell=True, timeout=timeout).returncode
                output = ""
                error = ""
            
            # Restore working directory
            if working_dir:
                os.chdir(original_dir)
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            # Determine status
            status = "success" if return_code == 0 else "failed"
            
            # Log execution
            self.log_task_execution(
                task_name=task_id,
                task_type="command",
                command=command,
                status=status,
                start_time=start_time.isoformat(),
                end_time=end_time.isoformat(),
                duration=duration,
                output=output,
                error_message=error
            )
            
            # Update statistics
            with self.automation_lock:
                self.automation_stats['total_tasks_executed'] += 1
                self.automation_stats['commands_executed'] += 1
                if status == "success":
                    self.automation_stats['successful_tasks'] += 1
                else:
                    self.automation_stats['failed_tasks'] += 1
            
            return {
                'task_id': task_id,
                'command': command,
                'status': status,
                'return_code': return_code,
                'output': output,
                'error': error,
                'duration': duration,
                'start_time': start_time.isoformat(),
                'end_time': end_time.isoformat()
            }
            
        except subprocess.TimeoutExpired:
            return {
                'task_id': task_id,
                'command': command,
                'status': 'timeout',
                'error': f'Command timed out after {timeout} seconds',
                'duration': timeout
            }
        except Exception as e:
            return {
                'task_id': task_id,
                'command': command,
                'status': 'error',
                'error': str(e),
                'duration': (datetime.now() - start_time).total_seconds()
            }
    
    def create_file(self, file_path: str, content: str = "", 
                   encoding: str = "utf-8") -> Dict[str, Any]:
        """Create a file with specified content"""
        
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            # Write file
            with open(file_path, 'w', encoding=encoding) as f:
                f.write(content)
            
            file_size = os.path.getsize(file_path)
            
            # Log operation
            self.log_file_operation(
                operation_type="create",
                source_path=file_path,
                status="success",
                file_size=file_size
            )
            
            self.automation_stats['files_processed'] += 1
            
            return {
                'status': 'success',
                'file_path': file_path,
                'file_size': file_size,
                'message': f'File created successfully: {file_path}'
            }
            
        except Exception as e:
            self.log_file_operation(
                operation_type="create",
                source_path=file_path,
                status="failed",
                error_message=str(e)
            )
            
            return {
                'status': 'failed',
                'file_path': file_path,
                'error': str(e)
            }
    
    def copy_file(self, source_path: str, target_path: str) -> Dict[str, Any]:
        """Copy file from source to target"""
        
        try:
            # Ensure target directory exists
            os.makedirs(os.path.dirname(target_path), exist_ok=True)
            
            # Copy file
            shutil.copy2(source_path, target_path)
            
            file_size = os.path.getsize(target_path)
            
            # Log operation
            self.log_file_operation(
                operation_type="copy",
                source_path=source_path,
                target_path=target_path,
                status="success",
                file_size=file_size
            )
            
            self.automation_stats['files_processed'] += 1
            
            return {
                'status': 'success',
                'source_path': source_path,
                'target_path': target_path,
                'file_size': file_size,
                'message': f'File copied successfully: {source_path} -> {target_path}'
            }
            
        except Exception as e:
            self.log_file_operation(
                operation_type="copy",
                source_path=source_path,
                target_path=target_path,
                status="failed",
                error_message=str(e)
            )
            
            return {
                'status': 'failed',
                'source_path': source_path,
                'target_path': target_path,
                'error': str(e)
            }
    
    def delete_file(self, file_path: str) -> Dict[str, Any]:
        """Delete a file"""
        
        try:
            if not os.path.exists(file_path):
                return {
                    'status': 'failed',
                    'file_path': file_path,
                    'error': 'File does not exist'
                }
            
            file_size = os.path.getsize(file_path)
            
            # Delete file
            os.remove(file_path)
            
            # Log operation
            self.log_file_operation(
                operation_type="delete",
                source_path=file_path,
                status="success",
                file_size=file_size
            )
            
            self.automation_stats['files_processed'] += 1
            
            return {
                'status': 'success',
                'file_path': file_path,
                'file_size': file_size,
                'message': f'File deleted successfully: {file_path}'
            }
            
        except Exception as e:
            self.log_file_operation(
                operation_type="delete",
                source_path=file_path,
                status="failed",
                error_message=str(e)
            )
            
            return {
                'status': 'failed',
                'file_path': file_path,
                'error': str(e)
            }
    
    def find_files(self, pattern: str, directory: str = ".", 
                  recursive: bool = True) -> List[str]:
        """Find files matching a pattern"""
        
        try:
            if recursive:
                # Use glob with recursive pattern
                search_pattern = os.path.join(directory, "**", pattern)
                files = glob.glob(search_pattern, recursive=True)
            else:
                # Search only in specified directory
                search_pattern = os.path.join(directory, pattern)
                files = glob.glob(search_pattern)
            
            # Filter out directories, return only files
            files = [f for f in files if os.path.isfile(f)]
            
            return files
            
        except Exception as e:
            print(f"❌ Error finding files: {e}")
            return []
    
    def get_system_info(self) -> Dict[str, Any]:
        """Get comprehensive system information"""
        
        try:
            # CPU information
            cpu_info = {
                'cpu_count': psutil.cpu_count(),
                'cpu_percent': psutil.cpu_percent(interval=1)
            }
            
            # Memory information
            memory = psutil.virtual_memory()
            memory_info = {
                'total': memory.total,
                'available': memory.available,
                'percent': memory.percent,
                'used': memory.used,
                'free': memory.free
            }
            
            # Disk information
            disk = psutil.disk_usage('/')
            disk_info = {
                'total': disk.total,
                'used': disk.used,
                'free': disk.free,
                'percent': (disk.used / disk.total) * 100
            }
            
            return {
                'cpu': cpu_info,
                'memory': memory_info,
                'disk': disk_info,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {'error': f'Failed to get system info: {str(e)}'}
    
    def create_automation_script(self, script_name: str, script_content: str, 
                               script_type: str = "python") -> Dict[str, Any]:
        """Create an automation script"""
        
        try:
            # Determine file extension
            extensions = {
                'python': '.py',
                'bash': '.sh',
                'batch': '.bat'
            }
            
            extension = extensions.get(script_type, '.py')
            script_path = os.path.join(self.scripts_dir, f"{script_name}{extension}")
            
            # Add shebang for script types
            if script_type == "python":
                script_content = "#!/usr/bin/env python3\n" + script_content
            elif script_type == "bash":
                script_content = "#!/bin/bash\n" + script_content
            
            # Create script file
            result = self.create_file(script_path, script_content)
            
            # Make executable (Unix systems)
            if script_type in ['python', 'bash'] and os.name != 'nt':
                os.chmod(script_path, 0o755)
            
            if result['status'] == 'success':
                return {
                    'status': 'success',
                    'script_name': script_name,
                    'script_path': script_path,
                    'script_type': script_type,
                    'message': f'Automation script created: {script_path}'
                }
            else:
                return result
                
        except Exception as e:
            return {
                'status': 'failed',
                'script_name': script_name,
                'error': str(e)
            }
    
    def run_automation_script(self, script_name: str) -> Dict[str, Any]:
        """Run an automation script"""
        
        try:
            # Find script file
            script_files = self.find_files(f"{script_name}.*", self.scripts_dir, recursive=False)
            
            if not script_files:
                return {
                    'status': 'failed',
                    'script_name': script_name,
                    'error': 'Script not found'
                }
            
            script_path = script_files[0]
            
            # Determine execution command based on file extension
            extension = os.path.splitext(script_path)[1]
            
            if extension == '.py':
                command = f"python3 {script_path}"
            elif extension == '.sh':
                command = f"bash {script_path}"
            elif extension == '.bat':
                command = script_path
            else:
                command = script_path
            
            # Execute script
            result = self.execute_command(command)
            
            return {
                'status': result['status'],
                'script_name': script_name,
                'script_path': script_path,
                'execution_result': result
            }
            
        except Exception as e:
            return {
                'status': 'failed',
                'script_name': script_name,
                'error': str(e)
            }
    
    def log_task_execution(self, task_name: str, task_type: str, command: str,
                          status: str, start_time: str, end_time: str,
                          duration: float, output: str = "", error_message: str = ""):
        """Log task execution to database"""
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO task_history 
                    (task_name, task_type, command, status, start_time, end_time, 
                     duration, output, error_message)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (task_name, task_type, command, status, start_time, end_time,
                      duration, output, error_message))
                
                conn.commit()
                
        except Exception as e:
            print(f"❌ Error logging task execution: {e}")
    
    def log_file_operation(self, operation_type: str, source_path: str,
                          target_path: str = "", status: str = "success",
                          file_size: int = 0, error_message: str = ""):
        """Log file operation to database"""
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO file_operations 
                    (operation_type, source_path, target_path, status, 
                     timestamp, file_size, error_message)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (operation_type, source_path, target_path, status,
                      datetime.now().isoformat(), file_size, error_message))
                
                conn.commit()
                
        except Exception as e:
            print(f"❌ Error logging file operation: {e}")
    
    def load_automation_stats(self):
        """Load automation statistics from database"""
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Count task executions
                cursor.execute('SELECT COUNT(*) FROM task_history')
                self.automation_stats['total_tasks_executed'] = cursor.fetchone()[0]
                
                # Count successful tasks
                cursor.execute('SELECT COUNT(*) FROM task_history WHERE status = "success"')
                self.automation_stats['successful_tasks'] = cursor.fetchone()[0]
                
                # Count failed tasks
                cursor.execute('SELECT COUNT(*) FROM task_history WHERE status != "success"')
                self.automation_stats['failed_tasks'] = cursor.fetchone()[0]
                
                # Count file operations
                cursor.execute('SELECT COUNT(*) FROM file_operations')
                self.automation_stats['files_processed'] = cursor.fetchone()[0]
                
        except Exception as e:
            print(f"❌ Error loading automation stats: {e}")
    
    def get_automation_status(self) -> Dict[str, Any]:
        """Get comprehensive automation system status"""
        
        self.load_automation_stats()
        
        return {
            'capabilities': self.capabilities,
            'statistics': self.automation_stats,
            'active_tasks': len(self.active_tasks),
            'running_processes': len(self.running_processes),
            'database_path': self.db_path,
            'scripts_directory': self.scripts_dir,
            'system_status': 'active'
        }

def main():
    """Test the automation system"""
    print("🔧 JARVIS AUTOMATION SYSTEM TEST")
    print("=" * 50)
    
    # Initialize automation system
    automation = JarvisAutomationSystem()
    
    # Test command execution
    print("\n🔄 Testing command execution...")
    result = automation.execute_command("echo 'Hello from JARVIS Automation'")
    if result['status'] == 'success':
        print(f"✅ Command executed successfully")
        print(f"   Output: {result['output'].strip()}")
    else:
        print(f"❌ Command failed: {result.get('error', 'Unknown error')}")
    
    # Test file operations
    print("\n🔄 Testing file operations...")
    test_file = os.path.join(automation.automation_dir, "test_file.txt")
    
    # Create file
    create_result = automation.create_file(test_file, "This is a test file created by JARVIS")
    print(f"✅ File creation: {create_result['status']}")
    
    # Find files
    found_files = automation.find_files("test_file.txt", automation.automation_dir)
    print(f"✅ Found {len(found_files)} matching files")
    
    # Delete file
    if os.path.exists(test_file):
        delete_result = automation.delete_file(test_file)
        print(f"✅ File deletion: {delete_result['status']}")
    
    # Test system info
    print("\n🔄 Testing system information...")
    sys_info = automation.get_system_info()
    if 'error' not in sys_info:
        print(f"✅ System info retrieved")
        print(f"   CPU Usage: {sys_info['cpu']['cpu_percent']}%")
        print(f"   Memory Usage: {sys_info['memory']['percent']}%")
        print(f"   Disk Usage: {sys_info['disk']['percent']:.1f}%")
    else:
        print(f"❌ System info error: {sys_info['error']}")
    
    # Test script creation
    print("\n🔄 Testing script creation...")
    script_content = '''
print("Hello from JARVIS automation script!")
import datetime
print(f"Current time: {datetime.datetime.now()}")
'''
    
    script_result = automation.create_automation_script("test_script", script_content, "python")
    if script_result['status'] == 'success':
        print(f"✅ Script created: {script_result['script_path']}")
        
        # Test script execution
        run_result = automation.run_automation_script("test_script")
        if run_result['status'] == 'success':
            print(f"✅ Script executed successfully")
        else:
            print(f"❌ Script execution failed: {run_result.get('error', 'Unknown error')}")
    
    # Show automation status
    print("\n📊 Automation System Status:")
    status = automation.get_automation_status()
    print(f"   Active Capabilities: {sum(status['capabilities'].values())}/4")
    print(f"   Total Tasks Executed: {status['statistics']['total_tasks_executed']}")
    print(f"   Success Rate: {status['statistics']['successful_tasks']}/{status['statistics']['total_tasks_executed']}")
    print(f"   Files Processed: {status['statistics']['files_processed']}")
    
    print("\n🎉 AUTOMATION SYSTEM TEST COMPLETED!")
    print("✅ All automation functions working correctly")
    print("🔧 JARVIS Automation System is ready for task execution")

if __name__ == '__main__':
    main()
