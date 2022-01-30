from PyQt5.QtWidgets import QGroupBox, QGridLayout, QLabel, QGraphicsProxyWidget
from PyQt5.QtCore import QPointF, Qt
from PyQt5 import QtCore
from Consumer import Consumer


INITIAL_POS_X = 50
INITIAL_POS_Y = 50


class ConsumerWidget(QGraphicsProxyWidget):

    # Signal
    widget_selected = QtCore.pyqtSignal(object)

    def __init__(self, consumer: Consumer, parent=None):
        super(ConsumerWidget, self).__init__(parent)

        self.consumer = consumer
        self.grp_box = QGroupBox()
        self.component = "Consumer"

        self.move_grpbox = False

        # creation of widget & layout
        self.layout = QGridLayout()
        self.ref_component_label = QLabel(self.consumer.ref_component)
        self.info_label = QLabel(self.consumer.info)
        self.equivalence_code_label = QLabel(self.consumer.equivalence_code)
        self.line_label = QLabel("------------")
        self.input_label = QLabel("Input")
        self.voltage_input_label = QLabel(str(self.consumer.voltage_input) + " V")
        self.current_input_label = QLabel(str(self.consumer.current_input) + " mA")
        self.power_input_label = QLabel(str(self.consumer.power_input) + " mW")

        # Layout
        self.layout.addWidget(self.ref_component_label, 0, 0)
        self.layout.addWidget(self.info_label, 1, 0)
        self.layout.addWidget(self.equivalence_code_label, 2, 0)
        self.layout.addWidget(self.line_label, 3, 0)
        self.layout.addWidget(self.input_label, 4, 0)
        self.layout.addWidget(self.voltage_input_label, 5, 0)
        self.layout.addWidget(self.current_input_label, 6, 0)
        self.layout.addWidget(self.power_input_label, 7, 0)

        # Widget settings
        self.grp_box.setTitle(str(self.consumer.name))
        self.grp_box.setLayout(self.layout)
        # self.grp_box.setFixedSize(150, 200)

        self.setPos(INITIAL_POS_X, INITIAL_POS_Y)
        self.setWidget(self.grp_box)

    def add_parent(self, element):
        if element.component == "DCDC":
            self.consumer.add_parent(element.dcdc)
        elif element.component == "Psu":
            self.consumer.add_parent(element.psu)
        elif element.component == "Consumer":
            self.consumer.add_parent(element.consumer)

    def add_child(self, element):
        print("DEBUG : ConsumerWidget cannot have children !")

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self.move_grpbox = True
        elif event.button() == Qt.LeftButton:
            self.move_grpbox = False
            # Send to the page power plan the widget
            self.widget_selected.emit(self)

    def mouseMoveEvent(self, event):
        if self.move_grpbox:
            orig_cursor_position = event.lastScenePos()
            updated_cursor_position = event.scenePos()

            orig_position = self.scenePos()

            updated_cursor_x = updated_cursor_position.x() - orig_cursor_position.x() + orig_position.x()
            updated_cursor_y = updated_cursor_position.y() - orig_cursor_position.y() + orig_position.y()
            self.setPos(QPointF(updated_cursor_x, updated_cursor_y))

    def mouseReleaseEvent(self, event):
        pass