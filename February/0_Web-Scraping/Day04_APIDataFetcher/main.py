import requests
from json import dumps

def get_joke() -> dict:
    try:
        url = f"https://icanhazdadjoke.com/"
        headers = {'Accept': 'application/json'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return {}

print(get_joke()["joke"])