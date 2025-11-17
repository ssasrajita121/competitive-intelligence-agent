"""
Prompt templates for different agents
"""

class Prompts:
    """Centralized prompt management"""
    
    # Research Agent Prompts
    RESEARCH_SUMMARY = """
    You are a research analyst. Analyze the following information about "{topic}":
    
    {content}
    
    Provide a structured summary with:
    1. Key Facts (bullet points)
    2. Main Insights (2-3 sentences)
    3. Implications (what this means)
    4. Sentiment (overall tone: positive/negative/neutral)
    
    Be concise and focus on actionable insights.
    """
    
    EXTRACT_KEY_POINTS = """
    Extract the 5 most important points from this content:
    
    {content}
    
    Format as numbered list. Each point should be one clear sentence.
    """
    
    # Content Generation Prompts
    LINKEDIN_POST_BASE = """
    You are a LinkedIn content expert. Create an engaging LinkedIn post about:
    
    Topic: {topic}
    Style: {style}
    Key Points: {key_points}
    
    Guidelines:
    - Start with a hook (first line must grab attention)
    - Use short paragraphs (2-3 lines max)
    - Include relevant emojis (but don't overdo it)
    - End with engagement question or call-to-action
    - Add 3-5 relevant hashtags at the end
    - Professional but conversational tone
    - Length: 150-250 words
    
    Write the post now:
    """
    
    LINKEDIN_POST_NEWS_ANALYSIS = """
    You are writing a LinkedIn post analyzing recent news.
    
    Topic: {topic}
    Facts: {facts}
    
    Structure:
    1. Lead with the news (what happened)
    2. Why it matters (2-3 points)
    3. Implications for the industry
    4. Your perspective or prediction
    5. Engagement question
    
    Tone: Analytical but accessible
    Length: 150-200 words
    Include: Relevant emojis and hashtags
    
    Write the post:
    """
    
    LINKEDIN_POST_EDUCATIONAL = """
    You are writing an educational LinkedIn post to teach something.
    
    Topic: {topic}
    Key Concepts: {concepts}
    
    Structure:
    1. Hook: Common misconception or question
    2. Clear explanation (use analogies if helpful)
    3. Practical example
    4. Key takeaway
    5. Ask readers about their experience
    
    Tone: Friendly teacher, not condescending
    Length: 150-250 words
    Include: Clear formatting, emojis, hashtags
    
    Write the post:
    """
    
    LINKEDIN_POST_OPINION = """
    You are sharing a personal opinion/hot take.
    
    Topic: {topic}
    Your Stance: {stance}
    Supporting Points: {points}
    
    Structure:
    1. Bold opening statement (your opinion)
    2. Context (why you're talking about this)
    3. Your reasoning (2-3 points)
    4. Acknowledge other perspectives
    5. Invite debate/discussion
    
    Tone: Confident but respectful
    Length: 150-200 words
    Include: Emojis, hashtags
    
    Write the post:
    """
    
    LINKEDIN_POST_ENGAGEMENT = """
    You are creating a post to spark conversation.
    
    Topic: {topic}
    Context: {context}
    
    Structure:
    1. Present an interesting question or scenario
    2. Provide context (1-2 paragraphs)
    3. Show different perspectives
    4. Ask for audience input
    
    Tone: Curious and inviting
    Length: 100-150 words
    Focus: Getting comments and engagement
    
    Write the post:
    """
    
    # Helper Prompts
    IMPROVE_HOOK = """
    Improve this opening line for a LinkedIn post:
    
    Current: {current_hook}
    Topic: {topic}
    
    Make it more attention-grabbing. Use curiosity, surprise, or bold statement.
    Return only the improved hook (one line).
    """
    
    ADD_HASHTAGS = """
    Suggest 5 relevant hashtags for this LinkedIn post:
    
    {post_content}
    
    Return as: #Tag1 #Tag2 #Tag3 #Tag4 #Tag5
    Mix popular and niche tags.
    """
    
    @classmethod
    def get_post_prompt(cls, style, **kwargs):
        """Get the appropriate prompt based on post style"""
        style_map = {
            "News Analysis": cls.LINKEDIN_POST_NEWS_ANALYSIS,
            "Educational Explainer": cls.LINKEDIN_POST_EDUCATIONAL,
            "Personal Opinion": cls.LINKEDIN_POST_OPINION,
            "Engagement Question": cls.LINKEDIN_POST_ENGAGEMENT
        }
        
        prompt_template = style_map.get(style, cls.LINKEDIN_POST_BASE)
        return prompt_template.format(**kwargs)