from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from django.http import JsonResponse
import time
from django.shortcuts import render


def scrape_website(request):
    job_title = request.GET.get('job_title', 'web_developer') 
    location = request.GET.get('location', 'bangalore') 


    chrome_options = Options()
    chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--no-sandbox")  
    chrome_options.add_argument("--disable-dev-shm-usage") 

    service = Service('./drivers/chromedriver.exe')
    driver = webdriver.Chrome(service=service)
    # driver = webdriver.Chrome(executable_path='./chromedriver.exe')
    url = f"https://www.linkedin.com/jobs/search/?keywords={job_title}&location={location}"
    driver.get(url)
    
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    jobs = []
    
    for job_card in soup.find_all('div', class_='base-card'):
        title = job_card.find('h3').text.strip() if job_card.find('h3') else None
        company = job_card.find('h4').text.strip() if job_card.find('h4') else None
        job_link = job_card.find('a')['href'] if job_card.find('a') else None
        location = job_card.find('span', class_='job-search-card__location').text.strip() if job_card.find('span', class_='job-search-card__location') else None
        description = job_card.find('p', class_='job-search-card__description').text.strip() if job_card.find('p', class_='job-search-card__description') else None

        salary = job_card.find('span', class_='salary-text')  
        salary = salary.text.strip() if salary else "Not specified"

        jobs.append({
            'title': title,
            'company': company,
            'job_link': job_link,
            'location': location,
            'description': description,
            'salary': salary  
        })

    driver.quit()
    print(jobs)
    # return JsonResponse({'jobs': jobs})
    return render(request, 'jobList.html', {'jobs': jobs})
