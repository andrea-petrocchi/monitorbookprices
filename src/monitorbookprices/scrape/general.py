"""Functions to update prices of a database."""

from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

import polars as pl
from monitorbookprices.scrape.sites import (
    list_sites,
    list_sites_links_short,
    scrape_url,
)
from tqdm import tqdm


def scrape_database(books_df, date=datetime.today().date(), parallel=True):
    """Scrape database."""
    list_isbn, list_link = prepare_scrape(books_df)
    list_price = scrape_list(list_link, parallel=parallel)
    list_site = from_list_link_to_list_site(list_link)
    list_date = [date] * len(list_price)
    return pl.DataFrame(
        {
            'isbn': list_isbn,
            'site': list_site,
            'price': list_price,
            'date': list_date,
        }
    )


def prepare_scrape(books_df):
    """Prepare scrape."""
    list_isbn = []
    list_site = []
    for book in books_df.iter_slices(1):
        list_site_i = book.select(pl.col(list_sites()))[
            [s.name for s in book[list_sites()] if not s.null_count()]
        ]
        if list_site_i.shape[0] > 0:
            for site in list_site_i:
                list_isbn.append(book['isbn'][0])
                list_site.append(site[0])
    return list_isbn, list_site


def scrape_list(list_site, parallel=True):
    """Scrape list of sites."""
    if parallel:
        with ThreadPoolExecutor() as executor:
            list_price = list(
                tqdm(executor.map(scrape_url, list_site), total=len(list_site))
            )
    else:
        list_price = []
        for site in tqdm(list_site):
            list_price.append(scrape_url(site))
    return list_price


def from_list_link_to_list_site(list_link):
    """Derive `list_site` from `list_link`."""
    dd = dict(zip(list_sites_links_short(), list_sites()))
    list_site = []
    for link in list_link:
        for sl in dd.keys():
            if sl in link:
                list_site.append(dd[sl])
                break
    return list_site
