#!/usr/bin/env python3
"""
JARVIS Plugin Marketplace - Plugin Discovery and Installation
"""

import os
import json
from typing import Dict, List, Any
from jarvis_plugin_system import PluginManager, PluginInterface

class PluginMarketplace:
    """Plugin marketplace for discovering and installing JARVIS plugins"""
    
    def __init__(self, plugin_manager: PluginManager):
        self.plugin_manager = plugin_manager
        
        # Sample marketplace plugins
        self.marketplace_plugins = {
            'time_plugin': {
                'id': 'time_plugin',
                'name': 'Time & Date Plugin',
                'version': '1.0.0',
                'author': 'JARVIS Time Team',
                'description': 'Provides current time, date, and timezone information',
                'category': 'utilities',
                'rating': 4.8,
                'downloads': 1250,
                'commands': ['get_time', 'get_date', 'convert_timezone'],
                'capabilities': ['time_services', 'timezone_conversion'],
                'verified': True
            },
            'translator_plugin': {
                'id': 'translator_plugin',
                'name': 'Language Translator',
                'version': '2.1.0',
                'author': 'JARVIS Language Team',
                'description': 'Translates text between multiple languages',
                'category': 'language',
                'rating': 4.9,
                'downloads': 2100,
                'commands': ['translate_text', 'detect_language', 'list_languages'],
                'capabilities': ['translation', 'language_detection'],
                'verified': True
            },
            'file_manager_plugin': {
                'id': 'file_manager_plugin',
                'name': 'File Manager',
                'version': '1.5.0',
                'author': 'JARVIS System Team',
                'description': 'Manages files and directories with advanced operations',
                'category': 'system',
                'rating': 4.6,
                'downloads': 890,
                'commands': ['list_files', 'create_directory', 'move_file', 'search_files'],
                'capabilities': ['file_management', 'directory_operations'],
                'verified': True
            },
            'music_plugin': {
                'id': 'music_plugin',
                'name': 'Music Player',
                'version': '3.0.0',
                'author': 'JARVIS Entertainment',
                'description': 'Controls music playback and manages playlists',
                'category': 'entertainment',
                'rating': 4.7,
                'downloads': 1800,
                'commands': ['play_music', 'pause_music', 'create_playlist', 'search_songs'],
                'capabilities': ['music_control', 'playlist_management'],
                'verified': False
            },
            'email_plugin': {
                'id': 'email_plugin',
                'name': 'Email Manager',
                'version': '1.3.0',
                'author': 'JARVIS Communication',
                'description': 'Sends and manages emails with smart features',
                'category': 'communication',
                'rating': 4.5,
                'downloads': 1500,
                'commands': ['send_email', 'read_emails', 'search_emails', 'schedule_email'],
                'capabilities': ['email_management', 'communication'],
                'verified': True
            }
        }
    
    def browse_marketplace(self, category: str = None, verified_only: bool = False) -> Dict[str, Any]:
        """Browse available plugins in the marketplace"""
        filtered_plugins = []
        
        for plugin_id, plugin_info in self.marketplace_plugins.items():
            # Apply filters
            if category and plugin_info['category'] != category:
                continue
            if verified_only and not plugin_info['verified']:
                continue
            
            filtered_plugins.append(plugin_info)
        
        # Sort by rating and downloads
        filtered_plugins.sort(key=lambda x: (x['rating'], x['downloads']), reverse=True)
        
        return {
            'success': True,
            'plugins': filtered_plugins,
            'total_count': len(filtered_plugins),
            'categories': list(set(p['category'] for p in self.marketplace_plugins.values()))
        }
    
    def search_plugins(self, query: str) -> Dict[str, Any]:
        """Search for plugins by name, description, or capabilities"""
        matching_plugins = []
        query_lower = query.lower()
        
        for plugin_id, plugin_info in self.marketplace_plugins.items():
            # Search in name, description, and capabilities
            if (query_lower in plugin_info['name'].lower() or
                query_lower in plugin_info['description'].lower() or
                any(query_lower in cap.lower() for cap in plugin_info['capabilities'])):
                matching_plugins.append(plugin_info)
        
        # Sort by relevance (rating for now)
        matching_plugins.sort(key=lambda x: x['rating'], reverse=True)
        
        return {
            'success': True,
            'plugins': matching_plugins,
            'total_count': len(matching_plugins),
            'query': query
        }
    
    def get_plugin_details(self, plugin_id: str) -> Dict[str, Any]:
        """Get detailed information about a specific plugin"""
        if plugin_id not in self.marketplace_plugins:
            return {
                'success': False,
                'error': f'Plugin {plugin_id} not found in marketplace'
            }
        
        plugin_info = self.marketplace_plugins[plugin_id].copy()
        
        # Add additional details
        plugin_info['is_installed'] = plugin_id in self.plugin_manager.loaded_plugins
        plugin_info['installation_size'] = '2.5 MB'  # Mock data
        plugin_info['last_updated'] = '2025-01-10'
        plugin_info['compatibility'] = 'JARVIS v1.0.0+'
        
        return {
            'success': True,
            'plugin': plugin_info
        }
    
    def simulate_plugin_installation(self, plugin_id: str) -> Dict[str, Any]:
        """Simulate plugin installation (creates a mock plugin)"""
        if plugin_id not in self.marketplace_plugins:
            return {
                'success': False,
                'error': f'Plugin {plugin_id} not found in marketplace'
            }
        
        if plugin_id in self.plugin_manager.loaded_plugins:
            return {
                'success': False,
                'error': f'Plugin {plugin_id} is already installed'
            }
        
        plugin_info = self.marketplace_plugins[plugin_id]
        
        # Create a mock plugin class dynamically
        class MockPlugin(PluginInterface):
            def __init__(self, info):
                self.info = info
            
            def get_plugin_info(self) -> Dict[str, Any]:
                return self.info
            
            def initialize(self, jarvis_context: Dict[str, Any]) -> bool:
                print(f"🔌 {self.info['name']} initialized from marketplace")
                return True
            
            def execute(self, command: str, parameters: Dict[str, Any] = None) -> Dict[str, Any]:
                return {
                    'success': True,
                    'message': f'Mock execution of {command} from {self.info["name"]}',
                    'plugin': self.info['name'],
                    'command': command,
                    'parameters': parameters or {}
                }
            
            def cleanup(self) -> bool:
                print(f"🔌 {self.info['name']} cleaned up")
                return True
            
            def get_commands(self) -> List[str]:
                return self.info['commands']
            
            def get_capabilities(self) -> List[str]:
                return self.info['capabilities']
        
        # Create and register the mock plugin
        mock_plugin = MockPlugin(plugin_info)
        jarvis_context = self.plugin_manager.create_jarvis_context()
        
        if mock_plugin.initialize(jarvis_context):
            # Register plugin
            self.plugin_manager.loaded_plugins[plugin_id] = mock_plugin
            self.plugin_manager.plugin_metadata[plugin_id] = plugin_info
            
            # Register commands
            for command in mock_plugin.get_commands():
                self.plugin_manager.plugin_commands[command] = plugin_id
            
            # Register capabilities
            for capability in mock_plugin.get_capabilities():
                if capability not in self.plugin_manager.plugin_capabilities:
                    self.plugin_manager.plugin_capabilities[capability] = []
                self.plugin_manager.plugin_capabilities[capability].append(plugin_id)
            
            # Update statistics
            self.plugin_manager.plugin_stats['total_plugins'] += 1
            self.plugin_manager.plugin_stats['active_plugins'] += 1
            self.plugin_manager.plugin_stats['commands_registered'] += len(mock_plugin.get_commands())
            
            return {
                'success': True,
                'plugin_id': plugin_id,
                'message': f'Plugin {plugin_info["name"]} installed successfully',
                'commands_added': mock_plugin.get_commands(),
                'capabilities_added': mock_plugin.get_capabilities()
            }
        else:
            return {
                'success': False,
                'error': f'Failed to initialize plugin {plugin_id}'
            }
    
    def get_marketplace_stats(self) -> Dict[str, Any]:
        """Get marketplace statistics"""
        categories = {}
        total_downloads = 0
        verified_count = 0
        
        for plugin_info in self.marketplace_plugins.values():
            category = plugin_info['category']
            if category not in categories:
                categories[category] = 0
            categories[category] += 1
            
            total_downloads += plugin_info['downloads']
            if plugin_info['verified']:
                verified_count += 1
        
        return {
            'total_plugins': len(self.marketplace_plugins),
            'categories': categories,
            'total_downloads': total_downloads,
            'verified_plugins': verified_count,
            'average_rating': sum(p['rating'] for p in self.marketplace_plugins.values()) / len(self.marketplace_plugins)
        }


def main():
    """Test the plugin marketplace"""
    print("🏪 JARVIS PLUGIN MARKETPLACE TEST")
    print("=" * 50)
    
    # Initialize plugin manager and marketplace
    plugin_manager = PluginManager()
    marketplace = PluginMarketplace(plugin_manager)
    
    # Test 1: Browse marketplace
    print("\n1️⃣ Browsing Plugin Marketplace...")
    browse_result = marketplace.browse_marketplace()
    if browse_result['success']:
        print(f"✅ Found {browse_result['total_count']} plugins in marketplace")
        print(f"📂 Available categories: {browse_result['categories']}")
        
        for plugin in browse_result['plugins'][:3]:  # Show top 3
            verified_icon = "✅" if plugin['verified'] else "⚠️"
            print(f"\n   {verified_icon} {plugin['name']} v{plugin['version']}")
            print(f"      By: {plugin['author']}")
            print(f"      Category: {plugin['category']}")
            print(f"      Rating: {plugin['rating']}/5.0 ({plugin['downloads']} downloads)")
            print(f"      Description: {plugin['description']}")
            print(f"      Commands: {plugin['commands']}")
    
    # Test 2: Search plugins
    print("\n2️⃣ Searching Plugins...")
    search_result = marketplace.search_plugins("time")
    if search_result['success']:
        print(f"✅ Found {search_result['total_count']} plugins matching 'time':")
        for plugin in search_result['plugins']:
            print(f"   🔍 {plugin['name']} - {plugin['description']}")
    
    # Test 3: Get plugin details
    print("\n3️⃣ Getting Plugin Details...")
    details_result = marketplace.get_plugin_details('translator_plugin')
    if details_result['success']:
        plugin = details_result['plugin']
        print(f"✅ Plugin Details for {plugin['name']}:")
        print(f"   Version: {plugin['version']}")
        print(f"   Author: {plugin['author']}")
        print(f"   Rating: {plugin['rating']}/5.0")
        print(f"   Downloads: {plugin['downloads']}")
        print(f"   Installed: {plugin['is_installed']}")
        print(f"   Size: {plugin['installation_size']}")
        print(f"   Commands: {plugin['commands']}")
        print(f"   Capabilities: {plugin['capabilities']}")
    
    # Test 4: Install plugins
    print("\n4️⃣ Installing Plugins from Marketplace...")
    
    plugins_to_install = ['time_plugin', 'translator_plugin', 'file_manager_plugin']
    
    for plugin_id in plugins_to_install:
        install_result = marketplace.simulate_plugin_installation(plugin_id)
        if install_result['success']:
            print(f"✅ Installed: {install_result['message']}")
            print(f"   Commands added: {install_result['commands_added']}")
            print(f"   Capabilities added: {install_result['capabilities_added']}")
        else:
            print(f"❌ Installation failed: {install_result['error']}")
    
    # Test 5: Test installed plugins
    print("\n5️⃣ Testing Installed Plugins...")
    
    # Test time plugin
    time_result = plugin_manager.execute_plugin_command('get_time')
    if time_result['success']:
        print(f"✅ Time Plugin: {time_result['message']}")
    
    # Test translator plugin
    translate_result = plugin_manager.execute_plugin_command('translate_text', {
        'text': 'Hello World',
        'target_language': 'Spanish'
    })
    if translate_result['success']:
        print(f"✅ Translator Plugin: {translate_result['message']}")
    
    # Test file manager plugin
    files_result = plugin_manager.execute_plugin_command('list_files', {'directory': '/home'})
    if files_result['success']:
        print(f"✅ File Manager Plugin: {files_result['message']}")
    
    # Test 6: Updated system status
    print("\n6️⃣ Updated System Status...")
    status = plugin_manager.get_plugin_system_status()
    print(f"   📦 Total plugins: {status['loaded_plugins']}")
    print(f"   🔧 Available commands: {status['available_commands']}")
    print(f"   🎯 Available capabilities: {status['available_capabilities']}")
    print(f"   📊 Plugin executions: {status['statistics']['plugin_executions']}")
    
    # Test 7: Marketplace statistics
    print("\n7️⃣ Marketplace Statistics...")
    marketplace_stats = marketplace.get_marketplace_stats()
    print(f"   🏪 Total marketplace plugins: {marketplace_stats['total_plugins']}")
    print(f"   📂 Categories: {marketplace_stats['categories']}")    
    # Test file manager plu   print(f"   📥 Total downloads: {ma   tp    files_result = plugin_man}"    if files_result['success' plugins: {marketplace_stats['verified_plugins']}")
    print(f"   ⭐ Average rating: {marketplace_stats['average_rating']:.1f}/5.0")
    
    print("\n🎉 PLUGIN MARKETPLACE TEST COMPLETED!")


if __name__ == "__main__":
    main()
