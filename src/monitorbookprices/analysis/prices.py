"""Prices functions."""

import polars as pl
from monitorbookprices.book.general import schema as get_schema_default
from monitorbookprices.data.database import read_database, write_database


def update_min(books_df, prices_df):
    """Update min in table books."""
    mapping = {}
    for book in books_df.iter_slices(1):
        isbn = book['isbn'][0]
        prs = prices_df.filter(pl.col('isbn') == isbn)
        mm = prs.min()['price'][0]
        min_price = book['min_price'][0]
        if mm is None:
            # list_min_price.append(min_price)
            mapping[isbn] = min_price
        elif min_price is None:
            # list_min_price.append(mm)
            mapping[isbn] = mm
        elif mm < min_price:
            # list_min_price.append(mm)
            mapping[isbn] = mm
        elif min_price <= mm:
            # list_min_price.append(min_price)
            mapping[isbn] = min_price
        else:
            print('What?')
    return books_df.with_columns(
        min_price=pl.col('isbn').replace_strict(mapping)
    )


def update_min_whole_database(
    books_table='books',
    prices_table='prices',
    engine=None,
    url=None,
):
    """Update min_price in database.

    Updates value `min_price` in the table specified by `books_table` with the
    minimum of all prices registered in the table specified by `prices_table`.
    """
    books = read_database(
        table_name=books_table,
        engine=engine,
        url=url,
        schema=get_schema_default(),
    )
    prices = read_database(
        table_name=prices_table,
        engine=engine,
        url=url,
        schema=get_schema_default(),
    )
    b2 = update_min(books, prices)
    write_database(
        b2,
        table_name=books_table,
        engine=engine,
        url=url,
        if_table_exists='replace',
    )
