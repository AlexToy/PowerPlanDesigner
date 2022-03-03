from PyQt5.QtWidgets import QTabWidget, QScrollArea, QGroupBox, QHBoxLayout, QGridLayout, QPushButton, QLineEdit, \
    QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QDoubleValidator
from PyQt5 import QtCore
from loading_database import loading_database
from Components.DcdcWidget import DcdcWidget
from Components.PsuWidget import PsuWidget
from Components.LdoWidget import LdoWidget
from Components.SwitchWidget import SwitchWidget
from AddComponentConsumer import AddComponentConsumer


class AddElement(QTabWidget):
    # This class loads the database, asks the user which element they want to add to their page (graphical widget) and
    # sends the page a copy of the chosen element

    # Signal
    dcdc_selected = QtCore.pyqtSignal(object)

    def __init__(self, parent=None):
        super(AddElement, self).__init__(parent)

        # 1 Import the database
        self.list_dcdc_database, self.list_psu_database, self.list_ldo_database, self.list_consumer_database, \
        self.list_switch_database = loading_database()

        # 2 Graphical widget
        # DC/DC
        self.tab_dcdc = QScrollArea()
        self.widget_dcdc = QWidget()
        self.tab_dcdc_layout = QVBoxLayout()
        for dcdc in self.list_dcdc_database:
            self.select_dcdc_widget = SelectDcdcWidget(dcdc)
            self.select_dcdc_widget.clicked_add_dcdc.connect(self.send_element_selected)
            self.tab_dcdc_layout.addWidget(self.select_dcdc_widget)
        self.widget_dcdc.setLayout(self.tab_dcdc_layout)
        self.tab_dcdc.setWidget(self.widget_dcdc)

        # PSU
        self.tab_psu = QScrollArea()
        self.widget_psu = QWidget()
        self.tab_psu_layout = QVBoxLayout()
        for psu in self.list_psu_database:
            self.select_psu_widget = SelectPsuWidget(psu)
            self.select_psu_widget.clicked_add_psu.connect(self.send_element_selected)
            self.tab_psu_layout.addWidget(self.select_psu_widget)
        self.widget_psu.setLayout(self.tab_psu_layout)
        self.tab_psu.setWidget(self.widget_psu)

        # LDO
        self.tab_ldo = QScrollArea()
        self.widget_ldo = QWidget()
        self.tab_ldo_layout = QVBoxLayout()
        for ldo in self.list_ldo_database:
            self.select_ldo_widget = SelectLdoWidget(ldo)
            self.select_ldo_widget.clicked_add_ldo.connect(self.send_element_selected)
            self.tab_ldo_layout.addWidget(self.select_ldo_widget)
        self.widget_ldo.setLayout(self.tab_ldo_layout)
        self.tab_ldo.setWidget(self.widget_ldo)

        # SWITCH
        self.tab_switch = QScrollArea()
        self.widget_switch = QWidget()
        self.tab_switch_layout = QVBoxLayout()
        for switch in self.list_switch_database:
            self.select_switch_widget = SelectSwitchWidget(switch)
            self.select_switch_widget.clicked_add_switch.connect(self.send_element_selected)
            self.tab_switch_layout.addWidget(self.select_switch_widget)
        self.widget_switch.setLayout(self.tab_switch_layout)
        self.tab_switch.setWidget(self.widget_switch)

        # CONSUMER
        self.tab_consumer = AddComponentConsumer(self.list_consumer_database)
        self.tab_consumer.add_consumer.connect(self.send_element_selected)

        self.addTab(self.tab_dcdc, "DC/DC")
        self.addTab(self.tab_psu, "PSU")
        self.addTab(self.tab_ldo, "LDO")
        self.addTab(self.tab_switch, "SWITCH")
        self.addTab(self.tab_consumer, "CONSUMER")

        self.setWindowTitle("Add new element")

    def send_element_selected(self, element):
        self.dcdc_selected.emit(element)


class SelectDcdcWidget(QGroupBox):
    # Signal
    clicked_add_dcdc = QtCore.pyqtSignal(object)

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
                    self.clicked_add_dcdc.emit(self.dcdc_copy)

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


class SelectLdoWidget(QGroupBox):
    # Signal
    clicked_add_ldo = QtCore.pyqtSignal(object)

    def __init__(self, ldo: LdoWidget, parent=None):
        super(SelectLdoWidget, self).__init__(parent)

        # Get dcdc from database
        self.ldo_copy = ldo

        # creation of widget & layout
        self.layout = QHBoxLayout()
        self.layout_1 = QVBoxLayout()
        self.layout_2 = QGridLayout()
        self.add_ldo_button = QPushButton("Add")
        self.name_label = QLabel("Name : ")
        self.name = QLineEdit()
        self.v_in_label = QLabel("Vin : ")
        self.v_in = QLineEdit()
        self.current_label = QLabel(str(self.ldo_copy.current_max) + " A")
        self.voltage_input_label = QLabel("Vin : " + str(self.ldo_copy.voltage_input_min) + " V - " +
                                          str(self.ldo_copy.voltage_input_max) + " V")
        self.voltage_output_label = QLabel("Vout : " + str(self.ldo_copy.voltage_output) + " V")
        self.label_restriction = QDoubleValidator(0, 100, 2)

        # layout
        self.layout_2.addWidget(self.name_label, 0, 0)
        self.layout_2.addWidget(self.name, 0, 1)
        self.layout_2.addWidget(self.v_in_label, 1, 0)
        self.layout_2.addWidget(self.v_in, 1, 1)
        self.layout_2.addWidget(self.add_ldo_button, 2, 0, 1, 2)

        self.layout_1.addWidget(self.current_label)
        self.layout_1.addWidget(self.voltage_input_label)
        self.layout_1.addWidget(self.voltage_output_label)

        self.layout.addLayout(self.layout_1)
        self.layout.addLayout(self.layout_2)

        # Widget settings
        self.add_ldo_button.clicked.connect(self.clicked_button_function)
        # self.add_dcdc_button.setFixedSize(150, 25)
        self.name.setFixedSize(150, 25)
        self.v_in.setFixedSize(150, 25)
        # self.v_in.setValidator(self.label_restriction)
        self.setTitle(self.ldo_copy.ref_component)
        self.setLayout(self.layout)

    def clicked_button_function(self):
        if self.name.displayText() != "" and self.v_in.displayText() != "":

            if float(self.ldo_copy.voltage_input_min) <= float(self.v_in.displayText()) <= float(
                    self.ldo_copy.voltage_input_max):

                # Add user parameters to the DC/DC
                self.ldo_copy.voltage_input = self.v_in.displayText()
                self.ldo_copy.name = self.name.displayText()

                # Send dcdc_selected signal
                self.clicked_add_ldo.emit(self.ldo_copy)

                # Clear parameters
                self.name.setText("")
                self.v_in.setText("")

            else:
                print("DEBUG : Input voltage is not in the DC/DC Scope !")
        else:
            print("DEBUG : Some fields are empty !")


class SelectSwitchWidget(QGroupBox):
    # Signal
    clicked_add_switch = QtCore.pyqtSignal(object)

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
                self.clicked_add_switch.emit(self.switch_copy)

                # Clear parameters
                self.name.setText("")
                self.v_in.setText("")

            else:
                print("DEBUG : Input voltage is not in the DC/DC Scope !")
        else:
            print("DEBUG : Some fields are empty !")


class SelectPsuWidget(QGroupBox):
    # Signal
    clicked_add_psu = QtCore.pyqtSignal(object)

    def __init__(self, psu: PsuWidget, parent=None):
        super(SelectPsuWidget, self).__init__(parent)

        # Get psu from database
        self.psu = psu

        # creation of widget & layout
        self.layout = QGridLayout()
        self.line_1 = QLabel("PSU " + self.psu.supplier + " " + str(self.psu.current_max))
        self.line_2 = QLabel(str(self.psu.voltage_input) + " / " + str(self.psu.voltage_output))
        self.line_3 = QLabel("Jack : " + self.psu.jack)
        self.line_4 = QLabel(self.psu.equivalence_code)
        self.name_label = QLabel("Name : ")
        self.name = QLineEdit()
        self.add_psu_button = QPushButton("Add")

        # Layout
        self.layout.addWidget(self.line_1, 0, 0)
        self.layout.addWidget(self.line_2, 1, 0)
        self.layout.addWidget(self.line_3, 2, 0)
        self.layout.addWidget(self.line_4, 3, 0)
        self.layout.addWidget(self.name_label, 0, 1)
        self.layout.addWidget(self.name, 0, 2)
        self.layout.addWidget(self.add_psu_button, 4, 1)

        # Widget settings
        self.add_psu_button.clicked.connect(self.clicked_button_function)
        self.name.setFixedSize(150, 25)
        self.setTitle("PSU")
        self.setLayout(self.layout)

    def clicked_button_function(self):
        if self.name.displayText() != "":
            # Add user parameters to the PSU
            self.psu.name = self.name.displayText()
            # Emit the signal
            self.clicked_add_psu.emit(self.psu)
            # Clear parameters
            self.name.setText("")
        else:
            print("DEBUG : The name is empty !")
