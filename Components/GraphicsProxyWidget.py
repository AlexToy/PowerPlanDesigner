from PyQt5.QtWidgets import QGraphicsProxyWidget
from PyQt5.QtCore import QPointF, Qt
from PyQt5 import QtCore


class GraphicsProxyWidget(QGraphicsProxyWidget):
    # Signal
    widget_clicked = QtCore.pyqtSignal()
    new_widget_position = QtCore.pyqtSignal(float, float)

    def __init__(self, parent=None):
        super(GraphicsProxyWidget, self).__init__(parent)

        self.updated_cursor_x = 0
        self.updated_cursor_y = 0
        self.height = 0
        self.width = 0

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self.move_grpbox = True
        elif event.button() == Qt.LeftButton:
            self.move_grpbox = False
            # Send to the page power plan the widget
            self.widget_clicked.emit()

    def mouseMoveEvent(self, event):
        if self.move_grpbox:
            orig_cursor_position = event.lastScenePos()
            updated_cursor_position = event.scenePos()

            orig_position = self.scenePos()

            self.updated_cursor_x = updated_cursor_position.x() - orig_cursor_position.x() + orig_position.x()
            self.updated_cursor_y = updated_cursor_position.y() - orig_cursor_position.y() + orig_position.y()
            self.setPos(QPointF(self.updated_cursor_x, self.updated_cursor_y))

            # Send the new position to the arrow
            self.new_widget_position.emit(self.updated_cursor_x, self.updated_cursor_y)

    def mouseReleaseEvent(self, event):
        pass

    def resizeEvent(self, event):
        self.height = event.newSize().height()
        self.width = event.newSize().width()