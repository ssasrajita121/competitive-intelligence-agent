"""
Research Agent - Handles data gathering and analysis
"""
from utils.api_helpers import APIHelpers, DataProcessor
from utils.prompts import Prompts
from config.config import Config
from datetime import datetime
from utils.cache_manager import CacheManager
import json


class ResearchAgent:
    """Agent responsible for researching topics and gathering insights"""
    
    def __init__(self):
        self.api_helper = APIHelpers()
        self.data_processor = DataProcessor()
        self.cache_manager = CacheManager(ttl_hours=Config.CACHE_TTL_HOURS)  # NEW!
    
    def research_topic(self, topic, research_type="company"):
        """
        Main research function - coordinates all research activities
        
        Args:
            topic: The topic to research (company name, technology, etc.)
            research_type: Type of research ("company", "trend", "technology", "news")
            
        Returns:
            Dictionary with research results
        """
        print(f"🔍 Researching: {topic}")
        
        # CHECK CACHE FIRST (NEW in v2.0!)
        if Config.CACHE_ENABLED:
            cached_results = self.cache_manager.get(topic, research_type)
            if cached_results:
                print("⚡ Using cached data - instant results!")
                return cached_results
        
        # Cache miss - do fresh research
        print("🌐 Fetching fresh data from APIs...")
        
        # Gather data from multiple sources
        news_results = self._search_news(topic)
        web_results = self._search_web(topic)
        
        # Analyze and summarize
        summary = self._generate_summary(topic, news_results, web_results)
        
        # Extract key insights
        insights = self._extract_insights(topic, summary)
        
        # Compile results
        results = {
            "topic": topic,
            "research_type": research_type,
            "timestamp": datetime.now().isoformat(),
            "news_articles": news_results,
            "web_results": web_results,
            "summary": summary,
            "insights": insights,
            "key_facts": self._extract_key_facts(summary),
            "sentiment": self._analyze_sentiment(summary),
            "cached": False  # NEW: indicate this is fresh data
        }
        
        # CACHE THE RESULTS (NEW in v2.0!)
        if Config.CACHE_ENABLED:
            self.cache_manager.set(topic, research_type, results)
        
        return results
    
    def _search_news(self, query):
        """Search for recent news articles"""
        try:
            articles = self.api_helper.search_news(query, days_back=Config.RESEARCH_DAYS_BACK)
            
            # Process and clean articles
            processed_articles = []
            for article in articles[:Config.MAX_SEARCH_RESULTS]:
                processed_articles.append({
                    "title": article.get("title", ""),
                    "description": article.get("description", ""),
                    "url": article.get("url", ""),
                    "source": article.get("source", {}).get("name", "Unknown"),
                    "published_at": self.data_processor.extract_date(
                        article.get("publishedAt", "")
                    )
                })
            
            return processed_articles
        except Exception as e:
            print(f"News search error: {e}")
            return []
    
    def _search_web(self, query):
        """Search the web for additional information"""
        try:
            results = self.api_helper.get_google_search_results(
                query, 
                num_results=5
            )
            return results
        except Exception as e:
            print(f"Web search error: {e}")
            return []
    
    def _generate_summary(self, topic, news_results, web_results):
        """Generate a summary of all research findings"""
        
        # Combine all content
        content = f"Topic: {topic}\n\n"
        
        # Add news
        content += "Recent News:\n"
        for article in news_results[:5]:
            content += f"- {article['title']}\n"
            if article['description']:
                content += f"  {article['description']}\n"
        
        # Add web results
        content += "\nWeb Results:\n"
        for result in web_results[:3]:
            content += f"- {result.get('title', '')}\n"
            content += f"  {result.get('snippet', '')}\n"
        
        # Use LLM to create summary
        prompt = Prompts.RESEARCH_SUMMARY.format(
            topic=topic,
            content=content
        )
        
        try:
            summary = self.api_helper.call_openai(prompt)
            return summary
        except Exception as e:
            print(f"Summary generation error: {e}")
            return content  # Fallback to raw content
    
    def _extract_insights(self, topic, summary):
        """Extract key insights from the summary"""
        
        prompt = f"""Based on this research summary about {topic}, 
        identify the 3 most important insights or takeaways.
        
        Summary:
        {summary}
        
        Format as:
        1. [First insight]
        2. [Second insight]
        3. [Third insight]
        """
        
        try:
            insights = self.api_helper.call_openai(prompt, max_tokens=300)
            return insights
        except Exception as e:
            print(f"Insight extraction error: {e}")
            return "Unable to extract insights"
    
    def _extract_key_facts(self, summary):
        """Extract key facts as bullet points"""
        
        prompt = Prompts.EXTRACT_KEY_POINTS.format(content=summary)
        
        try:
            facts = self.api_helper.call_openai(prompt, max_tokens=300)
            return facts
        except Exception as e:
            print(f"Fact extraction error: {e}")
            return ""
    
    def _analyze_sentiment(self, text):
        """Analyze sentiment of the research findings"""
        
        prompt = f"""Analyze the overall sentiment of this text in one word:
        Positive, Negative, or Neutral.
        
        Text: {text[:500]}
        
        Answer with just one word:"""
        
        try:
            sentiment = self.api_helper.call_openai(
                prompt, 
                temperature=0.3,
                max_tokens=10
            ).strip()
            return sentiment
        except Exception as e:
            print(f"Sentiment analysis error: {e}")
            return "Neutral"
    
    def get_research_angles(self, topic, summary):
        """
        Suggest different angles for LinkedIn posts based on research
        
        Returns:
            List of possible post angles
        """
        prompt = f"""Based on this research about {topic}, suggest 5 interesting 
        angles for LinkedIn posts. Each angle should be one sentence.
        
        Research Summary:
        {summary[:1000]}
        
        Format as:
        1. [Angle 1]
        2. [Angle 2]
        3. [Angle 3]
        4. [Angle 4]
        5. [Angle 5]
        """
        
        try:
            angles = self.api_helper.call_openai(prompt, max_tokens=300)
            return angles
        except Exception as e:
            print(f"Angle generation error: {e}")
            return "1. Main news update\n2. Industry impact\n3. Personal take"


# Helper function for easy import
def create_research_agent():
    """Factory function to create a research agent"""
    return ResearchAgent()