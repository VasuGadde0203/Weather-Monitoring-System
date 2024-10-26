# weather_monitor/tests.py

from django.test import TestCase
from .models import WeatherData, DailySummary
from .utils import get_weather_data, calculate_daily_summary, check_alerts

class WeatherMonitorTests(TestCase):
    def setUp(self):
        WeatherData.objects.create(
            city="Mumbai",
            main="Clear",
            temp=305.15 - 273.15,  # Kelvin to Celsius
            feels_like=308.15 - 273.15,
            timestamp="2024-01-01T12:00:00Z"
        )

    def test_temperature_conversion(self):
        weather = WeatherData.objects.get(city="Mumbai")
        self.assertAlmostEqual(weather.temp, 32.0, places=1)
        self.assertAlmostEqual(weather.feels_like, 35.0, places=1)

    def test_daily_summary_calculation(self):
        # Ensure calculate_daily_summary works correctly
        calculate_daily_summary()
        summary = DailySummary.objects.get(city="Mumbai", date="2024-01-01")
        self.assertAlmostEqual(summary.avg_temp, 32.0, places=1)

    def test_alert_trigger(self):
        # Insert data to trigger an alert
        WeatherData.objects.create(city="Mumbai", temp=36.0)
        WeatherData.objects.create(city="Mumbai", temp=37.0)
        
        # Expect alert for consecutive high temperatures
        with self.assertLogs(level='INFO') as log:
            check_alerts(threshold_temp=35)
            self.assertIn("Alert: High temperature", log.output[0])
