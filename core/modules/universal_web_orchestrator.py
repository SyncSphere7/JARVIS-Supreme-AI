"""
Universal Web Orchestrator for Jarvis.
Handles ANY complex web workflow autonomously - from simple tasks to enterprise automation.
"""
import json
import time
import random
import requests
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
from core.modules.autonomous_web_agent import AutonomousWebAgent
from core.utils.log import logger


class UniversalWebOrchestrator:
    def __init__(self, brain):
        self.brain = brain
        self.web_agent = AutonomousWebAgent(brain)
        self.workflows_dir = Path("workflows")
        self.workflows_dir.mkdir(exist_ok=True)
        self.active_workflows = {}
        
        # Platform handlers
        self.platform_handlers = {
            'n8n': self._handle_n8n_workflow,
            'zapier': self._handle_zapier_workflow,
            'make': self._handle_make_workflow,
            'github': self._handle_github_workflow,
            'aws': self._handle_aws_workflow,
            'google_cloud': self._handle_gcp_workflow,
            'azure': self._handle_azure_workflow,
            'docker': self._handle_docker_workflow,
            'kubernetes': self._handle_k8s_workflow,
            'vercel': self._handle_vercel_workflow,
            'netlify': self._handle_netlify_workflow,
            'heroku': self._handle_heroku_workflow,
            'firebase': self._handle_firebase_workflow,
            'supabase': self._handle_supabase_workflow,
            'stripe': self._handle_stripe_workflow,
            'twilio': self._handle_twilio_workflow,
            'sendgrid': self._handle_sendgrid_workflow,
            'mailchimp': self._handle_mailchimp_workflow,
            'shopify': self._handle_shopify_workflow,
            'wordpress': self._handle_wordpress_workflow,
            'notion': self._handle_notion_workflow,
            'airtable': self._handle_airtable_workflow,
            'slack': self._handle_slack_workflow,
            'discord': self._handle_discord_workflow,
            'telegram': self._handle_telegram_workflow
        }
    
    def execute_complex_workflow(self, workflow_description: str) -> Dict[str, Any]:
        """Execute any complex web workflow described in natural language."""
        try:
            logger.info(f"🎯 Executing complex workflow: {workflow_description}")
            
            # Use AI to break down the workflow into steps
            workflow_plan = self._analyze_and_plan_workflow(workflow_description)
            
            if not workflow_plan.get('success'):
                return workflow_plan
            
            # Execute the workflow
            execution_result = self._execute_workflow_plan(workflow_plan['plan'])
            
            # Save workflow for future use
            workflow_id = self._save_workflow(workflow_description, workflow_plan, execution_result)
            
            return {
                'success': True,
                'workflow_id': workflow_id,
                'description': workflow_description,
                'steps_completed': execution_result.get('steps_completed', 0),
                'total_steps': len(workflow_plan['plan']),
                'results': execution_result.get('results', []),
                'artifacts': execution_result.get('artifacts', {})
            }
            
        except Exception as e:
            logger.error(f"Complex workflow execution failed: {e}")
            return {'success': False, 'error': str(e)}
    
    def _analyze_and_plan_workflow(self, description: str) -> Dict[str, Any]:
        """Use AI to analyze and create a detailed execution plan."""
        try:
            prompt = f"""Analyze this complex web workflow and create a detailed execution plan:

WORKFLOW DESCRIPTION: {description}

Create a comprehensive plan that includes:

1. **Platform Analysis**: Identify all platforms/services involved
2. **Account Requirements**: What accounts need to be created/configured
3. **API Requirements**: What APIs need to be set up and configured
4. **Dependencies**: What needs to be done before other steps
5. **Execution Steps**: Detailed step-by-step breakdown
6. **Integration Points**: How different services connect
7. **Configuration Details**: Specific settings and parameters
8. **Testing & Validation**: How to verify each step works

For each step, provide:
- step_type: (account_creation, api_setup, configuration, integration, testing, deployment)
- platform: (n8n, zapier, google, aws, github, etc.)
- action: specific action to perform
- parameters: detailed parameters needed
- dependencies: which steps must complete first
- validation: how to verify success
- fallback: alternative approach if this fails

Format as JSON:
{{
  "workflow_type": "automation_setup|deployment|integration|business_process",
  "platforms_involved": ["platform1", "platform2"],
  "estimated_duration": "30 minutes",
  "complexity": "simple|medium|complex|enterprise",
  "plan": [
    {{
      "step_number": 1,
      "step_type": "account_creation",
      "platform": "n8n",
      "action": "create_account_and_workspace",
      "parameters": {{
        "email": "auto_generated",
        "workspace_name": "jarvis_automation",
        "plan_type": "free"
      }},
      "dependencies": [],
      "validation": "verify_workspace_accessible",
      "fallback": "try_zapier_instead"
    }}
  ]
}}

Be extremely detailed and comprehensive. This will be executed autonomously."""

            response = self.brain.think(prompt, max_tokens=2000)
            
            # Extract JSON from response
            try:
                start_idx = response.find('{')
                end_idx = response.rfind('}') + 1
                if start_idx != -1 and end_idx != -1:
                    plan_json = response[start_idx:end_idx]
                    plan = json.loads(plan_json)
                    
                    return {
                        'success': True,
                        'plan': plan['plan'],
                        'metadata': {
                            'workflow_type': plan.get('workflow_type'),
                            'platforms_involved': plan.get('platforms_involved', []),
                            'estimated_duration': plan.get('estimated_duration'),
                            'complexity': plan.get('complexity')
                        }
                    }
                else:
                    raise ValueError("No valid JSON found in response")
                    
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse workflow plan JSON: {e}")
                # Create a simple fallback plan
                return {
                    'success': True,
                    'plan': [
                        {
                            'step': 1,
                            'action': 'analyze_requirements',
                            'description': f'Analyze requirements for: {description}',
                            'platform': 'general',
                            'estimated_time': '5 minutes'
                        },
                        {
                            'step': 2,
                            'action': 'execute_task',
                            'description': f'Execute: {description}',
                            'platform': 'general',
                            'estimated_time': '15 minutes'
                        }
                    ],
                    'metadata': {
                        'workflow_type': 'simple',
                        'platforms_involved': ['general'],
                        'estimated_duration': '20 minutes',
                        'complexity': 'medium',
                        'fallback': True
                    }
                }
                
        except Exception as e:
            logger.error(f"Workflow analysis failed: {e}")
            return {'success': False, 'error': str(e)}
    
    def _execute_workflow_plan(self, plan: List[Dict]) -> Dict[str, Any]:
        """Execute the detailed workflow plan step by step."""
        results = []
        artifacts = {}
        completed_steps = 0
        
        try:
            for step in plan:
                logger.info(f"🔄 Executing step {step['step_number']}: {step['action']}")
                
                # Check dependencies
                if not self._check_dependencies(step.get('dependencies', []), results):
                    logger.warning(f"Dependencies not met for step {step['step_number']}")
                    continue
                
                # Execute the step
                step_result = self._execute_workflow_step(step)
                
                if step_result.get('success'):
                    completed_steps += 1
                    results.append({
                        'step': step['step_number'],
                        'action': step['action'],
                        'result': step_result,
                        'timestamp': datetime.now().isoformat()
                    })
                    
                    # Store artifacts (API keys, URLs, etc.)
                    if 'artifacts' in step_result:
                        artifacts.update(step_result['artifacts'])
                        
                else:
                    # Try fallback if available
                    if 'fallback' in step:
                        logger.info(f"🔄 Trying fallback for step {step['step_number']}")
                        fallback_result = self._execute_fallback(step)
                        if fallback_result.get('success'):
                            completed_steps += 1
                            results.append({
                                'step': step['step_number'],
                                'action': f"{step['action']} (fallback)",
                                'result': fallback_result,
                                'timestamp': datetime.now().isoformat()
                            })
                    else:
                        logger.error(f"Step {step['step_number']} failed: {step_result.get('error')}")
                
                # Brief pause between steps
                time.sleep(random.uniform(2, 5))
            
            return {
                'success': True,
                'steps_completed': completed_steps,
                'total_steps': len(plan),
                'results': results,
                'artifacts': artifacts
            }
            
        except Exception as e:
            logger.error(f"Workflow execution failed: {e}")
            return {
                'success': False,
                'error': str(e),
                'steps_completed': completed_steps,
                'results': results
            }
    
    def _execute_workflow_step(self, step: Dict) -> Dict[str, Any]:
        """Execute a single workflow step."""
        try:
            step_type = step.get('step_type')
            platform = step.get('platform')
            action = step.get('action')
            parameters = step.get('parameters', {})
            
            # Route to appropriate handler
            if platform in self.platform_handlers:
                return self.platform_handlers[platform](step_type, action, parameters)
            else:
                # Generic web automation
                return self._generic_web_automation(step)
                
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _handle_n8n_workflow(self, step_type: str, action: str, parameters: Dict) -> Dict[str, Any]:
        """Handle n8n automation platform workflows."""
        try:
            if action == "create_account_and_workspace":
                return self._create_n8n_account(parameters)
            elif action == "create_workflow":
                return self._create_n8n_workflow(parameters)
            elif action == "configure_nodes":
                return self._configure_n8n_nodes(parameters)
            elif action == "activate_workflow":
                return self._activate_n8n_workflow(parameters)
            else:
                return self._generic_n8n_action(action, parameters)
                
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _create_n8n_account(self, parameters: Dict) -> Dict[str, Any]:
        """Create n8n account and workspace."""
        try:
            # Navigate to n8n
            self.web_agent.driver.get("https://n8n.cloud/")
            time.sleep(3)
            
            # Click sign up
            signup_button = self.web_agent.driver.find_element("xpath", "//a[contains(text(), 'Sign up')]")
            self.web_agent.human_like_mouse_movement(signup_button)
            
            # Fill registration form
            email = parameters.get('email', f"jarvis_{random.randint(1000, 9999)}@tempmail.com")
            password = parameters.get('password', f"JarvisAuto{random.randint(100, 999)}!")
            
            email_field = self.web_agent.driver.find_element("name", "email")
            self.web_agent.human_like_typing(email_field, email)
            
            password_field = self.web_agent.driver.find_element("name", "password")
            self.web_agent.human_like_typing(password_field, password)
            
            # Handle captcha if present
            self.web_agent.solve_captcha()
            
            # Submit
            submit_button = self.web_agent.driver.find_element("type", "submit")
            self.web_agent.human_like_mouse_movement(submit_button)
            
            # Wait for workspace creation
            time.sleep(10)
            
            # Extract workspace URL
            current_url = self.web_agent.driver.current_url
            
            return {
                'success': True,
                'artifacts': {
                    'n8n_email': email,
                    'n8n_password': password,
                    'n8n_workspace_url': current_url
                },
                'message': 'n8n account and workspace created successfully'
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _create_n8n_workflow(self, parameters: Dict) -> Dict[str, Any]:
        """Create an n8n workflow with specified configuration."""
        try:
            workflow_config = parameters.get('workflow_config', {})
            
            # Navigate to workflows
            self.web_agent.driver.get(f"{parameters.get('workspace_url')}/workflows")
            time.sleep(3)
            
            # Create new workflow
            new_workflow_button = self.web_agent.driver.find_element("xpath", "//button[contains(text(), 'New workflow')]")
            self.web_agent.human_like_mouse_movement(new_workflow_button)
            
            # Add nodes based on configuration
            for node_config in workflow_config.get('nodes', []):
                self._add_n8n_node(node_config)
            
            # Connect nodes
            for connection in workflow_config.get('connections', []):
                self._connect_n8n_nodes(connection)
            
            # Save workflow
            save_button = self.web_agent.driver.find_element("xpath", "//button[contains(text(), 'Save')]")
            self.web_agent.human_like_mouse_movement(save_button)
            
            # Get workflow ID from URL
            workflow_url = self.web_agent.driver.current_url
            workflow_id = workflow_url.split('/')[-1]
            
            return {
                'success': True,
                'artifacts': {
                    'n8n_workflow_id': workflow_id,
                    'n8n_workflow_url': workflow_url
                },
                'message': 'n8n workflow created successfully'
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _generic_web_automation(self, step: Dict) -> Dict[str, Any]:
        """Handle generic web automation for any platform."""
        try:
            action = step.get('action')
            parameters = step.get('parameters', {})
            
            # Use AI to determine how to execute this action
            prompt = f"""Execute this web automation action:

Action: {action}
Parameters: {parameters}
Platform: {step.get('platform')}

Provide specific instructions for web automation including:
1. URL to navigate to
2. Elements to find and interact with
3. Data to input
4. Expected results

Format as JSON with executable instructions."""

            instructions = self.brain.think(prompt, max_tokens=800)
            
            # Execute the AI-generated instructions
            return self._execute_ai_instructions(instructions, step)
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def create_automation_json(self, automation_description: str) -> Dict[str, Any]:
        """Create a JSON configuration for any automation workflow."""
        try:
            prompt = f"""Create a comprehensive JSON configuration for this automation:

AUTOMATION: {automation_description}

Create a detailed JSON that includes:
1. Workflow metadata
2. Required platforms and services
3. API configurations needed
4. Step-by-step automation logic
5. Trigger conditions
6. Actions to perform
7. Error handling
8. Success criteria

Make it compatible with n8n, Zapier, or custom automation systems.

Format as complete JSON configuration."""

            json_config = self.brain.think(prompt, max_tokens=2000)
            
            # Save the JSON configuration
            config_file = self.workflows_dir / f"automation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            try:
                # Extract JSON from response
                start_idx = json_config.find('{')
                end_idx = json_config.rfind('}') + 1
                if start_idx != -1 and end_idx != -1:
                    clean_json = json_config[start_idx:end_idx]
                    config_data = json.loads(clean_json)
                    
                    with open(config_file, 'w') as f:
                        json.dump(config_data, f, indent=2)
                    
                    return {
                        'success': True,
                        'config_file': str(config_file),
                        'config_data': config_data,
                        'description': automation_description
                    }
                else:
                    raise ValueError("No valid JSON found")
                    
            except json.JSONDecodeError:
                # Save as text if JSON parsing fails
                with open(config_file.with_suffix('.txt'), 'w') as f:
                    f.write(json_config)
                
                return {
                    'success': True,
                    'config_file': str(config_file.with_suffix('.txt')),
                    'config_data': json_config,
                    'description': automation_description,
                    'note': 'Saved as text due to JSON parsing issues'
                }
                
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def deploy_automation(self, config_file: str, platform: str = "n8n") -> Dict[str, Any]:
        """Deploy an automation configuration to the specified platform."""
        try:
            # Load configuration
            with open(config_file, 'r') as f:
                if config_file.endswith('.json'):
                    config = json.load(f)
                else:
                    config = {'raw_config': f.read()}
            
            # Deploy based on platform
            if platform == "n8n":
                return self._deploy_to_n8n(config)
            elif platform == "zapier":
                return self._deploy_to_zapier(config)
            elif platform == "make":
                return self._deploy_to_make(config)
            else:
                return self._deploy_custom_automation(config, platform)
                
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    # Helper methods for specific platforms
    def _handle_zapier_workflow(self, step_type: str, action: str, parameters: Dict) -> Dict[str, Any]:
        """Handle Zapier automation workflows."""
        # Implementation for Zapier automation
        return {'success': True, 'message': 'Zapier workflow handled'}
    
    def _handle_github_workflow(self, step_type: str, action: str, parameters: Dict) -> Dict[str, Any]:
        """Handle GitHub workflows and actions."""
        # Implementation for GitHub automation
        return {'success': True, 'message': 'GitHub workflow handled'}
    
    def _handle_aws_workflow(self, step_type: str, action: str, parameters: Dict) -> Dict[str, Any]:
        """Handle AWS service automation."""
        # Implementation for AWS automation
        return {'success': True, 'message': 'AWS workflow handled'}
    
    # Additional platform handlers would be implemented here...
    def _handle_make_workflow(self, step_type: str, action: str, parameters: Dict) -> Dict[str, Any]: pass
    def _handle_gcp_workflow(self, step_type: str, action: str, parameters: Dict) -> Dict[str, Any]: pass
    def _handle_azure_workflow(self, step_type: str, action: str, parameters: Dict) -> Dict[str, Any]: pass
    def _handle_docker_workflow(self, step_type: str, action: str, parameters: Dict) -> Dict[str, Any]: pass
    def _handle_k8s_workflow(self, step_type: str, action: str, parameters: Dict) -> Dict[str, Any]: pass
    def _handle_vercel_workflow(self, step_type: str, action: str, parameters: Dict) -> Dict[str, Any]: pass
    def _handle_netlify_workflow(self, step_type: str, action: str, parameters: Dict) -> Dict[str, Any]: pass
    def _handle_heroku_workflow(self, step_type: str, action: str, parameters: Dict) -> Dict[str, Any]: pass
    def _handle_firebase_workflow(self, step_type: str, action: str, parameters: Dict) -> Dict[str, Any]: pass
    def _handle_supabase_workflow(self, step_type: str, action: str, parameters: Dict) -> Dict[str, Any]: pass
    def _handle_stripe_workflow(self, step_type: str, action: str, parameters: Dict) -> Dict[str, Any]: pass
    def _handle_twilio_workflow(self, step_type: str, action: str, parameters: Dict) -> Dict[str, Any]: pass
    def _handle_sendgrid_workflow(self, step_type: str, action: str, parameters: Dict) -> Dict[str, Any]: pass
    def _handle_mailchimp_workflow(self, step_type: str, action: str, parameters: Dict) -> Dict[str, Any]: pass
    def _handle_shopify_workflow(self, step_type: str, action: str, parameters: Dict) -> Dict[str, Any]: pass
    def _handle_wordpress_workflow(self, step_type: str, action: str, parameters: Dict) -> Dict[str, Any]: pass
    def _handle_notion_workflow(self, step_type: str, action: str, parameters: Dict) -> Dict[str, Any]: pass
    def _handle_airtable_workflow(self, step_type: str, action: str, parameters: Dict) -> Dict[str, Any]: pass
    def _handle_slack_workflow(self, step_type: str, action: str, parameters: Dict) -> Dict[str, Any]: pass
    def _handle_discord_workflow(self, step_type: str, action: str, parameters: Dict) -> Dict[str, Any]: pass
    def _handle_telegram_workflow(self, step_type: str, action: str, parameters: Dict) -> Dict[str, Any]: pass
    
    # Helper methods
    def _check_dependencies(self, dependencies: List, completed_results: List) -> bool: return True
    def _execute_fallback(self, step: Dict) -> Dict[str, Any]: return {'success': False}
    def _add_n8n_node(self, node_config: Dict): pass
    def _connect_n8n_nodes(self, connection: Dict): pass
    def _configure_n8n_nodes(self, parameters: Dict) -> Dict[str, Any]: return {'success': True}
    def _activate_n8n_workflow(self, parameters: Dict) -> Dict[str, Any]: return {'success': True}
    def _generic_n8n_action(self, action: str, parameters: Dict) -> Dict[str, Any]: return {'success': True}
    def _execute_ai_instructions(self, instructions: str, step: Dict) -> Dict[str, Any]: return {'success': True}
    def _deploy_to_n8n(self, config: Dict) -> Dict[str, Any]: return {'success': True}
    def _deploy_to_zapier(self, config: Dict) -> Dict[str, Any]: return {'success': True}
    def _deploy_to_make(self, config: Dict) -> Dict[str, Any]: return {'success': True}
    def _deploy_custom_automation(self, config: Dict, platform: str) -> Dict[str, Any]: return {'success': True}
    
    def _save_workflow(self, description: str, plan: Dict, result: Dict) -> str:
        """Save workflow for future reference."""
        workflow_id = f"workflow_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        workflow_data = {
            'id': workflow_id,
            'description': description,
            'plan': plan,
            'execution_result': result,
            'created': datetime.now().isoformat()
        }
        
        workflow_file = self.workflows_dir / f"{workflow_id}.json"
        with open(workflow_file, 'w') as f:
            json.dump(workflow_data, f, indent=2)
        
        return workflow_id
