#!/usr/bin/env python3
"""
JARVIS Supreme Being AI - All Features Integrated
Supreme Being AI V01 with Voice, Memory, Learning, Internet, and Chat capabilities built-in
"""

import asyncio
import json
import os
import threading
import time
from datetime import datetime
from typing import Dict, List, Any, Optional
import webbrowser
from flask import Flask, render_template, request, jsonify

# Import all JARVIS components
try:
    from jarvis_memory_system import JarvisMemorySystem
    MEMORY_AVAILABLE = True
except ImportError:
    MEMORY_AVAILABLE = False
    print("⚠️ Memory system not available")

try:
    from jarvis_learning_system import JarvisLearningSystem
    LEARNING_AVAILABLE = True
except ImportError:
    LEARNING_AVAILABLE = False
    print("⚠️ Learning system not available")

try:
    from jarvis_chat_interface import JarvisChatAI
    CHAT_AVAILABLE = True
except ImportError:
    CHAT_AVAILABLE = False
    print("⚠️ Chat AI not available")

try:
    from jarvis_internet_system import JarvisInternetSystem
    INTERNET_AVAILABLE = True
except ImportError:
    INTERNET_AVAILABLE = False
    print("⚠️ Internet system not available")

try:
    from jarvis_automation_system import JarvisAutomationSystem
    AUTOMATION_AVAILABLE = True
except ImportError:
    AUTOMATION_AVAILABLE = False
    print("⚠️ Automation system not available")

try:
    from jarvis_reasoning_system import JarvisReasoningSystem
    REASONING_AVAILABLE = True
except ImportError:
    REASONING_AVAILABLE = False
    print("⚠️ Reasoning system not available")

try:
    from jarvis_security_system import JarvisSecuritySystem
    SECURITY_AVAILABLE = True
except ImportError:
    SECURITY_AVAILABLE = False
    print("⚠️ Security system not available")

# Try voice components
try:
    from voice import listen, speak
    VOICE_AVAILABLE = True
except ImportError:
    VOICE_AVAILABLE = False
    print("⚠️ Voice system not available")

class JarvisSupremeBeing:
    """JARVIS Supreme Being AI system with all capabilities integrated"""
    
    def __init__(self):
        self.name = "JARVIS Supreme Being AI"
        self.version = "V01"
        self.status = "initializing"
        
        # Initialize all subsystems
        self.memory_system = None
        self.learning_system = None
        self.chat_ai = None
        self.internet_system = None
        self.automation_system = None
        self.reasoning_system = None
        self.security_system = None
        
        # System capabilities
        self.capabilities = {
            'memory': MEMORY_AVAILABLE,
            'learning': LEARNING_AVAILABLE,
            'chat': CHAT_AVAILABLE,
            'voice': VOICE_AVAILABLE,
            'internet': INTERNET_AVAILABLE,
            'automation': AUTOMATION_AVAILABLE,
            'reasoning': REASONING_AVAILABLE,
            'security': SECURITY_AVAILABLE
        }
        
        # Session management
        self.current_session = self.generate_session_id()
        self.conversation_history = []
        
        # Initialize all systems
        self.initialize_all_systems()
        
        # Flask app for web interface
        self.app = Flask(__name__)
        self.setup_web_routes()
    
    def initialize_all_systems(self):
        """Initialize all JARVIS subsystems"""
        print("🚀 INITIALIZING JARVIS SUPREME BEING AI...")
        print("=" * 60)
        
        try:
            # Initialize Memory System
            if MEMORY_AVAILABLE:
                print("🧠 Initializing Memory System...")
                self.memory_system = JarvisMemorySystem()
                print("✅ Memory System: ACTIVE")
            else:
                print("❌ Memory System: UNAVAILABLE")
            
            # Initialize Learning System
            if LEARNING_AVAILABLE:
                print("🎓 Initializing Learning System...")
                self.learning_system = JarvisLearningSystem()
                print("✅ Learning System: ACTIVE")
            else:
                print("❌ Learning System: UNAVAILABLE")
            
            # Initialize Chat AI
            if CHAT_AVAILABLE:
                print("💬 Initializing Chat AI...")
                self.chat_ai = JarvisChatAI()
                print("✅ Chat AI: ACTIVE")
            else:
                print("❌ Chat AI: UNAVAILABLE")
            
            # Initialize Internet System
            if INTERNET_AVAILABLE:
                print("🌐 Initializing Internet System...")
                self.internet_system = JarvisInternetSystem()
                print("✅ Internet System: ACTIVE")
            else:
                print("❌ Internet System: UNAVAILABLE")
            
            # Initialize Automation System
            if AUTOMATION_AVAILABLE:
                print("🔧 Initializing Automation System...")
                self.automation_system = JarvisAutomationSystem()
                print("✅ Automation System: ACTIVE")
            else:
                print("❌ Automation System: UNAVAILABLE")
            
            # Initialize Reasoning System
            if REASONING_AVAILABLE:
                print("🧠 Initializing Reasoning System...")
                self.reasoning_system = JarvisReasoningSystem()
                print("✅ Reasoning System: ACTIVE")
            else:
                print("❌ Reasoning System: UNAVAILABLE")
            
            # Initialize Security System
            if SECURITY_AVAILABLE:
                print("🔒 Initializing Security System...")
                self.security_system = JarvisSecuritySystem()
                print("✅ Security System: ACTIVE")
            else:
                print("❌ Security System: UNAVAILABLE")
            
            # Check Voice System
            if VOICE_AVAILABLE:
                print("✅ Voice System: ACTIVE")
            else:
                print("❌ Voice System: UNAVAILABLE")
            
            self.status = "active"
            print("\n🎉 JARVIS SUPREME BEING AI FULLY OPERATIONAL!")
            print(f"🤖 {self.name} {self.version} - All systems integrated and ready")
            
        except Exception as e:
            print(f"❌ System initialization error: {e}")
            self.status = "error"
    
    def process_input(self, user_input: str, input_type: str = "text") -> str:
        """Process user input through all integrated systems"""
        try:
            timestamp = datetime.now().isoformat()
            
            # Check for reasoning requests first (more specific patterns)
            if any(phrase in user_input.lower() for phrase in ['solve:', 'analyze:', 'decide:', 'should i choose', 'logic:', 'reason about']):
                response = self.handle_reasoning_request(user_input)
            # Check for automation requests
            elif any(word in user_input.lower() for word in ['create file', 'run command', 'execute', 'automate', 'script']):
                response = self.handle_automation_request(user_input)
            # Check for internet requests
            elif any(word in user_input.lower() for word in ['search', 'web search', 'news', 'weather']):
                response = self.handle_internet_request(user_input)
            # Generate response using Chat AI
            elif CHAT_AVAILABLE:
                response = self.chat_ai.generate_response(user_input)
            else:
                response = self.generate_fallback_response(user_input)
            
            # Store in memory system
            if MEMORY_AVAILABLE:
                self.memory_system.store_conversation(
                    user_input, 
                    response, 
                    importance=2
                )
            
            # Learn from interaction
            if LEARNING_AVAILABLE:
                self.learning_system.learn_from_interaction(
                    user_input, 
                    response, 
                    success=True
                )
            
            # Add to conversation history
            self.conversation_history.append({
                'timestamp': timestamp,
                'user_input': user_input,
                'jarvis_response': response,
                'input_type': input_type
            })
            
            # Keep only last 100 conversations in memory
            if len(self.conversation_history) > 100:
                self.conversation_history = self.conversation_history[-100:]
            
            return response
            
        except Exception as e:
            return f"I encountered an error processing your request: {str(e)}"
    
    def handle_reasoning_request(self, user_input: str) -> str:
        """Handle reasoning and problem-solving requests"""
        user_lower = user_input.lower()
        
        if not REASONING_AVAILABLE or not self.reasoning_system:
            return "Advanced reasoning system is not available in this session."
        
        try:
            if 'solve' in user_lower or 'problem' in user_lower:
                # Extract problem statement
                problem_indicators = ['solve', 'problem', 'how can', 'how do', 'what is the best way']
                problem_statement = user_input
                
                for indicator in problem_indicators:
                    if indicator in user_lower:
                        parts = user_input.split(indicator, 1)
                        if len(parts) > 1:
                            problem_statement = parts[1].strip()
                        break
                
                # Determine problem type
                if any(word in user_lower for word in ['plan', 'strategy', 'optimize']):
                    problem_type = 'planning'
                elif any(word in user_lower for word in ['choose', 'decide', 'select']):
                    problem_type = 'decision'
                elif any(word in user_lower for word in ['calculate', 'math', 'compute']):
                    problem_type = 'mathematical'
                else:
                    problem_type = 'general'
                
                result = self.reasoning_system.solve_problem(problem_statement, problem_type)
                
                if 'error' not in result:
                    response = f"🧠 **Problem Analysis Complete**\n\n"
                    response += f"**Problem Type:** {result['problem_type'].title()}\n"
                    response += f"**Reasoning Method:** {result['reasoning_method'].replace('_', ' ').title()}\n"
                    response += f"**Confidence:** {result['confidence_score']:.1%}\n\n"
                    response += f"**Solution Steps:**\n"
                    for step in result['solution_steps']:
                        response += f"• {step}\n"
                    response += f"\n**Analysis:** {result['final_solution']}"
                    return response
                else:
                    return f"❌ **Problem Solving Failed**\n\nError: {result['error']}"
            
            elif 'decide' in user_lower or 'choose' in user_lower:
                # Simple decision making - extract options if provided
                if ' or ' in user_input:
                    parts = user_input.split(' or ')
                    options = [part.strip().strip('?.,!') for part in parts]
                    context = f"Decision context: {user_input}"
                    
                    decision = self.reasoning_system.make_decision(context, options)
                    
                    if 'error' not in decision:
                        response = f"🎯 **Decision Analysis Complete**\n\n"
                        response += f"**Chosen Option:** {decision['chosen_option']}\n"
                        response += f"**Confidence:** {decision['confidence_score']:.1%}\n"
                        response += f"**Reasoning:** {decision['reasoning']}\n\n"
                        response += f"**Options Evaluated:**\n"
                        for option in decision['options_evaluated']:
                            response += f"• {option}\n"
                        return response
                    else:
                        return f"❌ **Decision Making Failed**\n\nError: {decision['error']}"
                else:
                    return "For decision making, please provide options separated by 'or'. Example: 'Should I choose Python or JavaScript for my project?'"
            
            elif 'logic' in user_lower or 'if' in user_lower and 'then' in user_lower:
                # Logical inference
                premises = [user_input]  # Simple single premise for now
                inference = self.reasoning_system.perform_logical_inference(premises)
                
                if 'error' not in inference:
                    response = f"🔍 **Logical Analysis Complete**\n\n"
                    response += f"**Inference Rule:** {inference['inference_rule'].replace('_', ' ').title()}\n"
                    response += f"**Conclusion:** {inference['conclusion']}\n"
                    response += f"**Validity:** {'✅ Valid' if inference['validity'] else '❌ Invalid'}\n"
                    response += f"**Confidence:** {inference['confidence_score']:.1%}"
                    return response
                else:
                    return f"❌ **Logical Inference Failed**\n\nError: {inference['error']}"
            
            elif 'analyze' in user_lower:
                return "🧠 **Advanced Analysis Capabilities:**\n\n" \
                       "• **Problem Solving:** Multi-step reasoning for complex challenges\n" \
                       "• **Decision Making:** Weighted criteria analysis for optimal choices\n" \
                       "• **Logical Inference:** Formal logic rules (modus ponens, modus tollens)\n" \
                       "• **Pattern Recognition:** Sequence and frequency pattern identification\n" \
                       "• **Strategic Planning:** Goal-oriented step-by-step planning\n\n" \
                       "Example: 'Solve: How can I improve my productivity?' or 'Decide: Python or JavaScript?'"
            
            return "I can help with advanced reasoning tasks like problem solving, decision making, and logical analysis. What would you like me to analyze?"
            
        except Exception as e:
            return f"Error processing reasoning request: {str(e)}"
    
    def handle_automation_request(self, user_input: str) -> str:
        """Handle automation-specific requests"""
        user_lower = user_input.lower()
        
        if not AUTOMATION_AVAILABLE or not self.automation_system:
            return "Automation system is not available in this session."
        
        try:
            if 'create file' in user_lower:
                # Extract file path and content
                parts = user_input.split('create file', 1)
                if len(parts) > 1:
                    file_info = parts[1].strip()
                    # Simple parsing - can be enhanced
                    if ' with content ' in file_info:
                        file_path, content = file_info.split(' with content ', 1)
                        file_path = file_path.strip().strip('"\'')
                        content = content.strip().strip('"\'')
                    else:
                        file_path = file_info.strip().strip('"\'')
                        content = ""
                    
                    # Ensure file_path is not empty
                    if not file_path:
                        return "Please specify a valid file path. Example: 'create file test.txt with content Hello World'"
                    
                    result = self.automation_system.create_file(file_path, content)
                    if result['status'] == 'success':
                        return f"✅ **File Created Successfully**\n\n" \
                               f"📁 Path: {result['file_path']}\n" \
                               f"📊 Size: {result['file_size']} bytes\n" \
                               f"✨ {result['message']}"
                    else:
                        return f"❌ **File Creation Failed**\n\nError: {result['error']}"
                else:
                    return "Please specify the file path. Example: 'create file test.txt with content Hello World'"
            
            elif 'run command' in user_lower or 'execute' in user_lower:
                # Extract command
                for phrase in ['run command', 'execute']:
                    if phrase in user_lower:
                        parts = user_input.split(phrase, 1)
                        if len(parts) > 1:
                            command = parts[1].strip().strip('"\'')
                            result = self.automation_system.execute_command(command)
                            
                            if result['status'] == 'success':
                                return f"✅ **Command Executed Successfully**\n\n" \
                                       f"💻 Command: {result['command']}\n" \
                                       f"⏱️ Duration: {result['duration']:.2f}s\n" \
                                       f"📤 Output:\n```\n{result['output']}\n```"
                            else:
                                return f"❌ **Command Execution Failed**\n\n" \
                                       f"💻 Command: {result['command']}\n" \
                                       f"❌ Error: {result['error']}"
                        break
                else:
                    return "Please specify the command to execute. Example: 'run command ls -la'"
            
            elif 'system info' in user_lower or 'system status' in user_lower:
                sys_info = self.automation_system.get_system_info()
                if 'error' not in sys_info:
                    return f"🖥️ **System Information**\n\n" \
                           f"🔧 CPU Usage: {sys_info['cpu']['cpu_percent']}%\n" \
                           f"🧠 Memory Usage: {sys_info['memory']['percent']}%\n" \
                           f"💾 Disk Usage: {sys_info['disk']['percent']:.1f}%\n" \
                           f"⚡ CPU Cores: {sys_info['cpu']['cpu_count']}\n" \
                           f"📊 Available Memory: {sys_info['memory']['available'] / (1024**3):.1f} GB"
                else:
                    return f"❌ Unable to get system information: {sys_info['error']}"
            
            elif 'script' in user_lower:
                return "🔧 **Automation Script Features:**\n\n" \
                       "• Create Python/Bash scripts\n" \
                       "• Execute automation scripts\n" \
                       "• Schedule recurring tasks\n" \
                       "• File operations (create, copy, move, delete)\n" \
                       "• System monitoring and info\n\n" \
                       "Example: 'create file my_script.py with content print(\"Hello JARVIS\")'"
            
            return "I can help with automation tasks like creating files, running commands, and system operations. What would you like me to automate?"
            
        except Exception as e:
            return f"Error processing automation request: {str(e)}"
    
    def handle_internet_request(self, user_input: str) -> str:
        """Handle internet-specific requests"""
        user_lower = user_input.lower()
        
        if not INTERNET_AVAILABLE or not self.internet_system:
            return "Internet access is not available in this session."
        
        try:
            if 'search' in user_lower or 'web' in user_lower:
                # Extract search query
                query = user_input.replace('search for', '').replace('search', '').replace('web', '').strip()
                if query:
                    results = self.internet_system.search_web(query, num_results=3)
                    if results:
                        response = f"🔍 **Web Search Results for '{query}':**\n\n"
                        for i, result in enumerate(results, 1):
                            response += f"{i}. **{result.get('title', 'No title')}**\n"
                            response += f"   {result.get('snippet', 'No description')[:100]}...\n"
                            if result.get('url'):
                                response += f"   🔗 {result['url']}\n\n"
                        return response
                    else:
                        return f"No search results found for '{query}'. Please try a different search term."
                else:
                    return "Please specify what you'd like me to search for."
            
            elif 'news' in user_lower:
                news = self.internet_system.get_news("general", num_articles=3)
                if news:
                    response = "📰 **Latest News:**\n\n"
                    for i, article in enumerate(news, 1):
                        response += f"{i}. **{article.get('title', 'No title')}**\n"
                        response += f"   {article.get('summary', 'No summary')[:100]}...\n"
                        if article.get('url'):
                            response += f"   🔗 {article['url']}\n\n"
                    return response
                else:
                    return "Unable to fetch news at the moment. Please try again later."
            
            elif 'weather' in user_lower:
                # Extract location if provided
                location = "London"  # Default location
                weather = self.internet_system.get_weather(location)
                if 'error' not in weather:
                    return f"🌤️ **Weather in {location}:**\n\n" \
                           f"Temperature: {weather.get('temperature', 'N/A')}°C\n" \
                           f"Condition: {weather.get('condition', 'N/A')}\n" \
                           f"Humidity: {weather.get('humidity', 'N/A')}%\n" \
                           f"Wind Speed: {weather.get('wind_speed', 'N/A')} km/h"
                else:
                    return f"Unable to get weather data: {weather['error']}"
            
            return "I can help with web searches, news, and weather. Please specify what you'd like me to look up."
            
        except Exception as e:
            return f"Error processing internet request: {str(e)}"
    
    def generate_fallback_response(self, user_input: str) -> str:
        """Generate fallback response when chat AI is unavailable"""
        user_lower = user_input.lower()
        
        if any(word in user_lower for word in ['who created', 'creator', 'made you']):
            return "I was created by an advanced development team. I'm JARVIS Supreme Being AI, an advanced AI system with integrated memory, learning, internet access, and conversational capabilities."
        
        elif any(word in user_lower for word in ['hello', 'hi', 'hey']):
            return f"Hello! I'm {self.name}, your Supreme Being AI assistant. All my systems are integrated and working together to help you."
        
        elif any(word in user_lower for word in ['capabilities', 'what can you do']):
            active_systems = [k for k, v in self.capabilities.items() if v]
            capabilities_text = f"I have integrated {', '.join(active_systems)} systems working together.\n\n"
            capabilities_text += "🧠 **Memory & Learning:** Remember conversations and learn from interactions\n"
            capabilities_text += "💬 **Intelligent Chat:** Advanced conversational AI with context awareness\n"
            if self.capabilities.get('internet'):
                capabilities_text += "🌐 **Internet Access:** Web search, scraping, news, weather, and real-time data\n"
            if self.capabilities.get('automation'):
                capabilities_text += "🔧 **Automation System:** File operations, command execution, and task automation\n"
            if self.capabilities.get('reasoning'):
                capabilities_text += "🧠 **Advanced Reasoning:** Problem solving, decision making, and logical analysis\n"
            if self.capabilities.get('voice'):
                capabilities_text += "🎤 **Voice Interface:** Speech recognition and text-to-speech\n"
            capabilities_text += "\nWhat would you like me to help you with?"
            return capabilities_text
        

        else:
            return f"I understand you're asking about: {user_input}. I'm processing this through my integrated systems to provide the best response."
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        status = {
            'jarvis_info': {
                'name': self.name,
                'version': self.version,
                'status': self.status,
                'session_id': self.current_session
            },
            'capabilities': self.capabilities,
            'subsystems': {},
            'conversation_stats': {
                'current_session_conversations': len(self.conversation_history),
                'last_interaction': self.conversation_history[-1]['timestamp'] if self.conversation_history else None
            }
        }
        
        # Get subsystem statuses
        if MEMORY_AVAILABLE and self.memory_system:
            status['subsystems']['memory'] = self.memory_system.get_memory_status()
        
        if LEARNING_AVAILABLE and self.learning_system:
            status['subsystems']['learning'] = self.learning_system.get_learning_status()
        
        if INTERNET_AVAILABLE and self.internet_system:
            status['subsystems']['internet'] = self.internet_system.get_internet_status()
        
        if AUTOMATION_AVAILABLE and self.automation_system:
            status['subsystems']['automation'] = self.automation_system.get_automation_status()
        
        if REASONING_AVAILABLE and self.reasoning_system:
            status['subsystems']['reasoning'] = self.reasoning_system.get_reasoning_status()
        
        return status
    
    def setup_web_routes(self):
        """Setup Flask web routes for unified interface"""
        
        @self.app.route('/')
        def index():
            return '''<!DOCTYPE html>
<html>
<head>
    <title>JARVIS Supreme Being AI</title>
    <style>
        body { 
            font-family: 'Courier New', monospace; 
            background: #0a0a0a; 
            color: #00ff41; 
            padding: 20px; 
            margin: 0;
        }
        .container { max-width: 1200px; margin: 0 auto; }
        .header { 
            text-align: center; 
            border: 2px solid #00ff41; 
            padding: 20px; 
            margin-bottom: 20px; 
            background: rgba(0,255,65,0.1);
            border-radius: 10px;
        }
        .chat-area { 
            border: 1px solid #00ff41; 
            padding: 20px; 
            margin-bottom: 20px; 
            background: rgba(0,255,65,0.05);
            border-radius: 10px;
            height: 400px;
            overflow-y: auto;
        }
        .input-area {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
        }
        .input-field {
            flex: 1;
            background: #1a1a1a;
            border: 1px solid #00ff41;
            color: #00ff41;
            padding: 10px;
            border-radius: 5px;
            font-family: 'Courier New', monospace;
        }
        .send-btn {
            background: #00ff41;
            color: #0a0a0a;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            font-weight: bold;
        }
        .send-btn:hover { background: #00cc33; }
        .status-panel {
            border: 1px solid #00ff41;
            padding: 15px;
            background: rgba(0,255,65,0.05);
            border-radius: 10px;
        }
        .message {
            margin: 10px 0;
            padding: 8px;
            border-radius: 5px;
        }
        .user-message {
            background: rgba(0,100,255,0.2);
            text-align: right;
        }
        .jarvis-message {
            background: rgba(0,255,65,0.2);
        }
        .timestamp {
            font-size: 0.8em;
            opacity: 0.7;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 JARVIS SUPREME BEING AI 🤖</h1>
            <p>Supreme Being AI - All Systems Integrated</p>
            <p>Memory • Learning • Chat • Voice - Working Together</p>
        </div>
        
        <div class="chat-area" id="chatArea">
            <div class="jarvis-message">
                <strong>JARVIS:</strong> Hello! I'm JARVIS Supreme Being AI. All my capabilities are integrated and working together. How can I assist you today?
                <div class="timestamp">System initialized</div>
            </div>
        </div>
        
        <div class="input-area">
            <input type="text" id="messageInput" class="input-field" placeholder="Type your message here..." onkeypress="if(event.key==='Enter') sendMessage()">
            <button onclick="sendMessage()" class="send-btn">Send</button>
        </div>
        
        <div class="status-panel">
            <h3>🔧 System Status</h3>
            <div id="statusInfo">Loading system status...</div>
        </div>
    </div>

    <script>
        function sendMessage() {
            const input = document.getElementById('messageInput');
            const message = input.value.trim();
            if (!message) return;
            
            // Add user message to chat
            addMessage('user', message);
            input.value = '';
            
            // Send to JARVIS
            fetch('/api/chat', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({message: message})
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    addMessage('jarvis', data.response);
                } else {
                    addMessage('jarvis', 'Error: ' + data.error);
                }
            })
            .catch(error => {
                addMessage('jarvis', 'Connection error: ' + error);
            });
        }
        
        function addMessage(sender, message) {
            const chatArea = document.getElementById('chatArea');
            const messageDiv = document.createElement('div');
            messageDiv.className = sender === 'user' ? 'message user-message' : 'message jarvis-message';
            
            const timestamp = new Date().toLocaleTimeString();
            messageDiv.innerHTML = `
                <strong>${sender === 'user' ? 'You' : 'JARVIS'}:</strong> ${message}
                <div class="timestamp">${timestamp}</div>
            `;
            
            chatArea.appendChild(messageDiv);
            chatArea.scrollTop = chatArea.scrollHeight;
        }
        
        function updateStatus() {
            fetch('/api/status')
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const status = data.status;
                    document.getElementById('statusInfo').innerHTML = `
                        <strong>JARVIS ${status.jarvis_info.version}</strong><br>
                        Status: ${status.jarvis_info.status.toUpperCase()}<br>
                        Memory: ${status.capabilities.memory ? '✅ Active' : '❌ Inactive'}<br>
                        Learning: ${status.capabilities.learning ? '✅ Active' : '❌ Inactive'}<br>
                        Chat AI: ${status.capabilities.chat ? '✅ Active' : '❌ Inactive'}<br>
                        Voice: ${status.capabilities.voice ? '✅ Active' : '❌ Inactive'}<br>
                        Session: ${status.conversation_stats.current_session_conversations} conversations
                    `;
                }
            });
        }
        
        // Update status every 5 seconds
        updateStatus();
        setInterval(updateStatus, 5000);
    </script>
</body>
</html>'''
        
        @self.app.route('/api/chat', methods=['POST'])
        def api_chat():
            try:
                data = request.get_json()
                message = data.get('message', '')
                
                if not message:
                    return jsonify({'success': False, 'error': 'No message provided'})
                
                response = self.process_input(message, 'web')
                
                return jsonify({
                    'success': True,
                    'response': response,
                    'timestamp': datetime.now().isoformat()
                })
                
            except Exception as e:
                return jsonify({'success': False, 'error': str(e)})
        
        @self.app.route('/api/status')
        def api_status():
            try:
                status = self.get_system_status()
                return jsonify({'success': True, 'status': status})
            except Exception as e:
                return jsonify({'success': False, 'error': str(e)})
    
    def start_voice_interface(self):
        """Start voice interface in background thread"""
        if not VOICE_AVAILABLE:
            print("❌ Voice interface not available")
            return
        
        def voice_loop():
            print("🎤 Voice interface active - say 'Hey JARVIS' to activate")
            
            while True:
                try:
                    # Listen for wake word
                    text = listen()
                    if text and 'jarvis' in text.lower():
                        speak("Yes, how can I help you?")
                        
                        # Listen for command
                        command = listen()
                        if command:
                            response = self.process_input(command, 'voice')
                            speak(response)
                        
                except Exception as e:
                    print(f"Voice error: {e}")
                    time.sleep(1)
        
        voice_thread = threading.Thread(target=voice_loop, daemon=True)
        voice_thread.start()
    
    def start_web_interface(self, port: int = 5002):
        """Start web interface"""
        print(f"🌐 Starting JARVIS Supreme Being AI Web Interface on port {port}...")
        
        def open_browser():
            time.sleep(1)
            webbrowser.open(f'http://127.0.0.1:{port}')
        
        threading.Timer(1.0, open_browser).start()
        self.app.run(host='127.0.0.1', port=port, debug=False)
    
    def start_cli_interface(self):
        """Start command line interface"""
        print("💻 JARVIS CLI Interface Active")
        print("Type 'quit' to exit, 'status' for system status")
        print("-" * 50)
        
        while True:
            try:
                user_input = input("\n🤖 You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("👋 JARVIS signing off. Goodbye!")
                    break
                
                elif user_input.lower() == 'status':
                    status = self.get_system_status()
                    print(f"\n📊 JARVIS Status:")
                    print(f"   Version: {status['jarvis_info']['version']}")
                    print(f"   Status: {status['jarvis_info']['status']}")
                    print(f"   Active Systems: {sum(status['capabilities'].values())}/4")
                    print(f"   Conversations: {status['conversation_stats']['current_session_conversations']}")
                
                elif user_input:
                    response = self.process_input(user_input, 'cli')
                    print(f"\n🤖 JARVIS: {response}")
                
            except KeyboardInterrupt:
                print("\n👋 JARVIS signing off. Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
    
    def generate_session_id(self) -> str:
        """Generate unique session ID"""
        import hashlib
        return f"unified_{hashlib.md5(f'{datetime.now().isoformat()}_{os.getpid()}'.encode()).hexdigest()[:16]}"

def main():
    """Main function to start JARVIS Supreme Being AI"""
    print("🚀 STARTING JARVIS SUPREME BEING AI...")
    
    # Initialize JARVIS
    jarvis = JarvisSupremeBeing()
    
    if jarvis.status != "active":
        print("❌ JARVIS initialization failed")
        return
    
    # Start voice interface in background if available
    if VOICE_AVAILABLE:
        jarvis.start_voice_interface()
    
    print("\nChoose interface mode:")
    print("1. 💻 CLI Interface")
    print("2. 🌐 Web Interface") 
    print("3. 🎤 Voice Only (if available)")
    
    choice = input("\nSelect mode (1-3): ").strip()
    
    if choice == '1':
        jarvis.start_cli_interface()
    elif choice == '2':
        jarvis.start_web_interface()
    elif choice == '3' and VOICE_AVAILABLE:
        print("🎤 Voice-only mode active. Say 'Hey JARVIS' to interact.")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n👋 JARVIS signing off. Goodbye!")
    else:
        print("❌ Invalid choice or voice not available")

if __name__ == '__main__':
    main()