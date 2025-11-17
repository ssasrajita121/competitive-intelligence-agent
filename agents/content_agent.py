"""
Content Agent - Generates LinkedIn posts from research
"""
from utils.api_helpers import APIHelpers
from utils.prompts import Prompts
from config.config import Config
import re


class ContentAgent:
    """Agent responsible for generating LinkedIn content"""
    
    def __init__(self):
        self.api_helper = APIHelpers()
    
    def generate_linkedin_post(self, topic, research_summary, style, angle=None):
        """
        Generate a LinkedIn post based on research
        
        Args:
            topic: The main topic
            research_summary: Summary from research agent
            style: Post style (News Analysis, Educational, etc.)
            angle: Specific angle to focus on (optional)
            
        Returns:
            Generated LinkedIn post
        """
        print(f"✍️ Generating {style} post about {topic}")
        
        # Extract key points for the post
        key_points = self._extract_key_points(research_summary)
        
        # Generate the post based on style
        post = self._generate_post_by_style(
            topic=topic,
            style=style,
            key_points=key_points,
            research_summary=research_summary,
            angle=angle
        )
        
        # Enhance the post
        enhanced_post = self._enhance_post(post, topic)
        
        return enhanced_post
    
    def _extract_key_points(self, research_summary):
        """Extract 3-5 key points from research"""
        
        prompt = f"""From this research summary, extract 3-5 key points 
        that would be interesting for a LinkedIn post.
        
        Summary:
        {research_summary[:1500]}
        
        Return as a bulleted list:
        • Point 1
        • Point 2
        • Point 3
        """
        
        try:
            points = self.api_helper.call_openai(prompt, max_tokens=300)
            return points
        except Exception as e:
            print(f"Key point extraction error: {e}")
            return research_summary[:500]
    
    def _generate_post_by_style(self, topic, style, key_points, research_summary, angle):
        """Generate post based on selected style"""
        
        # Map style to prompt template
        style_prompts = {
            "News Analysis": self._generate_news_analysis,
            "Educational Explainer": self._generate_educational,
            "Personal Opinion": self._generate_opinion,
            "Engagement Question": self._generate_engagement,
            "Trend Prediction": self._generate_trend
        }
        
        # Get the appropriate generator function
        generator = style_prompts.get(
            style, 
            self._generate_generic
        )
        
        # Generate the post
        return generator(topic, key_points, research_summary, angle)
    
    def _generate_news_analysis(self, topic, key_points, research_summary, angle):
        """Generate news analysis style post"""
        
        prompt = Prompts.LINKEDIN_POST_NEWS_ANALYSIS.format(
            topic=topic,
            facts=key_points
        )
        
        try:
            post = self.api_helper.call_openai(
                prompt, 
                temperature=0.7,
                max_tokens=Config.MAX_TOKENS
            )
            return post
        except Exception as e:
            print(f"Post generation error: {e}")
            return self._generate_fallback_post(topic, key_points)
    
    def _generate_educational(self, topic, key_points, research_summary, angle):
        """Generate educational explainer style post"""
        
        prompt = Prompts.LINKEDIN_POST_EDUCATIONAL.format(
            topic=topic,
            concepts=key_points
        )
        
        try:
            post = self.api_helper.call_openai(
                prompt,
                temperature=0.7,
                max_tokens=Config.MAX_TOKENS
            )
            return post
        except Exception as e:
            return self._generate_fallback_post(topic, key_points)
    
    def _generate_opinion(self, topic, key_points, research_summary, angle):
        """Generate personal opinion style post"""
        
        # Determine stance from research
        stance = f"This development in {topic} is significant"
        
        prompt = Prompts.LINKEDIN_POST_OPINION.format(
            topic=topic,
            stance=stance,
            points=key_points
        )
        
        try:
            post = self.api_helper.call_openai(
                prompt,
                temperature=0.8,
                max_tokens=Config.MAX_TOKENS
            )
            return post
        except Exception as e:
            return self._generate_fallback_post(topic, key_points)
    
    def _generate_engagement(self, topic, key_points, research_summary, angle):
        """Generate engagement question style post"""
        
        prompt = Prompts.LINKEDIN_POST_ENGAGEMENT.format(
            topic=topic,
            context=key_points
        )
        
        try:
            post = self.api_helper.call_openai(
                prompt,
                temperature=0.7,
                max_tokens=Config.MAX_TOKENS
            )
            return post
        except Exception as e:
            return self._generate_fallback_post(topic, key_points)
    
    def _generate_trend(self, topic, key_points, research_summary, angle):
        """Generate trend prediction style post"""
        
        prompt = f"""Write a LinkedIn post predicting future trends based on {topic}.
        
        Current insights:
        {key_points}
        
        Structure:
        1. What's happening now
        2. Why it matters
        3. What's coming next (prediction)
        4. How to prepare
        5. Engagement question
        
        Tone: Analytical but accessible
        Length: 150-200 words
        Include: Emojis and hashtags
        
        Write the post:
        """
        
        try:
            post = self.api_helper.call_openai(
                prompt,
                temperature=0.8,
                max_tokens=Config.MAX_TOKENS
            )
            return post
        except Exception as e:
            return self._generate_fallback_post(topic, key_points)
    
    def _generate_generic(self, topic, key_points, research_summary, angle):
        """Generic post generator (fallback)"""
        
        prompt = Prompts.LINKEDIN_POST_BASE.format(
            topic=topic,
            style="Informative",
            key_points=key_points
        )
        
        try:
            post = self.api_helper.call_openai(prompt)
            return post
        except Exception as e:
            return self._generate_fallback_post(topic, key_points)
    
    def _enhance_post(self, post, topic):
        """Enhance the post with better formatting and hashtags"""
        
        # Add hashtags if missing
        if "#" not in post:
            hashtags = self._generate_hashtags(topic, post)
            post = f"{post}\n\n{hashtags}"
        
        return post.strip()
    
    def _generate_hashtags(self, topic, post):
        """Generate relevant hashtags for the post"""
        
        prompt = Prompts.ADD_HASHTAGS.format(post_content=post[:500])
        
        try:
            hashtags = self.api_helper.call_openai(
                prompt,
                temperature=0.5,
                max_tokens=50
            )
            return hashtags.strip()
        except Exception as e:
            # Fallback hashtags
            topic_words = topic.split()[:2]
            return f"#{''.join(topic_words)} #AI #Technology #Innovation #Business"
    
    def _generate_fallback_post(self, topic, key_points):
        """Simple fallback post if AI generation fails"""
        
        return f"""Interesting developments in {topic} 🔍

{key_points}

What are your thoughts on this?

#Technology #Innovation #Business"""
    
    def improve_hook(self, current_post, topic):
        """Improve the opening line of a post"""
        
        lines = current_post.split('\n')
        current_hook = lines[0] if lines else ""
        
        prompt = Prompts.IMPROVE_HOOK.format(
            current_hook=current_hook,
            topic=topic
        )
        
        try:
            improved_hook = self.api_helper.call_openai(
                prompt,
                temperature=0.8,
                max_tokens=50
            )
            
            # Replace first line
            lines[0] = improved_hook.strip()
            return '\n'.join(lines)
        except Exception as e:
            return current_post
    
    def regenerate_post(self, topic, research_summary, style, previous_post):
        """Regenerate a post with a different angle"""
        
        prompt = f"""The following LinkedIn post needs to be rewritten with a fresh angle:

Previous post:
{previous_post}

Topic: {topic}
Style: {style}
Research: {research_summary[:500]}

Generate a completely different post on the same topic with:
- Different opening hook
- Different angle/perspective
- Different examples or points
- Same professional tone
- 150-200 words

Write the new post:
"""
        
        try:
            new_post = self.api_helper.call_openai(
                prompt,
                temperature=0.9,
                max_tokens=Config.MAX_TOKENS
            )
            return self._enhance_post(new_post, topic)
        except Exception as e:
            return previous_post


# Helper function for easy import
def create_content_agent():
    """Factory function to create a content agent"""
    return ContentAgent()