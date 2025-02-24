import requests

def get_motivation() -> tuple[str, str]:
    try:
        url = f"https://zenquotes.io/api/random"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return (data[0]["q"], data[0]["a"])
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return {}
    
print(f"{get_motivation()[0]}\n    ~ {get_motivation()[1]}")