from pathlib import Path
from typing import Dict, List, Optional

from PySide6.QtWidgets import QFileDialog, QWidget


class FileDialog:
    """
    A class with a bunch on static methods for opening file dialogs.

    Use open / save
        parent: QWidget, `self`
        directory: Path, `./path/to/directory`
        caption: str,
        filter: str, `*.file`

    Parameters
    ----------
    parent: Optional[QWidget]
        Parent Qt object.
    directory: Optional[Path]
        Directory to open the FileDialog into.
    caption: Optional[str]
        Caption to give the file dialog
    filter: Optional[str]
        Set a filter to force a filetype.
        eg = `filter="CSV (*.csv);; JPEG (*.jpg);; PNG (*.png);; Tagged Image File Format (*.tiff)"`
    """

    @staticmethod
    def open(
        parent: Optional[QWidget] = None,
        directory: Optional[Path] = None,
        caption: str = "Open File",
        filter: Optional[str] = None,
    ) -> Optional[Path]:
        """
        Opens a file dialog window, and returns a selected Path.
        If no file is selected, nothing happens returning None.

        Returns
        ----------
        path: Optional[Path]
            If path selected, else None.
        """
        qfilepath, _ = QFileDialog.getOpenFileName(
            parent=parent,
            caption=caption,
            dir=str(directory),
            filter=filter if filter else "",
        )

        # Do nothing if no file selected.
        if len(qfilepath) == 0:
            return None

        return Path(qfilepath)

    @staticmethod
    def opens(
        parent: Optional[QWidget] = None,
        directory: Optional[Path] = None,
        caption: str = "Open Files",
        filter: Optional[str] = None,
    ) -> Optional[List[Path]]:
        """
        Same as open, but for multiple filepaths. Returning all filepaths as a list, even if only one is selected.
        If no file is selected, nothing happens returning None.

        Returns
        ----------
        paths: Optional[List[Path]]
            If path selected, else None. Will return, Path or List of Paths.
        """
        qfilepaths, _ = QFileDialog.getOpenFileNames(
            parent=parent,
            caption=caption,
            dir=str(directory),
            filter=filter if filter else "",
        )

        # Do nothing if no file selected.
        if len(qfilepaths) == 0:
            return None

        # Catch if one path is chosen and is not a list.
        if not isinstance(qfilepaths, list):
            return [Path(qfilepaths)]
        return [Path(path) for path in qfilepaths]

    @staticmethod
    def save(
        parent: Optional[QWidget] = None,
        directory: Optional[Path] = None,
        caption: str = "Save File",
        filter: Optional[Dict[str, str]] = None,
        append_suffix: bool = True,
    ) -> Optional[Path]:
        """
        Opens a file dialog window, and returns a selected Path.
        If no file is selected, nothing happens returning None.

        Set append_suffix to auto append the choosen suffix

        Filter
        ----------
        filepath = FileDialog.save(
            ...,
            filter={
                "Bitmap (*.bmp)": ".bmp",
            },
        )


        Returns
        ----------
        path: Optional[Path]
            If path selected, else None.
        """
        # As the Dialog will return the selected filter, use this as the key to return the correctly formatted suffix
        # EG: "Bitmap (*.bmp);; JPEG (*.jpg);; PNG (*.png);; Tagged Image File Format (*.tiff)"
        filter_list = [key for key in filter.keys()] if filter is not None else []

        # QT Expects a string seperated by `;; `
        filter_string = ";; ".join(filter_list)

        qfilepath, selected_filter = QFileDialog.getSaveFileName(
            parent=parent,
            caption=caption,
            dir=str(directory) if directory is not None else "",
            filter=filter_string,
            selectedFilter=filter_list[0] if filter is not None else "",
        )
        # Do nothing if no file selected.
        if len(qfilepath) == 0:
            return None

        filepath = Path(qfilepath)

        if filepath.suffix:
            return filepath

        if append_suffix and filter is not None:
            return filepath.with_suffix(filter[selected_filter])

        return filepath
