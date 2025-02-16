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
from django.shortcuts import render
import google.generativeai as genai
import re
from django.conf import settings
 
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
        email.send_keys(settings.Linked_in_email)  # Replace with your secondary email
        
        password = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'password')))
        password.send_keys(settings.Linked_in_pswd)  # Replace with your secondary password
        
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

def hiring_process_insights(request):
    return render(request,'hiringInsights.html')

def hiring_process_insights(request):
    insights = None

    if request.method == "POST":
        company_name = request.POST.get("company_name")
        job_role = request.POST.get("job_role")
        location = request.POST.get("location")

        if not company_name or not job_role or not location:
            return render(request, "hiringInsights.html", {"error": "All fields are required!"})

        try:
            # Configure Gemini AI
            genai.configure(api_key=os.getenv('GENAI_API_KEY'))
            model = genai.GenerativeModel('gemini-1.5-flash-latest')

            prompt = f"""
            Generate a detailed and structured hiring guide for a {job_role} position at {company_name} in {location}.
            If specific information about {company_name} is not available, provide general hiring trends and industry insights.

            1. Company Overview:
               - If {company_name} is well-known, provide details about its culture, work environment, and mission.
               - If {company_name} is a startup or has limited data, give a general overview of what candidates can expect in a company of this size.

            2. Salary Insights:
               - Provide the expected salary range for {job_role} in {location} based on industry standards.
               - Include salary variations by experience level (Entry, Mid, Senior).

            3. Interview Process:
               - Describe the typical interview structure for {job_role}.
               - If {company_name} has publicly available hiring information, mention it.
               - If data is limited, provide a general hiring framework used by similar companies.

            4. Past Interview Questions:
               - If available, list real questions asked in interviews at {company_name}.
               - Otherwise, provide common industry-standard questions for {job_role}.

            5. Key Topics to Prepare:
               - List technical and behavioral topics candidates should focus on.
               - Mention must-know concepts based on the job role.

            6. Best Study Resources:
               - Recommend useful books, courses, and platforms for interview preparation.

            7. Candidate Insights and Common Mistakes:
               - Share common challenges faced by candidates.
               - Provide actionable advice for acing the hiring process.

            Ensure the response is structured like an informative article rather than a direct answer to a prompt.
            Avoid using asterisks or formatting symbols.
            """

            # Generate response
            response = model.generate_content(prompt)
            insights = response.text if response and hasattr(response, "text") else "No insights available."

        except Exception as e:
            return render(request, "hiring_insights.html", {"error": str(e)})

    return render(request, "hiringInsights.html", {"insights": insights})

def career_roadmap(request):
    roadmap = None

    if request.method == "POST":
        Career_goal = request.POST.get("Career_goal")

        if not Career_goal:
            return render(request, "careerRoadmap.html", {"error": "All fields are required!"})

        try:
            # Configure Gemini AI
            os.environ["API_KEY"] = 'AIzaSyDyU3NhJ7MhfZT0fUWJH8S-xU8ZLqe9r9M'
            genai.configure(api_key=os.environ["API_KEY"])
            model = genai.GenerativeModel('gemini-1.5-flash-latest')
            
            prompt = f"""
            You are a career advisor, providing clear and actionable roadmaps for students and early career professionals. Act as a friendly instructor guiding them on their career journey.

            The user wants to become a {Career_goal}. Generate a detailed, step-by-step roadmap to achieve this goal.

            The roadmap MUST be broken down into well-defined sections using HTML heading tags (<h2> for section titles).  Use HTML paragraph tags (<p>) for regular text.  Use HTML unordered lists (<ul><li>) for lists of skills or steps.

            Each step should be practical and easy to follow. Include specific skills to learn, resources to explore, and actions to take. Be specific.

            Make sure each step is very detailed and also guide if there is any prerequisite to follow that step.

            Here are the required sections and how to format them:

            <h2>Foundational Skills and Knowledge</h2>
            <p>What basic knowledge/skills are needed BEFORE starting? Be specific.  For example:  Basic understanding of programming concepts.  Strong communication skills.</p>

            <h2>Education and Training</h2>
            <p>Specific degrees, certifications, online courses, bootcamps, etc.  Include specific course/certification names if possible and explain why each is valuable.</p>

            <h2>Skill Development</h2>
            <p>Detailed list of technical and soft skills.  Use an HTML unordered list (<ul><li> for each skill).  For each skill, suggest ways to learn it.  For example:</p>
            <ul>
            <li>Python: Learn through Codecademy, DataCamp, or freeCodeCamp</li>
            <li>Communication Skills: Practice public speaking, take a communication workshop.</li>
            </ul>

            <h2>Experience Building</h2>
            <p>Internships, personal projects, volunteer work, etc.  Explain how each type of experience helps and provide examples. Give very specific guidance on creating personal projects that will be impressive.</p>

            <h2>Networking</h2>
            <p>How to connect with professionals in the field.  Specific advice.  For example: Attend industry events. Join relevant LinkedIn groups. Reach out to alumni on LinkedIn for informational interviews.</p>

            <h2>Job Search Strategies</h2>
            <p>Resume/cover letter tips, interview preparation, online job boards to use, etc. Provide some very specific advice.</p>

            <h2>Continuous Learning and Advancement</h2>
            <p>How to stay up-to-date with industry trends and advance in their career over time. Mention any specific courses or certifications that are beneficial.</p>

            Important:
            *   The response is AI-generated and should be presented as such.
            *   Focus on providing a practical, actionable, and easy-to-follow guide.
            *   Do not include any introductory or concluding remarks. Only the roadmap itself.
            *   Use valid HTML tags.  Do not use Markdown.

            Here is the Roadmap:
            """


            # Generate response
            response = model.generate_content(prompt)
            roadmap = response.text if response and hasattr(response, "text") else "No roadmap available."

        except Exception as e:
            return render(request, "careerRoadmap.html", {"error": str(e)})

    return render(request, "careerRoadmap.html", {"roadmap": roadmap})


