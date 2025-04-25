from langchain_groq import ChatGroq
from config import GROQ_API_KEY, REQUEST_TIMEOUT

def get_groq_llm(model_name, temperature=0.7):
    """Create and return a Groq LLM instance with the specified parameters"""
    return ChatGroq(
        api_key=GROQ_API_KEY,
        model_name=model_name,
        temperature=temperature,
        timeout=REQUEST_TIMEOUT
    )

def get_token_estimate(text):
    """Get a rough estimate of token count for a text string"""
    # A rough approximation: 4 characters per token
    return len(text) // 4

def truncate_to_token_limit(text, max_tokens=8000):
    """Truncate text to stay within token limits"""
    # Rough estimate of token count
    estimated_tokens = get_token_estimate(text)
    
    if estimated_tokens <= max_tokens:
        return text
    
    # Calculate how many characters to keep (very approximate)
    chars_to_keep = int(max_tokens * 4 * 0.9)  # 90% to be safe
    
    # Truncate and add a note
    truncated = text[:chars_to_keep]
    return truncated + "\n\n[Note: Text was truncated to fit token limits]"
