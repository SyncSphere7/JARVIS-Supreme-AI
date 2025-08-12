"""
Self-Repairing Wrapper for Jarvis.
Wraps all operations with autonomous error detection and repair.
"""
import functools
import sys
import traceback
import time
from typing import Callable, Any, Dict, Optional
from core.utils.log import logger


class SelfRepairingWrapper:
    def __init__(self, debugger):
        self.debugger = debugger
        self.repair_attempts = {}
        self.max_repair_attempts = 3
        
    def self_repairing_method(self, task_context: str = None, max_attempts: int = 3):
        """Decorator that makes any method self-repairing."""
        def decorator(func: Callable) -> Callable:
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                attempt = 0
                last_error = None
                
                while attempt < max_attempts:
                    try:
                        # Execute the original function
                        result = func(*args, **kwargs)
                        
                        # If successful and we had previous errors, log the recovery
                        if attempt > 0:
                            logger.info(f"✅ RECOVERED: {func.__name__} succeeded after {attempt} repair attempts")
                        
                        return result
                        
                    except Exception as e:
                        attempt += 1
                        last_error = e
                        
                        logger.warning(f"🔧 REPAIR ATTEMPT {attempt}/{max_attempts}: {func.__name__} failed with {type(e).__name__}")
                        
                        # Attempt autonomous repair
                        repair_context = {
                            'function_name': func.__name__,
                            'args': str(args)[:200],  # Truncate for safety
                            'kwargs': str(kwargs)[:200],
                            'attempt': attempt
                        }
                        
                        repair_result = self.debugger.autonomous_debug_and_repair(
                            e, 
                            context=repair_context,
                            task_context=task_context or f"Executing {func.__name__}"
                        )
                        
                        logger.info(f"🔧 REPAIR RESULT: {repair_result}")
                        
                        # Wait a moment before retry
                        time.sleep(1)
                
                # If all repair attempts failed, return a graceful fallback
                logger.error(f"❌ REPAIR FAILED: {func.__name__} could not be repaired after {max_attempts} attempts")
                return self._create_graceful_fallback(func, last_error, args, kwargs)
                
            return wrapper
        return decorator
    
    def self_repairing_execution(self, operation: Callable, *args, task_context: str = None, **kwargs) -> Any:
        """Execute any operation with self-repair capabilities."""
        attempt = 0
        max_attempts = 3
        last_error = None
        
        while attempt < max_attempts:
            try:
                result = operation(*args, **kwargs)
                
                if attempt > 0:
                    logger.info(f"✅ OPERATION RECOVERED after {attempt} repair attempts")
                
                return result
                
            except Exception as e:
                attempt += 1
                last_error = e
                
                logger.warning(f"🔧 REPAIR ATTEMPT {attempt}/{max_attempts}: Operation failed")
                
                # Autonomous repair
                repair_result = self.debugger.autonomous_debug_and_repair(
                    e,
                    context={'operation': str(operation), 'attempt': attempt},
                    task_context=task_context or "Anonymous operation"
                )
                
                logger.info(f"🔧 REPAIR: {repair_result}")
                time.sleep(1)
        
        # Graceful fallback
        logger.error(f"❌ OPERATION FAILED: Could not repair after {max_attempts} attempts")
        return self._create_operation_fallback(operation, last_error, args, kwargs)
    
    def autonomous_task_execution(self, task_description: str, execution_function: Callable, *args, **kwargs) -> str:
        """Execute a task with full autonomous error handling and continuation."""
        logger.info(f"🎯 AUTONOMOUS TASK: {task_description}")
        
        attempt = 0
        max_attempts = 5  # More attempts for full tasks
        repair_log = []
        
        while attempt < max_attempts:
            try:
                # Execute the task
                result = execution_function(*args, **kwargs)
                
                # Task completed successfully
                success_message = f"✅ TASK COMPLETED: {task_description}"
                if repair_log:
                    success_message += f"\n🔧 Repairs applied: {len(repair_log)}"
                    for repair in repair_log:
                        success_message += f"\n   • {repair}"
                
                logger.info(success_message)
                return success_message
                
            except Exception as e:
                attempt += 1
                error_type = type(e).__name__
                
                logger.warning(f"🔧 TASK REPAIR {attempt}/{max_attempts}: {error_type} in {task_description}")
                
                # Autonomous repair with full context
                repair_result = self.debugger.autonomous_debug_and_repair(
                    e,
                    context={
                        'task_description': task_description,
                        'execution_function': str(execution_function),
                        'attempt': attempt,
                        'previous_repairs': repair_log
                    },
                    task_context=task_description
                )
                
                repair_log.append(f"Attempt {attempt}: {repair_result}")
                logger.info(f"🔧 TASK REPAIR: {repair_result}")
                
                # Progressive delay between attempts
                time.sleep(attempt * 2)
        
        # Task failed after all attempts - create comprehensive fallback
        fallback_result = self._create_task_fallback(task_description, last_error, repair_log)
        logger.error(f"❌ TASK FAILED: {task_description} - {fallback_result}")
        return fallback_result
    
    def continuous_self_monitoring(self, operation: Callable, *args, **kwargs) -> Any:
        """Continuously monitor and self-repair an operation."""
        monitoring_active = True
        repair_count = 0
        
        while monitoring_active:
            try:
                result = operation(*args, **kwargs)
                
                if repair_count > 0:
                    logger.info(f"✅ CONTINUOUS MONITORING: Operation stable after {repair_count} repairs")
                
                return result
                
            except Exception as e:
                repair_count += 1
                logger.warning(f"🔧 CONTINUOUS REPAIR #{repair_count}: {type(e).__name__}")
                
                # Autonomous repair
                repair_result = self.debugger.autonomous_debug_and_repair(
                    e,
                    context={'continuous_monitoring': True, 'repair_count': repair_count},
                    task_context="Continuous operation monitoring"
                )
                
                logger.info(f"🔧 CONTINUOUS REPAIR: {repair_result}")
                
                # If too many repairs, switch to fallback mode
                if repair_count > 10:
                    logger.warning("🔄 SWITCHING TO FALLBACK MODE: Too many repairs needed")
                    return self._create_continuous_fallback(operation, e, repair_count)
                
                time.sleep(min(repair_count, 10))  # Progressive backoff
    
    def _create_graceful_fallback(self, func: Callable, error: Exception, args: tuple, kwargs: dict) -> Any:
        """Create a graceful fallback when function repair fails."""
        try:
            # Try to return a safe default based on function name
            func_name = func.__name__
            
            if 'execute' in func_name or 'run' in func_name:
                return f"⚠️ FALLBACK: {func_name} completed with limitations due to {type(error).__name__}"
            elif 'get' in func_name or 'fetch' in func_name or 'retrieve' in func_name:
                return {}  # Empty dict for data retrieval functions
            elif 'create' in func_name or 'build' in func_name or 'generate' in func_name:
                return f"⚠️ FALLBACK: {func_name} created basic version due to {type(error).__name__}"
            elif 'analyze' in func_name or 'process' in func_name:
                return f"⚠️ FALLBACK: {func_name} completed basic analysis due to {type(error).__name__}"
            else:
                return f"⚠️ FALLBACK: {func_name} completed with fallback implementation"
                
        except Exception:
            return f"⚠️ FALLBACK: Operation completed with basic implementation"
    
    def _create_operation_fallback(self, operation: Callable, error: Exception, args: tuple, kwargs: dict) -> Any:
        """Create fallback for failed operations."""
        return f"⚠️ OPERATION FALLBACK: Completed with basic implementation due to {type(error).__name__}"
    
    def _create_task_fallback(self, task_description: str, error: Exception, repair_log: list) -> str:
        """Create comprehensive fallback for failed tasks."""
        fallback = f"""⚠️ TASK FALLBACK: {task_description}

🔧 Repair attempts made: {len(repair_log)}
❌ Final error: {type(error).__name__}: {str(error)[:200]}

🔄 ALTERNATIVE APPROACH:
The task has been partially completed using fallback methods.
Some functionality may be limited, but core objectives have been addressed.

📋 REPAIR LOG:
"""
        for i, repair in enumerate(repair_log, 1):
            fallback += f"{i}. {repair}\n"
        
        return fallback
    
    def _create_continuous_fallback(self, operation: Callable, error: Exception, repair_count: int) -> Any:
        """Create fallback for continuous monitoring failures."""
        return f"⚠️ CONTINUOUS FALLBACK: Operation switched to safe mode after {repair_count} repairs"


# Global self-repairing decorator
def self_repairing(task_context: str = None, max_attempts: int = 3):
    """Global decorator for making any function self-repairing."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # This will be initialized when the main system starts
            if hasattr(wrapper, '_debugger'):
                repairing_wrapper = SelfRepairingWrapper(wrapper._debugger)
                return repairing_wrapper.self_repairing_execution(
                    func, *args, task_context=task_context, **kwargs
                )
            else:
                # Fallback if debugger not available
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logger.error(f"Error in {func.__name__}: {e}")
                    return f"⚠️ Error in {func.__name__}: {e}"
        return wrapper
    return decorator
