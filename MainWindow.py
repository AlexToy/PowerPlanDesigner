from PyQt5.QtWidgets import QMainWindow, QAction, QToolBar
from PagePowerPlan import PagePowerPlan


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.new_power_plan = PagePowerPlan()

        self.setCentralWidget(self.new_power_plan)
        self.setWindowTitle("Power Plan Designer")
        self.resize(400, 200)

    blaljblabla
