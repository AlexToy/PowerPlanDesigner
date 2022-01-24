from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton
from AddElement import AddElement
from Dcdc import Dcdc
from DcdcWidget import DcdcWidget


class PagePowerPlan(QWidget):
    def __init__(self, parent=None):
        super(PagePowerPlan, self).__init__(parent)

        self.layout = QGridLayout()

        self.add_new_element_button = QPushButton("+")
        self.add_new_element_button.clicked.connect(self.open_add_element)
        self.layout.addWidget(self.add_new_element_button, 0, 0)

        self.add_element = AddElement()
        self.add_element.dcdc_selected.connect(self.add_new_element)

        self.list_element = []
        self.list_element_widget = []

        self.setLayout(self.layout)

    def open_add_element(self):
        self.add_element.show()

    def add_new_element(self, dcdc: Dcdc):
        # Create a copy from a database dcdc
        new_dcdc = Dcdc(dcdc.ref_component, dcdc.supplier, dcdc.current_max, dcdc.equivalence_code,
                        dcdc.voltage_input_min, dcdc.voltage_input_max, dcdc.voltage_output_min,
                        dcdc.voltage_output_max)
        new_dcdc.voltage_input = dcdc.voltage_input
        new_dcdc.voltage_output = dcdc.voltage_output
        new_dcdc.name = dcdc.name

        # Create the graphical widget of dcdc
        new_dcdc_widget = DcdcWidget(new_dcdc)

        # Add new_dcdc_widget to the layout
        self.layout.addWidget(new_dcdc_widget, 0, 0)

        # Close add_element window
        self.add_element.close()

        # Add the new element in the list
        self.list_element.append(new_dcdc)
        self.list_element_widget.append(new_dcdc_widget)
        for element in self.list_element:
            print("Element from current elements :" + element.name)