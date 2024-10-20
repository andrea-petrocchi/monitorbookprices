"""Data - Database functions."""

import polars as pl
from monitorbookprices.book.general import schema as get_schema_default
from sqlalchemy import create_engine


def read_database(
    engine=None,
    query=None,
    schema=get_schema_default(),
    table_name=None,
    url=None,
):
    """Read database.

    Read database from URL or from an `sqlalchemy.engine.Engine` object.
    At least one between `engine` and `url` must be user-defined.
    If both are, the engine has the priority.

    Parameters
    ----------
    engine: :class:`sqlalchemy.engine.Engine`, optional
        Engine object providing the connection to the database.
    schema: dict, optional.
        Override schema with dictionary of column : `polars` type.
    url: str, optional
        Database url.

    Returns
    -------
    :class:`polars.DataFrame`
        Database as a :class:`polars.DataFrame`.

    Raises
    ------
    AttributeError
        If neither `engine` nor `url` are user-defined.

    """
    if engine is None:
        if url is None:
            raise ValueError(
                'Either `engine` or `url` has to be user-defined.'
            )
        else:
            engine = create_engine(url)
    if query is None:
        if table_name is None:
            raise ValueError(
                'Either `query` or `table_name` has to be user-defined.'
            )
        query = f'SELECT * FROM {table_name}'  # noqa: S608
    return pl.read_database(
        query=query,
        connection=engine,
        schema_overrides=schema,
    )


def write_database(
    df,
    table_name,
    engine=None,
    url=None,
    if_table_exists='append',
    modify_df_before_writing=None,
):
    """Write database.

    Save :class:`polars.DataFrame` as database specified in the URL or
    `sqlalchemy.engine.Engine` object.
    At least one between `engine` and `url` must be user-defined.
    If both are, the engine has the priority.

    Parameters
    ----------
    df: :class:`polars.DataFrame`
        DataFrame to be stored.
    table_name: str
        Name of table to use in the database.
    engine: :class:`sqlalchemy.engine.Engine`, default=`None`
        Engine object providing the connection to the database.
    url: str, default=`None`
        Database url.
    if_table_exists: {'append', 'replace', 'fail'}, default='append'
        Specifies behavior for already existing tables. See
        the `polars.DataFrame.write_database <https://docs.pola.rs/api/python/stable/reference/api/polars.DataFrame.write_database.html#polars.DataFrame.write_database>`_
        options for more details.
    modify_df_before_writing: function
        Function to apply before writing to database.

    Raises
    ------
    AttributeError
        If neither `engine` nor `url` are user-defined.

    """
    if engine is None:
        if url is None:
            raise ValueError(
                'Either `engine` or `url` has to be user-defined.'
            )
        else:
            engine = create_engine(url)
    if modify_df_before_writing is not None:
        df = modify_df_before_writing(
            df=df,
            engine=engine,
            table_name=table_name,
        )
    df.write_database(
        table_name=table_name,
        connection=engine,
        if_table_exists=if_table_exists,
    )


def delete_known_books(
    df,
    df_db=None,
    table_name='books',
    engine=None,
    url=None,
):
    """Delete known books."""
    if df_db is None:
        df_db = read_database(
            query=f'SELECT isbn FROM {table_name}',  # noqa: S608
            engine=engine,
            url=url,
        )
    return df.join(
        df_db,
        on='isbn',
        how='anti',
    )
