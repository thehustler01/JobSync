import requests
import os
from django.conf import settings
def get_or_generate_video(question):
    media_path = os.path.join(settings.MEDIA_ROOT, "videos")
    os.makedirs(media_path, exist_ok=True)  # Ensure the "videos" folder exists

    save_path = os.path.join(media_path, f"{question}.mp4")

    # If video already exists, return its URL
    if os.path.exists(save_path):
        return settings.MEDIA_URL + f"videos/{question}.mp4"

    # Generate & download the video

    video_url=generate_video(question)
    response = requests.get(video_url, stream=True)
    if response.status_code == 200:
        with open(save_path, "wb") as video_file:
            for chunk in response.iter_content(chunk_size=1024):
                video_file.write(chunk)
        return settings.MEDIA_URL + f"videos/{question}.mp4"
    else:
        print("Failed to download video")
        return None


def generate_video(question):
    url = "https://api.heygen.com/v2/video/generate"

    payload = {
        "caption": False,
        "dimension": {
            "width": 1280,
            "height": 720
        },
        "title": "What is your experience with Python web frameworks like Django or Flask?",
        
        "video_inputs": [{
            "character":{
                "type" : "avatar",
                "avatar_id": "Leos_sitting_office_front",
            },

        "voice":{
            "type": "text",
            "voice_id" : "01d674cfd32b4728a3fddd21b7e7d543",
            "input_text": "What is your experience with Python web frameworks like Django or Flask?"
        }
        
        }]
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "x-api-key": ""
    }

    response = requests.post(url, json=payload, headers=headers)

    print(response.text)
    video_url=get_video_url(response.text)
    return video_url

#fetch the generated video
def get_video_url(video_id):
    url = "https://api.heygen.com/v1/video_status.get"

    headers = {
        "accept": "application/json",
        "x-api-key": ""
    }
    params ={
        "video_id": video_id
    }
    response = requests.get(url, headers=headers, params=params)
    print(response.status_code)
    response = response.json()
    print(response)
    video_url = response.get("data", {}).get("video_url")

    print(video_url)
    return video_url

