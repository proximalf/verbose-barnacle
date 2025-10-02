from typing import Tuple

import numpy as np
from PySide6.QtCore import QPoint, Qt
from PySide6.QtGui import QImage, QPixmap, QTransform
from PySide6.QtWidgets import QGraphicsItem, QGraphicsScene, QWidget


def numpy_to_pixmap(array: np.ndarray) -> QPixmap:
    """
    Converts a NumPy array to a QPixmap.
    The array should be in the format (height, width, channels).
    For grayscale, it should be (height, width).

    QImage unfortunately only accepts int types, values between 0-255 as RGB.
    If you encounter a scrambled image on load, check it's values.

    Parameters
    ----------
    array: ndarray
        Must be a uint array.

    Returns
    ----------
    image: QPixmap
        Image as a QPixmap to display within a qt application.
    """
    if not np.issubdtype(array.dtype, np.integer):
        raise TypeError(f"Unsupported array dtype: {array.dtype}")

    # Check if the array is grayscale (2D) or color (3D)
    depth = len(array.shape)

    if depth == 2:  # Grayscale
        height, width = array.shape
        image = QImage(array.data, width, height, width, QImage.Format.Format_Grayscale8)
    elif depth > 2:
        height, width, channels = array.shape

        if channels == 3:  # RGB
            image = QImage(array.data, width, height, 3 * width, QImage.Format.Format_RGB888)
        elif channels == 4:  # RGBA
            image = QImage(array.data, width, height, 4 * width, QImage.Format.Format_RGBA8888)
        else:
            raise TypeError(f"Unsupported number of channels: {channels}")

    else:
        raise TypeError(f"Unsupported array shape: {array.shape}")

    pixmap = QPixmap.fromImage(image, Qt.ImageConversionFlag.ColorOnly)
    return pixmap


def pythagoran_view_ratio(scene: QGraphicsScene, viewport: QWidget) -> float:
    """
    Calculates the pythagoran of a scene and viewport sizes, returning a ratio of from their respective sizes.

    Returns
    ----------
    float
    """
    sw, sh = scene.sceneRect().size().toTuple()  # type: ignore
    vw, vh = viewport.size().toTuple()  # type: ignore
    return ((sw**2 + sh**2) / (vw**2 + vh**2)) ** 0.5


def clamp_point_to_item(point: QPoint, item: QGraphicsItem) -> QPoint:
    """
    Clamps a given point to the region within a given item..

    Parameters
    ----------
    point: QPoint
        Point to clamp.
    item: QGraphicsItem
        A item to bound the point.

    Returns
    ----------
    QPoint
        Point clamped to image bounds.
    """
    rect = item.boundingRect()
    x_outside = min(point.x(), rect.right())
    y_outside = min(point.y(), rect.bottom())

    x = max(rect.left(), x_outside)
    y = max(rect.top(), y_outside)

    return QPoint(x, y)


def aboslute_scene_size(scene: QGraphicsScene, transform: QTransform) -> Tuple[float, float]:
    """
    Calculate the absolute size of the scene, this takes into account any scale transforms.

    Returns
    ---------
    Tuple[float, float]
        (width, heigth): pixel dimensions

    """
    rect = scene.sceneRect()

    # Get the scaling factors from the transform
    scale_y = transform.m11()  # Vertical scale
    scale_x = transform.m22()  # Horizontal scale

    # Apply the scaling to the scene's bounding rect to get the absolute size
    absolute_height = rect.height() * scale_y
    absolute_width = rect.width() * scale_x
    return absolute_height, absolute_width


def absolute_scene_scale_ratio_of_viewport(
    scene: QGraphicsScene,
    transform: QTransform,
    viewport: QWidget,
    adjustment_ratio: float = 1,
) -> Tuple[float, float]:
    """
    Calculate the ratio of absolute scene size with respect to the viewport.
    ie: `absolute_height / view_height, absolute_width / view_width`
    Providing a value for `adjustment_ratio` will adjust the scene dimensions by this amount, as it is an interpretation of what the size will be.

    Returns
    ----------
    Tuple[float, float]
        (height, width)

    """
    absolute_height, absolute_width = aboslute_scene_size(scene, transform)
    view_height, view_width = viewport.rect().bottomRight().toTuple()  # type: ignore

    # adjust with provided ratio.
    absolute_height *= adjustment_ratio
    absolute_width *= adjustment_ratio

    return absolute_height / view_height, absolute_width / view_width
