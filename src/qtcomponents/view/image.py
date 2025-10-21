from __future__ import annotations

from typing import Optional

from numpy import ndarray
from PySide6.QtCore import QRectF
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QGraphicsPixmapItem

from .lib import numpy_to_pixmap

Image = ndarray


class ImageItem(QGraphicsPixmapItem):
    """
    Image Item. For use in Qt Graphics Widgets.
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._image: Optional[Image] = None

    def set_raw_image(self, image: Image) -> None:
        """
        Repeated calls to this function do nothing after the first.
        """
        if self._image is None:
            self._image = image

    def reset(self) -> None:
        """
        Resets pixmap using stored raw image.
        """
        if self._image is None:
            raise Exception("No image was set, cannot reset.")

        self.update_image(self._image)

    def update_image(self, image: Image | QPixmap) -> QRectF:
        """
        Update the image used for display.
        The first call of this method using numpy array will set the raw image.
        """
        if not isinstance(image, QPixmap):
            self.set_raw_image(image)
            image = numpy_to_pixmap(image)

        self.setPixmap(image)

        return self.boundingRect()

    def is_image_set(self) -> bool:
        """
        Method that returns a bool result for whether there is a displayable image.
        """
        return not self.pixmap().isNull()

    def is_under_mouse(self) -> bool:
        """
        Return the `True` is under mouse else returns `False`.
        If image is empty, will return `False`.
        """
        return self.is_image_set() and self.isUnderMouse()

    @staticmethod
    def from_numpy(image: Image) -> ImageItem:
        """
        Convert a numpy array image into a pixmap image for use in Qt Widgets.
        Returns an element that can be inserted into a Qt scene.
        """
        pixmap = ImageItem()
        pixmap.update_image(image)
        return pixmap
