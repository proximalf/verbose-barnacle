# QtComponents
A collection of qt components that I've used in a few projects, rather than copying across projects, I've complied them into this small lib.

Uses uv package manager. 
Add using uv `uv add git+https://github.com/proximalf/verbose-barnacle` or add to pyproject:
```toml
[tool.uv.sources]
qtcomponents = { git = "https://github.com/proximalf/verbose-barnacle" }
```

## CLI App - `qtcomponent`
`pip install qtcomponents[cli]` <!-- REMINDER TO UPDATE WITH `UV ADD ...` FROM GIT I THINK IT IS THE SAME -->

A quick test utility for QtWidgets, initialises a QApplication instance if one doesn't already exist, that uses entrypoints to pass the desired object for display in a QApp.

This accepts two args `-w` & `-e`. (See [usage](#usage) for example)

### Widget `-w` 
Defines the entrypoint path to the desired widget / function.

### Enum `-e` 
Defines the entrypoint path for an enum, if you happen to use an enum alter the view of the widget. ie `Orientation.Vertical ...`

When passing either a Class that inherits `QWidget` or a function that returns the same.

### Raise `-R`
This will raise the traceback message if you entrypoint fails to load, the reason it is behind this is just due to it printing the traceback of `click` which can be a bit confusing.
Otherwise any exception that occurs will be returned, so they may not be much useful detail if your exception handling is poor.

### Usage:
```shell
qtcomponent -w qtcomponents.table:DataTable
qtcomponent -w test.test_widgets:test_event
# With Enum
qtcomponent -w operations:extension -e operations.menu:OperationAction.Threshold
```


### Entrypoints
Has support for overriding the default behaviour by creating an entrypoint.

I have a more complicated QtApp, creating widgets in code is way more mangable than QtCreator, and so I needed a quick means of checking them out.

Below is an example of defining the entrypoint. 
```toml
[project.entry-points."qtcomponents.function"]
function = "test.test_plugin:qtcomponent_plugin"
```

#### Plugin Function Signiture
It is possible to override the entry point process by using any function or class of choice, as this is passed in the `entry` variable, 
this would not really be in the spirit of this convenient app.


```python
def qtcomponent_plugin(entry: Callable[..., Any], enum: Enum) -> None:
    """
    Entry Point.

    Parameters
    ----------
    entry: Callable[..., Any] 
        Any object that would be returned from the arg passed to `-w`.
    
    enum: Enum
        Any Enum that would be returned from the arg passed to `-e`.
    """
```

It might be possible to use a watch program, to rerun on updates.


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

### ImageViewComponent
Relatively simple image view widget using a QGraphicsView. Accepts a numpy array, has to be integer dtype.

## Functions

### `show_error_dialog`
This will spawn a simple error dialog with some traceback info, if an exception is passed.
