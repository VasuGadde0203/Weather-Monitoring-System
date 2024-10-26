# weather_monitor/urls.py

from . import views
from django.urls import path, include
from django_plotly_dash import urls as plotly_dash_urls

urlpatterns = [
    path('', views.index, name='index'),
    path('daily_summary/', views.daily_summary_view, name='daily_summary'),
    path('fetch_weather/', views.fetch_weather_view, name='fetch_weather'),  
]
