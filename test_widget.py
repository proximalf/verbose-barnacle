import importlib
import sys

from test.lib import test_widget

def load_entrypoint(spec: str):
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
        raise SystemExit(f"{attr!r} not found in {module_path!r}")

    return obj

@test_widget
def main():
    if len(sys.argv) != 2:
        raise SystemExit(
            "Instances the widget directly."
            "Usage: uv run python test_widget.py qtcomponents.table:DataTable"
        )

    args = sys.argv[1]
    entry = load_entrypoint(args)

    try:
        return entry()
    except:
        print(f"Failed to load widget: {args}")

if __name__ == "__main__":
    main()
