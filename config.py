import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

SEARCH_ENGINE = "serpapi"  # Options: "tavily", "serpapi"
SEARCH_RESULTS_COUNT = 5

# Model configurations
DEFAULT_MODEL = "llama3-70b-8192"
CODE_MODEL = "llama3-70b-8192"
ARTICLE_MODEL = "llama3-70b-8192"
STUDY_MODEL = "llama3-70b-8192"

# Temperature defaults
DEFAULT_TEMP = 0.7
CODE_TEMP = 0.2
ARTICLE_DEFAULT_TEMP = 0.5
STUDY_TEMP = 0.3

# Timeout settings
REQUEST_TIMEOUT = 120

# Source attribution placeholder (would be replaced with actual logic)
DEFAULT_SOURCE_ATTRIBUTION = "Generated with AI - no web search capability in this version"
