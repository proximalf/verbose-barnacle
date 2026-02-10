from typing import Optional, Tuple

from PySide6.QtWidgets import QGroupBox, QVBoxLayout, QWidget

from .simple import RadioButton
from .spinbox import LabelledSpinbox


class XYPositionWidget(QWidget):
    """
    A widget for determining the position of a object.
    """

    def __init__(self, title: Optional[str] = None, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        layout = QVBoxLayout()

        self.x_spinbox = LabelledSpinbox("X:", parent=self)
        self.y_spinbox = LabelledSpinbox("Y:", parent=self)
        layout.addWidget(self.x_spinbox)
        layout.addWidget(self.y_spinbox)

        if title is not None:
            n_layout = QVBoxLayout()
            group = QGroupBox(title, self)
            group.setLayout(layout)
            n_layout.addWidget(group)
            n_layout.setContentsMargins(0,0,0,0)
            self.setLayout(n_layout)
        else:
            layout.setContentsMargins(0, 0, 0, 0)
            self.setLayout(layout)

    def set_spinbox_limits(self, xmax: int, ymax: int, min: int = 0, step: int = 1) -> None:
        self.x_spinbox.spinbox.setMinimum(min)
        self.y_spinbox.spinbox.setMinimum(min)

        self.x_spinbox.spinbox.setMaximum(xmax)
        self.y_spinbox.spinbox.setMaximum(ymax)

        self.x_spinbox.spinbox.setSingleStep(step)
        self.y_spinbox.spinbox.setSingleStep(step)

    def values(self) -> Tuple[int, int]:
        """
        Returns the values in the spinboxes.
        """
        return self.x_spinbox.value(), self.y_spinbox.value()


class PositionGroupWidget(QGroupBox):
    """
    A Grouped widget for determining the position of a object.
    Features a checkbox menu to choose which point to anchor to.
    """

    def __init__(self, title: str = "Position", *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setObjectName(f"PositionWidget-{title}")
        self.setTitle(title)

        layout = QVBoxLayout()

        self.position = XYPositionWidget(parent=self)
        layout.addWidget(self.position)

        self.radio_rect_top_left = RadioButton("Top Left:", True, self)
        self.radio_rect_centre = RadioButton("Centre:", False, self)

        layout.addWidget(self.radio_rect_top_left)
        layout.addWidget(self.radio_rect_centre)

        self.setLayout(layout)

    def set_spinbox_limits(self, xmax: int, ymax: int, min: int = 0, step: int = 1) -> None:
        self.position.set_spinbox_limits(xmax, ymax, min, step)

    def values(self) -> Tuple[int, int]:
        """
        Returns the values in the spinboxes.
        """
        return self.position.values()

    def is_top_left(self) -> bool:
        """
        Returns True if top left is checked.
        """
        return self.radio_rect_top_left.isChecked()
