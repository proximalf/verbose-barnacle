# QtComponents
A collection of qt components that I've used in a few projects, rather than copying across projects, I've complied them into this small lib.

Component is a Python object that holds reference to a widget, with some convience methods. If it doesn't inherit `QWidget` then the component should have a widget attribute that can be inserted into a layout.

Uses uv package manager. 
Add using uv `uv add git+https://github.com/proximalf/verbose-barnacle` or add to pyproject:
```toml
[tool.uv.sources]
qtcomponents = { git = "https://github.com/proximalf/verbose-barnacle" }
```

## Components / Widgets

### FileDialog
This is useful for simply instancing a `FileDialog`, after a file has been choosen, the resulting path is converted to a `Path` object.


Methods:
- FileDialog.open() -> Path
For opening a single file or directory.
- FileDialog.opens() -> List[Path]
For opening multiple files or directories.
- FileDialog.save() -> Path
For selecting a path to save to.

The file filter is a little bit confusing. It is effectively a dict, with the description and then suffix of a given filetype. Flexible, but not immediately useful. Remember to include the `.` on the suffix.

Filter Example:
```python
filepath = FileDialog.save(
    ...,
    filter={
        "Bitmap (*.bmp)": ".bmp",
        "JPEG (*.jpg)" : ".jpg",
        # "description" : "suffix"
        ...
    },
)
```

### Plot
The `MatplotlibWidget` instantiates a `Canvas` and `Figure` that can be used to display a plot within as a `QWidget`. Requires that the OOP mpl be used, rather than relying on the `pyplot` part.
Must call `MatplotlibWidget.draw()` when ever the plot updates.

Calling `set_data` on the line object, updates the plot.

Example:
This example is a trimmed down snippet from a TimeSeries plot, which is tracking voltage. Timestamps used are just floating points, and a function converts from float to a datetime string to add to the plot.
```python
figure = matplotlib_widget.figure
axes = figure.add_subplot(111)

# Create lines for plot.
measured_voltage_line = Line2D([0], [0], label="Measured Voltage (V)",
)
axes.add_line(measured_voltage_line)

# Loop this.
now = datetime.now()
timestamps.append((now - start_time).total_seconds())
# X
measured_voltage_line.set_xdata(timestamps)
# Y
measured_voltage_line.set_ydata(measured_voltage_data)
matplotlib_widget.draw()
```

### Serial
Two widgets for serial connections. `SerialConnectionWidget` and `SerialCommandWidget`. 
`SerialConnectionWidget` is just a widget wrapping a `QPushButton` and `QComboBox` for connecting to a serial device via the choosen port.
`SerialCommandWidget` is used to send commands to a serial interface, for debugging or intentional use.

### Log
`LoggingComponent` holds reference to a logging handler that emits its messages to a text edit widget. Remember to attach handler to internal logging, and to insert the widget into what ever parent.


## Function
### `show_error_dialog`
This will spawn a simple error dialog with some traceback info, if an exception is passed.