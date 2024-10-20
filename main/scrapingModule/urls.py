from django.urls import path
from .views import scrape_website

urlpatterns = [
    path('', scrape_website, name='scrape_website'),  
]