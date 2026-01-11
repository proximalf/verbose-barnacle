from functools import partial
from typing import List, Dict
from PySide6.QtCore import Signal, Qt
from enum import Enum
from PySide6.QtWidgets import QWidget, QDialog, QVBoxLayout, QHBoxLayout, QDialogButtonBox, QRadioButton

class ButtonBox(QDialogButtonBox):
    """
    Standard button box widget.
    """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setStandardButtons(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        

class Orientation(Enum):
    Vertical = "vertical"
    Horizontal = "horizontal"


class RadioButton(QRadioButton):

    def __init__(self, label: str, state: bool, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setContentsMargins(0, 0, 0, 0)  # They pad too much, alignment seemed off.
        self.state = state

        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.setText(label)
        self.setChecked(state)

class RadioButtonWidget(QWidget):
    """
    Takes a List of Enum with String values to create a list of radio buttons of a given orientation.
    """

    signal_radio_selected = Signal(Enum)

    def __init__(self, radios: List[Enum], orientation: Orientation | None = None, active: Enum | None = None,  *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        layout = QHBoxLayout() if orientation is Orientation.Horizontal else QVBoxLayout()
        self.setLayout(layout)

        self.radio_buttons: Dict[Enum, RadioButton] = {}

        for radio in radios:
            
            state = active is not None and radio is active
            button = RadioButton(radio.value, state, parent=self)
            layout.addWidget(button)
            
            self.radio_buttons[radio] = button
            button.clicked.connect(partial(self.signal_radio_selected.emit, radio))