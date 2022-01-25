from PyQt5.QtWidgets import QGroupBox, QGridLayout, QLabel
from Consumer import Consumer


class ConsumerWidget(QGroupBox):
    def __init__(self, consumer: Consumer, parent=None):
        super(ConsumerWidget, self).__init__(parent)

        self.consumer = consumer

        # creation of widget & layout
        self.layout = QGridLayout()
        self.ref_component_label = QLabel(self.consumer.ref_component)
        self.info_label = QLabel(self.consumer.info)
        self.equivalence_code_label = QLabel(self.consumer.equivalence_code)
        self.line_label = QLabel("----------------------------------")
        self.input_label = QLabel("Input")
        self.voltage_input_label = QLabel(str(self.consumer.voltage_input) + " V")
        self.current_input_label = QLabel(str(self.consumer.current_input) + " A")
        self.power_input_label = QLabel(str(self.consumer.power_input) + " W")

        # Layout
        self.layout.addWidget(self.ref_component_label, 0, 0)
        self.layout.addWidget(self.info_label, 1, 0)
        self.layout.addWidget(self.equivalence_code_label, 2, 0)
        self.layout.addWidget(self.line_label, 3, 0)
        self.layout.addWidget(self.input_label, 4, 0)
        self.layout.addWidget(self.voltage_input_label, 5, 0)
        self.layout.addWidget(self.current_input_label, 6, 0)
        self.layout.addWidget(self.power_input_label, 7, 0)

        # Widget settings
        self.setTitle(str(self.consumer.name))
        self.setLayout(self.layout)
        self.setFixedSize(150, 200)