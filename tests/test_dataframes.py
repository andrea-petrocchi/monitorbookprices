"""Test functions related to dataframes, databases, etc."""

from pathlib import Path

import polars as pl
import pytest
from polars.testing import assert_frame_equal

import monitorbookprices as mbp


def get_simple_df():
    """Create simple dataframe."""
    book = mbp.new_book(
        {
            'isbn': '9783866473256',
            'author': 'Karl Marx',
            'title': 'Das Kapital',
            'year': '2009',
            'publisher': 'Anaconda',
            'full_price': 7.95,
            'buecher': 'https://www.buecher.de/artikel/buch/das-kapital/25646129/',
            'osiander': 'https://www.osiander.de/shop/home/artikeldetails/A1006759980',
        }
    )
    df = pl.DataFrame(book, schema_overrides=mbp.schema())
    return df


def test_sqldb():
    """Test SQL databases."""
    df_1 = get_simple_df()
    sqldb_path = Path(__file__).parent/'data/test_dataframes/database.db'
    df_2 = mbp.read_database(
        table_name='books',
        url=f'sqlite:///{sqldb_path}',
        schema=mbp.schema(),
    )
    assert_frame_equal(df_1, df_2)


def test_excel():
    """Test excel files."""
    df_1 = get_simple_df()
    sqlexcel_path = Path(__file__).parent/'data/test_dataframes/database.xlsx'
    df_2 = mbp.read_excel(
        sqlexcel_path,
        schema=mbp.schema()
    )
    assert_frame_equal(df_1, df_2)
