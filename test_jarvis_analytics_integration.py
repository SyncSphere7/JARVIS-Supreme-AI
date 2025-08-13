#!/usr/bin/env python3
"""
Test JARVIS Analytics Integration
Comprehensive test of analytics system with multiple JARVIS components
"""

import time
import random
from jarvis_analytics_system import JarvisAnalyticsSystem

def simulate_jarvis_usage():
    """Simulate realistic JARVIS usage patterns"""
    print("🚀 SIMULATING REALISTIC JARVIS USAGE PATTERNS")
    print("=" * 60)
    
    # Initialize analytics
    analytics = JarvisAnalyticsSystem()
    
    # Simulate different users and components
    users = ["alice", "bob", "charlie", "diana", "eve"]
    components = [
        "memory_system", "learning_system", "internet_system", 
        "automation_system", "reasoning_system", "multilang_system"
    ]
    
    commands = [
        "remember my preferences", "search the internet", "translate text",
        "analyze data", "automate task", "learn from conversation",
        "reason about problem", "store knowledge", "get weather",
        "schedule meeting", "send email", "calculate result"
    ]
    
    print("\n🔄 Simulating user interactions...")
    
    # Simulate 50 interactions
    for i in range(50):
        user = random.choice(users)
        component = random.choice(components)
        command = random.choice(commands)
        
        # Simulate varying response times
        response_time = random.uniform(0.1, 3.0)
        success = random.choice([True, True, True, True, False])  # 80% success rate
        
        # Track interaction
        analytics.track_user_interaction(
            user_id=user,
            session_id=f"session_{user}_{i//10}",
            interaction_type="command",
            command=command,
            response_time=response_time,
            success=success,
            component_used=component,
            input_length=len(command),
            output_length=random.randint(20, 200)
        )
        
        # Track component performance
        execution_time = response_time * 0.8  # Component time is part of total time
        analytics.track_component_performance(
            component_name=component,
            operation=command.split()[0],  # First word as operation
            execution_time=execution_time,
            success=success,
            memory_used=random.uniform(5.0, 50.0),
            cpu_used=random.uniform(1.0, 20.0)
        )
        
        # Occasionally log errors
        if not success:
            analytics.log_error(
                error_type="operation_failed",
                error_message=f"Failed to execute: {command}",
                component=component,
                severity=random.choice(["low", "medium", "high"]),
                user_id=user
            )
        
        # Small delay to simulate real usage
        time.sleep(0.01)
        
        if (i + 1) % 10 == 0:
            print(f"   Processed {i + 1}/50 interactions...")
    
    print("✅ Simulation completed!")
    
    # Wait for monitoring to collect some data
    print("\n⏳ Waiting for system monitoring data...")
    time.sleep(3)
    
    # Generate comprehensive reports
    print("\n📊 GENERATING COMPREHENSIVE REPORTS")
    print("=" * 40)
    
    # Usage report
    print("\n1. Usage Analytics Report:")
    usage_report = analytics.generate_usage_report()
    if usage_report['success']:
        data = usage_report['report_data']
        print(f"   ✅ Total interactions: {data['total_interactions']}")
        print(f"   ✅ Unique users: {data['unique_users']}")
        print(f"   ✅ Average response time: {data['avg_response_time']}s")
        print(f"   ✅ Success rate: {data['success_rate']}%")
        print(f"   ✅ Top commands: {len(data['top_commands'])}")
        print(f"   ✅ Top components: {len(data['top_components'])}")
        
        # Save report
        save_result = analytics.save_report_to_file(data, "comprehensive_usage_report")
        if save_result['success']:
            print(f"   💾 Report saved: {save_result['file_path']}")
    
    # Performance report
    print("\n2. Performance Analysis Report:")
    perf_report = analytics.generate_performance_report()
    if perf_report['success']:
        data = perf_report['report_data']
        sys_perf = data.get('system_performance', {})
        print(f"   ✅ Avg CPU usage: {sys_perf.get('avg_cpu_usage', 0)}%")
        print(f"   ✅ Avg memory usage: {sys_perf.get('avg_memory_usage', 0)}%")
        print(f"   ✅ Components analyzed: {len(data.get('component_performance', []))}")
        
        # Show component performance
        for comp in data.get('component_performance', [])[:3]:
            print(f"      - {comp['component']}: {comp['total_calls']} calls, "
                  f"{comp['avg_execution_time']}s avg, {comp['success_rate']}% success")
    
    # Error analysis report
    print("\n3. Error Analysis Report:")
    error_report = analytics.generate_error_analysis_report()
    if error_report['success']:
        data = error_report['report_data']
        print(f"   ✅ Total errors: {data['total_errors']}")
        print(f"   ✅ Error types: {len(data['errors_by_type'])}")
        print(f"   ✅ Affected components: {len(data['errors_by_component'])}")
        
        # Show top errors
        for error in data['errors_by_type'][:3]:
            print(f"      - {error['error_type']}: {error['count']} occurrences")
    
    # Dashboard data
    print("\n4. Real-time Dashboard Data:")
    dashboard = analytics.get_analytics_dashboard_data()
    if dashboard['success']:
        data = dashboard['dashboard_data']
        current = data['current_status']
        recent = data['recent_metrics']
        
        print(f"   ✅ Active users: {current['active_users']}")
        print(f"   ✅ System uptime: {current['uptime_seconds']:.0f}s")
        print(f"   ✅ Interactions (24h): {recent['interactions_24h']}")
        print(f"   ✅ Errors (24h): {recent['errors_24h']}")
        print(f"   ✅ Avg response time (24h): {recent['avg_response_time_24h']}s")
        
        # Show alerts
        alerts = data.get('alerts', [])
        if alerts:
            print(f"   ⚠️ Active alerts: {len(alerts)}")
            for alert in alerts:
                print(f"      - {alert['type']}: {alert['message']}")
        else:
            print("   ✅ No active alerts")
    
    # Component metrics summary
    print("\n5. Component Metrics Summary:")
    status = analytics.get_analytics_status()
    comp_metrics = status['component_metrics']
    
    for comp_name, metrics in comp_metrics.items():
        if metrics['calls'] > 0:
            error_rate = (metrics['errors'] / metrics['calls']) * 100
            print(f"   ✅ {comp_name}:")
            print(f"      - Calls: {metrics['calls']}")
            print(f"      - Avg time: {metrics['avg_time']:.3f}s")
            print(f"      - Error rate: {error_rate:.1f}%")
    
    # System statistics
    print("\n📈 FINAL SYSTEM STATISTICS")
    print("=" * 30)
    stats = status['statistics']
    print(f"Total interactions tracked: {stats['total_interactions']}")
    print(f"Total users: {stats['total_users']}")
    print(f"Average response time: {stats['average_response_time']}s")
    print(f"Total errors: {stats['error_count']}")
    print(f"Reports generated: {stats['reports_generated']}")
    print(f"Data points collected: {stats['data_points_collected']}")
    print(f"System uptime: {stats['system_uptime']:.0f}s")
    
    # Capabilities summary
    print(f"\nAnalytics capabilities: {sum(status['capabilities'].values())}/8 active")
    for capability, active in status['capabilities'].items():
        status_icon = "✅" if active else "❌"
        print(f"  {status_icon} {capability}")
    
    # Stop monitoring
    analytics.stop_monitoring()
    print("\n🎉 JARVIS Analytics Integration Test Completed Successfully!")
    
    return analytics

if __name__ == "__main__":
    simulate_jarvis_usage()
