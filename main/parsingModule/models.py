from django.db import models

class Resume(models.Model):
    original_filename = models.CharField(max_length=255) 
    extracted_text = models.TextField()  
    email = models.EmailField(unique=True)  
    phone_number = models.CharField(max_length=20, null=True, blank=True) 
    skills = models.JSONField()  
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f"{self.original_filename} by {self.email}"

class JobRole(models.Model):
    role_name = models.CharField(max_length=255, unique=True)  
    description = models.TextField(null=True, blank=True)  
    required_skills = models.JSONField() 
    missing_skills = models.JSONField(null=True, blank=True) 

    def __str__(self):
        return self.role_name

class Recommendation(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='recommendations')  
    job_role = models.ForeignKey(JobRole, on_delete=models.CASCADE, related_name='recommendations') 
    created_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f"Recommendation for {self.resume} - {self.job_role}"


