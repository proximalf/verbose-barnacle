from enum import Enum
from typing import NamedTuple

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QWidget, QMainWindow, QDockWidget, QTextEdit, QTabWidget


class MoveableWidget(NamedTuple):
    name: str
    widget: QWidget
    dock: QDockWidget

class Area(Enum):
    """Shorthand for Qt's long enum"""
    Right = Qt.DockWidgetArea.RightDockWidgetArea
    Left = Qt.DockWidgetArea.LeftDockWidgetArea
    Bottom = Qt.DockWidgetArea.BottomDockWidgetArea
    Top = Qt.DockWidgetArea.TopDockWidgetArea

class DockingManger:
    """
    Basic Docking window manager.

    Holds reference to mainwindow, add widgets to window using this.
    """

    active: MoveableWidget | None
    widgets: dict[str, MoveableWidget]

    def __init__(self, window: QMainWindow) -> None:
        self.window = window
        self.widgets = {}       
        self.active = None

        self.window.setDockNestingEnabled(True)
        self.window.setDockOptions(
            QMainWindow.DockOption.AllowNestedDocks
            | QMainWindow.DockOption.AllowTabbedDocks
            | QMainWindow.DockOption.AnimatedDocks
        )

        self.window.setTabPosition(
            Qt.DockWidgetArea.AllDockWidgetAreas,
            QTabWidget.TabPosition.North
        )

        self.window.tabifiedDockWidgetActivated.connect(
            self.dock_activated
        )

    def dock_activated(self, dock: QDockWidget):
        """Store the active dock widget"""
        for name, mw in self.widgets.items():
            if mw.dock == dock:
                self.active = mw
                return
        
        self.active = None
    
    def has_widgets(self) -> bool:
        return len(self.widgets) > 0
        

    def add_widget(self, widget: QWidget, name: str, area: Area = Area.Right, tab: bool = True, parent: MoveableWidget | None = None) -> MoveableWidget:
        """
        Add a widget, name is given to the dock widget.
        if tab is True, will stack with the first tab.        
        """
        
        if self.widgets.get(name) is not None:
            dict_name = name + f"-{len(self.widgets)}"
        else:
            dict_name = name

        widget.setParent(self.window)
        widget.setObjectName(name)

        dock_widget = QDockWidget(dict_name, self.window)
        dock_widget.setWidget(widget)
        dock_widget.setAllowedAreas(Qt.DockWidgetArea.AllDockWidgetAreas)
        dock_widget.setFeatures(
            QDockWidget.DockWidgetFeature.DockWidgetClosable
            | QDockWidget.DockWidgetFeature.DockWidgetMovable
            # | QDockWidget.DockWidgetFeature.DockWidgetFloatable # Doesn't work so nicely
        )

        self.window.addDockWidget(
            area.value,
            dock_widget
            )
        
        mw = MoveableWidget(dict_name, widget, dock_widget)
        
        if tab and len(self.widgets) > 1:
            # Do tab onto itself.
            parent = parent or list(self.widgets.values())[0]
            self.window.tabifyDockWidget(parent.dock, dock_widget)
        
        if self.active is None:
            self.active = mw

        self.widgets[dict_name] = mw

        return mw

    def lock_docking(self, locked: bool = True) -> None:
        """
        Lock movement for dock widgets.
        """
        for widget in self.widgets.values():
            features = widget.dock.features()

            if locked:
                features &= ~QDockWidget.DockWidgetFeature.DockWidgetMovable
            else:
                features |= QDockWidget.DockWidgetFeature.DockWidgetMovable

            widget.dock.setFeatures(features)
