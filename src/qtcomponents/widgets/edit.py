from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QVBoxLayout, QWidget


class LabelledLineEdit(QWidget):
    """
    A line entry with a label.

    label
    -----
    edit

    or

    label | edit
    """

    edit: QLineEdit

    def __init__(
        self, label: str, default_string: str | None = None, placeholder_text: str = "", vertical: bool = True, *args, **kwargs
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
        
        if default_string:
            self.edit.setText(default_string)

        layout.addWidget(self.label)
        layout.addWidget(self.edit)

    @property
    def text(self) -> str:
        return self.edit.text()

    @text.setter
    def text(self, text: str) -> None:
        self.edit.setText(text)

# Validation property name
# eg: QWidget[is_invalid="true" ] {...}
_VALIDATION_PROPERTY = "is_invalid"

class ValidatedLineEdit(QLineEdit):
    """
    Validation Styling
    ------------------
    When user edits line edit the path will be validated, you can specify the
    styling for this.

    ```
        ValidatedLineEdit[is_invalid="true"] {
            background-color: red;
            border: 1px solid red;
        }
    ```
    """

    def is_invalid(self, is_invalid: bool) -> None:
        """
        Update the stylesheet of the widget if the line edit is invalid.
        """
        if self.property(_VALIDATION_PROPERTY) == is_invalid:
            # block frequent calls
            return

        self.setProperty(_VALIDATION_PROPERTY, is_invalid)
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()