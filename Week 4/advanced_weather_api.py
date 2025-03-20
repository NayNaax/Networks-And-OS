import socket
import requests
import json
from datetime import datetime

# London coordinates
london_lat = 51.5074
london_lon = -0.1278

# Create a more advanced API request with multiple parameters
api_url = (f"https://api.open-meteo.com/v1/forecast?"
           f"latitude={london_lat}&longitude={london_lon}"
           f"&hourly=temperature_2m,precipitation_probability,windspeed_10m"
           f"&daily=temperature_2m_max,temperature_2m_min,sunrise,sunset"
           f"&current_weather=true&timezone=Europe/London")

response = requests.get(api_url)

if response.status_code == 200:
    weather_data = response.json()
    
    # Extract current weather
    current = weather_data["current_weather"]
    current_temp = current["temperature"]
    current_wind = current["windspeed"]
    
    # Get today's date in the format used by the API
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Find today's index in the daily data
    today_index = weather_data["daily"]["time"].index(today) if today in weather_data["daily"]["time"] else 0
    
    # Extract daily forecast for today
    max_temp = weather_data["daily"]["temperature_2m_max"][today_index]
    min_temp = weather_data["daily"]["temperature_2m_min"][today_index]
    sunrise = weather_data["daily"]["sunrise"][today_index]
    sunset = weather_data["daily"]["sunset"][today_index]
    
    # Format a detailed weather report
    message = (f"London Weather Report\n"
               f"---------------------\n"
               f"Current temperature: {current_temp}°C\n"
               f"Current wind speed: {current_wind} km/h\n"
               f"Today's high: {max_temp}°C\n"
               f"Today's low: {min_temp}°C\n"
               f"Sunrise: {sunrise.split('T')[1]}\n"
               f"Sunset: {sunset.split('T')[1]}\n\n"
               f"Next 3 hours forecast:\n")
    
    # Add hourly forecast for the next 3 hours
    current_hour = datetime.now().hour
    for i in range(3):
        hour_index = current_hour + i
        if hour_index < len(weather_data["hourly"]["time"]):
            hour_time = weather_data["hourly"]["time"][hour_index].split("T")[1]
            hour_temp = weather_data["hourly"]["temperature_2m"][hour_index]
            hour_precip = weather_data["hourly"]["precipitation_probability"][hour_index]
            hour_wind = weather_data["hourly"]["windspeed_10m"][hour_index]
            
            message += (f"{hour_time}: {hour_temp}°C, "
                        f"Precipitation: {hour_precip}%, "
                        f"Wind: {hour_wind} km/h\n")
else:
    message = "Failed to fetch weather data"

# Send the detailed weather report using UDP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('localhost', 65433)
client_socket.sendto(message.encode(), server_address)
print("Detailed weather report sent!")
client_socket.close()