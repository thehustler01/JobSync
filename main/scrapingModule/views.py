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
        driver = webdriver.Chrome(service=service, options=chrome_options)
        # driver = webdriver.Chrome(service=service)
        
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
            <h2>Hiring Guide for <span class="job-role">{job_role}</span> at <span class="company-name">{company_name}</span> in <span class="location">{location}</span></h2>

            <h3>1. Company Overview</h3>
            <p>If <span class="company-name">{company_name}</span> is well-known, provide details about its culture, work environment, and mission.</p>
            <p>If <span class="company-name">{company_name}</span> is a startup or has limited data, give a general overview of what candidates can expect in a company of this size.</p>

            <h3>2. Salary Insights</h3>
            <ul>
            <li>Expected salary range for <span class="job-role">{job_role}</span> in <span class="location">{location}</span> based on industry standards.</li>
            <li>Salary variations by experience level:
            <ul>
                <li><strong>Entry Level:</strong> [Insert range]</li>
                <li><strong>Mid-Level:</strong> [Insert range]</li>
                <li><strong>Senior Level:</strong> [Insert range]</li>
            </ul>
            </li>
            </ul>

            <h3>3. Interview Process</h3>
            <ul>
            <li>Typical interview structure for <span class="job-role">{job_role}</span>.</li>
            <li>If <span class="company-name">{company_name}</span> has public hiring information, mention it.</li>
            <li>If data is limited, provide a general hiring framework used by similar companies.</li>
            </ul>

            <h3>4. Past Interview Questions</h3>
            <ul>
            <li>If available, list real questions asked in interviews at <span class="company-name">{company_name}</span>.</li>
            <li>Otherwise, provide common industry-standard questions for <span class="job-role">{job_role}</span>.</li>
            </ul>

            <h3>5. Key Topics to Prepare</h3>
            <ul>
            <li>Technical and behavioral topics candidates should focus on.</li>
            <li>Must-know concepts based on the job role.</li>
            </ul>

            <h3>6. Best Study Resources</h3>
            <ul>
            <li>Recommended books, courses, and platforms for interview preparation.</li>
            </ul>

            <h3>7. Candidate Insights and Common Mistakes</h3>
            <ul>
            <li>Common challenges faced by candidates.</li>
            <li>Actionable advice for acing the hiring process.</li>
            </ul>

            """

            # Generate response
            response = model.generate_content(prompt)
            insights = response.text if response and hasattr(response, "text") else "No insights available."
            print(insights)

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
            genai.configure(api_key=os.getenv('GENAI_API_KEY'))
            # model = genai.GenerativeModel('gemini-1.5-flash-latest')
            model = genai.GenerativeModel('gemini-1.5-pro')
            
            prompt = f"""
            Given a career goal of <strong>{Career_goal}</strong>, generate a detailed career roadmap outlining the essential steps and time required to achieve this goal in phases. The roadmap should include:

            <h2>Skills to Learn</h2>
            <p>List the core technical and soft skills required for this role:</p>
            <ul>
            <li>Technical Skills (e.g., programming languages, software tools, etc.)</li>
            <li>Soft Skills (e.g., communication, problem-solving, teamwork)</li>
            <li>Industry-specific knowledge (e.g., finance, healthcare, technology)</li>
            </ul>

            <h2>Learning Resources</h2>
            <p>Suggest online courses, books, or platforms to acquire these skills:</p>
            <ul>
            <li><strong>Coursera</strong> – Offers comprehensive courses tailored to the career goal</li>
            <li><strong>edX</strong> – Provides professional certificates in related fields</li>
            <li><strong>Books</strong> – Relevant literature that covers theory and practical applications</li>
            <li><strong>Online Communities</strong> – Platforms like StackOverflow, Reddit, and LinkedIn groups</li>
            </ul>

            <h2>Projects to Build</h2>
            <p>Recommend practical projects to solidify knowledge and improve hands-on experience:</p>
            <ul>
            <li>Work on an open-source project to gain collaboration experience</li>
            <li>Develop a portfolio showcasing your best work</li>
            </ul>

            <h2>Certifications (if applicable)</h2>
            <p>Mention any industry-recognized certifications that can add value:</p>
            <ul>
            <li>Relevant industry certification </li>
            <li>Course completion certificates from recognized platforms like Coursera or edX</li>
            </ul>

            <h2>Experience Building</h2>
            <p>Suggest internships, open-source contributions, or part-time work that can help gain practical exposure:</p>
            <ul>
            <li>Apply for internships in relevant fields to gain real-world experience</li>
            <li>Contribute to open-source projects for portfolio building</li>
            <li>Seek freelance or part-time work to build practical skills</li>
            </ul>

            <h2>Interview Preparation</h2>
            <p>Provide guidance on common interview topics, coding platforms for practice, and behavioral interview tips:</p>
            <ul>
            <li>Review technical questions related to the role and practice coding challenges</li>
            <li>Prepare for behavioral interviews using the STAR method (Situation, Task, Action, Result)</li>
            <li>Practice mock interviews with peers or mentors</li>
            </ul>

            <h2>Career Progression</h2>
            <p>Outline a typical career path and possible specializations in this field:</p>
            <ul>
            <li>Entry-Level Position</li>
            <li>Mid-Level Position with increased responsibility</li>
            <li>Senior-Level Role or Specialist Role</li>
            <li>Transition into management or advanced specialization</li>
            </ul>

            <p>Ensure the roadmap is structured step-by-step, practical, and aligned with industry standards. Provide clear action points that a beginner can follow systematically. Word limit should be 400 words.</p>

            Use valid HTML tags.  Do not use Markdown.
            """


            # Generate response
            response = model.generate_content(prompt)
            roadmap = response.text if response and hasattr(response, "text") else "No roadmap available."

        except Exception as e:
            return render(request, "careerRoadmap.html", {"error": str(e)})

    return render(request, "careerRoadmap.html", {"roadmap": roadmap})


