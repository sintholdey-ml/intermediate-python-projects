import argparse
import sys
import requests

GEO_API_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_API_URL = "https://api.open-meteo.com/v1/forecast"

def get_coordinates(city_name):
    try:
        response = requests.get(GEO_API_URL, params={"name": city_name, "count": 1}, timeout=10)
        response.raise_for_status()
        data = response.json()

        if not data.get("results"):
            print(f"Error: City '{city_name}' not found.")
            sys.exit(1)

        location = data["results"][0]
        return location["latitude"], location["longitude"], location["name"], location.get("country", "")
    except requests. RequestException as e:
        print(f" Connection Error: {e}")
        sys.exit(1)

def get_weather_fallback(city_name):
    # Fallback to wttr.in API if Open-Meteo times out
    try:
        url = f"https://wttr.in/{city_name}?format=j1"
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        data = response.json()
        current = data["current_condition"][0]
        
        print("\n" + "=" * 45)
        print(f"  WEATHER FORECAST: {city_name.upper()} (via wttr.in)")
        print("=" * 45)
        print(f"  Temperature       : {current['temp_C']} °C")
        print(f"  Relative Humidity : {current['humidity']} %")
        print(f"  Wind Speed        : {current['windspeedKmph']} km/h")
        print("=" * 45 + "\n")
        return True
    except Exception as e:
        print(f" Fallback Error: {e}")
        return False

def get_weather(lat, lon):
    params = {
        "latitude" : lat,
        "longitude" : lon,
        "current" : ["temperature_2m", "relative_humidity_2m", "wind_speed_10m", "weather_code"],
        "timezone": "auto"
    }
    try:
        response = requests.get(WEATHER_API_URL, params= params, timeout= 10)
        response.raise_for_status()
        return response.json().get("current", {})
    except requests.RequestException as e:
        print(f"Connection Error: {e}")
        sys.exit(1)


def display_weather(city, country, current):
    temp= current.get("temperature_2m")
    humidity = current.get("relative_humidity_2m")
    wind_speed = current.get("wind_speed_10m")

    print("\n" + "=" * 45)
    print(f" WEATHER FORECAST: {city.upper()}, {country.upper()}")
    print("=" * 45)
    print(f"  Temperature       : {temp} °C")
    print(f"  Relative Humidity : {humidity} %")
    print(f"  Wind Speed        : {wind_speed} km/h")
    print("=" * 45 + "\n")

def main():
    parser = argparse.ArgumentParser(description="Python CLI Weather Forecast Tool")
    parser.add_argument("-c", "--city", default="Dhaka", help="City name (default: Dhaka)")

    args = parser.parse_args()

    lat, lon, city_name, country = get_coordinates(args.city)
    current_weather = get_weather(lat, lon)
    display_weather(city_name, country, current_weather)

if __name__ == "__main__":
    main()