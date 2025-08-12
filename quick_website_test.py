#!/usr/bin/env python3
"""
Quick website analysis test - standalone version.
"""
import urllib.request
import re
import time

def analyze_website(url):
    """Simple website analysis."""
    try:
        print(f"🔍 Analyzing: {url}")
        
        # Ensure URL has protocol
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        # Create request
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'}
        )
        
        # Fetch website
        start_time = time.time()
        response = urllib.request.urlopen(req, timeout=30)
        load_time = time.time() - start_time
        
        # Read content
        content = response.read().decode('utf-8', errors='ignore')
        
        # Extract title
        title_match = re.search(r'<title[^>]*>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
        title = title_match.group(1).strip() if title_match else "No title found"
        title = re.sub(r'\s+', ' ', title)
        
        # Basic metrics
        page_size = len(content.encode('utf-8'))
        status_code = response.getcode()
        
        # Count elements
        images = len(re.findall(r'<img[^>]*>', content, re.IGNORECASE))
        links = len(re.findall(r'<a[^>]*href[^>]*>', content, re.IGNORECASE))
        
        # Results
        print(f"""
✅ **Website Analysis Complete!**

📊 **Basic Info:**
• Title: {title}
• Status: {status_code}
• Load Time: {load_time:.3f}s
• Page Size: {page_size/1024:.2f}KB

📈 **Content:**
• Images: {images}
• Links: {links}
• HTTPS: {'✅' if url.startswith('https://') else '❌'}

🎉 **Analysis successful!**
""")
        
        return True
        
    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Quick Website Analysis Test")
    print("=" * 40)
    
    # Test with example.com
    success = analyze_website("https://example.com")
    
    if success:
        print("\n✅ Test passed! Website analysis is working.")
        print("\nNow try with your website:")
        user_url = input("Enter URL: ").strip()
        if user_url:
            analyze_website(user_url)
    else:
        print("\n❌ Test failed!")
