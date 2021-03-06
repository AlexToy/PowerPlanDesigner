from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QWidget
from PyQt5 import QtCore
from Components.GraphicsProxyWidget import GraphicsProxyWidget

INITIAL_POS_X = 200
INITIAL_POS_Y = 200


def get_voltage_input_usage(voltage_input_max):
    if voltage_input_max > 20:
        return str("20 V")
    elif voltage_input_max < 12:
        return str("<= 5 V")
    else:
        return str("12 V")


class DcdcWidget(QWidget):
    # Signal
    widget_selected = QtCore.pyqtSignal(object)

    def __init__(self, ref_component: str, supplier: str, current_max: float, mode: str, equivalence_code: str,
                 voltage_input_min: float, voltage_input_max: float, voltage_output_min: float,
                 voltage_output_max: float, efficiency_formula, parent=None):
        super(DcdcWidget, self).__init__(parent)

        #  Fixed parameters
        self.ref_component = ref_component
        self.supplier = supplier
        self.current_max = current_max
        self.mode = mode
        self.equivalence_code = equivalence_code
        self.voltage_input_min = voltage_input_min
        self.voltage_input_max = voltage_input_max
        self.voltage_output_min = voltage_output_min
        self.voltage_output_max = voltage_output_max
        self.voltage_input_usage = get_voltage_input_usage(self.voltage_input_max)
        self.efficiency_formula = efficiency_formula
        self.efficiency_is_set = False
        self.component = "DCDC"
        self.dict_filters = {"Output Current": self.current_max, "Mode": self.mode,
                             "Input voltage": self.voltage_input_usage}

        # Dynamic parameters
        self.name = ""
        self.signal_control = 0
        self.voltage_input = 0
        self.voltage_output = 0
        self.current_input = 0
        self.current_output = 0
        self.power_input = 0
        self.power_output = 0
        self.efficiency = 0
        self.power_dissipation = 0

        # UI Parameters
        self.voltage_in_label = QLabel()
        self.current_in_label = QLabel()
        self.power_in_label = QLabel()
        self.power_dissipation_label = QLabel()
        self.efficiency_label = QLabel()
        self.voltage_out_label = QLabel()
        self.current_out_label = QLabel()
        self.power_out_label = QLabel()

        self.parent = 0
        self.children = []
        # Dict key = child widget & value = arrow
        self.arrows = {}

        self.move_grpbox = False
        self.proxy_widget = GraphicsProxyWidget()

    def ui_init(self):
        self.proxy_widget.widget_clicked.connect(self.send_widget)
        grp_box = QGroupBox()
        grp_box.setObjectName("DCDC_GrpBox")
        # Layouts
        v_layout = QVBoxLayout()
        h_layout_1 = QHBoxLayout()
        h_layout_2 = QHBoxLayout()
        grid_layout = QGridLayout()

        # Line 1
        component_label = QLabel("DCDC ")
        component_label.setObjectName("Bold_Word")
        current_max_label = QLabel(str(self.current_max) + " A")
        h_layout_1.addWidget(component_label)
        h_layout_1.addWidget(current_max_label)

        # Line 2
        ref_component_label = QLabel(self.ref_component + " ")
        supplier_label = QLabel(self.supplier + " ")
        h_layout_2.addWidget(ref_component_label)
        h_layout_2.addWidget(supplier_label)

        # Line 3
        equivalence_code_label = QLabel(self.equivalence_code)

        # Line 4
        line_label = QLabel("----------------------------------")

        # Grid Layout
        # Input
        input_label = QLabel("Input")
        input_label.setObjectName("Bold_Word")
        self.voltage_in_label.setText(str(self.voltage_input) + " V")
        self.voltage_in_label.setObjectName("Voltage")
        self.current_in_label.setText(str(self.current_input) + " mA")
        self.current_in_label.setObjectName("Current")
        self.power_in_label.setText(str(self.power_input) + " mW")
        self.power_in_label.setObjectName("Power")
        grid_layout.addWidget(input_label, 0, 0)
        grid_layout.addWidget(self.voltage_in_label, 1, 0)
        grid_layout.addWidget(self.current_in_label, 2, 0)
        grid_layout.addWidget(self.power_in_label, 3, 0)

        # DC/DC Consumption
        self.power_dissipation_label.setText("- " + str(self.power_dissipation) + " mW")
        self.efficiency_label.setText("- %")
        grid_layout.addWidget(self.power_dissipation_label, 2, 1)
        grid_layout.addWidget(self.efficiency_label, 3, 1)

        # Output
        output_label = QLabel("Output")
        output_label.setObjectName("Bold_Word")
        self.voltage_out_label.setText(str(self.voltage_output) + " V")
        self.voltage_out_label.setObjectName("Voltage")
        self.current_out_label.setText(str(self.current_output) + " mA")
        self.current_out_label.setObjectName("Current")
        self.power_out_label.setText(str(self.power_output) + " mW")
        self.power_out_label.setObjectName("Power")
        grid_layout.addWidget(output_label, 0, 2)
        grid_layout.addWidget(self.voltage_out_label, 1, 2)
        grid_layout.addWidget(self.current_out_label, 2, 2)
        grid_layout.addWidget(self.power_out_label, 3, 2)

        # Layouts
        v_layout.addLayout(h_layout_1)
        v_layout.addLayout(h_layout_2)
        v_layout.addWidget(equivalence_code_label)
        v_layout.addWidget(line_label)
        v_layout.addLayout(grid_layout)

        # Widget Settings
        grp_box.setTitle(str(self.name))
        grp_box.setLayout(v_layout)
        # grp_box.setFixedSize(150, 200)

        self.proxy_widget.setPos(INITIAL_POS_X, INITIAL_POS_Y)
        self.proxy_widget.setWidget(grp_box)

        return self.proxy_widget

    def update_efficiency_value(self):
        if self.efficiency_formula.formula_is_empty:
            if self.efficiency_is_set:
                return
            else:
                self.efficiency = 85
                return

        else:
            # Look for the same voltage input & voltage output
            if self.efficiency_formula.voltage_input == float(self.voltage_input) and \
                    self.efficiency_formula.voltage_output == float(self.voltage_output):
                formula_str = self.efficiency_formula.get_formula_efficiency(self.current_output)
                self.efficiency = eval(formula_str.replace("x", str(self.current_output / 1000)))
                print("DEBUG : New efficiency : " + str(self.efficiency))
                return
            # TODO : Look for the closest formula if the voltage input/output are not in the list of formula
            else:
                self.efficiency = 85
                print("DEBUG : New efficiency : " + str(self.efficiency))
                return

    def add_parent(self, parent):
        if float(self.voltage_input) == float(parent.voltage_output):
            self.parent = parent
            print("DEBUG : add " + parent.name + "as parent to " + self.name)
            return True
        else:
            print("DEBUG : " + str(self.voltage_input) + "'s output voltage is different from " + str(
                parent.voltage_output) + "'s")
            return False

    def remove_parent(self):
        if self.parent != 0:
            print("DEBUG : remove " + self.parent.name + "as parent to " + self.name)
        self.parent = 0

    def get_parent(self):
        return self.parent

    def add_child(self, child) -> bool:
        # Add a child to the dcdc children list
        # If return True, the child is added on the list and you must add this dcdc as a parent to the child
        # Else, action aborted
        if float(self.voltage_output) == float(child.voltage_input):
            self.children.append(child)
            # Update parameters
            self.update_parameters()
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
                if self.children[index] == remove_child:
                    # Remove child to the dcdc children list
                    print("DEBUG : remove " + self.children[index].name + " as child to " + self.name)
                    del self.children[index]
                    # Update parameters
                    self.update_parameters()
                    return
                else:
                    print("DEBUG : " + self.children[index].name + " not find in the children list !")
        else:
            print("DEBUG : " + self.name + " has no children !")

    def remove_all_children(self):
        if len(self.children) != 0:
            for child in self.children:
                self.children.remove(child)
            print("DEBUG : All children removed !")
        else:
            print("DEBUG : Any children in the list ! ")

    def get_children(self):
        if len(self.children) != 0:
            return self.children
        else:
            return 0

    def update_parameters(self):
        # Editing output parameters
        self.power_output = 0
        if len(self.children) != 0:
            for child in self.children:
                self.power_output = float(self.power_output) + float(child.power_input)
        self.current_output = float(self.power_output) / float(self.voltage_output)

        # Efficiency parameter
        self.update_efficiency_value()

        # Editing input parameters
        self.power_input = float(self.power_output) * (float(self.efficiency) / 100)
        self.current_input = float(self.power_input) / float(self.voltage_input)

        # Power dissipation parameter
        self.power_dissipation = self.power_output - self.power_input

        # Update graphics parameters
        self.update_graphics_parameters()

    def update_graphics_parameters(self):
        # Input parameters
        self.voltage_in_label.setText(str(self.voltage_input) + " V")
        self.current_in_label.setText(str(round(self.current_input, 1)) + " mA")
        self.power_in_label.setText(str(round(self.power_input, 1)) + " mW")

        # Efficiency parameter
        self.efficiency_label.setText(str(round(self.efficiency, 1)) + " %")

        # Output parameters
        self.voltage_out_label.setText(str(self.voltage_output) + " V")
        self.current_out_label.setText(str(round(self.current_output, 1)) + " mA")
        self.power_out_label.setText(str(round(self.power_output, )) + " mW")

        # Power dissipation parameter
        self.power_dissipation_label.setText(str(round(self.power_dissipation, 1)) + " W")

        # Update parent parameters
        if self.parent != 0:
            self.parent.update_parameters()

    def send_widget(self):
        self.widget_selected.emit(self)
