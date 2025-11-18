"""
Configuration settings for Competitive Intelligence Agent
"""
import os
from dotenv import load_dotenv

# Load environment variables for local development
load_dotenv()


def get_secret(key: str, default: str = None) -> str:
    """
    Universal secret getter - works both locally and on Streamlit Cloud.
    
    Priority:
    1. Streamlit Secrets (for cloud deployment)
    2. Environment variables (for local .env)
    3. Default value
    
    Args:
        key: Secret key name
        default: Default value if not found
        
    Returns:
        Secret value or default
    """
    # Try Streamlit secrets first (Cloud)
    try:
        import streamlit as st
        if hasattr(st, 'secrets') and key in st.secrets:
            return st.secrets[key]
    except (ImportError, FileNotFoundError, AttributeError):
        pass
    
    # Fall back to environment variables (Local)
    value = os.getenv(key)
    if value is not None:
        return value
    
    # Return default
    return default


class Config:
    """Application configuration"""
    
    # API Keys - now works everywhere!
    OPENAI_API_KEY = get_secret("OPENAI_API_KEY")
    NEWS_API_KEY = get_secret("NEWS_API_KEY", "")
    
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
    CACHE_ENABLED = True
    CACHE_TTL_HOURS = 24
    CACHE_DIR = get_secret("CACHE_DIR", "data/cache")
    
    # Streamlit Settings
    PAGE_TITLE = "🔍 Competitive Intelligence + Content Generator"
    PAGE_ICON = "🔍"
    LAYOUT = "wide"
    
    @classmethod
    def validate(cls):
        """
        Validate that required API keys are present.
        Returns (is_valid, message) instead of raising exception.
        """
        if not cls.OPENAI_API_KEY:
            return False, "OPENAI_API_KEY not found"
        return True, "Configuration valid"
    
    @classmethod
    def get_missing_keys(cls):
        """Get list of missing required keys"""
        missing = []
        if not cls.OPENAI_API_KEY:
            missing.append("OPENAI_API_KEY")
        return missing


# DO NOT validate on import - let the app handle it