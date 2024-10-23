from django.urls import path
from .views import scrape_website ,job_search_without_skill

urlpatterns = [
    path('', scrape_website, name='scrape_website'),  
    path('jobs/',job_search_without_skill,name='job_search_without_skill'),
]