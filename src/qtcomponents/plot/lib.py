
from pathlib import Path
from typing import List, Tuple

from matplotlib.figure import Figure
import numpy as np

def save_figure_fixed_size(path: Path, figure: Figure, width: float = 8.3, height: float = 5.8, dpi: int = 300) -> None:
    """
    Save a Matplotlib figure with fixed size, regardless of how it appears in a GUI.
    A5 8.3x5.8
    """
    original_size = figure.get_size_inches() # get original size

    figure.tight_layout()
    
    figure.set_size_inches(width, height) # set fixed size in inches
    
    figure.savefig(path, dpi=dpi, bbox_inches='tight')

    figure.set_size_inches(*original_size) # reset plot

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