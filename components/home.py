import streamlit as st
from PIL import Image
import base64
def home_page():


    # Apply custom CSS from your style.css file
    with open("assets/style.css") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    # Additional custom CSS for homepage
    st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
        padding: 0;
    }
    
    .header-container {
        background: linear-gradient(135deg, #1890ff 0%, #52c41a 100%);
        padding: 3rem 1rem;
        text-align: center;
        color: white;
        border-radius: 0 0 10px 10px;
        margin-bottom: 2rem;
    }
    
    .header-title {
        font-size: 3.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    
    .header-tagline {
        font-size: 1.5rem;
        font-weight: 300;
        margin-bottom: 1rem;
        opacity: 0.9;
    }
    
    .intro-section {
        background-color: white;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 2rem;
    }
    
    .feature-card {
        background-color: white;
        border-radius: 10px;
        padding: 1.5rem;
        height: 100%;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.15);
    }
    
    .feature-title {
        color: #1890ff;
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    .feature-desc {
        color: #555;
        font-size: 1rem;
    }
    
    .image-placeholder {
        background-color: #f0f2f5;
        height: 200px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 5px;
        margin-bottom: 1rem;
        color: #888;
    }
    
    .cta-section {
        background-color: #e6f7ff;
        padding: 1rem;
        border-radius: 5px;
        text-align: center;
        margin-top: 4rem;
        margin-bottom: 1rem;
        border-left: 2px solid #1890ff;
    }
    
    .footer {
        background-color: #333;
        color: white;
        padding: 1.5rem;
        text-align: center;
        border-radius: 10px;
        margin-top: 2rem;
    }
    
    .footer p {
        color: #aaa;
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }
    
    /* Fix Streamlit's default padding */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        max-width: 100%;
    }
    
    /* Custom button styling */
    .stButton>button {
        background: linear-gradient(135deg, #1890ff 0%, #52c41a 100%);
        color: white;
        border: none;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: opacity 0.3s;
    }
    
    .stButton>button:hover {
        opacity: 0.9;
        color: white;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

    # # Header section
    # st.markdown("""
    # <div class="header-container">
    #     <h1 class="header-title">articulAIte</h1>
    #     <p class="header-tagline">Your comprehensive AI-powered career development assistant</p>
    # </div>
    # """, unsafe_allow_html=True)

    # # def image_to_base64(img_path):
    # #     with open(img_path, "rb") as image_file:
    # #         encoded_string = base64.b64encode(image_file.read()).decode()
    # #     return encoded_string

    # Introduction section
    # st.markdown("""
    # <div class="intro-section">
    #     <h2 style="color: #1890ff; text-align: center; margin-bottom: 1rem;">Help yourself with AI-Driven Insights</h2>
    #     <p style="text-align: center; color: #555; font-size: 1.1rem;">
    #         articulAIte harnesses the power of LangChain and Groq to provide comprehensive career development assistance.
    #         From CV analysis and interview preparation to code explanation and content creation, our tools are designed to
    #         help you excel in today's competitive professional landscape.
    #     </p>
    # </div>
    # """, unsafe_allow_html=True)

    # Features section
    st.markdown("<h2 style='text-align: center; color: #333; margin-bottom: 1.5rem;'>Our Features</h2>", unsafe_allow_html=True)
    
    # Create 2x2 grid for features
    col1, col2 = st.columns(2)
    
    with col1:
        st.image(r"images/resume.png" ,use_container_width=True)
        st.markdown("""
        <div class="feature-card">
            <p class="feature-desc">
                Upload your resume for in-depth analysis and receive personalized interview questions on specific job descriptions.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        
        st.image(r"images/article.png", use_container_width=True)
        st.markdown("""
        <div class="feature-card">
            <p class="feature-desc">
                Create well-researched, professionally formatted articles on any topic with customizable length, style, and creativity levels.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.image(r"images/code.png", use_container_width=True)
        st.markdown("""
        <div class="feature-card">
            <p class="feature-desc">
                Get detailed explanations of code, identify and fix errors, and receive optimization suggestions for your programming projects.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        
        st.image(r"images/study.png", use_container_width=True)
        st.markdown("""
        <div class="feature-card">
            <p class="feature-desc">
                Develop personalized learning schedules with recommended resources and time estimates for any subject.
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Call to action section
    st.markdown("""
    <div class="cta-section">
        <h2 style="color: violet; margin-bottom: 1rem;">Use the sidebar to navigate between our specialized tools today.</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # col1, col2 = st.columns([0.43,0.57], vertical_alignment="center")
    # with col2:
    #     st.button("Get Started", on_click=cv_assistant)

    # Footer
    st.markdown("""
    <div class="footer">
        <p style="font-size: 0.9rem; color: #aaa; margin: 0;">
            A fun website by <a href="https://github.com/sambitcodes" target="_blank" style="color: #1890ff; text-decoration: none;">@sambitcodes</a> |
            <a href="mailto:sambitmaths123@gmail.com" style="color: #1890ff; text-decoration: none;">sambitmaths123@gmail.com</a> |
            <a href="tel:+917008014842" style="color: #1890ff; text-decoration: none;">+917008014842</a>
        </p>
    </div>
    """, unsafe_allow_html=True)
