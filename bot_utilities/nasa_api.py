import os
import json
import random
import dotenv
import requests

dotenv.load_dotenv()

class NasaApi(object):
    def __init__(self):
       self._api_key = os.getenv('NASA_API_TOKEN') 
       self._apod_url = f'https://api.nasa.gov/planetary/apod?api_key={self._api_key}'
       self._mars_photos_url = f'https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?sol={random.randint(1, 1000)}&page=1&api_key={self._api_key}'


    def get_apod(self):
        url = self._apod_url
        try:
            response = requests.get(url)
            data = json.loads(response.text)

            image_description = data['explanation']
            image_url = data.get('hdurl', data['url']) #We are going to use the hdurl if it exits, else we will use the normal url

            return [image_description, image_url]
        
        except Exception as e:
            return None


    def get_mars_rover_photo(self):
        url = self._mars_photos_url
        try:
            response = requests.get(url)
            data = json.loads(response.text)

            list_of_photos = data['photos']
            photo = random.choice(list_of_photos)

            #items to be returned
            img_src = photo['img_src']
            photo_date = photo['earth_date']
            camera_name = photo['camera']['full_name']
        
            return [img_src, photo_date, camera_name]
        
        except:
            return None

    
