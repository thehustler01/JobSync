from django.urls import path
from .views import scrape_website ,job_search_without_skill,hiring_process_insights,career_roadmap

urlpatterns = [
    path('', scrape_website, name='scrape_website'),  
    path('jobs/',job_search_without_skill,name='job_search_without_skill'),
    path('hiring_insights/',hiring_process_insights,name='hiring_process_insights'),
    path('career_roadmap/',career_roadmap,name='career_roadmap'),
]
