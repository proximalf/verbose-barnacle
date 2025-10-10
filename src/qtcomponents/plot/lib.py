from datetime import timedelta
from pathlib import Path
from typing import List, Tuple

import numpy as np
from matplotlib.figure import Figure


def save_figure_fixed_size(path: Path, figure: Figure, width: float = 8.3, height: float = 5.8, dpi: int = 300) -> None:
    """
    Save a Matplotlib figure with fixed size, regardless of how it appears in a GUI.
    A5 8.3x5.8
    """
    original_size = figure.get_size_inches()  # get original size

    figure.set_size_inches(width, height)  # set fixed size in inches

    figure.tight_layout()  # set to tight after resizing

    figure.savefig(path, dpi=dpi, bbox_inches="tight")

    figure.set_size_inches(*original_size)  # reset plot


def convert_timestamp_to_string(timestamp: float) -> str:
    """
    Converts a datetime timestamp to a string for use on a plot x axis.

    Returns
    ---------
    "%H:%M:%S" or if delta is greater than a day "%dd %H:%M:%S"

    """
    td = timedelta(seconds=timestamp)

    days = td.days
    hours, remainder = divmod(td.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    if days > 0:
        return f"{days}d {hours:02}:{minutes:02}:{seconds:02}"

    return f"{hours:02}:{minutes:02}:{seconds:02}"


def find_plot_limits(data: np.ndarray | List, pad: float = 0.2) -> Tuple[float, float]:
    """
    Find the bottom and top limits of a data set. If data has a negative value then the pad is adjusted.

    Returns
    ----------
    bottom, top
    """
    bottom = min(data)
    top = max(data)

    bottom *= (1 + pad) if bottom < 0 else (1 - pad)
    top *= (1 - pad) if top < 0 else (1 + pad)

    return bottom, top
