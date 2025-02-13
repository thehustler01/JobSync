from django.urls import path
from . import views
from .views import upload_resume, course_recommend , chatbot , trending_courses,tempF, search_course

urlpatterns = [
    path('', upload_resume, name='resumeParser'),
    path('course-recommend/',course_recommend,name='course_recommend'),
    path('trending-courses/',trending_courses,name='trending_courses'),
    path('search-course/',search_course,name='search_course'),
    path('chatbot/', chatbot, name='chatbot'),
    path('temp/', tempF, name='tempF'),
]
