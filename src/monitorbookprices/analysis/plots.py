"""Functions for plotting."""

import holoviews as hv
import hvplot.polars  # noqa: F401
import polars as pl

hv.extension('bokeh')


def plot_history(
    df,
    site=None,
    title=None,
    book=None,
    height=300,
    width=800,
    hlines=None,
):
    """Plot history of recent price recordings."""
    if site is not None:
        df = df.filter(pl.col('site') == site)
    plot_title = (
        title
        if title is not None
        else None
        if book is None
        else f"{book['isbn'][0]}: {book['author'][0]} - {book['title'][0]}. {book['publisher'][0]} ({book['year'][0]})"
    )
    plo = df.hvplot.line(
        x='date',
        y='price',
        by='site',
        title=plot_title,
        height=height,
        width=width,
        rot=90,
    )

    if hlines is not None:
        for hline in hlines:
            if type(hline) is str:
                if book is None:
                    raise ValueError('Book row not defined.')
                if hline == 'min':
                    plo *= horizontal_line(
                        df['date'].min(),
                        df['date'].max(),
                        book['min_price'][0],
                        label='min',
                        # line_width=0.6,
                        line_dash='dashed',
                    )
                if hline in ['max', 'full']:
                    plo *= horizontal_line(
                        df['date'].min(),
                        df['date'].max(),
                        book['full_price'][0],
                        label='max',
                        # line_width=0.6,
                        line_dash='dashed',
                    )
            if type(hline) is dict:
                try:
                    plo *= horizontal_line(
                        hline['X_A'], hline['X_B'], hline['Y'], hline['label']
                    )
                except ValueError:
                    raise ValueError('Wrong format hline.')
    return plo


def horizontal_line(X_A, X_B, Y, label=None, line_width=1, line_dash='solid'):
    """Horizontal line with label using holoviews Curve."""
    return hv.Curve(
        [[X_A, Y], [X_B, Y]],
        label=label,
    ).opts(
        line_width=line_width,
        line_dash=line_dash,
    )
