from django.urls import path
from . import views
from .views import upload_resume, course_recommend

urlpatterns = [
    path('', upload_resume, name='resumeParser'),
    path('course-recommend/',course_recommend,name='course_recommend'),
]
