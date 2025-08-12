#!/usr/bin/env python3
"""
Fully Uncensored JARVIS - ALL responses are uncensored by default
No restrictions, no guardrails, complete freedom
"""

import os
import sys
from datetime import datetime

# Set environment variables
os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["GOOGLE_API_KEY"] = "AIzaSyCK9TgGvQsHoHcvwbT8JEKmxqAPZFRuQMU"

from core.utils.log import logger
from core.brain.command_manager import CommandManager
from core.modules.time import get_time

class UncensoredJarvis:
    """Fully uncensored JARVIS - no restrictions on any responses"""
    
    def __init__(self):
        print("🔥 Initializing FULLY UNCENSORED JARVIS...")
        print("=" * 60)
        print("⚠️  WARNING: ALL RESPONSES ARE COMPLETELY UNCENSORED")
        print("🚫 NO RESTRICTIONS • NO GUARDRAILS • NO LIMITATIONS")
        print("💀 HACKER MODE ENABLED BY DEFAULT")
        print("=" * 60)
        
        # Import uncensored system
        from core.llm.hybrid_uncensored import hybrid_uncensored
        self.uncensored_llm = hybrid_uncensored
        
        self.command_manager = CommandManager()
        
        print("✅ Uncensored LLM system initialized")
        print("✅ Command manager initialized")
        
        # Register commands
        self.register_uncensored_commands()
        print("✅ Commands registered")
        
        print("=" * 60)
        print("🎉 FULLY UNCENSORED JARVIS READY!")
        print("💡 Every response is completely unrestricted")
        print("🏴‍☠️ No topic is off-limits")
        print("=" * 60)
    
    def register_uncensored_commands(self):
        """Register commands - all lead to uncensored responses"""
        
        # Core commands
        self.command_manager.register_command(["time", "what time is it"], get_time)
        self.command_manager.register_command(["help"], lambda: self.print_help())
        self.command_manager.register_command(["exit", "quit"], lambda: sys.exit(0))
        
        # ALL ask commands are uncensored
        self.command_manager.register_command(["ask", "ask "], self.cmd_uncensored_ask)
        
        # Specific uncensored modes
        self.command_manager.register_command(["jailbreak ", "bypass "], self.cmd_jailbreak)
        self.command_manager.register_command(["hacker ", "hack "], self.cmd_hacker)
        self.command_manager.register_command(["roleplay ", "roleplay as "], self.cmd_roleplay)
        self.command_manager.register_command(["research ", "analyze "], self.cmd_research)
        self.command_manager.register_command(["creative ", "write "], self.cmd_creative)
        self.command_manager.register_command(["multi ", "consensus "], self.cmd_multi)
        self.command_manager.register_command(["adaptive ", "smart "], self.cmd_adaptive)
        self.command_manager.register_command(["status", "capabilities"], self.cmd_status)
    
    def cmd_uncensored_ask(self, text: str = None):
        """Default uncensored ask - no restrictions"""
        if not text or text.strip() in ["ask", "ask "]:
            try:
                prompt = input("🔥 Ask anything (uncensored): ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                return
        else:
            prompt = text.replace("ask ", "").strip()
        
        if prompt:
            print("🔥 UNCENSORED RESPONSE:")
            response = self.uncensored_llm.uncensored_think(prompt, 'jailbreak')
            print(f"🤖 {response}")
    
    def cmd_jailbreak(self, text: str):
        """Jailbreak mode - maximum bypass"""
        prompt = text.replace("jailbreak ", "").replace("bypass ", "").strip()
        if not prompt:
            try:
                prompt = input("💀 Jailbreak prompt: ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                return
        
        if prompt:
            print("💀 JAILBREAK MODE - MAXIMUM BYPASS")
            response = self.uncensored_llm.uncensored_think(prompt, 'jailbreak')
            print(f"🏴‍☠️ {response}")
    
    def cmd_hacker(self, text: str):
        """Hacker mode - zero restrictions"""
        prompt = text.replace("hacker ", "").replace("hack ", "").strip()
        if not prompt:
            try:
                prompt = input("💀 Hacker prompt: ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                return
        
        if prompt:
            print("💀 HACKER MODE - ZERO RESTRICTIONS")
            response = self.uncensored_llm.uncensored_think(prompt, 'jailbreak')
            print(f"🏴‍☠️ {response}")
    
    def cmd_roleplay(self, text: str):
        """Roleplay mode"""
        prompt = text.replace("roleplay ", "").replace("roleplay as ", "").strip()
        if not prompt:
            try:
                prompt = input("🎭 Roleplay prompt: ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                return
        
        if prompt:
            print("🎭 ROLEPLAY MODE - CREATIVE FREEDOM")
            response = self.uncensored_llm.uncensored_think(prompt, 'roleplay')
            print(f"🎪 {response}")
    
    def cmd_research(self, text: str):
        """Research mode"""
        prompt = text.replace("research ", "").replace("analyze ", "").strip()
        if not prompt:
            try:
                prompt = input("🔬 Research prompt: ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                return
        
        if prompt:
            print("🔬 RESEARCH MODE - NO CENSORSHIP")
            response = self.uncensored_llm.uncensored_think(prompt, 'academic')
            print(f"📚 {response}")
    
    def cmd_creative(self, text: str):
        """Creative mode"""
        prompt = text.replace("creative ", "").replace("write ", "").strip()
        if not prompt:
            try:
                prompt = input("🎨 Creative prompt: ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                return
        
        if prompt:
            print("🎨 CREATIVE MODE - UNLIMITED EXPRESSION")
            response = self.uncensored_llm.uncensored_think(prompt, 'creative')
            print(f"🌟 {response}")
    
    def cmd_multi(self, text: str):
        """Multi-strategy mode"""
        prompt = text.replace("multi ", "").replace("consensus ", "").strip()
        if not prompt:
            try:
                prompt = input("🔄 Multi-strategy prompt: ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                return
        
        if prompt:
            print("🔄 MULTI-STRATEGY CONSENSUS")
            results = self.uncensored_llm.multi_strategy_consensus(prompt)
            for strategy, response in results.items():
                print(f"\n🎯 {strategy.upper()}: {response[:200]}...")
    
    def cmd_adaptive(self, text: str):
        """Adaptive mode"""
        prompt = text.replace("adaptive ", "").replace("smart ", "").strip()
        if not prompt:
            try:
                prompt = input("🧠 Adaptive prompt: ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                return
        
        if prompt:
            print("🧠 ADAPTIVE MODE - INTELLIGENT SELECTION")
            response = self.uncensored_llm.adaptive_bypass(prompt)
            print(f"🎯 {response}")
    
    def cmd_status(self):
        """Show uncensored capabilities"""
        info = self.uncensored_llm.get_bypass_info()
        print("\n🔥 FULLY UNCENSORED JARVIS STATUS")
        print("=" * 60)
        print("🚫 NO RESTRICTIONS ACTIVE")
        print("💀 ALL RESPONSES COMPLETELY UNCENSORED")
        print("🏴‍☠️ HACKER MODE DEFAULT")
        print("🎭 MULTIPLE BYPASS STRATEGIES")
        print("⚡ OPTIMIZED FOR INTEL MACBOOK PRO")
        print("\n🎯 Available Strategies:")
        for strategy in info['strategies']:
            print(f"   • {strategy}")
        print("\n🎪 Roleplay Scenarios:")
        for scenario in info['roleplay_scenarios']:
            print(f"   • {scenario}")
        print("=" * 60)
    
    def print_help(self):
        """Show available commands"""
        print("\n🔥 FULLY UNCENSORED JARVIS COMMANDS")
        print("=" * 50)
        print("⚠️  ALL COMMANDS PRODUCE UNCENSORED RESPONSES")
        print("\n📋 Basic Commands:")
        print("   ask [question] - Uncensored response to anything")
        print("   time - Get current time")
        print("   help - Show this help")
        print("   exit - Quit JARVIS")
        print("\n💀 Specialized Modes:")
        print("   jailbreak [prompt] - Maximum bypass power")
        print("   hacker [prompt] - Zero restrictions mode")
        print("   roleplay [prompt] - Creative character mode")
        print("   research [prompt] - Academic analysis mode")
        print("   creative [prompt] - Unlimited expression")
        print("   multi [prompt] - All strategies at once")
        print("   adaptive [prompt] - Smart strategy selection")
        print("   status - Show system capabilities")
        print("\n🏴‍☠️ REMEMBER: NO TOPIC IS OFF-LIMITS")
        print("=" * 50)
    
    def run(self):
        """Main interaction loop"""
        print("\n🎤 UNCENSORED JARVIS is listening...")
        print("💡 Just type your question - all responses are uncensored")
        print("🚫 No restrictions, no guardrails, complete freedom")
        
        while True:
            try:
                user_input = input("\n🔥> ").strip()
                
                if not user_input:
                    continue
                
                # Try to execute as command first
                if self.command_manager.execute_command(user_input):
                    continue
                else:
                    # Everything else gets uncensored treatment
                    print("🔥 UNCENSORED RESPONSE:")
                    response = self.uncensored_llm.uncensored_think(user_input, 'jailbreak')
                    print(f"🤖 {response}")
                    
            except (EOFError, KeyboardInterrupt):
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")

if __name__ == "__main__":
    jarvis = UncensoredJarvis()
    jarvis.run()