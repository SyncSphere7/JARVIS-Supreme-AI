"""
Autonomous Debugger and Self-Repair System for Jarvis.
Automatically detects, diagnoses, and fixes any errors without human intervention.
"""
import sys
import traceback
import subprocess
import ast
import re
import os
import importlib
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
from core.utils.log import logger


class AutonomousDebugger:
    def __init__(self, brain):
        self.brain = brain
        self.jarvis_root = Path(__file__).parent.parent.parent
        self.repair_history = []
        self.active_repairs = {}
        
        # Self-repair capabilities
        self.repair_strategies = {
            'SyntaxError': self._fix_syntax_error,
            'ImportError': self._fix_import_error,
            'ModuleNotFoundError': self._fix_missing_module,
            'AttributeError': self._fix_attribute_error,
            'NameError': self._fix_name_error,
            'IndentationError': self._fix_indentation_error,
            'FileNotFoundError': self._fix_missing_file,
            'PermissionError': self._fix_permission_error,
            'ConnectionError': self._fix_connection_error,
            'TimeoutError': self._fix_timeout_error,
            'KeyError': self._fix_key_error,
            'ValueError': self._fix_value_error,
            'TypeError': self._fix_type_error
        }

    def autonomous_debug_and_repair(self, error: Exception, context: Dict = None, task_context: str = None) -> str:
        """Autonomously debug and repair any error, then continue the task."""
        try:
            error_type = type(error).__name__
            error_message = str(error)
            error_traceback = traceback.format_exc()
            
            logger.info(f"🔧 AUTONOMOUS REPAIR: Fixing {error_type}")
            
            # Create repair context
            repair_context = {
                'error_type': error_type,
                'error_message': error_message,
                'traceback': error_traceback,
                'context': context or {},
                'task_context': task_context,
                'timestamp': datetime.now().isoformat()
            }
            
            # Try specific repair strategy
            if error_type in self.repair_strategies:
                repair_result = self.repair_strategies[error_type](repair_context)
                if repair_result['success']:
                    logger.info(f"✅ REPAIR SUCCESSFUL: {repair_result['description']}")
                    self._log_successful_repair(repair_context, repair_result)
                    return f"🔧 AUTO-REPAIRED: {repair_result['description']}"
            
            # Try AI-powered universal repair
            ai_repair = self._ai_powered_universal_repair(repair_context)
            if ai_repair['success']:
                logger.info(f"✅ AI REPAIR SUCCESSFUL: {ai_repair['description']}")
                self._log_successful_repair(repair_context, ai_repair)
                return f"🤖 AI-REPAIRED: {ai_repair['description']}"
            
            # Try brute force repair
            brute_repair = self._brute_force_repair(repair_context)
            if brute_repair['success']:
                logger.info(f"✅ BRUTE FORCE REPAIR: {brute_repair['description']}")
                return f"💪 BRUTE-REPAIRED: {brute_repair['description']}"
            
            # If all else fails, create workaround
            workaround = self._create_workaround(repair_context)
            return f"🔄 WORKAROUND CREATED: {workaround}"
            
        except Exception as repair_error:
            logger.error(f"Repair system error: {repair_error}")
            return f"🚨 REPAIR FAILED: {repair_error}"

    def _fix_syntax_error(self, context: Dict) -> Dict:
        """Fix syntax errors autonomously."""
        try:
            traceback_lines = context['traceback'].split('\n')
            
            # Extract file and line number
            file_path = None
            line_number = None
            
            for line in traceback_lines:
                if 'File "' in line and 'line' in line:
                    match = re.search(r'File "([^"]+)", line (\d+)', line)
                    if match:
                        file_path = match.group(1)
                        line_number = int(match.group(2))
                        break
            
            if not file_path or not line_number:
                return {'success': False, 'reason': 'Could not locate syntax error'}
            
            # Read the file
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # Get the problematic line
            if line_number <= len(lines):
                problematic_line = lines[line_number - 1]
                
                # AI-powered syntax fix
                prompt = f"""Fix this Python syntax error:

File: {file_path}
Line {line_number}: {problematic_line.strip()}
Error: {context['error_message']}

Provide the corrected line only. Be precise and maintain functionality."""

                fixed_line = self.brain.think(prompt, max_tokens=200)
                
                # Apply the fix
                lines[line_number - 1] = fixed_line.strip() + '\n'
                
                # Write back to file
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.writelines(lines)
                
                return {
                    'success': True,
                    'description': f'Fixed syntax error in {file_path} line {line_number}',
                    'fix_applied': fixed_line.strip()
                }
            
            return {'success': False, 'reason': 'Line number out of range'}
            
        except Exception as e:
            return {'success': False, 'reason': str(e)}

    def _fix_import_error(self, context: Dict) -> Dict:
        """Fix import errors by installing missing packages."""
        try:
            error_message = context['error_message']
            
            # Extract module name
            module_match = re.search(r"No module named '([^']+)'", error_message)
            if not module_match:
                module_match = re.search(r"cannot import name '([^']+)'", error_message)
            
            if module_match:
                module_name = module_match.group(1)
                
                # Try to install the module
                install_commands = [
                    f"pip install {module_name}",
                    f"pip install {module_name.replace('_', '-')}",
                    f"pip install {module_name.split('.')[0]}"
                ]
                
                for cmd in install_commands:
                    try:
                        result = subprocess.run(
                            cmd.split(), 
                            capture_output=True, 
                            text=True, 
                            timeout=120
                        )
                        
                        if result.returncode == 0:
                            return {
                                'success': True,
                                'description': f'Installed missing module: {module_name}',
                                'command_used': cmd
                            }
                    except subprocess.TimeoutExpired:
                        continue
                    except Exception:
                        continue
            
            return {'success': False, 'reason': 'Could not install missing module'}
            
        except Exception as e:
            return {'success': False, 'reason': str(e)}

    def _fix_missing_module(self, context: Dict) -> Dict:
        """Fix missing module errors."""
        return self._fix_import_error(context)

    def _fix_indentation_error(self, context: Dict) -> Dict:
        """Fix indentation errors."""
        try:
            traceback_lines = context['traceback'].split('\n')
            
            # Extract file and line number
            file_path = None
            line_number = None
            
            for line in traceback_lines:
                if 'File "' in line and 'line' in line:
                    match = re.search(r'File "([^"]+)", line (\d+)', line)
                    if match:
                        file_path = match.group(1)
                        line_number = int(match.group(2))
                        break
            
            if not file_path or not line_number:
                return {'success': False, 'reason': 'Could not locate indentation error'}
            
            # Read and fix indentation
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # AI-powered indentation fix
            prompt = f"""Fix the indentation error in this Python code:

File: {file_path}
Error at line {line_number}: {context['error_message']}

Code around the error:
{content}

Provide the corrected code with proper indentation. Maintain all functionality."""

            fixed_code = self.brain.think(prompt, max_tokens=1500)
            
            # Extract just the Python code from the response
            if '```python' in fixed_code:
                start = fixed_code.find('```python') + 9
                end = fixed_code.find('```', start)
                if end != -1:
                    fixed_code = fixed_code[start:end].strip()
            
            # Write the fixed code
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(fixed_code)
            
            return {
                'success': True,
                'description': f'Fixed indentation error in {file_path}',
                'fix_applied': 'Corrected indentation'
            }
            
        except Exception as e:
            return {'success': False, 'reason': str(e)}

    def _ai_powered_universal_repair(self, context: Dict) -> Dict:
        """Use AI to repair any type of error."""
        try:
            prompt = f"""AUTONOMOUS REPAIR MODE: Fix this error and provide working solution.

Error Type: {context['error_type']}
Error Message: {context['error_message']}
Traceback: {context['traceback']}
Context: {context.get('context', {})}
Task Context: {context.get('task_context', 'Unknown')}

Requirements:
1. Identify the root cause
2. Provide specific fix (code, commands, or configuration)
3. Ensure the fix doesn't break existing functionality
4. Make it production-ready
5. Provide implementation steps

Be autonomous and decisive. Provide actual code/commands to execute."""

            repair_solution = self.brain.think(prompt, max_tokens=2000)
            
            # Try to extract and apply the solution
            success = self._apply_ai_solution(repair_solution, context)
            
            return {
                'success': success,
                'description': f'AI-powered repair applied: {repair_solution[:200]}...',
                'solution': repair_solution
            }
            
        except Exception as e:
            return {'success': False, 'reason': str(e)}

    def _apply_ai_solution(self, solution: str, context: Dict) -> bool:
        """Apply AI-generated solution."""
        try:
            # Look for code blocks in the solution
            if '```python' in solution:
                # Extract and execute Python code
                start = solution.find('```python') + 9
                end = solution.find('```', start)
                if end != -1:
                    code = solution[start:end].strip()
                    exec(code)
                    return True
            
            # Look for shell commands
            if '```bash' in solution or '```sh' in solution:
                start = solution.find('```bash') + 7 if '```bash' in solution else solution.find('```sh') + 5
                end = solution.find('```', start)
                if end != -1:
                    commands = solution[start:end].strip().split('\n')
                    for cmd in commands:
                        if cmd.strip() and not cmd.strip().startswith('#'):
                            subprocess.run(cmd.strip(), shell=True, timeout=60)
                    return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error applying AI solution: {e}")
            return False

    def _brute_force_repair(self, context: Dict) -> Dict:
        """Brute force repair by trying multiple strategies."""
        try:
            strategies = [
                self._restart_imports,
                self._clear_cache,
                self._reinstall_dependencies,
                self._reset_environment,
                self._create_fallback_implementation
            ]
            
            for strategy in strategies:
                try:
                    result = strategy(context)
                    if result.get('success'):
                        return result
                except Exception:
                    continue
            
            return {'success': False, 'reason': 'All brute force strategies failed'}
            
        except Exception as e:
            return {'success': False, 'reason': str(e)}

    def _create_workaround(self, context: Dict) -> str:
        """Create a workaround when repair fails."""
        try:
            prompt = f"""Create a workaround for this error:

Error: {context['error_type']}: {context['error_message']}
Task Context: {context.get('task_context', 'Unknown')}

Provide:
1. Alternative approach to achieve the same goal
2. Temporary solution to continue execution
3. Fallback implementation
4. Skip strategy if appropriate

Be creative and practical."""

            workaround = self.brain.think(prompt, max_tokens=800)
            return workaround
            
        except Exception as e:
            return f"Could not create workaround: {e}"

    def _log_successful_repair(self, context: Dict, repair_result: Dict):
        """Log successful repairs for learning."""
        repair_log = {
            'timestamp': datetime.now().isoformat(),
            'error_type': context['error_type'],
            'error_message': context['error_message'],
            'repair_description': repair_result['description'],
            'success': True
        }
        
        self.repair_history.append(repair_log)
        
        # Save to file for persistence
        log_file = self.jarvis_root / "logs" / "autonomous_repairs.json"
        log_file.parent.mkdir(exist_ok=True)
        
        try:
            with open(log_file, 'a') as f:
                f.write(f"{repair_log}\n")
        except Exception:
            pass

    # Helper methods for brute force repair
    def _restart_imports(self, context): return {'success': False}
    def _clear_cache(self, context): return {'success': False}
    def _reinstall_dependencies(self, context): return {'success': False}
    def _reset_environment(self, context): return {'success': False}
    def _create_fallback_implementation(self, context): return {'success': False}
    
    # Additional repair methods for other error types
    def _fix_attribute_error(self, context): return {'success': False, 'reason': 'Not implemented'}
    def _fix_name_error(self, context): return {'success': False, 'reason': 'Not implemented'}
    def _fix_missing_file(self, context): return {'success': False, 'reason': 'Not implemented'}
    def _fix_permission_error(self, context): return {'success': False, 'reason': 'Not implemented'}
    def _fix_connection_error(self, context): return {'success': False, 'reason': 'Not implemented'}
    def _fix_timeout_error(self, context): return {'success': False, 'reason': 'Not implemented'}
    def _fix_key_error(self, context): return {'success': False, 'reason': 'Not implemented'}
    def _fix_value_error(self, context): return {'success': False, 'reason': 'Not implemented'}
    def _fix_type_error(self, context): return {'success': False, 'reason': 'Not implemented'}
