from PyQt5.QtWidgets import QWidget, QGridLayout


class PagePowerPlan(QWidget):
    def __init__(self, parent=None):
        super(PagePowerPlan, self).__init__(parent)

        self.layout = QGridLayout()

        self.setLayout(self.layout)