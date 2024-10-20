from django.db import models

class JobListing(models.Model):
    title = models.TextField()  
    company = models.TextField()  
    job_link = models.URLField(max_length=1000)  
    location = models.TextField()  
    description = models.TextField(null=True, blank=True)  
    salary = models.TextField(null=True, blank=True) 
    scraped_for = models.CharField()  
    scraped_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} at {self.company}"

