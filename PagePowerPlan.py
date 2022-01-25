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
        self.button_right = AddElementButton("Right")
        self.button_right.clicked_button.connect(self.open_add_element)
        self.button_right.pos_x = 0
        self.button_right.pos_y = 0
        self.layout.addWidget(self.button_right,self.button_right.pos_x, self.button_right.pos_y, QtCore.Qt.AlignCenter)

        # The second button is used when there is a widget on the page
        self.button_bottom = AddElementButton("Bottom")
        self.button_bottom.clicked_button.connect(self.open_add_element)
        self.button_bottom.pos_x = -1
        self.button_bottom.pos_y = 1

        # Add element page
        self.add_element = AddElement()
        self.add_element.dcdc_selected.connect(self.add_new_element)

        self.list_element = []
        self.list_element_widget = []

        self.setLayout(self.layout)

    def open_add_element(self, widget_location: str, pos_x: int, pos_y: int):
        print("DEBUG : Button " + widget_location + " clicked")
        print("DEBUG : Position " + str(pos_x) + str(pos_y))
        self.add_element.set_widget_position(widget_location, pos_x, pos_y)
        self.add_element.show()

    def add_new_element(self, dcdc: Dcdc, location: str, pos_x: int, pos_y: int):
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
        self.graphic_update(new_dcdc_widget, location, pos_x, pos_y)

        # Close add_element window
        self.add_element.close()

        # Add the new element in the list
        self.list_element.append(new_dcdc)
        self.list_element_widget.append(new_dcdc_widget)

    def graphic_update(self, dcdc_widget, location: str, pos_x: int, pos_y: int):
        # Calculate the new buttons positions
        if location == "Right":
            self.button_right.pos_x = self.button_right.pos_x + 1
            self.button_bottom.pos_x = self.button_bottom.pos_x + 1
        elif location == "Bottom":
            self.button_right.pos_y = self.button_right.pos_y + 1
            self.button_bottom.pos_y = self.button_bottom.pos_y + 1
        # Add buttons to their new position
        self.layout.addWidget(self.button_right, self.button_right.pos_y, self.button_right.pos_x, QtCore.Qt.AlignLeft)
        self.layout.addWidget(self.button_bottom, self.button_bottom.pos_y, self.button_bottom.pos_x, QtCore.Qt.AlignTop)
        # Add the widget to its new position
        self.layout.addWidget(dcdc_widget, pos_y, pos_x)

class AddElementButton(QPushButton):
    #Signal
    clicked_button = QtCore.pyqtSignal(str, int, int)

    def __init__(self, widget_location, parent=None):
        super(AddElementButton, self).__init__(parent)

        self.setText("+")
        self.setFixedSize(50, 50)
        self.pos_x = 0
        self.pos_y = 0
        self.widget_location = widget_location

        self.clicked.connect(self.clicked_button_function)

    def clicked_button_function(self):
        self.clicked_button.emit(self.widget_location, self.pos_x, self.pos_y)