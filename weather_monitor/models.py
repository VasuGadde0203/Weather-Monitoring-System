# weather_monitor/models.py

from django.db import models

class WeatherData(models.Model):
    city = models.CharField(max_length=50)
    main = models.CharField(max_length=50)  # e.g., Rain, Clear
    temp = models.FloatField()  # Current temperature in Celsius
    feels_like = models.FloatField()  # Feels like temperature in Celsius
    timestamp = models.DateTimeField(auto_now_add=True)  # Time of data update

    def __str__(self):
        return f"{self.city} - {self.main} at {self.timestamp}"

class DailySummary(models.Model):
    city = models.CharField(max_length=50)
    date = models.DateField()
    avg_temp = models.FloatField()
    max_temp = models.FloatField()
    min_temp = models.FloatField()
    dominant_weather = models.CharField(max_length=50)

    def __str__(self):
        return f"Summary for {self.city} on {self.date}"

class WeatherAlert(models.Model):
    condition = models.CharField(max_length=100)
    temperature = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.condition} Alert at {self.timestamp}"
