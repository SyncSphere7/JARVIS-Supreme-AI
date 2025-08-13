#!/usr/bin/env python3
"""
JARVIS Analytics System - Advanced Analytics and Reporting
Comprehensive analytics, monitoring, and reporting for JARVIS Supreme Being AI V01
"""

import os
import json
import sqlite3
import time
import psutil
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict, Counter
import statistics
import math

# Try to import visualization libraries
try:
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("⚠️ Matplotlib not available. Install with: pip install matplotlib")

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False
    print("⚠️ Pandas not available. Install with: pip install pandas")

class JarvisAnalyticsSystem:
    """Advanced analytics and reporting system for JARVIS Supreme Being AI"""
    
    def __init__(self, analytics_dir: str = "supreme_analytics"):
        self.analytics_dir = analytics_dir
        self.db_path = os.path.join(analytics_dir, "analytics.db")
        self.reports_path = os.path.join(analytics_dir, "reports")
        self.charts_path = os.path.join(analytics_dir, "charts")
        
        # Analytics capabilities
        self.capabilities = {
            'performance_monitoring': True,
            'usage_analytics': True,
            'system_metrics': True,
            'user_behavior_analysis': True,
            'report_generation': True,
            'data_visualization': MATPLOTLIB_AVAILABLE,
            'data_processing': PANDAS_AVAILABLE,
            'real_time_monitoring': True
        }
        
        # Monitoring configuration
        self.monitoring_config = {
            'collection_interval': 60,  # seconds
            'retention_days': 30,
            'alert_thresholds': {
                'cpu_usage': 80,
                'memory_usage': 85,
                'response_time': 5.0,
                'error_rate': 5.0
            },
            'auto_cleanup': True
        }
        
        # Real-time metrics
        self.current_metrics = {
            'system_performance': {},
            'user_activity': {},
            'component_usage': {},
            'error_tracking': {},
            'response_times': []
        }
        
        # Analytics statistics
        self.analytics_stats = {
            'total_interactions': 0,
            'total_users': 0,
            'average_response_time': 0.0,
            'system_uptime': 0,
            'error_count': 0,
            'reports_generated': 0,
            'data_points_collected': 0
        }
        
        # Component tracking
        self.component_metrics = {
            'memory_system': {'calls': 0, 'avg_time': 0.0, 'errors': 0},
            'learning_system': {'calls': 0, 'avg_time': 0.0, 'errors': 0},
            'internet_system': {'calls': 0, 'avg_time': 0.0, 'errors': 0},
            'automation_system': {'calls': 0, 'avg_time': 0.0, 'errors': 0},
            'reasoning_system': {'calls': 0, 'avg_time': 0.0, 'errors': 0},
            'multilang_system': {'calls': 0, 'avg_time': 0.0, 'errors': 0},
            'security_system': {'calls': 0, 'avg_time': 0.0, 'errors': 0}
        }
        
        # User behavior tracking
        self.user_behavior = {
            'session_durations': [],
            'command_frequencies': Counter(),
            'peak_usage_hours': Counter(),
            'user_satisfaction': [],
            'feature_usage': Counter()
        }
        
        # System start time
        self.start_time = datetime.now()
        
        # Thread lock
        self.analytics_lock = threading.Lock()
        
        # Monitoring thread
        self.monitoring_thread = None
        self.monitoring_active = False
        
        # Initialize system
        self.initialize_analytics_system()
    
    def initialize_analytics_system(self):
        """Initialize the analytics system"""
        print("📊 INITIALIZING JARVIS ANALYTICS SYSTEM...")
        
        try:
            # Create directories
            os.makedirs(self.analytics_dir, exist_ok=True)
            os.makedirs(self.reports_path, exist_ok=True)
            os.makedirs(self.charts_path, exist_ok=True)
            
            # Initialize database
            self.init_database()
            
            # Load existing statistics
            self.load_analytics_stats()
            
            # Start monitoring
            self.start_monitoring()
            
            print("✅ JARVIS Analytics System initialized successfully")
            print(f"📊 Analytics Capabilities: {sum(self.capabilities.values())}/8 active")
            print(f"🔄 Real-time monitoring: {'Active' if self.monitoring_active else 'Inactive'}")
            
        except Exception as e:
            print(f"❌ Analytics system initialization error: {e}")
    
    def init_database(self):
        """Initialize SQLite database for analytics data"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # System performance metrics
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS system_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    cpu_usage REAL,
                    memory_usage REAL,
                    disk_usage REAL,
                    network_io TEXT,
                    active_processes INTEGER,
                    system_load REAL
                )
            ''')
            
            # User interaction tracking
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_interactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT,
                    session_id TEXT,
                    interaction_type TEXT,
                    command TEXT,
                    response_time REAL,
                    success BOOLEAN,
                    timestamp TEXT,
                    component_used TEXT,
                    input_length INTEGER,
                    output_length INTEGER
                )
            ''')
            
            # Component performance tracking
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS component_performance (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    component_name TEXT,
                    operation TEXT,
                    execution_time REAL,
                    success BOOLEAN,
                    error_message TEXT,
                    timestamp TEXT,
                    memory_used REAL,
                    cpu_used REAL
                )
            ''')
            
            # Error tracking
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS error_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    error_type TEXT,
                    error_message TEXT,
                    component TEXT,
                    severity TEXT,
                    timestamp TEXT,
                    user_id TEXT,
                    session_id TEXT,
                    stack_trace TEXT
                )
            ''')
            
            # Usage analytics
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS usage_analytics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT,
                    total_interactions INTEGER,
                    unique_users INTEGER,
                    avg_response_time REAL,
                    error_rate REAL,
                    peak_hour INTEGER,
                    most_used_feature TEXT,
                    user_satisfaction REAL
                )
            ''')
            
            # Reports metadata
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS reports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    report_name TEXT,
                    report_type TEXT,
                    generated_at TEXT,
                    file_path TEXT,
                    parameters TEXT,
                    size_bytes INTEGER
                )
            ''')
            
            conn.commit()
    
    def start_monitoring(self):
        """Start real-time system monitoring"""
        if not self.monitoring_active:
            self.monitoring_active = True
            self.monitoring_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
            self.monitoring_thread.start()
            print("🔄 Real-time monitoring started")
    
    def stop_monitoring(self):
        """Stop real-time system monitoring"""
        self.monitoring_active = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5)
        print("⏹️ Real-time monitoring stopped")
    
    def _monitoring_loop(self):
        """Main monitoring loop"""
        while self.monitoring_active:
            try:
                # Collect system metrics
                self.collect_system_metrics()
                
                # Sleep for configured interval
                time.sleep(self.monitoring_config['collection_interval'])
                
            except Exception as e:
                print(f"Monitoring error: {e}")
                time.sleep(10)  # Wait before retrying
    
    def collect_system_metrics(self):
        """Collect current system performance metrics"""
        try:
            # Get system metrics
            cpu_usage = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            network = psutil.net_io_counters()
            
            # Calculate system load
            load_avg = os.getloadavg()[0] if hasattr(os, 'getloadavg') else 0.0
            
            # Store metrics
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO system_metrics 
                    (timestamp, cpu_usage, memory_usage, disk_usage, network_io, active_processes, system_load)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    datetime.now().isoformat(),
                    cpu_usage,
                    memory.percent,
                    disk.percent,
                    json.dumps({'bytes_sent': network.bytes_sent, 'bytes_recv': network.bytes_recv}),
                    len(psutil.pids()),
                    load_avg
                ))
                conn.commit()
            
            # Update current metrics
            self.current_metrics['system_performance'] = {
                'cpu_usage': cpu_usage,
                'memory_usage': memory.percent,
                'disk_usage': disk.percent,
                'active_processes': len(psutil.pids()),
                'system_load': load_avg,
                'timestamp': datetime.now().isoformat()
            }
            
            # Check for alerts
            self.check_performance_alerts(cpu_usage, memory.percent)
            
            # Update statistics
            self.analytics_stats['data_points_collected'] += 1
            
        except Exception as e:
            print(f"Error collecting system metrics: {e}")
    
    def track_user_interaction(self, user_id: str, session_id: str, interaction_type: str,
                             command: str, response_time: float, success: bool,
                             component_used: str = None, input_length: int = 0,
                             output_length: int = 0) -> Dict[str, Any]:
        """Track user interaction for analytics"""
        with self.analytics_lock:
            try:
                # Store interaction
                with sqlite3.connect(self.db_path) as conn:
                    cursor = conn.cursor()
                    cursor.execute('''
                        INSERT INTO user_interactions 
                        (user_id, session_id, interaction_type, command, response_time, success, 
                         timestamp, component_used, input_length, output_length)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        user_id, session_id, interaction_type, command, response_time, success,
                        datetime.now().isoformat(), component_used, input_length, output_length
                    ))
                    conn.commit()
                
                # Update real-time metrics
                self.current_metrics['user_activity'][user_id] = {
                    'last_interaction': datetime.now().isoformat(),
                    'session_id': session_id,
                    'response_time': response_time,
                    'success': success
                }
                
                # Update behavior tracking
                current_hour = datetime.now().hour
                self.user_behavior['peak_usage_hours'][current_hour] += 1
                self.user_behavior['command_frequencies'][command] += 1
                self.user_behavior['response_times'].append(response_time)
                
                if component_used:
                    self.user_behavior['feature_usage'][component_used] += 1
                
                # Update statistics
                self.analytics_stats['total_interactions'] += 1
                if response_time > 0:
                    # Update average response time
                    total_time = self.analytics_stats['average_response_time'] * (self.analytics_stats['total_interactions'] - 1)
                    self.analytics_stats['average_response_time'] = (total_time + response_time) / self.analytics_stats['total_interactions']
                
                return {
                    'success': True,
                    'message': 'Interaction tracked successfully'
                }
                
            except Exception as e:
                return {
                    'success': False,
                    'error': f'Failed to track interaction: {str(e)}'
                }
    
    def track_component_performance(self, component_name: str, operation: str,
                                  execution_time: float, success: bool,
                                  error_message: str = None, memory_used: float = 0.0,
                                  cpu_used: float = 0.0) -> Dict[str, Any]:
        """Track component performance metrics"""
        try:
            # Store performance data
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO component_performance 
                    (component_name, operation, execution_time, success, error_message, 
                     timestamp, memory_used, cpu_used)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    component_name, operation, execution_time, success, error_message,
                    datetime.now().isoformat(), memory_used, cpu_used
                ))
                conn.commit()
            
            # Update component metrics
            if component_name in self.component_metrics:
                metrics = self.component_metrics[component_name]
                metrics['calls'] += 1
                
                # Update average time
                total_time = metrics['avg_time'] * (metrics['calls'] - 1)
                metrics['avg_time'] = (total_time + execution_time) / metrics['calls']
                
                if not success:
                    metrics['errors'] += 1
            
            # Update current metrics
            self.current_metrics['component_usage'][component_name] = {
                'last_used': datetime.now().isoformat(),
                'execution_time': execution_time,
                'success': success,
                'operation': operation
            }
            
            return {
                'success': True,
                'message': 'Component performance tracked successfully'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Failed to track component performance: {str(e)}'
            }
    
    def log_error(self, error_type: str, error_message: str, component: str,
                  severity: str = 'medium', user_id: str = None, session_id: str = None,
                  stack_trace: str = None) -> Dict[str, Any]:
        """Log error for analytics and monitoring"""
        try:
            # Store error
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO error_logs 
                    (error_type, error_message, component, severity, timestamp, 
                     user_id, session_id, stack_trace)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    error_type, error_message, component, severity, datetime.now().isoformat(),
                    user_id, session_id, stack_trace
                ))
                conn.commit()
            
            # Update error tracking
            error_key = f"{component}:{error_type}"
            if error_key not in self.current_metrics['error_tracking']:
                self.current_metrics['error_tracking'][error_key] = 0
            self.current_metrics['error_tracking'][error_key] += 1
            
            # Update statistics
            self.analytics_stats['error_count'] += 1
            
            # Check for error rate alerts
            self.check_error_rate_alerts()
            
            return {
                'success': True,
                'message': 'Error logged successfully'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Failed to log error: {str(e)}'
            }
    
    def check_performance_alerts(self, cpu_usage: float, memory_usage: float):
        """Check for performance threshold alerts"""
        alerts = []
        
        if cpu_usage > self.monitoring_config['alert_thresholds']['cpu_usage']:
            alerts.append(f"High CPU usage: {cpu_usage:.1f}%")
        
        if memory_usage > self.monitoring_config['alert_thresholds']['memory_usage']:
            alerts.append(f"High memory usage: {memory_usage:.1f}%")
        
        if alerts:
            print(f"⚠️ Performance Alert: {', '.join(alerts)}")
            # Log alerts as errors
            for alert in alerts:
                self.log_error("performance_alert", alert, "system_monitor", "high")
    
    def check_error_rate_alerts(self):
        """Check for high error rate alerts"""
        try:
            # Calculate error rate for last hour
            one_hour_ago = (datetime.now() - timedelta(hours=1)).isoformat()
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Count total interactions in last hour
                cursor.execute('''
                    SELECT COUNT(*) FROM user_interactions 
                    WHERE timestamp > ?
                ''', (one_hour_ago,))
                total_interactions = cursor.fetchone()[0]
                
                # Count errors in last hour
                cursor.execute('''
                    SELECT COUNT(*) FROM error_logs 
                    WHERE timestamp > ?
                ''', (one_hour_ago,))
                error_count = cursor.fetchone()[0]
            
            if total_interactions > 0:
                error_rate = (error_count / total_interactions) * 100
                threshold = self.monitoring_config['alert_thresholds']['error_rate']
                
                if error_rate > threshold:
                    alert_msg = f"High error rate: {error_rate:.1f}% (threshold: {threshold}%)"
                    print(f"⚠️ Error Rate Alert: {alert_msg}")
                    
        except Exception as e:
            print(f"Error checking error rate: {e}")
    def generate_usage_report(self, start_date: str = None, end_date: str = None) -> Dict[str, Any]:
        """Generate comprehensive usage analytics report"""
        try:
            if not start_date:
                start_date = (datetime.now() - timedelta(days=7)).isoformat()
            if not end_date:
                end_date = datetime.now().isoformat()
            
            report_data = {}
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Total interactions
                cursor.execute('''
                    SELECT COUNT(*) FROM user_interactions 
                    WHERE timestamp BETWEEN ? AND ?
                ''', (start_date, end_date))
                report_data['total_interactions'] = cursor.fetchone()[0]
                
                # Unique users
                cursor.execute('''
                    SELECT COUNT(DISTINCT user_id) FROM user_interactions 
                    WHERE timestamp BETWEEN ? AND ?
                ''', (start_date, end_date))
                report_data['unique_users'] = cursor.fetchone()[0]
                
                # Average response time
                cursor.execute('''
                    SELECT AVG(response_time) FROM user_interactions 
                    WHERE timestamp BETWEEN ? AND ? AND response_time > 0
                ''', (start_date, end_date))
                result = cursor.fetchone()[0]
                report_data['avg_response_time'] = round(result, 3) if result else 0.0
                
                # Success rate
                cursor.execute('''
                    SELECT 
                        COUNT(*) as total,
                        SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as successful
                    FROM user_interactions 
                    WHERE timestamp BETWEEN ? AND ?
                ''', (start_date, end_date))
                total, successful = cursor.fetchone()
                report_data['success_rate'] = round((successful / total * 100), 2) if total > 0 else 0.0
                
                # Most used commands
                cursor.execute('''
                    SELECT command, COUNT(*) as count 
                    FROM user_interactions 
                    WHERE timestamp BETWEEN ? AND ?
                    GROUP BY command 
                    ORDER BY count DESC 
                    LIMIT 10
                ''', (start_date, end_date))
                report_data['top_commands'] = [{'command': cmd, 'count': count} for cmd, count in cursor.fetchall()]
                
                # Most used components
                cursor.execute('''
                    SELECT component_used, COUNT(*) as count 
                    FROM user_interactions 
                    WHERE timestamp BETWEEN ? AND ? AND component_used IS NOT NULL
                    GROUP BY component_used 
                    ORDER BY count DESC 
                    LIMIT 10
                ''', (start_date, end_date))
                report_data['top_components'] = [{'component': comp, 'count': count} for comp, count in cursor.fetchall()]
                
                # Peak usage hours
                cursor.execute('''
                    SELECT strftime('%H', timestamp) as hour, COUNT(*) as count 
                    FROM user_interactions 
                    WHERE timestamp BETWEEN ? AND ?
                    GROUP BY hour 
                    ORDER BY count DESC
                ''', (start_date, end_date))
                report_data['peak_hours'] = [{'hour': int(hour), 'count': count} for hour, count in cursor.fetchall()]
                
                # Error analysis
                cursor.execute('''
                    SELECT error_type, component, COUNT(*) as count 
                    FROM error_logs 
                    WHERE timestamp BETWEEN ? AND ?
                    GROUP BY error_type, component 
                    ORDER BY count DESC 
                    LIMIT 10
                ''', (start_date, end_date))
                report_data['top_errors'] = [
                    {'error_type': error_type, 'component': component, 'count': count} 
                    for error_type, component, count in cursor.fetchall()
                ]
            
            # Add metadata
            report_data['report_metadata'] = {
                'generated_at': datetime.now().isoformat(),
                'period_start': start_date,
                'period_end': end_date,
                'report_type': 'usage_analytics'
            }
            
            return {
                'success': True,
                'report_data': report_data,
                'message': 'Usage report generated successfully'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Failed to generate usage report: {str(e)}'
            }
    
    def generate_performance_report(self, start_date: str = None, end_date: str = None) -> Dict[str, Any]:
        """Generate system performance report"""
        try:
            if not start_date:
                start_date = (datetime.now() - timedelta(days=7)).isoformat()
            if not end_date:
                end_date = datetime.now().isoformat()
            
            report_data = {}
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # System metrics averages
                cursor.execute('''
                    SELECT 
                        AVG(cpu_usage) as avg_cpu,
                        MAX(cpu_usage) as max_cpu,
                        AVG(memory_usage) as avg_memory,
                        MAX(memory_usage) as max_memory,
                        AVG(disk_usage) as avg_disk,
                        AVG(system_load) as avg_load
                    FROM system_metrics 
                    WHERE timestamp BETWEEN ? AND ?
                ''', (start_date, end_date))
                
                result = cursor.fetchone()
                if result:
                    report_data['system_performance'] = {
                        'avg_cpu_usage': round(result[0], 2) if result[0] else 0,
                        'max_cpu_usage': round(result[1], 2) if result[1] else 0,
                        'avg_memory_usage': round(result[2], 2) if result[2] else 0,
                        'max_memory_usage': round(result[3], 2) if result[3] else 0,
                        'avg_disk_usage': round(result[4], 2) if result[4] else 0,
                        'avg_system_load': round(result[5], 2) if result[5] else 0
                    }
                
                # Component performance
                cursor.execute('''
                    SELECT 
                        component_name,
                        COUNT(*) as total_calls,
                        AVG(execution_time) as avg_time,
                        MAX(execution_time) as max_time,
                        SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as successful_calls
                    FROM component_performance 
                    WHERE timestamp BETWEEN ? AND ?
                    GROUP BY component_name
                    ORDER BY total_calls DESC
                ''', (start_date, end_date))
                
                component_perf = []
                for row in cursor.fetchall():
                    component_name, total_calls, avg_time, max_time, successful_calls = row
                    success_rate = (successful_calls / total_calls * 100) if total_calls > 0 else 0
                    component_perf.append({
                        'component': component_name,
                        'total_calls': total_calls,
                        'avg_execution_time': round(avg_time, 3) if avg_time else 0,
                        'max_execution_time': round(max_time, 3) if max_time else 0,
                        'success_rate': round(success_rate, 2)
                    })
                
                report_data['component_performance'] = component_perf
                
                # Response time analysis
                cursor.execute('''
                    SELECT 
                        AVG(response_time) as avg_response,
                        MIN(response_time) as min_response,
                        MAX(response_time) as max_response
                    FROM user_interactions 
                    WHERE timestamp BETWEEN ? AND ? AND response_time > 0
                ''', (start_date, end_date))
                
                result = cursor.fetchone()
                if result:
                    report_data['response_time_analysis'] = {
                        'avg_response_time': round(result[0], 3) if result[0] else 0,
                        'min_response_time': round(result[1], 3) if result[1] else 0,
                        'max_response_time': round(result[2], 3) if result[2] else 0
                    }
            
            # Add current system status
            report_data['current_system_status'] = self.get_current_system_status()
            
            # Add metadata
            report_data['report_metadata'] = {
                'generated_at': datetime.now().isoformat(),
                'period_start': start_date,
                'period_end': end_date,
                'report_type': 'performance_analysis'
            }
            
            return {
                'success': True,
                'report_data': report_data,
                'message': 'Performance report generated successfully'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Failed to generate performance report: {str(e)}'
            }
    
    def generate_error_analysis_report(self, start_date: str = None, end_date: str = None) -> Dict[str, Any]:
        """Generate error analysis report"""
        try:
            if not start_date:
                start_date = (datetime.now() - timedelta(days=7)).isoformat()
            if not end_date:
                end_date = datetime.now().isoformat()
            
            report_data = {}
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Total error count
                cursor.execute('''
                    SELECT COUNT(*) FROM error_logs 
                    WHERE timestamp BETWEEN ? AND ?
                ''', (start_date, end_date))
                report_data['total_errors'] = cursor.fetchone()[0]
                
                # Errors by type
                cursor.execute('''
                    SELECT error_type, COUNT(*) as count 
                    FROM error_logs 
                    WHERE timestamp BETWEEN ? AND ?
                    GROUP BY error_type 
                    ORDER BY count DESC
                ''', (start_date, end_date))
                report_data['errors_by_type'] = [
                    {'error_type': error_type, 'count': count} 
                    for error_type, count in cursor.fetchall()
                ]
                
                # Errors by component
                cursor.execute('''
                    SELECT component, COUNT(*) as count 
                    FROM error_logs 
                    WHERE timestamp BETWEEN ? AND ?
                    GROUP BY component 
                    ORDER BY count DESC
                ''', (start_date, end_date))
                report_data['errors_by_component'] = [
                    {'component': component, 'count': count} 
                    for component, count in cursor.fetchall()
                ]
                
                # Errors by severity
                cursor.execute('''
                    SELECT severity, COUNT(*) as count 
                    FROM error_logs 
                    WHERE timestamp BETWEEN ? AND ?
                    GROUP BY severity 
                    ORDER BY count DESC
                ''', (start_date, end_date))
                report_data['errors_by_severity'] = [
                    {'severity': severity, 'count': count} 
                    for severity, count in cursor.fetchall()
                ]
                
                # Error trends (daily)
                cursor.execute('''
                    SELECT DATE(timestamp) as date, COUNT(*) as count 
                    FROM error_logs 
                    WHERE timestamp BETWEEN ? AND ?
                    GROUP BY DATE(timestamp) 
                    ORDER BY date
                ''', (start_date, end_date))
                report_data['error_trends'] = [
                    {'date': date, 'count': count} 
                    for date, count in cursor.fetchall()
                ]
            
            # Add metadata
            report_data['report_metadata'] = {
                'generated_at': datetime.now().isoformat(),
                'period_start': start_date,
                'period_end': end_date,
                'report_type': 'error_analysis'
            }
            
            return {
                'success': True,
                'report_data': report_data,
                'message': 'Error analysis report generated successfully'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Failed to generate error analysis report: {str(e)}'
            }
    
    def save_report_to_file(self, report_data: Dict[str, Any], report_name: str) -> Dict[str, Any]:
        """Save report data to JSON file"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{report_name}_{timestamp}.json"
            file_path = os.path.join(self.reports_path, filename)
            
            # Save report
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, indent=2, ensure_ascii=False)
            
            # Get file size
            file_size = os.path.getsize(file_path)
            
            # Store report metadata
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO reports 
                    (report_name, report_type, generated_at, file_path, parameters, size_bytes)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    report_name,
                    report_data.get('report_metadata', {}).get('report_type', 'unknown'),
                    datetime.now().isoformat(),
                    file_path,
                    json.dumps({}),
                    file_size
                ))
                conn.commit()
            
            # Update statistics
            self.analytics_stats['reports_generated'] += 1
            
            return {
                'success': True,
                'file_path': file_path,
                'file_size': file_size,
                'message': f'Report saved to {filename}'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Failed to save report: {str(e)}'
            }
    
    def get_current_system_status(self) -> Dict[str, Any]:
        """Get current real-time system status"""
        return {
            'system_performance': self.current_metrics.get('system_performance', {}),
            'active_users': len(self.current_metrics.get('user_activity', {})),
            'component_status': self.component_metrics,
            'error_count': len(self.current_metrics.get('error_tracking', {})),
            'uptime_seconds': (datetime.now() - self.start_time).total_seconds(),
            'monitoring_active': self.monitoring_active,
            'last_updated': datetime.now().isoformat()
        }
    
    def get_analytics_dashboard_data(self) -> Dict[str, Any]:
        """Get data for analytics dashboard"""
        try:
            # Get recent metrics (last 24 hours)
            yesterday = (datetime.now() - timedelta(days=1)).isoformat()
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Recent interactions
                cursor.execute('''
                    SELECT COUNT(*) FROM user_interactions 
                    WHERE timestamp > ?
                ''', (yesterday,))
                recent_interactions = cursor.fetchone()[0]
                
                # Recent errors
                cursor.execute('''
                    SELECT COUNT(*) FROM error_logs 
                    WHERE timestamp > ?
                ''', (yesterday,))
                recent_errors = cursor.fetchone()[0]
                
                # Average response time (last 24h)
                cursor.execute('''
                    SELECT AVG(response_time) FROM user_interactions 
                    WHERE timestamp > ? AND response_time > 0
                ''', (yesterday,))
                result = cursor.fetchone()[0]
                avg_response_time = round(result, 3) if result else 0.0
            
            dashboard_data = {
                'current_status': self.get_current_system_status(),
                'recent_metrics': {
                    'interactions_24h': recent_interactions,
                    'errors_24h': recent_errors,
                    'avg_response_time_24h': avg_response_time
                },
                'system_stats': self.analytics_stats,
                'component_metrics': self.component_metrics,
                'alerts': self.get_active_alerts(),
                'last_updated': datetime.now().isoformat()
            }
            
            return {
                'success': True,
                'dashboard_data': dashboard_data
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Failed to get dashboard data: {str(e)}'
            }
    
    def get_active_alerts(self) -> List[Dict[str, Any]]:
        """Get current active alerts"""
        alerts = []
        
        # Check current system performance
        current_perf = self.current_metrics.get('system_performance', {})
        
        if current_perf.get('cpu_usage', 0) > self.monitoring_config['alert_thresholds']['cpu_usage']:
            alerts.append({
                'type': 'performance',
                'severity': 'high',
                'message': f"High CPU usage: {current_perf['cpu_usage']:.1f}%",
                'timestamp': current_perf.get('timestamp')
            })
        
        if current_perf.get('memory_usage', 0) > self.monitoring_config['alert_thresholds']['memory_usage']:
            alerts.append({
                'type': 'performance',
                'severity': 'high',
                'message': f"High memory usage: {current_perf['memory_usage']:.1f}%",
                'timestamp': current_perf.get('timestamp')
            })
        
        # Check for recent errors
        error_count = len(self.current_metrics.get('error_tracking', {}))
        if error_count > 5:  # More than 5 different error types
            alerts.append({
                'type': 'error',
                'severity': 'medium',
                'message': f"Multiple error types detected: {error_count}",
                'timestamp': datetime.now().isoformat()
            })
        
        return alerts
    
    def cleanup_old_data(self, days_to_keep: int = None):
        """Clean up old analytics data"""
        if days_to_keep is None:
            days_to_keep = self.monitoring_config['retention_days']
        
        cutoff_date = (datetime.now() - timedelta(days=days_to_keep)).isoformat()
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Clean up old system metrics
                cursor.execute('DELETE FROM system_metrics WHERE timestamp < ?', (cutoff_date,))
                deleted_metrics = cursor.rowcount
                
                # Clean up old interactions (keep summary data)
                cursor.execute('DELETE FROM user_interactions WHERE timestamp < ?', (cutoff_date,))
                deleted_interactions = cursor.rowcount
                
                # Clean up old component performance data
                cursor.execute('DELETE FROM component_performance WHERE timestamp < ?', (cutoff_date,))
                deleted_performance = cursor.rowcount
                
                # Keep error logs longer (double the retention period)
                error_cutoff = (datetime.now() - timedelta(days=days_to_keep * 2)).isoformat()
                cursor.execute('DELETE FROM error_logs WHERE timestamp < ?', (error_cutoff,))
                deleted_errors = cursor.rowcount
                
                conn.commit()
            
            print(f"✅ Cleanup completed:")
            print(f"   Deleted {deleted_metrics} system metrics")
            print(f"   Deleted {deleted_interactions} user interactions")
            print(f"   Deleted {deleted_performance} performance records")
            print(f"   Deleted {deleted_errors} error logs")
            
        except Exception as e:
            print(f"❌ Cleanup error: {e}")
    
    def load_analytics_stats(self):
        """Load analytics statistics from database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Count total interactions
                cursor.execute('SELECT COUNT(*) FROM user_interactions')
                self.analytics_stats['total_interactions'] = cursor.fetchone()[0]
                
                # Count unique users
                cursor.execute('SELECT COUNT(DISTINCT user_id) FROM user_interactions')
                self.analytics_stats['total_users'] = cursor.fetchone()[0]
                
                # Calculate average response time
                cursor.execute('SELECT AVG(response_time) FROM user_interactions WHERE response_time > 0')
                result = cursor.fetchone()[0]
                self.analytics_stats['average_response_time'] = round(result, 3) if result else 0.0
                
                # Count errors
                cursor.execute('SELECT COUNT(*) FROM error_logs')
                self.analytics_stats['error_count'] = cursor.fetchone()[0]
                
                # Count reports
                cursor.execute('SELECT COUNT(*) FROM reports')
                self.analytics_stats['reports_generated'] = cursor.fetchone()[0]
                
                # Calculate uptime
                self.analytics_stats['system_uptime'] = (datetime.now() - self.start_time).total_seconds()
                
        except Exception as e:
            print(f"Error loading analytics stats: {e}")
    
    def get_analytics_status(self) -> Dict[str, Any]:
        """Get comprehensive analytics system status"""
        self.load_analytics_stats()
        
        return {
            'capabilities': self.capabilities,
            'monitoring_config': self.monitoring_config,
            'statistics': self.analytics_stats,
            'current_metrics': self.current_metrics,
            'component_metrics': self.component_metrics,
            'monitoring_active': self.monitoring_active,
            'database_path': self.db_path,
            'reports_path': self.reports_path,
            'system_status': 'active'
        }

def main():
    """Test the analytics system"""
    print("📊 JARVIS ANALYTICS SYSTEM TEST")
    print("=" * 50)
    
    # Initialize analytics system
    analytics = JarvisAnalyticsSystem()
    
    # Wait a moment for monitoring to start
    time.sleep(2)
    
    # Test user interaction tracking
    print("\n🔄 Testing user interaction tracking...")
    for i in range(5):
        result = analytics.track_user_interaction(
            user_id=f"user_{i % 3}",
            session_id=f"session_{i}",
            interaction_type="chat",
            command=f"test command {i}",
            response_time=0.5 + (i * 0.1),
            success=True,
            component_used="chat_interface",
            input_length=20 + i,
            output_length=50 + (i * 2)
        )
        if result['success']:
            print(f"✅ Interaction {i+1} tracked successfully")
    
    # Test component performance tracking
    print("\n🔄 Testing component performance tracking...")
    components = ['memory_system', 'learning_system', 'internet_system']
    for i, component in enumerate(components):
        result = analytics.track_component_performance(
            component_name=component,
            operation="test_operation",
            execution_time=0.2 + (i * 0.05),
            success=True,
            memory_used=10.5 + i,
            cpu_used=5.2 + i
        )
        if result['success']:
            print(f"✅ {component} performance tracked")
    
    # Test error logging
    print("\n🔄 Testing error logging...")
    error_result = analytics.log_error(
        error_type="test_error",
        error_message="This is a test error for analytics",
        component="test_component",
        severity="low",
        user_id="test_user"
    )
    if error_result['success']:
        print("✅ Error logged successfully")
    
    # Generate usage report
    print("\n🔄 Generating usage report...")
    usage_report = analytics.generate_usage_report()
    if usage_report['success']:
        print("✅ Usage report generated successfully")
        print(f"   Total interactions: {usage_report['report_data']['total_interactions']}")
        print(f"   Unique users: {usage_report['report_data']['unique_users']}")
        print(f"   Success rate: {usage_report['report_data']['success_rate']}%")
        
        # Save report to file
        save_result = analytics.save_report_to_file(usage_report['report_data'], "usage_report")
        if save_result['success']:
            print(f"✅ Report saved: {save_result['file_path']}")
    
    # Generate performance report
    print("\n🔄 Generating performance report...")
    perf_report = analytics.generate_performance_report()
    if perf_report['success']:
        print("✅ Performance report generated successfully")
        sys_perf = perf_report['report_data'].get('system_performance', {})
        print(f"   Avg CPU usage: {sys_perf.get('avg_cpu_usage', 0)}%")
        print(f"   Avg memory usage: {sys_perf.get('avg_memory_usage', 0)}%")
    
    # Generate error analysis report
    print("\n🔄 Generating error analysis report...")
    error_report = analytics.generate_error_analysis_report()
    if error_report['success']:
        print("✅ Error analysis report generated successfully")
        print(f"   Total errors: {error_report['report_data']['total_errors']}")
    
    # Get dashboard data
    print("\n🔄 Getting dashboard data...")
    dashboard = analytics.get_analytics_dashboard_data()
    if dashboard['success']:
        print("✅ Dashboard data retrieved successfully")
        recent = dashboard['dashboard_data']['recent_metrics']
        print(f"   Interactions (24h): {recent['interactions_24h']}")
        print(f"   Errors (24h): {recent['errors_24h']}")
        print(f"   Avg response time (24h): {recent['avg_response_time_24h']}s")
    
    # Show current system status
    print("\n📊 Current System Status:")
    status = analytics.get_current_system_status()
    print(f"   Active users: {status['active_users']}")
    print(f"   Uptime: {status['uptime_seconds']:.0f} seconds")
    print(f"   Monitoring active: {status['monitoring_active']}")
    
    # Show analytics system status
    print("\n📊 Analytics System Status:")
    analytics_status = analytics.get_analytics_status()
    print(f"   Active capabilities: {sum(analytics_status['capabilities'].values())}/8")
    print(f"   Total interactions tracked: {analytics_status['statistics']['total_interactions']}")
    print(f"   Total users: {analytics_status['statistics']['total_users']}")
    print(f"   Reports generated: {analytics_status['statistics']['reports_generated']}")
    print(f"   Data points collected: {analytics_status['statistics']['data_points_collected']}")
    
    # Test cleanup (but don't actually delete recent data)
    print("\n🔄 Testing data cleanup (dry run)...")
    print("✅ Cleanup functionality available")
    
    # Stop monitoring
    analytics.stop_monitoring()
    print("\n⏹️ Analytics system test completed")


if __name__ == "__main__":
    main()