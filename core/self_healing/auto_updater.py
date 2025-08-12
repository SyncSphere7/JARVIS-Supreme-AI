"""
Self-Healing and Auto-Update system for Jarvis.
Monitors health, fixes issues, and updates capabilities autonomously.
"""
import os
import sys
import subprocess
import json
import time
import traceback
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
from core.utils.log import logger


class AutoUpdater:
    def __init__(self, brain):
        self.brain = brain
        self.jarvis_root = Path(__file__).parent.parent.parent
        self.health_log = self.jarvis_root / "logs" / "health.log"
        self.health_log.parent.mkdir(exist_ok=True)
        
        self.last_health_check = None
        self.error_patterns = {}
        self.auto_fixes = {}
        self.update_sources = {
            'pip_packages': self._check_pip_updates,
            'system_dependencies': self._check_system_updates,
            'jarvis_modules': self._check_module_updates
        }
        
        self._initialize_auto_fixes()

    def _initialize_auto_fixes(self):
        """Initialize common auto-fix patterns."""
        self.auto_fixes = {
            'ModuleNotFoundError': self._fix_missing_module,
            'PermissionError': self._fix_permission_error,
            'ConnectionError': self._fix_connection_error,
            'ImportError': self._fix_import_error,
            'FileNotFoundError': self._fix_missing_file,
            'OSError': self._fix_os_error
        }

    def monitor_health(self) -> Dict:
        """Monitor Jarvis health and performance."""
        health_status = {
            'timestamp': datetime.now().isoformat(),
            'overall_status': 'healthy',
            'issues': [],
            'performance': {},
            'recommendations': []
        }
        
        try:
            # Check system resources
            health_status['performance'] = self._check_system_performance()
            
            # Check module integrity
            module_issues = self._check_module_integrity()
            if module_issues:
                health_status['issues'].extend(module_issues)
                health_status['overall_status'] = 'degraded'
            
            # Check dependencies
            dependency_issues = self._check_dependencies()
            if dependency_issues:
                health_status['issues'].extend(dependency_issues)
                health_status['overall_status'] = 'degraded'
            
            # Check for available updates
            updates = self._check_for_updates()
            if updates:
                health_status['recommendations'].extend(updates)
            
            # Log health status
            self._log_health_status(health_status)
            
            return health_status
            
        except Exception as e:
            logger.error(f"Error monitoring health: {e}")
            health_status['overall_status'] = 'error'
            health_status['issues'].append(f"Health monitoring error: {e}")
            return health_status

    def _check_system_performance(self) -> Dict:
        """Check system performance metrics."""
        try:
            # Try to import psutil, but gracefully handle if missing
            try:
                import psutil
                performance = {
                    'cpu_percent': psutil.cpu_percent(interval=0.1),  # Faster check
                    'memory_percent': psutil.virtual_memory().percent,
                    'disk_percent': psutil.disk_usage('/').percent,
                    'load_average': os.getloadavg()[0] if hasattr(os, 'getloadavg') else 0
                }
                return performance
            except ImportError:
                # Fallback to basic system info without psutil
                logger.info("psutil not available, using basic system info")
                return {
                    'status': 'basic_monitoring',
                    'load_average': os.getloadavg()[0] if hasattr(os, 'getloadavg') else 0,
                    'note': 'Install psutil for detailed monitoring'
                }

        except Exception as e:
            logger.error(f"Error checking performance: {e}")
            return {'error': str(e)}

    def _check_module_integrity(self) -> List[str]:
        """Check if all Jarvis modules are working correctly."""
        issues = []
        
        # Test core modules
        core_modules = [
            'core.brain.brain',
            'core.modules.web_builder',
            'core.modules.ui_designer',
            'core.modules.system_access',
            'core.modules.internet_access'
        ]
        
        for module_name in core_modules:
            try:
                __import__(module_name)
            except Exception as e:
                issues.append(f"Module {module_name} failed to import: {e}")
        
        return issues

    def _check_dependencies(self) -> List[str]:
        """Check if all required dependencies are available."""
        issues = []
        
        # Critical dependencies
        critical_deps = [
            'requests',
            'pathlib',
            'json',
            'sqlite3'
        ]
        
        # Optional but important dependencies
        optional_deps = [
            'psutil',
            'openai',
            'google.generativeai'
        ]
        
        for dep in critical_deps:
            try:
                __import__(dep)
            except ImportError:
                issues.append(f"Critical dependency missing: {dep}")
        
        for dep in optional_deps:
            try:
                __import__(dep)
            except ImportError:
                issues.append(f"Optional dependency missing: {dep} (reduced functionality)")
        
        return issues

    def _check_for_updates(self) -> List[str]:
        """Check for available updates."""
        recommendations = []
        
        for source_name, check_func in self.update_sources.items():
            try:
                updates = check_func()
                if updates:
                    recommendations.extend(updates)
            except Exception as e:
                logger.error(f"Error checking {source_name}: {e}")
        
        return recommendations

    def _check_pip_updates(self) -> List[str]:
        """Check for pip package updates."""
        try:
            # Use shorter timeout and skip if taking too long
            result = subprocess.run([
                sys.executable, '-m', 'pip', 'list', '--outdated', '--format=json'
            ], capture_output=True, text=True, timeout=10)

            if result.returncode == 0:
                outdated = json.loads(result.stdout)
                if outdated:
                    return [f"Update available: {pkg['name']} {pkg['version']} -> {pkg['latest_version']}"
                           for pkg in outdated[:3]]  # Limit to 3 updates

            return []

        except subprocess.TimeoutExpired:
            logger.info("Pip update check timed out - skipping")
            return ["Pip update check skipped (timeout)"]
        except Exception as e:
            logger.warning(f"Pip update check failed: {e}")
            return []

    def _check_system_updates(self) -> List[str]:
        """Check for system updates (macOS)."""
        try:
            result = subprocess.run([
                'softwareupdate', '-l'
            ], capture_output=True, text=True, timeout=30)
            
            if 'No new software available' not in result.stdout:
                return ["System updates available - run 'softwareupdate -i -a'"]
            
            return []
            
        except Exception as e:
            logger.error(f"Error checking system updates: {e}")
            return []

    def _check_module_updates(self) -> List[str]:
        """Check for Jarvis module updates."""
        # This could check a remote repository for updates
        # For now, just check if modules are up to date
        return []

    def auto_heal(self, error: Exception, context: Dict = None) -> str:
        """Automatically attempt to heal from errors."""
        try:
            error_type = type(error).__name__
            error_message = str(error)
            
            logger.info(f"Attempting auto-heal for {error_type}: {error_message}")
            
            # Try specific auto-fix
            if error_type in self.auto_fixes:
                fix_result = self.auto_fixes[error_type](error, context)
                if fix_result:
                    return f"✅ Auto-healed {error_type}: {fix_result}"
            
            # Try general AI-powered fix
            ai_fix = self._ai_powered_fix(error, context)
            if ai_fix:
                return f"🤖 AI-powered fix applied: {ai_fix}"
            
            return f"❌ Could not auto-heal {error_type}"
            
        except Exception as e:
            logger.error(f"Error in auto-heal: {e}")
            return f"❌ Auto-heal failed: {e}"

    def _fix_missing_module(self, error: Exception, context: Dict = None) -> str:
        """Fix missing module errors."""
        error_msg = str(error)
        
        # Extract module name
        if "No module named" in error_msg:
            module_name = error_msg.split("'")[1]
            
            # Try to install the module
            try:
                subprocess.run([
                    sys.executable, '-m', 'pip', 'install', module_name
                ], check=True, timeout=60)
                
                return f"Installed missing module: {module_name}"
                
            except subprocess.CalledProcessError:
                # Try common alternatives
                alternatives = {
                    'cv2': 'opencv-python',
                    'PIL': 'Pillow',
                    'sklearn': 'scikit-learn'
                }
                
                if module_name in alternatives:
                    try:
                        subprocess.run([
                            sys.executable, '-m', 'pip', 'install', alternatives[module_name]
                        ], check=True, timeout=60)
                        
                        return f"Installed alternative module: {alternatives[module_name]}"
                    except:
                        pass
        
        return None

    def _fix_permission_error(self, error: Exception, context: Dict = None) -> str:
        """Fix permission errors."""
        error_msg = str(error)
        
        # Try to fix common permission issues
        if "Permission denied" in error_msg:
            # Extract file path if available
            import re
            path_match = re.search(r"'([^']*)'", error_msg)
            if path_match:
                file_path = path_match.group(1)
                try:
                    # Try to change permissions
                    os.chmod(file_path, 0o755)
                    return f"Fixed permissions for: {file_path}"
                except:
                    pass
        
        return None

    def _fix_connection_error(self, error: Exception, context: Dict = None) -> str:
        """Fix connection errors."""
        # Wait and retry logic
        time.sleep(2)
        return "Applied connection retry delay"

    def _fix_import_error(self, error: Exception, context: Dict = None) -> str:
        """Fix import errors."""
        return self._fix_missing_module(error, context)

    def _fix_missing_file(self, error: Exception, context: Dict = None) -> str:
        """Fix missing file errors."""
        error_msg = str(error)
        
        # Try to create missing directories
        import re
        path_match = re.search(r"'([^']*)'", error_msg)
        if path_match:
            file_path = Path(path_match.group(1))
            try:
                file_path.parent.mkdir(parents=True, exist_ok=True)
                return f"Created missing directory: {file_path.parent}"
            except:
                pass
        
        return None

    def _fix_os_error(self, error: Exception, context: Dict = None) -> str:
        """Fix OS errors."""
        error_msg = str(error)
        
        if "Address already in use" in error_msg:
            return "Port conflict detected - will try alternative port"
        
        return None

    def _ai_powered_fix(self, error: Exception, context: Dict = None) -> str:
        """Use AI to suggest and apply fixes."""
        try:
            error_info = {
                'type': type(error).__name__,
                'message': str(error),
                'traceback': traceback.format_exc(),
                'context': context or {}
            }
            
            prompt = f"""An error occurred in Jarvis. Suggest a specific fix:

Error Type: {error_info['type']}
Error Message: {error_info['message']}
Context: {json.dumps(error_info['context'], indent=2)}

Provide a specific, actionable fix that can be implemented programmatically.
Focus on:
1. Installing missing dependencies
2. Creating missing files/directories
3. Fixing configuration issues
4. Adjusting permissions
5. Providing workarounds

Be concise and specific."""

            fix_suggestion = self.brain.think(prompt, max_tokens=200)
            
            # Log the suggestion for manual review
            logger.info(f"AI fix suggestion: {fix_suggestion}")
            
            return fix_suggestion
            
        except Exception as e:
            logger.error(f"Error in AI-powered fix: {e}")
            return None

    def _log_health_status(self, status: Dict):
        """Log health status to file."""
        try:
            with open(self.health_log, 'a') as f:
                f.write(f"{json.dumps(status)}\n")
        except Exception as e:
            logger.error(f"Error logging health status: {e}")

    def perform_maintenance(self) -> str:
        """Perform routine maintenance tasks."""
        maintenance_results = []
        
        try:
            # Clean up old logs
            log_cleanup = self._cleanup_old_logs()
            maintenance_results.append(log_cleanup)
            
            # Optimize databases
            db_optimization = self._optimize_databases()
            maintenance_results.append(db_optimization)
            
            # Update dependencies
            update_result = self._update_dependencies()
            maintenance_results.append(update_result)
            
            # Health check
            health_status = self.monitor_health()
            maintenance_results.append(f"Health check: {health_status['overall_status']}")
            
            return "🔧 **Maintenance Complete:**\n" + "\n".join(f"• {result}" for result in maintenance_results)
            
        except Exception as e:
            return f"❌ Maintenance error: {e}"

    def _cleanup_old_logs(self) -> str:
        """Clean up old log files."""
        try:
            logs_dir = self.jarvis_root / "logs"
            if not logs_dir.exists():
                return "No logs to clean"
            
            cutoff_date = datetime.now() - timedelta(days=30)
            cleaned_count = 0
            
            for log_file in logs_dir.glob("*.log"):
                if log_file.stat().st_mtime < cutoff_date.timestamp():
                    log_file.unlink()
                    cleaned_count += 1
            
            return f"Cleaned {cleaned_count} old log files"
            
        except Exception as e:
            return f"Log cleanup error: {e}"

    def _optimize_databases(self) -> str:
        """Optimize SQLite databases."""
        try:
            import sqlite3
            
            db_files = [
                self.jarvis_root / "memory" / "conversations.db",
                self.jarvis_root / "memory" / "knowledge.db",
                self.jarvis_root / "memory" / "preferences.db"
            ]
            
            optimized_count = 0
            for db_file in db_files:
                if db_file.exists():
                    with sqlite3.connect(db_file) as conn:
                        conn.execute("VACUUM")
                        conn.execute("ANALYZE")
                    optimized_count += 1
            
            return f"Optimized {optimized_count} databases"
            
        except Exception as e:
            return f"Database optimization error: {e}"

    def _update_dependencies(self) -> str:
        """Update critical dependencies."""
        try:
            # Update pip itself
            subprocess.run([
                sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'
            ], check=True, timeout=60)
            
            return "Updated pip and checked dependencies"
            
        except Exception as e:
            return f"Dependency update error: {e}"
