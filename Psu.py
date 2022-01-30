from PyQt5.QtWidgets import QWidget
from PyQt5 import QtCore


class Psu(QWidget):
    # Signals
    update_parameters = QtCore.pyqtSignal()

    def __init__(self, ref_component: str, supplier: str, equivalence_code: str, current_max: float,
                 voltage_input: float, voltage_output: float, jack: str,  parent=None):
        super(Psu, self).__init__(parent)

        #  Fixed parameters
        self.ref_component = ref_component
        self.supplier = supplier
        self.equivalence_code = equivalence_code
        self.current_max = current_max
        self.voltage_output = voltage_output
        self.voltage_input = voltage_input
        self.jack = jack
        self.component = "PSU"

        # Dynamic parameters
        self.name = ""
        self.current_output = 0
        self.power_output = 0

        self.children = []

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

        # Update graphics parameters
        self.update_parameters.emit()

