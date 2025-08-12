"""
Website Analyzer for Jarvis.
Analyzes any website comprehensively - content, design, performance, SEO, security, etc.
"""
import requests
import time
import json
from urllib.parse import urljoin, urlparse
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
from bs4 import BeautifulSoup
from core.utils.log import logger

try:
    import whois
    WHOIS_AVAILABLE = True
except ImportError:
    WHOIS_AVAILABLE = False

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False


class WebsiteAnalyzer:
    def __init__(self, brain):
        self.brain = brain
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        
    def analyze_website(self, url: str, deep_analysis: bool = True) -> Dict[str, Any]:
        """Perform comprehensive website analysis."""
        try:
            logger.info(f"🔍 Analyzing website: {url}")
            
            # Ensure URL has protocol
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            analysis_result = {
                'url': url,
                'timestamp': datetime.now().isoformat(),
                'analysis_type': 'comprehensive' if deep_analysis else 'basic'
            }
            
            # Basic website fetch and analysis
            basic_analysis = self._basic_website_analysis(url)
            analysis_result.update(basic_analysis)
            
            if deep_analysis:
                # Deep analysis components
                seo_analysis = self._seo_analysis(url, basic_analysis.get('soup'))
                performance_analysis = self._performance_analysis(url)
                security_analysis = self._security_analysis(url)
                content_analysis = self._content_analysis(basic_analysis.get('soup'))
                technical_analysis = self._technical_analysis(url, basic_analysis.get('soup'))
                
                analysis_result.update({
                    'seo': seo_analysis,
                    'performance': performance_analysis,
                    'security': security_analysis,
                    'content': content_analysis,
                    'technical': technical_analysis
                })
                
                # AI-powered insights
                ai_insights = self._ai_powered_insights(analysis_result)
                analysis_result['ai_insights'] = ai_insights
            
            # Generate summary
            summary = self._generate_analysis_summary(analysis_result)
            analysis_result['summary'] = summary
            
            # Save analysis
            self._save_analysis(analysis_result)
            
            return analysis_result
            
        except Exception as e:
            logger.error(f"Website analysis failed: {e}")
            return {
                'success': False,
                'error': str(e),
                'url': url
            }
    
    def _basic_website_analysis(self, url: str) -> Dict[str, Any]:
        """Perform basic website analysis."""
        try:
            # Fetch the website
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            # Parse HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Basic information
            title = soup.find('title')
            title_text = title.get_text().strip() if title else "No title found"
            
            # Meta description
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            description = meta_desc.get('content', '') if meta_desc else "No description found"
            
            # Basic metrics
            page_size = len(response.content)
            load_time = response.elapsed.total_seconds()
            status_code = response.status_code
            
            # Count elements
            images = soup.find_all('img')
            links = soup.find_all('a')
            scripts = soup.find_all('script')
            stylesheets = soup.find_all('link', rel='stylesheet')
            
            return {
                'success': True,
                'basic_info': {
                    'title': title_text,
                    'description': description,
                    'status_code': status_code,
                    'page_size_bytes': page_size,
                    'page_size_kb': round(page_size / 1024, 2),
                    'load_time_seconds': load_time,
                    'final_url': response.url
                },
                'elements': {
                    'images_count': len(images),
                    'links_count': len(links),
                    'scripts_count': len(scripts),
                    'stylesheets_count': len(stylesheets)
                },
                'soup': soup,  # For further analysis
                'response': response
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _seo_analysis(self, url: str, soup: BeautifulSoup) -> Dict[str, Any]:
        """Analyze SEO aspects of the website."""
        try:
            seo_data = {}
            
            # Title analysis
            title = soup.find('title')
            if title:
                title_text = title.get_text().strip()
                seo_data['title'] = {
                    'text': title_text,
                    'length': len(title_text),
                    'optimal': 30 <= len(title_text) <= 60
                }
            
            # Meta description
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            if meta_desc:
                desc_text = meta_desc.get('content', '')
                seo_data['meta_description'] = {
                    'text': desc_text,
                    'length': len(desc_text),
                    'optimal': 120 <= len(desc_text) <= 160
                }
            
            # Headings structure
            headings = {}
            for i in range(1, 7):
                h_tags = soup.find_all(f'h{i}')
                headings[f'h{i}'] = {
                    'count': len(h_tags),
                    'texts': [h.get_text().strip() for h in h_tags[:5]]  # First 5
                }
            seo_data['headings'] = headings
            
            # Images with alt text
            images = soup.find_all('img')
            images_with_alt = [img for img in images if img.get('alt')]
            seo_data['images'] = {
                'total': len(images),
                'with_alt': len(images_with_alt),
                'alt_percentage': round((len(images_with_alt) / len(images)) * 100, 1) if images else 0
            }
            
            # Internal vs external links
            domain = urlparse(url).netloc
            links = soup.find_all('a', href=True)
            internal_links = []
            external_links = []
            
            for link in links:
                href = link.get('href')
                if href.startswith('http'):
                    if domain in href:
                        internal_links.append(href)
                    else:
                        external_links.append(href)
                elif href.startswith('/'):
                    internal_links.append(href)
            
            seo_data['links'] = {
                'total': len(links),
                'internal': len(internal_links),
                'external': len(external_links)
            }
            
            # Meta tags
            meta_tags = soup.find_all('meta')
            important_meta = {}
            for meta in meta_tags:
                name = meta.get('name') or meta.get('property')
                if name in ['keywords', 'author', 'robots', 'viewport', 'og:title', 'og:description', 'twitter:card']:
                    important_meta[name] = meta.get('content', '')
            
            seo_data['meta_tags'] = important_meta
            
            return seo_data
            
        except Exception as e:
            return {'error': str(e)}
    
    def _performance_analysis(self, url: str) -> Dict[str, Any]:
        """Analyze website performance."""
        try:
            performance_data = {}
            
            # Multiple load time tests
            load_times = []
            for i in range(3):
                start_time = time.time()
                response = self.session.get(url, timeout=30)
                load_time = time.time() - start_time
                load_times.append(load_time)
                time.sleep(1)
            
            performance_data['load_times'] = {
                'average': round(sum(load_times) / len(load_times), 3),
                'min': round(min(load_times), 3),
                'max': round(max(load_times), 3),
                'tests': load_times
            }
            
            # Response headers analysis
            headers = dict(response.headers)
            performance_data['caching'] = {
                'cache_control': headers.get('Cache-Control', 'Not set'),
                'expires': headers.get('Expires', 'Not set'),
                'etag': headers.get('ETag', 'Not set'),
                'last_modified': headers.get('Last-Modified', 'Not set')
            }
            
            # Compression
            performance_data['compression'] = {
                'content_encoding': headers.get('Content-Encoding', 'None'),
                'gzip_enabled': 'gzip' in headers.get('Content-Encoding', '')
            }
            
            # Server information
            performance_data['server'] = {
                'server': headers.get('Server', 'Unknown'),
                'powered_by': headers.get('X-Powered-By', 'Unknown')
            }
            
            return performance_data
            
        except Exception as e:
            return {'error': str(e)}
    
    def _security_analysis(self, url: str) -> Dict[str, Any]:
        """Analyze website security."""
        try:
            security_data = {}
            
            # HTTPS check
            security_data['https'] = url.startswith('https://')
            
            # Security headers
            response = self.session.get(url, timeout=30)
            headers = dict(response.headers)
            
            security_headers = {
                'Strict-Transport-Security': headers.get('Strict-Transport-Security'),
                'Content-Security-Policy': headers.get('Content-Security-Policy'),
                'X-Frame-Options': headers.get('X-Frame-Options'),
                'X-Content-Type-Options': headers.get('X-Content-Type-Options'),
                'X-XSS-Protection': headers.get('X-XSS-Protection'),
                'Referrer-Policy': headers.get('Referrer-Policy')
            }
            
            security_data['security_headers'] = security_headers
            security_data['security_score'] = sum(1 for v in security_headers.values() if v) / len(security_headers) * 100
            
            # Domain information (if whois available)
            if WHOIS_AVAILABLE:
                try:
                    domain = urlparse(url).netloc
                    domain_info = whois.whois(domain)
                    security_data['domain_info'] = {
                        'registrar': getattr(domain_info, 'registrar', 'Unknown'),
                        'creation_date': str(getattr(domain_info, 'creation_date', 'Unknown')),
                        'expiration_date': str(getattr(domain_info, 'expiration_date', 'Unknown'))
                    }
                except:
                    security_data['domain_info'] = {'error': 'Could not retrieve domain info'}
            
            return security_data
            
        except Exception as e:
            return {'error': str(e)}
    
    def _content_analysis(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Analyze website content."""
        try:
            content_data = {}
            
            # Text content
            text_content = soup.get_text()
            words = text_content.split()
            
            content_data['text_stats'] = {
                'total_characters': len(text_content),
                'total_words': len(words),
                'average_word_length': round(sum(len(word) for word in words) / len(words), 2) if words else 0
            }
            
            # Language detection (basic)
            html_tag = soup.find('html')
            content_data['language'] = html_tag.get('lang', 'Not specified') if html_tag else 'Not specified'
            
            # Forms
            forms = soup.find_all('form')
            content_data['forms'] = {
                'count': len(forms),
                'methods': [form.get('method', 'GET').upper() for form in forms]
            }
            
            # Social media links
            social_patterns = {
                'facebook': ['facebook.com', 'fb.com'],
                'twitter': ['twitter.com', 'x.com'],
                'instagram': ['instagram.com'],
                'linkedin': ['linkedin.com'],
                'youtube': ['youtube.com', 'youtu.be'],
                'tiktok': ['tiktok.com']
            }
            
            social_links = {}
            links = soup.find_all('a', href=True)
            
            for platform, patterns in social_patterns.items():
                found_links = []
                for link in links:
                    href = link.get('href', '')
                    if any(pattern in href for pattern in patterns):
                        found_links.append(href)
                social_links[platform] = found_links
            
            content_data['social_media'] = social_links
            
            return content_data
            
        except Exception as e:
            return {'error': str(e)}
    
    def _technical_analysis(self, url: str, soup: BeautifulSoup) -> Dict[str, Any]:
        """Analyze technical aspects."""
        try:
            technical_data = {}
            
            # JavaScript frameworks detection
            scripts = soup.find_all('script')
            frameworks = {
                'react': False,
                'vue': False,
                'angular': False,
                'jquery': False,
                'bootstrap': False
            }
            
            for script in scripts:
                src = script.get('src', '')
                script_content = script.get_text()
                
                if 'react' in src.lower() or 'react' in script_content.lower():
                    frameworks['react'] = True
                if 'vue' in src.lower() or 'vue' in script_content.lower():
                    frameworks['vue'] = True
                if 'angular' in src.lower() or 'angular' in script_content.lower():
                    frameworks['angular'] = True
                if 'jquery' in src.lower() or 'jquery' in script_content.lower():
                    frameworks['jquery'] = True
                if 'bootstrap' in src.lower() or 'bootstrap' in script_content.lower():
                    frameworks['bootstrap'] = True
            
            technical_data['frameworks'] = frameworks
            
            # CSS frameworks
            stylesheets = soup.find_all('link', rel='stylesheet')
            css_frameworks = {
                'bootstrap': False,
                'tailwind': False,
                'foundation': False
            }
            
            for stylesheet in stylesheets:
                href = stylesheet.get('href', '')
                if 'bootstrap' in href.lower():
                    css_frameworks['bootstrap'] = True
                if 'tailwind' in href.lower():
                    css_frameworks['tailwind'] = True
                if 'foundation' in href.lower():
                    css_frameworks['foundation'] = True
            
            technical_data['css_frameworks'] = css_frameworks
            
            # Responsive design
            viewport_meta = soup.find('meta', attrs={'name': 'viewport'})
            technical_data['responsive'] = viewport_meta is not None
            
            return technical_data
            
        except Exception as e:
            return {'error': str(e)}
    
    def _ai_powered_insights(self, analysis_data: Dict) -> Dict[str, Any]:
        """Generate AI-powered insights about the website."""
        try:
            # Prepare data for AI analysis
            basic_info = analysis_data.get('basic_info', {})
            seo = analysis_data.get('seo', {})
            performance = analysis_data.get('performance', {})
            security = analysis_data.get('security', {})
            
            prompt = f"""Analyze this website data and provide insights:

Website: {analysis_data.get('url')}
Title: {basic_info.get('title')}
Description: {basic_info.get('description')}
Load Time: {basic_info.get('load_time_seconds')}s
Page Size: {basic_info.get('page_size_kb')}KB
HTTPS: {security.get('https')}
Security Score: {security.get('security_score', 0)}%

SEO Data: {json.dumps(seo, default=str)[:500]}
Performance: {json.dumps(performance, default=str)[:500]}

Provide:
1. Overall website quality assessment (1-10)
2. Top 3 strengths
3. Top 3 areas for improvement
4. Specific recommendations
5. Competitive analysis insights
6. User experience assessment

Be specific and actionable."""

            ai_response = self.brain.think(prompt, max_tokens=1000)
            
            return {
                'ai_analysis': ai_response,
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def _generate_analysis_summary(self, analysis_data: Dict) -> str:
        """Generate a human-readable summary."""
        try:
            basic_info = analysis_data.get('basic_info', {})
            url = analysis_data.get('url', 'Unknown')
            
            summary = f"""
🔍 **Website Analysis Summary for {url}**

📊 **Basic Information:**
• Title: {basic_info.get('title', 'N/A')}
• Load Time: {basic_info.get('load_time_seconds', 'N/A')}s
• Page Size: {basic_info.get('page_size_kb', 'N/A')}KB
• Status: {basic_info.get('status_code', 'N/A')}

🔒 **Security:**
• HTTPS: {'✅' if analysis_data.get('security', {}).get('https') else '❌'}
• Security Score: {analysis_data.get('security', {}).get('security_score', 0):.1f}%

📈 **SEO:**
• Title Length: {analysis_data.get('seo', {}).get('title', {}).get('length', 'N/A')} chars
• Images with Alt: {analysis_data.get('seo', {}).get('images', {}).get('alt_percentage', 0)}%

⚡ **Performance:**
• Average Load Time: {analysis_data.get('performance', {}).get('load_times', {}).get('average', 'N/A')}s
• Compression: {'✅' if analysis_data.get('performance', {}).get('compression', {}).get('gzip_enabled') else '❌'}

🎯 **AI Insights:**
{analysis_data.get('ai_insights', {}).get('ai_analysis', 'Analysis not available')[:300]}...
"""
            
            return summary.strip()
            
        except Exception as e:
            return f"Summary generation failed: {e}"
    
    def _save_analysis(self, analysis_data: Dict):
        """Save analysis results."""
        try:
            analyses_dir = Path("website_analyses")
            analyses_dir.mkdir(exist_ok=True)
            
            # Create filename from URL and timestamp
            url_safe = analysis_data.get('url', 'unknown').replace('https://', '').replace('http://', '').replace('/', '_')
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{url_safe}_{timestamp}.json"
            
            # Remove soup and response objects for JSON serialization
            clean_data = analysis_data.copy()
            clean_data.pop('soup', None)
            clean_data.pop('response', None)
            
            with open(analyses_dir / filename, 'w') as f:
                json.dump(clean_data, f, indent=2, default=str)
            
            logger.info(f"✅ Analysis saved: {filename}")
            
        except Exception as e:
            logger.error(f"Failed to save analysis: {e}")
    
    def quick_analysis(self, url: str) -> str:
        """Quick website analysis with summary."""
        analysis = self.analyze_website(url, deep_analysis=False)
        
        if analysis.get('success'):
            return analysis.get('summary', 'Analysis completed but summary not available')
        else:
            return f"❌ Analysis failed: {analysis.get('error', 'Unknown error')}"
