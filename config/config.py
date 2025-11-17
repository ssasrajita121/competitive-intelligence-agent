"""
Configuration settings for Competitive Intelligence Agent
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration"""
    
    # API Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    NEWS_API_KEY = os.getenv("NEWS_API_KEY", "")
    
    # OpenAI Settings
    OPENAI_MODEL = "gpt-3.5-turbo"
    OPENAI_TEMPERATURE = 0.7
    MAX_TOKENS = 1000
    
    # Research Settings
    MAX_SEARCH_RESULTS = 10
    RESEARCH_DAYS_BACK = 30
    
    # Content Settings
    POST_STYLES = [
        "News Analysis",
        "Educational Explainer",
        "Personal Opinion",
        "Engagement Question",
        "Trend Prediction"
    ]
    
    # RAG Settings
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200
    TOP_K_RESULTS = 5
    
    # Cache Settings
    ENABLE_CACHE = True
    CACHE_DIR = "data/cache"
    
    # Streamlit Settings
    PAGE_TITLE = "🔍 Competitive Intelligence + Content Generator"
    PAGE_ICON = "🔍"
    LAYOUT = "wide"
    
    @classmethod
    def validate(cls):
        """Validate that required API keys are present"""
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        return True

# Validate on import
Config.validate()