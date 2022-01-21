from PyQt5.QtWidgets import QWidget


class Consumer(QWidget):
    def __init__(self, name, text, voltage, current, parent=None):

        #  Fixed parameters
        self.name = name
        self.text = text
        self.voltage_input = voltage
        self.current_input = current
        self.power_input = float(self.voltage_input) * float(self.current_input)

        self.parent = 0
        self.children = []

    def print_parameters(self):
        print(self.name)
        print("Vin : " + str(self.voltage_input) + " V")
        print("Iin : " + str(self.current_input) + " mA")
        print("Pin : " + str(self.power_input) + " mW")

    def add_parent(self, parent):
        self.parent = parent
        print("DEBUG : add " + parent.name + "as parent to " + self.name)

    def remove_parent(self):
        print("DEBUG : remove " + self.parent.name + "as parent to " + self.name)
        self.parent = 0