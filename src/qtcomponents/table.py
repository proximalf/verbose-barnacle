from typing import List, Optional

import numpy as np
from PySide6.QtCore import (
    QAbstractTableModel,
    QModelIndex,
    QPersistentModelIndex,
    Qt,
)
from PySide6.QtWidgets import QHeaderView, QTableView


class StructuredArrayModel(QAbstractTableModel):
    """
    A Structured Array Model built from a numpy array.
    The arrays dtype must be specified with names, these names are used for the columns.
    """

    def __init__(self, array: np.ndarray) -> None:
        super().__init__()
        self._array = array
        self._field_names: List[str] = array.dtype.names # type: ignore
        self._data_alignment = Qt.AlignmentFlag.AlignCenter

    def rowCount(self, *args, **kwargs) -> int:
        return len(self._array)

    def columnCount(self, *args, **kwargs) -> int:
        return len(self._field_names)

    def data(
        self, index: QModelIndex | QPersistentModelIndex, role: int = Qt.ItemDataRole.DisplayRole
    ) -> Optional[str | Qt.AlignmentFlag]:
        """
        The data as a string for a given index.
        """
        if role == Qt.ItemDataRole.DisplayRole:
            row = index.row()
            col = index.column()
            field = self._field_names[col]
            data = str(self._array[row][field])
            return data
        elif role == Qt.ItemDataRole.TextAlignmentRole:
            return self._data_alignment
        return

    def headerData(
        self, section: int, orientation: Qt.Orientation, role: int = Qt.ItemDataRole.DisplayRole
    ) -> Optional[str]:
        """
        Header data, column names.
        """
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                # Use dtype field names as headers
                return self._field_names[section]
            if orientation == Qt.Orientation.Vertical:
                return str(section)
        return


class DataTable(QTableView):
    """
    An implementation of QTableView that accepts numpy structed arrays.

    Where the dtype is specified with labels.
    eg:
        np.array(data, dtype=[("NAME", "U10"), ("NUM", "I")])
    """

    def __init__(self, parent=None, show_row_index: bool = False, *args, **kwargs) -> None:
        super().__init__(parent=parent, *args, **kwargs)
        self.show_row_index(show_row_index)
        self.data = None
        self._model = None

    def show_row_index(self, visible: bool) -> None:
        """
        Method to set whether the row numbers are visible.
        """
        self.verticalHeader().setVisible(visible)

    def set_data(self, data: np.ndarray) -> None:
        """
        Set the data to display in the table. Accepts only a structed numpy array.
        Where the dtype is specified with labels -> np.array(data, dtype=[("NAME", "U10"), ("NUM", "I")])
        """
        self.data = data
        self._model = StructuredArrayModel(data)
        self.setModel(self._model)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.adjustSize()
        self.adjustSize()
