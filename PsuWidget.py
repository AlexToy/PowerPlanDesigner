from PyQt5.QtWidgets import QGroupBox, QGridLayout, QLabel, QGraphicsProxyWidget, QWidget
from PyQt5.QtCore import QPointF, Qt
from PyQt5 import QtCore


INITIAL_POS_X = 50
INITIAL_POS_Y = 50


class PsuWidget(QWidget):

    # Signal
    widget_selected = QtCore.pyqtSignal(object)

    def __init__(self, ref_component: str, supplier: str, equivalence_code: str, current_max: float,
                 voltage_input: float, voltage_output: float, jack: str, parent=None):
        super(PsuWidget, self).__init__(parent)

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

        # UI Parameters
        self.voltage_output_label = QLabel()
        self.current_output_label = QLabel()
        self.power_output_label = QLabel()
        self.proxy_widget = GraphicsProxyWidget()

    def ui_init(self):
        grp_box = QGroupBox()
        self.proxy_widget.widget_clicked.connect(self.send_widget)

        layout = QGridLayout()

        # Line 1
        psu_label = QLabel("PSU ")
        voltage_input_label = QLabel(str(self.voltage_input) + " V")
        current_max_label = QLabel(str(self.current_max) + " A")
        layout.addWidget(psu_label, 0, 0)
        layout.addWidget(voltage_input_label, 0, 1)
        layout.addWidget(current_max_label, 0, 2)

        # Line 2
        supplier_label = QLabel(self.supplier)
        ref_component_label = QLabel(self.ref_component)
        layout.addWidget(supplier_label, 1, 0)
        layout.addWidget(ref_component_label, 1, 1)

        # Line 3
        equivalence_code_label = QLabel(self.equivalence_code)
        layout.addWidget(equivalence_code_label, 2, 0)

        # Line 4
        jack_label = QLabel("Jack : ")
        jack_info_label = QLabel(self.jack)
        layout.addWidget(jack_label, 3, 0)
        layout.addWidget(jack_info_label, 3, 1)

        # Line 5
        line_label = QLabel("----------------------------------")
        layout.addWidget(line_label, 4, 0)

        # Line 6
        output_label = QLabel("Output")
        layout.addWidget(output_label, 5, 0)

        # Line 7
        self.voltage_output_label.setText(str(self.voltage_output) + " V")
        layout.addWidget(self.voltage_output_label, 6, 0)

        # Line 8
        self.current_output_label.setText(str(self.current_output) + " mA")
        layout.addWidget(self.current_output_label, 7, 0)

        # Line 9
        self.power_output_label.setText(str(self.power_output) + " mW")
        layout.addWidget(self.power_output_label, 8, 0)

        # Widget Settings
        grp_box.setTitle(str(self.name))
        grp_box.setLayout(layout)
        # self.grp_box.setFixedSize(150, 200)

        self.proxy_widget.setPos(INITIAL_POS_X, INITIAL_POS_Y)
        self.proxy_widget.setWidget(grp_box)

        return self.proxy_widget

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
                if self.children[index].name == remove_child.name:
                    # Remove child to the dcdc children list
                    print("DEBUG : remove " + self.children[index].name + " as child to " + self.name)
                    del self.children[index]
                    # Update parameters
                    self.update_parameters()
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

    def add_parent(self, element):
        print("DEBUG : PsuWidget cannot have parents !")

    def remove_parent(self, element):
        print("DEBUG : PsuWidget cannot have parents !")

    def get_parent(self):
        print("DEBUG : PsuWidget cannot have parents !")
        return 0

    def update_parameters(self):
        # Editing output parameters
        self.power_output = 0
        if len(self.children) != 0:
            for child in self.children:
                self.power_output = float(self.power_output) + float(child.power_input)
        self.current_output = float(self.power_output) / float(self.voltage_output)

        # Update graphics parameters
        self.update_graphics_parameters()

    def update_graphics_parameters(self):
        # Output parameters
        self.voltage_output_label.setText(str(self.voltage_output) + " V")
        self.current_output_label.setText(str(self.current_output) + " mA")
        self.power_output_label.setText(str(self.power_output) + " mW")

    def send_widget(self):
        self.widget_selected.emit(self)


class GraphicsProxyWidget(QGraphicsProxyWidget):

    # Signal
    widget_clicked = QtCore.pyqtSignal()

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

            updated_cursor_x = updated_cursor_position.x() - orig_cursor_position.x() + orig_position.x()
            updated_cursor_y = updated_cursor_position.y() - orig_cursor_position.y() + orig_position.y()
            self.setPos(QPointF(updated_cursor_x, updated_cursor_y))

    def mouseReleaseEvent(self, event):
        pass
