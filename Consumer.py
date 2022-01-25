from PyQt5.QtWidgets import QWidget


class Consumer(QWidget):
    def __init__(self, name: str, ref_component: str, info: str, equivalence_code: str,
                 voltage_input: float, current_input: float, parent=None):

        #  Fixed parameters
        self.name = name
        self.ref_component = ref_component
        self.info = info
        self.equivalence_code = equivalence_code
        self.voltage_input = voltage_input
        self.current_input = current_input
        self.power_input = voltage_input * current_input
        self.component = "Consumer"

