from PyQt5.QtWidgets import QWidget
from PyQt5 import QtCore


class Dcdc(QWidget):
    # Signals
    parameters_is_updated = QtCore.pyqtSignal(str)
    add_child_clicked = QtCore.pyqtSignal(str)

    def __init__(self, ref_component, supplier, current_max, equivalence_code, voltage_input_min, voltage_input_max,
                 voltage_output_min, voltage_output_max):
        #  Fixed parameters
        self.ref_component = ref_component
        self.supplier = supplier
        self.current_max = current_max
        self.equivalence_code = equivalence_code
        self.voltage_input_min = voltage_input_min
        self.voltage_input_max = voltage_input_max
        self.voltage_output_min = voltage_output_min
        self.voltage_output_max = voltage_output_max

        # Dynamic parameters
        self.name = ""
        self.signal_control = 0
        self.voltage_input = 0
        self.voltage_output = 0
        self.current_input = 0
        self.current_output = 0
        self.power_input = 0
        self.power_output = 0
        self.efficiency = 90
        self.power_dissipation = 0

        self.parent = 0
        self.children = []

    def add_parent(self, parent):
        self.parent = parent
        print("DEBUG : add " + parent.name + "as parent to " + self.name)

    def remove_parent(self):
        print("DEBUG : remove " + self.parent.name + "as parent to " + self.name)
        self.parent = 0

    def add_child(self, child) -> bool:
        # Add a child to the dcdc children list
        # If return True, the child is added on the list and you must add this dcdc as a parent to the child
        # Else, action aborted
        if float(self.voltage_output) == float(child.voltage_input):
            self.children.append(child)
            # Update parameters
            self.update_input_output_parameters()
            print("DEBUG : add " + child.name + " as child to " + self.name)
            return True
        else:
            print("DEBUG : " + str(self.voltage_output) + "'s output voltage is different from " + str(
                child.voltage_input) + "'s")
            return False

    def remove_child(self, remove_child):
        if len(self.children) != 0:
            # Find the good child in the children list
            for index in range(len(self.children)):
                if self.children[index].name == remove_child.name:
                    # Remove child to the dcdc children list
                    print("DEBUG : remove " + self.children[index].name + " as child to " + self.name)
                    del self.children[index]
                    # Update parameters
                    self.update_input_output_parameters()
                else:
                    print("DEBUG : " + self.children[index].name + " not find in the children list !")
        else:
            print("DEBUG : " + self.name + " has no children !")

    def update_input_output_parameters(self):
        # Editing output parameters
        self.power_output = 0
        if len(self.children) != 0:
            for child in self.children:
                self.power_output = float(self.power_output) + float(child.power_input)
        self.current_output = float(self.power_output) / float(self.voltage_output)

        # Editing input parameters
        self.power_input = float(self.power_output) * (float(self.efficiency) / 100)
        self.current_input = float(self.power_input) / float(self.voltage_input)

        # Tell to the parent that the parameters have been changed
        self.parameters_is_updated.emit(self.parent.name)

    def print_parameters(self):
        print(self.name)
        print("Vin : " + str(self.voltage_input) + " V")
        print("Iin : " + str(self.current_input) + " mA")
        print("Pin : " + str(self.power_input) + " mW")
        print("Vout : " + str(self.voltage_output) + " V")
        print("Iout : " + str(self.current_output) + " mA")
        print("Pout : " + str(self.power_output) + " mW")
        if self.parent != 0:
            print("Parent : " + str(self.parent.name))
        else:
            print("No parents !")
        for child in self.children:
            print("Child : " + str(child.name))