from PyQt5.QtWidgets import QGraphicsScene, QApplication, QGraphicsRectItem, QGraphicsRectItem, QRubberBand
from PyQt5.QtCore import QPointF, Qt, QRectF, QSize, QRect
from PyQt5.QtGui import QTransform, QPainterPath, QPainter

SPEED_MOVE_FACTOR = 0.6


class GraphicsScene(QGraphicsScene):

    def __init__(self, parent=None):
        super(GraphicsScene, self).__init__(parent)

        self.move_scene_locked = True
        self.move_item_locked = True
        self.item = None

    def mousePressEvent(self, event):
        self.item = self.itemAt(event.scenePos(), QTransform())

        if event.button() == Qt.LeftButton:
            # Left click --> Move an item on the scene
            self.move_scene_locked = True
            self.move_item_locked = False
            if self.item is not None:
                self.setFocusItem(self.item)
                self.item.item_clicked_from_scene()

        elif event.button() == Qt.RightButton:
            # Right click --> Move the view on the scene
            self.move_scene_locked = False
            self.move_item_locked = True
            self.orig_cursor_position = event.lastScenePos()
            self.orig_scene_position = self.sceneRect()
            QApplication.setOverrideCursor(Qt.OpenHandCursor)

    def mouseMoveEvent(self, event):

        # Move an item on the scene
        if self.item is not None and not self.move_item_locked:
            orig_item_position = self.item.scenePos()
            updated_cursor_x = updated_cursor_position.x() - orig_cursor_position.x() + orig_item_position.x()
            updated_cursor_y = updated_cursor_position.y() - orig_cursor_position.y() + orig_item_position.y()
            self.item.setPos(QPointF(updated_cursor_x, updated_cursor_y))
            self.item.item_moved_from_scene(updated_cursor_x, updated_cursor_y)

        # Move the view of the scene
        if not self.move_scene_locked:
            QApplication.changeOverrideCursor(Qt.ClosedHandCursor)
            updated_cursor_position = event.scenePos()
            print(updated_cursor_position)
            dx = (updated_cursor_position.x() - self.orig_cursor_position.x()) * SPEED_MOVE_FACTOR
            dy = (updated_cursor_position.y() - self.orig_cursor_position.y()) * SPEED_MOVE_FACTOR
            updated_cursor_x = self.orig_scene_position.x() + dx
            updated_cursor_y = self.orig_scene_position.y() + dy
            self.setSceneRect(updated_cursor_x, updated_cursor_y, 500, 500)

    def mouseReleaseEvent(self, event):
        self.item = None
        self.move_item_locked = True
        self.move_scene_locked = True
        QApplication.changeOverrideCursor(Qt.ArrowCursor)