from PyQt5.QtWidgets import QGroupBox, QGridLayout, QLabel, QGraphicsProxyWidget, QWidget
from PyQt5.QtCore import QPointF, Qt
from PyQt5 import QtCore


INITIAL_POS_X = 50
INITIAL_POS_Y = 50


class ConsumerWidget(QWidget):

    # Signal
    widget_selected = QtCore.pyqtSignal(object)

    def __init__(self, name: str, ref_component: str, info: str, equivalence_code: str,
                 voltage_input: float, current_input: float, parent=None):
        super(ConsumerWidget, self).__init__(parent)

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

        # UI parameters
        self.proxy_widget = GraphicsProxyWidget()

    def ui_init(self):
        grp_box = QGroupBox()
        self.proxy_widget.widget_clicked.connect(self.send_widget)

        # creation of widget & layout
        layout = QGridLayout()
        ref_component_label = QLabel(self.ref_component)
        info_label = QLabel(self.info)
        equivalence_code_label = QLabel(self.equivalence_code)
        line_label = QLabel("------------")
        input_label = QLabel("Input")
        voltage_input_label = QLabel(str(self.voltage_input) + " V")
        current_input_label = QLabel(str(self.current_input) + " mA")
        power_input_label = QLabel(str(self.power_input) + " mW")

        # Layout
        layout.addWidget(ref_component_label, 0, 0)
        layout.addWidget(info_label, 1, 0)
        layout.addWidget(equivalence_code_label, 2, 0)
        layout.addWidget(line_label, 3, 0)
        layout.addWidget(input_label, 4, 0)
        layout.addWidget(voltage_input_label, 5, 0)
        layout.addWidget(current_input_label, 6, 0)
        layout.addWidget(power_input_label, 7, 0)

        # Widget settings
        grp_box.setTitle(str(self.name))
        grp_box.setLayout(layout)
        # self.grp_box.setFixedSize(150, 200)

        self.proxy_widget.setPos(INITIAL_POS_X, INITIAL_POS_Y)
        self.proxy_widget.setWidget(grp_box)

        return self.proxy_widget

    def add_parent(self, parent):
        if float(self.voltage_input) == float(parent.voltage_output):
            self.parent = parent
            print("DEBUG : add " + parent.name + "as parent to " + self.name)
        else:
            print("DEBUG : " + str(self.voltage_input) + "'s output voltage is different from " + str(
                parent.voltage_output) + "'s")

    def get_parent(self):
        return self.parent

    def remove_parent(self):
        if self.parent != 0:
            print("DEBUG : remove " + self.parent.name + "as parent to " + self.name)
        self.parent = 0

    def add_child(self, child) -> bool:
        print("DEBUG : PsuWidget cannot have children !")

    def remove_child(self, remove_child):
        print("DEBUG : PsuWidget cannot have children !")

    def remove_all_children(self):
        print("DEBUG : PsuWidget cannot have children !")

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