from typing import Tuple

from PySide6.QtCore import Qt, SignalInstance
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QSizePolicy,
    QSlider,
    QSpinBox,
    QWidget,
)


class LabelledSpinbox(QWidget):
    """
    A labelled spinbox.

    Label SpinBox

    Parameters
    ----------
    label: str,
    min: int = 0,
    max: int = 100,
    step: int = 5,
    initial_value: int = 10,
    """

    def __init__(
        self, label: str, min: int = 0, max: int = 100, step: int = 5, initial_value: int = 10, *args, **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self.label: QLabel = QLabel(label, parent=self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignCenter)
        self.label.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Ignored))
        layout.addWidget(self.label)

        self.spinbox: QSpinBox = QSpinBox(self)
        self.spinbox.setMinimum(min)
        self.spinbox.setMaximum(max)
        self.spinbox.setValue(initial_value)
        self.spinbox.setSingleStep(step)
        layout.addWidget(self.spinbox)

        # Expose common signals
        self.valueChanged: SignalInstance = self.spinbox.valueChanged

    def value(self) -> int:
        """
        Get spinbox value.
        """
        return self.spinbox.value()

    def setValue(self, value: int) -> None:
        """
        Set spinbox value.
        """
        self.spinbox.setValue(value)


class SpinboxSlider(QWidget):

    slider: QSlider
    spinbox: QSpinBox

    valueChanged: SignalInstance

    def __init__(
        self, value: int = 0, label: str | None = None, range: Tuple[int, int] = (0, 100), suffix="%", *args, **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        low, high = range

        layout = QHBoxLayout()
        self.setLayout(layout)

        if label is not None:
            self.label = QLabel(label, self)
            layout.addWidget(self.label)

        self.slider = QSlider(Qt.Orientation.Horizontal, self)
        self.slider.setMinimum(low)
        self.slider.setMaximum(high)
        self.slider.setSingleStep(5)
        self.slider.setValue(value)
        self.slider.setSliderPosition(value)
        layout.addWidget(self.slider)

        self.spinbox = QSpinBox(self, suffix=suffix)
        self.spinbox.setMinimum(low)
        self.spinbox.setMaximum(high)
        self.spinbox.setSingleStep(5)
        self.slider.setValue(value)
        layout.addWidget(self.spinbox)

        self.connect_signals()

    def connect_signals(self) -> None:
        self.slider.valueChanged.connect(self.spinbox.setValue)
        self.spinbox.valueChanged.connect(self.slider.setValue)
        self.valueChanged = self.spinbox.valueChanged

    def value(self) -> int | float:
        return self.spinbox.value()
