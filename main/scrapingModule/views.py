import os
import pickle
import logging
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from django.shortcuts import render  
from .models import JobListing  
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def scrape_website(request):
    job_title = request.GET.get('job_title', 'web_developer') 
    location = request.GET.get('location', 'bangalore') 

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920x1080")

    service = Service('./drivers/chromedriver.exe')
    
    try:
        # driver = webdriver.Chrome(service=service, options=chrome_options)
        driver = webdriver.Chrome(service=service)
        
        # Load cookies if they exist
        if os.path.exists("linkedin_cookies.pkl"):
            with open("linkedin_cookies.pkl", "rb") as cookiesfile:
                cookies = pickle.load(cookiesfile)
                driver.get("https://www.linkedin.com")
                for cookie in cookies:
                    driver.add_cookie(cookie)
                driver.refresh()  # Refresh to apply cookies

        # Check if still logged in by looking for a specific element on the homepage
        driver.get("https://www.linkedin.com")
        time.sleep(5)  # Allow time for page to load

        if "login" in driver.current_url:
            perform_login(driver)

        # Scrape job listings after ensuring logged in
        url = f"https://www.linkedin.com/jobs/search/?geoId=102713980&keywords={job_title}&origin=JOB_SEARCH_PAGE_SEARCH_BUTTON&refresh=true"
        driver.get(url)
        
        time.sleep(5)  # Allow time for job listings to load

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        for job_card in soup.find_all('div', class_='base-card'):
            try:
                title = (job_card.find('h3').text.strip() if job_card.find('h3') else None)[:1000] 
                company = (job_card.find('h4').text.strip() if job_card.find('h4') else None)[:500]  
                job_link = (job_card.find('a')['href'] if job_card.find('a') else None)[:1000]
                location_element = job_card.find('span', class_='job-search-card__location')
                location = location_element.text.strip()[:500] if location_element else "Location not specified"
                description = (job_card.find('p', class_='job-search-card__description').text.strip() if job_card.find('p', class_='job-search-card__description') else None)
                salary_element = job_card.find('span', class_='salary-text')
                salary = (salary_element.text.strip() if salary_element else "Not specified")[:500]  

                # Check for asterisks in the fields
                if any(field and field.count('*') > 1 for field in [title, company, location, description, salary]):
                    continue  # Skip saving this job if any field contains more than one asterisk

                # Save the job listing only if it does not already exist in the database
                if not JobListing.objects.filter(job_link=job_link).exists():
                    JobListing.objects.create(
                        title=title,
                        company=company,
                        job_link=job_link,
                        location=location,
                        description=description,
                        salary=salary,
                        scraped_for=job_title,
                        scraped_at=datetime.now()
                    )
            except Exception as e:
                logging.error(f"Error processing job card: {e}")
        
    except Exception as e:
        logging.error(f"An error occurred during scraping: {e}")
        return render(request, 'error.html', {'message': 'An error occurred while scraping the website. Please try again later.'})
    
    finally:
        driver.quit()

    # Retrieve and sort jobs based on scraped_at field (latest first)
    jobs = JobListing.objects.filter(scraped_for=job_title).order_by('-scraped_at')

    return render(request, 'jobList.html', {'jobs': jobs})

def perform_login(driver):
    """Handles the login process."""
    try:
        driver.get("https://www.linkedin.com/login")
        
        email = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'username')))
        email.send_keys("abhaykesarwani010@gmail.com")  # Replace with your secondary email
        
        password = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'password')))
        password.send_keys("abhay123")  # Replace with your secondary password
        
        login_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
        login_button.click()
        
        time.sleep(5)  # Allow time for the page to load after logging in
        
        with open("linkedin_cookies.pkl", "wb") as cookiesfile:
            pickle.dump(driver.get_cookies(), cookiesfile)

    except Exception as e:
        logging.error(f"Login failed: {e}")
    
def check_login_popup(driver):
    """Check for the presence of a login popup."""
    try:
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, 'username')))
        return True  # Login popup is visible
    except Exception as e:
        logging.warning(f"Login popup check failed: {e}")
        return False  # No login popup

def job_search_without_skill(request):
    return render(request,'jobs.html')