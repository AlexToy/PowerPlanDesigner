from PyQt5.QtWidgets import QGroupBox, QHBoxLayout, QGridLayout, QPushButton, QLineEdit, QLabel, QVBoxLayout
from PyQt5.QtGui import QDoubleValidator
from PyQt5 import QtCore
from Components.SwitchWidget import SwitchWidget


class SelectSwitchWidget(QGroupBox):
    # Signal
    clicked_add_component = QtCore.pyqtSignal(object)

    def __init__(self, switch: SwitchWidget, parent=None):
        super(SelectSwitchWidget, self).__init__(parent)

        # Get dcdc from database
        self.switch_copy = switch

        # creation of widget & layout
        self.layout = QHBoxLayout()
        self.layout_1 = QVBoxLayout()
        self.layout_2 = QGridLayout()
        self.add_switch_button = QPushButton("Add")
        self.name_label = QLabel("Name : ")
        self.name = QLineEdit()
        self.v_in_label = QLabel("Voltage : ")
        self.v_in = QLineEdit()
        self.supplier_label = QLabel(self.switch_copy.supplier)
        self.ref_label = QLabel(self.switch_copy.ref_component)
        self.code_equiv_label = QLabel(self.switch_copy.equivalence_code)
        self.label_restriction = QDoubleValidator(0, 100, 2)

        # layout
        self.layout_2.addWidget(self.name_label, 0, 0)
        self.layout_2.addWidget(self.name, 0, 1)
        self.layout_2.addWidget(self.v_in_label, 1, 0)
        self.layout_2.addWidget(self.v_in, 1, 1)
        self.layout_2.addWidget(self.add_switch_button, 2, 0, 1, 2)

        self.layout_1.addWidget(self.supplier_label)
        self.layout_1.addWidget(self.ref_label)
        self.layout_1.addWidget(self.code_equiv_label)

        self.layout.addLayout(self.layout_1)
        self.layout.addLayout(self.layout_2)

        # Widget settings
        self.add_switch_button.clicked.connect(self.clicked_button_function)
        # self.add_dcdc_button.setFixedSize(150, 25)
        self.name.setFixedSize(150, 25)
        self.v_in.setFixedSize(150, 25)
        # self.v_in.setValidator(self.label_restriction)
        self.setTitle(self.switch_copy.switch_type + " " + str(self.switch_copy.current_max) + " A")
        self.setLayout(self.layout)

    def clicked_button_function(self):
        if self.name.displayText() != "" and self.v_in.displayText() != "":

            if float(self.switch_copy.voltage_input_min) <= float(self.v_in.displayText()) <= float(
                    self.switch_copy.voltage_input_max):

                # Add user parameters to the DC/DC
                self.switch_copy.voltage_input = self.v_in.displayText()
                self.switch_copy.name = self.name.displayText()

                # Send dcdc_selected signal
                self.clicked_add_component.emit(self.switch_copy)

                # Clear parameters
                self.name.setText("")
                self.v_in.setText("")

            else:
                print("DEBUG : Input voltage is not in the DC/DC Scope !")
        else:
            print("DEBUG : Some fields are empty !")

    def get_widget_filters(self):
        return self.switch_copy.dict_filters

    def get_name(self):
        return self.switch_copy.ref_component

    def value_is_present(self, filter_name, try_value):
        if self.switch_copy.dict_filters[filter_name] == try_value:
            return True
        else:
            return False
