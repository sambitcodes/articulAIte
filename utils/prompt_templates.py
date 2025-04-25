"""
Collection of reusable prompt templates for various tasks
"""

# CV Analysis and Interview Prep templates
CV_ANALYSIS_TEMPLATE = """
You are an expert career advisor and technical interviewer. 

Analyze this CV/resume:
{cv_text}

Please provide:
1. A brief analysis of the candidate's profile (strengths/weaknesses)
2. 10 technical interview questions tailored to the candidate's background and projects
3. 5 behavioral interview questions based on their experience
4. Suggestions for skills to highlight during interviews
"""

JOB_MATCH_TEMPLATE = """
You are an expert career advisor and technical interviewer. 

Analyze this CV/resume:
{cv_text}

And consider this job description:
{job_description}

Please provide:
1. A brief analysis of the candidate's profile (strengths/weaknesses) in relation to the job description
2. 10 technical interview questions tailored to the candidate's skills and the job requirements
3. 5 behavioral interview questions relevant to the role
4. Suggestions for skills to highlight during the interview
"""

# Code Explanation templates
CODE_EXPLANATION_TEMPLATE = """
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

CODE_ERROR_FIXING_TEMPLATE = """
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

CODE_OPTIMIZATION_TEMPLATE = """
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

CODE_SOLUTION_TEMPLATE = """
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

# Article Generation templates
ARTICLE_TEMPLATE = """
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

# Study Plan templates
STUDY_PLAN_TEMPLATE = """
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
