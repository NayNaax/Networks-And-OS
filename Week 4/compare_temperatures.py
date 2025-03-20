import socket
import requests

# University coordinates (assumed to be the ones from the original example)
university_lat = 51.47
university_lon = -0.0363

# British Library coordinates
british_library_lat = 51.5290
british_library_lon = -0.1263

# Fetch weather data for university
uni_api_url = f"https://api.open-meteo.com/v1/forecast?latitude={university_lat}&longitude={university_lon}&current_weather=true"
uni_response = requests.get(uni_api_url)

# Fetch weather data for British Library
bl_api_url = f"https://api.open-meteo.com/v1/forecast?latitude={british_library_lat}&longitude={british_library_lon}&current_weather=true"
bl_response = requests.get(bl_api_url)

# Process the responses
if uni_response.status_code == 200 and bl_response.status_code == 200:
    uni_data = uni_response.json()
    bl_data = bl_response.json()
    
    uni_temp = uni_data["current_weather"]["temperature"]
    bl_temp = bl_data["current_weather"]["temperature"]
    
    temp_diff = abs(uni_temp - bl_temp)
    
    if uni_temp > bl_temp:
        comparison = "warmer than"
    elif uni_temp < bl_temp:
        comparison = "cooler than"
    else:
        comparison = "the same as"
    
    message = (f"University temperature: {uni_temp}°C\n"
               f"British Library temperature: {bl_temp}°C\n"
               f"The university is {comparison} the British Library by {temp_diff}°C")
else:
    message = "Failed to fetch weather data for one or both locations"

# Send the weather comparison using UDP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('localhost', 65433)
client_socket.sendto(message.encode(), server_address)
print("Weather comparison sent!")
client_socket.close()