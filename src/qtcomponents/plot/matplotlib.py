from pathlib import Path
from typing import Optional

from matplotlib.backends.backend_qt import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PySide6.QtWidgets import QVBoxLayout, QWidget


class MatplotlibWidget(QWidget):
    """
    Matplotlib figure as a QWidget. Toolbar is set with initialisation flag.
    Can either set the figure or call the method `add_figure`.
    whenever the plot needs to update, call `draw`.
    `save` is avalible out of convience.

    Best to use the non-pyplot version of mpl.

    Example
    ----------
    fig = plot_widget.add_figure()
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    axes = fig.add_subplot(111)
    axes.axis("off")

    line = Line2D([0], [0])
    axes.add_line(line)

    # loop for live changes
    line.set_xdata(x_data)
    line.set_ydata(y_data)
    axes.set_xlim(x_data[0], x_data[-1])
    axes.set_ylim(min(y_data)*0.8, max(y_data)*1.2) # some padding
    plot_widget.draw()
    """

    def __init__(self, parent=None, toolbar: bool = True, dpi=100, *args, **kwargs) -> None:
        super().__init__(parent=parent, *args, **kwargs)
        self.dpi = dpi
        self._figure: Optional[Figure] = None
        self.vbox = QVBoxLayout()
        self.setLayout(self.vbox)
        self.vbox.setContentsMargins(0, 0, 0, 0)
        self.vbox.setSpacing(0)
        
        self.canvas = FigureCanvas()

        if toolbar:
            self.toolbar = NavigationToolbar(self.canvas, self)
            self.vbox.addWidget(self.toolbar)

        self.vbox.addWidget(self.canvas)

    @property
    def figure(self) -> Optional[Figure]:
        return self._figure

    @figure.setter
    def figure(self, figure: Figure) -> None:
        self._figure = figure
        figure.set_canvas(self.canvas)
        self.canvas.figure = self._figure

    def add_figure(self) -> Figure:
        figure = Figure()
        self.figure = figure
        return figure

    def draw(self) -> None:
        if self.canvas is not None:
            self.canvas.draw_idle()

    def save(self, path: Path, file_format: str = "png", dpi: Optional[int] = None) -> None:
        """
        Save the rendered figure. Will save a figure with the excess whitespace trimmed.
        """
        if self.figure is None:
            raise Exception("Cannot save if there is no figure.")
        # Setting the bbox to tight recalculates dimensions, removing the whitespace padding from being a widget.
        self.figure.savefig(path, format=file_format, bbox_inches="tight", dpi="figure" if dpi is None else dpi)
