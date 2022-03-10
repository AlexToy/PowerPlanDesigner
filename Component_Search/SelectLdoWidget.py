from PyQt5.QtWidgets import QGroupBox, QHBoxLayout, QGridLayout, QPushButton, QLineEdit, QLabel, QVBoxLayout
from PyQt5.QtGui import QDoubleValidator
from PyQt5 import QtCore
from Components.LdoWidget import LdoWidget


class SelectLdoWidget(QGroupBox):
    # Signal
    clicked_add_component = QtCore.pyqtSignal(object)

    def __init__(self, ldo: LdoWidget, parent=None):
        super(SelectLdoWidget, self).__init__(parent)

        # Get dcdc from database
        self.ldo_copy = ldo
        self.setObjectName("LDO_addElement_GrpBox")

        # creation of widget & layout
        self.layout = QHBoxLayout()
        self.layout_1 = QVBoxLayout()
        self.layout_2 = QGridLayout()
        self.add_ldo_button = QPushButton("Add")
        self.name_label = QLabel("Name : ")
        self.name = QLineEdit()
        self.v_in_label = QLabel("Vin : ")
        self.v_in = QLineEdit()
        self.equiv_code_label = QLabel(str(self.ldo_copy.equivalence_code))
        self.ref_label = QLabel(self.ldo_copy.ref_component)
        self.supplier_label = QLabel(self.ldo_copy.supplier)
        self.label_restriction = QDoubleValidator(0, 100, 2)

        # layout
        self.layout_2.addWidget(self.name_label, 0, 0)
        self.layout_2.addWidget(self.name, 0, 1)
        self.layout_2.addWidget(self.v_in_label, 1, 0)
        self.layout_2.addWidget(self.v_in, 1, 1)
        self.layout_2.addWidget(self.add_ldo_button, 2, 0, 1, 2)

        self.layout_1.addWidget(self.supplier_label)
        self.layout_1.addWidget(self.ref_label)
        self.layout_1.addWidget(self.equiv_code_label)

        self.layout.addLayout(self.layout_1)
        self.layout.addLayout(self.layout_2)

        # Widget settings
        self.add_ldo_button.clicked.connect(self.clicked_button_function)
        # self.add_dcdc_button.setFixedSize(150, 25)
        self.name.setFixedSize(150, 25)
        self.v_in.setFixedSize(150, 25)
        # self.v_in.setValidator(self.label_restriction)
        self.setTitle("LDO   " + str(self.ldo_copy.voltage_output) + " V   " +
                      str(self.ldo_copy.current_max * 1000) + " mA")
        self.setLayout(self.layout)

    def clicked_button_function(self):
        if self.name.displayText() != "" and self.v_in.displayText() != "":

            if float(self.ldo_copy.voltage_input_min) <= float(self.v_in.displayText()) <= float(
                    self.ldo_copy.voltage_input_max):

                # Add user parameters to the DC/DC
                self.ldo_copy.voltage_input = self.v_in.displayText()
                self.ldo_copy.name = self.name.displayText()

                # Send dcdc_selected signal
                self.clicked_add_component.emit(self.ldo_copy)

                # Clear parameters
                self.name.setText("")
                self.v_in.setText("")

            else:
                print("DEBUG : Input voltage is not in the DC/DC Scope !")
        else:
            print("DEBUG : Some fields are empty !")

    def get_widget_filters(self):
        return self.ldo_copy.dict_filters

    def get_name(self):
        return self.ldo_copy.ref_component

    def value_is_present(self, filter_name, try_value):
        if self.ldo_copy.dict_filters[filter_name] == try_value:
            return True
        else:
            return False
