"""
This script enables testing of basic widgets

Two modes, widget mode, and function
both expect to be a widget

widget mode is just the class object itself, arranged so it can be displayed as such.

function mode, allows for a widget to be prepopulated with data before hand.
"""

try:
    import click
except:
    pass
    

from PySide6.QtWidgets import QWidget, QApplication
import importlib
import sys

def load_entrypoint(spec: str):
    """
    Load a class entrypoint of format module.submodule:object.

    Module has to be on path.
    """
    try:
        module_path, attr = spec.split(":", 1)
    except ValueError:
        raise SystemExit(
            "Entry point must be in form module.submodule:object"
        )

    module = importlib.import_module(module_path)

    try:
        obj = getattr(module, attr)
    except AttributeError:
        raise SystemExit(f"{attr!r} not found in {module_path!r} - check system path!")

    return obj

def main():
    if len(sys.argv) != 2:
        raise SystemExit(
            "Instances the widget directly."
            "Usage: uv run -m test_widget qtcomponents.table:DataTable"
        )



    args = sys.argv[1]
    entry = load_entrypoint(args)

    # Needs to be global.
    QT_APP = QApplication([])

    try:
        widget: QWidget = entry()
        widget.show()
    except:
        print(f"Failed to load widget: {args}")
        raise
    
    exit_code = QT_APP.exec()

if __name__ == "__main__":
    main()
