from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Tuple, NamedTuple

from PySide6.QtWidgets import QFileDialog, QWidget


class FileFilter(NamedTuple):
    """
    FileFilter to use with FileDialog class.
    eg = FileFilter(
        display_text="Bitmap",
        suffix="bmp"
    )

    """
   
    display_text: str
    suffix: str

    def as_Qfilter(self) -> str:
        """
        Convert to 
        Bitmap (*.bmp)
        """
        # Strip the leading `.`` incase it was included.
        return f"{self.display_text} (*.{self.suffix.lstrip(".")})"

def convert_filter_to_qt(filter: Optional[List[FileFilter]] = None,) -> Tuple[List[str], str]:
    """
    Converts a filter dict into something Qt can use.
    """
    # As the Dialog will return the selected filter, use this as the key to return the correctly formatted suffix
    # EG: "Bitmap (*.bmp);; JPEG (*.jpg);; PNG (*.png);; Tagged Image File Format (*.tiff)"
    filter_list: List[str] | List = [key.as_Qfilter() for key in filter] if filter is not None else []

    # QT Expects a string seperated by `;; `
    filter_string = ";; ".join(filter_list)

    return filter_list, filter_string

class FileDialog:
    """
    A class with a bunch on static methods for opening file dialogs.

    Use open / save
        parent: QWidget, `self`
        directory: Path, `./path/to/directory`
        caption: str,
        ...

    Parameters
    ----------
    parent: QWidget | None
        Parent Qt object.
    directory: Path | None
        Directory to open the FileDialog into.
    caption: str | None
        Caption to give the file dialog
    filter: List[FileFilter] | None
        Set a filter to force a filetype. Always assumes the first entry is the choosen filter.

    Filter
    ----------
    filepath = FileDialog.save(
        ...,
        filter=[
            FileFilter("Bitmap", ".bmp")
        ]
    )

    """

    @staticmethod
    def open(
        parent: Optional[QWidget] = None,
        directory: Optional[Path] = None,
        caption: str = "Open File",
        filter: List[FileFilter] | None = None,
    ) -> Optional[Path]:
        """
        Opens a file dialog window, and returns a selected Path.
        If no file is selected, nothing happens returning None.

        Returns
        ----------
        path: Optional[Path]
            If path selected, else None.
        """
        filter_list, filter_string = convert_filter_to_qt(filter)

        qfilepath, _ = QFileDialog.getOpenFileName(
            parent=parent,
            caption=caption,
            dir=str(directory) if directory is not None else "",
            filter=filter_string,
            selectedFilter=filter_list[0] if filter is not None else "",
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
        filter: List[FileFilter] | None = None,
    ) -> Optional[List[Path]]:
        """
        Same as open, but for multiple filepaths. Returning all filepaths as a list, even if only one is selected.
        If no file is selected, nothing happens returning None.

        Returns
        ----------
        paths: Optional[List[Path]]
            If path selected, else None. Will return, Path or List of Paths.
        """
        filter_list, filter_string = convert_filter_to_qt(filter)

        qfilepaths, _ = QFileDialog.getOpenFileNames(
            parent=parent,
            caption=caption,
            dir=str(directory) if directory is not None else "",
            filter=filter_string,
            selectedFilter=filter_list[0] if filter is not None else "",
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
        filter: List[FileFilter] | None = None,
        append_suffix: bool = True,
    ) -> Optional[Path]:
        """
        Opens a file dialog window, and returns a selected Path.
        If no file is selected, nothing happens returning None.

        Set append_suffix to auto append the choosen suffix

        Returns
        ----------
        path: Optional[Path]
            If path selected, else None.
        """
        filter_list, filter_string = convert_filter_to_qt(filter)

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
