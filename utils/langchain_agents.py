from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from utils.groq_helpers import truncate_to_token_limit
from config import GROQ_API_KEY, DEFAULT_MODEL, DEFAULT_TEMP

def create_basic_chain(template, model_name=DEFAULT_MODEL, temperature=DEFAULT_TEMP):
    """Create a basic LangChain chain with the given template"""
    llm = ChatGroq(
        api_key=GROQ_API_KEY,
        model_name=model_name,
        temperature=temperature,
    )
    
    prompt = ChatPromptTemplate.from_template(template)
    return LLMChain(llm=llm, prompt=prompt)

def create_iterative_chain(task_description, model_name=DEFAULT_MODEL, temperature=DEFAULT_TEMP):
    """Create a chain that can iterate and refine outputs"""
    llm = ChatGroq(
        api_key=GROQ_API_KEY,
        model_name=model_name,
        temperature=temperature,
    )
    
    initial_template = """
    {task_description}
    
    Initial input: {input}
    
    Please create an initial draft based on the input.
    """
    
    refine_template = """
    {task_description}
    
    Current draft:
    {current_draft}
    
    Feedback: {feedback}
    
    Please refine the draft based on the feedback.
    """
    
    initial_prompt = ChatPromptTemplate.from_template(initial_template)
    refine_prompt = ChatPromptTemplate.from_template(refine_template)
    
    initial_chain = LLMChain(llm=llm, prompt=initial_prompt)
    refine_chain = LLMChain(llm=llm, prompt=refine_prompt)
    
    class IterativeChain:
        def __init__(self, task_description, initial_chain, refine_chain):
            self.task_description = task_description
            self.initial_chain = initial_chain
            self.refine_chain = refine_chain
            self.current_draft = None
        
        def initial_draft(self, input_text):
            """Generate the initial draft"""
            input_text = truncate_to_token_limit(input_text)
            result = self.initial_chain.invoke({
                "task_description": self.task_description,
                "input": input_text
            })
            self.current_draft = result["text"]
            return self.current_draft
        
        def refine(self, feedback):
            """Refine the current draft based on feedback"""
            if not self.current_draft:
                return "Please generate an initial draft first."
            
            result = self.refine_chain.invoke({
                "task_description": self.task_description,
                "current_draft": truncate_to_token_limit(self.current_draft),
                "feedback": feedback
            })
            self.current_draft = result["text"]
            return self.current_draft
    
    return IterativeChain(task_description, initial_chain, refine_chain)
