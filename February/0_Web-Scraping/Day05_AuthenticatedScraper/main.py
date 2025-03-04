
# https://www.zenrows.com/blog/web-scraping-login-python#scrape-sites-requiring-login

import requests

login_url = "https://www.scrapingcourse.com/login"

payload = {
    "email": "hihi@hehe.huh",
    "password": "passwd",
}

response = requests.post(login_url, data=payload)

print(f"Status code: {response.status_code}")
