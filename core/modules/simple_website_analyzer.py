"""
Simple Website Analyzer for Jarvis.
Basic website analysis using only standard library modules.
"""
import urllib.request
import urllib.parse
import json
import re
import time
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
from core.utils.log import logger


class SimpleWebsiteAnalyzer:
    def __init__(self, brain):
        self.brain = brain
        
    def analyze_website(self, url: str, deep_analysis: bool = True) -> Dict[str, Any]:
        """Perform basic website analysis using standard library."""
        try:
            logger.info(f"🔍 Analyzing website: {url}")
            
            # Ensure URL has protocol
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            analysis_result = {
                'url': url,
                'timestamp': datetime.now().isoformat(),
                'analysis_type': 'basic',
                'success': True
            }
            
            # Basic website fetch and analysis
            basic_analysis = self._basic_website_analysis(url)
            analysis_result.update(basic_analysis)
            
            if deep_analysis and basic_analysis.get('success'):
                # Additional analysis
                content_analysis = self._analyze_content(basic_analysis.get('content', ''))
                analysis_result['content_analysis'] = content_analysis
                
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
        """Perform basic website analysis using urllib."""
        try:
            # Create request with headers
            req = urllib.request.Request(
                url,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                }
            )
            
            # Fetch the website
            start_time = time.time()
            response = urllib.request.urlopen(req, timeout=30)
            load_time = time.time() - start_time
            
            # Read content
            content = response.read().decode('utf-8', errors='ignore')
            
            # Basic information
            title = self._extract_title(content)
            description = self._extract_meta_description(content)
            
            # Basic metrics
            page_size = len(content.encode('utf-8'))
            status_code = response.getcode()
            
            # Count elements
            images_count = len(re.findall(r'<img[^>]*>', content, re.IGNORECASE))
            links_count = len(re.findall(r'<a[^>]*href[^>]*>', content, re.IGNORECASE))
            scripts_count = len(re.findall(r'<script[^>]*>', content, re.IGNORECASE))
            
            return {
                'success': True,
                'basic_info': {
                    'title': title,
                    'description': description,
                    'status_code': status_code,
                    'page_size_bytes': page_size,
                    'page_size_kb': round(page_size / 1024, 2),
                    'load_time_seconds': round(load_time, 3),
                    'final_url': response.geturl()
                },
                'elements': {
                    'images_count': images_count,
                    'links_count': links_count,
                    'scripts_count': scripts_count
                },
                'content': content,
                'headers': dict(response.headers)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _extract_title(self, content: str) -> str:
        """Extract title from HTML content."""
        try:
            title_match = re.search(r'<title[^>]*>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
            if title_match:
                title = title_match.group(1).strip()
                # Clean up title (remove extra whitespace, newlines)
                title = re.sub(r'\s+', ' ', title)
                return title
            return "No title found"
        except:
            return "No title found"
    
    def _extract_meta_description(self, content: str) -> str:
        """Extract meta description from HTML content."""
        try:
            desc_match = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\']([^"\']*)["\']', content, re.IGNORECASE)
            if desc_match:
                return desc_match.group(1).strip()
            return "No description found"
        except:
            return "No description found"
    
    def _analyze_content(self, content: str) -> Dict[str, Any]:
        """Analyze HTML content for additional insights."""
        try:
            content_analysis = {}
            
            # Check for HTTPS
            content_analysis['https_used'] = 'https://' in content.lower()
            
            # Check for responsive design indicators
            viewport_meta = re.search(r'<meta[^>]*name=["\']viewport["\']', content, re.IGNORECASE)
            content_analysis['responsive_design'] = viewport_meta is not None
            
            # Check for common frameworks
            frameworks = {
                'jquery': bool(re.search(r'jquery', content, re.IGNORECASE)),
                'bootstrap': bool(re.search(r'bootstrap', content, re.IGNORECASE)),
                'react': bool(re.search(r'react', content, re.IGNORECASE)),
                'vue': bool(re.search(r'vue\.js|vuejs', content, re.IGNORECASE)),
                'angular': bool(re.search(r'angular', content, re.IGNORECASE))
            }
            content_analysis['frameworks'] = frameworks
            
            # Count headings
            headings = {}
            for i in range(1, 7):
                headings[f'h{i}'] = len(re.findall(f'<h{i}[^>]*>', content, re.IGNORECASE))
            content_analysis['headings'] = headings
            
            # Check for forms
            forms_count = len(re.findall(r'<form[^>]*>', content, re.IGNORECASE))
            content_analysis['forms_count'] = forms_count
            
            # Extract text content (rough)
            text_content = re.sub(r'<[^>]+>', '', content)
            text_content = re.sub(r'\s+', ' ', text_content).strip()
            words = text_content.split()
            
            content_analysis['text_stats'] = {
                'total_characters': len(text_content),
                'total_words': len(words),
                'average_word_length': round(sum(len(word) for word in words) / len(words), 2) if words else 0
            }
            
            # Check for social media links
            social_patterns = {
                'facebook': r'facebook\.com|fb\.com',
                'twitter': r'twitter\.com|x\.com',
                'instagram': r'instagram\.com',
                'linkedin': r'linkedin\.com',
                'youtube': r'youtube\.com|youtu\.be'
            }
            
            social_links = {}
            for platform, pattern in social_patterns.items():
                matches = re.findall(pattern, content, re.IGNORECASE)
                social_links[platform] = len(matches) > 0
            
            content_analysis['social_media'] = social_links
            
            return content_analysis
            
        except Exception as e:
            logger.error(f"Content analysis failed: {e}")
            return {}
    
    def _ai_powered_insights(self, analysis_data: Dict) -> Dict[str, Any]:
        """Generate AI-powered insights about the website."""
        try:
            # Prepare data for AI analysis
            basic_info = analysis_data.get('basic_info', {})
            content_analysis = analysis_data.get('content_analysis', {})
            
            prompt = f"""Analyze this website data and provide insights:

Website: {analysis_data.get('url')}
Title: {basic_info.get('title')}
Description: {basic_info.get('description')}
Load Time: {basic_info.get('load_time_seconds')}s
Page Size: {basic_info.get('page_size_kb')}KB
HTTPS: {content_analysis.get('https_used')}
Responsive: {content_analysis.get('responsive_design')}
Frameworks: {content_analysis.get('frameworks', {})}

Provide:
1. Overall website quality assessment (1-10)
2. Top 3 strengths
3. Top 3 areas for improvement
4. Specific recommendations
5. User experience assessment

Be specific and actionable."""

            ai_response = self.brain.think(prompt, max_tokens=800)
            
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
            content_analysis = analysis_data.get('content_analysis', {})
            url = analysis_data.get('url', 'Unknown')
            
            summary = f"""
🔍 **Website Analysis Summary for {url}**

📊 **Basic Information:**
• Title: {basic_info.get('title', 'N/A')}
• Load Time: {basic_info.get('load_time_seconds', 'N/A')}s
• Page Size: {basic_info.get('page_size_kb', 'N/A')}KB
• Status: {basic_info.get('status_code', 'N/A')}

🔒 **Security & Design:**
• HTTPS: {'✅' if content_analysis.get('https_used') else '❌'}
• Responsive: {'✅' if content_analysis.get('responsive_design') else '❌'}

📈 **Content:**
• Images: {analysis_data.get('elements', {}).get('images_count', 'N/A')}
• Links: {analysis_data.get('elements', {}).get('links_count', 'N/A')}
• Scripts: {analysis_data.get('elements', {}).get('scripts_count', 'N/A')}

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
            
            # Remove content for JSON serialization (too large)
            clean_data = analysis_data.copy()
            clean_data.pop('content', None)
            
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
