from django.urls import path
from .views import interview_view, get_next_question,analyze_answer_view

urlpatterns = [
    path('', interview_view, name='home'),  
    path('interview/', interview_view, name='interview'),
    path('next-question/', get_next_question, name='next_question'),  
    path('analyze-answer/', analyze_answer_view, name='analyze_answer'),  
]