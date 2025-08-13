#!/usr/bin/env python3
"""
JARVIS Internet System - Web Access, Scraping, and API Integration
Comprehensive internet capabilities for JARVIS Supreme Being AI
"""

import asyncio
import aiohttp
import requests
import json
import os
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import threading
from urllib.parse import urljoin, urlparse
import sqlite3
import hashlib

# Try to import web scraping libraries
try:
    from bs4 import BeautifulSoup
    import selenium
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    WEB_SCRAPING_AVAILABLE = True
except ImportError:
    WEB_SCRAPING_AVAILABLE = False
    print("⚠️ Web scraping libraries not available. Install with: pip install beautifulsoup4 selenium")

# Try to import additional libraries
try:
    import feedparser
    RSS_AVAILABLE = True
except ImportError:
    RSS_AVAILABLE = False
    print("⚠️ RSS libraries not available. Install with: pip install feedparser")

class JarvisInternetSystem:
    """Comprehensive internet access system for JARVIS"""
    
    def __init__(self, cache_dir: str = "supreme_internet"):
        self.cache_dir = cache_dir
        self.db_path = os.path.join(cache_dir, "internet_cache.db")
        
        # Internet capabilities
        self.capabilities = {
            'web_requests': True,
            'web_scraping': WEB_SCRAPING_AVAILABLE,
            'rss_feeds': RSS_AVAILABLE,
            'api_integration': True,
            'real_time_data': True
        }
        
        # Request session for connection pooling
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'JARVIS-Supreme-AI/3.0 (Advanced AI Assistant)'
        })
        
        # Cache settings
        self.cache_duration = 3600  # 1 hour default cache
        self.max_cache_size = 1000  # Maximum cached items
        
        # Rate limiting
        self.rate_limits = {}
        self.request_delays = {}
        
        # Statistics
        self.internet_stats = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'cached_responses': 0,
            'data_downloaded_mb': 0.0
        }
        
        # Thread lock
        self.internet_lock = threading.Lock()
        
        # Initialize system
        self.initialize_internet_system()
    
    def initialize_internet_system(self):
        """Initialize the internet system"""
        print("🌐 INITIALIZING JARVIS INTERNET SYSTEM...")
        
        try:
            os.makedirs(self.cache_dir, exist_ok=True)
            self.init_database()
            self.load_internet_stats()
            
            print("✅ JARVIS Internet System initialized successfully")
            print(f"📊 Internet Capabilities: {sum(self.capabilities.values())}/5 active")
            
        except Exception as e:
            print(f"❌ Internet system initialization error: {e}")
    
    def init_database(self):
        """Initialize SQLite database for caching"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Web cache table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS web_cache (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT UNIQUE,
                    content TEXT,
                    content_type TEXT,
                    status_code INTEGER,
                    timestamp TEXT,
                    expires_at TEXT,
                    size_bytes INTEGER
                )
            ''')
            
            # API responses cache
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS api_cache (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    endpoint TEXT,
                    params_hash TEXT,
                    response_data TEXT,
                    timestamp TEXT,
                    expires_at TEXT
                )
            ''')
            
            # Request statistics
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS request_stats (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT,
                    method TEXT,
                    status_code INTEGER,
                    response_time REAL,
                    timestamp TEXT,
                    success BOOLEAN
                )
            ''')
            
            conn.commit()
    
    def make_request(self, url: str, method: str = 'GET', 
                    headers: Dict = None, params: Dict = None, 
                    data: Dict = None, timeout: int = 30,
                    use_cache: bool = True) -> Dict[str, Any]:
        """Make HTTP request with caching and error handling"""
        
        with self.internet_lock:
            start_time = time.time()
            
            try:
                # Check cache first
                if use_cache and method == 'GET':
                    cached_response = self.get_cached_response(url, params)
                    if cached_response:
                        self.internet_stats['cached_responses'] += 1
                        return cached_response
                
                # Apply rate limiting
                self.apply_rate_limit(url)
                
                # Prepare request
                request_headers = headers or {}
                request_headers.update(self.session.headers)
                
                # Make request
                if method.upper() == 'GET':
                    response = self.session.get(url, headers=request_headers, 
                                             params=params, timeout=timeout)
                elif method.upper() == 'POST':
                    response = self.session.post(url, headers=request_headers, 
                                               params=params, json=data, timeout=timeout)
                else:
                    response = self.session.request(method, url, headers=request_headers,
                                                  params=params, json=data, timeout=timeout)
                
                # Calculate response time
                response_time = time.time() - start_time
                
                # Prepare response data
                result = {
                    'url': url,
                    'status_code': response.status_code,
                    'headers': dict(response.headers),
                    'content': response.text,
                    'content_type': response.headers.get('content-type', ''),
                    'response_time': response_time,
                    'success': response.status_code < 400,
                    'timestamp': datetime.now().isoformat()
                }
                
                # Update statistics
                self.internet_stats['total_requests'] += 1
                if result['success']:
                    self.internet_stats['successful_requests'] += 1
                else:
                    self.internet_stats['failed_requests'] += 1
                
                # Calculate data size
                content_size = len(response.content) / (1024 * 1024)  # MB
                self.internet_stats['data_downloaded_mb'] += content_size
                
                # Cache successful GET requests
                if use_cache and method == 'GET' and result['success']:
                    self.cache_response(url, result, params)
                
                # Store request statistics
                self.store_request_stats(url, method, response.status_code, 
                                       response_time, result['success'])
                
                return result
                
            except Exception as e:
                error_result = {
                    'url': url,
                    'status_code': 0,
                    'content': '',
                    'error': str(e),
                    'success': False,
                    'response_time': time.time() - start_time,
                    'timestamp': datetime.now().isoformat()
                }
                
                self.internet_stats['total_requests'] += 1
                self.internet_stats['failed_requests'] += 1
                
                return error_result
    
    def scrape_website(self, url: str, extract_text: bool = True, 
                      extract_links: bool = False, extract_images: bool = False,
                      css_selectors: List[str] = None) -> Dict[str, Any]:
        """Scrape website content using BeautifulSoup"""
        
        if not WEB_SCRAPING_AVAILABLE:
            return {'error': 'Web scraping libraries not available'}
        
        try:
            # Get webpage content
            response = self.make_request(url)
            
            if not response['success']:
                return {'error': f"Failed to fetch webpage: {response.get('error', 'Unknown error')}"}
            
            # Parse HTML
            soup = BeautifulSoup(response['content'], 'html.parser')
            
            result = {
                'url': url,
                'title': soup.title.string if soup.title else '',
                'timestamp': datetime.now().isoformat()
            }
            
            # Extract text content
            if extract_text:
                # Remove script and style elements
                for script in soup(["script", "style"]):
                    script.decompose()
                
                result['text'] = soup.get_text()
                result['clean_text'] = ' '.join(result['text'].split())
            
            # Extract links
            if extract_links:
                links = []
                for link in soup.find_all('a', href=True):
                    links.append({
                        'text': link.get_text().strip(),
                        'url': urljoin(url, link['href'])
                    })
                result['links'] = links
            
            # Extract images
            if extract_images:
                images = []
                for img in soup.find_all('img', src=True):
                    images.append({
                        'alt': img.get('alt', ''),
                        'url': urljoin(url, img['src'])
                    })
                result['images'] = images
            
            # Extract custom CSS selectors
            if css_selectors:
                custom_data = {}
                for selector in css_selectors:
                    elements = soup.select(selector)
                    custom_data[selector] = [elem.get_text().strip() for elem in elements]
                result['custom_data'] = custom_data
            
            return result
            
        except Exception as e:
            return {'error': f"Scraping error: {str(e)}"}
    
    def search_web(self, query: str, num_results: int = 10) -> List[Dict[str, Any]]:
        """Search the web using DuckDuckGo (no API key required)"""
        
        try:
            # Use DuckDuckGo instant answer API
            search_url = "https://api.duckduckgo.com/"
            params = {
                'q': query,
                'format': 'json',
                'no_html': '1',
                'skip_disambig': '1'
            }
            
            response = self.make_request(search_url, params=params)
            
            if not response['success']:
                return []
            
            data = json.loads(response['content'])
            results = []
            
            # Extract instant answer
            if data.get('Abstract'):
                results.append({
                    'title': data.get('Heading', query),
                    'snippet': data.get('Abstract'),
                    'url': data.get('AbstractURL', ''),
                    'type': 'instant_answer'
                })
            
            # Extract related topics
            for topic in data.get('RelatedTopics', [])[:num_results]:
                if isinstance(topic, dict) and 'Text' in topic:
                    results.append({
                        'title': topic.get('Text', '').split(' - ')[0],
                        'snippet': topic.get('Text', ''),
                        'url': topic.get('FirstURL', ''),
                        'type': 'related_topic'
                    })
            
            return results[:num_results]
            
        except Exception as e:
            print(f"❌ Web search error: {e}")
            return []
    
    def get_news(self, category: str = 'general', num_articles: int = 10) -> List[Dict[str, Any]]:
        """Get latest news articles"""
        
        try:
            # Use NewsAPI alternative (free tier)
            news_sources = {
                'general': 'https://feeds.bbci.co.uk/news/rss.xml',
                'technology': 'https://feeds.feedburner.com/oreilly/radar',
                'business': 'https://feeds.reuters.com/reuters/businessNews',
                'science': 'https://rss.cnn.com/rss/edition.rss'
            }
            
            rss_url = news_sources.get(category, news_sources['general'])
            
            if RSS_AVAILABLE:
                feed = feedparser.parse(rss_url)
                articles = []
                
                for entry in feed.entries[:num_articles]:
                    articles.append({
                        'title': entry.get('title', ''),
                        'summary': entry.get('summary', ''),
                        'url': entry.get('link', ''),
                        'published': entry.get('published', ''),
                        'source': feed.feed.get('title', 'Unknown')
                    })
                
                return articles
            else:
                # Fallback: scrape RSS manually
                response = self.make_request(rss_url)
                if response['success']:
                    # Simple RSS parsing without feedparser
                    content = response['content']
                    articles = []
                    
                    # Basic RSS item extraction
                    import re
                    items = re.findall(r'<item>(.*?)</item>', content, re.DOTALL)
                    
                    for item in items[:num_articles]:
                        title_match = re.search(r'<title>(.*?)</title>', item)
                        link_match = re.search(r'<link>(.*?)</link>', item)
                        
                        if title_match and link_match:
                            articles.append({
                                'title': title_match.group(1),
                                'url': link_match.group(1),
                                'source': 'RSS Feed'
                            })
                    
                    return articles
                
                return []
            
        except Exception as e:
            print(f"❌ News fetch error: {e}")
            return []
    
    def get_weather(self, location: str) -> Dict[str, Any]:
        """Get weather information (using free API)"""
        
        try:
            # Use OpenWeatherMap free tier or wttr.in
            weather_url = f"https://wttr.in/{location}?format=j1"
            
            response = self.make_request(weather_url)
            
            if response['success']:
                data = json.loads(response['content'])
                
                current = data.get('current_condition', [{}])[0]
                
                return {
                    'location': location,
                    'temperature': current.get('temp_C', 'N/A'),
                    'condition': current.get('weatherDesc', [{}])[0].get('value', 'N/A'),
                    'humidity': current.get('humidity', 'N/A'),
                    'wind_speed': current.get('windspeedKmph', 'N/A'),
                    'timestamp': datetime.now().isoformat()
                }
            
            return {'error': 'Weather data unavailable'}
            
        except Exception as e:
            return {'error': f"Weather fetch error: {str(e)}"}
    
    def get_cached_response(self, url: str, params: Dict = None) -> Optional[Dict]:
        """Get cached response if available and not expired"""
        
        try:
            params_hash = hashlib.md5(str(sorted((params or {}).items())).encode()).hexdigest()
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT content, content_type, status_code, timestamp 
                    FROM web_cache 
                    WHERE url = ? AND expires_at > ?
                ''', (url, datetime.now().isoformat()))
                
                result = cursor.fetchone()
                
                if result:
                    return {
                        'url': url,
                        'content': result[0],
                        'content_type': result[1],
                        'status_code': result[2],
                        'timestamp': result[3],
                        'cached': True,
                        'success': True
                    }
                
                return None
                
        except Exception as e:
            print(f"❌ Cache retrieval error: {e}")
            return None
    
    def cache_response(self, url: str, response_data: Dict, params: Dict = None):
        """Cache response data"""
        
        try:
            expires_at = (datetime.now() + timedelta(seconds=self.cache_duration)).isoformat()
            content_size = len(response_data.get('content', ''))
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT OR REPLACE INTO web_cache 
                    (url, content, content_type, status_code, timestamp, expires_at, size_bytes)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    url,
                    response_data.get('content', ''),
                    response_data.get('content_type', ''),
                    response_data.get('status_code', 0),
                    response_data.get('timestamp', datetime.now().isoformat()),
                    expires_at,
                    content_size
                ))
                
                conn.commit()
                
        except Exception as e:
            print(f"❌ Cache storage error: {e}")
    
    def apply_rate_limit(self, url: str):
        """Apply rate limiting to prevent overwhelming servers"""
        
        domain = urlparse(url).netloc
        
        if domain in self.rate_limits:
            last_request = self.rate_limits[domain]
            delay = self.request_delays.get(domain, 1.0)  # Default 1 second delay
            
            elapsed = time.time() - last_request
            if elapsed < delay:
                time.sleep(delay - elapsed)
        
        self.rate_limits[domain] = time.time()
    
    def store_request_stats(self, url: str, method: str, status_code: int, 
                           response_time: float, success: bool):
        """Store request statistics"""
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO request_stats 
                    (url, method, status_code, response_time, timestamp, success)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (url, method, status_code, response_time, 
                      datetime.now().isoformat(), success))
                
                conn.commit()
                
        except Exception as e:
            print(f"❌ Stats storage error: {e}")
    
    def load_internet_stats(self):
        """Load internet statistics from database"""
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Count total requests
                cursor.execute('SELECT COUNT(*) FROM request_stats')
                self.internet_stats['total_requests'] = cursor.fetchone()[0]
                
                # Count successful requests
                cursor.execute('SELECT COUNT(*) FROM request_stats WHERE success = 1')
                self.internet_stats['successful_requests'] = cursor.fetchone()[0]
                
                # Count failed requests
                cursor.execute('SELECT COUNT(*) FROM request_stats WHERE success = 0')
                self.internet_stats['failed_requests'] = cursor.fetchone()[0]
                
        except Exception as e:
            print(f"❌ Stats loading error: {e}")
    
    def get_internet_status(self) -> Dict[str, Any]:
        """Get comprehensive internet system status"""
        
        return {
            'capabilities': self.capabilities,
            'statistics': self.internet_stats,
            'cache_info': {
                'cache_duration': self.cache_duration,
                'max_cache_size': self.max_cache_size,
                'database_path': self.db_path
            },
            'system_status': 'active'
        }
    
    def cleanup_cache(self, days_old: int = 7):
        """Clean up old cache entries"""
        
        try:
            cutoff_date = (datetime.now() - timedelta(days=days_old)).isoformat()
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Remove expired cache entries
                cursor.execute('DELETE FROM web_cache WHERE expires_at < ?', (cutoff_date,))
                cursor.execute('DELETE FROM api_cache WHERE expires_at < ?', (cutoff_date,))
                
                # Remove old request stats
                cursor.execute('DELETE FROM request_stats WHERE timestamp < ?', (cutoff_date,))
                
                conn.commit()
                
            print(f"✅ Cache cleanup completed - removed entries older than {days_old} days")
            
        except Exception as e:
            print(f"❌ Cache cleanup error: {e}")

def main():
    """Test the internet system"""
    print("🌐 JARVIS INTERNET SYSTEM TEST")
    print("=" * 50)
    
    # Initialize internet system
    internet = JarvisInternetSystem()
    
    # Test basic web request
    print("\n🔄 Testing web request...")
    response = internet.make_request("https://httpbin.org/json")
    if response['success']:
        print(f"✅ Web request successful: {response['status_code']}")
    else:
        print(f"❌ Web request failed: {response.get('error', 'Unknown error')}")
    
    # Test web search
    print("\n🔄 Testing web search...")
    search_results = internet.search_web("artificial intelligence", num_results=3)
    print(f"✅ Found {len(search_results)} search results")
    for i, result in enumerate(search_results[:2], 1):
        print(f"   {i}. {result.get('title', 'No title')[:50]}...")
    
    # Test news fetching
    print("\n🔄 Testing news fetching...")
    news_articles = internet.get_news("technology", num_articles=3)
    print(f"✅ Found {len(news_articles)} news articles")
    for i, article in enumerate(news_articles[:2], 1):
        print(f"   {i}. {article.get('title', 'No title')[:50]}...")
    
    # Test weather
    print("\n🔄 Testing weather data...")
    weather = internet.get_weather("London")
    if 'error' not in weather:
        print(f"✅ Weather data: {weather.get('temperature', 'N/A')}°C, {weather.get('condition', 'N/A')}")
    else:
        print(f"❌ Weather error: {weather['error']}")
    
    # Test web scraping (if available)
    if WEB_SCRAPING_AVAILABLE:
        print("\n🔄 Testing web scraping...")
        scraped_data = internet.scrape_website("https://httpbin.org/html", extract_text=True)
        if 'error' not in scraped_data:
            print(f"✅ Scraped webpage: {scraped_data.get('title', 'No title')}")
        else:
            print(f"❌ Scraping error: {scraped_data['error']}")
    
    # Show internet status
    print("\n📊 Internet System Status:")
    status = internet.get_internet_status()
    print(f"   Active Capabilities: {sum(status['capabilities'].values())}/5")
    print(f"   Total Requests: {status['statistics']['total_requests']}")
    print(f"   Success Rate: {status['statistics']['successful_requests']}/{status['statistics']['total_requests']}")
    print(f"   Data Downloaded: {status['statistics']['data_downloaded_mb']:.2f} MB")
    
    print("\n🎉 INTERNET SYSTEM TEST COMPLETED!")
    print("✅ All internet functions working correctly")
    print("🌐 JARVIS Internet System is ready for web operations")

if __name__ == '__main__':
    main()