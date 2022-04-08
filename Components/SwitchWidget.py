from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QWidget
from PyQt5 import QtCore
from Components.GraphicsProxyWidget import GraphicsProxyWidget

INITIAL_POS_X = 50
INITIAL_POS_Y = 50


class SwitchWidget(QWidget):
    # Signal
    widget_selected = QtCore.pyqtSignal(object)

    def __init__(self, type: str, current_max: float, rds_on: float, ref_component: str, supplier: str,
                 equivalence_code: str, voltage_input_min: float, voltage_input_max: float, voltage_bias_min,
                 voltage_bias_max, parent=None):
        super(SwitchWidget, self).__init__(parent)

        #  Fixed parameters
        self.ref_component = ref_component
        self.supplier = supplier
        self.switch_type = type
        self.rds_on = rds_on
        self.current_max = current_max
        self.equivalence_code = equivalence_code
        self.voltage_input_min = voltage_input_min
        self.voltage_input_max = voltage_input_max
        self.voltage_bias_min = voltage_bias_min
        self.voltage_bias_max = voltage_bias_max
        self.component = "SWITCH"
        self.dict_filters = {"Switch type": self.switch_type}

        # Dynamic parameters
        self.name = ""
        self.signal_control = 0
        self.voltage_input = 0
        self.power_input = 0
        self.current_input = 0
        self.voltage_output = 0
        self.current_output = 0
        self.power_output = 0
        self.power_dissipation = 0

        # UI Parameters
        self.voltage_in_label = QLabel()
        self.current_in_label = QLabel()
        self.power_in_label = QLabel()
        self.power_dissipation_label = QLabel()
        self.voltage_out_label = QLabel()
        self.current_out_label = QLabel()
        self.power_out_label = QLabel()
        self.proxy_widget = GraphicsProxyWidget()

        self.parent = 0
        self.children = []
        # Dict key = child widget & value = arrow
        self.arrows = {}

        self.move_grpbox = False

    def ui_init(self):
        self.proxy_widget.widget_clicked.connect(self.send_widget)
        grp_box = QGroupBox()
        grp_box.setObjectName("SWITCH_GrpBox")
        # Layouts
        v_layout = QVBoxLayout()
        h_layout_1 = QHBoxLayout()
        h_layout_2 = QHBoxLayout()
        grid_layout = QGridLayout()

        # Line 1
        component_label = QLabel(self.switch_type)
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

        # Line if switch has a Vbias
        if self.voltage_bias_min != "None":
            vbias_label = QLabel("Vbias: " + str(self.voltage_bias_min) + " V - " + str(self.voltage_bias_max) + " V")

        # Line 4 or 5
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
        grid_layout.addWidget(self.power_dissipation_label, 3, 1)

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
        if self.voltage_bias_min != "None":
            v_layout.addWidget(vbias_label)
        v_layout.addWidget(line_label)
        v_layout.addLayout(grid_layout)

        # Widget Settings
        grp_box.setTitle(str(self.name))
        grp_box.setLayout(v_layout)
        # grp_box.setFixedSize(150, 200)

        self.proxy_widget.setPos(INITIAL_POS_X, INITIAL_POS_Y)
        self.proxy_widget.setWidget(grp_box)

        return self.proxy_widget

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

        # Power dissipation parameter
        self.power_dissipation = (self.rds_on * (self.current_output ** 2)) / 1000

        # Editing input parameters
        self.current_input = self.current_output
        self.power_input = self.current_input * float(self.voltage_input)

        # Update graphics parameters
        self.update_graphics_parameters()

    def update_graphics_parameters(self):
        # Input parameters
        self.voltage_in_label.setText(self.voltage_input + " V")
        self.current_in_label.setText(str(round(self.current_input, 1)) + " mA")
        self.power_in_label.setText(str(round(self.power_input, 1)) + " mW")

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
