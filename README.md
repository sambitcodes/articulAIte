# AI Career Assistant

A comprehensive Streamlit-based web application that uses LangChain and Groq to provide career development assistance.

## Features

### 1. CV Analysis & Interview Preparation
- Upload your CV/resume for analysis
- Get personalized interview questions based on your experience
- Receive suggestions on skills to highlight during interviews
- Add job descriptions for targeted advice

### 2. Code Explainer & Problem Solver
- Get line-by-line explanations of your code
- Identify and fix errors in your code
- Receive optimization suggestions
- Get solutions to coding problems

### 3. Article Generator
- Create well-researched articles on any topic
- Control word count and creativity level
- Choose from various writing styles
- Get properly formatted content ready for publishing

### 4. Study Plan Generator
- Create personalized study plans for any subject
- Get week-by-week learning schedules
- Find recommended resources and materials
- Receive time estimates and progress tracking metrics

- App Link - https://articulaite.onrender.com/

## Setup Instructions

1. Clone this repository
2. Install requirements:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your API keys:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```
4. Run the application:
   ```
   streamlit run app.py
   ```

## Requirements

- Python 3.8+
- Streamlit
- LangChain
- Groq API access

## Project Structure

```
career_assistant/
├── app.py                  # Main Streamlit application
├── requirements.txt        # Dependencies
├── config.py               # Configuration and API keys
├── README.md               # Project documentation
├── components/
│   ├── __init__.py
│   ├── cv_analyzer.py      # CV analysis and interview prep
│   ├── code_explainer.py   # Code explanation functionality
│   ├── article_generator.py # Article creation with temp control
│   └── study_planner.py    # Study plan generator
├── utils/
│   ├── __init__.py
│   ├── groq_helpers.py     # Groq API wrappers
│   ├── langchain_agents.py # Custom LangChain agents
│   └── prompt_templates.py # Reusable prompt templates
└── assets/
    └── style.css           # Custom styling
```

## Usage

1. Navigate to the desired feature using the sidebar
2. Follow the instructions for each specific tool
3. Maintain a conversational flow with the AI assistant
4. Download or copy the generated content as needed

## Notes

- The application uses Groq's language models via the LangChain integration
- Each feature maintains its own conversation history
- Source citations are displayed with each AI response
