from typing import Optional, Tuple

from PySide6.QtCore import QPointF, Qt, Signal
from PySide6.QtGui import QCursor, QKeyEvent, QMouseEvent, QPainter, QWheelEvent
from PySide6.QtWidgets import QGraphicsView

from .lib import absolute_scene_scale_ratio_of_viewport

DELTA_SCALE = 0.05  # Rate of change x% an update
MAX_ZOOM_IN_RATIO = 40  # 40x zoom
MAX_ZOOM_OUT_RATIO = 0.7  # 0.7x zoom
DRAG_MODE_DEFAULT = False  # Do not enable drag mode on initialisation
MOUSE_TRACKING = True
LOCK_MOUSE_TRACKING_TO_SCENE = True  # Setting this to false will break alot of stuff.


class ImageViewer(QGraphicsView):
    """
    An implementation of QGraphicsView for viewing images, partially inspired by pyqtGraph.
    The signals emitted return coordinates relative to the scene.
    """

    signal_key_pressed: Signal = Signal(QKeyEvent)
    signal_zoom_changed: Signal = Signal(float)
    # Mapped to scene position
    signal_mouse_position: Signal = Signal(QPointF)
    signal_mouse_pressed: Signal = Signal(QPointF, Qt.MouseButton)
    signal_mouse_released: Signal = Signal(QPointF, Qt.MouseButton)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._drag_mode = DRAG_MODE_DEFAULT
        self.setMouseTracking(MOUSE_TRACKING)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)

    def absolute_scene_scale_ratio_of_viewport(self, adjustment_ratio: float = 1.0) -> Tuple[float, float]:
        """
        Returns the absolute scale of the the scene with respect to the viewport.
        """
        return absolute_scene_scale_ratio_of_viewport(
            scene=self.scene(),
            transform=self.transform(),
            viewport=self.viewport(),
            adjustment_ratio=adjustment_ratio,
        )

    def reset_view(self) -> None:
        """
        Reset the view to the current largest items bounding rect.
        If there are no items the method call is ignored.
        """
        self.fitInView(self.scene().sceneRect(), aspectRadioMode=Qt.AspectRatioMode.KeepAspectRatio)

    def zoom(self, direction: int, rate: float = DELTA_SCALE) -> None:
        """
        Zoom on displayed scene. Rate cannot be greater than or equal to 1.
        If the zoom would exceed bounds set by `MAX_ZOOM_[min/max]_RATIO` the the reqeust is ignored.

        Parameters
        ----------
        direction: int
            The direction to zoom, positive int is in, negative is out.
        rate: float
            The rate at which to zoom, this applies to both, so a percentage of the rate.
            eg: IN -> 1 + rate, out -> 1 - rate.
        """
        if rate >= 1:
            raise Exception(f"Rate cannot be greater than or equal to 1. Rate: {rate} ")
        # direction positive - zoom in.
        # direction negative - zoom out.
        zoom = 1 + rate if direction > 0 else 1 - rate

        # calculate the size of the scene will be and ignore if the scene exceeds set bounds.
        scale_ratio = self.absolute_scene_scale_ratio_of_viewport(zoom)
        # we take the smallest value when zooming out and largest when zooming in
        # this corrasponds with which ever dimension is the largest.
        zoom_ratio = min(scale_ratio) if direction > 0 else max(scale_ratio)

        # zoom, otherwise return.
        cant_zoom_in = zoom_ratio > MAX_ZOOM_IN_RATIO and direction > 0
        cant_zoom_out = zoom_ratio < MAX_ZOOM_OUT_RATIO and direction < 0
        if cant_zoom_in or cant_zoom_out:
            return

        # the same value for scale to maintain aspect
        self.scale(zoom, zoom)

        self.signal_zoom_changed.emit(min(scale_ratio))

    def set_drag_mode(self, drag: bool = True) -> None:
        """
        Set the drag mode on the view.
        """
        self._drag_mode = drag
        if drag:
            self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        else:
            self.setDragMode(QGraphicsView.DragMode.NoDrag)

    def emit_cursor_position(self, event: Optional[QMouseEvent] = None) -> None:
        """
        Emits the cursor position from global context to within the scene.
        If a QMouseEvent is supplied the position of the event is used instead.
        """
        if not LOCK_MOUSE_TRACKING_TO_SCENE:
            return

        cursor_pos = self.mapFromGlobal(QCursor.pos()) if event is None else event.pos()

        # emit if in scene
        scene_position = self.mapToScene(cursor_pos)
        if self.scene().sceneRect().contains(scene_position):
            self.signal_mouse_position.emit(scene_position)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        """
        Emits key presses as a signal.
        """
        self.signal_key_pressed.emit(event)
        return super().keyPressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        """
        Handle mouse move events. If mouse is moved outside of scene bounds it is ignored.
        When the mouse moves a signal is emitted, this position has been mapped to scene.
        """
        self.emit_cursor_position(event)
        super().mouseMoveEvent(event)

    def wheelEvent(self, event: QWheelEvent) -> None:
        """
        Handle mouse wheel events.

        If modifier is held pass events on to normal scroll area functionality.
        Otherwise zoom.
        """
        modifier_held = event.modifiers()

        if modifier_held:
            super().wheelEvent(event)
            return

        # Angle delta refers to mousewheel movement, x will be zero, unless its a fancy mouse.
        if event.angleDelta().y() > 0:
            self.zoom(1)
        else:
            self.zoom(-1)
        event.ignore()

        self.emit_cursor_position()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        """
        Reimplemented method.
        Handle mouse press event.
        """
        button = event.button()
        scene_position = self.mapToScene(event.pos())
        self.signal_mouse_pressed.emit(scene_position, event.button())

        if button == Qt.MouseButton.MiddleButton:
            # switch on click
            self.set_drag_mode(not self._drag_mode)

        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        """
        Reimplemented method.
        Handle mouse release event.
        """
        scene_position = self.mapToScene(event.pos())
        self.signal_mouse_released.emit(scene_position, event.button())
        super().mouseReleaseEvent(event)

    def mouseDoubleClickEvent(self, event) -> None:
        """
        Handle double click
        """
        ...
