from click import Context
from enum import Enum
from pathlib import Path
from typing import Callable, Iterator, Dict, List

try:
    import click
    from click import echo
except ImportError:
    raise

import sys

from PySide6.QtWidgets import QApplication, QWidget

from .lib import (
    find_project_root,
    load_function_entry_point,
    load_widget_as_entrypoint,
    resolve_enum,
)


@click.command(
    name="qtcomponent-execute",
    context_settings=dict(
        ignore_unknown_options=True,
        allow_extra_args=True,
    )
)
@click.option("-w", "--widget", "widget_path", default=None)
@click.option("-e", "--enum", "enum_path", default=None)
@click.option("-R", "--raise", "raise_on_error", default=False, is_flag=True)
@click.option("-D", "--default", "default_behaviour", default=False, is_flag=True)
@click.argument("addtional_options", nargs=-1, type=click.UNPROCESSED)
def main(
    widget_path: str | None, enum_path: str | None, raise_on_error: bool = False, default_behaviour: bool = False, addtional_options: List[str] | None = None,
) -> None:
    """
    A cli interface for executing a given QWidget from an entry point, or object returns a widget.

    Usage
    -----
    `qtcomponent -w qtcomponents.table:DataTable`
    `qtcomponent -w test.test_widgets:test_event`

    Parameters
    ----------
    widget_path: str
        Example: `qtcomponents.table:DataTable`
    enum_path: str
        Example: `module:Enum.Value`
    raise_on_error: bool
        Print Exception traceback rather than print an error message when trying to load entrypoint.
    default_behaviour: bool
        Set flag to force default behaviour, used when environment has a custom plugin entrypoint.
    addtional_options: str
        A list of raw strs, any addtional options that are passed to plugin.
        Example: ('--path', '~/image.png', '--pixel-size', '11.6')
        This is converted into a dict of pairs, '--' stripped, and passed as `**kwargs` to the plugin.
        kebab-case is converted to snake_case.
        (path='~/image.png', pixel_size='11.6')

    """
    if widget_path is None:
        raise SystemExit("Instances the widget directly." "Usage: qtcomponent -w qtcomponents.table:DataTable")

    try:
        # Add the project to path.
        root = find_project_root()
        sys.path.insert(0, str(root))
    except:
        echo("Failed to find module pyproject file.")

    try:
        entry = load_widget_as_entrypoint(widget_path)
    except ModuleNotFoundError as ex:
        echo(f"Failed to load module - Error: {ex}")
        if raise_on_error:
            raise
        return
    except:
        echo("Failed to find module.")
        raise

    enum = None if enum_path is None else resolve_enum(enum_path)

    plugin = load_function_entry_point()
    
    if addtional_options is not None: 
        echo(f"Addtional options passsed - {addtional_options}")
        try:
            if isinstance(addtional_options, tuple):
                options: Dict[str, str] = {}
                
                for i in addtional_options:
                    name, value = i.split("=")
                    n = name.lstrip("--").replace("-", "_") 
                    options[n] = value

                echo(f"Converted options - {options}")
            
        except:
            raise
    
    if plugin is None or default_behaviour:
        if isinstance(options, dict):
            default(widget_path, entry, enum, **options)
            return

        default(widget_path, entry, enum)
        return

    echo(f"Plugin entrypoint discovered - {plugin}")

    try:
        if isinstance(options, dict):
            plugin(entry, enum, **options)
            return
        
        plugin(entry, enum, addtional_options)
        return
        
    except:
        echo(f"Failed to run plugin - {plugin}")
        raise


def default(widget_path: str, entry: Callable[..., QWidget], enum: Enum | None, **kwargs) -> None:
    """
    Default operation of CLI app if no entrypoint is found.
    """
    QT_APP = QApplication.instance()
    if QT_APP is None:
        QT_APP = QApplication(sys.argv)

    try:

        widget: QWidget = entry(**kwargs) if enum is None else entry(enum)
        
        if widget is None:
            echo(f"Returned value was None.")
            return
        
        widget.show()
    
    except:
        echo(f"Failed to run widget - {widget_path}")
        raise

    exit_code = QT_APP.exec()
    sys.exit(exit_code)


if __name__ == "__main__":

    main()
