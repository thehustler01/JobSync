import os
import speech_recognition as sr
import pyttsx3
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import google.generativeai as genai

# Set your API key here
os.environ["API_KEY"] = 'AIzaSyDyU3NhJ7MhfZT0fUWJH8S-xU8ZLqe9r9M'
genai.configure(api_key=os.environ["API_KEY"])

# Initialize text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Change index as needed
engine.setProperty('rate', 150)  # Set slower speed

def generate_interview_questions(skills, job_role):
    # Generate interview questions based on skills and job role.
    prompt = f"Generate a list of top asked interview questions for a {job_role} position focusing on the following skills: {', '.join(skills)}. Provide each question on a new line without any headings or extra formatting."
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    response = model.generate_content(prompt)
    questions = response.text.strip().split('\n')
    return [question.strip() for question in questions if question.strip()]

def analyze_answer(answer):
    # Analyze the user's answer and suggest improvements.
    prompt = f"Please analyze the following answer:\n\n{answer}\nProvide concise suggestions for improvement.answer which i am providing is recorded through mic so make sure you won't suggest any gramatical corrections in suggestion.Provide each suggestion on a new line without any headings,bullet points, asterisks for making bold or extra formatting.only add some line-spacing"
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    response = model.generate_content(prompt)
    return response.text.strip()

def generate_ideal_answer(question, answer):
    # Generate an ideal answer based on the user's answer and the corresponding question.
    prompt = f"Based on the following question: \n\n'{question}'\n provide an ideal answer for this question for interview. Make sure that answer should be in two paragraph without any headings or extra formatting, only give line-spacing between paragraph.Should be easy to understand & Don't give too long answer "
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    response = model.generate_content(prompt)
    return response.text.strip()

@csrf_exempt  # Allow CSRF exempt for testing purposes; consider securing this in production
def interview_view(request):
    if request.method == "POST":
        data = json.loads(request.body)  # Parse JSON data from request body
        skills = data.get('skills', [])
        job_role = data.get('job_role', '')
        questions = generate_interview_questions(skills, job_role)
        
        # Store questions in session or return them directly
        request.session['questions'] = questions
        request.session['current_question_index'] = 0
        
        return JsonResponse({'questions': questions})
    
    return render(request, 'interview.html')

@csrf_exempt  # Allow CSRF exempt for testing purposes; consider securing this in production
def get_next_question(request):
    if request.method == "GET":
        current_index = request.session.get('current_question_index', 0)
        questions = request.session.get('questions', [])
        
        if current_index < len(questions):
            question = questions[current_index]
            request.session['current_question_index'] += 1
            return JsonResponse({'question': question})
        else:
            return JsonResponse({'question': None})  # No more questions

@csrf_exempt  # Allow CSRF exempt for testing purposes; consider securing this in production
def analyze_answer_view(request):
    if request.method == "POST":
        data = json.loads(request.body)  # Parse JSON data from request body
        answer = data.get('answer', '')
        current_index = data.get('current_index', 0)
        
        questions = request.session.get('questions', [])
        
        if current_index < len(questions):
            question = questions[current_index]
            suggestions = analyze_answer(answer)
            ideal_answer = generate_ideal_answer(question, answer)

            return JsonResponse({
                'suggestions': suggestions,
                'ideal_answer': ideal_answer
            })
        else:
            return JsonResponse({'error': 'Invalid question index'}, status=400)