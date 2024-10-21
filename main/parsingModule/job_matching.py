from django.conf import settings
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
from .models import JobRole,Recommendation
from .views import resume_details

def recommend_job(skillset):

    print(skillset,"in matchingggggggg")
    User=skillset
    User=', '.join(User)
    path = os.path.join(settings.MEDIA_ROOT, 'job_role_matching.csv')

    df=pd.read_csv(path)

    req_skills=df['Skills Required'].tolist()
    corpus=[User]+req_skills

    vectorizer=CountVectorizer()
    skill_matrix = vectorizer.fit_transform(corpus)

    user_vector = skill_matrix[0] 
    job_vectors = skill_matrix[1:]

    similarities = cosine_similarity(user_vector, job_vectors)

    most_similar_job_index = similarities.argmax()
    most_similar_job_description = req_skills[most_similar_job_index]

    job_skillset=set(most_similar_job_description.split(', '))
    User_skillset=set(User.split(', '))

    jobRole=df['Job Role'][most_similar_job_index]
    job_skillset=list(map(str.lower,job_skillset))
    User_skillset=list(map(str.lower,User_skillset))

    missing_skills = set(job_skillset) - set(User_skillset)
    suggested_job=JobRole(role_name=jobRole,required_skills=job_skillset,missing_skills=list(missing_skills))
    suggested_job.save()
    recommend=Recommendation(job_role_id=suggested_job.id, resume_id=resume_details.id)
    recommend.save()
    print(job_skillset)
    print(User_skillset)
    print(missing_skills)
    print(jobRole)
