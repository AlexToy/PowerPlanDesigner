from PyQt5.QtWidgets import QTabWidget, QScrollArea, QGroupBox, QHBoxLayout, QGridLayout, QPushButton, QTextEdit, \
    QLabel, QVBoxLayout
from PyQt5 import QtCore
from loading_database import loading_database
from DcdcWidget import DcdcWidget
from PsuWidget import PsuWidget
from ConsumerWidget import ConsumerWidget


class AddElement(QTabWidget):
    # This class loads the database, asks the user which element they want to add to their page (graphical widget) and
    # sends the page a copy of the chosen element

    # Signal
    dcdc_selected = QtCore.pyqtSignal(object)

    def __init__(self, parent=None):
        super(AddElement, self).__init__(parent)

        # 1 Import the database
        self.list_dcdc_database, self.list_psu_database, self.list_consumer_database = loading_database()

        # 2 Graphical widget
        # DC/DC
        self.tab_dcdc = QScrollArea()
        self.tab_dcdc_layout = QVBoxLayout()
        for dcdc in self.list_dcdc_database:
            self.select_dcdc_widget = SelectDcdcWidget(dcdc)
            self.select_dcdc_widget.clicked_add_dcdc.connect(self.send_element_selected)
            self.tab_dcdc_layout.addWidget(self.select_dcdc_widget)
        self.tab_dcdc.setLayout(self.tab_dcdc_layout)

        # PSU
        self.tab_psu = QScrollArea()
        self.tab_psu_layout = QVBoxLayout()
        for psu in self.list_psu_database:
            self.select_psu_widget = SelectPsuWidget(psu)
            self.select_psu_widget.clicked_add_psu.connect(self.send_element_selected)
            self.tab_psu_layout.addWidget(self.select_psu_widget)
        self.tab_psu.setLayout(self.tab_psu_layout)

        # LDO
        self.tab_consumer = QScrollArea()
        self.tab_consumer_layout = QVBoxLayout()
        for consumer in self.list_consumer_database:
            self.select_consumer_widget = SelectConsumerWidget(consumer)
            self.select_consumer_widget.clicked_add_consumer.connect(self.send_element_selected)
            self.tab_consumer_layout.addWidget(self.select_consumer_widget)
        self.tab_consumer.setLayout(self.tab_consumer_layout)

        # TODO : SWITCH
        self.tab_switch = QScrollArea()
        # TODO : LDO
        self.tab_ldo = QScrollArea()

        self.addTab(self.tab_dcdc, "DC/DC")
        self.addTab(self.tab_psu, "PSU")
        self.addTab(self.tab_ldo, "LDO")
        self.addTab(self.tab_switch, "SWITCH")
        self.addTab(self.tab_consumer, "CONSUMER")

        self.setWindowTitle("Add new element")
        self.setFixedSize(600, 600)

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
        # self.add_dcdc_button.setFixedSize(150, 25)
        self.name.setFixedSize(150, 25)
        self.v_in.setFixedSize(150, 25)
        self.v_out.setFixedSize(150, 25)
        self.setTitle(self.dcdc_copy.ref_component)
        self.setLayout(self.layout)

    def clicked_button_function(self):
        if self.name.toPlainText() != "" and self.v_in.toPlainText() != "" and self.v_out.toPlainText() != "":

            if float(self.dcdc_copy.voltage_input_min) <= float(self.v_in.toPlainText()) <= float(self.dcdc_copy.voltage_input_max):

                if float(self.dcdc_copy.voltage_output_min) <= float(self.v_out.toPlainText()) <= float(self.dcdc_copy.voltage_output_max):

                    # Add user parameters to the DC/DC
                    self.dcdc_copy.voltage_input = self.v_in.toPlainText()
                    self.dcdc_copy.voltage_output = self.v_out.toPlainText()
                    self.dcdc_copy.name = self.name.toPlainText()

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
        self.name = QTextEdit()
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
        if self.name.toPlainText() != "":
            # Add user parameters to the PSU
            self.psu.name = self.name.toPlainText()
            # Emit the signal
            self.clicked_add_psu.emit(self.psu)
            # Clear parameters
            self.name.setText("")
        else:
            print("DEBUG : The name is empty !")


class SelectConsumerWidget(QGroupBox):
    # Signal
    clicked_add_consumer = QtCore.pyqtSignal(object)

    def __init__(self, consumer: ConsumerWidget, parent=None):
        super(SelectConsumerWidget, self).__init__(parent)

        # Get consumer from database
        self.consumer = consumer

        # creation of widget & layout
        self.layout = QGridLayout()
        self.line_1 = QLabel(self.consumer.ref_component)
        self.line_2 = QLabel(self.consumer.info)
        self.line_3 = QLabel(self.consumer.equivalence_code)
        self.add_consumer_button = QPushButton("Add")

        # Layout
        self.layout.addWidget(self.line_1, 0, 0)
        self.layout.addWidget(self.line_2, 1, 0)
        self.layout.addWidget(self.line_3, 2, 0)
        self.layout.addWidget(self.add_consumer_button, 0, 1)

        # Widget settings
        self.add_consumer_button.clicked.connect(self.clicked_button_function)
        self.setTitle(self.consumer.name)
        self.setLayout(self.layout)

    def clicked_button_function(self):
        self.clicked_add_consumer.emit(self.consumer)