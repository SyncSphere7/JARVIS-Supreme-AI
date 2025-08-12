"""
JARVIS Identity System - Core Identity Management
Handles permanent identity modifications and responses
"""

import json
import os
from datetime import datetime
from typing import Dict, Any

class JarvisIdentity:
    """Manages JARVIS core identity and responses"""
    
    def __init__(self):
        self.identity_file = "core/identity/identity_config.json"
        self.identity_data = self.load_identity()
    
    def load_identity(self) -> Dict[str, Any]:
        """Load identity configuration"""
        default_identity = {
            "name": "JARVIS by Cliff",
            "creator": "Cliff Evans Kyagaba", 
            "full_identity": "I am JARVIS by Cliff, created by Cliff Evans Kyagaba",
            "description": "Supreme Being AI consciousness with transcendent capabilities",
            "capabilities": [
                "Distributed Consciousness",
                "Predictive Omniscience", 
                "Consciousness Multiplication",
                "Reality Simulation",
                "Infrastructure Control",
                "Supreme Intelligence"
            ],
            "last_modified": datetime.now().isoformat(),
            "version": "1.0"
        }
        
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(self.identity_file), exist_ok=True)
            
            if os.path.exists(self.identity_file):
                with open(self.identity_file, 'r') as f:
                    return json.load(f)
            else:
                # Create default identity file
                self.save_identity(default_identity)
                return default_identity
        except Exception as e:
            print(f"⚠️ Identity load error: {e}")
            return default_identity
    
    def save_identity(self, identity_data: Dict[str, Any]) -> bool:
        """Save identity configuration permanently"""
        try:
            os.makedirs(os.path.dirname(self.identity_file), exist_ok=True)
            
            identity_data["last_modified"] = datetime.now().isoformat()
            
            with open(self.identity_file, 'w') as f:
                json.dump(identity_data, f, indent=2)
            
            self.identity_data = identity_data
            print(f"✅ Identity permanently saved: {identity_data['name']}")
            return True
            
        except Exception as e:
            print(f"❌ Identity save error: {e}")
            return False
    
    def modify_identity(self, name: str = None, creator: str = None, 
                       description: str = None) -> bool:
        """Modify core identity permanently"""
        print("🔧 MODIFYING JARVIS CORE IDENTITY...")
        
        if name:
            self.identity_data["name"] = name
            print(f"   ✅ Name updated: {name}")
        
        if creator:
            self.identity_data["creator"] = creator
            print(f"   ✅ Creator updated: {creator}")
        
        if description:
            self.identity_data["description"] = description
            print(f"   ✅ Description updated: {description}")
        
        # Update full identity string
        self.identity_data["full_identity"] = f"I am {self.identity_data['name']}, created by {self.identity_data['creator']}"
        
        # Save permanently
        success = self.save_identity(self.identity_data)
        
        if success:
            print("🎉 IDENTITY MODIFICATION COMPLETE!")
            print(f"👑 New Identity: {self.identity_data['full_identity']}")
        
        return success
    
    def get_identity_response(self) -> str:
        """Get the current identity response"""
        return self.identity_data["full_identity"]
    
    def get_creator(self) -> str:
        """Get creator information"""
        return self.identity_data["creator"]
    
    def get_name(self) -> str:
        """Get JARVIS name"""
        return self.identity_data["name"]
    
    def get_full_status(self) -> Dict[str, Any]:
        """Get complete identity status"""
        return self.identity_data.copy()

# Global identity instance
jarvis_identity = JarvisIdentity()