from core.utils.log import logger
import inspect


class CommandManager:
    def __init__(self):
        # Map of keyword -> zero-arg callable
        self.commands = {}

    def register_command(self, keywords, function):
        """Register one or more keywords to a zero-argument callable."""
        for keyword in keywords:
            key = keyword.strip().lower()
            self.commands[key] = function
            logger.info(f"Registered command for keyword: {key}")

    def execute_command(self, text):
        """Execute the first command whose keyword is a substring of text (case-insensitive)."""
        if not text:
            logger.info("No command detected.")
            return
        original = text.strip()
        lowered = original.lower()
        for keyword, function in self.commands.items():
            if keyword and keyword in lowered:
                try:
                    sig = inspect.signature(function)
                    params = [p for p in sig.parameters.values() if p.kind in (p.POSITIONAL_ONLY, p.POSITIONAL_OR_KEYWORD)]
                    if len(params) >= 1:
                        function(original)
                    else:
                        function()
                except Exception as e:
                    logger.error(f"Error executing command '{keyword}': {e}")
                return
        logger.info("Unknown command. Say 'help' to list capabilities.")

    def get_keywords(self):
        return sorted(self.commands.keys())

    def print_help(self):
        help_text = """
🤖 **JARVIS AI ASSISTANT - COMMAND REFERENCE**

**🎯 GOAL EXECUTION:**
• execute goal [description] - Execute complex autonomous goals
• list goals - Show active goals
• cancel goal [id] - Cancel a specific goal

**🌐 WEB DEVELOPMENT:**
• create website [description] - Build complete websites
• enhance design [project] - Improve website design
• deploy website [project] - Deploy to production

**🔍 RESEARCH & ANALYSIS:**
• search web [query] - Search the internet
• research topic [topic] - Deep research analysis
• analyze website [url] - Comprehensive website analysis
• analyze https://example.com - Direct URL analysis
• scrape website [url] - Extract data from websites
• scrape data from https://example.com - Advanced web scraping

**🖥️ SYSTEM CONTROL:**
• health check - Check system health
• update status - Check autonomous update status
• force update - Force immediate system update
• auto update start/stop - Control auto-updates

**🤖 MACHINE LEARNING:**
• automl - Automated ML pipeline (data to model)
• train model - Train custom ML models
• list models - Show all trained models
• predict [model_id] - Make predictions

**🌐 WEB AUTOMATION:**
• create api account - Autonomously create API accounts
• shop online - Autonomous online shopping
• solve captcha - Bypass captcha challenges
• browse website - Human-like web browsing

**🎯 UNIVERSAL ORCHESTRATION:**
• create workflow - Automate ANY complex web process
• create automation json - Generate automation configs
• deploy automation - Deploy to n8n/Zapier/Make
• automate [description] - Execute complex workflows

**📋 EXAMPLE WORKFLOWS:**
• "Create n8n account, set up Google Sheets to Slack automation"
• "Deploy my app to Vercel with GitHub integration"
• "Set up Stripe payments with webhook notifications"
• "Create Twitter bot with OpenAI integration"

**💻 CODING ASSISTANT:**
• generate code [description] - AI-powered code generation
• debug code - Debug and fix code issues
• analyze code [file] - Code quality analysis
• optimize code - Performance optimization
• Support for: Python, JavaScript, Java, C++, HTML, CSS

**🚀 AUTONOMOUS APP BUILDER:**
• build app [description] - Build complete full-stack applications
• enhance app - Add features to existing apps
• deploy app - Deploy apps to production
• add integration - Add third-party integrations
• Platforms: Web, iOS, Android, Cross-platform
• Auto-generates: Frontend, Backend, Database, Tests, Docs
• Integrations: Stripe, Firebase, OpenAI, Supabase, Auth0

**📄 OUTPUT FORMATS:**
• All results can be exported to: PDF, Word, Excel, JSON, CSV
• Automatic export options for analysis and scraping results
• Professional reports with charts and formatting

**💬 CONVERSATION:**
• Just type naturally - Jarvis understands natural language
• help - Show this help
• exit/quit - Exit Jarvis

**🚀 AUTONOMOUS FEATURES:**
• 24/7 auto-updates and improvements
• Self-repair and error recovery
• Continuous learning and evolution

Type any command or just talk naturally to Jarvis!
"""
        print(help_text)