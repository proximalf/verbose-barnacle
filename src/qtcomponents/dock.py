from enum import Enum
from typing import NamedTuple

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QWidget, QMainWindow, QDockWidget, QTextEdit, QTabWidget, QToolButton, QHBoxLayout


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


class DockTitleBar(QWidget):

    def __init__(self, dock: QDockWidget) -> None:
        super().__init__(dock)
        self.dock = dock
        self.setObjectName("docktitle") # for qss styling

        layout = QHBoxLayout(self)
        
        self.title = QLabel(dock.windowTitle())

        self.close_button = QToolButton()
        self.close_button.setText("×")
        self.close_button.setCursor(Qt.CursorShape.PointingHandCursor)
        
        self.close_button.clicked.connect(dock.close)

        layout.addWidget(self.title)
        layout.addStretch()
        layout.addWidget(self.close_button)

class DockingManager:
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
            raise ValueError("Can't add if name already exists")

        widget.setParent(self.window)
        widget.setObjectName(name)

        dock_widget = QDockWidget(name, self.window)
        dock_widget.setWidget(widget)
        dock_widget.setAllowedAreas(Qt.DockWidgetArea.AllDockWidgetAreas)
        dock_widget.setFeatures(
            QDockWidget.DockWidgetFeature.DockWidgetClosable
            | QDockWidget.DockWidgetFeature.DockWidgetMovable
            # | QDockWidget.DockWidgetFeature.DockWidgetFloatable # Doesn't work so nicely
        )

        dock_widget.setTitleBarWidget(DockTitleBar(dock_widget))

        self.window.addDockWidget(
            area.value,
            dock_widget
            )
        
        mw = MoveableWidget(name, widget, dock_widget)
        
        if tab and len(self.widgets) >= 1:
            # Do tab onto itself.
            parent = parent or list(self.widgets.values())[0]
            self.window.tabifyDockWidget(parent.dock, dock_widget)
        
        if self.active is None:
            self.active = mw

        self.widgets[name] = mw

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
