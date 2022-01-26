from PyQt5.QtWidgets import QGroupBox, QGridLayout, QLabel, QGraphicsProxyWidget
from PyQt5.QtCore import QPointF
from Psu import Psu


INITIAL_POS_X = 50
INITIAL_POS_Y = 50


class PsuWidget(QGraphicsProxyWidget):
    def __init__(self, psu: Psu, parent=None):
        super(PsuWidget, self).__init__(parent)

        self.psu = psu
        self.grp_box = QGroupBox()

        self.layout = QGridLayout()

        # Line 1
        self.psu_label = QLabel("PSU ")
        self.voltage_input_label = QLabel(str(self.psu.voltage_input) + " V")
        self.current_max_label = QLabel(str(self.psu.current_max) + " A")
        self.layout.addWidget(self.psu_label, 0, 0)
        self.layout.addWidget(self.voltage_input_label, 0, 1)
        self.layout.addWidget(self.current_max_label, 0, 2)

        # Line 2
        self.supplier_label = QLabel(self.psu.supplier)
        self.ref_component_label = QLabel(self.psu.ref_component)
        self.layout.addWidget(self.psu_label, 1, 0)
        self.layout.addWidget(self.voltage_input_label, 1, 1)

        # Line 3
        self.equivalence_code_label = QLabel(self.psu.equivalence_code)
        self.layout.addWidget(self.equivalence_code_label, 2, 0)

        # Line 4
        self.jack_label = QLabel("Jack : ")
        self.jack_info_label = QLabel(self.psu.jack)
        self.layout.addWidget(self.jack_label, 3, 0)
        self.layout.addWidget(self.jack_info_label, 3, 1)

        # Line 5
        self.line_label = QLabel("----------------------------------")
        self.layout.addWidget(self.line_label, 4, 0)

        # Line 6
        self.output_label = QLabel("Output")
        self.layout.addWidget(self.output_label, 5, 0)

        # Line 7
        self.voltage_output = QLabel(str(self.psu.voltage_output) + " V")
        self.layout.addWidget(self.voltage_output, 6, 0)

        # Line 8
        self.current_output = QLabel(str(self.psu.current_output) + " A")
        self.layout.addWidget(self.current_output, 7, 0)

        # Line 9
        self.power_output = QLabel(str(self.psu.power_output) + " P")
        self.layout.addWidget(self.power_output, 8, 0)

        # Widget Settings
        self.grp_box.setTitle(str(self.psu.name))
        self.grp_box.setLayout(self.layout)
        self.grp_box.setFixedSize(150, 200)

        self.setPos(INITIAL_POS_X, INITIAL_POS_Y)
        self.setWidget(self.grp_box)

    def mousePressEvent(self, event):
        pass

    def mouseMoveEvent(self, event):
        orig_cursor_position = event.lastScenePos()
        updated_cursor_position = event.scenePos()

        orig_position = self.scenePos()

        updated_cursor_x = updated_cursor_position.x() - orig_cursor_position.x() + orig_position.x()
        updated_cursor_y = updated_cursor_position.y() - orig_cursor_position.y() + orig_position.y()
        self.setPos(QPointF(updated_cursor_x, updated_cursor_y))

    def mouseReleaseEvent(self, event):
        pass
