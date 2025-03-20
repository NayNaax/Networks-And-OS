import socket
import requests

# Fetch weather data
api_url = "https://api.open-meteo.com/v1/forecast?latitude=51.47&longitude=-0.0363&current_weather=true"
response = requests.get(api_url)

if response.status_code == 200:
    weather_data = response.json()
    temperature = weather_data["current_weather"]["temperature"]
    message = f"Current temperature: {temperature}°C"
else:
    message = "Failed to fetch weather data"

# Send the weather data using UDP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('localhost', 65433)
client_socket.sendto(message.encode(), server_address)
print("Weather data sent!")
client_socket.close()