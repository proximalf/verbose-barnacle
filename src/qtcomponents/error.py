import traceback
from typing import Optional

from PySide6.QtWidgets import QMessageBox, QWidget


def show_error_dialog(message: str, exception: Optional[Exception] = None, parent: Optional[QWidget] = None) -> None:
    """
    Helper function to generate an error dialog. Dialog will execute at the end of the function.
    """
    dialog = QMessageBox(parent)
    dialog.setIcon(QMessageBox.Icon.Critical)
    dialog.setWindowTitle("Error")
    dialog.setText("An error has occurred.")
    dialog.setInformativeText(message)

    if exception is not None:
        details = traceback.format_exc()
        dialog.setDetailedText(details)

    dialog.setStandardButtons(QMessageBox.StandardButton.Ok)
    dialog.adjustSize()
    dialog.exec()
