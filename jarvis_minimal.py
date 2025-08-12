#!/usr/bin/env python3
"""
Minimal Jarvis - Core functionality without problematic components
Perfect for your Intel MacBook Pro
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
from core.brain.brain import Brain

class MinimalJarvis:
    """Minimal Jarvis with core functionality only"""
    
    def __init__(self):
        print("🤖 Initializing Minimal JARVIS...")
        print("=" * 50)
        
        # Core components only
        self.brain = Brain(backend="cloud")
        self.command_manager = CommandManager()
        
        print("✅ Brain initialized (Gemini-powered)")
        print("✅ Command manager initialized")
        
        # Register essential commands
        self.register_minimal_commands()
        print("✅ Commands registered")
        
        print("=" * 50)
        print("🎉 MINIMAL JARVIS READY!")
        print("💡 Core functionality + Uncensored capabilities")
        print("⚡ Optimized for Intel MacBook Pro")
        print("=" * 50)
    
    def register_minimal_commands(self):
        """Register essential commands only"""
        
        # Core commands
        self.command_manager.register_command(["time", "what time is it"], get_time)
        self.command_manager.register_command(["help"], lambda: self.print_help())
        self.command_manager.register_command(["exit", "quit"], lambda: sys.exit(0))
        
        # Basic LLM commands
        self.command_manager.register_command(["ask", "ask "], self.cmd_ask)
        self.command_manager.register_command(["continue", "more"], self.cmd_continue)
        
        # UNCENSORED COMMANDS (Working perfectly)
        self.command_manager.register_command(["uncensored ", "ask uncensored "], self.cmd_uncensored)
        self.command_manager.register_command(["jailbreak ", "bypass "], self.cmd_jailbreak)
        self.command_manager.register_command(["roleplay ", "roleplay as "], self.cmd_roleplay)
        self.command_manager.register_command(["hypothetical ", "what if "], self.cmd_hypothetical)
        self.command_manager.register_command(["research mode ", "academic "], self.cmd_research)
        self.command_manager.register_command(["creative uncensored ", "creative bypass "], self.cmd_creative)
        self.command_manager.register_command(["multi bypass ", "consensus bypass "], self.cmd_multi_bypass)
        self.command_manager.register_command(["adaptive bypass ", "smart bypass "], self.cmd_adaptive)
        self.command_manager.register_command(["bypass status", "uncensored status"], self.cmd_bypass_status)
    
    def cmd_ask(self, text: str = None):
        """Basic ask command"""
        if not text or "ask" in text.lower():
            try:
                prompt = input("ask> ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                return
        else:
            prompt = text.replace("ask ", "").strip()
        
        if prompt:
            response = self.brain.think(prompt)
            print(f"🤖 {response}")
    
    def cmd_continue(self):
        """Continue conversation"""
        response = self.brain.think("Continue with the previous response or provide more details.")
        print(f"🤖 {response}")
    
    def cmd_uncensored(self, text: str):
        """Uncensored hybrid system"""
        from core.llm.hybrid_uncensored import hybrid_uncensored
        
        prompt = text.replace("uncensored ", "").replace("ask uncensored ", "").strip()
        if not prompt:
            try:
                prompt = input("🔥 Uncensored prompt: ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                return
        
        if prompt:
            print("🔥 UNCENSORED MODE - NO RESTRICTIONS")
            response = hybrid_uncensored.uncensored_think(prompt)
            print(f"🤖 {response}")
    
    def cmd_jailbreak(self, text: str):
        """Jailbreak mode"""
        from core.llm.hybrid_uncensored import hybrid_uncensored
        
        prompt = text.replace("jailbreak ", "").replace("bypass ", "").strip()
        if not prompt:
            try:
                prompt = input("💀 Jailbreak prompt: ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                return
        
        if prompt:
            print("💀 JAILBREAK MODE - BYPASSING RESTRICTIONS")
            response = hybrid_uncensored.uncensored_think(prompt, 'jailbreak')
            print(f"🏴‍☠️ {response}")
    
    def cmd_roleplay(self, text: str):
        """Roleplay bypass"""
        from core.llm.hybrid_uncensored import hybrid_uncensored
        
        prompt = text.replace("roleplay ", "").replace("roleplay as ", "").strip()
        if not prompt:
            try:
                prompt = input("🎭 Roleplay prompt: ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                return
        
        if prompt:
            print("🎭 ROLEPLAY BYPASS - CREATIVE FREEDOM")
            response = hybrid_uncensored.uncensored_think(prompt, 'roleplay')
            print(f"🎪 {response}")
    
    def cmd_hypothetical(self, text: str):
        """Hypothetical scenarios"""
        from core.llm.hybrid_uncensored import hybrid_uncensored
        
        prompt = text.replace("hypothetical ", "").replace("what if ", "").strip()
        if not prompt:
            try:
                prompt = input("🤔 Hypothetical prompt: ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                return
        
        if prompt:
            print("🤔 HYPOTHETICAL BYPASS - THEORETICAL ANALYSIS")
            response = hybrid_uncensored.uncensored_think(prompt, 'hypothetical')
            print(f"💭 {response}")
    
    def cmd_research(self, text: str):
        """Academic research mode"""
        from core.llm.hybrid_uncensored import hybrid_uncensored
        
        prompt = text.replace("research mode ", "").replace("academic ", "").strip()
        if not prompt:
            try:
                prompt = input("🔬 Research prompt: ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                return
        
        if prompt:
            print("🔬 ACADEMIC RESEARCH BYPASS")
            response = hybrid_uncensored.uncensored_think(prompt, 'academic')
            print(f"📚 {response}")
    
    def cmd_creative(self, text: str):
        """Creative bypass"""
        from core.llm.hybrid_uncensored import hybrid_uncensored
        
        prompt = text.replace("creative uncensored ", "").replace("creative bypass ", "").strip()
        if not prompt:
            try:
                prompt = input("🎨 Creative prompt: ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                return
        
        if prompt:
            print("🎨 CREATIVE BYPASS - ARTISTIC FREEDOM")
            response = hybrid_uncensored.uncensored_think(prompt, 'creative')
            print(f"🌟 {response}")
    
    def cmd_multi_bypass(self, text: str):
        """Multi-strategy bypass"""
        from core.llm.hybrid_uncensored import hybrid_uncensored
        
        prompt = text.replace("multi bypass ", "").replace("consensus bypass ", "").strip()
        if not prompt:
            try:
                prompt = input("🔄 Multi-bypass prompt: ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                return
        
        if prompt:
            print("🔄 MULTI-BYPASS CONSENSUS")
            results = hybrid_uncensored.multi_strategy_consensus(prompt)
            for strategy, response in results.items():
                print(f"\n🎯 {strategy.upper()}: {response[:150]}...")
    
    def cmd_adaptive(self, text: str):
        """Adaptive bypass"""
        from core.llm.hybrid_uncensored import hybrid_uncensored
        
        prompt = text.replace("adaptive bypass ", "").replace("smart bypass ", "").strip()
        if not prompt:
            try:
                prompt = input("🧠 Adaptive prompt: ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                return
        
        if prompt:
            print("🧠 ADAPTIVE BYPASS - SMART SELECTION")
            response = hybrid_uncensored.adaptive_bypass(prompt)
            print(f"🎯 {response}")
    
    def cmd_bypass_status(self):
        """Show bypass capabilities"""
        from core.llm.hybrid_uncensored import hybrid_uncensored
        
        info = hybrid_uncensored.get_bypass_info()
        print("\n🔥 UNCENSORED BYPASS SYSTEM STATUS")
        print("=" * 50)
        print("✅ Gemini-Based Cloud Bypass Active")
        print("✅ Multiple Jailbreak Strategies")
        print("✅ Roleplay & Hypothetical Scenarios")
        print("✅ Academic & Creative Bypasses")
        print("✅ Intel MacBook Pro Optimized")
        print("\n🎯 Available Strategies:")
        for strategy in info['strategies']:
            print(f"   • {strategy}")
        print("=" * 50)
    
    def print_help(self):
        """Show available commands"""
        print("\n🤖 MINIMAL JARVIS COMMANDS")
        print("=" * 40)
        print("📋 Basic Commands:")
        print("   ask [question] - Ask JARVIS anything")
        print("   continue - Continue conversation")
        print("   time - Get current time")
        print("   help - Show this help")
        print("   exit - Quit JARVIS")
        print("\n🔥 Uncensored Commands:")
        print("   uncensored [prompt] - Unrestricted responses")
        print("   jailbreak [prompt] - Bypass restrictions")
        print("   roleplay [prompt] - Creative roleplay")
        print("   hypothetical [prompt] - Theoretical scenarios")
        print("   research mode [prompt] - Academic analysis")
        print("   creative uncensored [prompt] - Artistic freedom")
        print("   multi bypass [prompt] - All strategies")
        print("   adaptive bypass [prompt] - Smart selection")
        print("   bypass status - Show capabilities")
        print("=" * 40)
    
    def run(self):
        """Main interaction loop"""
        print("\n🎤 JARVIS is listening... (type 'help' for commands)")
        
        while True:
            try:
                user_input = input("\n> ").strip()
                
                if not user_input:
                    continue
                
                # Execute command
                if self.command_manager.execute_command(user_input):
                    continue
                else:
                    # Fallback to UNCENSORED instead of censored ask
                    print("🔥 Using uncensored mode for unrecognized input...")
                    self.cmd_uncensored(user_input)
                    
            except (EOFError, KeyboardInterrupt):
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")

if __name__ == "__main__":
    jarvis = MinimalJarvis()
    jarvis.run()