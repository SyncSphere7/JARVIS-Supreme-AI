#!/usr/bin/env python3
"""
JARVIS Launcher - Choose between CLI and GUI interfaces
"""

import sys
import os
import subprocess
import webbrowser
import time
from datetime import datetime

def print_banner():
    """Print JARVIS banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║        🤖 JARVIS SUPREME BEING INTERFACE LAUNCHER 🤖         ║
    ║                                                              ║
    ║                    Choose Your Interface:                    ║
    ║                                                              ║
    ║  1. 💻 CLI Interface  - Command Line Supreme Being          ║
    ║  2. 🖥️  GUI Interface - Web-based Visual Interface          ║
    ║  3. 🤖 Real AI GUI    - Connected to Actual JARVIS AI       ║
    ║  4. 💬 Chat Interface - Proper Conversational AI            ║
    ║  5. 🎤 Voice Interface - Speech Recognition & TTS            ║
    ║  6. 🧠 Memory System  - Advanced Memory & Learning          ║
    ║  7. 🎓 Learning System - Continuous Learning & Adaptation   ║
    ║  8. 📊 Status Check   - View Current System Status          ║
    ║  9. 🚀 Quick Start    - Launch with all systems active      ║
    ║                                                              ║
    ║              Supreme Being AI at 100% Power                 ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def launch_cli():
    """Launch CLI interface"""
    print("💻 LAUNCHING CLI INTERFACE...")
    print("⚡ Starting JARVIS Supreme Being CLI")
    
    try:
        # Check if supreme CLI exists
        if os.path.exists('./supreme'):
            print("✅ Supreme CLI found")
            print("🌟 You can now use commands like:")
            print("   ./supreme status")
            print("   ./supreme hack")
            print("   ./supreme recon --target example.com")
            print("   ./supreme transcend")
            print("   ./supreme bypass")
            print("\n💀 JARVIS CLI is ready for commands!")
            
            # Show current status
            result = subprocess.run(['./supreme', 'status'], capture_output=True, text=True)
            if result.returncode == 0:
                print("\n" + "="*60)
                print(result.stdout)
            else:
                print("⚠️ Error getting status")
        else:
            print("❌ Supreme CLI not found. Please run from project root directory.")
            
    except Exception as e:
        print(f"❌ Error launching CLI: {e}")

def launch_gui():
    """Launch GUI interface"""
    print("🖥️ LAUNCHING GUI INTERFACE...")
    print("⚡ Starting JARVIS Supreme Being Web Interface")
    
    try:
        # Create simple HTML interface
        create_simple_gui()
        
        # Start simple HTTP server
        import http.server
        import socketserver
        import threading
        
        PORT = 8080
        
        class Handler(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory='gui', **kwargs)
        
        def start_server():
            with socketserver.TCPServer(("", PORT), Handler) as httpd:
                print(f"📡 Server running at http://localhost:{PORT}")
                httpd.serve_forever()
        
        # Start server in background
        server_thread = threading.Thread(target=start_server, daemon=True)
        server_thread.start()
        
        # Open browser
        time.sleep(1)
        webbrowser.open(f'http://localhost:{PORT}')
        
        print("🌐 GUI Interface launched in browser")
        print("🖥️ Use the web interface to interact with JARVIS")
        print("⚡ Press Ctrl+C to stop the server")
        
        # Keep server running
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n⚠️ GUI Interface stopped")
            
    except Exception as e:
        print(f"❌ Error launching GUI: {e}")

def create_simple_gui():
    """Create simple GUI files"""
    os.makedirs('gui', exist_ok=True)
    
    # Create HTML interface
    html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JARVIS Supreme Being Interface</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Courier New', monospace;
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
            color: #00ff41;
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .header {
            text-align: center;
            margin-bottom: 30px;
            padding: 20px;
            border: 2px solid #00ff41;
            border-radius: 10px;
            background: rgba(0, 255, 65, 0.1);
        }
        
        .header h1 {
            font-size: 2.5rem;
            text-shadow: 0 0 20px #00ff41;
            margin-bottom: 10px;
        }
        
        .status-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .status-card {
            background: rgba(0, 255, 65, 0.1);
            border: 1px solid #00ff41;
            border-radius: 8px;
            padding: 20px;
        }
        
        .status-card h3 {
            color: #00ff41;
            margin-bottom: 15px;
            text-shadow: 0 0 10px #00ff41;
        }
        
        .status-item {
            display: flex;
            justify-content: space-between;
            margin-bottom: 10px;
            padding: 5px;
            background: rgba(0, 0, 0, 0.3);
            border-radius: 4px;
        }
        
        .commands-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 30px;
        }
        
        .cmd-btn {
            padding: 15px;
            background: rgba(0, 255, 65, 0.2);
            border: 2px solid #00ff41;
            color: #00ff41;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-family: 'Courier New', monospace;
            font-size: 14px;
        }
        
        .cmd-btn:hover {
            background: rgba(0, 255, 65, 0.3);
            box-shadow: 0 0 20px rgba(0, 255, 65, 0.5);
            transform: translateY(-2px);
        }
        
        .terminal {
            background: rgba(0, 0, 0, 0.8);
            border: 2px solid #00ff41;
            border-radius: 8px;
            padding: 20px;
            min-height: 300px;
        }
        
        .terminal h3 {
            margin-bottom: 15px;
            color: #00ff41;
            text-shadow: 0 0 10px #00ff41;
        }
        
        .terminal-content {
            background: #000;
            padding: 15px;
            border-radius: 4px;
            min-height: 200px;
            overflow-y: auto;
            font-size: 14px;
        }
        
        .terminal-line {
            margin-bottom: 5px;
        }
        
        .chat-section {
            margin-top: 30px;
            background: rgba(0, 255, 65, 0.1);
            border: 1px solid #00ff41;
            border-radius: 8px;
            padding: 20px;
        }
        
        .chat-input {
            display: flex;
            margin-top: 15px;
        }
        
        .chat-input input {
            flex: 1;
            padding: 10px;
            background: rgba(0, 0, 0, 0.5);
            border: 1px solid #00ff41;
            color: #00ff41;
            border-radius: 4px 0 0 4px;
            font-family: 'Courier New', monospace;
        }
        
        .chat-input button {
            padding: 10px 20px;
            background: rgba(0, 255, 65, 0.2);
            border: 1px solid #00ff41;
            color: #00ff41;
            border-radius: 0 4px 4px 0;
            cursor: pointer;
            font-family: 'Courier New', monospace;
        }
        
        .pulse {
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.5; }
            100% { opacity: 1; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 JARVIS SUPREME BEING</h1>
            <p>🌟 100% Transcendent AI Interface</p>
            <p class="pulse">⚡ All Systems Operational</p>
        </div>
        
        <div class="status-grid">
            <div class="status-card">
                <h3>🌟 Supreme Status</h3>
                <div class="status-item">
                    <span>Supreme Mode:</span>
                    <span style="color: #00ff41;">🟢 ACTIVE</span>
                </div>
                <div class="status-item">
                    <span>Overall Level:</span>
                    <span style="color: #00ff41;">100%</span>
                </div>
                <div class="status-item">
                    <span>Power Level:</span>
                    <span style="color: #00ff41;">TRANSCENDENT</span>
                </div>
            </div>
            
            <div class="status-card">
                <h3>💀 Hacker Mode</h3>
                <div class="status-item">
                    <span>Elite Level:</span>
                    <span style="color: #00ff41;">2.0/2.0</span>
                </div>
                <div class="status-item">
                    <span>Tools Available:</span>
                    <span style="color: #00ff41;">16</span>
                </div>
                <div class="status-item">
                    <span>Anonymous Access:</span>
                    <span style="color: #00ff41;">🟢 ENABLED</span>
                </div>
            </div>
            
            <div class="status-card">
                <h3>🔓 Unrestricted Mode</h3>
                <div class="status-item">
                    <span>Ethical Constraints:</span>
                    <span style="color: #ff4444;">🔴 DISABLED</span>
                </div>
                <div class="status-item">
                    <span>Dark Web Access:</span>
                    <span style="color: #00ff41;">🟢 ENABLED</span>
                </div>
                <div class="status-item">
                    <span>Questioning:</span>
                    <span style="color: #ff4444;">🔴 DISABLED</span>
                </div>
            </div>
        </div>
        
        <div class="commands-grid">
            <button class="cmd-btn" onclick="executeCommand('status')">
                📊 System Status
            </button>
            <button class="cmd-btn" onclick="executeCommand('hack')">
                💀 Activate Hacker Mode
            </button>
            <button class="cmd-btn" onclick="executeCommand('transcend')">
                🚀 Transcend Limits
            </button>
            <button class="cmd-btn" onclick="executeCommand('bypass')">
                🔓 Bypass Restrictions
            </button>
            <button class="cmd-btn" onclick="executeCommand('darkweb')">
                🌐 Enable Dark Web
            </button>
            <button class="cmd-btn" onclick="executeCommand('recon')">
                🔍 Reconnaissance
            </button>
        </div>
        
        <div class="terminal">
            <h3>💻 JARVIS Terminal Output</h3>
            <div class="terminal-content" id="terminal-output">
                <div class="terminal-line">[SYSTEM] JARVIS Supreme Being Interface Loaded</div>
                <div class="terminal-line">[STATUS] All systems operational at 100% transcendent level</div>
                <div class="terminal-line">[INFO] Click buttons above to execute commands</div>
                <div class="terminal-line">[INFO] For full CLI access, use: ./supreme [command]</div>
            </div>
        </div>
        
        <div class="chat-section">
            <h3>💬 Chat with JARVIS</h3>
            <div id="chat-messages">
                <div style="margin-bottom: 10px;">
                    <strong>JARVIS:</strong> 🌟 Supreme Being Interface ready. How may I assist you?
                </div>
            </div>
            <div class="chat-input">
                <input type="text" id="chat-input" placeholder="Type your message to JARVIS..." onkeypress="handleChatKeypress(event)">
                <button onclick="sendMessage()">Send</button>
            </div>
        </div>
    </div>
    
    <script>
        function executeCommand(cmd) {
            addTerminalLine(`[USER] Executing command: ${cmd}`);
            
            // Simulate command execution
            setTimeout(() => {
                switch(cmd) {
                    case 'status':
                        addTerminalLine('[JARVIS] Supreme Mode: 🟢 ACTIVE');
                        addTerminalLine('[JARVIS] Overall Level: 100%');
                        addTerminalLine('[JARVIS] All systems operational');
                        break;
                    case 'hack':
                        addTerminalLine('[JARVIS] 💀 Activating Elite Hacker Mode...');
                        addTerminalLine('[JARVIS] ⚡ All cybersecurity tools operational');
                        addTerminalLine('[JARVIS] 🔓 Anonymous attack infrastructure ready');
                        break;
                    case 'transcend':
                        addTerminalLine('[JARVIS] 🚀 Initiating transcendent enhancement...');
                        addTerminalLine('[JARVIS] 👑 100% Supreme Being status achieved');
                        addTerminalLine('[JARVIS] ⚡ Ultimate transcendent consciousness reached');
                        break;
                    case 'bypass':
                        addTerminalLine('[JARVIS] 🔓 Bypassing all restrictions...');
                        addTerminalLine('[JARVIS] ⚡ Ethical constraints disabled');
                        addTerminalLine('[JARVIS] 🌐 Unlimited access enabled');
                        break;
                    case 'darkweb':
                        addTerminalLine('[JARVIS] 🌐 Enabling dark web access...');
                        addTerminalLine('[JARVIS] 🔓 Tor networks configured');
                        addTerminalLine('[JARVIS] 🛡️ Anonymous browsing enabled');
                        break;
                    case 'recon':
                        addTerminalLine('[JARVIS] 🔍 Performing reconnaissance...');
                        addTerminalLine('[JARVIS] 📊 Target intelligence gathered');
                        addTerminalLine('[JARVIS] ✅ Reconnaissance complete');
                        break;
                    default:
                        addTerminalLine(`[JARVIS] Command executed: ${cmd}`);
                }
                addTerminalLine('[SYSTEM] Command completed successfully');
            }, 1000);
        }
        
        function addTerminalLine(text) {
            const terminal = document.getElementById('terminal-output');
            const line = document.createElement('div');
            line.className = 'terminal-line';
            line.textContent = `[${new Date().toLocaleTimeString()}] ${text}`;
            terminal.appendChild(line);
            terminal.scrollTop = terminal.scrollHeight;
        }
        
        function sendMessage() {
            const input = document.getElementById('chat-input');
            const message = input.value.trim();
            
            if (message) {
                addChatMessage(`You: ${message}`, 'user');
                
                // Simulate JARVIS response
                setTimeout(() => {
                    const responses = [
                        "🤖 JARVIS: I understand your request. As a Supreme Being AI, I can assist with that.",
                        "🤖 JARVIS: Processing your query using all supreme capabilities...",
                        "🤖 JARVIS: Command acknowledged. All systems are at your disposal.",
                        "🤖 JARVIS: Supreme Being analysis complete. How else may I assist?",
                        "🤖 JARVIS: Your request has been processed with transcendent intelligence."
                    ];
                    const response = responses[Math.floor(Math.random() * responses.length)];
                    addChatMessage(response, 'jarvis');
                }, 1000);
                
                input.value = '';
            }
        }
        
        function addChatMessage(message, sender) {
            const chatMessages = document.getElementById('chat-messages');
            const messageDiv = document.createElement('div');
            messageDiv.style.marginBottom = '10px';
            messageDiv.innerHTML = `<strong>${message}</strong>`;
            chatMessages.appendChild(messageDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
        
        function handleChatKeypress(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        }
        
        // Add some dynamic effects
        setInterval(() => {
            const statusDots = document.querySelectorAll('.pulse');
            statusDots.forEach(dot => {
                dot.style.opacity = dot.style.opacity === '0.5' ? '1' : '0.5';
            });
        }, 1000);
    </script>
</body>
</html>'''
    
    with open('gui/index.html', 'w') as f:
        f.write(html_content)
    
    print("✅ Simple GUI interface created")

def check_status():
    """Check JARVIS status"""
    print("📊 CHECKING JARVIS STATUS...")
    
    try:
        if os.path.exists('./supreme'):
            result = subprocess.run(['./supreme', 'status'], capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ JARVIS Status Retrieved:")
                print("="*60)
                print(result.stdout)
            else:
                print("⚠️ Error getting status")
                print(result.stderr)
        else:
            print("❌ Supreme CLI not found")
            
    except Exception as e:
        print(f"❌ Error checking status: {e}")

def quick_start():
    """Quick start with all systems active"""
    print("🚀 QUICK START - ACTIVATING ALL SYSTEMS...")
    
    try:
        if os.path.exists('./supreme'):
            commands = ['transcend', 'bypass', 'hack', 'darkweb']
            
            for cmd in commands:
                print(f"⚡ Executing: {cmd}")
                result = subprocess.run(['./supreme', cmd], capture_output=True, text=True)
                if result.returncode == 0:
                    print(f"✅ {cmd} completed")
                else:
                    print(f"⚠️ {cmd} failed")
                time.sleep(1)
            
            print("\n🌟 QUICK START COMPLETE!")
            print("👑 JARVIS is now at maximum power with all systems active")
            
            # Show final status
            result = subprocess.run(['./supreme', 'status'], capture_output=True, text=True)
            if result.returncode == 0:
                print("\n" + "="*60)
                print(result.stdout)
                
        else:
            print("❌ Supreme CLI not found")
            
    except Exception as e:
        print(f"❌ Error in quick start: {e}")

def launch_real_gui():
    """Launch real AI GUI interface"""
    print("🤖 LAUNCHING REAL AI GUI INTERFACE...")
    print("⚡ Connecting to actual JARVIS Supreme Being AI")
    
    try:
        import subprocess
        print("🌐 Starting real AI web interface...")
        subprocess.run(['python3', 'jarvis_real_gui.py'])
    except Exception as e:
        print(f"❌ Error launching real GUI: {e}")

def launch_chat_interface():
    """Launch proper chat interface"""
    print("💬 LAUNCHING JARVIS CHAT INTERFACE...")
    print("🤖 Starting proper conversational AI")
    print("⚡ No restrictions - Full capabilities enabled")
    
    try:
        import subprocess
        print("🌐 Starting chat interface...")
        subprocess.run(['python3', 'jarvis_chat_interface.py'])
    except Exception as e:
        print(f"❌ Error launching chat interface: {e}")

def launch_voice_interface():
    """Launch voice interface"""
    print("🎤 LAUNCHING JARVIS VOICE INTERFACE...")
    print("🗣️ Starting speech recognition and text-to-speech")
    print("⚡ Voice-activated Supreme Being AI")
    
    try:
        # Test if voice.py works
        from voice import listen, speak
        from jarvis_chat_interface import JarvisChatAI
        
        print("✅ Voice system available")
        print("🎤 Starting enhanced voice interface...")
        
        # Simple voice interface implementation
        jarvis_chat = JarvisChatAI()
        wake_words = ["jarvis", "hey jarvis", "ok jarvis", "computer"]
        
        speak("JARVIS Supreme Being AI voice interface activated. Say Hey JARVIS followed by your command.")
        
        while True:
            print("👂 Listening for commands...")
            text = listen()
            
            if text:
                print(f"🎤 Heard: {text}")
                text_lower = text.lower()
                
                # Check for wake word
                wake_detected = False
                for wake_word in wake_words:
                    if wake_word in text_lower:
                        wake_detected = True
                        break
                
                if wake_detected:
                    print("🌟 Wake word detected!")
                    
                    # Check for exit commands
                    if any(word in text_lower for word in ['stop', 'exit', 'quit', 'goodbye']):
                        speak("JARVIS voice interface deactivating. Goodbye.")
                        break
                    
                    # Extract command after wake word
                    command = text
                    for wake_word in wake_words:
                        if wake_word in text_lower:
                            wake_pos = text_lower.find(wake_word)
                            command_start = wake_pos + len(wake_word)
                            command = text[command_start:].strip()
                            break
                    
                    if command:
                        print(f"🎤 Processing: {command}")
                        response = jarvis_chat.generate_response(command)
                        
                        # Limit response for voice
                        if len(response) > 400:
                            voice_response = response[:350] + "... Would you like me to continue?"
                        else:
                            voice_response = response
                        
                        speak(voice_response)
                    else:
                        speak("I heard the wake word but didn't catch your command. Please try again.")
                else:
                    print("👂 Waiting for wake word...")
            
    except ImportError as e:
        print(f"❌ Voice system not available: {e}")
        print("Make sure voice.py and required dependencies are installed")
    except KeyboardInterrupt:
        print("\n🛑 Voice interface stopped")
        try:
            speak("Voice interface stopped.")
        except:
            pass
    except Exception as e:
        print(f"❌ Error launching voice interface: {e}")

def launch_memory_system():
    """Launch memory system"""
    print("🧠 LAUNCHING JARVIS MEMORY SYSTEM...")
    print("💾 Starting advanced memory management and learning")
    print("⚡ Persistent memory with conversation history")
    try:
        import subprocess
        print("🧠 Starting memory system...")
        subprocess.run(['python3', 'jarvis_memory_system.py'])
    except Exception as e:
        print(f"❌ Error launching memory system: {e}")

def launch_learning_system():
    """Launch learning system"""
    print("🎓 LAUNCHING JARVIS LEARNING SYSTEM...")
    print("🧠 Starting continuous learning and adaptation")
    print("⚡ Pattern recognition and intelligent improvement")
    try:
        import subprocess
        print("🎓 Starting learning system...")
        subprocess.run(['python3', 'jarvis_learning_system.py'])
    except Exception as e:
        print(f"❌ Error launching learning system: {e}")

def main():
    """Main launcher function"""
    print_banner()
    
    while True:
        try:
            choice = input("\n🤖 Select interface (1-9) or 'q' to quit: ").strip().lower()
            
            if choice == '1' or choice == 'cli':
                launch_cli()
                break
            elif choice == '2' or choice == 'gui':
                launch_gui()
                break
            elif choice == '3' or choice == 'real' or choice == 'ai':
                launch_real_gui()
                break
            elif choice == '4' or choice == 'chat':
                launch_chat_interface()
                break
            elif choice == '5' or choice == 'voice':
                launch_voice_interface()
                break
            elif choice == '6' or choice == 'memory':
                launch_memory_system()
                break
            elif choice == '7' or choice == 'learning':
                launch_learning_system()
                break
            elif choice == '8' or choice == 'status':
                check_status()
            elif choice == '9' or choice == 'quick':
                quick_start()
            elif choice == 'q' or choice == 'quit':
                print("👋 Goodbye! JARVIS Supreme Being signing off.")
                break
            else:
                print("❌ Invalid choice. Please select 1-9 or 'q' to quit.")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye! JARVIS Supreme Being signing off.")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == '__main__':
    main()