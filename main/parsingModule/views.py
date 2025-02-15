from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, FileResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
import PyPDF2
from PyPDF2 import PdfReader, PdfFileWriter, PdfFileMerger
import re
import spacy
import docx2txt
from spacy.matcher import Matcher
import pandas as pd
import os
from nltk.corpus import stopwords
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .job_matching import recommend_job
from .course_recommendation import recommendCourse, trendingCourses, searchCourse
from .chatbot import  get_chatbot_response
from django.core.mail import send_mail

import json

skillset=[]
miss_skill=[]
dic={}
@csrf_exempt
def upload_resume(request):
    if request.method == 'POST' and request.FILES['resume']:
        resume = request.FILES['resume']
        
        fs = FileSystemStorage()
        filename = fs.save(resume.name, resume)
        file_url = fs.url(filename)
        file_path = fs.path(filename)

        if file_path.endswith('.docx'):
            Res_text = doc2text(file_path )
    
        elif file_path.endswith('.pdf'):
            Res_text = pdf2text(file_path)
        else:
            print("File not support")


        nlp = spacy.load('en_core_web_sm')
        selfMatcher = Matcher(nlp.vocab)
        text=' '.join(Res_text.split())

        newNlp = nlp(text)
        noun_chunks = list(newNlp.noun_chunks)
       
        # name=extract_name(newNlp,matcher=selfMatcher)
        skillset=extract_skills(newNlp, noun_chunks)
        email=extract_email(text)
        phone=extract_mobile_number(text)
        global miss_skill
        jobRole,miss_skill = recommend_job(skillset,email,phone,filename,resume,Res_text)
       
        # print(skillset)
        print(".........................")
        print(email)
        print(".........................")
        print(phone)
        print("..........................")

        print(miss_skill)
        print(jobRole)
       
        return JsonResponse({
            'success': True,
            'pdf_url': file_url,
            'missing_skills' : miss_skill,
            'suggested_job_role' : jobRole,
            'extracted_text':Res_text,
            'skillset':skillset
        })
    
        # return JsonResponse({'success': False, 'error': 'No file uploaded'})
    return render(request, 'resumeParser.html')

def pdf2text(file_path):
    
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def doc2text(file_path):
    temp = docx2txt.process(file_path)
    resume_text = [line.replace('\t', ' ') for line in temp.split('\n') if line]
    text = ' '.join(resume_text)
    return (text)

def extract_skills(nlp_text, noun_chunks):
    
    tokens = [token.text for token in nlp_text if not token.is_stop]
    # print(tokens)
    skills_file_path = os.path.join(settings.MEDIA_ROOT, 'Generated_Skills_Final.csv')
    data = pd.read_csv(skills_file_path) 
    skills =  data.values.flatten().tolist()
    skillset = []

    # check for one-grams
    for token in tokens:
        if token.lower() in skills:
            skillset.append(token)
    
    # check for bi-grams and tri-grams
    for token in noun_chunks:
        token = token.text.lower().strip()
        if token in skills:
            skillset.append(token)
    return [i.capitalize() for i in set([i.lower() for i in skillset])]
    # returns list of extracted skills 



def extract_email(text):
    
    regex= re.compile(r'[a-zA-Z0-9_.±]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', re.IGNORECASE)
    email = re.findall(regex,text)
    if email:
        try:
            return email[0].split()[0].strip(';')
        except IndexError:
            return None

def extract_name(nlp_text, matcher):
    NAME_PATTERN      = [{'POS': 'PROPN'}, {'POS': 'PROPN'}]
    pattern = [NAME_PATTERN]
    
    matcher.add('NAME',None,*pattern)
    
    matches = matcher(nlp_text)
    
    for match_id, start, end in matches:
        span = nlp_text[start:end]
        if 'name' not in span.text.lower():
            return span.text

def extract_mobile_number(text):
    
    phone = re.findall(r'(?:\+?\d{1,3})?[-.\s]?[789]\d{9}', text)
    if phone:
        number = ''.join(phone[0])
        if len(number) > 10:
            return '+' + number
        else:
            return number


def course_recommend(request):
    print("passsedd value")
    global miss_skill
    global dic
    print(miss_skill)
    courses,dic=recommendCourse(miss_skill)
    print(dic)
    send_skill_reminder()
    return render(request,'course.html',{'course_data':courses , 'course_heading':"Customized Courses to Strengthen Your Weak Spots"})
def trending_courses(request):
    courses=trendingCourses()
    return render(request,'course.html',{'course_data':courses, 'course_heading':"Top Trending Courses to Elevate Your Career"})

def search_course(request):
    course_title = request.GET.get('course_title', '')
    courses=searchCourse(course_title)
    return render(request,'course.html',{'course_data':courses, 'course_heading':"Searched Course"})


@csrf_exempt
def chatbot(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_message = data.get("message", "")

            # Get previous chat history from session
            chat_history = request.session.get("chat_history", [])
            bot_reply = get_chatbot_response(user_message,chat_history)

            # Update chat history and store in session
            chat_history.append(f"User: {user_message}")
            chat_history.append(f"Bot: {bot_reply}")
            request.session["chat_history"] = chat_history

            return JsonResponse({"reply": bot_reply})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return render(request, 'chat.html')


def send_skill_reminder():
    email="rishabhvaish2002@gmail.com" #Replace with user email
    subject = "Skill Improvement Recommendation"

    skills_str = "\n".join([f"- {skill}" for skill, url in dic.items()])
    skills_course_str = "\n".join([f"- {skill} - {url}" for skill, url in dic.items()])
    message = f"""
    Hello,

    We noticed that you're missing the following skills for better job matches: 
    {skills_str}

    To boost your profile, we recommend these courses:

    {skills_course_str}

    🔗 Click the links above to start learning today!

    Keep learning and growing!
    🚀 Your dream job is just a step away! Use **JobSync** to match with the best opportunities, prepare for the jobs and stay ahead in your career.  
    Let JobSync be your **Ultimate Career Assistant** - helping you **Grow, Learn, and Succeed**! 
    
    Best Regards,
    Team JobSync
    """

    send_mail(subject, message, settings.EMAIL_HOST_USER, [email])
    return