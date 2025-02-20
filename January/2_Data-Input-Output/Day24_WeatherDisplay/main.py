import requests
from json import dumps

def get_weather(lat: int = 51.2217, lon: int = 6.7762) -> dict:
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,apparent_temperature,is_day,precipitation,rain,showers,snowfall,weather_code,cloud_cover,pressure_msl,surface_pressure,wind_speed_10m,wind_direction_10m,wind_gusts_10m&forecast_days=1"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return {}

def get_weather_as_dict(lat: int = 51.2217, lon: int = 6.7762) -> dict:
    weather = get_weather(lat, lon)
    return weather

weather = get_weather_as_dict()
for key, value in weather["current"].items():
    print(f"{key} is {value}")