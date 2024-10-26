# weather_monitor/views.py

from django.shortcuts import render
from .models import WeatherData, DailySummary
from .models import WeatherAlert 
from .utils import fetch_weather, check_alerts
from django.http import JsonResponse
import os
import requests
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
from django.shortcuts import render
from .models import DailySummary
from django.http import HttpResponse
from django.core.files.base import ContentFile
import base64

API_KEY = '83fca560fdc127629c028b99f934c309'  # Replace with your actual API key
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'

def fetch_weather_view(request):
    # Call the fetch_weather function and get weather data
    if request.method == 'POST':
        weather_data = fetch_weather()  # Assuming fetch_weather() returns the weather data
        city = request.POST.get('city')
        weather_data_list = []
        for wd in weather_data:
            weather_data_list.append(
                {
                    "city": wd.city,
                    "main": wd.main,
                    "temp": wd.temp,
                    "feels_like": wd.feels_like,
                    "timestamp": wd.timestamp,
                }
            )

        alerts = check_alerts(weather_data_list)

        # If you are getting multiple weather records, filter to get the correct one based on the city
        weather_entry = next((item for item in weather_data_list if item['city'].lower() == city.lower()), None)

        if weather_entry:
            # Prepare the response data
            response_data = {
                'weather_data': {
                    'city': weather_entry['city'],
                    'main': weather_entry['main'],
                    'temp': round(weather_entry['temp'], 2),
                    'feels_like': round(weather_entry['feels_like'], 2),
                    'timestamp': weather_entry['timestamp'].astimezone().strftime("%Y-%m-%d %H:%M:%S")  # Format the timestamp
                },
                'alerts': [
                {
                    "condition": alert.condition,
                    "temperature": alert.temperature,
                    "timestamp": alert.timestamp,
                } for alert in alerts
            ]  # Your existing alert check
            }
        else:
            response_data = {
                'weather_data': None,
                'alerts': []
            }
        
        return JsonResponse(response_data)

def index(request):
    latest_weather = WeatherData.objects.all().order_by('-timestamp')[:10]
    return render(request, 'weather_monitor/index.html', {'latest_weather': latest_weather})


def fetch_and_store_weather_data(city):
    url = f"{BASE_URL}?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        
        # Parse the data
        city_name = data['name']
        avg_temp = data['main']['temp']
        max_temp = data['main']['temp_max']
        min_temp = data['main']['temp_min']
        dominant_weather = data['weather'][0]['description']
        date = datetime.now().date()

        # Save to DailySummary model
        DailySummary.objects.create(
            city=city_name,
            date=date,
            avg_temp=avg_temp,
            max_temp=max_temp,
            min_temp=min_temp,
            dominant_weather=dominant_weather
        )
        return f"Weather data for {city_name} on {date} stored successfully!"
    else:
        return f"Error fetching data: {response.status_code}"

def generate_weather_visualization():
    summaries = DailySummary.objects.all()
    
    if not summaries:
        return None  # No data to visualize

    dates = [summary.date for summary in summaries]
    avg_temps = [summary.avg_temp for summary in summaries]
    max_temps = [summary.max_temp for summary in summaries]
    min_temps = [summary.min_temp for summary in summaries]

    plt.figure(figsize=(10, 6))
    plt.plot(dates, avg_temps, label='Average Temperature (°C)', marker='o')
    plt.plot(dates, max_temps, label='Max Temperature (°C)', marker='o')
    plt.plot(dates, min_temps, label='Min Temperature (°C)', marker='o')

    plt.title('Weather Summary Trends')
    plt.xlabel('Date')
    plt.ylabel('Temperature (°C)')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()

    # Save the figure to a bytes buffer
    from io import BytesIO
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)

    # Encode the image in base64 to display in HTML
    image_png = buffer.getvalue()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')
    return graphic

def daily_summary_view(request):
    summaries = DailySummary.objects.all()  # Fetch all daily summaries
    if request.method == 'POST':
        city = request.POST.get('city')
        if city:
            message = fetch_and_store_weather_data(city)
            graphic = generate_weather_visualization()
            return render(request, 'weather_monitor/daily_summary.html', {'message': message, 'summaries': summaries, 'graphic': graphic})

    return render(request, 'weather_monitor/daily_summary.html')