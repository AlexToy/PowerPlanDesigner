from PyQt5.QtWidgets import QGroupBox, QGridLayout, QLabel, QWidget
from PyQt5 import QtCore
from Components.GraphicsProxyWidget import GraphicsProxyWidget

INITIAL_POS_X = 50
INITIAL_POS_Y = 50


class ConsumerWidget(QWidget):
    # Signal
    widget_selected = QtCore.pyqtSignal(object)

    def __init__(self, name, type, supplier, ref_component, equivalence_code, info, voltage_input,
                 current_theoretical, current_min_measure, current_max_measure, current_peak, parent=None):
        super(ConsumerWidget, self).__init__(parent)

        #  Fixed parameters
        self.name = name
        self.type = type
        self.supplier = supplier
        self.ref_component = ref_component
        self.equivalence_code = equivalence_code
        self.info = info
        self.current_theoretical = current_theoretical
        self.current_min_measure = current_min_measure
        self.current_max_measure = current_max_measure
        self.current_peak = current_peak
        self.component = "Consumer"

        self.current_input = current_theoretical
        self.voltage_input = voltage_input
        self.power_input = self.voltage_input * self.current_input

        self.parent = 0
        self.arrows = {}

        # UI parameters
        self.proxy_widget = GraphicsProxyWidget()

    def ui_init(self):
        grp_box = QGroupBox()
        grp_box.setObjectName("CONSUMER_GrpBox")
        self.proxy_widget.widget_clicked.connect(self.send_widget)

        # creation of widget & layout
        layout = QGridLayout()
        layout.setSpacing(5)
        ref_component_label = QLabel(self.ref_component)
        equivalence_code_label = QLabel(self.equivalence_code)
        line_label = QLabel("------------")
        input_label = QLabel("Input")
        input_label.setObjectName("Bold_Word")
        voltage_input_label = QLabel(str(self.voltage_input) + " V")
        voltage_input_label.setObjectName("Voltage")
        current_input_label = QLabel(str(self.current_input) + " mA")
        current_input_label.setObjectName("Current")
        power_input_label = QLabel(str(self.power_input) + " mW")
        power_input_label.setObjectName("Power")

        # Layout
        layout.addWidget(ref_component_label, 0, 0)
        layout.addWidget(equivalence_code_label, 1, 0)
        layout.addWidget(line_label, 2, 0)
        layout.addWidget(input_label, 3, 0)
        layout.addWidget(voltage_input_label, 4, 0)
        layout.addWidget(current_input_label, 5, 0)
        layout.addWidget(power_input_label, 6, 0)

        # Widget settings
        grp_box.setTitle(str(self.name) + " - " + str(self.info))
        grp_box.setLayout(layout)
        grp_box.setMinimumWidth(150)

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

    def get_parent(self):
        return self.parent

    def remove_parent(self):
        if self.parent != 0:
            print("DEBUG : remove " + self.parent.name + "as parent to " + self.name)
        self.parent = 0

    def add_child(self) -> bool:
        print("DEBUG : ConsumerWidget cannot have children !")

    def remove_child(self):
        print("DEBUG : ConsumerWidget cannot have children !")

    def remove_all_children(self):
        print("DEBUG : ConsumerWidget cannot have children !")

    def get_children(self):
        return 0

    def send_widget(self):
        self.widget_selected.emit(self)
