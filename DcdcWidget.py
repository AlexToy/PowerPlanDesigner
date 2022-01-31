from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QGraphicsProxyWidget, QPushButton
from PyQt5.QtCore import QPointF, Qt
from PyQt5 import QtCore
from Dcdc import Dcdc


INITIAL_POS_X = 50
INITIAL_POS_Y = 50


class DcdcWidget(QGraphicsProxyWidget):

    # Signal
    widget_selected = QtCore.pyqtSignal(object)

    def __init__(self, dcdc: Dcdc, parent=None):
        super(DcdcWidget, self).__init__(parent)

        self.dcdc = dcdc
        self.dcdc.update_parameters.connect(self.update_graphics_parameters)
        self.grp_box = QGroupBox()
        self.component = "DCDC"

        self.move_grpbox = False

        # Layouts
        self.v_layout = QVBoxLayout()
        self.h_layout_1 = QHBoxLayout()
        self.h_layout_2 = QHBoxLayout()
        self.grid_layout = QGridLayout()

        # Line 1
        self.component_label = QLabel("DCDC ")
        self.current_max_label = QLabel(str(self.dcdc.current_max) + " A")
        self.h_layout_1.addWidget(self.component_label)
        self.h_layout_1.addWidget(self.current_max_label)

        # Line 2
        self.ref_component_label = QLabel(self.dcdc.ref_component + " ")
        self.supplier_label = QLabel(self.dcdc.supplier + " ")
        self.h_layout_2.addWidget(self.ref_component_label)
        self.h_layout_2.addWidget(self.supplier_label)

        # Line 3
        self.equivalence_code_label = QLabel(self.dcdc.equivalence_code)

        # Line 4
        self.line_label = QLabel("----------------------------------")

        # Grid Layout
        # Input
        self.input_label = QLabel("Input")
        self.voltage_in_label = QLabel(str(self.dcdc.voltage_input) + " V")
        self.current_in_label = QLabel(str(self.dcdc.current_input) + " mA")
        self.power_in_label = QLabel(str(self.dcdc.power_input) + " mW")
        self.grid_layout.addWidget(self.input_label, 0, 0)
        self.grid_layout.addWidget(self.voltage_in_label, 1, 0)
        self.grid_layout.addWidget(self.current_in_label, 2, 0)
        self.grid_layout.addWidget(self.power_in_label, 3, 0)

        # DC/DC Consumption
        self.power_dissipation_label = QLabel("- " + str(self.dcdc.power_dissipation) + " W")
        self.efficiency_label = QLabel("- %")
        self.grid_layout.addWidget(self.power_dissipation_label, 2, 1)
        self.grid_layout.addWidget(self.efficiency_label, 3, 1)

        # Output
        self.output_label = QLabel("Output")
        self.voltage_out_label = QLabel(str(self.dcdc.voltage_output) + " V")
        self.current_out_label = QLabel(str(self.dcdc.current_output) + " mA")
        self.power_out_label = QLabel(str(self.dcdc.power_output) + " mW")
        self.grid_layout.addWidget(self.output_label, 0, 2)
        self.grid_layout.addWidget(self.voltage_out_label, 1, 2)
        self.grid_layout.addWidget(self.current_out_label, 2, 2)
        self.grid_layout.addWidget(self.power_out_label, 3, 2)

        # Layouts
        self.v_layout.addLayout(self.h_layout_1)
        self.v_layout.addLayout(self.h_layout_2)
        self.v_layout.addWidget(self.equivalence_code_label)
        self.v_layout.addWidget(self.line_label)
        self.v_layout.addLayout(self.grid_layout)

        # Widget Settings
        self.grp_box.setTitle(str(self.dcdc.name))
        self.grp_box.setLayout(self.v_layout)
        # self.grp_box.setFixedSize(150, 200)

        self.setPos(INITIAL_POS_X, INITIAL_POS_Y)
        self.setWidget(self.grp_box)

    def add_parent(self, element):
        if element.component == "DCDC":
            self.dcdc.add_parent(element.dcdc)
        elif element.component == "Psu":
            self.dcdc.add_parent(element.psu)
        elif element.component == "Consumer":
            self.dcdc.add_parent(element.consumer)

    def add_child(self, element):
        if element.component == "DCDC":
            self.dcdc.add_child(element.dcdc)
        elif element.component == "Psu":
            self.dcdc.add_child(element.psu)
        elif element.component == "Consumer":
            self.dcdc.add_child(element.consumer)

        self.update_graphics_parameters()

    def get_children(self):
        return self.dcdc.children

    def remove_all_children(self):
        self.dcdc.remove_all_children()

    def get_parent(self):
        if self.dcdc.parent != 0:
            return self.dcdc.parent
        else:
            print("DEBUG : No parent ")
            return 0

    def update_graphics_parameters(self):
        # Input parameters
        self.voltage_in_label.setText(str(self.dcdc.voltage_input) + " V")
        self.current_in_label.setText(str(self.dcdc.current_input) + " mA")
        self.power_in_label.setText(str(self.dcdc.power_input) + " mW")

        # Output parameters
        self.voltage_out_label.setText(str(self.dcdc.voltage_output) + " V")
        self.current_out_label.setText(str(self.dcdc.current_output) + " mA")
        self.power_out_label.setText(str(self.dcdc.power_output) + " mW")

        # Update parent parameters
        if self.dcdc.parent != 0:
            self.dcdc.parent.update_input_output_parameters()

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
