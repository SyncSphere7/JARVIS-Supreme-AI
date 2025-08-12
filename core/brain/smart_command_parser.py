"""
Smart Command Parser for Jarvis.
Uses AI to understand user intent and route commands correctly.
"""
import re
from typing import Dict, List, Tuple, Optional
from core.utils.log import logger


class SmartCommandParser:
    def __init__(self, brain):
        self.brain = brain
        
        # Command patterns and their intents
        self.command_patterns = {
            'website_analysis': [
                r'analyze.*website.*',
                r'analyze.*site.*',
                r'check.*website.*',
                r'review.*website.*',
                r'audit.*website.*',
                r'analyze.*https?://.*',
                r'analyze.*www\..*',
                r'.*analysis.*of.*website.*',
                r'do.*analysis.*https?://.*',
                r'scrape.*and.*analyze.*',
                r'get.*info.*from.*website.*'
            ],
            'web_scraping': [
                r'scrape.*website.*',
                r'scrape.*data.*from.*',
                r'extract.*data.*from.*',
                r'get.*data.*from.*website.*',
                r'scrape.*https?://.*',
                r'extract.*content.*from.*',
                r'harvest.*data.*',
                r'crawl.*website.*',
                r'scrape.*www\..*'
            ],
            'website_creation': [
                r'create.*website.*',
                r'build.*website.*',
                r'make.*website.*',
                r'generate.*website.*',
                r'design.*website.*',
                r'develop.*website.*',
                r'build.*me.*a.*site.*'
            ],
            'api_creation': [
                r'create.*api.*account.*',
                r'setup.*api.*',
                r'get.*api.*key.*',
                r'register.*api.*'
            ],
            'automation_workflow': [
                r'create.*workflow.*',
                r'automate.*(?!.*analyze)(?!.*website)',  # Don't match if contains analyze or website
                r'setup.*automation.*',
                r'create.*automation.*'
            ],
            'ml_training': [
                r'train.*model.*',
                r'automl.*',
                r'machine.*learning.*',
                r'create.*model.*'
            ],
            'shopping': [
                r'shop.*online.*',
                r'buy.*',
                r'purchase.*',
                r'find.*product.*'
            ],
            'system_health': [
                r'health.*check.*',
                r'system.*status.*',
                r'check.*system.*'
            ],
            'goal_execution': [
                r'execute.*goal.*',
                r'accomplish.*',
                r'complete.*task.*',
                r'do.*this.*',
                r'help.*me.*with.*',
                r'i.*need.*you.*to.*'
            ],
            'research': [
                r'research.*',
                r'find.*information.*about.*',
                r'search.*for.*',
                r'look.*up.*',
                r'investigate.*'
            ],
            'file_operations': [
                r'save.*to.*file.*',
                r'export.*to.*',
                r'create.*report.*',
                r'generate.*document.*',
                r'save.*as.*pdf.*',
                r'export.*as.*excel.*',
                r'create.*word.*document.*'
            ],
            'data_processing': [
                r'process.*data.*',
                r'analyze.*data.*',
                r'clean.*data.*',
                r'transform.*data.*'
            ],
            'code_generation': [
                r'generate.*code.*',
                r'create.*code.*',
                r'write.*code.*',
                r'build.*function.*',
                r'create.*script.*',
                r'generate.*program.*'
            ],
            'code_debugging': [
                r'debug.*code.*',
                r'fix.*code.*',
                r'debug.*error.*',
                r'fix.*bug.*',
                r'troubleshoot.*'
            ],
            'code_analysis': [
                r'analyze.*code.*',
                r'review.*code.*',
                r'check.*code.*',
                r'analyze.*file.*',
                r'code.*quality.*'
            ],
            'code_optimization': [
                r'optimize.*code.*',
                r'improve.*code.*',
                r'refactor.*code.*',
                r'optimize.*performance.*'
            ],
            'app_building': [
                r'build.*app.*',
                r'create.*app.*',
                r'build.*application.*',
                r'create.*application.*',
                r'make.*app.*',
                r'develop.*app.*',
                r'build.*full.*stack.*',
                r'create.*full.*stack.*'
            ],
            'app_enhancement': [
                r'enhance.*app.*',
                r'improve.*app.*',
                r'add.*feature.*',
                r'upgrade.*app.*',
                r'extend.*app.*'
            ],
            'app_deployment': [
                r'deploy.*app.*',
                r'publish.*app.*',
                r'launch.*app.*',
                r'release.*app.*',
                r'go.*live.*'
            ],
            'integration_building': [
                r'add.*integration.*',
                r'integrate.*with.*',
                r'connect.*to.*',
                r'setup.*integration.*',
                r'build.*integration.*'
            ]
        }
    
    def parse_command(self, text: str) -> Dict[str, any]:
        """Parse user command and determine intent."""
        try:
            text_lower = text.lower().strip()
            
            # First, try pattern matching
            intent = self._match_patterns(text_lower)
            
            if intent:
                # Extract parameters based on intent
                parameters = self._extract_parameters(text, intent)
                
                return {
                    'intent': intent,
                    'parameters': parameters,
                    'confidence': 'high',
                    'original_text': text
                }
            
            # If no pattern match, use AI to understand intent
            ai_intent = self._ai_intent_detection(text)
            
            return {
                'intent': ai_intent.get('intent', 'unknown'),
                'parameters': ai_intent.get('parameters', {}),
                'confidence': 'medium',
                'original_text': text,
                'ai_analysis': ai_intent.get('analysis', '')
            }
            
        except Exception as e:
            logger.error(f"Command parsing failed: {e}")
            return {
                'intent': 'unknown',
                'parameters': {},
                'confidence': 'low',
                'error': str(e),
                'original_text': text
            }
    
    def _match_patterns(self, text: str) -> Optional[str]:
        """Match text against command patterns with priority."""
        # Check website analysis first (highest priority)
        if any(re.search(pattern, text) for pattern in self.command_patterns.get('website_analysis', [])):
            return 'website_analysis'

        # Check web scraping second
        if any(re.search(pattern, text) for pattern in self.command_patterns.get('web_scraping', [])):
            return 'web_scraping'

        # Check other patterns
        for intent, patterns in self.command_patterns.items():
            if intent in ['website_analysis', 'web_scraping']:
                continue  # Already checked above

            for pattern in patterns:
                if re.search(pattern, text):
                    return intent
        return None
    
    def _extract_parameters(self, text: str, intent: str) -> Dict[str, any]:
        """Extract parameters based on intent."""
        parameters = {}
        
        if intent == 'website_analysis':
            # Extract URL
            url_pattern = r'https?://[^\s]+|www\.[^\s]+|[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
            urls = re.findall(url_pattern, text)
            if urls:
                parameters['url'] = urls[0]
            
            # Check for deep analysis request
            if any(word in text.lower() for word in ['detailed', 'deep', 'comprehensive', 'full']):
                parameters['deep_analysis'] = True
            else:
                parameters['deep_analysis'] = False
        
        elif intent == 'website_creation':
            # Extract website type/description
            create_words = ['create', 'build', 'make', 'generate', 'design', 'develop']
            website_words = ['website', 'site', 'page']
            
            # Find description after create/website keywords
            for create_word in create_words:
                for website_word in website_words:
                    pattern = f'{create_word}.*{website_word}\\s+(.*?)(?:\\.|$)'
                    match = re.search(pattern, text.lower())
                    if match:
                        parameters['description'] = match.group(1).strip()
                        break
        
        elif intent == 'api_creation':
            # Extract platform
            platforms = ['meta', 'facebook', 'twitter', 'google', 'openai', 'github', 'stripe']
            for platform in platforms:
                if platform in text.lower():
                    parameters['platform'] = platform
                    break
        
        elif intent == 'automation_workflow':
            # Extract workflow description
            workflow_words = ['workflow', 'automation', 'automate']
            for word in workflow_words:
                if word in text.lower():
                    # Get text after the workflow keyword
                    parts = text.lower().split(word)
                    if len(parts) > 1:
                        parameters['description'] = parts[1].strip()
                    break
        
        elif intent == 'ml_training':
            # Extract data file and target
            if 'automl' in text.lower():
                parameters['type'] = 'automl'
            else:
                parameters['type'] = 'custom'
        
        elif intent == 'shopping':
            # Extract item and budget
            buy_words = ['buy', 'purchase', 'shop for', 'find']
            for word in buy_words:
                if word in text.lower():
                    parts = text.lower().split(word)
                    if len(parts) > 1:
                        parameters['item'] = parts[1].strip()
                    break
        
        elif intent == 'goal_execution':
            # Extract goal description
            goal_words = ['execute goal', 'accomplish', 'complete task', 'do this']
            for word in goal_words:
                if word in text.lower():
                    parts = text.lower().split(word)
                    if len(parts) > 1:
                        parameters['goal'] = parts[1].strip()
                    break
        
        return parameters
    
    def _ai_intent_detection(self, text: str) -> Dict[str, any]:
        """Use AI to detect intent when patterns don't match."""
        try:
            prompt = f"""Analyze this user command and determine the intent:

Command: "{text}"

Available intents:
1. website_analysis - User wants to analyze/audit/review an existing website
2. website_creation - User wants to create/build/design a new website
3. api_creation - User wants to create API accounts or get API keys
4. automation_workflow - User wants to create automations or workflows
5. ml_training - User wants to train machine learning models
6. shopping - User wants to buy/purchase/shop for something online
7. system_health - User wants to check system status or health
8. goal_execution - User wants to execute a complex goal or task
9. general_conversation - General chat or questions
10. unknown - Cannot determine intent

Respond with JSON:
{{
  "intent": "detected_intent",
  "confidence": "high|medium|low",
  "parameters": {{"key": "value"}},
  "analysis": "Brief explanation of why this intent was chosen"
}}

Focus on the main action the user wants to perform."""

            response = self.brain.think(prompt, max_tokens=300)
            
            # Try to extract JSON from response
            try:
                import json
                start_idx = response.find('{')
                end_idx = response.rfind('}') + 1
                if start_idx != -1 and end_idx != -1:
                    json_str = response[start_idx:end_idx]
                    return json.loads(json_str)
                else:
                    raise ValueError("No JSON found")
            except:
                # Fallback parsing
                return self._fallback_intent_parsing(response, text)
                
        except Exception as e:
            logger.error(f"AI intent detection failed: {e}")
            return {
                'intent': 'unknown',
                'confidence': 'low',
                'parameters': {},
                'analysis': f'AI analysis failed: {e}'
            }
    
    def _fallback_intent_parsing(self, response: str, original_text: str) -> Dict[str, any]:
        """Fallback intent parsing when JSON extraction fails."""
        response_lower = response.lower()
        
        # Simple keyword matching in AI response
        if 'website_analysis' in response_lower or 'analyze' in response_lower:
            return {'intent': 'website_analysis', 'confidence': 'medium', 'parameters': {}}
        elif 'website_creation' in response_lower or 'create' in response_lower:
            return {'intent': 'website_creation', 'confidence': 'medium', 'parameters': {}}
        elif 'api' in response_lower:
            return {'intent': 'api_creation', 'confidence': 'medium', 'parameters': {}}
        elif 'automation' in response_lower or 'workflow' in response_lower:
            return {'intent': 'automation_workflow', 'confidence': 'medium', 'parameters': {}}
        elif 'machine learning' in response_lower or 'ml' in response_lower:
            return {'intent': 'ml_training', 'confidence': 'medium', 'parameters': {}}
        elif 'shop' in response_lower or 'buy' in response_lower:
            return {'intent': 'shopping', 'confidence': 'medium', 'parameters': {}}
        elif 'health' in response_lower or 'system' in response_lower:
            return {'intent': 'system_health', 'confidence': 'medium', 'parameters': {}}
        elif 'goal' in response_lower or 'execute' in response_lower:
            return {'intent': 'goal_execution', 'confidence': 'medium', 'parameters': {}}
        else:
            return {'intent': 'general_conversation', 'confidence': 'low', 'parameters': {}}
    
    def get_command_suggestions(self, partial_text: str) -> List[str]:
        """Get command suggestions based on partial input."""
        suggestions = []
        partial_lower = partial_text.lower()
        
        # Common command starters
        if partial_lower.startswith('anal'):
            suggestions.extend([
                'analyze website https://example.com',
                'analyze this website for SEO issues',
                'analyze website performance'
            ])
        elif partial_lower.startswith('creat'):
            suggestions.extend([
                'create website for my business',
                'create api account for Meta',
                'create workflow automation',
                'create automation json'
            ])
        elif partial_lower.startswith('exec'):
            suggestions.extend([
                'execute goal build me a landing page',
                'execute goal set up e-commerce store',
                'execute goal create social media automation'
            ])
        elif partial_lower.startswith('auto'):
            suggestions.extend([
                'automl with my dataset',
                'automate social media posting',
                'auto update system'
            ])
        
        return suggestions[:5]  # Return top 5 suggestions
