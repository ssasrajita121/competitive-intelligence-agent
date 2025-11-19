"""
Competitive Intelligence + LinkedIn Content Generator
Main Streamlit Application
"""
import streamlit as st
from agents.research_agent import ResearchAgent
from agents.content_agent import ContentAgent
from config.config import Config
import json
import streamlit as st

# TEMPORARY: Force clear cache on every load
st.cache_data.clear()
st.cache_resource.clear()

# Rest of your app...
# ========== ADD THIS SECTION ==========
# Check configuration before starting app
is_valid, message = Config.validate()
if not is_valid:
    st.error(f"⚠️ Configuration Error: {message}")
    st.info("**Please set your API keys:**")
    st.code("""
# Local Development (.env file):
OPENAI_API_KEY=sk-...
NEWS_API_KEY=your-key-here

# Streamlit Cloud (Secrets):
OPENAI_API_KEY = "sk-..."
NEWS_API_KEY = "your-key-here"
    """, language="bash")
    st.stop()
# ========================================

# Page configuration
st.set_page_config(
    page_title=Config.PAGE_TITLE,
    page_icon=Config.PAGE_ICON,
    layout=Config.LAYOUT
)

# Initialize session state
if 'research_results' not in st.session_state:
    st.session_state.research_results = None
if 'generated_post' not in st.session_state:
    st.session_state.generated_post = None
if 'research_done' not in st.session_state:
    st.session_state.research_done = False

# Initialize agents
@st.cache_resource
def get_agents():
    """Initialize and cache agents"""
    return ResearchAgent(), ContentAgent()

research_agent, content_agent = get_agents()

# Title and description
st.title("🔍 Competitive Intelligence + Content Generator")
st.markdown("""
Generate LinkedIn posts based on competitive intelligence research.
**User-driven:** You control what to research and how to present it.
""")

st.divider()

# ====================
# STEP 1: RESEARCH
# ====================
st.header("Step 1: Research Your Topic")

col1, col2 = st.columns([3, 1])

with col1:
    topic = st.text_input(
        "What do you want to research?",
        placeholder="Example: Anthropic funding, RAG vs Fine-tuning, AI regulations",
        help="Enter a company, technology, trend, or topic you want to learn about"
    )

with col2:
    research_type = st.selectbox(
        "Research Type",
        ["Company News", "Technology", "Market Trend", "Industry News"]
    )

if st.button("🔍 Start Research", type="primary", disabled=not topic):
    with st.spinner(f"Researching {topic}..."):
        try:
            # Perform research
            results = research_agent.research_topic(topic, research_type.lower())
            st.session_state.research_results = results
            st.session_state.research_done = True
            if results.get('cached', False):
                st.success(f"✅ Research completed for: {topic}")
            else:
                st.success(f"⚡ Using cached data for: {topic} (instant!)")
        except Exception as e:
            st.error(f"❌ Research failed: {str(e)}")
            st.session_state.research_done = False

# Display research results
if st.session_state.research_done and st.session_state.research_results:
    st.divider()
    
    # Research Summary
    with st.expander("📊 Research Summary", expanded=True):
        results = st.session_state.research_results
        
        # Key Facts
        st.subheader("Key Facts")
        st.markdown(results.get('key_facts', 'No key facts available'))
        
        # Insights
        st.subheader("Insights")
        st.markdown(results.get('insights', 'No insights available'))
        
        # Sentiment
        sentiment = results.get('sentiment', 'Neutral')
        sentiment_emoji = {
            'Positive': '👍',
            'Negative': '👎',
            'Neutral': '😐'
        }
        st.metric("Overall Sentiment", f"{sentiment_emoji.get(sentiment, '😐')} {sentiment}")
    
    # Sources
    with st.expander("📰 News Sources", expanded=False):
        articles = results.get('news_articles', [])
        if articles:
            for article in articles[:5]:
                st.markdown(f"""
                **{article.get('title', 'No title')}**  
                *{article.get('source', 'Unknown')} - {article.get('published_at', 'Unknown date')}*  
                {article.get('description', '')}  
                [Read more]({article.get('url', '#')})
                """)
                st.divider()
        else:
            st.info("No news articles found. Using web search results.")
    
    # ====================
    # STEP 2: CHOOSE ANGLE
    # ====================
    st.divider()
    st.header("Step 2: Choose Your Post Angle")
    
    # Get suggested angles
    with st.spinner("Generating post angles..."):
        try:
            angles = research_agent.get_research_angles(
                results['topic'],
                results['summary']
            )
            st.markdown("**Suggested angles for your LinkedIn post:**")
            st.markdown(angles)
        except Exception as e:
            st.warning("Could not generate angles")
    
    # User selects what to post about
    col1, col2 = st.columns(2)
    
    with col1:
        selected_angle = st.text_area(
            "What angle do you want to focus on?",
            placeholder="Example: The $450M funding round, AI safety focus, etc.",
            help="Choose one of the suggested angles above or write your own"
        )
    
    with col2:
        post_style = st.selectbox(
            "Post Style",
            Config.POST_STYLES,
            help="Choose the tone and format for your post"
        )
    
    # ====================
    # STEP 3: GENERATE POST
    # ====================
    if st.button("✨ Generate LinkedIn Post", type="primary", disabled=not selected_angle):
        with st.spinner("Generating your LinkedIn post..."):
            try:
                post = content_agent.generate_linkedin_post(
                    topic=results['topic'],
                    research_summary=results['summary'],
                    style=post_style,
                    angle=selected_angle
                )
                st.session_state.generated_post = post
                st.success("✅ Post generated!")
            except Exception as e:
                st.error(f"❌ Post generation failed: {str(e)}")
    
    # Display generated post
    if st.session_state.generated_post:
        st.divider()
        st.header("Step 3: Your LinkedIn Post")
        
        # Display post in a nice box
        st.markdown("### 📝 Draft Post:")
        post_container = st.container()
        with post_container:
            st.text_area(
                "Your LinkedIn Post",
                value=st.session_state.generated_post,
                height=400,
                label_visibility="collapsed"
            )
        
        # Action buttons
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔄 Regenerate"):
                with st.spinner("Regenerating..."):
                    try:
                        new_post = content_agent.regenerate_post(
                            topic=results['topic'],
                            research_summary=results['summary'],
                            style=post_style,
                            previous_post=st.session_state.generated_post
                        )
                        st.session_state.generated_post = new_post
                        st.rerun()
                    except Exception as e:
                        st.error(f"Regeneration failed: {str(e)}")
        
        with col2:
            if st.button("✨ Improve Hook"):
                with st.spinner("Improving opening line..."):
                    try:
                        improved = content_agent.improve_hook(
                            st.session_state.generated_post,
                            results['topic']
                        )
                        st.session_state.generated_post = improved
                        st.rerun()
                    except Exception as e:
                        st.error(f"Hook improvement failed: {str(e)}")
        
        with col3:
            st.download_button(
                label="📋 Copy to Clipboard",
                data=st.session_state.generated_post,
                file_name=f"linkedin_post_{results['topic'].replace(' ', '_')}.txt",
                mime="text/plain"
            )
        
        st.info("💡 **Next Steps:** Review the post, make any edits, and manually post it to LinkedIn!")

# ====================
# SIDEBAR
# ====================
import streamlit as st
from config.config import Config

# ========== DEBUG TEST - ADD THIS ==========
st.sidebar.write("### 🔧 API Key Test")
if Config.OPENAI_API_KEY:
    st.sidebar.success(f"✅ Key found: {Config.OPENAI_API_KEY[:15]}...")
else:
    st.sidebar.error("❌ NO KEY FOUND!")
st.sidebar.write(f"**Key length:** {len(Config.OPENAI_API_KEY) if Config.OPENAI_API_KEY else 0}")
# ==========================================

# Rest of your app...
with st.sidebar:
    st.header("🔧 Debug Tools")
    
    # Clear Cache Button
    if st.button("🗑️ CLEAR ALL CACHE"):
        # Clear Streamlit cache
        st.cache_data.clear()
        st.cache_resource.clear()
        
        # Clear research agent cache
        try:
            from agents.research_agent import ResearchAgent
            agent = ResearchAgent()
            if hasattr(agent, 'cache_manager'):
                cleared = agent.cache_manager.clear_all()
                st.success(f"Cleared {cleared} cached research files!")
        except Exception as e:
            st.warning(f"Could not clear research cache: {e}")
        
        st.success("✅ All caches cleared! Try researching again.")
        st.rerun()
    
    st.divider()
with st.sidebar:
    st.header("ℹ️ How It Works")
    
    st.markdown("""
    ### User-Controlled Process:
    
    **Step 1: Research**
    - You provide the topic
    - AI researches news & web
    - Shows you the findings
    
    **Step 2: Choose Angle**
    - AI suggests post angles
    - You select what to write about
    - You choose the style
    
    **Step 3: Generate Post**
    - AI creates draft post
    - You review and edit
    - You manually post to LinkedIn
    
    ---
    
    ### 🎯 Features:
    - ✅ Multi-source research
    - ✅ AI-powered summaries
    - ✅ 5 post styles
    - ✅ Regenerate options
    - ✅ Full user control
    
    ---
    
    ### 🔒 Privacy:
    - No auto-posting
    - You control everything
    - Your API keys stay secure
    """)
    
    st.divider()
    
    st.markdown("""
    **Tech Stack:**
    - Python 3.11
    - Streamlit
    - OpenAI GPT
    - Multi-agent architecture
    """)
    
    # Reset button
    if st.button("🔄 Start New Research"):
        st.session_state.research_results = None
        st.session_state.generated_post = None
        st.session_state.research_done = False
        st.rerun()

# Footer
st.divider()
st.caption("🔍 Competitive Intelligence + Content Generator | User-driven research & content creation")