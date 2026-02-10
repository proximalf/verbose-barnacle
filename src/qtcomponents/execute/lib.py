from enum import Enum
from pathlib import Path
from typing import Callable

try:
    import click
except:
    pass


import importlib
import sys

from PySide6.QtWidgets import QApplication, QWidget

ENTRY_POINT_NAME = "qtcomponents.execute"

def load_function_entry_point() -> Callable | None:
    """
    Finds the first entrypoint of associated group name and return the Callable.
    """
    from importlib.metadata import entry_points

    eps = entry_points(group=ENTRY_POINT_NAME)

    for ep in eps.select(name="execute"):
        extension: Callable = ep.load()
        return extension


def find_project_root() -> Path:
    """
    Find a module root, looks for a pyproject file, so is a bit crude.
    """

    cwd = Path.cwd().resolve()

    # loop thru and find a local pyproject file.
    for parent in [cwd, *cwd.parents]:
        if (parent / "pyproject.toml").exists():
            return parent

    raise RuntimeError("Project root not found - expects a `pyproject.toml` file to attach module to system path")


def load_widget_as_entrypoint(path: str) -> Callable[..., QWidget]:
    """
    Load a QWidget as an entrypoint for a given path in format module.submodule:object.

    Module has to be on path.

    Returns
    -------
    uninstanced_widget
        This will still need to be called to get the object.
    """
    try:
        module_path, widget_class_name = path.split(":", 1)
    except ValueError:
        raise SystemExit("Entry point must be in form `module.submodule:object`")
    module = importlib.import_module(module_path)

    try:
        # Uninstanced object.
        uninstanced_widget = getattr(module, widget_class_name)
    except AttributeError:
        raise SystemExit(f"{widget_class_name!r} not found in {module_path!r} - check system path!")

    return uninstanced_widget


def resolve_enum(path: str) -> Enum:
    """
    Load a Enum as an entrypoint for a given path in format module.submodule:object.

    Loads an enum and initialises with the stated value.
    """
    try:
        module_path, enum_path = path.split(":", 1)
    except ValueError:
        raise SystemExit("Entry point must be in form `module.submodule:Enum.Value`")

    try:
        enum_name, member_name = enum_path.split(".")
    except ValueError:
        raise SystemExit("Enum must be initialised correctly: `Enum.Value`")

    module = importlib.import_module(module_path)

    enum_cls = getattr(module, enum_name)
    return enum_cls[member_name]
