import streamlit as st
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from config import GROQ_API_KEY, CODE_MODEL, CODE_TEMP, DEFAULT_SOURCE_ATTRIBUTION
import pygments
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
import markdown

def format_code(code, language):
    """Format code with syntax highlighting"""
    try:
        lexer = get_lexer_by_name(language, stripall=True)
        formatter = HtmlFormatter(style="monokai")
        result = pygments.highlight(code, lexer, formatter)
        css = formatter.get_style_defs('.highlight')
        return f"<style>{css}</style>{result}"
    except Exception:
        # Fall back to markdown formatting if specific lexer is not found
        return markdown.markdown(f"```{language}\n{code}\n```")

def explain_code(code, model, language, explanation_type):
    """Generate code explanation using Groq"""
    try:
        llm = ChatGroq(
            api_key=GROQ_API_KEY,
            model_name=model,
            temperature=CODE_TEMP,
        )
        
        if explanation_type == "Line by line explanation":
            template = """
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
            """
        elif explanation_type == "Fix errors":
            template = """
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
            """
        elif explanation_type == "Optimize code":
            template = """
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
            """
        else:  # "Solve coding problem"
            template = """
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
            """
            
        prompt = ChatPromptTemplate.from_template(template)
        chain = LLMChain(llm=llm, prompt=prompt)
        response = chain.invoke({"code": code, "language": language})
        
        return response["text"], DEFAULT_SOURCE_ATTRIBUTION
    except Exception as e:
        return f"Error in analyzing code: {str(e)}", DEFAULT_SOURCE_ATTRIBUTION

def display_chat_messages():
    """Display chat history"""
    for message in st.session_state.code_messages:
        with st.chat_message(message["role"]):
            # Format code snippets in the content if needed
            if message.get("is_code", False):
                st.markdown(message["content"], unsafe_allow_html=True)
            else:
                st.markdown(message["content"])
                
            if "source" in message and message["role"] == "assistant":
                st.markdown(f"<div class='source-citation'>{message['source']}</div>", unsafe_allow_html=True)

def code_assistant():
    """Main code explanation assistant"""
    with st.expander("About", expanded=False):
        st.header("Code Explainer & Problem Solver </>👨🏻‍💻💻 </>")
        st.markdown("""
        Paste your code or coding problems to get:
        - :red[Line-by-line explanations]
        - :red[Error identification and fixes]
        - :red[Code optimization suggestions]
        - :red[Solutions to coding problems]
        """)
    
    # Language selection
    left_col, right_col = st.columns([1, 2])
    with right_col:
        language = st.selectbox(
            "Select programming language",
            ["python", "javascript", "java", "c++", "c#", "ruby", "go", "rust", "php", "typescript", "sql", "html", "css", "other"]
        )
    
        if language == "other":
            language = st.text_input("Specify language")
        
        model_choice = st.selectbox("Select model for analysis",
            options=["llama3-70b-8192","llama-3.3-70b-versatile", "gemma2-9b-it","deepseek-r1-distill-llama-70b"],
            index=0)
    
    # Explanation type selection
    with left_col:
        with st.container(border=True):
            explanation_type = st.radio(
                "What do you need help with?",
                ["Line by line explanation", "Fix errors", "Optimize code", "Solve coding problem"]
            )
    
    # Code input area
    code_input = st.text_area(
        "Enter your code or describe your coding problem",
        height=250,
        help="Paste code or describe a coding problem"
    )
    
    # Display chat history
    display_chat_messages()
    
    # Submit button for code analysis
    if code_input and st.button("Analyze Code"):
        # Format code for display
        formatted_code = format_code(code_input, language)
        
        # Add user message to chat history
        prompt_text = f"Please {explanation_type.lower()} for this {language} code."
        st.session_state.code_messages.append({"role": "user", "content": prompt_text})
        st.session_state.code_messages.append({"role": "user", "content": formatted_code, "is_code": True})
        
        # Process with groq
        with st.spinner("Analyzing code..."):
            response, source = explain_code(code_input,model_choice, language, explanation_type)
        
        # Add assistant response to chat history
        st.session_state.code_messages.append({"role": "assistant", "content": response, "source": source})
        
        # Rerun to display messages
        st.rerun()
    
    # Chat input for follow-up questions
    if user_input := st.chat_input("Ask follow-up questions about your code..."):
        # Add user message to chat history
        st.session_state.code_messages.append({"role": "user", "content": user_input})
        
        # Display the new message
        with st.chat_message("user"):
            st.markdown(user_input)
        
        # Process with groq
        llm = ChatGroq(
            api_key=GROQ_API_KEY,
            model_name=model_choice,
            temperature=CODE_TEMP,
        )
        
        # If no previous code context exists
        if len(st.session_state.code_messages) < 2:
            response = "Please paste your code and use the 'Analyze Code' button first to get started."
            source = DEFAULT_SOURCE_ATTRIBUTION
        else:
            # Get the code context and previous explanations
            code_context = next((m["content"] for m in st.session_state.code_messages if m.get("is_code", False)), "")
            previous_explanations = "\n\n".join([
                m["content"] for m in st.session_state.code_messages 
                if m["role"] == "assistant" and not m.get("is_code", False)
            ])
            
            template = """
            You are an expert programming teacher specializing in {language}.
            
            Previous code context:
            {code_context}
            
            Previous explanations:
            {previous_explanations}
            
            User question: {question}
            
            Provide a helpful, detailed response to the user's follow-up question about the code.
            Include code examples if relevant.
            """
            prompt = ChatPromptTemplate.from_template(template)
            chain = LLMChain(llm=llm, prompt=prompt)
            
            with st.spinner("Generating response..."):
                try:
                    result = chain.invoke({
                        "language": language,
                        "code_context": code_context,
                        "previous_explanations": previous_explanations,
                        "question": user_input
                    })
                    response = result["text"]
                    source = DEFAULT_SOURCE_ATTRIBUTION
                except Exception as e:
                    response = f"Error generating response: {str(e)}"
                    source = "Error occurred"
        
        # Add assistant response to chat history
        st.session_state.code_messages.append({"role": "assistant", "content": response, "source": source})
        
        # Display the response
        with st.chat_message("assistant"):
            st.markdown(response)
            st.markdown(f"<div class='source-citation'>{source}</div>", unsafe_allow_html=True)
