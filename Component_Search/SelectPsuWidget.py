from PyQt5.QtWidgets import QGroupBox, QGridLayout, QPushButton, QLineEdit, QLabel
from PyQt5 import QtCore
from Components.PsuWidget import PsuWidget


class SelectPsuWidget(QGroupBox):
    # Signal
    clicked_add_component = QtCore.pyqtSignal(object)

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
            self.clicked_add_component.emit(self.psu)
            # Clear parameters
            self.name.setText("")
        else:
            print("DEBUG : The name is empty !")

    def get_widget_filters(self):
        return self.psu.list_filter

    def get_widget(self):
        return self.psu
