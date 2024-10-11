from django.urls import path
from . import views
from .views import upload_resume

urlpatterns = [
    path('', upload_resume, name='resumeParser'),
]
