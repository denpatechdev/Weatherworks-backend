import requests
import os

API_KEY = os.getenv('OPENWEATHER_API_KEY')

def forecastData(lat, lon, systemUnit):
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units={systemUnit}"    
    
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    return None

def geocodingData(lat, lon):
    url = f"http://api.openweathermap.org/geo/1.0/reverse?lat={lat}&lon={lon}&limit=1&appid={API_KEY}"

    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    return None

def currentWeatherData(lat, lon, systemUnit):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units={systemUnit}"
    
    # print(f"API Key: {API_KEY}")  # Check if API key is loaded
    # print(f"URL: {url}")  # Check the full URL
    
    response = requests.get(url)
    
    # print(f"Status Code: {response.status_code}")  # Check response
    # print(f"Response: {response.text}")  # See what the API returned
    
    if response.status_code == 200:
        return response.json()
    return None
