from enum import Enum
from pathlib import Path
from typing import List
import logging 

from PySide6.QtCore import Qt, Signal, SignalInstance
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QSizePolicy,
    QWidget, QPushButton, QVBoxLayout,
)

from ..file import FileDialog, FileFilter
from .edit import ValidatedLineEdit

logger = logging.getLogger(__package__)

class PathWidgetState(Enum):
    Open = "Open File..."
    OpenMany = "Select Files..."
    Save = "Save File..."

# uv run qtcomponent -w qtcomponents.widgets.path:PathWidget --label="Test Label" --button-text="Button"
class PathWidget(QWidget):
    """
    A simple widget for displaying a line_edit with a button,
    clicking the button will open a FileDialog, result of this will 
    be emitted as a signal and store in the widget.


    When user edits line edit the path will be validated, you can specify the
    styling for this, refer to `ValidationLineEdit`.

    label (optional)
    -----
    | line_edit | button |
    
    Parameters
    ----------
    state: PathWidgetState = PathWidgetState.Open
        State to initialise the Widget as.
    label: str | None
        If no label provide it will not display a label.
    button_text: str | None
        Set the text on the button, else defaults to PathWidgetState value.
    caption: str = ""
        The caption used in the FileDialog.
    filter: List[FileFilter] | None
        The filter used for the FileDialog.
    path: Path 
        Provide a path to preload widget with, set the attribute `directory` as the parent of this path.

    Attributes
    ----------
    signal_path_selected: SignalInstance
    signal_many_paths_selected: SignalInstance

    path: Path | None
    paths: List[Path] | None
        List of Paths if OpenMany is the set state.
    directory: Path | None
        The directory the dialog when open into, this can be set at widget initialisation,
        or updated later, when the button is clicked it will open into this dir, if valid.

    """

    signal_path_selected: SignalInstance = Signal(Path)  # ty:ignore[invalid-assignment]
    signal_many_paths_selected: SignalInstance = Signal(List[Path])  # ty:ignore[invalid-assignment]
    
    path: Path | None = None
    paths: List[Path] | None = None
    directory: Path | None = None

    line_edit: ValidatedLineEdit
    button: QPushButton

    def __init__(
        self,
        state: PathWidgetState = PathWidgetState.Open,
        label: str | None = None,
        button_text: str | None = None,
        caption: str = "",
        filter: List[FileFilter] | None = None,
        path: Path | None = None,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.setContentsMargins(0, 0, 0, 0)  # They pad too much, alignment seemed off.
        self.path = path
        
        if path and path.is_file():
            self.directory = path.parent
        elif path and path.is_dir(): 
            self.directory = path
        else:
            self.directory = None

        self.state = state
        self.caption = caption
        self.filter = filter
        self.label = label
        
        vlayout = QVBoxLayout()
        self.setLayout(vlayout)
        
        if label:
            _label = QLabel(label, self) 
            _label.setAlignment(Qt.AlignmentFlag.AlignBottom)
            vlayout.addWidget(_label)

        hlayout = QHBoxLayout()
        vlayout.addLayout(hlayout)
        
        self.line_edit = ValidatedLineEdit(self)
        hlayout.addWidget(self.line_edit)
        # Updates text in lineedit if a path was provided.
        self.update_line_edit()
        
        self.button = QPushButton(self)
        self.button.setText(button_text or state.value)
        hlayout.addWidget(self.button)

        self.connect_signals()

    def connect_signals(self) -> None:
        self.button.clicked.connect(self.handle_button)
        self.line_edit.editingFinished.connect(self.handle_line_edit)
        
    def update_line_edit(self) -> None:
        """
        Update line edit with stored path, setting first path if OpenMany.
        initialises with directory if directory is availble
        """
        if self.path:
            self.line_edit.setText(str(self.path))
        elif self.paths:
            self.line_edit.setText(str(self.paths[0].parent))
        elif self.directory: # lowest priority
            self.line_edit.setText(str(self.directory))

    def open_file_dialog(self, directory: Path | None = None) -> Path | List[Path] | None:
        """
        Setting directory will open dialog in said directory.
        """
        match self.state:
            case PathWidgetState.Open:
                return FileDialog.open(self, directory, self.caption, self.filter)
            case PathWidgetState.OpenMany:
                return FileDialog.opens(self, directory, self.caption, self.filter)
            case PathWidgetState.Save:
                return FileDialog.save(self, directory, self.caption, self.filter)
            case _:
                return
    
    def handle_button(self) -> None:
        """
        When button clicked open dialog, then store result in widget and also emit signal.
        """

        path = self.open_file_dialog(self.directory)

        if path is None:
            return

        if isinstance(path, Path):
            self.path = path
            self.directory = path.parent
            self.signal_path_selected.emit(self.path)
        else:
            self.paths = path
            self.path = path[0] # set as first path
            self.directory = path[0].parent
            self.signal_many_paths_selected.emit(self.path)
        
        self.update_line_edit()
    
    def handle_line_edit(self, string: str = "") -> None:
        """
        Update path with string from line edit.
        """
        try:
            path = Path(string).resolve()
        except:
            logger.warning(f"Failed to convert path from line edit string. {string =}")
            self.line_edit.is_invalid(True)
            return
        
        self.path = path
        self.directory = path.parent
                
        # Reset if path is valid.
        self.line_edit.is_invalid(False)


# uv run qtcomponent -w qtcomponents.widgets.path:PathWidget --label="Test Label" --button-text="Button"
class PathButton(QPushButton):
    """
    A simple button, a reduced version of PathWidget, clicking the button 
    will open a FileDialog, result of this will be emitted as a signal and 
    stored in the button.
    
    Parameters
    ----------
    state: PathWidgetState = PathWidgetState.Open
        State to initialise the Widget as.
    label: str | None
        If no label provide it will not display a label.
    button_text: str | None
        Set the text on the button, else defaults to PathWidgetState value.
    caption: str = ""
        The caption used in the FileDialog.
    filter: List[FileFilter] | None
        The filter used for the FileDialog.
    path: Path 
        Provide a path to preload widget with, set the attribute `directory` as the parent of this path.

    Attributes
    ----------
    signal_path_selected: SignalInstance
    signal_many_paths_selected: SignalInstance

    path: Path | None
    paths: List[Path] | None
        List of Paths if OpenMany is the set state.
    directory: Path | None
        The directory the dialog when open into, this can be set at widget initialisation,
        or updated later, when the button is clicked it will open into this dir, if valid.

    """

    signal_path_selected: SignalInstance = Signal(Path)  # ty:ignore[invalid-assignment]
    signal_many_paths_selected: SignalInstance = Signal(List[Path])  # ty:ignore[invalid-assignment]
    
    path: Path | None = None
    paths: List[Path] | None = None
    directory: Path | None = None


    def __init__(
        self,
        state: PathWidgetState = PathWidgetState.Open,
        button_text: str | None = None,
        caption: str = "",
        filter: List[FileFilter] | None = None,
        path: Path | None = None,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.path = path
        
        if path and path.is_file():
            self.directory = path.parent
        elif path and path.is_dir(): 
            self.directory = path
        else:
            self.directory = None

        self.state = state
        self.caption = caption
        self.filter = filter
        
        self.setText(button_text or state.value)

        self.connect_signals()

    def connect_signals(self) -> None:
        self.clicked.connect(self.handle_button)    

    def open_file_dialog(self, directory: Path | None = None) -> Path | List[Path] | None:
        """
        Setting directory will open dialog in said directory.
        """
        match self.state:
            case PathWidgetState.Open:
                return FileDialog.open(self, directory, self.caption, self.filter)
            case PathWidgetState.OpenMany:
                return FileDialog.opens(self, directory, self.caption, self.filter)
            case PathWidgetState.Save:
                return FileDialog.save(self, directory, self.caption, self.filter)
            case _:
                return
    
    def handle_button(self) -> None:
        """
        When button clicked open dialog, then store result in widget and also emit signal.
        """

        path = self.open_file_dialog(self.directory)

        if path is None:
            return

        if isinstance(path, Path):
            self.path = path
            self.directory = path.parent
            self.signal_path_selected.emit(self.path)
        else:
            self.paths = path
            self.path = path[0] # set as first path
            self.directory = path[0].parent
            self.signal_many_paths_selected.emit(self.path)
        