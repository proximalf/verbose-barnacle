from enum import Enum
from typing import Optional

from PySide6.QtCore import QPointF
from PySide6.QtWidgets import QWidget

from .graphicsview import ImageViewer
from .image import Image, ImageItem
from .scene import ImageViewerScene, SceneLayer


class ImageViewComponent:
    """
    Image Viewer Component, holds reference to the encompassing widget and scene.
    """

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        self._raw_image: Optional[Image] = None

        self.viewer = ImageViewer(parent=parent)
        self.scene = ImageViewerScene(parent=parent)
        self.viewer.setScene(self.scene)

    @property
    def widget(self) -> QWidget:
        return self.viewer

    def set_image(self, image: Image) -> None:
        """
        Sets the displayed image. Stores the image for reference for displaying intensity values.
        """
        self._raw_image = image
        pixmap = ImageItem.from_numpy(image)
        self.scene.add_item(pixmap, layer=SceneLayer.Image)
        w, h = pixmap.boundingRect().bottomRight().toTuple()  # type: ignore
        self.scene.setSceneRect(0, 0, w, h)

    def reset_view(self) -> None:
        """
        Rescales view to fit the widget.
        """
        self.viewer.reset_view()

    def point_within_image(self, x: int, y: int) -> bool:
        """
        Check if a given x, y point is within bounds of image.
        Returns False is no image has been set.
        """
        if self._raw_image is None:
            return False

        img_y, img_x = self._raw_image.shape[0:2]
        # Just bring in by 1 pixel for rounding errors.
        return x < img_x - 1 and x > 0 and y < img_y - 1 and y > 0
