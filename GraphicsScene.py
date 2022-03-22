from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtCore import QPointF, Qt
from PyQt5.QtGui import QTransform
from PyQt5 import QtCore


class GraphicsScene(QGraphicsScene):

    def __init__(self, parent=None):
        super(GraphicsScene, self).__init__(parent)

        self.move_scene_locked = True
        self.move_item_locked = True
        self.item = None

    def mousePressEvent(self, event):
        self.item = self.itemAt(event.scenePos(), QTransform())

        if event.button() == Qt.LeftButton:
            self.move_scene_locked = True
            self.move_item_locked = False
            if self.item is not None:
                self.item.item_clicked_from_scene()

        elif event.button() == Qt.RightButton:
            self.move_scene_locked = False
            self.move_item_locked = True

    def mouseMoveEvent(self, event):

        # Move an item on the scene
        if self.item is not None and not self.move_item_locked:
            orig_cursor_position = event.lastScenePos()
            updated_cursor_position = event.scenePos()
            orig_item_position = self.item.scenePos()

            updated_cursor_x = updated_cursor_position.x() - orig_cursor_position.x() + orig_item_position.x()
            updated_cursor_y = updated_cursor_position.y() - orig_cursor_position.y() + orig_item_position.y()
            self.item.setPos(QPointF(updated_cursor_x, updated_cursor_y))
            self.item.item_moved_from_scene(updated_cursor_x, updated_cursor_y)

        if self.item is None and not self.move_scene_locked:
            print("#############################")
            orig_cursor_position = event.lastScenePos()
            print("Origin cursor : ", orig_cursor_position)
            updated_cursor_position = event.scenePos()
            print("Update cursor : ", updated_cursor_position)
            orig_scene_position = self.sceneRect()
            print("Origin scene : ", orig_scene_position)

            updated_cursor_x = updated_cursor_position.x() - orig_cursor_position.x() + orig_scene_position.x()
            updated_cursor_y = updated_cursor_position.y() - orig_cursor_position.y() + orig_scene_position.y()
            print("New scene pos : ", updated_cursor_x, ", ", updated_cursor_y)

            self.setSceneRect(updated_cursor_x, updated_cursor_y, 500, 500)

    def mouseReleaseEvent(self, event):
        self.item = None
        self.move_item_locked = True
        self.move_scene_locked = True
