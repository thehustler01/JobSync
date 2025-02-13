from django.db import models

class Resume(models.Model):
    original_filename = models.CharField(max_length=255) 
    resume_file = models.FileField(upload_to='resumes/', null=True, blank=True)  
    email = models.EmailField(null=True) 
    phone_number = models.CharField(max_length=20, null=True, blank=True)  
    skills = models.JSONField(null=True) 
    suggested_job_role = models.CharField(max_length=255, null=True) 
    required_skills = models.JSONField(null=True)  
    missing_skills = models.JSONField(null=True, blank=True) 
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)  

    def __str__(self):
        return f"{self.original_filename} by {self.email}"
    

class CourseListings(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField()
    skills = models.JSONField()
    rating = models.FloatField()
    details = models.JSONField()
    scraped_for = models.CharField(default="trending") 

    def __str__(self):
        return self.title
