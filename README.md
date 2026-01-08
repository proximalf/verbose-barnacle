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
This overides the default behaviour and can be used for effectively anything.


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
