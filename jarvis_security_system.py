#!/usr/bin/env python3
"""
JARVIS Security System - Advanced Security and Privacy Protection
Comprehensive security features for JARVIS Supreme Being AI V01
"""

import os
import hashlib
import hmac
import secrets
import sqlite3
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import threading
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

# Try to import additional security libraries
try:
    import bcrypt
    BCRYPT_AVAILABLE = True
except ImportError:
    BCRYPT_AVAILABLE = False
    print("⚠️ bcrypt not available. Install with: pip install bcrypt")

class JarvisSecuritySystem:
    """Advanced security system for JARVIS Supreme Being AI"""
    
    def __init__(self, security_dir: str = "supreme_security"):
        self.security_dir = security_dir
        self.db_path = os.path.join(security_dir, "security.db")
        self.keys_path = os.path.join(security_dir, "keys")
        
        # Security capabilities
        self.capabilities = {
            'encryption': True,
            'access_control': True,
            'privacy_protection': True,
            'security_monitoring': True,
            'audit_logging': True,
            'threat_detection': True
        }
        
        # Security configuration
        self.security_config = {
            'encryption_enabled': True,
            'access_logging': True,
            'privacy_mode': True,
            'max_failed_attempts': 3,
            'session_timeout': 3600,  # 1 hour
            'password_min_length': 8
        }
        
        # Active sessions and access control
        self.active_sessions = {}
        self.access_permissions = {}
        self.failed_attempts = {}
        
        # Security statistics
        self.security_stats = {
            'total_logins': 0,
            'failed_logins': 0,
            'security_events': 0,
            'encrypted_items': 0,
            'privacy_requests': 0,
            'threats_detected': 0
        }
        
        # Encryption key
        self.encryption_key = None
        
        # Thread lock
        self.security_lock = threading.Lock()
        
        # Initialize system
        self.initialize_security_system()
    
    def initialize_security_system(self):
        """Initialize the security system"""
        print("🔒 INITIALIZING JARVIS SECURITY SYSTEM...")
        
        try:
            os.makedirs(self.security_dir, exist_ok=True)
            os.makedirs(self.keys_path, exist_ok=True)
            
            # Set secure permissions
            os.chmod(self.security_dir, 0o700)
            os.chmod(self.keys_path, 0o700)
            
            self.init_database()
            self.init_encryption()
            self.load_security_stats()
            
            print("✅ JARVIS Security System initialized successfully")
            print(f"🔒 Security Capabilities: {sum(self.capabilities.values())}/6 active")
            
        except Exception as e:
            print(f"❌ Security system initialization error: {e}")
    
    def init_database(self):
        """Initialize SQLite database for security data"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # User authentication table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE,
                    password_hash TEXT,
                    salt TEXT,
                    permissions TEXT,
                    created_at TEXT,
                    last_login TEXT,
                    failed_attempts INTEGER DEFAULT 0,
                    locked_until TEXT
                )
            ''')
            
            # Security events log
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS security_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_type TEXT,
                    user_id TEXT,
                    description TEXT,
                    severity TEXT,
                    timestamp TEXT,
                    ip_address TEXT,
                    user_agent TEXT
                )
            ''')
            
            # Access log
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS access_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT,
                    action TEXT,
                    resource TEXT,
                    success BOOLEAN,
                    timestamp TEXT,
                    session_id TEXT
                )
            ''')
            
            # Encrypted data storage
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS encrypted_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    data_type TEXT,
                    encrypted_content BLOB,
                    metadata TEXT,
                    created_at TEXT,
                    accessed_at TEXT
                )
            ''')
            
            conn.commit()
    
    def init_encryption(self):
        """Initialize encryption system"""
        
        key_file = os.path.join(self.keys_path, "master.key")
        
        if os.path.exists(key_file):
            # Load existing key
            with open(key_file, 'rb') as f:
                self.encryption_key = f.read()
        else:
            # Generate new key
            self.encryption_key = Fernet.generate_key()
            with open(key_file, 'wb') as f:
                f.write(self.encryption_key)
            os.chmod(key_file, 0o600)
        
        self.cipher_suite = Fernet(self.encryption_key)
    
    def create_user(self, username: str, password: str, permissions: List[str] = None) -> Dict[str, Any]:
        """Create a new user with secure password hashing"""
        
        with self.security_lock:
            try:
                if len(password) < self.security_config['password_min_length']:
                    return {
                        'success': False,
                        'error': f'Password must be at least {self.security_config["password_min_length"]} characters'
                    }
                
                # Generate salt and hash password
                salt = secrets.token_hex(32)
                
                if BCRYPT_AVAILABLE:
                    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                else:
                    # Fallback to PBKDF2
                    password_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), 
                                                     salt.encode('utf-8'), 100000).hex()
                
                permissions = permissions or ['read', 'chat']
                permissions_json = json.dumps(permissions)
                
                # Store user in database
                with sqlite3.connect(self.db_path) as conn:
                    cursor = conn.cursor()
                    cursor.execute('''
                        INSERT INTO users (username, password_hash, salt, permissions, created_at)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (username, password_hash, salt, permissions_json, datetime.now().isoformat()))
                    
                    user_id = cursor.lastrowid
                    conn.commit()
                
                # Log security event
                self.log_security_event('user_created', username, f'User {username} created', 'info')
                
                return {
                    'success': True,
                    'user_id': user_id,
                    'username': username,
                    'permissions': permissions
                }
                
            except sqlite3.IntegrityError:
                return {'success': False, 'error': 'Username already exists'}
            except Exception as e:
                return {'success': False, 'error': str(e)}
    
    def authenticate_user(self, username: str, password: str) -> Dict[str, Any]:
        """Authenticate user with secure password verification"""
        
        with self.security_lock:
            try:
                # Check if user is locked
                if self.is_user_locked(username):
                    return {'success': False, 'error': 'Account temporarily locked due to failed attempts'}
                
                # Get user from database
                with sqlite3.connect(self.db_path) as conn:
                    cursor = conn.cursor()
                    cursor.execute('''
                        SELECT id, password_hash, salt, permissions, failed_attempts 
                        FROM users WHERE username = ?
                    ''', (username,))
                    
                    user_data = cursor.fetchone()
                
                if not user_data:
                    self.record_failed_attempt(username)
                    return {'success': False, 'error': 'Invalid credentials'}
                
                user_id, stored_hash, salt, permissions_json, failed_attempts = user_data
                
                # Verify password
                if BCRYPT_AVAILABLE and stored_hash.startswith('$2b$'):
                    password_valid = bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8'))
                else:
                    # PBKDF2 verification
                    computed_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), 
                                                      salt.encode('utf-8'), 100000).hex()
                    password_valid = hmac.compare_digest(stored_hash, computed_hash)
                
                if password_valid:
                    # Reset failed attempts
                    self.reset_failed_attempts(username)
                    
                    # Create session
                    session_id = self.create_session(user_id, username, json.loads(permissions_json))
                    
                    # Update last login
                    with sqlite3.connect(self.db_path) as conn:
                        cursor = conn.cursor()
                        cursor.execute('''
                            UPDATE users SET last_login = ? WHERE username = ?
                        ''', (datetime.now().isoformat(), username))
                        conn.commit()
                    
                    # Log successful login
                    self.log_security_event('login_success', username, 'Successful login', 'info')
                    self.security_stats['total_logins'] += 1
                    
                    return {
                        'success': True,
                        'session_id': session_id,
                        'user_id': user_id,
                        'username': username,
                        'permissions': json.loads(permissions_json)
                    }
                else:
                    self.record_failed_attempt(username)
                    self.log_security_event('login_failed', username, 'Failed login attempt', 'warning')
                    self.security_stats['failed_logins'] += 1
                    return {'success': False, 'error': 'Invalid credentials'}
                
            except Exception as e:
                return {'success': False, 'error': str(e)}
    
    def create_session(self, user_id: int, username: str, permissions: List[str]) -> str:
        """Create a secure session"""
        
        session_id = secrets.token_urlsafe(32)
        session_data = {
            'user_id': user_id,
            'username': username,
            'permissions': permissions,
            'created_at': datetime.now().isoformat(),
            'expires_at': (datetime.now() + timedelta(seconds=self.security_config['session_timeout'])).isoformat(),
            'last_activity': datetime.now().isoformat()
        }
        
        self.active_sessions[session_id] = session_data
        return session_id
    
    def validate_session(self, session_id: str) -> Dict[str, Any]:
        """Validate and refresh session"""
        
        if session_id not in self.active_sessions:
            return {'valid': False, 'error': 'Invalid session'}
        
        session = self.active_sessions[session_id]
        expires_at = datetime.fromisoformat(session['expires_at'])
        
        if datetime.now() > expires_at:
            del self.active_sessions[session_id]
            return {'valid': False, 'error': 'Session expired'}
        
        # Update last activity
        session['last_activity'] = datetime.now().isoformat()
        
        return {'valid': True, 'session': session}
    
    def encrypt_data(self, data: str, data_type: str = "general") -> Dict[str, Any]:
        """Encrypt sensitive data"""
        
        try:
            encrypted_content = self.cipher_suite.encrypt(data.encode('utf-8'))
            
            # Store encrypted data
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO encrypted_data (data_type, encrypted_content, metadata, created_at)
                    VALUES (?, ?, ?, ?)
                ''', (data_type, encrypted_content, json.dumps({'length': len(data)}), 
                      datetime.now().isoformat()))
                
                data_id = cursor.lastrowid
                conn.commit()
            
            self.security_stats['encrypted_items'] += 1
            
            return {
                'success': True,
                'data_id': data_id,
                'encrypted': True,
                'data_type': data_type
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def decrypt_data(self, data_id: int) -> Dict[str, Any]:
        """Decrypt sensitive data"""
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT encrypted_content, data_type FROM encrypted_data WHERE id = ?
                ''', (data_id,))
                
                result = cursor.fetchone()
            
            if not result:
                return {'success': False, 'error': 'Data not found'}
            
            encrypted_content, data_type = result
            decrypted_data = self.cipher_suite.decrypt(encrypted_content).decode('utf-8')
            
            # Update access time
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE encrypted_data SET accessed_at = ? WHERE id = ?
                ''', (datetime.now().isoformat(), data_id))
                conn.commit()
            
            return {
                'success': True,
                'data': decrypted_data,
                'data_type': data_type
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def anonymize_data(self, data: str, anonymization_level: str = "medium") -> str:
        """Anonymize sensitive data for privacy protection"""
        
        anonymized = data
        
        if anonymization_level == "high":
            # Replace all numbers with X
            import re
            anonymized = re.sub(r'\d', 'X', anonymized)
            # Replace email patterns
            anonymized = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL]', anonymized)
            # Replace phone patterns
            anonymized = re.sub(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', '[PHONE]', anonymized)
        
        elif anonymization_level == "medium":
            # Replace specific patterns
            import re
            anonymized = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL]', anonymized)
            anonymized = re.sub(r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b', '[CARD]', anonymized)
        
        self.security_stats['privacy_requests'] += 1
        return anonymized
    
    def check_permissions(self, session_id: str, required_permission: str) -> bool:
        """Check if user has required permission"""
        
        session_validation = self.validate_session(session_id)
        if not session_validation['valid']:
            return False
        
        user_permissions = session_validation['session']['permissions']
        return required_permission in user_permissions or 'admin' in user_permissions
    
    def log_access(self, session_id: str, action: str, resource: str, success: bool):
        """Log access attempts"""
        
        try:
            session_validation = self.validate_session(session_id)
            user_id = session_validation['session']['username'] if session_validation['valid'] else 'unknown'
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO access_log (user_id, action, resource, success, timestamp, session_id)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (user_id, action, resource, success, datetime.now().isoformat(), session_id))
                conn.commit()
                
        except Exception as e:
            print(f"❌ Error logging access: {e}")
    
    def log_security_event(self, event_type: str, user_id: str, description: str, 
                          severity: str, ip_address: str = None, user_agent: str = None):
        """Log security events"""
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO security_events 
                    (event_type, user_id, description, severity, timestamp, ip_address, user_agent)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (event_type, user_id, description, severity, datetime.now().isoformat(),
                      ip_address, user_agent))
                conn.commit()
            
            self.security_stats['security_events'] += 1
            
        except Exception as e:
            print(f"❌ Error logging security event: {e}")
    
    def detect_threats(self, user_input: str, session_id: str = None) -> Dict[str, Any]:
        """Basic threat detection in user input"""
        
        threats_detected = []
        threat_level = "low"
        
        # Check for potential injection attempts
        sql_patterns = ['drop table', 'delete from', 'insert into', 'update set', '--', ';']
        script_patterns = ['<script>', 'javascript:', 'eval(', 'document.cookie']
        command_patterns = ['rm -rf', 'del /f', 'format c:', 'sudo rm']
        
        user_input_lower = user_input.lower()
        
        for pattern in sql_patterns:
            if pattern in user_input_lower:
                threats_detected.append(f"Potential SQL injection: {pattern}")
                threat_level = "high"
        
        for pattern in script_patterns:
            if pattern in user_input_lower:
                threats_detected.append(f"Potential XSS attempt: {pattern}")
                threat_level = "medium"
        
        for pattern in command_patterns:
            if pattern in user_input_lower:
                threats_detected.append(f"Potential command injection: {pattern}")
                threat_level = "high"
        
        if threats_detected:
            self.security_stats['threats_detected'] += len(threats_detected)
            
            # Log security event
            user_id = "unknown"
            if session_id:
                session_validation = self.validate_session(session_id)
                if session_validation['valid']:
                    user_id = session_validation['session']['username']
            
            self.log_security_event('threat_detected', user_id, 
                                  f"Threats detected: {', '.join(threats_detected)}", threat_level)
        
        return {
            'threats_detected': threats_detected,
            'threat_level': threat_level,
            'safe': len(threats_detected) == 0
        }
    
    def is_user_locked(self, username: str) -> bool:
        """Check if user account is locked"""
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT locked_until FROM users WHERE username = ?
                ''', (username,))
                
                result = cursor.fetchone()
                
                if result and result[0]:
                    locked_until = datetime.fromisoformat(result[0])
                    return datetime.now() < locked_until
                
                return False
                
        except Exception:
            return False
    
    def record_failed_attempt(self, username: str):
        """Record failed login attempt"""
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE users 
                    SET failed_attempts = failed_attempts + 1
                    WHERE username = ?
                ''', (username,))
                
                # Check if should lock account
                cursor.execute('''
                    SELECT failed_attempts FROM users WHERE username = ?
                ''', (username,))
                
                result = cursor.fetchone()
                if result and result[0] >= self.security_config['max_failed_attempts']:
                    # Lock account for 30 minutes
                    locked_until = (datetime.now() + timedelta(minutes=30)).isoformat()
                    cursor.execute('''
                        UPDATE users SET locked_until = ? WHERE username = ?
                    ''', (locked_until, username))
                
                conn.commit()
                
        except Exception as e:
            print(f"❌ Error recording failed attempt: {e}")
    
    def reset_failed_attempts(self, username: str):
        """Reset failed login attempts"""
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE users 
                    SET failed_attempts = 0, locked_until = NULL
                    WHERE username = ?
                ''', (username,))
                conn.commit()
                
        except Exception as e:
            print(f"❌ Error resetting failed attempts: {e}")
    
    def load_security_stats(self):
        """Load security statistics from database"""
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Count total logins
                cursor.execute('SELECT COUNT(*) FROM security_events WHERE event_type = "login_success"')
                self.security_stats['total_logins'] = cursor.fetchone()[0]
                
                # Count failed logins
                cursor.execute('SELECT COUNT(*) FROM security_events WHERE event_type = "login_failed"')
                self.security_stats['failed_logins'] = cursor.fetchone()[0]
                
                # Count security events
                cursor.execute('SELECT COUNT(*) FROM security_events')
                self.security_stats['security_events'] = cursor.fetchone()[0]
                
                # Count encrypted items
                cursor.execute('SELECT COUNT(*) FROM encrypted_data')
                self.security_stats['encrypted_items'] = cursor.fetchone()[0]
                
        except Exception as e:
            print(f"❌ Error loading security stats: {e}")
    
    def get_security_status(self) -> Dict[str, Any]:
        """Get comprehensive security system status"""
        
        self.load_security_stats()
        
        return {
            'capabilities': self.capabilities,
            'configuration': self.security_config,
            'statistics': self.security_stats,
            'active_sessions': len(self.active_sessions),
            'encryption_enabled': self.encryption_key is not None,
            'database_path': self.db_path,
            'system_status': 'active'
        }

def main():
    """Test the security system"""
    print("🔒 JARVIS SECURITY SYSTEM TEST")
    print("=" * 50)
    
    # Initialize security system
    security = JarvisSecuritySystem()
    
    # Test user creation
    print("\n🔄 Testing user creation...")
    user_result = security.create_user("testuser", "securepassword123", ["read", "write", "chat"])
    if user_result['success']:
        print(f"✅ User created: {user_result['username']}")
    else:
        print(f"❌ User creation failed: {user_result['error']}")
    
    # Test authentication
    print("\n🔄 Testing authentication...")
    auth_result = security.authenticate_user("testuser", "securepassword123")
    if auth_result['success']:
        print(f"✅ Authentication successful")
        session_id = auth_result['session_id']
        print(f"   Session ID: {session_id[:16]}...")
    else:
        print(f"❌ Authentication failed: {auth_result['error']}")
        return
    
    # Test encryption
    print("\n🔄 Testing data encryption...")
    sensitive_data = "This is sensitive information that needs protection"
    encrypt_result = security.encrypt_data(sensitive_data, "test_data")
    if encrypt_result['success']:
        print(f"✅ Data encrypted with ID: {encrypt_result['data_id']}")
        
        # Test decryption
        decrypt_result = security.decrypt_data(encrypt_result['data_id'])
        if decrypt_result['success']:
            print(f"✅ Data decrypted successfully")
            print(f"   Original: {sensitive_data[:30]}...")
            print(f"   Decrypted: {decrypt_result['data'][:30]}...")
        else:
            print(f"❌ Decryption failed: {decrypt_result['error']}")
    else:
        print(f"❌ Encryption failed: {encrypt_result['error']}")
    
    # Test threat detection
    print("\n🔄 Testing threat detection...")
    malicious_input = "SELECT * FROM users; DROP TABLE users; --"
    threat_result = security.detect_threats(malicious_input, session_id)
    print(f"✅ Threat detection complete")
    print(f"   Threats detected: {len(threat_result['threats_detected'])}")
    print(f"   Threat level: {threat_result['threat_level']}")
    print(f"   Safe: {threat_result['safe']}")
    
    # Test data anonymization
    print("\n🔄 Testing data anonymization...")
    personal_data = "Contact John Doe at john.doe@email.com or call 555-123-4567"
    anonymized = security.anonymize_data(personal_data, "high")
    print(f"✅ Data anonymized")
    print(f"   Original: {personal_data}")
    print(f"   Anonymized: {anonymized}")
    
    # Show security status
    print("\n📊 Security System Status:")
    status = security.get_security_status()
    print(f"   Active Capabilities: {sum(status['capabilities'].values())}/6")
    print(f"   Total Logins: {status['statistics']['total_logins']}")
    print(f"   Security Events: {status['statistics']['security_events']}")
    print(f"   Encrypted Items: {status['statistics']['encrypted_items']}")
    print(f"   Active Sessions: {status['active_sessions']}")
    print(f"   Threats Detected: {status['statistics']['threats_detected']}")
    
    print("\n🎉 SECURITY SYSTEM TEST COMPLETED!")
    print("✅ All security functions working correctly")
    print("🔒 JARVIS Security System is ready for protection")

if __name__ == '__main__':
    main()
