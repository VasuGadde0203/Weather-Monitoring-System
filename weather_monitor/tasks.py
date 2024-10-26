# weather_monitor/tasks.py

from celery import shared_task
from .utils import get_weather_data, calculate_daily_summary, check_alerts

@shared_task
def fetch_weather_data_task():
    get_weather_data()

@shared_task
def calculate_daily_summary_task():
    calculate_daily_summary()

@shared_task
def check_alerts_task():
    check_alerts()
