from typing import Tuple

from PySide6.QtWidgets import QGroupBox, QVBoxLayout

from .simple import CheckBox
from .spinbox import LabelledSpinbox


class DimensionsGroupWidget(QGroupBox):
    """
    Dimensions Widget for initialising mark dimensions.
    """

    def __init__(self, wmax: int, hmax: int, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setTitle("Dimensions")
        self.match_dimensions = False
        dimensions_layout = QVBoxLayout()
        self.setLayout(dimensions_layout)

        self.width_spinbox = LabelledSpinbox("Width (px):", max=wmax)
        dimensions_layout.addWidget(self.width_spinbox)

        self.height_spinbox = LabelledSpinbox("Height (px):", max=hmax)
        dimensions_layout.addWidget(self.height_spinbox)

        self.dimension_match_checkbox = CheckBox("Width = Height", True, parent=self)
        dimensions_layout.addWidget(self.dimension_match_checkbox)

        self.set_dimensions_equal(True)
        self.connect_signals()

    def connect_signals(self) -> None:
        self.dimension_match_checkbox.checkStateChanged.connect(self.set_dimensions_equal)

    def set_dimensions_equal(self, state: bool) -> None:
        """
        Set's width equal to height.
        """
        if state:
            self.height_spinbox.setValue(self.width_spinbox.value())
        self.match_dimensions = state
        self.height_spinbox.setEnabled(not state)

    def value(self) -> Tuple[int, int]:
        return self.width_spinbox.value(), self.height_spinbox.value()
