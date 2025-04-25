import streamlit as st
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from config import GROQ_API_KEY, STUDY_MODEL, STUDY_TEMP, DEFAULT_SOURCE_ATTRIBUTION

def generate_study_plan(subject, duration_weeks, experience_level, goals):
    """Generate a study plan using Groq"""
    try:
        llm = ChatGroq(
            api_key=GROQ_API_KEY,
            model_name=STUDY_MODEL,
            temperature=STUDY_TEMP,
        )
        
        template = """
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
        """
        
        prompt = ChatPromptTemplate.from_template(template)
        chain = LLMChain(llm=llm, prompt=prompt)
        response = chain.invoke({
            "subject": subject,
            "duration_weeks": duration_weeks,
            "experience_level": experience_level,
            "goals": goals
        })
        
        return response["text"], DEFAULT_SOURCE_ATTRIBUTION
    except Exception as e:
        return f"Error in generating study plan: {str(e)}", DEFAULT_SOURCE_ATTRIBUTION

def display_chat_messages():
    """Display chat history"""
    for message in st.session_state.study_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "source" in message and message["role"] == "assistant":
                st.markdown(f"<div class='source-citation'>{message['source']}</div>", unsafe_allow_html=True)

def study_assistant():
    """Main study plan generation assistant"""
    with st.expander("About", expanded=False):
        st.header("Study Plan Generator")
        st.markdown("""
        Create personalized study plans for any subject:
        - Week-by-week learning schedules
        - Recommended resources and materials
        - Time estimates and progress tracking
        - Customized for your experience level and goals
        """)
    
    # Subject input
    subject = st.text_input("Enter subject or skill to learn", help="Be specific for a more targeted plan")
    
    # Duration selection
    duration_weeks = st.slider(
        "Study plan duration (weeks)",
        min_value=1,
        max_value=24,
        value=8,
        step=1
    )
    
    # Experience level selection
    experience_level = st.radio(
        "Your experience level with this subject",
        ["Beginner", "Intermediate", "Advanced"]
    )
    
    # Learning goals
    goals = st.text_area(
        "What are your learning goals or objectives?",
        height=100,
        help="What do you want to achieve by the end of this study plan?"
    )
    
    # Display chat history
    display_chat_messages()
    
    # Generate study plan button
    if subject and goals and st.button("Generate Study Plan"):
        prompt_text = f"Create a {duration_weeks}-week study plan for {subject} at {experience_level} level with these goals: {goals}"
        
        # Add user message to chat history
        st.session_state.study_messages.append({"role": "user", "content": prompt_text})
        
        # Display the message
        with st.chat_message("user"):
            st.markdown(prompt_text)
        
        # Process with groq
        with st.spinner(f"Generating {duration_weeks}-week study plan for {subject}..."):
            response, source = generate_study_plan(subject, duration_weeks, experience_level, goals)
        
        # Add assistant response to chat history
        st.session_state.study_messages.append({"role": "assistant", "content": response, "source": source})
        
        # Display the response
        with st.chat_message("assistant"):
            st.markdown(response)
            st.markdown(f"<div class='source-citation'>{source}</div>", unsafe_allow_html=True)
    
    # Chat input for follow-up questions
    if user_input := st.chat_input("Ask questions or request modifications to your study plan..."):
        # Add user message to chat history
        st.session_state.study_messages.append({"role": "user", "content": user_input})
        
        # Display the new message
        with st.chat_message("user"):
            st.markdown(user_input)
        
        # If no previous study plan exists
        if not any(m["role"] == "assistant" for m in st.session_state.study_messages):
            response = "Please generate a study plan first using the form above."
            source = DEFAULT_SOURCE_ATTRIBUTION
        else:
            # Get the last generated study plan
            last_plan = next((m["content"] for m in reversed(st.session_state.study_messages) 
                            if m["role"] == "assistant"), "")
            
            # Process with groq
            llm = ChatGroq(
                api_key=GROQ_API_KEY,
                model_name=STUDY_MODEL,
                temperature=STUDY_TEMP,
            )
            
            template = """
            You are an educational expert specializing in curriculum development.
            
            Original study plan for {subject} ({duration_weeks} weeks, {experience_level} level):
            {plan}
            
            User request: {request}
            
            Please respond to the user's request or question. If they are asking for modifications
            to the study plan, provide a complete revised version that incorporates their feedback.
            If they are asking a question, provide a helpful and detailed answer.
            
            Use proper Markdown formatting in your response.
            """
            
            prompt = ChatPromptTemplate.from_template(template)
            chain = LLMChain(llm=llm, prompt=prompt)
            
            with st.spinner("Processing your request..."):
                try:
                    result = chain.invoke({
                        "subject": subject if subject else "the subject",
                        "duration_weeks": duration_weeks,
                        "experience_level": experience_level,
                        "plan": last_plan,
                        "request": user_input
                    })
                    response = result["text"]
                    source = DEFAULT_SOURCE_ATTRIBUTION
                except Exception as e:
                    response = f"Error generating response: {str(e)}"
                    source = "Error occurred"
        
        # Add assistant response to chat history
        st.session_state.study_messages.append({"role": "assistant", "content": response, "source": source})
        
        # Display the response
        with st.chat_message("assistant"):
            st.markdown(response)
            st.markdown(f"<div class='source-citation'>{source}</div>", unsafe_allow_html=True)
