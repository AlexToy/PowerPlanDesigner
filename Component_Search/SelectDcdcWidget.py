from PyQt5.QtWidgets import QGroupBox, QHBoxLayout, QGridLayout, QPushButton, QLineEdit, QLabel, QVBoxLayout
from PyQt5.QtGui import QDoubleValidator
from PyQt5 import QtCore
from Components.DcdcWidget import DcdcWidget


class SelectDcdcWidget(QGroupBox):
    # Signal
    clicked_add_component = QtCore.pyqtSignal(object)

    def __init__(self, dcdc: DcdcWidget, parent=None):
        super(SelectDcdcWidget, self).__init__(parent)

        # Get dcdc from database
        self.dcdc_copy = dcdc

        # creation of widget & layout
        self.layout = QHBoxLayout()
        self.layout_1 = QVBoxLayout()
        self.layout_2 = QGridLayout()
        self.add_dcdc_button = QPushButton("Add")
        self.name_label = QLabel("Name : ")
        self.name = QLineEdit()
        self.v_in_label = QLabel("Vin : ")
        self.v_in = QLineEdit()
        self.v_out_label = QLabel("Vout : ")
        self.v_out = QLineEdit()
        self.current_label = QLabel(str(self.dcdc_copy.current_max) + " A")
        self.mode_label = QLabel(self.dcdc_copy.mode)
        self.voltage_input_label = QLabel("Vin : " + str(self.dcdc_copy.voltage_input_min) + " V - " +
                                          str(self.dcdc_copy.voltage_input_max) + " V")
        self.voltage_output_label = QLabel("Vout : " + str(self.dcdc_copy.voltage_output_min) + " V - " +
                                           str(self.dcdc_copy.voltage_output_max) + " V")
        self.label_restriction = QDoubleValidator(0, 100, 2)

        # layout
        self.layout_2.addWidget(self.name_label, 0, 0)
        self.layout_2.addWidget(self.name, 0, 1)
        self.layout_2.addWidget(self.v_in_label, 1, 0)
        self.layout_2.addWidget(self.v_in, 1, 1)
        self.layout_2.addWidget(self.v_out_label, 2, 0)
        self.layout_2.addWidget(self.v_out, 2, 1)
        self.layout_2.addWidget(self.add_dcdc_button, 3, 0, 1, 2)

        self.layout_1.addWidget(self.current_label)
        self.layout_1.addWidget(self.mode_label)
        self.layout_1.addWidget(self.voltage_input_label)
        self.layout_1.addWidget(self.voltage_output_label)

        self.layout.addLayout(self.layout_1)
        self.layout.addLayout(self.layout_2)

        # Widget settings
        self.add_dcdc_button.clicked.connect(self.clicked_button_function)
        # self.add_dcdc_button.setFixedSize(150, 25)
        self.name.setFixedSize(150, 25)
        self.v_in.setFixedSize(150, 25)
        # self.v_in.setValidator(self.label_restriction)
        self.v_out.setFixedSize(150, 25)
        # self.v_out.setValidator(self.label_restriction)
        self.setTitle(self.dcdc_copy.ref_component)
        self.setLayout(self.layout)

    def clicked_button_function(self):
        if self.name.displayText() != "" and self.v_in.displayText() != "" and self.v_out.displayText() != "":

            if float(self.dcdc_copy.voltage_input_min) <= float(self.v_in.displayText()) <= float(
                    self.dcdc_copy.voltage_input_max):

                if float(self.dcdc_copy.voltage_output_min) <= float(self.v_out.displayText()) <= float(
                        self.dcdc_copy.voltage_output_max):

                    # Add user parameters to the DC/DC
                    self.dcdc_copy.voltage_input = self.v_in.displayText()
                    self.dcdc_copy.voltage_output = self.v_out.displayText()
                    self.dcdc_copy.name = self.name.displayText()

                    # Send dcdc_selected signal
                    self.clicked_add_component.emit(self.dcdc_copy)

                    # Clear parameters
                    self.name.setText("")
                    self.v_in.setText("")
                    self.v_out.setText("")

                else:
                    print("DEBUG : Output voltage is not in the DC/DC Scope !")
            else:
                print("DEBUG : Input voltage is not in the DC/DC Scope !")
        else:
            print("DEBUG : Some fields are empty !")

    def get_widget_filters(self):
        return self.dcdc_copy.list_filter

    def get_widget(self):
        return self.dcdc_copy
