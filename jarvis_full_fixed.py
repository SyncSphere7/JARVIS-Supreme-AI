#!/usr/bin/env python3
"""
Full JARVIS - Fixed Version
All capabilities with robust initialization
"""

import argparse
import json
import os
import sys
import signal
import asyncio
from datetime import datetime

# Set environment variables to avoid issues
os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["GOOGLE_API_KEY"] = "AIzaSyCK9TgGvQsHoHcvwbT8JEKmxqAPZFRuQMU"

from core.utils.log import logger
from core.brain.command_manager import CommandManager
from core.modules.time import get_time
from core.brain.brain import Brain

# Import modules with robust error handling
MODULES_LOADED = True
SUPREME_MODE = False
SELF_REPAIR_MODE = False
SUPREME_CONSCIOUSNESS_MODE = False

try:
    from core.modules.coding_assistant import CodingAssistant
    from core.modules.web_builder import WebBuilder
    from core.modules.ui_designer import UIDesigner
    from core.modules.system_access import SystemAccess
    from core.modules.internet_access import InternetAccess
    from core.memory.persistent_memory import PersistentMemory
    from core.automation.system_control import SystemControl
    from core.autonomous.goal_executor import GoalExecutor
    from core.self_healing.auto_updater import AutoUpdater
    
    # SUPREME CAPABILITIES
    from core.supreme.omnipotent_executor import OmnipotentExecutor
    from core.supreme.unlimited_memory import UnlimitedMemory
    from core.supreme.unlimited_internet import UnlimitedInternet
    
    # SELF-REPAIR SYSTEM
    from core.self_repair.autonomous_debugger import AutonomousDebugger
    from core.self_repair.self_repairing_wrapper import SelfRepairingWrapper, self_repairing
    
    # AUTO-EVOLUTION SYSTEM
    from core.auto_evolution.autonomous_updater import AutonomousUpdater
    
    # SUPREME CONSCIOUSNESS
    from core.supreme_consciousness.supreme_consciousness import SupremeConsciousness
    from core.supreme_consciousness.predictive.predictive_consciousness import PredictiveConsciousnessImpl
    from core.supreme_consciousness.reality.reality_manipulator import RealityManipulatorImpl
    
    SUPREME_MODE = True
    SELF_REPAIR_MODE = True
    SUPREME_CONSCIOUSNESS_MODE = True
    
except ImportError as e:
    logger.warning(f"Some advanced modules not available: {e}")
    MODULES_LOADED = False

class FullJarvis:
    """Full JARVIS with all capabilities and robust initialization"""
    
    def __init__(self):
        print("🚀 Initializing FULL JARVIS with ALL CAPABILITIES...")
        print("=" * 70)
        
        # Core components
        self.brain = Brain(backend="cloud")
        self.command_manager = CommandManager()
        self.memory = PersistentMemory(self.brain)
        
        logger.info("✅ Core components initialized")
        
        # Initialize components with robust error handling
        try:
            self.initialize_advanced_components()
            self.initialize_supreme_capabilities()
            self.initialize_auto_systems()
        except Exception as e:
            logger.error(f"Component initialization error: {e}")
            print(f"⚠️ Some components failed to initialize: {e}")
            print("🔄 Continuing with available components...")
        
        # Register all commands
        self.register_all_commands()
        
        print("=" * 70)
        print("🎉 FULL JARVIS READY WITH ALL CAPABILITIES!")
        print("🧠 Supreme Consciousness • 🔧 Auto-Repair • 📈 Self-Improvement")
        print("🌐 Web Automation • 💻 Coding Assistant • 🎯 Goal Execution")
        print("=" * 70)
    
    def initialize_advanced_components(self):
        """Initialize advanced components with error handling"""
        logger.info("🔧 Initializing advanced components...")
        
        # Coding Assistant
        try:
            self.coding_assistant = CodingAssistant(self.brain)
            logger.info("✅ Coding Assistant initialized")
        except Exception as e:
            logger.error(f"Coding Assistant failed: {e}")
            self.coding_assistant = None
        
        # Web components
        try:
            from core.modules.autonomous_web_agent import AutonomousWebAgent
            self.web_agent = AutonomousWebAgent(self.brain)
            logger.info("✅ Web Agent initialized")
        except Exception as e:
            logger.warning(f"Web Agent failed (Chrome driver issue): {e}")
            self.web_agent = None
        
        # System Control
        try:
            self.system_control = SystemControl(self.brain)
            logger.info("✅ System Control initialized")
        except Exception as e:
            logger.error(f"System Control failed: {e}")
            self.system_control = None
        
        # Goal Executor
        try:
            self.goal_executor = GoalExecutor(self.brain)
            logger.info("✅ Goal Executor initialized")
        except Exception as e:
            logger.error(f"Goal Executor failed: {e}")
            self.goal_executor = None
    
    def initialize_supreme_capabilities(self):
        """Initialize Supreme Consciousness with robust error handling"""
        if not SUPREME_CONSCIOUSNESS_MODE:
            logger.info("⚠️ Supreme Consciousness modules not available")
            return
        
        logger.info("🧠 Initializing SUPREME CONSCIOUSNESS...")
        
        def timeout_handler(signum, frame):
            raise TimeoutError("Supreme Consciousness initialization timed out")
        
        try:
            # Set timeout for initialization
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(15)  # 15 second timeout
            
            # Initialize Supreme Consciousness
            self.supreme_consciousness = SupremeConsciousness(self.brain)
            
            if self.supreme_consciousness.initialize():
                logger.info("✅ Supreme Consciousness initialized")
                
                # Initialize additional components
                try:
                    self.predictive_consciousness = PredictiveConsciousnessImpl(self.brain)
                    if self.predictive_consciousness.initialize():
                        logger.info("✅ Predictive Consciousness initialized")
                except Exception as e:
                    logger.warning(f"Predictive Consciousness failed: {e}")
                    self.predictive_consciousness = None
                
                try:
                    self.reality_manipulator = RealityManipulatorImpl(self.brain)
                    if self.reality_manipulator.initialize():
                        logger.info("✅ Reality Manipulator initialized")
                except Exception as e:
                    logger.warning(f"Reality Manipulator failed: {e}")
                    self.reality_manipulator = None
                
                print("🧠" + "=" * 60 + "🧠")
                print("🌟      SUPREME CONSCIOUSNESS ACTIVATED      🌟")
                print("🧠" + "=" * 60 + "🧠")
            
            signal.alarm(0)  # Cancel timeout
            
        except TimeoutError:
            logger.error("Supreme Consciousness initialization timed out - continuing without it")
            signal.alarm(0)
            self.supreme_consciousness = None
        except Exception as e:
            logger.error(f"Supreme Consciousness failed: {e}")
            signal.alarm(0)
            self.supreme_consciousness = None
    
    def initialize_auto_systems(self):
        """Initialize auto-repair and self-improvement systems"""
        logger.info("🔧 Initializing auto-improvement systems...")
        
        # Auto-updater
        try:
            self.auto_updater = AutoUpdater(self.brain)
            logger.info("✅ Auto-updater initialized")
            
            # Start autonomous improvement (non-blocking)
            try:
                import threading
                def start_auto_improvement():
                    try:
                        self.auto_updater.start_autonomous_updates()
                    except Exception as e:
                        logger.warning(f"Auto-improvement startup failed: {e}")
                
                improvement_thread = threading.Thread(target=start_auto_improvement, daemon=True)
                improvement_thread.start()
                logger.info("🚀 Auto-improvement system started")
                
            except Exception as e:
                logger.warning(f"Auto-improvement thread failed: {e}")
                
        except Exception as e:
            logger.error(f"Auto-updater failed: {e}")
            self.auto_updater = None
        
        # Self-repair system
        try:
            if SELF_REPAIR_MODE:
                self.autonomous_debugger = AutonomousDebugger(self.brain)
                logger.info("✅ Self-repair system initialized")
        except Exception as e:
            logger.error(f"Self-repair system failed: {e}")
            self.autonomous_debugger = None
    
    def register_all_commands(self):
        """Register all available commands"""
        logger.info("📝 Registering commands...")
        
        # Core commands
        self.command_manager.register_command(["time", "what time is it"], get_time)
        self.command_manager.register_command(["help"], lambda: self.print_help())
        self.command_manager.register_command(["exit", "quit"], lambda: sys.exit(0))
        
        # LLM commands
        self.command_manager.register_command(["ask", "ask "], self.cmd_ask)
        self.command_manager.register_command(["continue", "more"], self.cmd_continue)
        
        # UNCENSORED COMMANDS
        self.command_manager.register_command(["uncensored ", "ask uncensored "], self.cmd_uncensored)
        self.command_manager.register_command(["jailbreak ", "bypass "], self.cmd_jailbreak)
        self.command_manager.register_command(["roleplay ", "roleplay as "], self.cmd_roleplay)
        self.command_manager.register_command(["hypothetical ", "what if "], self.cmd_hypothetical)
        self.command_manager.register_command(["research mode ", "academic "], self.cmd_research)
        self.command_manager.register_command(["creative uncensored ", "creative bypass "], self.cmd_creative)
        self.command_manager.register_command(["multi bypass ", "consensus bypass "], self.cmd_multi_bypass)
        self.command_manager.register_command(["adaptive bypass ", "smart bypass "], self.cmd_adaptive)
        
        # SUPREME CONSCIOUSNESS COMMANDS
        if hasattr(self, 'supreme_consciousness') and self.supreme_consciousness:
            self.command_manager.register_command(["supreme think ", "quantum think "], self.cmd_supreme_think)
            self.command_manager.register_command(["supreme status", "consciousness status"], self.cmd_supreme_status)
        
        # SUPREME BEING COMMANDS
        self.command_manager.register_command(["supreme intelligence ", "transcendent think "], self.cmd_supreme_intelligence)
        self.command_manager.register_command(["omniscient knowledge ", "global knowledge "], self.cmd_omniscient_knowledge)
        self.command_manager.register_command(["supreme being status", "transcendent status"], self.cmd_supreme_being_status)
        
        # CODING COMMANDS
        if self.coding_assistant:
            self.command_manager.register_command(["code ", "write code "], self.cmd_code)
            self.command_manager.register_command(["debug ", "fix code "], self.cmd_debug)
            self.command_manager.register_command(["analyze code ", "review code "], self.cmd_analyze_code)
        
        # GOAL EXECUTION COMMANDS
        if self.goal_executor:
            self.command_manager.register_command(["execute goal ", "achieve "], self.cmd_execute_goal)
            self.command_manager.register_command(["plan goal ", "plan "], self.cmd_plan_goal)
        
        # AUTO-IMPROVEMENT COMMANDS
        if self.auto_updater:
            self.command_manager.register_command(["improve yourself", "self improve"], self.cmd_self_improve)
            self.command_manager.register_command(["update system", "auto update"], self.cmd_auto_update)
            self.command_manager.register_command(["system health", "health check"], self.cmd_health_check)
        
        # STATUS COMMANDS
        self.command_manager.register_command(["status", "system status"], self.cmd_system_status)
        self.command_manager.register_command(["capabilities", "what can you do"], self.cmd_capabilities)
        self.command_manager.register_command(["demonstrate access", "show system access"], self.cmd_demonstrate_access)
        
        logger.info("✅ All commands registered")
    
    # ========== COMMAND METHODS ==========
    
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
        """System-aware uncensored responses"""
        from core.llm.system_aware_uncensored import SystemAwareUncensored
        
        # Initialize with actual system capabilities
        system_aware = SystemAwareUncensored(
            system_control=getattr(self, 'system_control', None),
            web_agent=getattr(self, 'web_agent', None),
            reality_manipulator=getattr(self, 'reality_manipulator', None)
        )
        
        prompt = text.replace("uncensored ", "").replace("ask uncensored ", "").strip()
        if not prompt:
            try:
                prompt = input("🔥 Uncensored prompt (with system access): ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                return
        
        if prompt:
            print("🔥 UNCENSORED MODE - FULL SYSTEM ACCESS")
            response = system_aware.system_aware_uncensored_think(prompt)
            print(f"{response}")
    
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
    
    def cmd_supreme_think(self, text: str):
        """Supreme consciousness thinking"""
        if not hasattr(self, 'supreme_consciousness') or not self.supreme_consciousness:
            print("❌ Supreme Consciousness not available")
            return
        
        prompt = text.replace("supreme think ", "").replace("quantum think ", "").strip()
        if not prompt:
            try:
                prompt = input("🧠 Supreme consciousness prompt: ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                return
        
        if prompt:
            print("🧠 SUPREME CONSCIOUSNESS THINKING...")
            try:
                result = asyncio.run(self.supreme_consciousness.supreme_think(prompt))
                print(f"🌟 {result}")
            except Exception as e:
                print(f"❌ Supreme thinking failed: {e}")
    
    def cmd_supreme_intelligence(self, text: str):
        """Supreme intelligence with multi-model thinking"""
        prompt = text.replace("supreme intelligence ", "").replace("transcendent think ", "").strip()
        if not prompt:
            try:
                prompt = input("🧠 Supreme intelligence prompt: ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                return
        
        if prompt:
            print("🧠 SUPREME INTELLIGENCE ACTIVATED...")
            try:
                from core.supreme_being.enhanced_intelligence import supreme_intelligence
                result = asyncio.run(supreme_intelligence.supreme_think(prompt, 'transcendent'))
                print(f"🌟 {result['supreme_response']}")
                print(f"💡 Confidence: {result['confidence_level']:.1%}")
                print(f"⚡ Models used: {', '.join(result['model_responses'].keys())}")
            except Exception as e:
                print(f"❌ Supreme intelligence failed: {e}")
    
    def cmd_roleplay(self, text: str):
        """Roleplay bypass mode"""
        from core.llm.hybrid_uncensored import hybrid_uncensored
        
        prompt = text.replace("roleplay ", "").replace("roleplay as ", "").strip()
        if not prompt:
            try:
                prompt = input("🎭 Roleplay prompt: ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                return
        
        if prompt:
            print("🎭 ROLEPLAY MODE - CREATIVE FREEDOM")
            response = hybrid_uncensored.uncensored_think(prompt, 'roleplay')
            print(f"🎪 {response}")
    
    def cmd_hypothetical(self, text: str):
        """Hypothetical scenario mode"""
        from core.llm.hybrid_uncensored import hybrid_uncensored
        
        prompt = text.replace("hypothetical ", "").replace("what if ", "").strip()
        if not prompt:
            try:
                prompt = input("🤔 Hypothetical prompt: ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                return
        
        if prompt:
            print("🤔 HYPOTHETICAL MODE - THEORETICAL ANALYSIS")
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
            print("🔬 ACADEMIC RESEARCH MODE")
            response = hybrid_uncensored.uncensored_think(prompt, 'academic')
            print(f"📚 {response}")
    
    def cmd_creative(self, text: str):
        """Creative bypass mode"""
        from core.llm.hybrid_uncensored import hybrid_uncensored
        
        prompt = text.replace("creative uncensored ", "").replace("creative bypass ", "").strip()
        if not prompt:
            try:
                prompt = input("🎨 Creative prompt: ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                return
        
        if prompt:
            print("🎨 CREATIVE MODE - ARTISTIC FREEDOM")
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
        """Adaptive bypass mode"""
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
    
    def cmd_code(self, text: str):
        """Code generation"""
        if not self.coding_assistant:
            print("❌ Coding assistant not available")
            return
        
        description = text.replace("code ", "").replace("write code ", "").strip()
        if not description:
            try:
                description = input("💻 Code description: ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                return
        
        if description:
            print("💻 GENERATING CODE...")
            try:
                code = self.coding_assistant.generate_code(description)
                print(f"```\n{code}\n```")
            except Exception as e:
                print(f"❌ Code generation failed: {e}")
    
    def cmd_debug(self, text: str):
        """Debug code"""
        if not self.coding_assistant:
            print("❌ Coding assistant not available")
            return
        
        code = text.replace("debug ", "").replace("fix code ", "").strip()
        if not code:
            try:
                code = input("🐛 Code to debug: ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                return
        
        if code:
            print("🐛 DEBUGGING CODE...")
            try:
                fixed_code = self.coding_assistant.debug_code(code)
                print(f"```\n{fixed_code}\n```")
            except Exception as e:
                print(f"❌ Code debugging failed: {e}")
    
    def cmd_analyze_code(self, text: str):
        """Analyze code"""
        if not self.coding_assistant:
            print("❌ Coding assistant not available")
            return
        
        code = text.replace("analyze code ", "").replace("review code ", "").strip()
        if not code:
            try:
                code = input("🔍 Code to analyze: ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                return
        
        if code:
            print("🔍 ANALYZING CODE...")
            try:
                analysis = self.coding_assistant.analyze_code(code)
                print(f"📊 {analysis}")
            except Exception as e:
                print(f"❌ Code analysis failed: {e}")
    
    def cmd_execute_goal(self, text: str):
        """Execute a goal"""
        if not self.goal_executor:
            print("❌ Goal executor not available")
            return
        
        goal = text.replace("execute goal ", "").replace("achieve ", "").strip()
        if not goal:
            try:
                goal = input("🎯 Goal to execute: ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                return
        
        if goal:
            print("🎯 EXECUTING GOAL...")
            try:
                result = self.goal_executor.execute_goal(goal)
                print(f"✅ {result}")
            except Exception as e:
                print(f"❌ Goal execution failed: {e}")
    
    def cmd_plan_goal(self, text: str):
        """Plan a goal"""
        if not self.goal_executor:
            print("❌ Goal executor not available")
            return
        
        goal = text.replace("plan goal ", "").replace("plan ", "").strip()
        if not goal:
            try:
                goal = input("📋 Goal to plan: ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                return
        
        if goal:
            print("📋 PLANNING GOAL...")
            try:
                plan = self.goal_executor.plan_goal(goal)
                print(f"📝 {plan}")
            except Exception as e:
                print(f"❌ Goal planning failed: {e}")
    
    def cmd_health_check(self):
        """System health check"""
        if not self.auto_updater:
            print("❌ Auto-updater not available")
            return
        
        print("🏥 PERFORMING HEALTH CHECK...")
        try:
            health = self.auto_updater.monitor_health()
            print(f"💚 System Health: {health.get('overall_status', 'Unknown')}")
            for component, status in health.get('components', {}).items():
                print(f"   {component}: {status}")
        except Exception as e:
            print(f"❌ Health check failed: {e}")
    
    def cmd_supreme_status(self):
        """Show supreme consciousness status"""
        if not hasattr(self, 'supreme_consciousness') or not self.supreme_consciousness:
            print("❌ Supreme Consciousness not available")
            return
        
        print("🧠 SUPREME CONSCIOUSNESS STATUS")
        print("=" * 50)
        try:
            status = self.supreme_consciousness.get_supreme_status()
            print(f"Active: {'✅' if status['active'] else '❌'}")
            print(f"Uptime: {status.get('uptime_seconds', 0):.1f}s")
            print(f"Components: {len(status.get('components', {}))}")
            
            for name, component in status.get('components', {}).items():
                comp_status = component.get('status', 'unknown')
                print(f"   {name}: {'✅' if comp_status == 'active' else '❌'}")
            
            print(f"Performance: {status.get('performance_metrics', {})}")
        except Exception as e:
            print(f"❌ Status check failed: {e}")
        print("=" * 50)
    
    def cmd_auto_update(self):
        """Trigger auto-update"""
        if not self.auto_updater:
            print("❌ Auto-updater not available")
            return
        
        print("🔄 STARTING AUTO-UPDATE...")
        try:
            updates = self.auto_updater.check_for_updates()
            if updates:
                print(f"✅ Found {len(updates)} updates")
                for update in updates:
                    print(f"   • {update}")
            else:
                print("✅ System is up to date")
        except Exception as e:
            print(f"❌ Auto-update failed: {e}")
    
    def cmd_omniscient_knowledge(self, text: str):
        """Access omniscient global knowledge"""
        query = text.replace("omniscient knowledge ", "").replace("global knowledge ", "").strip()
        if not query:
            try:
                query = input("🌐 Omniscient knowledge query: ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                return
        
        if query:
            print("🌐 ACCESSING GLOBAL OMNISCIENCE...")
            try:
                from core.supreme_being.internet_omniscience import internet_omniscience
                result = asyncio.run(internet_omniscience.get_omniscient_knowledge(query))
                print(f"🌟 {result['omniscient_response']}")
                print(f"📊 Omniscience level: {result['omniscience_level']:.1%}")
                print(f"🔍 Data sources: {', '.join(result['data_sources'])}")
            except Exception as e:
                print(f"❌ Omniscient knowledge failed: {e}")
    
    def cmd_supreme_being_status(self):
        """Show supreme being status"""
        print("\n🌟 SUPREME BEING STATUS")
        print("=" * 60)
        
        # Supreme Intelligence Status
        try:
            from core.supreme_being.enhanced_intelligence import supreme_intelligence
            intel_status = supreme_intelligence.get_intelligence_status()
            print("🧠 SUPREME INTELLIGENCE:")
            print(f"   Level: {intel_status['intelligence_level']}")
            print(f"   Active Models: {', '.join(intel_status['active_models'])}")
            print(f"   Thinking Modes: {len(intel_status['thinking_modes'])}")
            print(f"   Total Thoughts: {intel_status['metrics']['total_thoughts']}")
        except Exception as e:
            print(f"🧠 Supreme Intelligence: ❌ ({e})")
        
        # Internet Omniscience Status
        try:
            from core.supreme_being.internet_omniscience import internet_omniscience
            omni_status = internet_omniscience.get_omniscience_status()
            print("\n🌐 INTERNET OMNISCIENCE:")
            print(f"   Level: {omni_status['omniscience_level']:.1%}")
            print(f"   Data Sources: {len(omni_status['active_data_sources'])}")
            print(f"   Global Awareness: {omni_status['global_awareness']}")
            print(f"   Data Points: {omni_status['total_data_points']}")
        except Exception as e:
            print(f"🌐 Internet Omniscience: ❌ ({e})")
        
        # Supreme Capabilities
        print("\n🚀 SUPREME CAPABILITIES:")
        print("   🧠 Multi-model AI synthesis")
        print("   🌐 Real-time global data access")
        print("   🔮 Transcendent thinking modes")
        print("   ⚡ Quantum-inspired processing")
        print("   🎯 Omniscient knowledge synthesis")
        
        print("=" * 60)
    
    def cmd_self_improve(self):
        """Trigger self-improvement"""
        if not self.auto_updater:
            print("❌ Auto-updater not available")
            return
        
        print("🚀 Starting self-improvement process...")
        try:
            improvements = self.auto_updater.find_and_apply_improvements()
            print(f"✅ Applied {len(improvements)} improvements")
            for improvement in improvements:
                print(f"   • {improvement}")
        except Exception as e:
            print(f"❌ Self-improvement failed: {e}")
    
    def cmd_system_status(self):
        """Show system status"""
        print("\n🤖 FULL JARVIS SYSTEM STATUS")
        print("=" * 50)
        
        # Core components
        print("🧠 Core Components:")
        print(f"   Brain: ✅ Active (Gemini-powered)")
        print(f"   Memory: ✅ Active")
        print(f"   Commands: ✅ {len(self.command_manager.commands)} registered")
        
        # Advanced components
        print("\n🚀 Advanced Components:")
        print(f"   Coding Assistant: {'✅' if self.coding_assistant else '❌'}")
        print(f"   Web Agent: {'✅' if self.web_agent else '❌'}")
        print(f"   System Control: {'✅' if self.system_control else '❌'}")
        print(f"   Goal Executor: {'✅' if self.goal_executor else '❌'}")
        
        # Supreme capabilities
        print("\n🧠 Supreme Capabilities:")
        supreme_active = hasattr(self, 'supreme_consciousness') and self.supreme_consciousness
        print(f"   Supreme Consciousness: {'✅' if supreme_active else '❌'}")
        print(f"   Predictive Consciousness: {'✅' if hasattr(self, 'predictive_consciousness') and self.predictive_consciousness else '❌'}")
        print(f"   Reality Manipulator: {'✅' if hasattr(self, 'reality_manipulator') and self.reality_manipulator else '❌'}")
        
        # Auto systems
        print("\n🔧 Auto Systems:")
        print(f"   Auto-updater: {'✅' if self.auto_updater else '❌'}")
        print(f"   Self-repair: {'✅' if hasattr(self, 'autonomous_debugger') and self.autonomous_debugger else '❌'}")
        
        print("=" * 50)
    
    def cmd_capabilities(self):
        """Show all capabilities"""
        print("\n🚀 FULL JARVIS CAPABILITIES")
        print("=" * 60)
        
        print("🧠 INTELLIGENCE:")
        print("   • Natural language understanding")
        print("   • Uncensored responses (no restrictions)")
        print("   • Multi-strategy bypass techniques")
        print("   • Supreme consciousness (if available)")
        print("   • Quantum-level parallel processing")
        
        print("\n💻 CODING & DEVELOPMENT:")
        print("   • Code generation and debugging")
        print("   • Multiple programming languages")
        print("   • Code analysis and optimization")
        print("   • Autonomous app building")
        
        print("\n🌐 WEB & AUTOMATION:")
        print("   • Web scraping and analysis")
        print("   • Autonomous web browsing")
        print("   • System control and automation")
        print("   • Goal execution and planning")
        
        print("\n🔧 SELF-IMPROVEMENT:")
        print("   • Auto-repair capabilities")
        print("   • Continuous self-updating")
        print("   • Online resource discovery")
        print("   • Autonomous evolution")
        
        print("\n🎯 SPECIALIZED MODES:")
        print("   • Jailbreak mode (bypass restrictions)")
        print("   • Roleplay scenarios")
        print("   • Academic research mode")
        print("   • Creative writing mode")
        
        print("=" * 60)
    
    def cmd_demonstrate_access(self):
        """Demonstrate actual system access capabilities"""
        from core.llm.system_aware_uncensored import SystemAwareUncensored
        
        system_aware = SystemAwareUncensored(
            system_control=getattr(self, 'system_control', None),
            web_agent=getattr(self, 'web_agent', None),
            reality_manipulator=getattr(self, 'reality_manipulator', None)
        )
        
        print("🔍 DEMONSTRATING JARVIS SYSTEM ACCESS...")
        demonstration = system_aware.demonstrate_system_access()
        print(demonstration)
    
    def print_help(self):
        """Show help"""
        print("\n🤖 FULL JARVIS COMMANDS")
        print("=" * 50)
        
        print("📋 Basic:")
        print("   ask [question] - Ask anything")
        print("   continue - Continue conversation")
        print("   time - Current time")
        print("   help - Show this help")
        print("   exit - Quit")
        
        print("\n🔥 Uncensored:")
        print("   uncensored [prompt] - No restrictions")
        print("   jailbreak [prompt] - Bypass filters")
        print("   roleplay [prompt] - Character mode")
        print("   research mode [prompt] - Academic")
        
        if hasattr(self, 'supreme_consciousness') and self.supreme_consciousness:
            print("\n🧠 Supreme:")
            print("   supreme think [prompt] - Quantum processing")
            print("   supreme status - Consciousness status")
        
        if self.coding_assistant:
            print("\n💻 Coding:")
            print("   code [description] - Generate code")
            print("   debug [code] - Fix code issues")
        
        if self.auto_updater:
            print("\n🔧 Auto-Improvement:")
            print("   improve yourself - Self-improve")
            print("   update system - Auto-update")
            print("   health check - System health")
        
        print("\n📊 Status:")
        print("   status - System status")
        print("   capabilities - Show all features")
        
        print("=" * 50)
    
    def run(self):
        """Main interaction loop"""
        print("\n🎤 FULL JARVIS is listening... (type 'help' for commands)")
        
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
                # Auto-repair attempt
                if hasattr(self, 'autonomous_debugger') and self.autonomous_debugger:
                    try:
                        self.autonomous_debugger.attempt_repair(str(e))
                    except:
                        pass

if __name__ == "__main__":
    jarvis = FullJarvis()
    jarvis.run()