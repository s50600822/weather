import os
import requests
from datetime import datetime


def get_weather_forecast(api_key, location, date):
    url = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={location}&dt={date}"
    response = requests.get(url)
    return response.json()


try:
    api_key = os.environ['WEATHER_API_KEY']
    tday = today_date = datetime.today().strftime('%Y-%m-%d')
    res = get_weather_forecast(api_key, "Pymble", tday)
    by_hours = res['forecast']['forecastday'][0]['hour']
    for hour in by_hours:
        t = hour['time']
        epoch = hour['time_epoch']
        tempc = hour['temp_c']
        print(hour)
        print("\n")
        
except KeyError:
    print("Environment variable 'WEATHER_API_KEY' does not exist.")