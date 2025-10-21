import sys
from functools import wraps
from pathlib import Path
from typing import Tuple, Union

from PySide6.QtCore import QSize
from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget

import numpy as np
from PIL.Image import open

Image = np.ndarray

def load_image(path: Path) -> Image:
    return np.array(open(path))

TEST_IMAGE_PATH = Path(__file__).parent / "test_data/image.png"

TEST_IMAGE_PATH = Path(__file__).parent / "test_data/image.png"
def test_image() -> Image:
    image = load_image(TEST_IMAGE_PATH)
    return image

def test_image_w_path() -> Tuple[Image, Path]:
    image = load_image(TEST_IMAGE_PATH)
    return image, TEST_IMAGE_PATH

def test_widget(func):
    """
    Decorator function to test a widget in a window.

    """
    @wraps(func)
    def wrapper():
        qt_app = QApplication([])
        mw = QWidget()
        mw.resize(QSize(400, 300))
        layout = QVBoxLayout(mw)
        mw.setLayout(layout)

        widget = func()

        layout.addWidget(widget)
        mw.show()
        exit_code = qt_app.exec()

        sys.exit(exit_code)

    return wrapper
