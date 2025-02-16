from django.urls import path
from . import views
from .views import upload_resume, course_recommend , chatbot , trending_courses, search_course, assessment
from .skill_assessment import get_questions, evaluate

urlpatterns = [
    path('', upload_resume, name='resumeParser'),
    path('course-recommend/',course_recommend,name='course_recommend'),
    path('trending-courses/',trending_courses,name='trending_courses'),
    path('search-course/',search_course,name='search_course'),
    path('chatbot/', chatbot, name='chatbot'),


    path("assessment/", assessment, name="assessment"),
    path("get_questions/",get_questions, name="get_questions"),
    path("evaluate/", evaluate, name="evaluate"),
]
