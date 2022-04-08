from PyQt5.QtWidgets import QGraphicsProxyWidget, QGraphicsItem
from PyQt5 import QtCore


class GraphicsProxyWidget(QGraphicsProxyWidget):
    # Signal
    widget_clicked = QtCore.pyqtSignal()
    new_widget_position = QtCore.pyqtSignal(float, float)
    widget_resizing = QtCore.pyqtSignal(float, float, float, float)

    def __init__(self, parent=None):
        super(GraphicsProxyWidget, self).__init__(parent)

        self.widget_pos_x = 0
        self.widget_pos_y = 0
        self.height = 0
        self.width = 0

    def item_clicked_from_scene(self):
        self.widget_clicked.emit()

    def item_moved_from_scene(self, pos_x, pos_y):
        print("yo")
        self.widget_pos_x = pos_x
        self.widget_pos_y = pos_y
        self.new_widget_position.emit(pos_x, pos_y)

    """def resizeEvent(self, event):
        self.height = event.newSize().height()
        self.width = event.newSize().width()
        self.widget_resizing.emit(self.height, self.width, self.widget_pos_x, self.widget_pos_y)"""
