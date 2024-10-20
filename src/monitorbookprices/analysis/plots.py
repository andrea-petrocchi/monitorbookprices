"""Functions for plotting."""

import holoviews as hv
import hvplot.polars
import polars as pl


def plot_history(
    df,
    site=None,
    title=None,
    height=300,
    width=800,
    hline=None,
):
    """Plot history of recent price recordings."""
    if site is not None:
        df = df.filter(pl.col('site')==site)
    plo = df.hvplot.line(
        x="date",
        y="price",
        by='site',
        title=title,
        height=height,
        width=width,
        rot=90,
    )
    if hline is not None:
        line = hv.HLine(hline)
        line.opts(
            color='black',
            line_dash='dashed',
            line_width=0.5,
        )
        plo *= line
    return plo

