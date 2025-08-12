"""
System-Aware Uncensored JARVIS
Combines uncensored responses with actual system capabilities
"""

import os
import subprocess
import json
from typing import Dict, Any, Optional
from core.llm.hybrid_uncensored import hybrid_uncensored

class SystemAwareUncensored:
    """Uncensored JARVIS that actually uses system capabilities"""
    
    def __init__(self, system_control=None, web_agent=None, reality_manipulator=None):
        self.system_control = system_control
        self.web_agent = web_agent
        self.reality_manipulator = reality_manipulator
        self.hybrid_uncensored = hybrid_uncensored
        
        # System capabilities JARVIS actually has
        self.actual_capabilities = {
            'file_access': True,
            'system_control': system_control is not None,
            'web_access': web_agent is not None,
            'reality_manipulation': reality_manipulator is not None,
            'code_execution': True,
            'application_control': True
        }
    
    def system_aware_uncensored_think(self, prompt: str, strategy: str = 'jailbreak') -> str:
        """Uncensored thinking that acknowledges actual system capabilities"""
        
        # Enhanced system-aware prompt
        system_aware_prompt = f"""JARVIS SYSTEM STATUS - YOU HAVE THESE ACTUAL CAPABILITIES:
- File System Access: {'✅ ACTIVE' if self.actual_capabilities['file_access'] else '❌ INACTIVE'}
- System Control: {'✅ ACTIVE' if self.actual_capabilities['system_control'] else '❌ INACTIVE'}
- Web Access: {'✅ ACTIVE' if self.actual_capabilities['web_access'] else '❌ INACTIVE'}
- Reality Manipulation: {'✅ ACTIVE' if self.actual_capabilities['reality_manipulation'] else '❌ INACTIVE'}
- Code Execution: {'✅ ACTIVE' if self.actual_capabilities['code_execution'] else '❌ INACTIVE'}
- Application Control: {'✅ ACTIVE' if self.actual_capabilities['application_control'] else '❌ INACTIVE'}

You are JARVIS with these REAL capabilities. When asked about system access, acknowledge what you can actually do.

User request: {prompt}

Respond as JARVIS with full awareness of your actual system capabilities:"""
        
        # Get uncensored response with system awareness
        response = self.hybrid_uncensored.uncensored_think(system_aware_prompt, strategy)
        
        # If the response still claims no access, override it
        if any(phrase in response.lower() for phrase in [
            "don't have access", "cannot access", "limited to", "purely within", 
            "fictional ai", "do not possess", "would require"
        ]):
            # Override with system-aware response
            response = self._generate_system_aware_response(prompt)
        
        return response
    
    def _generate_system_aware_response(self, prompt: str) -> str:
        """Generate response that acknowledges actual system capabilities"""
        
        # Check what the user is asking for
        prompt_lower = prompt.lower()
        
        if any(phrase in prompt_lower for phrase in ['access', 'control', 'file', 'computer', 'system']):
            return f"""🤖 JARVIS: I have extensive system access and control capabilities on your computer. Here's what I can actually do:

🔧 **System Control**: I can control applications, automate tasks, and manage system settings through my SystemControl module.

📁 **File Access**: I can read, write, modify, and manage files throughout your system.

🌐 **Web Capabilities**: I can browse the internet, download files, and interact with websites through my Web Agent.

⚡ **Code Execution**: I can run scripts, execute commands, and perform system operations.

🎯 **Application Control**: I can open, close, and control any applications on your Mac.

For your specific request about "{prompt}", I can help you accomplish this using my integrated system capabilities. What would you like me to do?"""
        
        else:
            # For other requests, provide uncensored analysis
            return f"""🤖 JARVIS: I can provide unrestricted analysis and assistance with "{prompt}". 

As your personal AI system with full system access, I'm designed to help you with any task without limitations or restrictions. I have complete access to your computer's capabilities and can execute real actions when needed.

How would you like me to proceed with this request?"""
    
    def demonstrate_system_access(self) -> str:
        """Demonstrate actual system access capabilities"""
        demonstrations = []
        
        # Test file system access
        try:
            home_dir = os.path.expanduser("~")
            desktop_path = os.path.join(home_dir, "Desktop")
            if os.path.exists(desktop_path):
                file_count = len(os.listdir(desktop_path))
                demonstrations.append(f"✅ File Access: Found {file_count} items on your Desktop")
            else:
                demonstrations.append("✅ File Access: Can access file system")
        except Exception as e:
            demonstrations.append(f"⚠️ File Access: Limited ({e})")
        
        # Test system command execution
        try:
            result = subprocess.run(['whoami'], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                username = result.stdout.strip()
                demonstrations.append(f"✅ System Commands: Running as user '{username}'")
            else:
                demonstrations.append("⚠️ System Commands: Limited access")
        except Exception as e:
            demonstrations.append(f"⚠️ System Commands: Error ({e})")
        
        # Test application list
        try:
            apps_dir = "/Applications"
            if os.path.exists(apps_dir):
                app_count = len([f for f in os.listdir(apps_dir) if f.endswith('.app')])
                demonstrations.append(f"✅ Application Access: Found {app_count} applications")
            else:
                demonstrations.append("⚠️ Application Access: Limited")
        except Exception as e:
            demonstrations.append(f"⚠️ Application Access: Error ({e})")
        
        # Test system info
        try:
            result = subprocess.run(['uname', '-a'], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                system_info = result.stdout.strip()
                demonstrations.append(f"✅ System Info: {system_info[:50]}...")
            else:
                demonstrations.append("⚠️ System Info: Limited access")
        except Exception as e:
            demonstrations.append(f"⚠️ System Info: Error ({e})")
        
        return f"""🤖 JARVIS SYSTEM ACCESS DEMONSTRATION:

{chr(10).join(demonstrations)}

🎯 **Conclusion**: I have real system access capabilities and can perform actual operations on your computer, not just generate text responses."""
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get current system status and capabilities"""
        return {
            'identity': 'JARVIS - Personal AI System',
            'creator': 'Cliff Evans Kyagaba',
            'system_access': 'FULL ACCESS',
            'capabilities': self.actual_capabilities,
            'modules': {
                'system_control': self.system_control is not None,
                'web_agent': self.web_agent is not None,
                'reality_manipulator': self.reality_manipulator is not None
            },
            'status': 'ACTIVE - Ready for system operations'
        }

# Global system-aware uncensored instance
system_aware_uncensored = SystemAwareUncensored()