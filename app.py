import streamlit as st
from groq import Groq
from components.cv_analyzer import cv_assistant
from components.code_explainer import code_assistant
from components.article_generator import article_assistant
from components.study_planner import study_assistant
from components.home import home_page
import groq
import config

# Page configuration
st.set_page_config(
    page_title="articulAIte",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
with open('assets/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# App title
with st.container(border=True):
    st.title(":green[articul]:blue[AI]:green[te] 🤖")
    st.markdown("***:violet[Your comprehensive career development tool powered by AI]***")

# Initialize session state for conversation history
if "cv_messages" not in st.session_state:
    st.session_state.cv_messages = []
    
if "code_messages" not in st.session_state:
    st.session_state.code_messages = []
    
if "article_messages" not in st.session_state:
    st.session_state.article_messages = []
    
if "study_messages" not in st.session_state:
    st.session_state.study_messages = []

if 'groq_api_key' not in st.session_state:
    st.session_state.groq_api_key = ""

if 'serp_api_key' not in st.session_state:
    st.session_state.serp_api_key = ""

if 'tavily_api_key' not in st.session_state:
    st.session_state.tavily_api_key = ""

st.session_state.groq_api_key = st.sidebar.text_input(placeholder="Enter your Groq API key here",
                                                         label="Groq API Key",
                                                       value = st.session_state.groq_api_key,
                                                       type="password",
                                                       help="Your Groq API key is required to use this app. You can get it from [Groq](https://groq.com).")

st.session_state.serp_api_key = st.sidebar.text_input(placeholder="Enter your Serp API key here",
                                                         label="Serp API Key",
                                                       value = st.session_state.serp_api_key,
                                                       type="password",
                                                       help="Your Serp API key is required to use this app. You can get it from [Serp](https://serpapi.com).")

st.session_state.tavily_api_key = st.sidebar.text_input(placeholder="Enter your Tavily API key here",
                                                         label="Tavily API Key",
                                                       value = st.session_state.tavily_api_key,
                                                       type="password",
                                                       help="Your Tavily API key is required to use this app. You can get it from [Tavily](https://tavily.com).")


if st.session_state.groq_api_key:
        try:
            client = groq.Client(api_key=st.session_state.groq_api_key)
            # Just a simple API test
            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": "Hello"}],
                model="llama-3.3-70b-versatile",
                max_tokens=1000
            )
            st.sidebar.success("Groq API connected successfully! 🚀")
        except Exception as e:
            st.sidebar.error(f"Error connecting to Groq API: {str(e)}")

config.GROQ_API_KEY = st.session_state.groq_api_key
config.SERP_API_KEY = st.session_state.serp_api_key
config.TAVILY_API_KEY = st.session_state.tavily_api_key

# Create sidebar for navigation
st.sidebar.title("Navigation ")
page = st.sidebar.selectbox(
    "Select a feature:",
    [
        "Home",
        "Interview Helper (Resume/CV)", 
        "Code Helper", 
        "Article Generator", 
        "Study Plan Generator"
    ]
)

# Main content based on selected page
if page == "Home":
    home_page()
    
elif page == "Interview Helper (Resume/CV)":
    cv_assistant()
    
elif page == "Code Helper":
    code_assistant()
    
elif page == "Article Generator":
    article_assistant()
    
elif page == "Study Plan Generator":
    study_assistant()

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("© sambitcodes :heart: :sparkles:")
