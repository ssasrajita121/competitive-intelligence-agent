"""
API helper functions for external data sources
"""
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from openai import OpenAI
from config.config import Config
import os

# Remove proxy environment variables that conflict with OpenAI client
for proxy_var in ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy']:
    if proxy_var in os.environ:
        del os.environ[proxy_var]

# Initialize OpenAI client (NEW pattern for openai>=1.0)
client = None
if Config.OPENAI_API_KEY:
    try:
        client = OpenAI(api_key=Config.OPENAI_API_KEY)
    except Exception as e:
        print(f"OpenAI client initialization error: {e}")
        client = None


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
        # Check if API key is available
        if not Config.OPENAI_API_KEY:
            raise RuntimeError(
                "❌ OPENAI_API_KEY not configured!\n\n"
                "Local: Add to .env file\n"
                "Cloud: Add to Streamlit Secrets"
            )
        
        # Check if client is initialized
        if client is None:
            raise RuntimeError("OpenAI client not initialized. Check logs for initialization errors.")
        
        try:
            response = client.chat.completions.create(
                model=Config.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are a helpful AI assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature or Config.OPENAI_TEMPERATURE,
                max_tokens=max_tokens or Config.MAX_TOKENS
            )
            
            content = response.choices[0].message.content
            
            # Validate response is not empty
            if not content or content.strip() == "":
                raise ValueError("OpenAI returned empty response")
            
            return content
            
        except Exception as e:
            raise Exception(f"Error calling OpenAI: {str(e)}")
    
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
        try:
            # Use News API if key is available
            if Config.NEWS_API_KEY:
                from_date = (datetime.now() - timedelta(days=days_back)).isoformat()
                url = "https://newsapi.org/v2/everything"
                params = {
                    "q": query,
                    "from": from_date,
                    "sortBy": "relevancy",
                    "language": "en",
                    "apiKey": Config.NEWS_API_KEY
                }
                
                try:
                    response = requests.get(url, params=params, timeout=10)
                    if response.status_code == 200:
                        data = response.json()
                        articles = data.get("articles", [])
                        return articles[:Config.MAX_SEARCH_RESULTS]
                    else:
                        print(f"News API error: {response.status_code}")
                except requests.exceptions.Timeout:
                    print(f"News API timeout - using fallback data")
                except requests.exceptions.RequestException as req_err:
                    print(f"News API request error: {req_err}")
            
            # Fallback: Return simulated results for development
            return [
                {
                    "title": f"Breaking: Major developments in {query}",
                    "description": f"Recent analysis shows {query} is experiencing significant growth and innovation. Industry experts are closely monitoring the situation.",
                    "url": "https://newsapi.org",
                    "source": {"name": "Tech News"},
                    "publishedAt": datetime.now().isoformat()
                },
                {
                    "title": f"{query}: Market Analysis and Industry Trends",
                    "description": f"New data reveals {query} is reshaping the industry landscape. Key players are making strategic investments.",
                    "url": "https://newsapi.org",
                    "source": {"name": "Industry Report"},
                    "publishedAt": datetime.now().isoformat()
                },
                {
                    "title": f"What {query} Means for Business Innovation",
                    "description": f"Companies are increasingly adopting {query} technology to stay competitive in the rapidly evolving market.",
                    "url": "https://newsapi.org",
                    "source": {"name": "Business Insider"},
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
                "title": f"Comprehensive Guide to {query}",
                "link": f"https://example.com/guide-{i+1}",
                "snippet": f"Everything you need to know about {query}. Industry insights, best practices, and expert analysis."
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