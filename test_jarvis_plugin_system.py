#!/usr/bin/env python3
"""
Comprehensive test of JARVIS Plugin System
"""

import os
import shutil
from jarvis_plugin_system import PluginManager, PluginInterface
from typing import Dict, List, Any

# Example Plugin Classes
class WeatherPlugin(PluginInterface):
    """Example weather plugin"""
    
    def get_plugin_info(self) -> Dict[str, Any]:
        return {
            'name': 'Weather Plugin',
            'version': '1.0.0',
            'author': 'JARVIS Team',
            'description': 'Provides weather information and forecasts'
        }
    
    def initialize(self, jarvis_context: Dict[str, Any]) -> bool:
        print("🌤️ Weather Plugin initialized")
        self.context = jarvis_context
        return True
    
    def execute(self, command: str, parameters: Dict[str, Any] = None) -> Dict[str, Any]:
        if command == "get_weather":
            location = parameters.get('location', 'Unknown') if parameters else 'Unknown'
            return {
                'success': True,
                'weather': f'Sunny, 72°F in {location}',
                'temperature': 72,
                'condition': 'sunny',
                'location': location
            }
        elif command == "get_forecast":
            days = parameters.get('days', 3) if parameters else 3
            return {
                'success': True,
                'forecast': f'Sunny for the next {days} days',
                'days': days,
                'conditions': ['sunny', 'partly_cloudy', 'sunny']
            }
        else:
            return {
                'success': False,
                'error': f'Unknown command: {command}'
            }
    
    def cleanup(self) -> bool:
        print("🌤️ Weather Plugin cleaned up")
        return True
    
    def get_commands(self) -> List[str]:
        return ['get_weather', 'get_forecast']
    
    def get_capabilities(self) -> List[str]:
        return ['weather_data', 'forecasting', 'location_services']


class CalculatorPlugin(PluginInterface):
    """Example calculator plugin"""
    
    def get_plugin_info(self) -> Dict[str, Any]:
        return {
            'name': 'Calculator Plugin',
            'version': '1.2.0',
            'author': 'JARVIS Math Team',
            'description': 'Provides mathematical calculations and conversions'
        }
    
    def initialize(self, jarvis_context: Dict[str, Any]) -> bool:
        print("🧮 Calculator Plugin initialized")
        self.context = jarvis_context
        return True
    
    def execute(self, command: str, parameters: Dict[str, Any] = None) -> Dict[str, Any]:
        if command == "calculate":
            if not parameters or 'expression' not in parameters:
                return {
                    'success': False,
                    'error': 'Missing expression parameter'
                }
            
            try:
                expression = parameters['expression']
                # Basic safety check
                if any(char in expression for char in ['import', 'exec', 'eval', '__']):
                    return {
                        'success': False,
                        'error': 'Invalid expression for security reasons'
                    }
                
                # Simple math evaluation (in real plugin, use proper math parser)
                result = eval(expression)
                return {
                    'success': True,
                    'result': result,
                    'expression': expression,
                    'type': type(result).__name__
                }
            except Exception as e:
                return {
                    'success': False,
                    'error': f'Calculation error: {str(e)}'
                }
        
        elif command == "convert_units":
            if not parameters or 'value' not in parameters or 'from_unit' not in parameters or 'to_unit' not in parameters:
                return {
                    'success': False,
                    'error': 'Missing conversion parameters (value, from_unit, to_unit)'
                }
            
            # Simple unit conversion examples
            conversions = {
                ('celsius', 'fahrenheit'): lambda x: x * 9/5 + 32,
                ('fahrenheit', 'celsius'): lambda x: (x - 32) * 5/9,
                ('meters', 'feet'): lambda x: x * 3.28084,
                ('feet', 'meters'): lambda x: x / 3.28084
            }
            
            key = (parameters['from_unit'].lower(), parameters['to_unit'].lower())
            if key in conversions:
                result = conversions[key](parameters['value'])
                return {
                    'success': True,
                    'result': result,
                    'original_value': parameters['value'],
                    'from_unit': parameters['from_unit'],
                    'to_unit': parameters['to_unit']
                }
            else:
                return {
                    'success': False,
                    'error': f'Conversion from {parameters["from_unit"]} to {parameters["to_unit"]} not supported'
                }
        
        else:
            return {
                'success': False,
                'error': f'Unknown command: {command}'
            }
    
    def cleanup(self) -> bool:
        print("🧮 Calculator Plugin cleaned up")
        return True
    
    def get_commands(self) -> List[str]:
        return ['calculate', 'convert_units']
    
    def get_capabilities(self) -> List[str]:
        return ['mathematics', 'calculations', 'unit_conversion']


class NotesPlugin(PluginInterface):
    """Example notes plugin"""
    
    def get_plugin_info(self) -> Dict[str, Any]:
        return {
            'name': 'Notes Plugin',
            'version': '1.0.0',
            'author': 'JARVIS Productivity Team',
            'description': 'Manages notes and reminders'
        }
    
    def initialize(self, jarvis_context: Dict[str, Any]) -> bool:
        print("📝 Notes Plugin initialized")
        self.context = jarvis_context
        self.notes = {}  # Simple in-memory storage
        return True
    
    def execute(self, command: str, parameters: Dict[str, Any] = None) -> Dict[str, Any]:
        if command == "create_note":
            if not parameters or 'title' not in parameters or 'content' not in parameters:
                return {
                    'success': False,
                    'error': 'Missing note parameters (title, content)'
                }
            
            note_id = f"note_{len(self.notes) + 1}"
            self.notes[note_id] = {
                'title': parameters['title'],
                'content': parameters['content'],
                'created_at': '2025-01-13T01:00:00',
                'tags': parameters.get('tags', [])
            }
            
            return {
                'success': True,
                'note_id': note_id,
                'message': f'Note "{parameters["title"]}" created successfully'
            }
        
        elif command == "list_notes":
            notes_list = []
            for note_id, note in self.notes.items():
                notes_list.append({
                    'id': note_id,
                    'title': note['title'],
                    'created_at': note['created_at'],
                    'tags': note['tags']
                })
            
            return {
                'success': True,
                'notes': notes_list,
                'total_count': len(notes_list)
            }
        
        elif command == "get_note":
            if not parameters or 'note_id' not in parameters:
                return {
                    'success': False,
                    'error': 'Missing note_id parameter'
                }
            
            note_id = parameters['note_id']
            if note_id in self.notes:
                return {
                    'success': True,
                    'note': self.notes[note_id]
                }
            else:
                return {
                    'success': False,
                    'error': f'Note {note_id} not found'
                }
        
        else:
            return {
                'success': False,
                'error': f'Unknown command: {command}'
            }
    
    def cleanup(self) -> bool:
        print("📝 Notes Plugin cleaned up")
        return True
    
    def get_commands(self) -> List[str]:
        return ['create_note', 'list_notes', 'get_note']
    
    def get_capabilities(self) -> List[str]:
        return ['note_taking', 'content_management', 'productivity']


def create_plugin_files(plugin_manager):
    """Create plugin files for testing"""
    
    # Create weather plugin file
    weather_code = '''
from typing import Dict, List, Any
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from jarvis_plugin_system import PluginInterface

class WeatherPlugin(PluginInterface):
    def get_plugin_info(self) -> Dict[str, Any]:
        return {
            'name': 'Weather Plugin',
            'version': '1.0.0',
            'author': 'JARVIS Team',
            'description': 'Provides weather information'
        }
    
    def initialize(self, jarvis_context: Dict[str, Any]) -> bool:
        return True
    
    def execute(self, command: str, parameters: Dict[str, Any] = None) -> Dict[str, Any]:
        if command == "get_weather":
            location = parameters.get('location', 'Unknown') if parameters else 'Unknown'
            return {
                'success': True,
                'weather': f'Sunny, 72°F in {location}',
                'temperature': 72
            }
        return {'success': False, 'error': f'Unknown command: {command}'}
    
    def cleanup(self) -> bool:
        return True
    
    def get_commands(self) -> List[str]:
        return ['get_weather']
    
    def get_capabilities(self) -> List[str]:
        return ['weather_data']
'''
    
    weather_path = os.path.join(plugin_manager.installed_plugins_dir, 'weather_plugin.py')
    with open(weather_path, 'w') as f:
        f.write(weather_code)
    
    return weather_path


def test_plugin_system():
    """Comprehensive test of the plugin system"""
    print("🔌 COMPREHENSIVE JARVIS PLUGIN SYSTEM TEST")
    print("=" * 60)
    
    # Initialize plugin manager
    plugin_manager = PluginManager()
    
    # Test 1: Direct plugin registration (simulating loaded plugins)
    print("\n1️⃣ Testing Direct Plugin Registration...")
    
    # Manually register plugins for testing
    weather_plugin = WeatherPlugin()
    calc_plugin = CalculatorPlugin()
    notes_plugin = NotesPlugin()
    
    # Simulate plugin loading
    jarvis_context = plugin_manager.create_jarvis_context()
    
    # Initialize plugins
    weather_plugin.initialize(jarvis_context)
    calc_plugin.initialize(jarvis_context)
    notes_plugin.initialize(jarvis_context)
    
    # Register plugins manually
    plugin_manager.loaded_plugins['weather'] = weather_plugin
    plugin_manager.loaded_plugins['calculator'] = calc_plugin
    plugin_manager.loaded_plugins['notes'] = notes_plugin
    
    # Register metadata
    plugin_manager.plugin_metadata['weather'] = weather_plugin.get_plugin_info()
    plugin_manager.plugin_metadata['calculator'] = calc_plugin.get_plugin_info()
    plugin_manager.plugin_metadata['notes'] = notes_plugin.get_plugin_info()
    
    # Register commands
    for plugin_id, plugin in plugin_manager.loaded_plugins.items():
        for command in plugin.get_commands():
            plugin_manager.plugin_commands[command] = plugin_id
    
    # Register capabilities
    for plugin_id, plugin in plugin_manager.loaded_plugins.items():
        for capability in plugin.get_capabilities():
            if capability not in plugin_manager.plugin_capabilities:
                plugin_manager.plugin_capabilities[capability] = []
            plugin_manager.plugin_capabilities[capability].append(plugin_id)
    
    # Update stats
    plugin_manager.plugin_stats['total_plugins'] = len(plugin_manager.loaded_plugins)
    plugin_manager.plugin_stats['active_plugins'] = len(plugin_manager.loaded_plugins)
    plugin_manager.plugin_stats['commands_registered'] = len(plugin_manager.plugin_commands)
    
    print(f"✅ Registered {len(plugin_manager.loaded_plugins)} plugins directly")
    
    # Test 2: Plugin Listing
    print("\n2️⃣ Testing Plugin Listing...")
    plugins_list = plugin_manager.list_plugins()
    if plugins_list['success']:
        print(f"✅ Found {plugins_list['total_count']} plugins:")
        for plugin in plugins_list['plugins']:
            print(f"   📦 {plugin['name']} v{plugin['version']} by {plugin['author']}")
            print(f"      Description: {plugin['description']}")
            print(f"      Commands: {plugin['commands']}")
            print(f"      Capabilities: {plugin['capabilities']}")
            print()
    
    # Test 3: Available Commands
    print("3️⃣ Testing Available Commands...")
    commands = plugin_manager.get_available_commands()
    if commands['success']:
        print(f"✅ Available commands ({commands['total_count']}):")
        for command, info in commands['commands'].items():
            print(f"   🔧 {command} (from {info['plugin_name']})")
    
    # Test 4: Plugin Execution
    print("\n4️⃣ Testing Plugin Execution...")
    
    # Test weather commands
    print("\n🌤️ Weather Plugin Tests:")
    weather_result = plugin_manager.execute_plugin_command('get_weather', {'location': 'New York'})
    if weather_result['success']:
        print(f"✅ Weather: {weather_result['weather']}")
        print(f"   Temperature: {weather_result['temperature']}°F")
        print(f"   Condition: {weather_result['condition']}")
    
    forecast_result = plugin_manager.execute_plugin_command('get_forecast', {'days': 5})
    if forecast_result['success']:
        print(f"✅ Forecast: {forecast_result['forecast']}")
        print(f"   Days: {forecast_result['days']}")
    
    # Test calculator commands
    print("\n🧮 Calculator Plugin Tests:")
    calc_result = plugin_manager.execute_plugin_command('calculate', {'expression': '2 + 2 * 3'})
    if calc_result['success']:
        print(f"✅ Calculation: {calc_result['expression']} = {calc_result['result']}")
    
    convert_result = plugin_manager.execute_plugin_command('convert_units', {
        'value': 100,
        'from_unit': 'celsius',
        'to_unit': 'fahrenheit'
    })
    if convert_result['success']:
        print(f"✅ Conversion: {convert_result['original_value']}°{convert_result['from_unit']} = {convert_result['result']}°{convert_result['to_unit']}")
    
    # Test notes commands
    print("\n📝 Notes Plugin Tests:")
    note_result = plugin_manager.execute_plugin_command('create_note', {
        'title': 'JARVIS Plugin Test',
        'content': 'This is a test note created by the plugin system',
        'tags': ['test', 'jarvis', 'plugin']
    })
    if note_result['success']:
        print(f"✅ Note created: {note_result['message']}")
        
        # List notes
        list_result = plugin_manager.execute_plugin_command('list_notes')
        if list_result['success']:
            print(f"✅ Notes list: {list_result['total_count']} notes found")
            for note in list_result['notes']:
                print(f"   📄 {note['title']} (ID: {note['id']})")
    
    # Test 5: Error Handling
    print("\n5️⃣ Testing Error Handling...")
    
    # Test unknown command
    unknown_result = plugin_manager.execute_plugin_command('unknown_command')
    if not unknown_result['success']:
        print(f"✅ Unknown command handled: {unknown_result['error']}")
    
    # Test plugin error
    error_result = plugin_manager.execute_plugin_command('calculate', {'expression': 'invalid_expression'})
    if not error_result['success']:
        print(f"✅ Plugin error handled: {error_result['error']}")
    
    # Test 6: Capabilities
    print("\n6️⃣ Testing Capabilities...")
    print("Available capabilities:")
    for capability, plugin_ids in plugin_manager.plugin_capabilities.items():
        print(f"   🎯 {capability}: {plugin_ids}")
    
    # Test 7: System Status
    print("\n7️⃣ Plugin System Status:")
    status = plugin_manager.get_plugin_system_status()
    print(f"   🔌 Active capabilities: {sum(status['capabilities'].values())}/8")
    print(f"   📦 Loaded plugins: {status['loaded_plugins']}")
    print(f"   🔧 Available commands: {status['available_commands']}")
    print(f"   🎯 Available capabilities: {status['available_capabilities']}")
    print(f"   📊 Plugin executions: {status['statistics']['plugin_executions']}")
    print(f"   📈 Commands registered: {status['statistics']['commands_registered']}")
    print(f"   ✅ System status: {status['system_status']}")
    
    # Test 8: Plugin Capabilities Summary
    print("\n8️⃣ Plugin System Capabilities:")
    for capability, active in status['capabilities'].items():
        status_icon = "✅" if active else "❌"
        print(f"   {status_icon} {capability.replace('_', ' ').title()}")
    
    # Cleanup
    print("\n🧹 Cleaning up plugins...")
    for plugin in plugin_manager.loaded_plugins.values():
        plugin.cleanup()
    
    print("\n🎉 COMPREHENSIVE PLUGIN SYSTEM TEST COMPLETED!")
    print(f"📊 Final Statistics:")
    print(f"   Total Plugins: {status['statistics']['total_plugins']}")
    print(f"   Active Plugins: {status['statistics']['active_plugins']}")
    print(f"   Commands Registered: {status['statistics']['commands_registered']}")
    print(f"   Plugin Executions: {status['statistics']['plugin_executions']}")
    
    return plugin_manager


if __name__ == "__main__":
    test_plugin_system()
