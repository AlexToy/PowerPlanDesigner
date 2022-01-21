from PyQt5.QtWidgets import QTabWidget, QScrollArea, QGroupBox, QHBoxLayout, QGridLayout, QPushButton, QTextEdit, \
    QLabel, QVBoxLayout
from PyQt5 import QtCore
from loading_database import loading_database
from Dcdc import Dcdc
from Psu import Psu
from Consumer import Consumer


class AddElement(QTabWidget):
    # This class loads the database, asks the user which element they want to add to their page (graphical widget) and
    # sends the page a copy of the chosen element

    # Signal
    dcdc_selected = QtCore.pyqtSignal(object)

    def __init__(self, parent=None):
        super(AddElement, self).__init__(parent)

        # 1 import the database
        self.list_dcdc_database, self.list_psu_database, self.list_consumer_database = loading_database()

        # 2 Graphical widget
        # DC/DC
        self.tab_dcdc = QScrollArea()
        self.tab_dcdc_layout = QVBoxLayout()
        for dcdc in self.list_dcdc_database:
            self.select_dcdc_widget = SelectDcdcWidget(dcdc)
            self.select_dcdc_widget.clicked_add_dcdc.connect(self.send_dcdc_selected)
            self.tab_dcdc_layout.addWidget(self.select_dcdc_widget)
        self.tab_dcdc.setLayout(self.tab_dcdc_layout)

        # TODO : PSU
        self.tab_psu = QScrollArea()
        # TODO : LDO
        self.tab_ldo = QScrollArea()
        # TODO : SWITCH
        self.tab_switch = QScrollArea()
        # TODO : CONSUMER
        self.tab_consumer = QScrollArea()

        self.addTab(self.tab_dcdc, "DC/DC")
        self.addTab(self.tab_psu, "PSU")
        self.addTab(self.tab_ldo, "LDO")
        self.addTab(self.tab_switch, "SWITCH")
        self.addTab(self.tab_consumer, "CONSUMER")

        self.setWindowTitle("Add new element")

    def send_dcdc_selected(self, dcdc_copy: Dcdc):
        self.dcdc_selected.emit(dcdc_copy)


class SelectDcdcWidget(QGroupBox):
    # Signal
    clicked_add_dcdc = QtCore.pyqtSignal(object)

    def __init__(self, dcdc, parent=None):
        super(SelectDcdcWidget, self).__init__(parent)

        # Create a copy from a database dcdc
        self.dcdc_copy = Dcdc(dcdc.ref_component, dcdc.supplier, dcdc.current_max, dcdc.equivalence_code,
                              dcdc.voltage_input_min, dcdc.voltage_input_max, dcdc.voltage_output_min,
                              dcdc.voltage_output_max)

        # creation of widget & layout
        self.layout = QHBoxLayout()
        self.layout_2 = QGridLayout()
        self.add_dcdc_button = QPushButton("Add")
        self.name_label = QLabel("Name : ")
        self.name = QTextEdit()
        self.v_in_label = QLabel("Vin : ")
        self.v_in = QTextEdit()
        self.v_out_label = QLabel("Vout : ")
        self.v_out = QTextEdit()
        self.text = QLabel("Info DCDC")

        # layout
        self.layout_2.addWidget(self.name_label, 0, 0)
        self.layout_2.addWidget(self.name, 0, 1)
        self.layout_2.addWidget(self.v_in_label, 1, 0)
        self.layout_2.addWidget(self.v_in, 1, 1)
        self.layout_2.addWidget(self.v_out_label, 2, 0)
        self.layout_2.addWidget(self.v_out, 2, 1)
        self.layout_2.addWidget(self.add_dcdc_button, 3, 0, 1, 2)
        self.layout.addWidget(self.text)
        self.layout.addLayout(self.layout_2)

        # Widget settings
        self.add_dcdc_button.clicked.connect(self.clicked_button_function)
        self.add_dcdc_button.setFixedSize(150, 25)
        self.name.setFixedSize(150, 25)
        self.v_in.setFixedSize(150, 25)
        self.v_out.setFixedSize(150, 25)
        self.setTitle(self.dcdc_copy.ref_component)
        self.setLayout(self.layout)

    def clicked_button_function(self):
        if self.name.toPlainText() != "" and self.v_in.toPlainText() != "" and self.v_out.toPlainText() != "" and \
                self.pos_x.toPlainText() != "" and self.pos_y.toPlainText() != "":

            if float(self.dcdc_copy.voltage_input_min) <= float(self.v_in.toPlainText()) <= float(
                    self.dcdc_copy.voltage_input_max):

                if float(self.dcdc_copy.voltage_output_min) <= float(self.v_out.toPlainText()) <= float(
                        self.dcdc_copy.voltage_output_max):

                    # Add user parameters to the DC/DC
                    self.dcdc_copy.voltage_input = self.v_in.toPlainText()
                    self.dcdc_copy.voltage_output = self.v_out.toPlainText()
                    self.dcdc_copy.name = self.name.toPlainText()

                    # Send dcdc_selected signal
                    self.clicked_add_dcdc.emit(self.dcdc_copy)

                    # TODO : Deleted this class and AddElement class

                else:
                    print("DEBUG : Output voltage is not in the DC/DC Scope !")
            else:
                print("DEBUG : Input voltage is not in the DC/DC Scope !")
        else:
            print("DEBUG : Some fields are empty !")
