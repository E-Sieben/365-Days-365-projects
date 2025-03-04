from requests_html import HTMLSession
from bs4 import BeautifulSoup

STD_URL = "https://www.scrapethissite.com/pages/ajax-javascript/"

def scrape_for_films(url: str = STD_URL) -> list[tuple[str, str, str]]:
    result: list[tuple[str, str, str]] = []
    session = HTMLSession()
    response = session.get(url)
    site: BeautifulSoup = BeautifulSoup(response.html.html, "html.parser")
    categories = site.find_all("a", class_="year-link")
    for link in categories:
        link_url = f"{url}#{link.text.strip()}"
        sub_response = session.get(link_url)
        i: int = 2
        while True:
            sub_response.html.render(sleep=i)
            sub_site: BeautifulSoup = BeautifulSoup(sub_response.html.html, "html.parser")
            films = sub_site.find_all("tr", class_="film")
            if films is not None:
                break
            i += 1
        for film in films:
            title: str = film.find("td", class_="film-title").text.strip()
            nominations: str = film.find("td", class_="film-nominations").text.strip()
            awards: str = film.find("td", class_="film-awards").text.strip()
            result.append((title, nominations, awards, link.text.strip()))
    return result

def pretty_print_films(toPrint: list[tuple[str, str, str]], i: int = 0) -> None:
    if i == 0 or i > len(toPrint):
        i: int = len(toPrint)
        print(f"Printing {i} Objects, due to max Amount found")
    for j in range(i):
        print(f"{toPrint[j][0]}:")
        print(f"   Nominations: {toPrint[j][1]}")
        print(f"   Awards: {toPrint[j][2]}")
        print(f"   Year: {toPrint[j][3]}\n")

pretty_print_films(scrape_for_films())