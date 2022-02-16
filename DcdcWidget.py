from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QGraphicsProxyWidget, \
    QWidget
from PyQt5.QtCore import QPointF, Qt
from PyQt5 import QtCore


INITIAL_POS_X = 50
INITIAL_POS_Y = 50


class DcdcWidget(QWidget):

    # Signal
    widget_selected = QtCore.pyqtSignal(object)

    def __init__(self, ref_component: str, supplier: str, current_max: float, equivalence_code: str,
                 voltage_input_min: float, voltage_input_max: float, voltage_output_min: float,
                 voltage_output_max: float, formula_list, parent=None):
        super(DcdcWidget, self).__init__(parent)

        #  Fixed parameters
        self.ref_component = ref_component
        self.supplier = supplier
        self.current_max = current_max
        self.equivalence_code = equivalence_code
        self.voltage_input_min = voltage_input_min
        self.voltage_input_max = voltage_input_max
        self.voltage_output_min = voltage_output_min
        self.voltage_output_max = voltage_output_max
        self.formula_list = formula_list
        self.component = "DCDC"

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
        self.proxy_widget = GraphicsProxyWidget()

        self.parent = 0
        self.children = []
        # Dict key = child widget & value = arrow
        self.arrows = {}

        self.move_grpbox = False

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
        input_label.setStyleSheet("font: bold")
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
        self.power_dissipation_label.setText("- " + str(self.power_dissipation) + " W")
        self.efficiency_label.setText("- %")
        grid_layout.addWidget(self.power_dissipation_label, 2, 1)
        grid_layout.addWidget(self.efficiency_label, 3, 1)

        # Output
        output_label = QLabel("Output")
        output_label.setStyleSheet("font: bold")
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

    def refresh_efficiency_value(self):
        for formula in self.formula_list:
            # Look for the same voltage input & voltage output
            if formula.voltage_input == float(self.voltage_input) and \
                    formula.voltage_output == float(self.voltage_output):
                formula_str = formula.get_formula_efficiency(self.current_output)
                self.efficiency = eval(formula_str.replace("x", str(self.current_output/1000)))
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
        else:
            print("DEBUG : " + str(self.voltage_input) + "'s output voltage is different from " + str(
                parent.voltage_output) + "'s")

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

    def update_parameters(self):
        # Editing output parameters
        self.power_output = 0
        if len(self.children) != 0:
            for child in self.children:
                self.power_output = float(self.power_output) + float(child.power_input)
        self.current_output = float(self.power_output) / float(self.voltage_output)

        # Efficiency parameter
        self.refresh_efficiency_value()

        # Editing input parameters
        self.power_input = float(self.power_output) * (float(self.efficiency) / 100)
        self.current_input = float(self.power_input) / float(self.voltage_input)

        # Power dissipation parameter
        self.power_dissipation = self.power_output - self.power_input

        # Update graphics parameters
        self.update_graphics_parameters()

    def update_graphics_parameters(self):
        # Input parameters
        self.voltage_in_label.setText(self.voltage_input + " V")
        self.current_in_label.setText(str(round(self.current_input, 1)) + " mA")
        self.power_in_label.setText(str(round(self.power_input, 1)) + " mW")

        # Efficiency parameter
        self.efficiency_label.setText(str(round(self.efficiency, 1)) + " %")

        # Output parameters
        self.voltage_out_label.setText(self.voltage_output + " V")
        self.current_out_label.setText(str(round(self.current_output, 1)) + " mA")
        self.power_out_label.setText(str(round(self.power_output, )) + " mW")

        # Power dissipation parameter
        self.power_dissipation_label.setText(str(round(self.power_dissipation, 1)) + " W")

        # Update parent parameters
        if self.parent != 0:
            self.parent.update_parameters()

    def send_widget(self):
        self.widget_selected.emit(self)


class GraphicsProxyWidget(QGraphicsProxyWidget):

    # Signal
    widget_clicked = QtCore.pyqtSignal()
    new_widget_position = QtCore.pyqtSignal(float, float)

    def __init__(self, parent=None):
        super(GraphicsProxyWidget, self).__init__(parent)

        self.updated_cursor_x = 0
        self.updated_cursor_y = 0
        self.height = 0
        self.width = 0

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self.move_grpbox = True
        elif event.button() == Qt.LeftButton:
            self.move_grpbox = False
            # Send to the page power plan the widget
            self.widget_clicked.emit()

    def mouseMoveEvent(self, event):
        if self.move_grpbox:
            orig_cursor_position = event.lastScenePos()
            updated_cursor_position = event.scenePos()

            orig_position = self.scenePos()

            self.updated_cursor_x = updated_cursor_position.x() - orig_cursor_position.x() + orig_position.x()
            self.updated_cursor_y = updated_cursor_position.y() - orig_cursor_position.y() + orig_position.y()
            self.setPos(QPointF(self.updated_cursor_x, self.updated_cursor_y))

            # Send the new position to the arrow
            self.new_widget_position.emit(self.updated_cursor_x, self.updated_cursor_y)

    def mouseReleaseEvent(self, event):
        pass

    def resizeEvent(self, event):
        self.height = event.newSize().height()
        self.width = event.newSize().width()

