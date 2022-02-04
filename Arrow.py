from PyQt5.QtWidgets import QGraphicsLineItem


class Arrow(QGraphicsLineItem):
    def __init__(self):
        super(Arrow, self).__init__()

        self.x_parent = 0
        self.y_parent = 0
        self.x_child = 0
        self.y_child = 0

        self.update_arrow_position()

    def update_parent_position(self, x_parent, y_parent):
        self.x_parent = x_parent
        self.y_parent = y_parent
        self.update_arrow_position()

    def update_child_position(self, x_child, y_child):
        self.x_child = x_child
        self.y_child = y_child
        self.update_arrow_position()

    def update_arrow_position(self):
        self.setLine(self.x_parent, self.y_parent, self.x_child, self.y_child)