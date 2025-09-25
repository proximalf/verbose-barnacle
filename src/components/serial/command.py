from PySide6.QtCore import Signal
from PySide6.QtWidgets import (QHBoxLayout, QLineEdit, QTextEdit,
                               QPushButton, QVBoxLayout, QWidget)


class CommandEntryWidget(QWidget):
    """
    A WidgetComponent for managing sending commands to a serial device.

    When send is clicked a `command_entered` signal is emitted.
    """

    signal_command_entered = Signal(str)

    def __init__(self, parent: QWidget, *args, **kwargs) -> None:
        super().__init__(parent=parent, *args, **kwargs)

        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setContentsMargins(5, 5, 5, 5)

        self.message_widget = QTextEdit(self)
        self.message_widget.setReadOnly(True)

        self.command_entry = QLineEdit(self)
        self.command_entry.setPlaceholderText("Enter Command...")

        self.send_button = QPushButton(self)
        self.send_button.setText("Send")

        self.verticalLayout.addWidget(self.message_widget)
        self.horizontalLayout.addWidget(self.command_entry)
        self.horizontalLayout.addWidget(self.send_button)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.send_button.clicked.connect(self.send_command_entry)


    def send_command_entry(self) -> None:
        """
        Emit `command_entered` signal, and reset lineEdit box.
        """
        command = self.command_entry.text()
        self.signal_command_entered.emit(command)
        # Reset on send
        self.command_entry.setText("")
        self.insert_message(f"Sent: {command}")

    def insert_message(self, message: str) -> None:
        """
        Inserts a message into the TextEdit widget.
        """
        self.message_widget.append(message)

    def clear(self) -> None:
        """
        Clear the TextEdit widget.
        """
        self.message_widget.clear()
