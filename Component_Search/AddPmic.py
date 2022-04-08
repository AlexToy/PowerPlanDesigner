from PyQt5.QtWidgets import QScrollArea, QGroupBox, QPushButton, QVBoxLayout, QWidget
from PyQt5 import QtCore


class AddPmic(QScrollArea):
    # Signal
    component_selected = QtCore.pyqtSignal(object)

    def __init__(self, list_pmic_database, parent=None):
        super(AddPmic, self).__init__(parent)

        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)

        for pmic in list_pmic_database:
            new_selected_pmic = SelectedPmic(pmic)
            layout.addWidget(new_selected_pmic)
            new_selected_pmic.clicked_add_component.connect(self.send_component)

        self.setWidget(widget)

    def send_component(self, element):
        self.component_selected.emit(element)


class SelectedPmic(QGroupBox):
    # Signal
    clicked_add_component = QtCore.pyqtSignal(object)

    def __init__(self, pmic, parent=None):
        super(SelectedPmic, self).__init__(parent)

        self.pmic = pmic
        self.setObjectName("addElement_GrpBox")
        layout = QVBoxLayout()
        add_button = QPushButton("Add all")
        add_button.clicked.connect(self.clicked_button_function)
        layout.addWidget(add_button)

        self.setLayout(layout)
        self.setTitle(pmic.ref_component)

    def clicked_button_function(self):
        for dcdc in self.pmic.list_dcdc:
            self.clicked_add_component.emit(dcdc)
        for ldo in self.pmic.list_ldo:
            self.clicked_add_component.emit(ldo)