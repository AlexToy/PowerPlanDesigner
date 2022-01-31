from PyQt5.QtWidgets import QMainWindow, QAction, QToolBar
from PyQt5 import QtCore
from PagePowerPlan import PagePowerPlan
from AddElement import AddElement


class MainWindow(QMainWindow):

    # Signal
    add_new_parent_child_connection = QtCore.pyqtSignal(bool)
    element_is_deleted = QtCore.pyqtSignal(bool)

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        # Add new page
        self.new_power_plan = PagePowerPlan()
        self.new_power_plan.element_received.connect(self.close_add_element)
        self.add_new_parent_child_connection.connect(self.new_power_plan.set_add_child_parent_connection)
        self.element_is_deleted.connect(self.new_power_plan.set_delete_element)

        # Add toolbar and action
        self.create_actions()
        self.create_toolbar()

        self.setCentralWidget(self.new_power_plan)
        self.setWindowTitle("Power Plan Designer")
        self.resize(400, 200)

        # Create AddElement() page
        self.add_element = AddElement()
        self.add_element.dcdc_selected.connect(self.new_power_plan.add_new_element)

    def open_add_element(self):
        self.add_element.show()

    def close_add_element(self, element_received: bool):
        if element_received:
            self.add_element.close()

    def new_parent_child_connexion(self):
        self.add_new_parent_child_connection.emit(True)

    def delete_element(self):
        self.element_is_deleted.emit(True)

    def create_actions(self):
        self.action_add_element = QAction("Add Component", self)
        self.action_add_element.triggered.connect(self.open_add_element)
        self.action_parent_child_connexion = QAction("Add supply", self)
        self.action_parent_child_connexion.triggered.connect(self.new_parent_child_connexion)
        self.action_delete_element = QAction("Delete Component", self)
        self.action_delete_element.triggered.connect(self.delete_element)

    def create_toolbar(self):
        edit_toolbar = QToolBar("Edit", self)
        self.addToolBar(edit_toolbar)
        edit_toolbar.addAction(self.action_add_element)
        edit_toolbar.addAction(self.action_parent_child_connexion)
        edit_toolbar.addAction(self.action_delete_element)

