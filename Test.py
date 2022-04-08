from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsItem, QGraphicsProxyWidget, QPushButton, QGraphicsRectItem
from PyQt5.QtGui import QPainter, QColor, QBrush
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from Components.DcdcWidget import DcdcWidget


class View(QGraphicsView):

    def __init__(self):
        super(View, self).__init__()

        item = DcdcWidget("MP16", "MPS", 3, "Froced PWM", "2100000", 4.2, 20, 1, 12, None)
        item.name = "yoo"

        # on place le point de pivot des transformation au niveau du pointeur
        """self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorViewCenter)"""
        # on cache les scrollBar
        """self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)"""

        # active l’antialiasing
        self.setRenderHint(QPainter.Antialiasing)

        # creation du scene qui contient les items et sera dans la QView
        self.scene = QGraphicsScene()
        self.scene.setSceneRect(-50000, -50000, 100000, 100000)

        # Ajout d'une grille en fond
        self.setBackgroundBrush(QBrush(QColor(60, 60, 60), QtCore.Qt.CrossPattern))

        # creation de deux elipse simple a la scene, selectable et movable
        # item = QGraphicsRectItem(0, 0, 300, 300)
        # proxy = QGraphicsProxyWidget(item)

        # item.setFlag(QGraphicsItem.ItemIsMovable, True)
        # item.setFlag(QGraphicsItem.ItemIsSelectable, True)

        # proxy.setWidget(dcdc)
        epS = self.scene.addEllipse(20, 120, 50, 50)
        epS.setFlag(QGraphicsItem.ItemIsMovable, True)
        epS.setFlag(QGraphicsItem.ItemIsSelectable, True)

        # parametrage du drag mode  rubber …. permet davoir un lasso rectangulaire de selection
        # self.setRubberBandSelectionMode(Qt.IntersectsItemShape)
        self.setScene(self.scene)
        self.scene.addItem(item.ui_init())
        self.setDragMode(QGraphicsView.RubberBandDrag)
    # alt drag scroll bar, permet de se deplacer dans le graph grace a la touche alt.

    def keyPressEvent(self, event):
        QGraphicsView.keyPressEvent(self, event)
        if event.key() == QtCore.Qt.Key_Alt:
            self.setDragMode(QGraphicsView.ScrollHandDrag)

    def keyReleaseEvent(self, event):
        QGraphicsView.keyReleaseEvent(self, event)
        if event.key() == QtCore.Qt.Key_Alt:
            self.setDragMode(QGraphicsView.RubberBandDrag)

    def mousePressEvent(self, event):
        QGraphicsView.mousePressEvent(self, event)
        print("yo")
"""      
    def wheelEvent(self, event):
        zoom = event.angleDelta().y()
        if zoom > 0:
            factor = 1.2
        else:
            factor = 0.8
        self.scale(factor, factor)

   def mousePressEvent(self, event):
        self.init_mouse_pos = event.pos()

        self.setDragMode(QGraphicsView.RubberBandDrag)

        # Select an item
        self.item = self.itemAt(event.pos())
        print(self.item)

        # Move an item on the scene
        if event.button() == Qt.LeftButton:
            # Left click --> Move an item on the scene or drag rubber band
            self.move_scene_locked = True
            if self.item is not None:
                self.move_item_locked = False
                self.item.item_clicked_from_scene()
                self.delta_mouse_item_pos = self.item.scenePos() - self.mapToScene(self.init_mouse_pos)
            else:
                self.move_item_locked = True
                # Rubber band
                # self.rubber_band.setGeometry(QRect(self.init_mouse_pos, QSize()))
                # self.rubber_band.show()

        elif event.button() == Qt.RightButton:
            self.setDragMode(QGraphicsView.ScrollHandDrag)
            # Right click --> Move the view on the scene
            self.move_scene_locked = False
            self.move_item_locked = True
            QApplication.setOverrideCursor(Qt.OpenHandCursor)

    def mouseMoveEvent(self, event):
        update_mouse_pos = event.pos()
        new_pos_map = self.mapToScene(event.pos())

        # Move an item on the scene
        if not self.move_item_locked:
            updated_cursor_x = new_pos_map.x() + self.delta_mouse_item_pos.x()
            updated_cursor_y = new_pos_map.y() + self.delta_mouse_item_pos.y()
            self.item.setPos(QPointF(updated_cursor_x, updated_cursor_y))
            self.item.item_moved_from_scene(updated_cursor_x, updated_cursor_y)

        elif self.move_item_locked and self.move_scene_locked:
            pass
            # self.rubber_band.setGeometry(QRect(self.init_mouse_pos, update_mouse_pos).normalized())

        # Move the view of the scene
        if not self.move_scene_locked:
            QApplication.changeOverrideCursor(Qt.ClosedHandCursor)

            orig_scene_position = self.sceneRect()
            print(orig_scene_position)
            updated_cursor_x = (update_mouse_pos.x()) + orig_scene_position.x()
            updated_cursor_y = (update_mouse_pos.y()) + orig_scene_position.y()
            # self.setSceneRect(updated_cursor_x, updated_cursor_y, 500, 500)

    def mouseReleaseEvent(self, event):
        self.item = None
        self.move_item_locked = True
        self.move_scene_locked = True
        QApplication.changeOverrideCursor(Qt.ArrowCursor)
        # self.rubber_band.hide()
"""


