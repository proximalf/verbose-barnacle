from typing import List

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QHBoxLayout,
    QLabel,
    QRadioButton,
    QSizePolicy,
    QWidget,
)


class CheckBox(QCheckBox):

    def __init__(
        self,
        label: str,
        state: bool,
        layout_direction: Qt.LayoutDirection = Qt.LayoutDirection.RightToLeft,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.setContentsMargins(0, 0, 0, 0)  # They pad too much, alignment seemed off.
        self.state = state

        self.setLayoutDirection(layout_direction)
        self.setText(label)
        self.setChecked(state)


class RadioButton(QRadioButton):

    def __init__(self, label: str, state: bool, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setContentsMargins(0, 0, 0, 0)  # They pad too much, alignment seemed off.
        self.state = state

        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.setText(label)
        self.setChecked(state)


class LabelledComboBox(QWidget):
    def __init__(self, label: str, items: List[str] = [], placeholder: str = "", *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        layout = QHBoxLayout()
        self.setLayout(layout)

        self.label = QLabel(label, self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignCenter)
        self.label.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Ignored))
        layout.addWidget(self.label)
        self.combbox = QComboBox(self)
        self.combbox.addItems(items)
        layout.addWidget(self.combbox)

        self.item_choosen = self.combbox.currentTextChanged
