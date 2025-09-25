from pathlib import Path
from typing import Optional

from matplotlib.backends.backend_qt import \
    NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PySide6.QtWidgets import QVBoxLayout, QWidget


class MatplotlibWidget(QWidget):
    """
    Implements a Matplotlib figure inside a QWidget.
    Use figure() and draw() to interact with matplotlib.

    Example::

        mw = MatplotlibWidget()
        figure = Figure()
        axes = figure.add_subplot(111)
        ... # draw on axes
        mw.figure = figure
        mw.draw()
    """

    def __init__(
        self, parent=None, toolbar: bool = True, dpi=100, *args, **kwargs
    ) -> None:
        super(MatplotlibWidget, self).__init__(*args, **kwargs)
        self.canvas = None
        self._figure = None
        self.display_toolbar = toolbar
        self.dpi = dpi

    def add_figure(self) -> Figure:
        self._figure = Figure()
        return self._figure

    @property
    def figure(self) -> Optional[Figure]:
        return self._figure

    @figure.setter
    def figure(self, figure: Figure) -> None:
        self._figure = figure
        self.update_canvas()

    def update_canvas(self) -> None:
        if self._figure is None:
            raise AttributeError(f"Figure not initialised {self._figure}")
        self.vbox = QVBoxLayout()

        self.canvas = FigureCanvas(self._figure)
        self.canvas.setParent(self)

        if self.display_toolbar:
            self.toolbar = NavigationToolbar(self.canvas, self)
            self.vbox.addWidget(self.toolbar)

        self.vbox.addWidget(self.canvas)

        self.setLayout(self.vbox)

    def draw(self) -> None:
        if self.canvas is not None:
            self.canvas.draw_idle()

    def save(self, path: Path, file_format: str = "png") -> None:
        """
        Save the rendered figure. Will save a figure with the excess whitespace trimmed.
        """
        if not self.figure:
            raise Exception("Cannot save if there is no figure.")
        # Setting the bbox to tight takes the dimensions of the figure and trims whitespace.
        self.figure.savefig(path, format=file_format, bbox_inches="tight")
