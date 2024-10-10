"""Data - Excel functions."""

import polars as pl


def write_excel(
    df,
    fname,
):
    """Write `DataFrame` to `xlsx` file."""
    df.write_excel(fname)


def read_excel(fname, schema=None):
    """Load dataframe from template."""
    return pl.read_excel(
        source=fname,
        schema_overrides=schema,
    )
