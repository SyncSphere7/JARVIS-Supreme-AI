"""
Advanced Web Scraper for Jarvis.
Comprehensive data extraction with multiple methods and intelligent parsing.
"""
import requests
import time
import json
import re
from urllib.parse import urljoin, urlparse, parse_qs
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
from datetime import datetime
from bs4 import BeautifulSoup
from core.utils.log import logger

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    import undetected_chromedriver as uc
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False


class AdvancedWebScraper:
    def __init__(self, brain):
        self.brain = brain
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        self.driver = None
        self.scraped_data_dir = Path("scraped_data")
        self.scraped_data_dir.mkdir(exist_ok=True)
    
    def scrape_website(self, url: str, scrape_config: Dict[str, Any] = None) -> Dict[str, Any]:
        """Comprehensive website scraping with intelligent data extraction."""
        try:
            logger.info(f"🕷️ Scraping website: {url}")
            
            if not scrape_config:
                scrape_config = self._generate_smart_scrape_config(url)
            
            # Choose scraping method based on website type
            method = scrape_config.get('method', 'auto')
            
            if method == 'selenium' or (method == 'auto' and self._needs_selenium(url)):
                result = self._scrape_with_selenium(url, scrape_config)
            else:
                result = self._scrape_with_requests(url, scrape_config)
            
            # Post-process and structure data
            structured_data = self._structure_scraped_data(result, scrape_config)
            
            # Save scraped data
            self._save_scraped_data(structured_data, url)
            
            return structured_data
            
        except Exception as e:
            logger.error(f"Web scraping failed: {e}")
            return {
                'success': False,
                'error': str(e),
                'url': url
            }
    
    def _generate_smart_scrape_config(self, url: str) -> Dict[str, Any]:
        """Generate intelligent scraping configuration based on URL and AI analysis."""
        try:
            # Analyze URL to determine website type
            domain = urlparse(url).netloc.lower()
            
            # Pre-defined configurations for common sites
            if 'github.com' in domain:
                return self._github_config()
            elif 'linkedin.com' in domain:
                return self._linkedin_config()
            elif 'twitter.com' in domain or 'x.com' in domain:
                return self._twitter_config()
            elif 'reddit.com' in domain:
                return self._reddit_config()
            elif 'amazon.com' in domain:
                return self._amazon_config()
            elif 'news' in domain or 'blog' in domain:
                return self._news_blog_config()
            else:
                return self._generic_config(url)
                
        except Exception as e:
            logger.error(f"Config generation failed: {e}")
            return self._generic_config(url)
    
    def _scrape_with_requests(self, url: str, config: Dict) -> Dict[str, Any]:
        """Scrape using requests and BeautifulSoup."""
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            scraped_data = {
                'url': url,
                'method': 'requests',
                'timestamp': datetime.now().isoformat(),
                'status_code': response.status_code,
                'data': {}
            }
            
            # Extract data based on configuration
            for data_type, selectors in config.get('selectors', {}).items():
                scraped_data['data'][data_type] = self._extract_data_by_selectors(soup, selectors)
            
            # Extract structured data (JSON-LD, microdata)
            structured = self._extract_structured_data(soup)
            if structured:
                scraped_data['structured_data'] = structured
            
            # Extract all links
            scraped_data['links'] = self._extract_links(soup, url)
            
            # Extract all images
            scraped_data['images'] = self._extract_images(soup, url)
            
            # Extract all text content
            scraped_data['text_content'] = self._extract_text_content(soup)
            
            return scraped_data
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _scrape_with_selenium(self, url: str, config: Dict) -> Dict[str, Any]:
        """Scrape using Selenium for dynamic content."""
        try:
            if not SELENIUM_AVAILABLE:
                raise ImportError("Selenium not available")
            
            # Setup browser if not already done
            if not self.driver:
                self._setup_selenium_driver()
            
            self.driver.get(url)
            
            # Wait for page to load
            time.sleep(config.get('wait_time', 3))
            
            # Handle dynamic content loading
            if config.get('scroll_to_load'):
                self._scroll_to_load_content()
            
            # Wait for specific elements if configured
            if config.get('wait_for_elements'):
                self._wait_for_elements(config['wait_for_elements'])
            
            # Get page source and parse
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            
            scraped_data = {
                'url': url,
                'method': 'selenium',
                'timestamp': datetime.now().isoformat(),
                'data': {}
            }
            
            # Extract data based on configuration
            for data_type, selectors in config.get('selectors', {}).items():
                scraped_data['data'][data_type] = self._extract_data_by_selectors(soup, selectors)
            
            # Extract dynamic content
            scraped_data['dynamic_content'] = self._extract_dynamic_content()
            
            return scraped_data
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _extract_data_by_selectors(self, soup: BeautifulSoup, selectors: Dict) -> List[Dict]:
        """Extract data using CSS selectors."""
        extracted_data = []
        
        try:
            elements = soup.select(selectors.get('container', 'body'))
            
            for element in elements:
                item_data = {}
                
                for field, selector in selectors.get('fields', {}).items():
                    try:
                        field_element = element.select_one(selector)
                        if field_element:
                            # Extract text, attribute, or href based on field type
                            if field.endswith('_url') or field.endswith('_link'):
                                item_data[field] = field_element.get('href', field_element.get('src', ''))
                            elif field.endswith('_image'):
                                item_data[field] = field_element.get('src', field_element.get('data-src', ''))
                            else:
                                item_data[field] = field_element.get_text(strip=True)
                    except Exception:
                        item_data[field] = None
                
                if item_data:
                    extracted_data.append(item_data)
            
            return extracted_data
            
        except Exception as e:
            logger.error(f"Data extraction failed: {e}")
            return []
    
    def _extract_structured_data(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Extract structured data (JSON-LD, microdata, etc.)."""
        structured_data = {}
        
        try:
            # Extract JSON-LD
            json_ld_scripts = soup.find_all('script', type='application/ld+json')
            if json_ld_scripts:
                json_ld_data = []
                for script in json_ld_scripts:
                    try:
                        data = json.loads(script.string)
                        json_ld_data.append(data)
                    except:
                        continue
                structured_data['json_ld'] = json_ld_data
            
            # Extract Open Graph data
            og_data = {}
            og_tags = soup.find_all('meta', property=re.compile(r'^og:'))
            for tag in og_tags:
                property_name = tag.get('property', '').replace('og:', '')
                content = tag.get('content', '')
                if property_name and content:
                    og_data[property_name] = content
            
            if og_data:
                structured_data['open_graph'] = og_data
            
            # Extract Twitter Card data
            twitter_data = {}
            twitter_tags = soup.find_all('meta', attrs={'name': re.compile(r'^twitter:')})
            for tag in twitter_tags:
                name = tag.get('name', '').replace('twitter:', '')
                content = tag.get('content', '')
                if name and content:
                    twitter_data[name] = content
            
            if twitter_data:
                structured_data['twitter_card'] = twitter_data
            
            return structured_data
            
        except Exception as e:
            logger.error(f"Structured data extraction failed: {e}")
            return {}
    
    def _extract_links(self, soup: BeautifulSoup, base_url: str) -> List[Dict]:
        """Extract all links from the page."""
        links = []
        
        try:
            for link in soup.find_all('a', href=True):
                href = link.get('href')
                text = link.get_text(strip=True)
                
                # Convert relative URLs to absolute
                absolute_url = urljoin(base_url, href)
                
                links.append({
                    'url': absolute_url,
                    'text': text,
                    'title': link.get('title', ''),
                    'rel': link.get('rel', [])
                })
            
            return links
            
        except Exception as e:
            logger.error(f"Link extraction failed: {e}")
            return []
    
    def _extract_images(self, soup: BeautifulSoup, base_url: str) -> List[Dict]:
        """Extract all images from the page."""
        images = []
        
        try:
            for img in soup.find_all('img'):
                src = img.get('src') or img.get('data-src')
                if src:
                    absolute_url = urljoin(base_url, src)
                    
                    images.append({
                        'url': absolute_url,
                        'alt': img.get('alt', ''),
                        'title': img.get('title', ''),
                        'width': img.get('width'),
                        'height': img.get('height')
                    })
            
            return images
            
        except Exception as e:
            logger.error(f"Image extraction failed: {e}")
            return []
    
    def _extract_text_content(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Extract and analyze text content."""
        try:
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text content
            text = soup.get_text()
            
            # Clean up text
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            # Basic text analysis
            words = text.split()
            
            return {
                'full_text': text,
                'word_count': len(words),
                'character_count': len(text),
                'paragraph_count': len(soup.find_all('p')),
                'heading_count': len(soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']))
            }
            
        except Exception as e:
            logger.error(f"Text extraction failed: {e}")
            return {}
    
    def scrape_multiple_pages(self, urls: List[str], config: Dict = None) -> Dict[str, Any]:
        """Scrape multiple pages with the same configuration."""
        try:
            results = {}
            
            for i, url in enumerate(urls):
                logger.info(f"🕷️ Scraping page {i+1}/{len(urls)}: {url}")
                
                result = self.scrape_website(url, config)
                results[url] = result
                
                # Add delay between requests
                if i < len(urls) - 1:
                    time.sleep(2)
            
            return {
                'success': True,
                'total_pages': len(urls),
                'results': results,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def scrape_with_pagination(self, start_url: str, pagination_config: Dict) -> Dict[str, Any]:
        """Scrape website with pagination support."""
        try:
            all_data = []
            current_url = start_url
            page_count = 0
            max_pages = pagination_config.get('max_pages', 10)
            
            while current_url and page_count < max_pages:
                logger.info(f"🕷️ Scraping page {page_count + 1}: {current_url}")
                
                # Scrape current page
                result = self.scrape_website(current_url, pagination_config.get('scrape_config'))
                
                if result.get('success', True):
                    all_data.extend(result.get('data', {}).get('items', []))
                    
                    # Find next page URL
                    current_url = self._find_next_page_url(result, pagination_config)
                    page_count += 1
                else:
                    break
                
                # Add delay between pages
                time.sleep(pagination_config.get('delay', 2))
            
            return {
                'success': True,
                'total_pages': page_count,
                'total_items': len(all_data),
                'data': all_data,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    # Configuration methods for different website types
    def _github_config(self) -> Dict:
        return {
            'method': 'requests',
            'selectors': {
                'repositories': {
                    'container': '[data-testid="results-list"] .Box-row',
                    'fields': {
                        'name': 'h3 a',
                        'description': 'p',
                        'language': '[itemprop="programmingLanguage"]',
                        'stars': 'a[href*="/stargazers"]',
                        'url': 'h3 a'
                    }
                }
            }
        }
    
    def _linkedin_config(self) -> Dict:
        return {
            'method': 'selenium',
            'wait_time': 5,
            'scroll_to_load': True,
            'selectors': {
                'posts': {
                    'container': '.feed-shared-update-v2',
                    'fields': {
                        'author': '.feed-shared-actor__name',
                        'content': '.feed-shared-text',
                        'timestamp': '.feed-shared-actor__sub-description'
                    }
                }
            }
        }
    
    def _amazon_config(self) -> Dict:
        return {
            'method': 'requests',
            'selectors': {
                'products': {
                    'container': '[data-component-type="s-search-result"]',
                    'fields': {
                        'title': 'h2 a span',
                        'price': '.a-price-whole',
                        'rating': '.a-icon-alt',
                        'image': '.s-image',
                        'url': 'h2 a'
                    }
                }
            }
        }
    
    def _generic_config(self, url: str) -> Dict:
        return {
            'method': 'auto',
            'selectors': {
                'content': {
                    'container': 'article, .content, .post, .entry',
                    'fields': {
                        'title': 'h1, h2, .title',
                        'content': 'p, .content, .text',
                        'author': '.author, .by',
                        'date': '.date, .published, time'
                    }
                }
            }
        }
    
    # Helper methods
    def _needs_selenium(self, url: str) -> bool:
        """Determine if Selenium is needed for this URL."""
        selenium_indicators = [
            'linkedin.com', 'twitter.com', 'x.com', 'facebook.com',
            'instagram.com', 'tiktok.com', 'youtube.com'
        ]
        return any(indicator in url.lower() for indicator in selenium_indicators)
    
    def _setup_selenium_driver(self):
        """Setup Selenium driver."""
        if SELENIUM_AVAILABLE:
            options = uc.ChromeOptions()
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            self.driver = uc.Chrome(options=options)
    
    def _structure_scraped_data(self, raw_data: Dict, config: Dict) -> Dict[str, Any]:
        """Structure and clean scraped data."""
        if not raw_data.get('success', True):
            return raw_data
        
        # Add metadata
        structured = {
            'success': True,
            'metadata': {
                'url': raw_data.get('url'),
                'scraping_method': raw_data.get('method'),
                'timestamp': raw_data.get('timestamp'),
                'total_items': 0
            },
            'data': raw_data.get('data', {}),
            'links': raw_data.get('links', []),
            'images': raw_data.get('images', []),
            'text_analysis': raw_data.get('text_content', {}),
            'structured_data': raw_data.get('structured_data', {})
        }
        
        # Count total items
        total_items = 0
        for category, items in structured['data'].items():
            if isinstance(items, list):
                total_items += len(items)
        
        structured['metadata']['total_items'] = total_items
        
        return structured
    
    def _save_scraped_data(self, data: Dict, url: str):
        """Save scraped data to file."""
        try:
            # Create filename from URL and timestamp
            url_safe = urlparse(url).netloc.replace('.', '_')
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"scraped_{url_safe}_{timestamp}.json"
            
            with open(self.scraped_data_dir / filename, 'w') as f:
                json.dump(data, f, indent=2, default=str)
            
            logger.info(f"✅ Scraped data saved: {filename}")
            
        except Exception as e:
            logger.error(f"Failed to save scraped data: {e}")
    
    def close_driver(self):
        """Close Selenium driver."""
        if self.driver:
            self.driver.quit()
            self.driver = None
    
    def __del__(self):
        """Cleanup when object is destroyed."""
        self.close_driver()
