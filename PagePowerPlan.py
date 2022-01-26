from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton
from PyQt5 import QtCore
from Dcdc import Dcdc
from Psu import Psu
from Consumer import Consumer
from DcdcWidget import DcdcWidget
from PsuWidget import PsuWidget
from ConsumerWidget import ConsumerWidget


class PagePowerPlan(QWidget):

    # Signal
    element_received = QtCore.pyqtSignal(bool)

    def __init__(self, parent=None):
        super(PagePowerPlan, self).__init__(parent)

        # Widget for pagePowerPlan
        self.layout = QGridLayout()

        self.list_element_widget = []

        self.setLayout(self.layout)

    def add_new_element(self, element):
        # Find which is the element
        if element.component == "DCDC":

            # Create a copy from a database dcdc
            dcdc = element
            new_dcdc = Dcdc(dcdc.ref_component, dcdc.supplier, dcdc.current_max, dcdc.equivalence_code,
                            dcdc.voltage_input_min, dcdc.voltage_input_max, dcdc.voltage_output_min,
                            dcdc.voltage_output_max)
            new_dcdc.voltage_input = dcdc.voltage_input
            new_dcdc.voltage_output = dcdc.voltage_output
            new_dcdc.name = dcdc.name

            # Create the graphical widget of dcdc
            new_element_widget = DcdcWidget(new_dcdc)

        elif element.component == "PSU":
            psu = element
            new_psu = Psu(psu.ref_component, psu.supplier, psu.equivalence_code, psu.current_max,
                          psu.voltage_input, psu.voltage_output, psu.jack)
            new_psu.name = psu.name

            # Create the graphical widget of dcdc
            new_element_widget = PsuWidget(new_psu)

        elif element.component == "Consumer":
            consumer = element
            new_consumer = Consumer(consumer.name, consumer.ref_component, consumer.info, consumer.equivalence_code,
                                    consumer.voltage_input, consumer.current_input)

            # Create the graphical widget of dcdc
            new_element_widget = ConsumerWidget(new_consumer)

        # Add the new element in the list
        self.list_element_widget.append(new_element_widget)

        self.element_received.emit(True)