import os
from langchain_community.utilities.tavily_search import TavilySearchAPIWrapper
from langchain_community.utilities import SerpAPIWrapper
from dotenv import load_dotenv
import json
from datetime import datetime
from config import TAVILY_API_KEY, SERPAPI_API_KEY
# Load environment variables
load_dotenv()

class WebSearchTool:
    """Web search utility that supports multiple search backends"""
    
    def __init__(self, search_engine="tavily"):
        """Initialize the search tool with the specified backend"""
        self.search_engine = search_engine
        self.setup_search_tool()
        self.search_history = []
        
    def setup_search_tool(self):
        """Set up the appropriate search backend"""
        if self.search_engine == "tavily":
            self.api_key = TAVILY_API_KEY
            if not self.api_key:
                raise ValueError("TAVILY_API_KEY not found in environment variables")
            self.search_tool = TavilySearchAPIWrapper(api_key=self.api_key)
        
        elif self.search_engine == "serpapi":
            self.api_key = SERPAPI_API_KEY
            if not self.api_key:
                raise ValueError("SERPAPI_API_KEY not found in environment variables")
            self.search_tool = SerpAPIWrapper(serpapi_api_key=self.api_key)
        
        else:
            raise ValueError(f"Unsupported search engine: {self.search_engine}")
    
    def search(self, query, num_results=5):
        """Run a web search and return the results"""
        try:
            if self.search_engine == "tavily":
                results = self.search_tool.results(query, max_results=num_results)
                # Record search for attribution
                self.record_search(query, results)
                return results
            
            elif self.search_engine == "serpapi":
                results = self.search_tool.results(query, num_results=num_results)
                # Record search for attribution
                self.record_search(query, results)
                return results
        
        except Exception as e:
            print(f"Search error: {str(e)}")
            return []
    
    def record_search(self, query, results):
        """Record search query and results for attribution"""
        sources = []
        
        # Extract sources based on the search engine's result format
        if self.search_engine == "tavily":
            for result in results:
                if 'url' in result:
                    sources.append({
                        'title': result.get('title', 'Unknown Title'),
                        'url': result['url']
                    })
        
        elif self.search_engine == "serpapi":
            # SerpAPI structure is different
            organic_results = results.get('organic_results', [])
            for result in organic_results:
                if 'link' in result:
                    sources.append({
                        'title': result.get('title', 'Unknown Title'),
                        'url': result['link']
                    })
        
        # Add to search history
        self.search_history.append({
            'query': query,
            'timestamp': datetime.now().isoformat(),
            'sources': sources
        })
    
    def get_attribution_text(self):
        """Generate attribution text based on search history"""
        if not self.search_history:
            return "No web searches performed for this response."
        
        # Get unique sources from the last few searches
        recent_searches = self.search_history[-3:]  # Last 3 searches
        all_sources = []
        
        for search in recent_searches:
            all_sources.extend(search['sources'])
        
        # Get unique sources
        unique_sources = []
        urls_seen = set()
        
        for source in all_sources:
            if source['url'] not in urls_seen:
                urls_seen.add(source['url'])
                unique_sources.append(source)
        
        # Limit to top 5 sources
        unique_sources = unique_sources[:5]
        
        # Create attribution text
        if unique_sources:
            attribution = "Information from web search results including:\n"
            for idx, source in enumerate(unique_sources, 1):
                attribution += f"{idx}. {source['title']} ({source['url']})\n"
            return attribution
        else:
            return "Web search performed but no specific sources to cite."
    
    def clear_history(self):
        """Clear search history"""
        self.search_history = []
