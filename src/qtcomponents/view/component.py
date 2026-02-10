from typing import Optional

from PySide6.QtWidgets import QWidget

from .graphicsview import ImageViewer
from .image import Image, ImageItem
from .scene import ImageViewerScene, SceneLayer


class ImageViewComponent:
    """
    Image Viewer Component, holds reference to the encompassing widget and scene.
    Instantiates some tools
    """

    display_image: Image
    
    viewer: ImageViewer
    scene: ImageViewerScene

    def __init__(self, parent: Optional[QWidget] = None, *args, **kwargs) -> None:
        self.viewer = ImageViewer(parent=parent)
        self.scene = ImageViewerScene(parent=parent)
        self.viewer.setScene(self.scene)

        self.image_item = ImageItem()
        self.scene.add_item(self.image_item, layer=SceneLayer.Image)

    @property
    def _raw_image(self) -> Image:
        from warnings import warn

        warn("Depreciation warning")
        return self.image_item._image

    @property
    def image(self) -> Image:
        return self.display_image

    def set_image(self, image: Image) -> None:
        """
        Sets the stored image.
        """
        self.image_item.set_image(image)
        self.update_image(image)

    def update_image(self, image: Image) -> None:
        """
        Calling this will only update the image.
        """
        self.display_image = image.copy()
        bounding_rect = self.image_item.update_image(image)
        w, h = bounding_rect.bottomRight().toTuple()  # type: ignore
        self.scene.setSceneRect(0, 0, w, h)

    def reset_image(self) -> None:
        self.image_item.reset()

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
        if self.image_item._image is None:
            return False

        img_y, img_x = self.image_item._image.shape[0:2]
        # Just bring in by 1 pixel for rounding errors.
        return x < img_x - 1 and x > 0 and y < img_y - 1 and y > 0
