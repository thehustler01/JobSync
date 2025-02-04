from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
from django.shortcuts import render  
import urllib.parse
import json 

def recommendCourse(missing_skills):
    course_data=[]
    # Setup Chrome WebDriver
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode (no UI)
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Bypass detection
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-dev-shm-usage")
    service = Service('./drivers/chromedriver.exe')
    try:
        driver = webdriver.Chrome(service=service)
        
        # Open Udemy search results page
        # query = "machine+learning"
        if(len(missing_skills)==0):
            missing_skills=["machine learning"]
        missing_skills=missing_skills[:5]
        for skill in missing_skills:
            try:
                encoded_skill = urllib.parse.quote(skill)
                url = f"https://www.coursera.org/search?query={encoded_skill}"
                driver.get(url)

                # Wait for content to load
                time.sleep(5)

                # Scrape course titles
                courses = driver.find_elements(By.CSS_SELECTOR, "div.cds-ProductCard-content")[:5]
                i=0
                for course in courses:
                    link_element = course.find_element(By.CSS_SELECTOR, "a")  # Course Link inside div
                    link = link_element.get_attribute("href")  # Get course URL
                    title=link_element.text
                    
                    rating_element=course.find_element(By.CSS_SELECTOR, "div.cds-RatingStat-meter")
                    rating=rating_element.find_element(By.TAG_NAME, "span").text
                    
                    metadata=course.find_element(By.CSS_SELECTOR, "div.cds-CommonCard-metadata").text
                    
                    skills= course.find_element(By.CSS_SELECTOR, "div.cds-ProductCard-body").text
                    skills = skills.split(":", 1)[1].strip() 
                    skills= skills[:100] + "..." if len(skills) > 100 else skills
                    course_data.append({"title": title, "url": link, "skills":skills, "rating":rating, "details":metadata})
            except Exception as e:
                print("Error:", e)
    except Exception as e:
        print("Error:", e)
    finally:
        driver.quit()
    return course_data
