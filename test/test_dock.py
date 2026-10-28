"""
test_dock

simple mainwindow app 
"""

import logging

import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QTextEdit

from qtcomponents.dock import DockingManager, Area

logger = logging.getLogger(__name__)

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG)


def test_dock():

    app = QApplication(sys.argv)
    mw = QMainWindow()
    mw.setWindowTitle("test")
    
    dock_manager = DockingManager(mw)

    w = dock_manager.add_widget(QLabel("Main"), "main", Area.Left)

    dock_manager.add_widget(QLabel("Placeholder 1"), "place-1", Area.Bottom)
    dock_manager.add_widget(QLabel("Placeholder 2"), "place-3")
    dock_manager.add_widget(QLabel("Placeholder 3"), "place", tab=False)
    a = dock_manager.add_widget(QLabel("Placeholder 4"), "place-4", tab=False)
    dock_manager.add_widget(QTextEdit("Placeholder Panel"), "place-4", parent=a)

    # dock_manager.lock_docking()

    # raise the main tab
    w.dock.show()
    w.dock.raise_()

    mw.setMaximumSize(800, 700)
    mw.show()
    app.exec()


if __name__ == "__main__":
    test_dock()
