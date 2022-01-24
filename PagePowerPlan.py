from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton
from PyQt5 import QtCore
from AddElement import AddElement
from Dcdc import Dcdc
from DcdcWidget import DcdcWidget


class PagePowerPlan(QWidget):

    # Signal
    clicked_button = QtCore.pyqtSignal(str, int, int)

    def __init__(self, parent=None):
        super(PagePowerPlan, self).__init__(parent)

        # Widget for pagePowerPlan
        self.layout = QGridLayout()

        # Initial state, only one button is on the page at the pos : (0,0)
        self.button_right = QPushButton("+")
        self.button_right.setFixedSize(50, 50)
        self.button_right_pos_x = 0
        self.button_right_pos_y = 0
        self.button_right.clicked.connect(self.open_add_element_right_button)
        self.layout.addWidget(self.button_right, self.button_right_pos_y, self.button_right_pos_x)

        # The second button is used when there is a widget on the page
        self.button_bottom = QPushButton("+")
        self.button_bottom.setFixedSize(50, 50)
        self.button_bottom_pos_x = 0
        self.button_bottom_pos_y = 0
        self.button_bottom.clicked.connect(self.open_add_element_bottom_button)

        # Add element page
        self.add_element = AddElement()
        self.add_element.dcdc_selected.connect(self.add_new_element)

        self.list_element = []
        self.list_element_widget = []

        self.setLayout(self.layout)

    def open_add_element_right_button(self):
        print("DEBUG : Right button clicked")
        self.add_element.set_pos_x_y(self.button_right_pos_x, self.button_right_pos_y)
        self.add_element.set_adding_button("Right")
        self.add_element.show()

    def open_add_element_bottom_button(self):
        print("DEBUG : Bottom button clicked")
        self.add_element.set_pos_x_y(self.button_bottom_pos_x, self.button_bottom_pos_y)
        self.add_element.set_adding_button("Bottom")
        self.add_element.show()

    def add_new_element(self, dcdc: Dcdc, pos_x: int, pos_y: int, adding_button: str):
        # Create a copy from a database dcdc
        new_dcdc = Dcdc(dcdc.ref_component, dcdc.supplier, dcdc.current_max, dcdc.equivalence_code,
                        dcdc.voltage_input_min, dcdc.voltage_input_max, dcdc.voltage_output_min,
                        dcdc.voltage_output_max)
        new_dcdc.voltage_input = dcdc.voltage_input
        new_dcdc.voltage_output = dcdc.voltage_output
        new_dcdc.name = dcdc.name

        # Create the graphical widget of dcdc
        new_dcdc_widget = DcdcWidget(new_dcdc)

        # Adding dcdc on the page
        self.graphic_update(new_dcdc_widget, pos_x, pos_y, adding_button)

        # Close add_element window
        self.add_element.close()

        # Add the new element in the list
        self.list_element.append(new_dcdc)
        self.list_element_widget.append(new_dcdc_widget)
        for element in self.list_element:
            print("Element from current elements :" + element.name)

    def graphic_update(self, dcdc_widget, pos_x: int, pos_y: int, adding_button: str):
        self.layout.addWidget(dcdc_widget, pos_y, pos_x)
        if adding_button == "Right":
            self.layout.addWidget(self.button_right, pos_x + 1, pos_y)
            self.layout.addWidget(self.button_bottom, pos_x + 1, pos_y)
        elif adding_button == "Bottom":
            self.layout.addWidget(self.button_right, pos_x + 1, pos_y + 1)
            self.layout.addWidget(self.button_bottom, pos_x + 1, pos_y + 1)


class add_element_button(QPushButton):
    #Signal
    clicked_button = QtCore.pyqtSignal(str, int, int)

    def __init__(self, parent=None):
        super(add_element_button, self).__init__(parent)

        self.pos_x = 0
        self.pos_y = 0
        self.widget_position = ""

        self.clicked.connect(self.clicked_button_function)

    def clicked_button_function(self):
        self.clicked_button.emit(self.widget_position, self.pos_x, self.pos_y)