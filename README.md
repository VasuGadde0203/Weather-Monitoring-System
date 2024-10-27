# Real-Time Weather Monitoring System 🌦️

This project is a Real-Time Weather Monitoring System built with Django, enabling users to track weather conditions across multiple cities. The system provides both current weather information and a daily summary of weather trends, displaying the data in a user-friendly interface with visualizations.

## Table of Contents
- Features
- Tech Stack
- System Requirements
- Dependencies
- Setup and Installation
- Project Structure and Design Choices
- Running the Application
- Usage


## Features
- **Real-Time Weather Data:** Get live weather information by city, including temperature, main conditions, and timestamp.
- **Daily Summaries:** View summarized weather trends, including average, max, and min temperatures, and dominant weather conditions for the day.
- **Weather Alerts:** Displays weather alerts based on temperature thresholds and conditions.
- **Visualization:** Provides graphical representation of weather trends for better insights.

## Tech Stack
- **Backend:** Django (Python)
- **Frontend:** HTML, CSS, JavaScript (for UI and AJAX handling)
- **Database:** SQLite (default) or PostgreSQL (recommended for production)
- **Visualization:** Matplotlib (for generating weather trends images)

## System Requirements
- **Python** >= 3.8
- **Git** (for cloning the repository)

## Dependencies
To set up and run this project, install the following dependencies:

- **Django:** Web framework for the backend.
- **Django REST Framework:** For handling API calls.
- **Requests:** For making HTTP requests to external weather API.
- **Matplotlib:** For visualizing weather trends as images.
- **Database:** SQLite (default) or PostgreSQL (production recommendation).

## Install Dependencies
- pip install -r requirements.txt

## Setup and Installation
- **Clone the Repository**
  - **git clone https:**//github.com/VasuGadde0203/Weather-Monitoring-System.git
  - cd Weather-Monitoring-System

- **Create a Virtual Environment**
  - python3 -m venv venv
  - source venv/bin/activate  # on Windows: venv\Scripts\activate

## Apply Migrations
- python manage.py makemigrations
- python manage.py migrate

## Run the Server
- python manage.py runserver

## Project Structure and Design Choices

- **Structure**
  - **weather_monitor:** Contains the core app, managing the weather data fetching, processing, and display.
  - **templates:** HTML files for front-end views, styled to give a clean, professional look.
  - **static:** Contains CSS files and JavaScript (if applicable) for additional styling and
interactive UI elements.

- **Design Choices**
  - **Modular Code:** Each functionality (e.g., fetching weather data, generating summaries) is in a dedicated view or service function, enabling clean, maintainable code.
  - **API-Driven:** Fetches real-time weather data using an external API, making the system reliable and up-to-date.
  - **Visualization:** Generates plots for weather trends using Matplotlib, adding a visual representation for enhanced user experience.
  - **AJAX Support:** The data fetching uses AJAX to avoid page reloads when querying new weather information.
  - **Containerization:** Using Docker allows for isolated and consistent environments, making deployment and scaling easier.
  
## Running the Application
After setting up the application, navigate to http://127.0.0.1:8000 in your browser. The application offers three main sections:

- **Current Weather:** Select a city to get real-time weather information.
- **Daily Summary:** View a summary of the day's weather data with visualizations.
- **Alerts:** Weather alerts based on defined thresholds for different cities.

## Usage
- **Select City:** Enter or select a city from the list on the homepage.
- **View Data:** Once you submit, the system fetches the weather data and displays it.
- **Daily Summary and Alerts:** Access additional data, including summaries and alerts, through the navigation.
