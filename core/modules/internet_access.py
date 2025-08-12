"""
Internet Access module for Jarvis.
Provides web browsing, research, and real-time information capabilities.
Enhanced with Supreme Consciousness knowledge synthesis.
"""
import requests
import json
from typing import Dict, List, Optional
from urllib.parse import quote_plus
from core.utils.log import logger


class InternetAccess:
    def __init__(self, brain):
        self.brain = brain
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Knowledge synthesis capabilities
        self.knowledge_domains = {
            'computer_science': ['software', 'algorithm', 'programming', 'AI', 'data', 'computing', 'code'],
            'business': ['market', 'customer', 'revenue', 'strategy', 'profit', 'business', 'company'],
            'psychology': ['behavior', 'motivation', 'user', 'human', 'cognitive', 'mental', 'emotion'],
            'engineering': ['system', 'design', 'build', 'optimize', 'efficiency', 'performance', 'technical'],
            'mathematics': ['calculate', 'model', 'analyze', 'statistics', 'probability', 'number'],
            'physics': ['energy', 'force', 'motion', 'quantum', 'mechanics', 'physics'],
            'biology': ['natural', 'evolution', 'adaptation', 'organism', 'ecosystem', 'biological'],
            'philosophy': ['ethical', 'moral', 'principle', 'logic', 'reasoning', 'philosophical']
        }
        
        self.concept_relationships = {}
        self.cross_domain_insights = []

    def search_web(self, query: str, num_results: int = 5) -> str:
        """Search the web and return results."""
        try:
            # Use DuckDuckGo Instant Answer API (no API key required)
            search_url = f"https://api.duckduckgo.com/?q={quote_plus(query)}&format=json&no_html=1&skip_disambig=1"
            
            response = self.session.get(search_url, timeout=10)
            data = response.json()
            
            result = f"🔍 **Search Results for: {query}**\n\n"
            
            # Get instant answer if available
            if data.get('Abstract'):
                result += f"**Summary:** {data['Abstract']}\n"
                if data.get('AbstractURL'):
                    result += f"**Source:** {data['AbstractURL']}\n\n"
            
            # Get related topics
            if data.get('RelatedTopics'):
                result += "**Related Information:**\n"
                for i, topic in enumerate(data['RelatedTopics'][:num_results]):
                    if isinstance(topic, dict) and topic.get('Text'):
                        result += f"{i+1}. {topic['Text']}\n"
                        if topic.get('FirstURL'):
                            result += f"   🔗 {topic['FirstURL']}\n"
                result += "\n"
            
            # If no results, try alternative search
            if not data.get('Abstract') and not data.get('RelatedTopics'):
                result += "No direct results found. Try a more specific search term.\n"
            
            return result
            
        except Exception as e:
            return f"❌ Error searching web: {e}"

    def get_website_content(self, url: str) -> str:
        """Fetch and summarize website content."""
        try:
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            
            # Basic content extraction (you could use BeautifulSoup for better parsing)
            content = response.text
            
            # Ask AI to summarize the content
            prompt = f"""Summarize this website content in a clear, concise way:

URL: {url}
Content (first 2000 chars): {content[:2000]}...

Provide:
1. Main purpose/topic of the website
2. Key information or features
3. Relevant details for the user

Keep it concise but informative."""
            
            summary = self.brain.think(prompt, max_tokens=300)
            
            return f"📄 **Website Summary: {url}**\n\n{summary}"
            
        except Exception as e:
            return f"❌ Error fetching website: {e}"

    def get_current_trends(self, topic: str = "technology") -> str:
        """Get current trends and news."""
        try:
            # Search for recent trends
            query = f"latest {topic} trends 2024 news"
            return self.search_web(query, 8)
            
        except Exception as e:
            return f"❌ Error getting trends: {e}"

    def research_topic(self, topic: str) -> str:
        """Research a topic comprehensively."""
        try:
            # Search for the topic
            search_results = self.search_web(topic, 5)
            
            # Ask AI to provide comprehensive research
            prompt = f"""Based on these search results, provide comprehensive research on: {topic}

Search Results:
{search_results}

Please provide:
1. Overview of the topic
2. Key facts and current information
3. Recent developments or trends
4. Practical applications or implications
5. Additional resources or areas to explore

Make it informative and well-structured."""
            
            research = self.brain.think(prompt, max_tokens=800)
            
            return f"📚 **Research Report: {topic}**\n\n{research}\n\n---\n**Source Data:**\n{search_results}"
            
        except Exception as e:
            return f"❌ Error researching topic: {e}"

    def check_website_status(self, url: str) -> str:
        """Check if a website is accessible."""
        try:
            response = self.session.head(url, timeout=10)
            status_code = response.status_code
            
            if status_code == 200:
                return f"✅ {url} is accessible (Status: {status_code})"
            elif status_code == 404:
                return f"❌ {url} not found (Status: 404)"
            elif status_code >= 500:
                return f"⚠️ {url} server error (Status: {status_code})"
            else:
                return f"⚠️ {url} returned status: {status_code}"
                
        except requests.exceptions.Timeout:
            return f"⏱️ {url} timed out"
        except requests.exceptions.ConnectionError:
            return f"❌ Cannot connect to {url}"
        except Exception as e:
            return f"❌ Error checking {url}: {e}"

    def get_weather(self, location: str = "current location") -> str:
        """Get weather information."""
        try:
            # Use a free weather API or search
            query = f"weather {location} today"
            return self.search_web(query, 3)
            
        except Exception as e:
            return f"❌ Error getting weather: {e}"

    def get_news(self, topic: str = "technology") -> str:
        """Get latest news on a topic."""
        try:
            query = f"latest news {topic} today"
            return self.search_web(query, 6)
            
        except Exception as e:
            return f"❌ Error getting news: {e}"

    def find_resources(self, topic: str, resource_type: str = "tutorials") -> str:
        """Find learning resources on a topic."""
        try:
            query = f"{topic} {resource_type} guide documentation"
            results = self.search_web(query, 5)
            
            prompt = f"""Based on these search results, recommend the best learning resources for: {topic}

Search Results:
{results}

Provide:
1. Top recommended resources
2. Brief description of each
3. Skill level (beginner/intermediate/advanced)
4. Why each resource is valuable

Focus on high-quality, practical resources."""
            
            recommendations = self.brain.think(prompt, max_tokens=400)
            
            return f"📖 **Learning Resources: {topic}**\n\n{recommendations}"
            
        except Exception as e:
            return f"❌ Error finding resources: {e}"

    def analyze_competitor(self, website_url: str) -> str:
        """Analyze a competitor website."""
        try:
            # Get website content
            content_summary = self.get_website_content(website_url)
            
            # Ask AI to analyze
            prompt = f"""Analyze this competitor website and provide insights:

{content_summary}

Provide analysis on:
1. Business model and target audience
2. Key features and offerings
3. Design and user experience approach
4. Strengths and potential weaknesses
5. Opportunities for differentiation

Be objective and constructive."""
            
            analysis = self.brain.think(prompt, max_tokens=600)
            
            return f"🔍 **Competitor Analysis**\n\n{analysis}"
            
        except Exception as e:
            return f"❌ Error analyzing competitor: {e}"

    # ========== SUPREME CONSCIOUSNESS KNOWLEDGE SYNTHESIS METHODS ==========

    def synthesize_cross_domain_research(self, topic: str, domains: List[str] = None) -> str:
        """Research a topic across multiple knowledge domains"""
        try:
            if not domains:
                domains = self._identify_relevant_domains(topic)
            
            domain_research = {}
            
            # Research the topic from each domain perspective
            for domain in domains[:5]:  # Limit to 5 domains for performance
                domain_query = f"{topic} from {domain} perspective analysis"
                domain_results = self.search_web(domain_query, 3)
                domain_research[domain] = domain_results
            
            # Synthesize cross-domain insights
            synthesis_prompt = f"""Synthesize insights about '{topic}' from multiple knowledge domains:

Domain Research:
{json.dumps(domain_research, indent=2)}

Provide:
1. Cross-domain connections and patterns
2. Unique insights from each domain perspective
3. Breakthrough solutions combining multiple domains
4. Novel approaches not obvious from single-domain thinking
5. Practical applications leveraging cross-domain knowledge

Focus on innovative connections between domains."""
            
            synthesis = self.brain.think(synthesis_prompt, max_tokens=800)
            
            # Store insights for future use
            self.cross_domain_insights.append({
                'topic': topic,
                'domains': domains,
                'synthesis': synthesis,
                'timestamp': requests.utils.default_headers()
            })
            
            return f"🧠 **Cross-Domain Knowledge Synthesis: {topic}**\n\n{synthesis}"
            
        except Exception as e:
            return f"❌ Error in cross-domain research: {e}"

    def connect_concepts(self, concept_a: str, concept_b: str) -> str:
        """Find unexpected connections between two concepts"""
        try:
            # Research both concepts
            research_a = self.search_web(f"{concept_a} principles applications", 3)
            research_b = self.search_web(f"{concept_b} principles applications", 3)
            
            # Find connections
            connection_prompt = f"""Find unexpected and innovative connections between these two concepts:

Concept A: {concept_a}
Research: {research_a}

Concept B: {concept_b}
Research: {research_b}

Identify:
1. Surprising parallels or similarities
2. How principles from one could apply to the other
3. Hybrid approaches combining both concepts
4. Novel solutions using both concepts together
5. Metaphorical or structural connections

Be creative and think outside conventional boundaries."""
            
            connections = self.brain.think(connection_prompt, max_tokens=600)
            
            # Store relationship for future reference
            self.concept_relationships[f"{concept_a}_{concept_b}"] = connections
            
            return f"🔗 **Concept Connections: {concept_a} ↔ {concept_b}**\n\n{connections}"
            
        except Exception as e:
            return f"❌ Error connecting concepts: {e}"

    def research_with_breakthrough_thinking(self, problem: str) -> str:
        """Research a problem with breakthrough solution generation"""
        try:
            # Standard research
            standard_research = self.research_topic(problem)
            
            # Identify relevant domains
            domains = self._identify_relevant_domains(problem)
            
            # Research unconventional approaches
            unconventional_queries = [
                f"{problem} unconventional solutions creative approaches",
                f"{problem} biomimicry nature-inspired solutions",
                f"{problem} interdisciplinary approaches breakthrough methods",
                f"{problem} disruptive innovation paradigm shift"
            ]
            
            unconventional_research = []
            for query in unconventional_queries:
                result = self.search_web(query, 2)
                unconventional_research.append(result)
            
            # Generate breakthrough solutions
            breakthrough_prompt = f"""Generate breakthrough solutions for: {problem}

Standard Research:
{standard_research}

Unconventional Approaches:
{' '.join(unconventional_research)}

Relevant Domains: {domains}

Generate:
1. Revolutionary approaches that challenge assumptions
2. Solutions inspired by other domains or nature
3. Paradigm-shifting perspectives on the problem
4. Innovative combinations of existing solutions
5. Future-oriented solutions using emerging technologies

Think beyond conventional wisdom and current limitations."""
            
            breakthrough_solutions = self.brain.think(breakthrough_prompt, max_tokens=800)
            
            return f"💡 **Breakthrough Research: {problem}**\n\n{breakthrough_solutions}\n\n---\n**Foundation Research:**\n{standard_research}"
            
        except Exception as e:
            return f"❌ Error in breakthrough research: {e}"

    def analyze_trends_across_domains(self, trend_topic: str) -> str:
        """Analyze how a trend manifests across different domains"""
        try:
            domains = ['technology', 'business', 'society', 'science', 'culture']
            domain_trends = {}
            
            for domain in domains:
                query = f"{trend_topic} trends {domain} 2024 impact"
                trend_data = self.search_web(query, 3)
                domain_trends[domain] = trend_data
            
            # Cross-domain trend analysis
            analysis_prompt = f"""Analyze how the trend '{trend_topic}' manifests across different domains:

Domain Trends:
{json.dumps(domain_trends, indent=2)}

Provide:
1. Common patterns across all domains
2. Domain-specific manifestations and impacts
3. Cross-domain influences and spillover effects
4. Emerging opportunities at domain intersections
5. Future implications and convergence points
6. Strategic insights for leveraging this trend

Focus on interconnections and systemic effects."""
            
            analysis = self.brain.think(analysis_prompt, max_tokens=800)
            
            return f"📊 **Cross-Domain Trend Analysis: {trend_topic}**\n\n{analysis}"
            
        except Exception as e:
            return f"❌ Error in trend analysis: {e}"

    def generate_expert_insights(self, topic: str, expertise_level: str = 'phd') -> str:
        """Generate expert-level insights on a topic"""
        try:
            # Research the topic comprehensively
            comprehensive_research = self.research_topic(topic)
            
            # Get latest developments
            latest_developments = self.search_web(f"{topic} latest research developments 2024", 5)
            
            # Generate expert insights
            expert_prompt = f"""Provide {expertise_level}-level expert insights on: {topic}

Comprehensive Research:
{comprehensive_research}

Latest Developments:
{latest_developments}

As a world-class expert, provide:
1. Deep technical understanding and nuanced perspectives
2. Critical analysis of current approaches and limitations
3. Identification of knowledge gaps and research opportunities
4. Expert predictions and future directions
5. Practical implications for practitioners and researchers
6. Connections to cutting-edge developments in the field

Demonstrate mastery-level understanding with specific, actionable insights."""
            
            expert_insights = self.brain.think(expert_prompt, max_tokens=1000)
            
            return f"🎓 **Expert Insights ({expertise_level.upper()}): {topic}**\n\n{expert_insights}"
            
        except Exception as e:
            return f"❌ Error generating expert insights: {e}"

    def map_knowledge_relationships(self, central_concept: str, depth: int = 2) -> str:
        """Map relationships between concepts around a central topic"""
        try:
            # Start with central concept
            concept_map = {central_concept: {'level': 0, 'connections': []}}
            
            # Find related concepts
            related_query = f"{central_concept} related concepts principles applications"
            related_research = self.search_web(related_query, 5)
            
            # Extract key concepts (simplified - in practice would use NLP)
            mapping_prompt = f"""Create a knowledge relationship map for: {central_concept}

Research Data:
{related_research}

Identify:
1. Core related concepts (level 1 connections)
2. Secondary concepts connected to the core ones (level 2)
3. Relationship types (causal, analogical, hierarchical, etc.)
4. Strength of relationships (strong, moderate, weak)
5. Bidirectional influences and feedback loops

Format as a structured knowledge map showing concept relationships."""
            
            knowledge_map = self.brain.think(mapping_prompt, max_tokens=700)
            
            return f"🗺️ **Knowledge Relationship Map: {central_concept}**\n\n{knowledge_map}"
            
        except Exception as e:
            return f"❌ Error mapping knowledge relationships: {e}"

    def _identify_relevant_domains(self, topic: str) -> List[str]:
        """Identify relevant knowledge domains for a topic"""
        topic_lower = topic.lower()
        relevant_domains = []
        
        for domain, keywords in self.knowledge_domains.items():
            if any(keyword in topic_lower for keyword in keywords):
                relevant_domains.append(domain)
        
        # Ensure we have at least 3 domains for comprehensive analysis
        if len(relevant_domains) < 3:
            default_domains = ['computer_science', 'psychology', 'business']
            for domain in default_domains:
                if domain not in relevant_domains:
                    relevant_domains.append(domain)
                if len(relevant_domains) >= 3:
                    break
        
        return relevant_domains[:5]  # Limit to 5 domains

    def get_synthesis_insights(self) -> str:
        """Get accumulated cross-domain insights"""
        if not self.cross_domain_insights:
            return "No cross-domain insights accumulated yet."
        
        insights_summary = "🧠 **Accumulated Cross-Domain Insights:**\n\n"
        for i, insight in enumerate(self.cross_domain_insights[-5:], 1):  # Last 5 insights
            insights_summary += f"{i}. **{insight['topic']}** (Domains: {', '.join(insight['domains'])})\n"
            insights_summary += f"   Key Insight: {insight['synthesis'][:200]}...\n\n"
        
        return insights_summary
