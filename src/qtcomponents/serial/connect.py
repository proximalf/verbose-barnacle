from typing import List

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSpacerItem,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)


class SerialConnectionWidget(QWidget):
    """
    A WidgetComponent for managing serial connections.

    A ComboBox populated with avalible ports, a button to connect, and a status label.

    When the `Connect` button is pressed a `connection_requested` signal is emitted.
    The signal emits the port and `connection_flag` status.
    When connected the `connection_flag` will be set to `True`.
    """

    signal_connection_requested = Signal(bool, str)

    def __init__(self, parent: QWidget, *args, **kwargs) -> None:
        super().__init__(parent=parent, *args, **kwargs)
        self._connected_flag = False

        self.connection_layout = QHBoxLayout(self)
        self.connection_layout.setContentsMargins(0, 0, 0, 0)

        self.connect_button = QPushButton(self)
        self.port_cbox = QComboBox(self)

        self.label = QLabel(self)

        self.connection_layout.addWidget(self.label)
        self.connection_layout.addWidget(self.port_cbox)
        self.connection_layout.addWidget(self.connect_button)

        self.connect_button.clicked.connect(self.emit_connection_request)
        self.connect_button.setText("Connect")
        self.label.setText("Status: Not Connected!")

    def populate_ports(self, ports: List[str]) -> None:
        """
        Populate combobox with port addresses.
        """
        self.port_cbox.addItems(ports)

    def update_status(self, string: str) -> None:
        """
        Update the status label, the label is prepended with 'Status: {string}'.
        """
        self.label.setText(f"Status: {string}")

    def set_connected(self, connected: bool = False) -> None:
        """
        Disables or enables the ui elements if connected.
        Sets the internal flag.
        """
        self._connected_flag = connected
        self.connect_button.setText("Connect" if not connected else "Disconnect")
        self.update_status("Connected!" if connected else "Not Connected!")
        self.port_cbox.setEnabled(not connected)

    def emit_connection_request(self) -> None:
        self.signal_connection_requested.emit(
            self._connected_flag,
            self.port_cbox.currentText(),
        )
