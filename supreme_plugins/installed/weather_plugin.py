
from jarvis_plugin_system import PluginInterface
from typing import Dict, List, Any

class WeatherPlugin(PluginInterface):
    def get_plugin_info(self) -> Dict[str, Any]:
        return {
            'name': 'Weather Plugin',
            'version': '1.0.0',
            'author': 'JARVIS Team',
            'description': 'Provides weather information'
        }
    
    def initialize(self, jarvis_context: Dict[str, Any]) -> bool:
        print("🌤️ Weather Plugin initialized")
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
