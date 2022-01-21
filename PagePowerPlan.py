from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton
from AddElement import AddElement


class PagePowerPlan(QWidget):
    def __init__(self, parent=None):
        super(PagePowerPlan, self).__init__(parent)

        self.layout = QGridLayout()

        self.add_new_element_button = QPushButton("+")
        self.add_new_element_button.clicked.connect(self.open_add_element)
        self.layout.addWidget(self.add_new_element_button, 0, 0)

        self.add_element = AddElement()

        self.setLayout(self.layout)

    def open_add_element(self):
        self.add_element.show()

