from typing import Tuple

from PySide6.QtCore import Qt, SignalInstance
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QSizePolicy,
    QSlider,
    QSpinBox,
    QWidget, QDoubleSpinBox,
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

    spinbox: QSpinBox | QDoubleSpinBox

    def __init__(
        self, label: str, min: int | float = 0, max: int | float = 100, step: int | float = 5, initial_value: int | float = 10, type: type = int, *args, **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self.label: QLabel = QLabel(label, parent=self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignCenter)
        self.label.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Ignored))
        layout.addWidget(self.label)

        self._type = type
        
        if type is int:
            self.spinbox = QSpinBox(self)            
            self.spinbox.setMinimum(int(min))
            self.spinbox.setMaximum(int(max))
            self.spinbox.setValue(int(initial_value))
            self.spinbox.setSingleStep(int(step))
        else: 
            self.spinbox = QDoubleSpinBox(self)
            self.spinbox.setMinimum(int(min))
            self.spinbox.setMaximum(int(max))
            self.spinbox.setValue(int(initial_value))
            self.spinbox.setSingleStep(int(step))

        layout.addWidget(self.spinbox)

        # Expose common signals
        self.valueChanged: SignalInstance = self.spinbox.valueChanged

    def value(self) -> int | float:
        """
        Get spinbox value.
        """
        return self.spinbox.value()

    def setValue(self, value: int | float) -> None:
        """
        Set spinbox value.
        """
        if self._type is int:
            self.spinbox.setValue(int(value))
        else:
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
