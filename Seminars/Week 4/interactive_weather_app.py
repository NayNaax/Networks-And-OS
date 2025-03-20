import socket
import requests
import sys
import time

def get_weather_by_city(city_name):
    """Get weather for a city by name using geocoding and weather API"""
    
    try:
        # First, get coordinates for the city
        print(f"Searching for coordinates of {city_name}...")
        geo_api_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1"
        geo_response = requests.get(geo_api_url)
        
        if geo_response.status_code != 200:
            print(f"API Error: Status code {geo_response.status_code}")
            return f"Could not find coordinates for city: {city_name}"
        
        # Check if results exist
        results = geo_response.json().get("results")
        if not results:
            print(f"No results found for {city_name}")
            return f"Could not find coordinates for city: {city_name}"
        
        # Extract coordinates
        location = results[0]
        lat = location["latitude"]
        lon = location["longitude"]
        full_name = f"{location.get('name', city_name)}, {location.get('country', 'Unknown')}"
        
        print(f"Found location: {full_name} at coordinates {lat}, {lon}")
        
        # Now get weather data
        print(f"Fetching weather data...")
        weather_api_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        weather_response = requests.get(weather_api_url)
        
        if weather_response.status_code != 200:
            print(f"Weather API Error: Status code {weather_response.status_code}")
            return f"Could not get weather data for {city_name}"  # Fixed: Avoid using undefined `full_name`
        
        # Extract temperature
        weather_data = weather_response.json()
        temperature = weather_data["current_weather"]["temperature"]
        wind_speed = weather_data["current_weather"]["windspeed"]
        
        return f"Weather for {full_name}:\nTemperature: {temperature}°C\nWind Speed: {wind_speed} km/h"
    
    except requests.exceptions.ConnectionError as e:
        print(f"Connection error: {e}")
        return "Network connection error. Please check your internet connection."
    except KeyError as e:
        print(f"Key error in API response: {e}")
        return f"API format error: Missing expected data ({e})"
    except Exception as e:
        print(f"Unexpected error: {e}")
        return f"An error occurred: {e}"

if __name__ == "__main__":
    try:
        # Create a UDP socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_address = ('localhost', 65433)
        
        print("Interactive Weather App")
        print("Type 'exit' to quit")
        
        while True:
            try:
                city = input("Enter city name: ")
                if city.lower() == 'exit':
                    break
                
                weather_info = get_weather_by_city(city)
                print(weather_info)
                
                # Send to server as well
                try:
                    client_socket.sendto(weather_info.encode(), server_address)
                    print("Data sent to server successfully")
                except Exception as e:
                    print(f"Error sending data to server: {e}")
            
            except Exception as e:
                print(f"Error in main loop: {e}")
                
        client_socket.close()
        
    except Exception as e:
        print(f"Fatal error: {e}")
        print("Press Enter to exit...")
        input()  # This prevents the window from closing immediately