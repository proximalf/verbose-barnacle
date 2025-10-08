
from pathlib import Path

from matplotlib.figure import Figure

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
