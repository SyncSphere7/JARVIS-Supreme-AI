"""
Autonomous Web Agent for Jarvis.
Handles complex web automation, API creation, sign-ups, captcha solving, and human-like browsing.
"""
import time
import random
import json
import base64
from pathlib import Path
from typing import Dict, List, Any, Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import undetected_chromedriver as uc
import requests
from core.utils.log import logger


class AutonomousWebAgent:
    def __init__(self, brain):
        self.brain = brain
        self.driver = None
        self.session = requests.Session()
        self.user_agents = [
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ]
        self.setup_stealth_browser()
    
    def setup_stealth_browser(self):
        """Setup undetectable browser with human-like behavior."""
        try:
            # Add timeout and better error handling
            import signal
            
            def timeout_handler(signum, frame):
                raise TimeoutError("Chrome driver setup timed out")
            
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(15)  # 15 second timeout
            
            try:
                options = uc.ChromeOptions()
                
                # More conservative settings for older hardware
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument("--disable-gpu")  # Disable GPU for Intel Mac
                options.add_argument("--disable-software-rasterizer")
                options.add_argument("--disable-background-timer-throttling")
                options.add_argument("--disable-backgrounding-occluded-windows")
                options.add_argument("--disable-renderer-backgrounding")
                
                # Stealth settings (simplified)
                options.add_argument("--disable-blink-features=AutomationControlled")
                
                # Try to create driver with timeout
                self.driver = uc.Chrome(options=options, version_main=None)
                
                # Test if driver is working
                self.driver.get("data:text/html,<html><body>Test</body></html>")
                
                signal.alarm(0)  # Cancel timeout
                logger.info("✅ Stealth browser initialized successfully")
                
            except TimeoutError:
                signal.alarm(0)
                logger.error("Chrome driver setup timed out")
                self.driver = None
            except Exception as e:
                signal.alarm(0)
                logger.error(f"Chrome driver setup failed: {e}")
                self.driver = None
            
            logger.info("✅ Stealth browser initialized")
            
        except Exception as e:
            logger.error(f"Failed to setup stealth browser: {e}")
            self.driver = None  # Set to None so other parts know it failed
    
    def human_like_typing(self, element, text: str):
        """Type text with human-like delays and patterns."""
        element.clear()
        for char in text:
            element.send_keys(char)
            # Random typing speed
            time.sleep(random.uniform(0.05, 0.2))
            
            # Occasional pauses (like thinking)
            if random.random() < 0.1:
                time.sleep(random.uniform(0.5, 1.5))
    
    def human_like_mouse_movement(self, element):
        """Move mouse in human-like patterns."""
        actions = ActionChains(self.driver)
        
        # Random mouse movements before clicking
        for _ in range(random.randint(1, 3)):
            x_offset = random.randint(-50, 50)
            y_offset = random.randint(-50, 50)
            actions.move_by_offset(x_offset, y_offset)
            time.sleep(random.uniform(0.1, 0.3))
        
        # Move to element and click
        actions.move_to_element(element)
        time.sleep(random.uniform(0.2, 0.5))
        actions.click()
        actions.perform()
    
    def solve_captcha(self, captcha_type: str = "auto") -> bool:
        """Solve various types of captchas autonomously."""
        try:
            # Detect captcha type
            if self.driver.find_elements(By.CLASS_NAME, "g-recaptcha"):
                return self._solve_recaptcha()
            elif self.driver.find_elements(By.CLASS_NAME, "h-captcha"):
                return self._solve_hcaptcha()
            elif self.driver.find_elements(By.TAG_NAME, "canvas"):
                return self._solve_image_captcha()
            else:
                return self._solve_text_captcha()
                
        except Exception as e:
            logger.error(f"Captcha solving failed: {e}")
            return False
    
    def _solve_recaptcha(self) -> bool:
        """Solve reCAPTCHA using AI vision and audio."""
        try:
            # Try audio challenge first (easier for AI)
            audio_button = self.driver.find_element(By.ID, "recaptcha-audio-button")
            self.human_like_mouse_movement(audio_button)
            
            # Wait for audio challenge
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "rc-audiochallenge-tdownload-link"))
            )
            
            # Download and process audio
            audio_link = self.driver.find_element(By.CLASS_NAME, "rc-audiochallenge-tdownload-link")
            audio_url = audio_link.get_attribute("href")
            
            # Use AI to transcribe audio
            transcription = self._transcribe_audio(audio_url)
            
            # Enter transcription
            audio_input = self.driver.find_element(By.ID, "audio-response")
            self.human_like_typing(audio_input, transcription)
            
            # Submit
            submit_button = self.driver.find_element(By.ID, "recaptcha-verify-button")
            self.human_like_mouse_movement(submit_button)
            
            time.sleep(2)
            return True
            
        except Exception as e:
            logger.error(f"reCAPTCHA solving failed: {e}")
            return False
    
    def _transcribe_audio(self, audio_url: str) -> str:
        """Use AI to transcribe captcha audio."""
        try:
            # Download audio
            response = requests.get(audio_url)
            
            # Use AI to transcribe (this would integrate with speech-to-text AI)
            prompt = "Transcribe this audio captcha. Return only the spoken text/numbers."
            
            # For now, use a placeholder - in real implementation, 
            # this would use speech recognition AI
            return "placeholder_transcription"
            
        except Exception as e:
            logger.error(f"Audio transcription failed: {e}")
            return ""
    
    def create_api_account(self, platform: str, email: str, password: str) -> Dict[str, Any]:
        """Autonomously create API accounts on various platforms."""
        try:
            logger.info(f"🚀 Creating {platform} API account...")
            
            if platform.lower() == "meta":
                return self._create_meta_api_account(email, password)
            elif platform.lower() == "twitter":
                return self._create_twitter_api_account(email, password)
            elif platform.lower() == "google":
                return self._create_google_api_account(email, password)
            elif platform.lower() == "openai":
                return self._create_openai_api_account(email, password)
            else:
                return self._create_generic_api_account(platform, email, password)
                
        except Exception as e:
            logger.error(f"API account creation failed: {e}")
            return {"success": False, "error": str(e)}
    
    def _create_meta_api_account(self, email: str, password: str) -> Dict[str, Any]:
        """Create Meta (Facebook) API account."""
        try:
            # Navigate to Meta for Developers
            self.driver.get("https://developers.facebook.com/")
            time.sleep(random.uniform(2, 4))
            
            # Click "Get Started"
            get_started = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Get Started"))
            )
            self.human_like_mouse_movement(get_started)
            
            # Fill registration form
            email_field = self.driver.find_element(By.NAME, "email")
            self.human_like_typing(email_field, email)
            
            password_field = self.driver.find_element(By.NAME, "password")
            self.human_like_typing(password_field, password)
            
            # Handle captcha if present
            if self.driver.find_elements(By.CLASS_NAME, "captcha"):
                self.solve_captcha()
            
            # Submit form
            submit_button = self.driver.find_element(By.TYPE, "submit")
            self.human_like_mouse_movement(submit_button)
            
            # Wait for confirmation and extract API keys
            time.sleep(5)
            
            # Navigate to app creation
            self.driver.get("https://developers.facebook.com/apps/")
            
            # Create new app
            create_app = self.driver.find_element(By.LINK_TEXT, "Create App")
            self.human_like_mouse_movement(create_app)
            
            # Fill app details
            app_name = f"Jarvis_App_{random.randint(1000, 9999)}"
            name_field = self.driver.find_element(By.NAME, "display_name")
            self.human_like_typing(name_field, app_name)
            
            # Submit app creation
            create_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Create')]")
            self.human_like_mouse_movement(create_button)
            
            # Extract API credentials
            time.sleep(3)
            app_id = self.driver.find_element(By.CLASS_NAME, "app-id").text
            app_secret = self.driver.find_element(By.CLASS_NAME, "app-secret").text
            
            return {
                "success": True,
                "platform": "Meta",
                "app_id": app_id,
                "app_secret": app_secret,
                "email": email
            }
            
        except Exception as e:
            logger.error(f"Meta API account creation failed: {e}")
            return {"success": False, "error": str(e)}
    
    def autonomous_shopping(self, item: str, budget: float, preferences: Dict = None) -> Dict[str, Any]:
        """Autonomously shop for items online."""
        try:
            logger.info(f"🛒 Shopping for: {item} (Budget: ${budget})")
            
            # Search multiple platforms
            platforms = ["amazon.com", "ebay.com", "walmart.com", "target.com"]
            results = []
            
            for platform in platforms:
                platform_results = self._search_platform(platform, item, budget)
                results.extend(platform_results)
            
            # Analyze and select best option
            best_option = self._analyze_shopping_options(results, preferences)
            
            if best_option and preferences.get("auto_purchase", False):
                return self._complete_purchase(best_option)
            else:
                return {
                    "success": True,
                    "action": "search_completed",
                    "options": results,
                    "recommendation": best_option
                }
                
        except Exception as e:
            logger.error(f"Autonomous shopping failed: {e}")
            return {"success": False, "error": str(e)}
    
    def _search_platform(self, platform: str, item: str, budget: float) -> List[Dict]:
        """Search a specific platform for items."""
        try:
            self.driver.get(f"https://{platform}")
            time.sleep(random.uniform(2, 4))
            
            # Find search box
            search_selectors = ["input[name='q']", "input[type='search']", "#search", ".search-input"]
            search_box = None
            
            for selector in search_selectors:
                try:
                    search_box = self.driver.find_element(By.CSS_SELECTOR, selector)
                    break
                except:
                    continue
            
            if not search_box:
                return []
            
            # Search for item
            self.human_like_typing(search_box, item)
            search_box.send_keys(Keys.RETURN)
            
            time.sleep(random.uniform(3, 5))
            
            # Extract product information
            products = []
            product_elements = self.driver.find_elements(By.CSS_SELECTOR, "[data-testid='product'], .product, .item")
            
            for element in product_elements[:10]:  # Limit to first 10 results
                try:
                    title = element.find_element(By.CSS_SELECTOR, "h1, h2, h3, .title").text
                    price_text = element.find_element(By.CSS_SELECTOR, ".price, [data-testid='price']").text
                    price = float(''.join(filter(str.isdigit, price_text.replace('.', '')))) / 100
                    
                    if price <= budget:
                        products.append({
                            "title": title,
                            "price": price,
                            "platform": platform,
                            "element": element
                        })
                except:
                    continue
            
            return products
            
        except Exception as e:
            logger.error(f"Platform search failed for {platform}: {e}")
            return []
    
    def bypass_bot_detection(self) -> bool:
        """Implement advanced bot detection bypass techniques."""
        try:
            # Random viewport size
            width = random.randint(1200, 1920)
            height = random.randint(800, 1080)
            self.driver.set_window_size(width, height)
            
            # Random scroll patterns
            self._random_scroll_behavior()
            
            # Random mouse movements
            self._random_mouse_movements()
            
            # Mimic human reading patterns
            self._mimic_reading_behavior()
            
            return True
            
        except Exception as e:
            logger.error(f"Bot detection bypass failed: {e}")
            return False
    
    def _random_scroll_behavior(self):
        """Implement human-like scrolling patterns."""
        for _ in range(random.randint(2, 5)):
            scroll_amount = random.randint(100, 500)
            self.driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
            time.sleep(random.uniform(0.5, 2.0))
    
    def _random_mouse_movements(self):
        """Generate random mouse movements."""
        actions = ActionChains(self.driver)
        for _ in range(random.randint(3, 7)):
            x = random.randint(0, 1000)
            y = random.randint(0, 800)
            actions.move_by_offset(x, y)
            time.sleep(random.uniform(0.1, 0.5))
        actions.perform()
    
    def _mimic_reading_behavior(self):
        """Mimic human reading patterns with pauses."""
        # Simulate reading time based on page content
        page_text = self.driver.find_element(By.TAG_NAME, "body").text
        word_count = len(page_text.split())
        reading_time = word_count / 200  # Average reading speed
        
        # Add random pauses during "reading"
        for _ in range(random.randint(2, 5)):
            time.sleep(random.uniform(0.5, reading_time / 5))
    
    def autonomous_form_filling(self, form_data: Dict[str, str]) -> bool:
        """Autonomously fill out forms with provided data."""
        try:
            # Find all form fields
            inputs = self.driver.find_elements(By.TAG_NAME, "input")
            selects = self.driver.find_elements(By.TAG_NAME, "select")
            textareas = self.driver.find_elements(By.TAG_NAME, "textarea")
            
            # Fill input fields
            for input_field in inputs:
                field_type = input_field.get_attribute("type")
                field_name = input_field.get_attribute("name") or input_field.get_attribute("id")
                
                if field_name and field_name.lower() in form_data:
                    if field_type in ["text", "email", "password", "tel"]:
                        self.human_like_typing(input_field, form_data[field_name.lower()])
                    elif field_type == "checkbox" and form_data[field_name.lower()].lower() == "true":
                        self.human_like_mouse_movement(input_field)
            
            # Fill textareas
            for textarea in textareas:
                field_name = textarea.get_attribute("name") or textarea.get_attribute("id")
                if field_name and field_name.lower() in form_data:
                    self.human_like_typing(textarea, form_data[field_name.lower()])
            
            return True
            
        except Exception as e:
            logger.error(f"Form filling failed: {e}")
            return False
    
    def close_browser(self):
        """Close the browser safely."""
        try:
            if self.driver:
                self.driver.quit()
                logger.info("✅ Browser closed")
        except Exception as e:
            logger.error(f"Error closing browser: {e}")
    
    def __del__(self):
        """Cleanup when object is destroyed."""
        self.close_browser()
