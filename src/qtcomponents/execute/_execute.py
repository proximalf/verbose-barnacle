from enum import Enum
from pathlib import Path
from typing import Callable, Iterator

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


@click.command()
@click.option("-w", "--widget", "widget_path", default=None)
@click.option("-e", "--enum", "enum_path", default=None)
@click.option("-R", "--raise", "raise_on_error", default=False, is_flag=True)
@click.option("-D", "--default", "default_behaviour", default=False, is_flag=True)
def main(
    widget_path: str | None, enum_path: str | None, raise_on_error: bool = False, default_behaviour: bool = False
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
        ie: `qtcomponents.table:DataTable`
    enum_path: str
        ie: module:Enum.Value
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

    if plugin is None or default_behaviour:
        default(widget_path, entry, enum)
        return

    echo(f"Plugin entrypoint discovered - {plugin}")
    try:
        plugin(entry, enum)
    except:
        echo(f"Failed to run plugin - {plugin}")
        raise


def default(widget_path: str, entry: Callable[..., QWidget], enum: Enum | None) -> None:
    """
    Default operation of CLI app if no entrypoint is found.
    """
    QT_APP = QApplication.instance()
    if QT_APP is None:
        QT_APP = QApplication(sys.argv)

    try:
        widget: QWidget = entry() if enum is None else entry(enum)
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
