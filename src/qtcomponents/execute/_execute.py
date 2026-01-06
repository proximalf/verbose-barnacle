from typing import Callable, Iterator
from pathlib import Path
try:
    import click
except ImportError:
    raise

from PySide6.QtWidgets import QWidget, QApplication
import importlib
import sys

from .lib import load_widget_as_entrypoint, resolve_enum, find_project_root

@click.command()
@click.option("-w", "--widget", "widget_path", default=None)
@click.option("-e", "--enum", "enum_path", default=None)
@click.option("-R", "--raise", "raise_on_error", default = False, is_flag=True)
def main(widget_path: str | None, enum_path: str | None, raise_on_error: bool = False) -> None:
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
        raise SystemExit(
            "Instances the widget directly."
            "Usage: qtcomponent -w qtcomponents.table:DataTable"
        )

    try:
        # Add the project to path.
        root = find_project_root()
        sys.path.insert(0, str(root))
    except:
        print("Failed to find module pyproject file.")

    try:
        entry = load_widget_as_entrypoint(widget_path)
    except ModuleNotFoundError as ex:
        print(f"Failed to load module - Error: {ex}")
        if raise_on_error:
            raise
        return
    except:
        print("Failed to find module.")
        raise

    enum = None if enum_path is None else resolve_enum(enum_path)

    QT_APP = QApplication.instance()
    if QT_APP is None:
        QT_APP = QApplication(sys.argv)

    try:
        widget: QWidget = entry() if enum is None else entry(enum)
        widget.show()
    except:
        print(f"Failed to run widget - {widget}")
        raise
    
    exit_code = QT_APP.exec()
    sys.exit(exit_code)
    

if __name__ == "__main__":

    main()
