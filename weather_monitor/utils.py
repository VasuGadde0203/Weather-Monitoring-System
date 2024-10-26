# weather_monitor/utils.py

import requests
from datetime import datetime
from .models import WeatherData
from django.db.models import Avg, Max, Min, Count
from .models import DailySummary
from django.conf import settings
from django.utils import timezone
from .models import WeatherData, WeatherAlert


API_KEY = '83fca560fdc127629c028b99f934c309'
CITY_LIST = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'

def fetch_weather():
    api_key = '83fca560fdc127629c028b99f934c309'  # Replace with your actual API key
    cities = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']
    weather_data_list = []

    for city in cities:
        response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric")
        if response.status_code == 200:
            data = response.json()
            # Extract required data
            main_condition = data['weather'][0]['main']  # e.g., Rain, Clear
            temp = float(data['main']['temp'])
            feels_like = float(data['main']['feels_like'])

            # Save data to the database
            weather_data = WeatherData.objects.create(
                city=city,
                main=main_condition,
                temp=temp,
                feels_like=feels_like,
                timestamp=timezone.now()
            )
            weather_data_list.append(weather_data)

        else:
            print(f"Failed to retrieve data for {city}: {response.status_code} - {response.text}")
    # print(weather_data_list)
    
    return weather_data_list  # Return the saved WeatherData objects

def calculate_daily_summary():
    for city in CITY_LIST:
        weather_data = WeatherData.objects.filter(city=city, timestamp__date=datetime.today())
        if weather_data:
            avg_temp = weather_data.aggregate(Avg('temp'))['temp__avg']
            max_temp = weather_data.aggregate(Max('temp'))['temp__max']
            min_temp = weather_data.aggregate(Min('temp'))['temp__min']

            # Finding the dominant weather condition by frequency
            dominant_weather = weather_data.values('main').annotate(count=Count('main')).order_by('-count').first()['main']

            summary = DailySummary(
                city=city,
                date=datetime.today().date(),
                avg_temp=avg_temp,
                max_temp=max_temp,
                min_temp=min_temp,
                dominant_weather=dominant_weather
            )
            summary.save()


def check_alerts(weather_data):
    alerts = []
    temperature_threshold = 25  # Example threshold
    # print(weather_data)

    for entry in weather_data:
        # Check if the temperature exceeds the threshold
        # print(entry)
        if entry['temp'] > temperature_threshold:
            alert = WeatherAlert.objects.create(
                condition=f"Temperature exceeds {temperature_threshold}°C in {entry['city']}",
                temperature=entry['temp'],
                timestamp=timezone.now()
            )
            alerts.append(alert)
    
    return alerts  # Return the list of alerts

