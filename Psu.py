from PyQt5.QtWidgets import QWidget


class Psu(QWidget):
    def __init__(self, ref_component: str, supplier: str, equivalence_code: str, current_max: float,
                 voltage_input: float, voltage_output: float, jack: str,  parent=None):

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
