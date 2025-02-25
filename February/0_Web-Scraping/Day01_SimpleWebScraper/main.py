from requests import get
from bs4 import BeautifulSoup

STD_URL = "https://realpython.github.io/fake-jobs/"

def scrape_for_jobs(url: str = STD_URL) -> list[tuple[str, str, str]]:
    result: list[tuple[str, str, str]] = []
    site = get(url).content
    site: BeautifulSoup = BeautifulSoup(site, "html.parser")
    jobs = site.find_all("div", class_="card-content")
    for job in jobs:
        title: str = job.find("h2", class_="title").text.strip()
        company: str = job.find("h3", class_="company").text.strip()
        location: str = job.find("p", class_="location").text.strip()
        result.append((title, company, location))
    return result

def pretty_print_jobs(toPrint: list[tuple[str, str, str]], i: int = 10) -> None:
    if i == 0:
        i = len(toPrint)
    for j in range(i):
        print(f"{toPrint[j][0]}:")
        print(f"   Company: {toPrint[j][1]}")
        print(f"   Location: {toPrint[j][2]}\n")

pretty_print_jobs(scrape_for_jobs(), 2)