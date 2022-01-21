from PyQt5.QtWidgets import QWidget


class Psu(QWidget):
    def __init__(self, name, voltage_input, voltage_output, current, parent=None):

        #  Fixed parameters
        self.name = name
        self.voltage_input = voltage_input
        self.voltage_output = voltage_output
        self.current_output = current
