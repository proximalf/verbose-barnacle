from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional, Tuple

from matplotlib import ticker
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
from PySide6.QtWidgets import QWidget
import numpy as np

from qtcomponents.plot import MatplotlibWidget
from .lib import find_plot_limits

class TimeSeriesPlotComponent:
    """
    A component that displays a time series plot, only has one data line, it is recommended to either inherit or copy and paste this class.

    x-axis: timedelta
        As timedelta from start time.
    y-axis: float
        Data
    """

    def __init__(self, parent: QWidget) -> None:
        self.widget = MatplotlibWidget(parent)
        self.start_time: Optional[datetime] = None
        
        self._resize_plot = False # this gets set to true when the timestamps need realigning.
        self._update_plot_limits = False

        self.timestamps: List[float] = []
        self.data: List[float] = []
        
        self.initialise_plot()

    def initialise_plot(self) -> None:
        """
        Initialises the plot with an axes.
        """

        figure = Figure()
        axes = figure.add_subplot(111)

        self.axes = axes
        self.widget.figure = figure

        self.data_line = Line2D([0], [0])

        self.axes.add_line(self.data_line)
        
        formatter = ticker.FuncFormatter(self.format_time_ticks)
        self.axes.xaxis.set_major_formatter(formatter)

        figure.tight_layout()
        self.draw()
    
    def format_time_ticks(self, x: float, pos: int) -> str:
        """
        Format the timestamp into a string for display on the x axis.
        """
        if self.start_time and self._update_plot_limits and pos != 0:

            d = datetime.fromtimestamp(x, tz=timezone.utc)

            if d.day > 1:
                return d.strftime("%d %H:%M:%S")

            if d.hour > 0:
                return d.strftime("%H:%M:%S")

            if d.minute > 0:
                return d.strftime("%M:%S")

            if d.second > 0:
                return d.strftime("%S")

            return d.strftime("%S")

        if self.start_time and pos == 0:
            return self.start_time.strftime("%H:%M:%S")
        return ""

    def update_plot(self, data: float) -> None:
        """
        Update the plotting lines.

        new_data: 

        """
        now = datetime.now()

        if self.start_time is None:
            self.start_time = now

        self.timestamps.append((now - self.start_time).total_seconds())

        self.data.append(data)

        # X
        self.data_line.set_xdata(self.timestamps)  # type: ignore

        self.update_plot_limits()

        self.draw()
   
    def update_plot_limits(self) -> None:
        """
        If there isn't enough stored data points, the the plot will not be updated.
        """
        if not self._update_plot_limits:
            # Just want to calculate the lengths of arrays if there is not enough data, 
            # otherwise it is okay to assume there is enough points to set the limits.
            if (len(self.timestamps) > 2 and len(self.data) > 2):
                self._update_plot_limits = True

        if self._update_plot_limits:
            x_lims = self.timestamps[0], self.timestamps[-1]
            self.axes.set_xlim(*x_lims)
        
            self.axes.set_ylim(find_plot_limits(self.data))

    def draw(self) -> None:
        if self._resize_plot and self.widget.figure:
            self.widget.figure.tight_layout()
            self._resize_plot = False
        self.widget.draw()

    def clear(self) -> None:
        """
        Clear the plot of all data.
        """
        self._update_plot_limits = False
        self.timestamps = []
        self.start_time = None
        self.draw()

def run_once(f):
    """
    Decorator for only running a function once.
    """
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            wrapper.has_run = True
            return f(*args, **kwargs)
    wrapper.has_run = False
    return wrapper


def format_timestamp_into_timestring(timestamp: float) -> str:
    d = datetime.fromtimestamp(timestamp, tz=timezone.utc)

    if d.day > 1:
        return d.strftime("%d %H:%M:%S")

    if d.hour > 0:
        return d.strftime("%H:%M:%S")

    if d.minute > 0:
        return d.strftime("%M:%S")

    if d.second > 0:
        return d.strftime("%S").lstrip("0") # silly but strips the leading zero.
    
    return ""