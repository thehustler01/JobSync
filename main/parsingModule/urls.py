from django.urls import path
from . import views
from .views import upload_resume, course_recommend , chatbot

urlpatterns = [
    path('', upload_resume, name='resumeParser'),
    path('course-recommend/',course_recommend,name='course_recommend'),
    path('chatbot/', chatbot, name='chatbot'),
]
