from PyQt5.QtWidgets import QWidget


class Consumer(QWidget):
    def __init__(self, name: str, ref_component: str, info: str, equivalence_code: str,
                 voltage_input: float, current_input: float, parent=None):
        super(Consumer, self).__init__(parent)

        #  Fixed parameters
        self.name = name
        self.ref_component = ref_component
        self.info = info
        self.equivalence_code = equivalence_code
        self.voltage_input = voltage_input
        self.current_input = current_input
        self.power_input = voltage_input * current_input
        self.component = "Consumer"

        self.parent = 0

    def add_parent(self, parent):
        if float(self.voltage_input) == float(parent.voltage_output):
            self.parent = parent
            print("DEBUG : add " + parent.name + "as parent to " + self.name)
        else:
            print("DEBUG : " + str(self.voltage_input) + "'s output voltage is different from " + str(
                parent.voltage_output) + "'s")

    def remove_parent(self):
        print("DEBUG : remove " + self.parent.name + "as parent to " + self.name)
        self.parent = 0

