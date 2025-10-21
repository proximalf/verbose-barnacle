from enum import Enum
from typing import Dict, List

from PySide6.QtGui import QColor, QPen
from PySide6.QtWidgets import QGraphicsItem, QGraphicsRectItem, QGraphicsScene


class SceneLayer(Enum):
    Background = 0
    Image = 1
    Middle = 2
    Foreground = 3
    OnTop = 10


class ImageViewerScene(QGraphicsScene):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        # Mock layer effect.
        self._layers: Dict[SceneLayer, List[QGraphicsItem]] = {layer: [] for layer in SceneLayer}

    def add_item(self, item: QGraphicsItem, layer: SceneLayer = SceneLayer.Foreground) -> None:
        """
        Add a graphics item to scene, and set the Z value.
        """
        self.addItem(item)
        item.setZValue(layer.value)

    def show_layer(self, layer: SceneLayer, state: bool = False) -> None:
        """
        Set whether a given layer is visible or not.
        """
        for item in self._layers[layer]:
            item.setVisible(state)

    def debug(self):
        """
        Draws a box surrounding the sceneRect for debugging.
        """
        rect = QGraphicsRectItem(self.sceneRect())
        pen = QPen(QColor("red"))
        pen.setWidth(2)
        rect.setPen(pen)
        rect.setZValue(-1000)  # Behind everything else
        self.addItem(rect)
