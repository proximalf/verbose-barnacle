import sys
from pathlib import Path

from PySide6.QtCore import QSize
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QMainWindow,
    QVBoxLayout,
    QWidget,
)

from qtcomponents.file import FileDialog, FileFilter
from qtcomponents.widgets.path import PathWidget


def test_dialog() -> None:
    filter = [
        FileFilter("PNG", "png"),
        FileFilter("Python Files", ".py"),
    ]

    path = FileDialog.open(directory=Path(__file__).parent / "test_data", caption="Test", filter=filter)
    print(path)


def test_path(parent: QWidget) -> QWidget:
    filter = [
        FileFilter("PNG", "png"),
        FileFilter("Python Files", ".py"),
    ]

    return PathWidget(
        label="Test", caption="Test", filter=filter, path=Path(__file__).parent / "test_data", parent=parent
    )


if __name__ == "__main__":
    QT_APP = QApplication()

    mw = QMainWindow()

    layout = QVBoxLayout()
    mw.setLayout(layout)

    path = test_path(mw)
    layout.addWidget(path)

    mw.resize(QSize(400, 300))
    mw.show()
    # test_dialog()

    sys.exit(QT_APP.exec())
