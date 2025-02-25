from requests import get
from bs4 import BeautifulSoup

STD_URL = "https://www.scrapethissite.com/pages/frames/?frame=i"
STD_PATH = "February/0_Web-Scraping/Day02_ImageScraper/imgs/"

def scrape_for_images(url: str = STD_URL, i: int = 10) -> list[tuple[str, str]]:
    result: list[tuple[str, str]] = []
    request = get(url)
    if request.status_code != 200:
        raise Exception("Site not reachable")
    site: bytes = request.content
    site: BeautifulSoup = BeautifulSoup(site, "html.parser")
    turtels: str = site.find_all('div', class_="turtle-family-card")
    for k, turtle in enumerate(turtels):
        if k >= i:
            break
        name: str = turtle.find('h3', class_="family-name").text.strip()
        image: str = turtle.find('img').attrs['src']
        result.append((name, image))
    return result

def download_images(toDownload: list[tuple[str, str]], dir_path: str = STD_PATH) -> None:
    i = 0
    for link in toDownload:
        link = link[1]
        request = get(link)
        if request.status_code != 200:
            break
        with open(f"{dir_path}{link.split("/")[-1]}", "wb") as file:
            file.write(request.content)
        i += 1
    print(f"Extracted {i} Images")

def pretty_print(toPrint: list[tuple[str, str]]) -> None:
    for j in range(len(toPrint)):
        print(f"Turtle Type: {toPrint[j][0]}:")
        print(f"   Image Link: {toPrint[j][1]}")


response = scrape_for_images()
pretty_print(response)
download_images(response)
