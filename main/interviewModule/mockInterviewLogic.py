import os
import google.generativeai as genai

# Set your API key here
os.environ["API_KEY"] = 'AIzaSyDyU3NhJ7MhfZT0fUWJH8S-xU8ZLqe9r9M'
genai.configure(api_key=os.environ["API_KEY"])

def generate_interview_questions(skills, job_role):
    prompt = f"Generate a list of top asked interview questions for a {job_role} position focusing on the following skills: {', '.join(skills)}."
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    response = model.generate_content(prompt)
    
    # Clean up the response to ensure it only contains questions
    questions = response.text.strip().split('\n')
    return [question.strip() for question in questions if question.strip()]

def analyze_answer(answer):
    prompt = (
        f"Please analyze the following answer:\n\n{answer}\n"
        "given answer is recorded through mic, ignore the gramatical mistakes while giving suggestion."
        "Provide concise suggestions for improvement in an ordered list, followed by an ideal answer in another ordered list."
    )
    
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    response = model.generate_content(prompt)
    
    # Clean and format the response
    lines = response.text.strip().split('\n')
    
    suggestions = []
    ideal_answer = []
    
    # Separate suggestions and ideal answer based on expected format
    for line in lines:
        if line.strip().startswith("1.") or line.strip().startswith("2.") or line.strip().startswith("3."):
            if 'Ideal Answer:' not in line:  # Exclude the ideal answer heading
                suggestions.append(line)
            else:
                ideal_answer.append(line)

    # Format suggestions and ideal answer into paragraphs
    formatted_suggestions = ""
    formatted_ideal_answer = ""

    if suggestions:
        formatted_suggestions = "Suggestions for Improvement:\n" + "\n".join(suggestions)
    
    if ideal_answer:
        formatted_ideal_answer = "\nIdeal Answer:\n" + "\n".join(ideal_answer)

    # Combine results, ensuring no empty sections are returned
    result = []
    if formatted_suggestions:
        result.append(formatted_suggestions)
    if formatted_ideal_answer:
        result.append(formatted_ideal_answer)

    return "\n\n".join(result) if result else "No suggestions or ideal answers provided."