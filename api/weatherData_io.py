import requests
import os
from dotenv import load_dotenv
load_dotenv()

def currentWeatherData(lat, lon, systemUnit):
    api_key = os.getenv('OPENWEATHER_API_KEY')
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units={systemUnit}"
    
    print(f"API Key: {api_key}")  # Check if API key is loaded
    print(f"URL: {url}")  # Check the full URL
    
    response = requests.get(url)
    
    print(f"Status Code: {response.status_code}")  # Check response
    print(f"Response: {response.text}")  # See what the API returned
    
    if response.status_code == 200:
        return response.json()
    else:
        return None
