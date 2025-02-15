"""Extract prices."""

from shutil import which

import requests
from bs4 import BeautifulSoup
from selenium import webdriver

# from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

firefox_options = Options()
firefox_options.add_argument("--headless")  # Run in headless mode
firefox_service = Service(which("geckodriver"))

headers = {"User-Agent": "Dottor Professor Truffatore Imbroglione"}


def list_sites():
    """Return names of supported websites."""
    return [
        "adelphi",
        "buecher",
        "feltrinelli",
        "hoepli",
        "hugendubel",
        "ibs",
        "libcoop",
        "libraccio",
        "libuni",
        "mondadori",
        "osiander",
        "rizzoli",
    ]


def list_sites_links_short():
    """Return list of supported webiste, short version."""
    return [
        "adelphi.it",
        "buecher.de",
        "lafeltrinelli.it",
        "hoepli.it",
        "hugendubel.de",
        "ibs.it",
        "librerie.coop",
        "libraccio.it",
        "libreriauniversitaria.it",
        "mondadoristore.it",
        "osiander.de",
        "libreriarizzoli.it",
    ]


def list_sites_links():
    """Return links to supported websites."""
    return [
        "https://www.adelphi.it/",
        "https://www.buecher.de/",
        "https://www.lafeltrinelli.it/",
        "https://www.hoepli.it/",
        "https://www.hugendubel.de/",
        "https://www.ibs.it/",
        "https://www.librerie.coop/",
        "https://www.libraccio.it/",
        "https://www.libreriauniversitaria.it/",
        "https://www.mondadoristore.it/",
        "https://books.mondadoristore.it/",
        "https://www.osiander.de/",
        "https://www.libreriarizzoli.it/",
    ]


def scrape_url(url):
    """Read url and redirect to specialized scraping function."""
    if not any([website in url for website in list_sites_links()]):
        raise ValueError("Website not supported.")

    if "adelphi.it" in url:
        return scrape_adelphi(url)
    if "buecher" in url:
        return scrape_buecher(url)
    if "feltrinelli" in url or "ibs" in url:
        return scrape_feltrinelli_and_ibs(url)
    if "hoepli" in url:
        return scrape_hoepli(url)
    if "hugendubel" in url:
        return scrape_hugendubel(url)
    if "librerie.coop" in url:
        return scrape_libcoop(url)
    if "libraccio" in url:
        return scrape_libraccio(url)
    if "libreriauniversitaria" in url:
        return scrape_libuni(url)
    if "mondadori" in url:
        return scrape_mondadori(url)
    if "osiander" in url:
        return scrape_osiander(url)
    if "rizzoli" in url:
        return scrape_rizzoli(url)


def scrape_adelphi(url):
    """Scrape price from adelphi.it."""
    with requests.get(url, timeout=30) as res:
        soup = BeautifulSoup(res.content, "lxml")
    try:
        price = soup.find("div", {"class", "book-impressum-price"}).find(
            "span", {"class", "sale"}
        )
    except AttributeError:
        return
    if price is not None:
        return clean_up_price(price.text.strip())


def scrape_buecher(url):
    """Scrape price from buecher.de."""
    with requests.get(url, timeout=30) as res:
        soup = BeautifulSoup(res.content, "lxml")
    price = soup.find("div", {"class", "clearfix price-shipping-free"})
    if price is not None:
        return clean_up_price(price.text.strip())


def scrape_feltrinelli_and_ibs(url):
    """Scrape price from lafeltrinelli.it and ibs.it."""
    with requests.get(url, timeout=30) as res:
        soup = BeautifulSoup(res.content, "lxml")
    title_label = soup.find("span", {"cc-top-title-label"})
    if title_label is None or title_label.text == "LIBRO USATO":
        return
    try:
        price = (
            soup.find("div", {"class": "cc-pdp-main"})
            .find("div", {"class": "cc-content-price"})
            .find("span", {"class": "cc-price"})
        )
    except AttributeError:
        return
    if price is not None:
        return clean_up_price(price.text.strip())


def scrape_hoepli(url):
    """Scrape price from hoepli.it."""
    with requests.get(url, headers=headers, timeout=30) as res:
        soup = BeautifulSoup(res.content, "lxml")
    non_disponibile = soup.find("span", {"class", "disponibilita_Z"})
    if non_disponibile is not None and "Non disponibile" in non_disponibile.text:
        return
    price = soup.find("div", {"class", "prezzo"})
    price = price.find("span")
    if price is not None:
        return clean_up_price(price.text)


def scrape_hugendubel(url):
    """Scrape price from hugendubel.de."""
    with requests.get(url, timeout=30) as res:
        soup = BeautifulSoup(res.content, "lxml")
    price = soup.find("div", {"class", "current-price"})
    price = price.find("span", {"class", "price"})
    if price is not None:
        return clean_up_price(price.text)


def scrape_libcoop(url):
    """Scrape price from librerie.coop."""
    with requests.get(url, headers=headers, timeout=30) as res:
        soup = BeautifulSoup(res.content, "lxml")
    btn_disabled = soup.find("button", {"class", "btn btn-disabled"})
    btn_disabled_2 = soup.find("button", {"class", "btn btn-disabled mt-2"})
    if btn_disabled or btn_disabled_2:
        msg = btn_disabled if btn_disabled else btn_disabled_2
        if "NON DISPONIBILE" in msg.text:
            return
    price = soup.find("span", {"class", "current-price"})
    if price is not None:
        return clean_up_price(price.text)


def scrape_libraccio(url):
    """Scrape price from libraccio.it."""
    with requests.get(url, timeout=30) as res:
        soup = BeautifulSoup(res.content, "lxml")
    try:
        price = soup.find("div", {"class": "buybox"}).find(
            "span", {"class": "currentprice"}
        )
    except AttributeError:
        return
    if price is not None:
        return clean_up_price(price.text.strip())


def scrape_libuni(url):
    """Scrape price from libreriauniversitaria.it."""
    with requests.get(url, timeout=30) as res:
        soup = BeautifulSoup(res.content, "lxml")
    if "Prodotto momentaneamente non disponibile" in soup.text:
        return
    if "Fuori catalogo" in soup.text:
        return
    price = soup.find("span", {"class", "current-price"})
    if price is not None:
        return clean_up_price(price.text.strip())


def scrape_mondadori(url):
    """Scrape price from mondadoristore.it."""
    with requests.get(url, headers=headers, timeout=30) as res:
        soup = BeautifulSoup(res.content, "lxml")
    price = soup.find("span", {"class", "new-price new-detail-price"})
    if price is not None:
        return clean_up_price(price.text)


def scrape_osiander(url):
    """Scrape price from osiander.de."""
    with webdriver.Firefox(options=firefox_options) as driver:
        driver.get(url)
        li = driver.find_elements(By.CLASS_NAME, "streichpreisdarstellung")
        if len(li) > 0:  # a discount on the book is found
            price = li[0].text.splitlines()[0]
            return clean_up_price(price)
        else:  # book not on discount
            prices = [
                ee.text.splitlines()[0]
                for ee in driver.find_elements(By.CLASS_NAME, "element-headline-medium")
                if len(ee.text) > 0
                if "€" in ee.text
            ]
            if len(prices) > 0:
                return clean_up_price(prices[0])
            else:
                # TODO: Add log for failed scrape
                return


def scrape_rizzoli(url):
    """Scrape price from libreriarizzoli.it."""
    with requests.get(url, headers=headers, timeout=30) as res:
        soup = BeautifulSoup(res.content, "lxml")
    price = soup.find("span", {"class", "price-value"})
    if price is not None:
        return clean_up_price(price.text)


def clean_up_price(ss):
    """Clean up price into float.

    :param ss: price string, containing possibly symbols.
    :type ss: str
    :returns: price float
    :rtype: float
    """
    if len(ss) > 0:
        return float(
            ss.replace("\n", "")
            .replace("\xa0", "")
            .replace("€", "")
            .replace(",", ".")
            .strip()
        )
