import streamlit as st
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from config import GROQ_API_KEY, ARTICLE_MODEL, ARTICLE_DEFAULT_TEMP, DEFAULT_SOURCE_ATTRIBUTION

def generate_article(topic, word_count, temperature, style):
    """Generate an article using Groq"""
    try:
        llm = ChatGroq(
            api_key=GROQ_API_KEY,
            model_name=ARTICLE_MODEL,
            temperature=temperature,
        )
        
        template = """
        You are an expert content creator specializing in educational articles.
        
        Please write a comprehensive article about: {topic}
        
        Requirements:
        - Word Count: Approximately {word_count} words
        - Style: {style}
        - Format the article with proper Markdown formatting (headers, bullet points, etc.)
        - Include relevant subtopics and key concepts
        - The article should be well-structured with an introduction, body, and conclusion
        - Include practical examples or case studies where appropriate
        
        Note: Temperature setting is {temperature} (0 = more factual/conservative, 1 = more creative/innovative)
        
        Write the article now:
        """
        
        prompt = ChatPromptTemplate.from_template(template)
        chain = LLMChain(llm=llm, prompt=prompt)
        response = chain.invoke({
            "topic": topic,
            "word_count": word_count,
            "temperature": temperature,
            "style": style
        })
        
        return response["text"], DEFAULT_SOURCE_ATTRIBUTION
    except Exception as e:
        return f"Error in generating article: {str(e)}", DEFAULT_SOURCE_ATTRIBUTION

def display_chat_messages():
    """Display chat history"""
    for message in st.session_state.article_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "source" in message and message["role"] == "assistant":
                st.markdown(f"<div class='source-citation'>{message['source']}</div>", unsafe_allow_html=True)

def article_assistant():
    """Main article generation assistant"""
    with st.expander("About", expanded=False):
        st.header("Article Generator")
        st.markdown("""
        Generate well-researched articles on any topic:
        - Control word count and creativity level
        - Choose different writing styles
        - Get properly formatted content ready for publishing
        """)
    
    # Topic input
    topic = st.text_input("Enter article topic", help="Be specific for better results")
    
    # Word count selection
    word_count = st.select_slider(
        "Select approximate word count",
        options=[250, 500, 750, 1000, 1500, 2000, 3000],
        value=1000
    )
    
    # Writing style selection
    style = st.selectbox(
        "Select writing style",
        [
            "Academic", 
            "Conversational", 
            "Professional", 
            "Technical", 
            "Educational",
            "Journalistic",
            "Narrative"
        ],
        index=1
    )
    
    # Temperature slider
    temperature = st.slider(
        "Creativity level (temperature)",
        min_value=0.1,
        max_value=1.0,
        value=ARTICLE_DEFAULT_TEMP,
        step=0.1,
        help="Lower values produce more factual content, higher values more creative content"
    )
    
    # Temperature explanation
    st.caption(
        "Temperature guide: 0.1-0.3 (highly factual), 0.4-0.6 (balanced), 0.7-1.0 (more creative)"
    )
    
    # Display chat history
    display_chat_messages()
    
    # Generate article button
    if topic and st.button("Generate Article"):
        prompt_text = f"Generate a {word_count}-word {style.lower()} article about {topic} with temperature {temperature}"
        
        # Add user message to chat history
        st.session_state.article_messages.append({"role": "user", "content": prompt_text})
        
        # Display the message
        with st.chat_message("user"):
            st.markdown(prompt_text)
        
        # Process with groq
        with st.spinner(f"Generating a {word_count}-word article about {topic}..."):
            response, source = generate_article(topic, word_count, temperature, style)
        
        # Add assistant response to chat history
        st.session_state.article_messages.append({"role": "assistant", "content": response, "source": source})
        
        # Display the response
        with st.chat_message("assistant"):
            st.markdown(response)
            st.markdown(f"<div class='source-citation'>{source}</div>", unsafe_allow_html=True)
    
    # Chat input for article refinement
    if user_input := st.chat_input("Request refinements or ask questions about the article..."):
        # Add user message to chat history
        st.session_state.article_messages.append({"role": "user", "content": user_input})
        
        # Display the new message
        with st.chat_message("user"):
            st.markdown(user_input)
        
        # If no previous article exists
        if not any(m["role"] == "assistant" for m in st.session_state.article_messages):
            response = "Please generate an article first using the form above."
            source = DEFAULT_SOURCE_ATTRIBUTION
        else:
            # Get the last generated article and topic
            last_article = next((m["content"] for m in reversed(st.session_state.article_messages) 
                               if m["role"] == "assistant"), "")
            
            last_topic = topic if topic else "the previously discussed topic"
            
            # Process with groq
            llm = ChatGroq(
                api_key=GROQ_API_KEY,
                model_name=ARTICLE_MODEL,
                temperature=temperature,
            )
            
            template = """
            You are an expert content creator specializing in educational articles.
            
            Original article about {topic}:
            {article}
            
            User feedback/request: {request}
            
            Please respond to the user's feedback or request. If they are asking for revisions,
            provide a complete revised version of the article that incorporates their feedback.
            If they are asking a question, provide a helpful and detailed answer.
            
            Use proper Markdown formatting in your response.
            """
            
            prompt = ChatPromptTemplate.from_template(template)
            chain = LLMChain(llm=llm, prompt=prompt)
            
            with st.spinner("Processing your request..."):
                try:
                    result = chain.invoke({
                        "topic": last_topic,
                        "article": last_article,
                        "request": user_input
                    })
                    response = result["text"]
                    source = DEFAULT_SOURCE_ATTRIBUTION
                except Exception as e:
                    response = f"Error generating response: {str(e)}"
                    source = "Error occurred"

        st.session_state.article_messages.append({"role": "assistant", "content": response, "source": source})
        
        # Display the response
        with st.chat_message("assistant"):
            st.markdown(response)
            st.markdown(f"<div class='source-citation'>{source}</div>", unsafe_allow_html=True)