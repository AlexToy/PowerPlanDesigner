from PyQt5.QtWidgets import QGraphicsLineItem


class Arrow(QGraphicsLineItem):
    def __init__(self, x_parent, y_parent, width_parent, height_parent, x_child, y_child, height_child):
        super(Arrow, self).__init__()

        self.arrow_x_parent = x_parent + width_parent
        self.arrow_y_parent = y_parent + (height_parent / 2)
        self.width_parent = width_parent
        self.height_parent = height_parent

        self.arrow_x_child = x_child
        self.arrow_y_child = y_child + (height_child / 2)
        self.height_child = height_child

        self.update_arrow_position()

    def update_parent_position(self, x_parent, y_parent):
        self.arrow_x_parent = x_parent + self.width_parent
        self.arrow_y_parent = y_parent + (self.height_parent / 2)
        self.update_arrow_position()

    def update_parent_size(self, height, width, pos_x, pos_y):
        print("Update parent position")
        self.width_parent = width
        self.height_parent = height
        self.arrow_x_parent = pos_x + self.width_parent
        self.arrow_y_parent = pos_y + (self.height_parent / 2)
        self.update_arrow_position()

    def update_child_position(self, x_child, y_child):
        self.arrow_x_child = x_child
        self.arrow_y_child = y_child + (self.height_child / 2)
        self.update_arrow_position()

    def update_child_size(self, height, width, pos_x, pos_y):
        self.height_child = height
        self.arrow_x_child = pos_x
        self.arrow_y_child = pos_y + (self.height_child / 2)
        self.update_arrow_position()

    def update_arrow_position(self):
        self.setLine(self.arrow_x_parent, self.arrow_y_parent, self.arrow_x_child, self.arrow_y_child)