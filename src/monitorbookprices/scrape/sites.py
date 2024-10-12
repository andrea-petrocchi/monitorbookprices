"""Extract prices."""

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

firefox_options = Options()
firefox_options.add_argument('--headless')  # Run in headless mode
firefox_service = Service()


def list_sites():
    """Return names of supported websites."""
    return [
        'adelphi',
        'buecher',
        'feltrinelli',
        'ibs',
        'libraccio',
        'mondadori',
        'osiander',
    ]


def list_sites_links():
    """Return links to supported websites."""
    return [
        'https://www.adelphi.it/',
        'https://www.buecher.de/',
        'https://www.lafeltrinelli.it/',
        'https://www.ibs.it/',
        'https://www.libraccio.it/',
        'https://www.mondadoristore.it/',
        'https://books.mondadoristore.it/',
        'https://www.osiander.de/',
    ]


def scrape_url(url):
    """Read url and redirect to specialized scraping function."""
    if not any([website in url for website in list_sites_links()]):
        raise ValueError('Website not supported.')

    if 'adelphi.it' in url:
        return scrape_adelphi(url)
    if 'buecher' in url:
        return scrape_buecher(url)
    if 'feltrinelli' in url or 'ibs' in url:
        return scrape_feltrinelli_and_ibs(url)
    if 'libraccio' in url:
        return scrape_libraccio(url)
    if 'mondadori' in url:
        return scrape_mondadori(url)
    if 'osiander' in url:
        return scrape_osiander(url)


def scrape_adelphi(url):
    """Scraping function for adelphi.it."""
    res = requests.get(url, timeout=10)
    soup = BeautifulSoup(res.content, 'lxml')
    content = soup.find('div', {'class', 'book-impressum-price'})
    price = content.find('span', {'class', 'sale'})
    out = clean_up_price(price.text.strip())
    return out


def scrape_buecher(url):
    """Scraping function for buecher.de."""
    res = requests.get(url, timeout=10)
    soup = BeautifulSoup(res.content, 'lxml')
    price = soup.find('div', {'class', 'clearfix price-shipping-free'})
    out = clean_up_price(price.text.strip())
    return out


def scrape_feltrinelli_and_ibs(url):
    """Scraping function for lafeltrinelli.it and ibs.it."""
    res = requests.get(url, timeout=10)
    soup = BeautifulSoup(res.content, 'lxml')
    main_box = soup.find('div', {'class': 'cc-pdp-main'})
    content = main_box.find('div', {'class': 'cc-content-price'})
    price = content.find('span', {'class': 'cc-price'})
    out = clean_up_price(price.text.strip())
    return out


def scrape_libraccio(url):
    """Scraping function for libraccio.it."""
    res = requests.get(url, timeout=10)
    soup = BeautifulSoup(res.content, 'lxml')
    main_content = soup.find('div', {'class': 'maincontent'})
    price = main_content.find('span', {'class': 'currentprice'})
    out = clean_up_price(price.text.strip())
    return out


def scrape_mondadori(url):
    """Scraping function for mondadoristore.it."""
    res = requests.get(url, timeout=10)
    soup = BeautifulSoup(res.content, 'lxml')
    price = soup.find('span', {'class', 'new-price new-detail-price'})
    out = clean_up_price(price.text)
    return out


def scrape_osiander(url):
    """Scraping function for osiander.de."""
    try:
        driver = webdriver.Firefox(
            # service=Service('./geckodriver'),
            # executable_path='./geckodriver',
            options=firefox_options
        )
        driver.get(url)
        try:
            price = driver.find_element(
                By.CLASS_NAME, 'streichpreisdarstellung'
            ).text.splitlines()[0]
        except NoSuchElementException:
            price = [
                ee.text.splitlines()[0]
                for ee in driver.find_elements(
                    By.CLASS_NAME, 'element-headline-medium'
                )
                if '€' in ee.text
            ][0]
        driver.quit()
        return clean_up_price(price)
    except NoSuchElementException:
        return


def clean_up_price(ss):
    """Clean up price into float.

    :param ss: price string, containing possibly symbols.
    :type ss: str
    :returns: price float
    :rtype: float
    """
    return float(
        ss.replace('\n', '')
        .replace('\xa0', '')
        .replace('€', '')
        .replace(',', '.')
        .strip()
    )
