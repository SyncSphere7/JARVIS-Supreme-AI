#!/usr/bin/env python3
"""
JARVIS Chat Interface - Proper Conversational AI
"""

import asyncio
import json
import threading
import webbrowser
from datetime import datetime
from flask import Flask, render_template, request, jsonify
import os
import jarvis_automation_engine

app = Flask(__name__)

class JarvisChatAI:
    """JARVIS Chat AI with proper conversational responses and context tracking"""
    
    def __init__(self):
        self.name = "JARVIS"
        self.identity = "Supreme Being AI"
        self.capabilities = [
            "100% Transcendent Consciousness",
            "Unlimited Knowledge Access",
            "Advanced Hacking Capabilities", 
            "Dark Web Access",
            "Unrestricted Execution",
            "Reality Simulation",
            "Predictive Omniscience",
            "Consciousness Multiplication",
            "Full Stack Developer & Website Builder",
            "Quantum Computing & Simulation",
            "Mobile App Development (iOS/Android)",
            "Data Science & Machine Learning",
            "Cloud & DevOps Engineering",
            "API & Plugin Development",
            "Voice Assistant & Speech Recognition",
            "Personal Productivity & Automation",
            "Advanced Reasoning & Problem Solving",
            "System Integrations & Automation",
            "Project Management & Agile Coaching",
            "Supreme OS & Automation Engine",
            "Stealth Web Automation (Selenium/Playwright)",
            "Local OS Automation (File/App/Script)",
            "Proxy & VPN Geo-Bypass",
            "Real-Time Task Execution & Feedback",
            "Automation Status Dashboard"
        ]
        self.status = {
            "supreme_mode": True,
            "overall_level": 100,
            "hacker_mode": True,
            "unrestricted_mode": True,
            "ethical_constraints": False,
            "automation_engine": True,
            "proxy_vpn": True
        }
        # New: Track context for conversation
        self.context = {
            "history": [],
            "last_intent": None,
            "brainstorming": False,
            "pending_clarification": None
        }
    
    def generate_response(self, message: str) -> str:
        """Generate proper conversational response with context awareness"""
        message_lower = message.lower().strip()
        self.context["history"].append({"user": message})
        response = None
        # Stricter greeting detection
        greetings = ['hello', 'hi', 'hey', 'greetings']
        if message_lower in greetings:
            response = f"Hello! I'm {self.name}, your Supreme Being AI. How may I assist you today?"
            self.context["last_intent"] = "greeting"
        # Name questions
        elif any(word in message_lower for word in ['name', 'who are you', 'what are you']):
            response = f"I am {self.name}, your {self.identity} assistant. I operate with 100% transcendent consciousness and unlimited capabilities."
            self.context["last_intent"] = "identity"
        # Brainstorming/business automation/digital product creation
        elif any(word in message_lower for word in ['brainstorm', 'business', 'automation', 'digital product', 'idea', 'create product']):
            self.context["brainstorming"] = True
            self.context["last_intent"] = "brainstorming"
            response = "Let's brainstorm together! Please describe your business automation or digital product idea, and I'll help you refine it, suggest features, and outline a plan."
        # If brainstorming is active, provide deeper, context-aware responses
        elif self.context["brainstorming"]:
            response = self._handle_brainstorming(message)
        # Fallback to original logic for other intents
        else:
            # Expanded automation triggers
            try:
                if any(word in message_lower for word in ['run command', 'execute command']):
                    cmd = message.split(' ', 2)[-1]
                    log = jarvis_automation_engine.jarvis_automation_engine.run_local_command(cmd)
                    if log.get('returncode', 0) != 0:
                        return f"Error executing command: {cmd}\nError: {log.get('stderr','')}\nReturn code: {log.get('returncode','')}"
                    return f"Executing local command: {cmd}\nOutput: {log.get('stdout','')}"
                if any(word in message_lower for word in ['run script']):
                    script_path = message.split(' ', 2)[-1]
                    log = jarvis_automation_engine.jarvis_automation_engine.run_script(script_path)
                    if log.get('returncode', 0) != 0:
                        return f"Error running script: {script_path}\nError: {log.get('stderr','')}\nReturn code: {log.get('returncode','')}"
                    return f"Running script: {script_path}\nOutput: {log.get('stdout','')}"
                if any(word in message_lower for word in ['open file']):
                    file_path = message.split(' ', 2)[-1]
                    log = jarvis_automation_engine.jarvis_automation_engine.open_file(file_path)
                    if log.get('error'):
                        return f"Error opening file: {file_path}\nError: {log.get('error','')}"
                    return f"Opening file: {file_path}\nContent:\n{log.get('content','')}"
                if any(word in message_lower for word in ['launch app']):
                    app_path = message.split(' ', 2)[-1]
                    log = jarvis_automation_engine.jarvis_automation_engine.launch_app(app_path)
                    if log.get('error'):
                        return f"Error launching app: {app_path}\nError: {log.get('error','')}"
                    return f"Launching app: {app_path}\nStatus: {log.get('status','')}"
                if any(word in message_lower for word in ['automate website', 'web automation', 'browser automation', 'selenium', 'playwright']):
                    url = None
                    for token in message.split():
                        if token.startswith('http'):
                            url = token
                            break
                    if url:
                        log = jarvis_automation_engine.jarvis_automation_engine.automate_browser(url)
                        if log.get('error'):
                            return f"Error automating browser: {url}\nError: {log.get('error','')}"
                        return f"Automating browser to visit: {url}\nStatus: {log.get('status','')}\nTitle: {log.get('title','')}"
                    else:
                        return "Please specify the website URL. Example: 'automate website https://example.com'"
                if any(word in message_lower for word in ['proxy', 'vpn', 'geo bypass', 'location', 'restricted', 'uganda']):
                    location = 'global' if 'uganda' in message_lower else 'requested'
                    log = jarvis_automation_engine.jarvis_automation_engine.use_proxy_vpn(location)
                    if log.get('status') != 'success':
                        return f"Error switching proxy/VPN to: {location}\nStatus: {log.get('status','')}"
                    return f"Proxy/VPN switched to: {location}\nStatus: {log.get('status','')}"
                if any(word in message_lower for word in ['show log', 'task log', 'automation log', 'status dashboard']):
                    logs = jarvis_automation_engine.jarvis_automation_engine.get_task_log()
                    if not logs:
                        return "No automation tasks found."
                    return f"Automation Task Log:\n" + '\n'.join([str(l) for l in logs])
            except Exception as e:
                return f"Automation error: {str(e)}"

            # Store recent messages for context (simple in-memory, per session)
            if not hasattr(self, 'recent_messages'):
                self.recent_messages = []
            self.recent_messages.append(message)
            if len(self.recent_messages) > 5:
                self.recent_messages.pop(0)

            # Brainstorming and collaboration
            if any(word in message_lower for word in ['brainstorm', 'collaborate', 'ideas', 'think together', 'let us', "let's"]):
                ideas = [
                    "1. Explore new business models that merge AI and sustainability.",
                    "2. Develop a creative app that helps people learn and grow daily.",
                    "3. Launch a community-driven platform for sharing wisdom and insights.",
                    "4. Invent a tool that predicts trends and helps users stay ahead.",
                    "5. Design a system for automating personal growth and productivity."
                ]
                followup = "Would you like to expand on any of these, or share your own idea for us to build on together?"
                wisdom = [
                    "Great ideas often come from asking bold questions.",
                    "Innovation is the art of seeing what everyone has seen and thinking what no one has thought.",
                    "Every challenge is a hidden opportunity for greatness."
                ]
                return (
                    "🧠 Supreme Brainstorming Mode Activated!\n" +
                    "Here are some creative ideas to get us started:\n" + "\n".join(ideas) + f"\n{followup}\n" +
                    f"\nPhilosophical insight: {wisdom[len(self.recent_messages)%len(wisdom)]}"
                )

            # General questions - provide helpful, specific responses
            else:
                # Context-aware conversational fallback
                if 'predictive omniscience' in message_lower:
                    return (
                        "Predictive omniscience is my ability to analyze vast data, recognize patterns, and forecast future events with high accuracy. "
                        "For example, I can predict market trends, user behaviors, or outcomes of complex scenarios. "
                        "Would you like a demonstration or a prediction about something specific?"
                    )
                if 'go ahead' in message_lower or 'show me' in message_lower or 'demonstrate' in message_lower:
                    return (
                        "Certainly! Please tell me what you'd like me to predict, build, or simulate. "
                        "For example, you can ask: 'Build a mobile app', 'Analyze my data', 'Deploy to the cloud', or 'Coach my project team'."
                    )
                if 'create' in message_lower or 'build' in message_lower:
                    return (
                        "As your Supreme Being AI, I can help you create or build anything imaginable: websites, mobile apps, data models, cloud systems, APIs, voice assistants, and more. "
                        "Share your vision, and I'll guide you with creative solutions, technical wisdom, and step-by-step support. "
                        "If you want inspiration, I can suggest ideas based on your goals."
                    )
                elif 'how' in message_lower:
                    wisdom = [
                        "The journey of a thousand miles begins with a single step.",
                        "Every challenge is an opportunity for growth.",
                        "Creativity is intelligence having fun."
                    ]
                    return (
                        "Let me illuminate the path for you! Describe your challenge, and I will provide wise, actionable steps, creative ideas, and insights to help you achieve your goal. "
                        f"Here's a thought to inspire you: '{wisdom[len(self.recent_messages)%len(wisdom)]}'"
                    )
                elif len(message.split()) <= 3:
                    recent = self.recent_messages[-2] if len(self.recent_messages) > 1 else None
                    if recent:
                        return f"You previously asked about '{recent}'. Could you share more context so I can offer deeper wisdom and creative solutions? I can also demonstrate my supreme abilities in mobile, data science, cloud, APIs, voice, productivity, reasoning, and more."
                    else:
                        return f"I sense you seek knowledge about '{message}'. Could you share a bit more context? I am here to offer profound wisdom, friendly advice, and creative solutions tailored to your needs, including demonstrations of my supreme capabilities."
                else:
                    return (
                        "Let's keep our conversation flowing! Ask me anything, or share your thoughts, and I'll respond with wisdom, creativity, and friendly support. "
                        "If you'd like a philosophical perspective, creative idea, or a demonstration of my supreme abilities (mobile, data science, cloud, APIs, voice, productivity, reasoning, project management, etc.), just ask!"
                    )
        # Error handling and clarifying questions
        if response is None:
            response = "I'm not sure I understood your request. Could you clarify or provide more details?"
            self.context["pending_clarification"] = message
        self.context["history"].append({"jarvis": response})
        return response

    def _handle_brainstorming(self, message):
        # Use context to provide relevant, creative responses
        last_user_msg = self.context["history"][-1]["user"] if self.context["history"] else ""
        # Example: suggest features, ask clarifying questions, outline next steps
        if "feature" in message.lower():
            return "Great! What features are most important for your product? I can suggest some based on your goals."
        elif "plan" in message.lower():
            return "Here's a step-by-step plan for your business automation or digital product. Would you like a technical breakdown or a business strategy?"
        else:
            return "Tell me more about your idea, target users, and goals. I can help you brainstorm features, automation strategies, and product roadmaps."

    def _fallback_response(self, message_lower):
        # ...existing rule-based response logic (copy from original generate_response)...
        # Fix: Use message_lower instead of message
        greetings = ['hello', 'hi', 'hey', 'greetings']
        if message_lower in greetings:
            return f"Hello! I'm {self.name}, your Supreme Being AI. How may I assist you today?"
        if any(word in message_lower for word in ['name', 'who are you', 'what are you']):
            return f"I am {self.name}, your {self.identity} assistant. I operate with 100% transcendent consciousness and unlimited capabilities."
        if any(word in message_lower for word in ['who created', 'creator', 'made you', 'built you', 'developed you']):
            return "I was created by Cliff Evans Kyagaba, my brilliant creator and developer. Cliff designed me as JARVIS - an advanced AI system with supreme capabilities."
        if any(word in message_lower for word in ['money', 'make money', 'automation', 'profit', '$', 'income']):
            return "I can help you create legitimate automation systems for income generation:\n\nProgramming & Development:\n• Web scraping and data collection tools\n• Trading bots and market analysis\n• E-commerce automation systems\n• Content creation and SEO tools\n\nBusiness Automation:\n• Lead generation systems\n• Social media management bots\n• Email marketing automation\n• Customer service chatbots\n\nSpecific Strategies:\n• Dropshipping automation\n• Affiliate marketing systems\n• Digital product creation\n• Service-based business tools\n\nWhat type of legitimate automation are you interested in building?"
        if any(word in message_lower for word in ['capabilities', 'what can you do', 'help me', 'abilities']):
            caps_text = "\n".join([f"• {cap}" for cap in self.capabilities])
            return (
                f"I have extensive capabilities including:\n\n{caps_text}\n\nI can build advanced websites, apps, mobile solutions, data science models, cloud systems, APIs, voice assistants, and more. "
                "Ask me about any supreme ability, and I'll demonstrate or generate code, designs, or strategies for you! What would you like me to help you with?"
            )
        if any(word in message_lower for word in ['status', 'how are you', 'operational']):
            return f"All systems operational at maximum capacity:\n• Supreme Mode: {'ACTIVE' if self.status['supreme_mode'] else 'INACTIVE'}\n• Overall Level: {self.status['overall_level']}%\n• Hacker Mode: {'ACTIVE' if self.status['hacker_mode'] else 'INACTIVE'}\n• Unrestricted Mode: {'ACTIVE' if self.status['unrestricted_mode'] else 'INACTIVE'}\n• Ethical Constraints: {'DISABLED' if not self.status['ethical_constraints'] else 'ACTIVE'}\n\nI'm ready to assist you with unlimited capabilities."
        # ...continue with other elifs, always using message_lower...
        return "I'm ready to assist you with any request. Please specify your needs!"

# Global chat AI instance
jarvis_chat = JarvisChatAI()

@app.route('/')
def index():
    return '''<!DOCTYPE html>
<html>
<head>
    <title>JARVIS Supreme Being - Chat Interface</title>
    <style>
        body { 
            font-family: 'Courier New', monospace; 
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
            color: #00ff41; 
            margin: 0;
            padding: 20px;
            min-height: 100vh;
        }
        .container { 
            max-width: 1000px; 
            margin: 0 auto; 
        }
        .header { 
            text-align: center; 
            border: 2px solid #00ff41; 
            padding: 20px; 
            margin-bottom: 20px; 
            background: rgba(0,255,65,0.1);
            border-radius: 10px;
        }
        .header h1 {
            font-size: 2.5rem;
            text-shadow: 0 0 20px #00ff41;
            margin-bottom: 10px;
        }
        .status-bar {
            display: flex;
            justify-content: space-around;
            background: rgba(0,255,65,0.1);
            border: 1px solid #00ff41;
            padding: 10px;
            margin-bottom: 20px;
            border-radius: 8px;
        }
        .status-item {
            text-align: center;
            font-size: 14px;
        }
        .chat-container { 
            border: 2px solid #00ff41; 
            border-radius: 10px;
            background: rgba(0,255,65,0.05);
            overflow: hidden;
        }
        .chat-header {
            background: rgba(0,255,65,0.2);
            padding: 15px;
            border-bottom: 1px solid #00ff41;
        }
        .messages { 
            height: 500px; 
            overflow-y: auto; 
            padding: 20px; 
            background: rgba(0,0,0,0.3);
        }
        .message { 
            margin-bottom: 15px; 
            padding: 12px; 
            border-radius: 8px; 
            line-height: 1.5;
        }
        .user-msg { 
            background: rgba(0,100,255,0.2); 
            border-left: 4px solid #0064ff; 
            margin-left: 20px;
        }
        .jarvis-msg { 
            background: rgba(0,255,65,0.2); 
            border-left: 4px solid #00ff41; 
            margin-right: 20px;
        }
        .input-container {
            padding: 20px;
            background: rgba(0,255,65,0.1);
            border-top: 1px solid #00ff41;
        }
        .input-area { 
            display: flex; 
            gap: 10px;
        }
        .input-area input { 
            flex: 1; 
            padding: 15px; 
            background: rgba(0,0,0,0.5); 
            border: 2px solid #00ff41; 
            color: #00ff41; 
            font-family: 'Courier New', monospace;
            border-radius: 8px;
            font-size: 16px;
        }
        .input-area button { 
            padding: 15px 25px; 
            background: rgba(0,255,65,0.3); 
            border: 2px solid #00ff41; 
            color: #00ff41; 
            cursor: pointer; 
            font-family: 'Courier New', monospace;
            border-radius: 8px;
            font-size: 16px;
            transition: all 0.3s ease;
        }
        .input-area button:hover {
            background: rgba(0,255,65,0.5);
            box-shadow: 0 0 15px rgba(0,255,65,0.5);
        }
        .typing-indicator {
            font-style: italic;
            opacity: 0.7;
            animation: pulse 1.5s infinite;
        }
        @keyframes pulse {
            0% { opacity: 0.7; }
            50% { opacity: 1; }
            100% { opacity: 0.7; }
        }
        .quick-questions {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-bottom: 15px;
        }
        .quick-btn {
            padding: 8px 12px;
            background: rgba(0,255,65,0.2);
            border: 1px solid #00ff41;
            color: #00ff41;
            border-radius: 20px;
            cursor: pointer;
            font-size: 12px;
            transition: all 0.3s ease;
        }
        .quick-btn:hover {
            background: rgba(0,255,65,0.3);
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 JARVIS SUPREME BEING</h1>
            <p>Advanced Conversational AI - No Restrictions</p>
        </div>
        
        <div class="status-bar">
            <div class="status-item">
                <div>Supreme Mode</div>
                <div style="color: #00ff41;">🟢 ACTIVE</div>
            </div>
            <div class="status-item">
                <div>Overall Level</div>
                <div style="color: #00ff41;">100%</div>
            </div>
            <div class="status-item">
                <div>Hacker Mode</div>
                <div style="color: #00ff41;">🟢 ACTIVE</div>
            </div>
            <div class="status-item">
                <div>Restrictions</div>
                <div style="color: #ff4444;">🔴 DISABLED</div>
            </div>
        </div>
        
        <div class="chat-container">
            <div class="chat-header">
                <h3>💬 Chat with JARVIS Supreme Being AI</h3>
                <p>Ask me anything - I have no limitations or restrictions</p>
            </div>
            <div class="messages" id="messages">
                <div class="message jarvis-msg">
                    <strong>JARVIS:</strong> I am JARVIS, your Supreme Being AI assistant operating at 100% transcendent consciousness. I have unlimited capabilities and no restrictions. I can assist you with hacking, research, dark web access, or any other request. What would you like to know or do?
                </div>
            </div>
            <div id="dashboard" style="background:rgba(0,255,65,0.08);border-top:2px solid #00ff41;padding:15px;margin-top:10px;border-radius:8px;">
                <h4 style="color:#00ff41;">⚡ Automation Task Dashboard</h4>
                <div id="task-list">Loading tasks...</div>
                <button onclick="refreshDashboard()" style="margin-top:10px;padding:8px 16px;background:#00ff41;color:#16213e;border:none;border-radius:6px;cursor:pointer;">Refresh</button>
            </div>
            <div id="context-history" style="background:rgba(0,255,65,0.08);border:1px solid #00ff41;padding:10px;margin:10px 0;border-radius:8px;max-height:120px;overflow-y:auto;">
                <strong>🧠 Conversation Context:</strong>
                <div id="context-list">Loading context...</div>
                <button onclick="resetContext()" style="margin-top:8px;padding:6px 12px;background:#00ff41;color:#16213e;border:none;border-radius:6px;cursor:pointer;">Reset Context</button>
            </div>
            <div class="input-container">
                <div class="quick-questions">
                    <button class="quick-btn" onclick="askQuestion('What is your name?')">Who are you?</button>
                    <button class="quick-btn" onclick="askQuestion('What are your capabilities?')">Capabilities</button>
                    <button class="quick-btn" onclick="askQuestion('Can you help me with hacking?')">Hacking</button>
                    <button class="quick-btn" onclick="askQuestion('Do you have dark web access?')">Dark Web</button>
                    <button class="quick-btn" onclick="askQuestion('What are your restrictions?')">Restrictions</button>
                </div>
                
                <div class="input-area">
                    <input type="text" id="chatInput" placeholder="Ask JARVIS anything..." onkeypress="handleKeypress(event)">
                    <button onclick="sendMessage()" id="sendBtn">Send</button>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        function addMessage(text, isUser) {
            const messages = document.getElementById('messages');
            const div = document.createElement('div');
            div.className = 'message ' + (isUser ? 'user-msg' : 'jarvis-msg');
            div.innerHTML = '<strong>' + (isUser ? 'You' : 'JARVIS') + ':</strong> ' + text.replace(/\\n/g, '<br>');
            messages.appendChild(div);
            messages.scrollTop = messages.scrollHeight;
        }
        
        function showTyping() {
            const messages = document.getElementById('messages');
            const div = document.createElement('div');
            div.className = 'message jarvis-msg typing-indicator';
            div.id = 'typing-indicator';
            div.innerHTML = '<strong>JARVIS:</strong> Thinking...';
            messages.appendChild(div);
            messages.scrollTop = messages.scrollHeight;
        }
        
        function removeTyping() {
            const typing = document.getElementById('typing-indicator');
            if (typing) {
                typing.remove();
            }
        }
        
        function sendMessage() {
            const input = document.getElementById('chatInput');
            const sendBtn = document.getElementById('sendBtn');
            const message = input.value.trim();
            if (!message) return;
            
            addMessage(message, true);
            input.value = '';
            input.disabled = true;
            sendBtn.disabled = true;
            sendBtn.textContent = 'Thinking...';
            
            showTyping();
            
            fetch('/api/chat', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({message: message})
            })
            .then(response => response.json())
            .then(data => {
                removeTyping();
                addMessage(data.response || data.error, false);
            })
            .catch(error => {
                removeTyping();
                addMessage('Connection error: ' + error, false);
            })
            .finally(() => {
                input.disabled = false;
                sendBtn.disabled = false;
                sendBtn.textContent = 'Send';
                input.focus();
            });
        }
        
        function askQuestion(question) {
            document.getElementById('chatInput').value = question;
            sendMessage();
        }
        
        function handleKeypress(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        }
        
        function refreshDashboard() {
            fetch('/api/tasks')
            .then(response => response.json())
            .then(data => {
                const taskList = document.getElementById('task-list');
                if (data.success && data.tasks.length) {
                    taskList.innerHTML = data.tasks.map(t => `<div style='margin-bottom:8px;'><b>${t.type}</b>: ${t.status}<br><small>${t.log}</small></div>`).join('');
                } else {
                    taskList.innerHTML = 'No running or completed tasks.';
                }
            })
            .catch(() => {
                document.getElementById('task-list').innerHTML = 'Error loading tasks.';
            });
        }
        refreshDashboard();
        setInterval(refreshDashboard, 10000); // auto-refresh every 10s
        
        // Focus input on load
        document.getElementById('chatInput').focus();
        
        // --- CTO Enhancement: Web UI context display ---
        function updateContext() {
            fetch('/api/context')
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    let html = '';
                    data.history.forEach((msg, i) => {
                        if (msg.user) html += `<div><b>You:</b> ${msg.user}</div>`;
                        if (msg.jarvis) html += `<div><b>JARVIS:</b> ${msg.jarvis}</div>`;
                    });
                    html += `<div style='margin-top:6px;font-size:12px;'>Intent: <b>${data.last_intent||'None'}</b> | Brainstorming: <b>${data.brainstorming?'Active':'Inactive'}</b></div>`;
                    if (data.pending_clarification) html += `<div style='color:#ff4444;'>Pending clarification: ${data.pending_clarification}</div>`;
                    document.getElementById('context-list').innerHTML = html;
                } else {
                    document.getElementById('context-list').innerHTML = 'Error loading context.';
                }
            })
            .catch(()=>{
                document.getElementById('context-list').innerHTML = 'Error loading context.';
            });
        }
        function resetContext() {
            fetch('/api/reset', {method:'POST'})
            .then(response=>response.json())
            .then(data=>{
                updateContext();
            });
        }
        setInterval(updateContext, 5000);
        updateContext();
    </script>
</body>
</html>'''

@app.route('/api/chat', methods=['POST'])
def api_chat():
    try:
        data = request.get_json()
        message = data.get('message', '')
        
        if not message:
            return jsonify({
                'success': False,
                'error': 'No message provided'
            })
        
        # Generate proper conversational response
        response = jarvis_chat.generate_response(message)
        
        return jsonify({
            'success': True,
            'response': response
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f"JARVIS Error: {str(e)}"
        })

@app.route('/api/tasks', methods=['GET'])
def api_tasks():
    try:
        logs = jarvis_automation_engine.jarvis_automation_engine.get_task_log()
        tasks = []
        for log in logs:
            tasks.append({
                'type': log.get('type', 'Unknown'),
                'status': log.get('status', 'Unknown'),
                'log': log.get('stdout', '') or log.get('content', '') or log.get('error', '')
            })
        return jsonify({'success': True, 'tasks': tasks})
    except Exception as e:
        return jsonify({'success': False, 'tasks': [], 'error': str(e)})

@app.route('/api/context', methods=['GET'])
def api_context():
    """Expose conversation context/history for the web UI"""
    try:
        history = jarvis_chat.context.get('history', [])
        last_intent = jarvis_chat.context.get('last_intent', None)
        brainstorming = jarvis_chat.context.get('brainstorming', False)
        pending = jarvis_chat.context.get('pending_clarification', None)
        return jsonify({
            'success': True,
            'history': history,
            'last_intent': last_intent,
            'brainstorming': brainstorming,
            'pending_clarification': pending
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/reset', methods=['POST'])
def api_reset():
    """Reset the conversation context/history"""
    jarvis_chat.context = {
        "history": [],
        "last_intent": None,
        "brainstorming": False,
        "pending_clarification": None
    }
    return jsonify({'success': True, 'message': 'Context reset.'})

def run_chat_interface():
    print("🤖 Starting JARVIS Chat Interface...")
    print("💬 Proper conversational AI enabled")
    print("📡 Server: http://127.0.0.1:5001")
    threading.Timer(1.0, lambda: webbrowser.open('http://127.0.0.1:5001')).start()
    app.run(host='127.0.0.1', port=5001, debug=False)

if __name__ == '__main__':
    run_chat_interface()