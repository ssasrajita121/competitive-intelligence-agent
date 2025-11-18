"""
Simple caching system for research results
Reduces API calls and improves performance
"""
import json
import os
from datetime import datetime, timedelta
import hashlib


class CacheManager:
    """Manages caching of research results"""
    
    def __init__(self, cache_dir="data/cache", ttl_hours=24):
        """
        Initialize cache manager
        
        Args:
            cache_dir: Directory to store cache files
            ttl_hours: Time to live in hours (default 24)
        """
        self.cache_dir = cache_dir
        self.ttl = timedelta(hours=ttl_hours)
        
        # Create cache directory if it doesn't exist
        os.makedirs(cache_dir, exist_ok=True)
    
    def _get_cache_key(self, topic, research_type="general"):
        """
        Generate a unique cache key for a topic
        
        Args:
            topic: The research topic
            research_type: Type of research
            
        Returns:
            Hashed cache key
        """
        # Create a unique key based on topic and type
        key_string = f"{topic.lower()}_{research_type.lower()}"
        # Hash it to create a valid filename
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def _get_cache_path(self, cache_key):
        """Get full path to cache file"""
        return os.path.join(self.cache_dir, f"{cache_key}.json")
    
    def get(self, topic, research_type="general"):
        """
        Get cached research results
        
        Args:
            topic: The research topic
            research_type: Type of research
            
        Returns:
            Cached data if valid, None if not found or expired
        """
        cache_key = self._get_cache_key(topic, research_type)
        cache_path = self._get_cache_path(cache_key)
        
        # Check if cache file exists
        if not os.path.exists(cache_path):
            return None
        
        try:
            # Read cache file
            with open(cache_path, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)
            
            # Check if cache is still valid
            cached_time = datetime.fromisoformat(cache_data['cached_at'])
            age = datetime.now() - cached_time
            
            if age < self.ttl:
                print(f"✅ Cache HIT: Using cached data (age: {age.seconds//3600}h {(age.seconds//60)%60}m)")
                return cache_data['data']
            else:
                print(f"❌ Cache EXPIRED: Data is {age.days} days old")
                return None
                
        except Exception as e:
            print(f"Cache read error: {e}")
            return None
    
    def set(self, topic, research_type, data):
        """
        Cache research results
        
        Args:
            topic: The research topic
            research_type: Type of research
            data: Data to cache
            
        Returns:
            True if successful, False otherwise
        """
        cache_key = self._get_cache_key(topic, research_type)
        cache_path = self._get_cache_path(cache_key)
        
        try:
            # Prepare cache data
            cache_data = {
                'topic': topic,
                'research_type': research_type,
                'cached_at': datetime.now().isoformat(),
                'data': data
            }
            
            # Write to cache file
            with open(cache_path, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, indent=2, ensure_ascii=False)
            
            print(f"💾 Cached results for: {topic}")
            return True
            
        except Exception as e:
            print(f"Cache write error: {e}")
            return False
    
    def invalidate(self, topic, research_type="general"):
        """
        Invalidate (delete) cached data for a topic
        
        Args:
            topic: The research topic
            research_type: Type of research
            
        Returns:
            True if deleted, False if not found
        """
        cache_key = self._get_cache_key(topic, research_type)
        cache_path = self._get_cache_path(cache_key)
        
        try:
            if os.path.exists(cache_path):
                os.remove(cache_path)
                print(f"🗑️ Invalidated cache for: {topic}")
                return True
            return False
        except Exception as e:
            print(f"Cache invalidation error: {e}")
            return False
    
    def clear_all(self):
        """Clear all cached data"""
        try:
            count = 0
            for filename in os.listdir(self.cache_dir):
                if filename.endswith('.json'):
                    os.remove(os.path.join(self.cache_dir, filename))
                    count += 1
            print(f"🗑️ Cleared {count} cache files")
            return count
        except Exception as e:
            print(f"Cache clear error: {e}")
            return 0
    
    def get_cache_stats(self):
        """
        Get statistics about cached data
        
        Returns:
            Dictionary with cache statistics
        """
        try:
            cache_files = [f for f in os.listdir(self.cache_dir) if f.endswith('.json')]
            total_count = len(cache_files)
            valid_count = 0
            expired_count = 0
            
            for filename in cache_files:
                cache_path = os.path.join(self.cache_dir, filename)
                with open(cache_path, 'r', encoding='utf-8') as f:
                    cache_data = json.load(f)
                
                cached_time = datetime.fromisoformat(cache_data['cached_at'])
                age = datetime.now() - cached_time
                
                if age < self.ttl:
                    valid_count += 1
                else:
                    expired_count += 1
            
            return {
                'total': total_count,
                'valid': valid_count,
                'expired': expired_count,
                'ttl_hours': self.ttl.total_seconds() / 3600
            }
        except Exception as e:
            print(f"Cache stats error: {e}")
            return {'total': 0, 'valid': 0, 'expired': 0}


# Helper function for easy import
def create_cache_manager(ttl_hours=24):
    """Factory function to create a cache manager"""
    return CacheManager(ttl_hours=ttl_hours)