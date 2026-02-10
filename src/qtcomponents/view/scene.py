from enum import Enum
from typing import Dict, List, Optional

from PIL.Image import logger
from PySide6.QtCore import QPointF
from PySide6.QtGui import QColor, QPen, QTransform
from PySide6.QtWidgets import QGraphicsItem, QGraphicsRectItem, QGraphicsScene


class SceneLayer(Enum):
    Background = 0
    Image = 1
    OverLayImage = 2
    Foreground = 3
    OnTop = 10


class ImageViewerScene(QGraphicsScene):
    """
    A Scene with some mock layers, as defined by the `SceneLayer` enum.
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.drawn_debug = False # If debug is called, do not redraw.

        # Generate Layers
        # Mock layer effect.
        self._layers: Dict[SceneLayer, List[QGraphicsItem]] = {layer: [] for layer in SceneLayer}

    def add_item(self, item: QGraphicsItem, layer: SceneLayer = SceneLayer.Foreground) -> None:
        """
        Add a graphics item to scene, and set the Z value.
        """
        if item in self.scene_items():
            logger.warning(f"Warn: Already added to scene. {item}")
            return

        self.addItem(item)
        item.setZValue(layer.value)
        self._layers[layer].append(item)

    def show_layer(self, layer: SceneLayer, state: bool = False) -> None:
        """
        Set whether a given layer is visible or not.
        """
        for item in self._layers[layer]:
            item.setVisible(state)

    def remove_item(self, item: QGraphicsItem, layer: SceneLayer = SceneLayer.Foreground) -> None:
        """
        Remove item from a given layer, default is SceneLayer.Foreground.
        If item has not been added nothing happens.
        """
        if item not in self._layers[layer]:
            logger.debug(f"SceneWarning: Item has not been added removed! - {item}")
            return

        self.removeItem(item)

        try:
            self._layers[layer].remove(item)
        except Exception:
            logger.warning(f"Item already removed!: {item}")

    def debug(self):
        """
        Shows scene rect, can only be called once, subsequent calls are ignored.
        """        
        if self.drawn_debug:
            return

        self.drawn_debug = True
        rect = QGraphicsRectItem(self.sceneRect())
        pen = QPen(QColor("red"))
        pen.setWidth(2)
        rect.setPen(pen)
        rect.setZValue(10000)  # Above everything else
        self.addItem(rect)

    def get_item(self, position: QPointF) -> Optional[QGraphicsItem]:
        """
        Fetches item from under scene position, returns None if clicking on SceneLayer.Image items.
        """
        item = self.itemAt(position, QTransform())

        if item in self._layers[SceneLayer.Image]:
            # Ignore if grabbing image.
            return

        return item

    def scene_items(self) -> List[QGraphicsItem]:
        items = []

        for layer, item_list in self._layers.items():
            items.extend(item_list)

        return items
