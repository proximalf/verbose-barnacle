from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QVBoxLayout, QWidget


class LabelledLineEdit(QWidget):
    """
    A line entry with a label.
    """

    edit: QLineEdit

    def __init__(
        self, label: str, default_string: str = "", placeholder_text: str = "", vertical: bool = True, *args, **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.setContentsMargins(0, 0, 0, 0)

        layout = QVBoxLayout() if vertical else QHBoxLayout()
        self.setLayout(layout)

        self.label = QLabel(label, parent=self)
        if vertical:
            self.label.setAlignment(Qt.AlignmentFlag.AlignBottom)
        else:
            self.label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignCenter)

        self.edit = QLineEdit(self)
        self.edit.setPlaceholderText(placeholder_text)
        self.edit.setText(default_string)

        layout.addWidget(self.label)
        layout.addWidget(self.edit)

    @property
    def text(self) -> str:
        return self.edit.text()

    @text.setter
    def text(self, text: str) -> None:
        self.edit.setText(text)
