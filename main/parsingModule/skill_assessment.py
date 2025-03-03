import json
import os
import google.generativeai as genai
from django.views.decorators.csrf import csrf_exempt
import re
from django.http import JsonResponse

genai.configure(api_key=os.getenv('GENAI_API_KEY'))

@csrf_exempt
def generate_mcqs(skill):
    """
    Generates MCQ questions for a given skill using Gemini API.
    """
    prompt = f"""
    Generate 10 multiple-choice questions (MCQs) on the skill: {skill}.
    Each question should have 4 options, one correct answer, and an explanation.
    Format:
    Q: <question>
    A) <option1>
    B) <option2>
    C) <option3>
    D) <option4>
    Correct Answer: <Correct Option letter>
    Explanation: <Why this is correct?>
    Don't add asterisk keep it exactly in the format I gave you
    """
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    clean_text = re.sub(r"\*", "", response.text)
    return clean_text

@csrf_exempt
def get_questions(request):
   
    skill = request.POST.get("skill")
    questions_text = generate_mcqs(skill)
    print(question_text)
    questions = []
    q_list = questions_text.strip().split("\n\n")  
   
    for raw_q in q_list:
        lines = raw_q.strip().split("\n")
        if len(lines) < 6:  # Ensure at least 5 lines (1 question + 4 options)
            continue  

        try:
            # Identify where options start (first line that starts with A), assuming options follow directly after question
            options_start = next((i for i, line in enumerate(lines) if line.lstrip().startswith(("A)", "B)", "C)", "D)"))), None)

            if options_start is None or options_start < 1:
                continue  # Skip if options are not found properly

            # Extract multi-line question (everything before options)
            question_text = " ".join(lines[:options_start]).replace("Q: ", "").strip()

            # Extract options safely
            options = []
            for i in range(options_start, options_start + 4):  # Expecting exactly 4 options
                if i < len(lines) and ") " in lines[i]:  
                    options.append(lines[i].split(") ", 1)[1].strip())  
                elif i < len(lines):
                    options.append(lines[i].strip())  # Handle missing delimiters
                else:
                    options.append(f"Option {chr(65 + (i - options_start))}")  # Placeholder for missing options

            
            correct_option_line = next((line for line in lines if "Correct Answer: " in line), None)
            correct_option_letter = ""
            if correct_option_line:
                match = re.search(r"Correct Answer:\s*([A-D])", correct_option_line)
                if match:
                    correct_option_letter = match.group(1)

            # Extract explanation (if available)
            explanation = ""
            explanation_line = next((line for line in lines if "Explanation: " in line), None)
            if explanation_line:
                explanation = explanation_line.replace("Explanation: ", "").strip()

            # Append structured question
            questions.append({
                "question": question_text,
                "options": options,
                "answer": correct_option_letter,  # Store as A, B, C, D
                "explanation": explanation
            })

        except Exception as e:
            print(f"Skipping malformed question due to error: {e}")

    return JsonResponse(questions, safe=False)

@csrf_exempt    
def evaluate(request):
    if request.method == "POST":
        user_answers = request.POST.get("answers", "{}")
        correct_answers = request.POST.get("correct_answers", "{}")
        explanations = request.POST.get("explanations", "{}")
        if isinstance(user_answers, str):
            user_answers = json.loads(user_answers)
        if isinstance(correct_answers, str):
            correct_answers = json.loads(correct_answers)
        if isinstance(explanations, str):
            explanations = json.loads(explanations)
        print(user_answers)
        print(correct_answers)
        print(type(user_answers))
        result=[]
        score = sum(1 for q, a in user_answers.items() if a == correct_answers[q])
        for q, a in user_answers.items():
            if a == correct_answers[q]:
                result.append(f"✅ Correct")
            else:
                result.append(f"❌ Wrong")
        total = len(correct_answers)
        return JsonResponse({"score": score, "total": total, "result":result, "explanations": explanations,"correct_answers":correct_answers })
