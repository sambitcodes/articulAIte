from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from utils.web_search import WebSearchTool
from config import GROQ_API_KEY, DEFAULT_MODEL, SEARCH_ENGINE, SEARCH_RESULTS_COUNT

class SearchEnabledAgent:
    """Agent that can perform web searches to enhance responses"""
    
    def __init__(self, model_name=DEFAULT_MODEL, temperature=0.7):
        self.model_name = model_name
        self.temperature = temperature
        self.search_tool = WebSearchTool(search_engine=SEARCH_ENGINE)
        self.llm = ChatGroq(
            api_key=GROQ_API_KEY,
            model_name=model_name,
            temperature=temperature,
        )
    
    def _create_prompt_with_search_results(self, base_template, search_results, **kwargs):
        """Add search results to the prompt template"""
        # Extract relevant information from search results
        search_info = []
        
        for result in search_results[:SEARCH_RESULTS_COUNT]:
            if isinstance(result, dict):
                # Tavily format
                if 'content' in result and 'url' in result:
                    search_info.append(f"Source: {result.get('title', 'Unknown')}\nURL: {result['url']}\nContent: {result['content']}\n")
            else:
                # Generic format - just add as string
                search_info.append(str(result))
        
        search_context = "\n\n".join(search_info)
        
        # Add search results to the template
        enhanced_template = base_template + "\n\nWeb search results:\n{search_results}\n\n"
        
        # Create prompt
        prompt = ChatPromptTemplate.from_template(enhanced_template)
        
        # Return chain and kwargs with search results
        kwargs["search_results"] = search_context
        return prompt, kwargs
    
    def run(self, base_template, search_query=None, **kwargs):
        """Run the agent with optional web search"""
        # If search query is provided, perform search
        if search_query:
            search_results = self.search_tool.search(search_query)
            prompt, updated_kwargs = self._create_prompt_with_search_results(base_template, search_results, **kwargs)
        else:
            # No search, use base template
            prompt = ChatPromptTemplate.from_template(base_template)
            updated_kwargs = kwargs
        
        # Create and run chain
        chain = LLMChain(llm=self.llm, prompt=prompt)
        response = chain.invoke(updated_kwargs)
        
        # Get attribution text if search was performed
        attribution = self.search_tool.get_attribution_text() if search_query else "No web search performed for this response."
        
        return response["text"], attribution
    
    def clear_search_history(self):
        """Clear search history"""
        self.search_tool.clear_history()


class ArticleSearchAgent(SearchEnabledAgent):
    """Specialized agent for article generation with web search"""
    
    def generate_article(self, topic, word_count, temperature, style):
        """Generate an article with web search enhancement"""
        # Update the temperature for this specific request
        self.llm.temperature = temperature
        
        # Create search query
        search_query = f"{topic} facts information research"
        
        # Base template
        base_template = """
        You are an expert content creator specializing in educational articles.
        
        Please write a comprehensive article about: {topic}
        
        Requirements:
        - Word Count: Approximately {word_count} words
        - Style: {style}
        - Format the article with proper Markdown formatting (headers, bullet points, etc.)
        - Include relevant subtopics and key concepts
        - The article should be well-structured with an introduction, body, and conclusion
        - Include practical examples or case studies where appropriate
        - Incorporate relevant information from the web search results provided
        
        Note: Temperature setting is {temperature} (0 = more factual/conservative, 1 = more creative/innovative)
        
        Write the article now:
        """
        
        return self.run(
            base_template, 
            search_query=search_query,
            topic=topic,
            word_count=word_count,
            temperature=temperature,
            style=style
        )


class StudyPlanSearchAgent(SearchEnabledAgent):
    """Specialized agent for study plan generation with web search"""
    
    def generate_study_plan(self, subject, duration_weeks, experience_level, goals):
        """Generate a study plan with web search enhancement"""
        # Create search query
        search_query = f"{subject} learning resources curriculum study guide {experience_level} level"
        
        # Base template
        base_template = """
        You are an educational expert specializing in curriculum development.
        
        Create a comprehensive study plan for:
        - Subject: {subject}
        - Duration: {duration_weeks} weeks
        - Experience Level: {experience_level}
        - Learning Goals: {goals}
        
        Your study plan should include:
        1. A week-by-week breakdown with specific topics for each week
        2. Estimated hours of study per topic
        3. Recommended learning resources for each topic (books, courses, websites, videos, etc.)
        4. Practice exercises or projects
        5. Assessment methods to track progress
        
        Format the study plan with proper Markdown formatting:
        - Use headers (## for weeks, ### for topics)
        - Use bullet points for resources and activities
        - Use tables where appropriate
        - Include a summary at the beginning
        
        Make the plan realistic, comprehensive, and tailored to the learner's level and goals.
        Use the web search results to recommend specific, current, and high-quality learning resources.
        """
        
        return self.run(
            base_template, 
            search_query=search_query,
            subject=subject,
            duration_weeks=duration_weeks,
            experience_level=experience_level,
            goals=goals
        )


class CodeExplainerSearchAgent(SearchEnabledAgent):
    """Specialized agent for code explanation with web search for relevant documentation"""
    
    def explain_code(self, code, language, explanation_type):
        """Explain code with web search enhancement"""
        # Create search query based on code content and language
        # Extract some keywords from the code to form a better search query
        code_preview = code[:200]  # Take first 200 chars
        
        # Look for imports or includes to identify libraries
        libraries = []
        lines = code_preview.split('\n')
        for line in lines:
            if 'import ' in line or 'from ' in line or 'require(' in line or '#include' in line:
                libraries.append(line.strip())
        
        # Form search query
        search_terms = " ".join(libraries[:3]) if libraries else code_preview
        search_query = f"{language} programming {search_terms} documentation"
        
        if explanation_type == "Line by line explanation":
            base_template = """
            You are an expert programming teacher specializing in {language}.
            
            Analyze this code:
            ```{language}
            {code}
            ```
            
            Provide a detailed, line-by-line explanation of what this code does. For each line or logical block:
            1. Show the line number or block
            2. Explain what it does in detail
            3. Highlight any important programming concepts demonstrated
            4. Note any potential issues or improvements
            
            Make your explanation clear and educational, as if teaching a junior developer.
            Use the web search results to provide accurate information about the libraries, functions, or patterns used.
            """
        elif explanation_type == "Fix errors":
            base_template = """
            You are an expert programming debugger specializing in {language}.
            
            Analyze this code that may have errors:
            ```{language}
            {code}
            ```
            
            Please:
            1. Identify all errors (syntax errors, logical errors, runtime errors, etc.)
            2. Explain what causes each error
            3. Provide a corrected version of the code
            4. Explain what changes you made and why they fix the issues
            
            Make your explanation clear and educational.
            Use the web search results to find accurate solutions to the errors identified.
            """
        elif explanation_type == "Optimize code":
            base_template = """
            You are an expert programming optimizer specializing in {language}.
            
            Analyze this code:
            ```{language}
            {code}
            ```
            
            Please:
            1. Identify any performance issues or inefficiencies
            2. Suggest specific optimizations with explanations
            3. Provide an optimized version of the code
            4. Explain the benefits of your optimizations (speed, memory usage, readability, etc.)
            
            Make your explanation clear, educational, and focused on best practices.
            Use the web search results to recommend modern optimization techniques or patterns.
            """
        else:  # "Solve coding problem"
            base_template = """
            You are an expert programming problem solver specializing in {language}.
            
            The user has provided a coding problem or asked for a solution. Here's their input:
            ```{language}
            {code}
            ```
            
            Please:
            1. Identify the problem to be solved
            2. Provide a well-structured solution in {language}
            3. Explain your approach and algorithm
            4. Add comments in the code to explain key steps
            5. Discuss the time and space complexity if relevant
            
            Ensure your solution is correct, efficient, and follows best practices for {language}.
            Use the web search results to find current best practices and approaches to this type of problem.
            """
            
        return self.run(
            base_template, 
            search_query=search_query,
            code=code,
            language=language
        )
