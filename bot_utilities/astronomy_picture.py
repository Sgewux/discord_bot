import json
import requests

def get_astronomy_pic():
    url = 'https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY'
    try:
        response = requests.get(url)
        data = json.loads(response.text)

        image_description = data['explanation']
        image_url = data.get('hdurl', data['url']) #We are going to use the hdurl if it exits, else we will use the normal url

        return [image_description, image_url]
        
    except Exception as e:
        return None






