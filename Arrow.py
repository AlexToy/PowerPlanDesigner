from PyQt5.QtWidgets import QGraphicsLineItem


class Arrow(QGraphicsLineItem):
    def __init__(self, x_parent, y_parent, width_parent, height_parent, x_child, y_child, height_child):
        super(Arrow, self).__init__()

        self.x_parent = x_parent + width_parent
        self.y_parent = y_parent + (height_parent / 2)
        self.width_parent = width_parent
        self.height_parent = height_parent

        self.x_child = x_child
        self.y_child = y_child + (height_child / 2)
        self.height_child = height_child

        self.update_arrow_position()

    def update_parent_position(self, x_parent, y_parent):
        self.x_parent = x_parent + self.width_parent
        self.y_parent = y_parent + (self.height_parent / 2)
        self.update_arrow_position()

    def update_child_position(self, x_child, y_child):
        self.x_child = x_child
        self.y_child = y_child + (self.height_child / 2)
        self.update_arrow_position()

    def update_arrow_position(self):
        self.setLine(self.x_parent, self.y_parent, self.x_child, self.y_child)