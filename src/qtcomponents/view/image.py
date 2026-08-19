from __future__ import annotations

from ..image import Image, image_to_pixmap
from PySide6.QtCore import QRectF
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QGraphicsPixmapItem


class ImageItem(QGraphicsPixmapItem):
    """
    Image Item. For use in Qt Graphics Widgets.
    Holds reference to the numpy array used to generate the pixmap.

    """

    @staticmethod
    def from_numpy(array: Image) -> ImageItem:
        image = ImageItem()
        image.set_image(array)
        return image

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._image: Image

    def set_image(self, image: Image) -> QRectF:
        self._image = image
        return self.update_image(image)

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
        The first call of this method sets the image, if provided a numpy array.
        """
        if not isinstance(image, QPixmap):
            if self._image is None:
                self.set_image(image)

            image = image_to_pixmap(image)

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
