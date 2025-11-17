"""
API helper functions for external data sources
"""
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import openai
from config.config import Config

# Set OpenAI API key
openai.api_key = Config.OPENAI_API_KEY


class APIHelpers:
    """Helper functions for API calls"""
    
    @staticmethod
    def call_openai(prompt, temperature=None, max_tokens=None):
        """
        Call OpenAI API with given prompt
        
        Args:
            prompt: The prompt string
            temperature: Sampling temperature (default from config)
            max_tokens: Max tokens to generate (default from config)
            
        Returns:
            Generated text response
        """
        try:
            response = openai.chat.completions.create(
                model=Config.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are a helpful AI assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature or Config.OPENAI_TEMPERATURE,
                max_tokens=max_tokens or Config.MAX_TOKENS
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")
    
    @staticmethod
    def search_news(query, days_back=30):
        """
        Search for recent news articles
        
        Args:
            query: Search query
            days_back: How many days back to search
            
        Returns:
            List of news articles (title, url, date, source)
        """
        # For now, we'll use a simple web search
        # In production, you'd use News API or Google News API
        
        try:
            # Placeholder - replace with actual news API
            # Example with News API (when you get the key):
            """
            if Config.NEWS_API_KEY:
                from_date = (datetime.now() - timedelta(days=days_back)).isoformat()
                url = f"https://newsapi.org/v2/everything"
                params = {
                    "q": query,
                    "from": from_date,
                    "sortBy": "relevance",
                    "apiKey": Config.NEWS_API_KEY
                }
                response = requests.get(url, params=params)
                if response.status_code == 200:
                    data = response.json()
                    return data.get("articles", [])[:Config.MAX_SEARCH_RESULTS]
            """
            
            # Fallback: Return simulated results for development
            return [
                {
                    "title": f"Search results for: {query}",
                    "description": "This is a placeholder. Add News API key for real results.",
                    "url": "https://newsapi.org",
                    "source": {"name": "NewsAPI"},
                    "publishedAt": datetime.now().isoformat()
                }
            ]
            
        except Exception as e:
            print(f"News search error: {str(e)}")
            return []
    
    @staticmethod
    def scrape_webpage(url):
        """
        Scrape content from a webpage
        
        Args:
            url: URL to scrape
            
        Returns:
            Cleaned text content
        """
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text
            text = soup.get_text()
            
            # Clean up text
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            return text[:5000]  # Limit to first 5000 chars
            
        except Exception as e:
            return f"Error scraping webpage: {str(e)}"
    
    @staticmethod
    def get_google_search_results(query, num_results=5):
        """
        Simulate Google search results
        
        In production, use Google Custom Search API or SerpAPI
        
        Args:
            query: Search query
            num_results: Number of results to return
            
        Returns:
            List of search results
        """
        # Placeholder for development
        # In production, use: https://serpapi.com/ or Google Custom Search
        
        return [
            {
                "title": f"Result {i+1} for: {query}",
                "link": f"https://example.com/article-{i+1}",
                "snippet": f"This is a snippet about {query}. Add SerpAPI key for real results."
            }
            for i in range(num_results)
        ]


class DataProcessor:
    """Process and clean data"""
    
    @staticmethod
    def clean_text(text):
        """Clean and normalize text"""
        if not text:
            return ""
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        # Remove special characters (keep basic punctuation)
        # Add more cleaning as needed
        
        return text
    
    @staticmethod
    def extract_date(date_string):
        """Extract and format date"""
        try:
            if isinstance(date_string, str):
                dt = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
            else:
                dt = date_string
            return dt.strftime("%B %d, %Y")
        except:
            return "Unknown date"
    
    @staticmethod
    def truncate_text(text, max_length=1000):
        """Truncate text to max length"""
        if len(text) <= max_length:
            return text
        return text[:max_length] + "..."