"""Book functions."""

from pathlib import Path

import polars as pl

import monitorbookprices as mbp


def create_excel_template(
    fname=Path('template.xlsx').absolute(),
):
    """Create template for adding new books."""
    df = pl.DataFrame(schema=schema)
    df.write_excel(fname)


def new_book(book):
    """Check new book entries.

    Parameters
    ----------
    book: dict
        Book dictionary.
    """
    if 'isbn' not in book or len(book['isbn']) != 13:
        raise ValueError('ISBN missing or wrong format.')
    book = fill_book_schema(**book)
    return book


def fill_book_schema(**kwargs):
    """Fill book's schema with `None`s."""
    book_schema = dict.fromkeys(schema())
    return {**book_schema, **kwargs}


def schema():
    """Return supported schema."""
    out = {
        'isbn': pl.String,
        'author': pl.String,
        'title': pl.String,
        'year': pl.String,
        'publisher': pl.String,
        'full_price': pl.Float64,
    }
    for site in mbp.list_sites():
        out[site] = pl.String
    return out