import logging

from PySide6.QtWidgets import QTextEdit, QVBoxLayout, QWidget


class LoggingComponent(QWidget):
    """
    Inherits QWidget.
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.text_box = QTextEdit(self)
        self.text_box.setReadOnly(True)
        self.vertical_layout = QVBoxLayout(self)
        self.setLayout(self.vertical_layout)
        self.vertical_layout.addWidget(self.text_box)

    def append(self, msg: str) -> None:
        self.text_box.append(msg)


class LoggingComponentHandler(logging.Handler):
    """
    Inherits logging.Handler.
    Logging handler that sends the log results to a given window
    """

    def __init__(self, edit: LoggingComponent, level: int | str = logging.WARNING) -> None:
        """
        A log handler that outputs messages to a provided QTextEdit.
        """
        super().__init__()
        self.edit: LoggingComponent = edit
        self.setLevel(level)
        self.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s - %(message)s", datefmt="%H:%M:%S"))

    def emit(self, record: logging.LogRecord) -> None:
        """
        Write the log to the object

        Parameters
        ----------
        record : LogRecord
            Record to write

        """
        self.edit.append(self.format(record))
