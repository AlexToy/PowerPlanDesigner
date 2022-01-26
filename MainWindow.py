from PyQt5.QtWidgets import QMainWindow, QAction, QToolBar
from PagePowerPlan import PagePowerPlan
from AddElement import AddElement



class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        # Add new page
        self.new_power_plan = PagePowerPlan()

        # Add toolbar and action
        self.create_actions()
        self.create_toolbar()

        self.setCentralWidget(self.new_power_plan)
        self.setWindowTitle("Power Plan Designer")
        self.resize(400, 200)

        # Create AddElement() page
        self.add_element = AddElement()
        self.add_element.dcdc_selected.connect(self.new_power_plan.add_new_element)

        # Close add_element window
        self.add_element.close()

    def open_add_element(self):
        self.add_element.show()

    def create_actions(self):
        self.action_add_element = QAction("DCDC", self)
        self.action_add_element.triggered.connect(self.open_add_element)

    def create_toolbar(self):
        edit_toolbar = QToolBar("Edit", self)
        self.addToolBar(edit_toolbar)
        edit_toolbar.addAction(self.action_add_element)

