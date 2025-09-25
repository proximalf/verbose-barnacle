from typing import List

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (QComboBox, QHBoxLayout, QLabel, QPushButton,
                               QSpacerItem, QSpinBox, QVBoxLayout, QWidget)


class SerialConnectionWidget(QWidget):
    """
    A WidgetComponent for managing serial connections.

    A ComboBox populated with avalible ports, a button to connect, a spinbox for an address, starting at 11, and a status label.

    When the `Connect` button is pressed a `connection_requested` signal is emitted.
    The signal emits the `connection_flag` status, and address value.
    When connected the `connection_flag` will be set to `True`.
    """

    signal_connection_requested = Signal(bool, str, int)

    def __init__(self, parent: QWidget, *args, **kwargs) -> None:
        super().__init__(parent=parent, *args, **kwargs)
        self._connected_flag = False

        self.horizontalLayout = QHBoxLayout(self)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)

        self.connection_layout = QVBoxLayout()
        self.connection_layout.setContentsMargins(0, 0, 0, 0)

        self.connect_button = QPushButton(self)
        self.port_cbox = QComboBox(self)

        self.address_layout = QHBoxLayout()
        self.address_spinbox = QSpinBox(self)
        self.address_spinbox.setMinimum(11)
        self.address_spinbox.setMaximum(99)
        self.address_label = QLabel(self)
        self.address_label.setText("Address: ")
        self.address_label.setFixedWidth(65)

        self.address_layout.addWidget(self.address_label)
        self.address_layout.addWidget(self.address_spinbox)

        self.label = QLabel(self)

        self.connection_layout.addWidget(self.connect_button)
        self.connection_layout.addWidget(self.port_cbox)
        self.connection_layout.addLayout(self.address_layout)

        self.horizontalLayout.addLayout(self.connection_layout)
        self.horizontalLayout.addWidget(self.label)

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
        self.port_cbox.setEnabled(not connected)
        self.connect_button.setEnabled(not connected)
        self.address_spinbox.setEnabled(not connected)

    def emit_connection_request(self) -> None:
        self.signal_connection_requested.emit(
            self._connected_flag,
            self.port_cbox.currentText(),
            self.address_spinbox.value(),
        )
