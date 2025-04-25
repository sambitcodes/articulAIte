import streamlit as st
import tempfile
import os
import PyPDF2
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from config import GROQ_API_KEY, DEFAULT_MODEL, DEFAULT_TEMP, DEFAULT_SOURCE_ATTRIBUTION


def extract_text_from_pdf(pdf_file):
    """Extract text from uploaded PDF file"""
    text = ""
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(pdf_file.read())
        temp_file_path = temp_file.name

    try:
        reader = PyPDF2.PdfReader(temp_file_path)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    finally:
        os.unlink(temp_file_path)  # Clean up temp file
    
    return text

def get_cv_analysis(cv_text,model, job_description=None):
    """Analyze CV and generate interview questions using Groq"""
    try:
        llm = ChatGroq(
            api_key=GROQ_API_KEY,
            model_name=model,
            temperature=DEFAULT_TEMP,
        )
        
        # Prepare the prompt template
        if job_description:
            template = """
            You are an expert career advisor and technical interviewer. 
            
            First, analyze this CV/resume:
            {cv_text}
            
            And consider this job description:
            {job_description}
            
            Please provide:
            1. A brief analysis of the candidate's profile (strengths/weaknesses) in relation to the job description
            2. 10 technical interview questions tailored to the candidate's skills and the job requirements
            3. 5 behavioral interview questions relevant to the role
            4. Suggestions for skills to highlight during the interview
            """
            prompt = ChatPromptTemplate.from_template(template)
            chain = LLMChain(llm=llm, prompt=prompt)
            response = chain.invoke({"cv_text": cv_text, "job_description": job_description})
        else:
            template = """
            You are an expert career advisor and technical interviewer. 
            
            Analyze this CV/resume:
            {cv_text}
            
            Please provide:
            1. A brief analysis of the candidate's profile (strengths/weaknesses)
            2. 10 technical interview questions tailored to the candidate's background and projects
            3. 5 behavioral interview questions based on their experience
            4. Suggestions for skills to highlight during interviews
            """
            prompt = ChatPromptTemplate.from_template(template)
            chain = LLMChain(llm=llm, prompt=prompt)
            response = chain.invoke({"cv_text": cv_text})
        
        return response["text"], DEFAULT_SOURCE_ATTRIBUTION
    except Exception as e:
        return f"Error in analyzing CV: {str(e)}", DEFAULT_SOURCE_ATTRIBUTION

def display_chat_messages():
    """Display chat history"""
    for message in st.session_state.cv_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "source" in message and message["role"] == "assistant":
                st.markdown(f"<div class='source-citation'>{message['source']}</div>", unsafe_allow_html=True)

def cv_assistant():
    """Main CV analyzer and interview preparation assistant"""
    with st.expander("About", expanded=False):
        st.header("CV Analysis & Interview Preparation 📑📝💼📞")
        st.markdown("""
        Upload your CV/resume and optionally a job description to get:
        - :red[Profile analysis]
        - :red[Tailored interview questions]
        - :red[Skills highlighting recommendations]
        """)
    
    left_col, right_col = st.columns([1,2])
        
    # File uploader for CV
    with left_col:
        cv_file = st.file_uploader("Upload your CV/resume (PDF format)", type=["pdf"])
    
    # Text area for job description
    with right_col:
        job_description = st.text_area("Enter job description (optional)", height=150)
        model_choice = st.selectbox("Select model for analysis",
            options=["llama3-70b-8192","llama-3.3-70b-versatile", "gemma2-9b-it","deepseek-r1-distill-llama-70b"],
            index=0)
    
    # Initialize CV text
    cv_text = None
    
    # Process CV if uploaded
    if cv_file:
        with st.spinner("Extracting text from CV..."):
            cv_text = extract_text_from_pdf(cv_file)
            st.success("CV processed successfully!")
            
            # Show extracted text in expander for verification
            with st.expander("View extracted CV text"):
                st.text(cv_text)
    
    # Display chat history
    display_chat_messages()
    
    # Input field for user questions
    if user_input := st.chat_input("Ask follow-up questions about your interview preparation..."):
        # Add user message to chat history
        st.session_state.cv_messages.append({"role": "user", "content": user_input})
        
        # Display the new message
        with st.chat_message("user"):
            st.markdown(user_input)
        
        # If user hasn't uploaded CV yet
        if not cv_text:
            response = "Please upload your CV/resume first to get interview preparation assistance."
            source = DEFAULT_SOURCE_ATTRIBUTION
        else:
            # Combine previous context with new question
            context = "\n\n".join([m["content"] for m in st.session_state.cv_messages if m["role"] == "assistant"])
            
            # Process with groq
            llm = ChatGroq(
                api_key=GROQ_API_KEY,
                model_name=model_choice,
                temperature=DEFAULT_TEMP,
            )
            
            template = """
            You are an expert career advisor and technical interviewer.
            
            Context from CV: {cv_text}
            
            Job description (if provided): {job_description}
            
            Previous conversation:
            {context}
            
            User question: {question}
            
            Provide a helpful, detailed response to the user's question.
            """
            prompt = ChatPromptTemplate.from_template(template)
            chain = LLMChain(llm=llm, prompt=prompt)
            
            with st.spinner("Generating response..."):
                try:
                    result = chain.invoke({
                        "cv_text": cv_text, 
                        "job_description": job_description if job_description else "Not provided",
                        "context": context,
                        "question": user_input
                    })
                    response = result["text"]
                    source = DEFAULT_SOURCE_ATTRIBUTION
                except Exception as e:
                    response = f"Error generating response: {str(e)}"
                    source = "Error occurred"
        
        # Add assistant response to chat history
        st.session_state.cv_messages.append({"role": "assistant", "content": response, "source": source})
        
        # Display the response
        with st.chat_message("assistant"):
            st.markdown(response)
            st.markdown(f"<div class='source-citation'>{source}</div>", unsafe_allow_html=True)
    
    # Initial CV analysis button
    if cv_text and st.button("Generate Interview Preparation"):
        # Clear previous chat history if starting new analysis
        st.session_state.cv_messages = []
        
        with st.spinner("Analyzing CV and generating interview questions..."):
            response, source = get_cv_analysis(cv_text,model_choice, job_description)
        
        # Add system prompt and response to chat history
        st.session_state.cv_messages.append({
            "role": "user", 
            "content": "Please analyze my CV and provide interview preparation assistance."
        })
        
        st.session_state.cv_messages.append({
            "role": "assistant", 
            "content": response,
            "source": source
        })
        
        # Rerun to display messages
        st.rerun()
