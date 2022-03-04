from PyQt5.QtWidgets import QTabWidget, QScrollArea, QVBoxLayout, QWidget
from PyQt5 import QtCore
from loading_database import loading_database
from Component_Search.SelectDcdcWidget import SelectDcdcWidget
from Component_Search.SelectPsuWidget import SelectPsuWidget
from Component_Search.SelectLdoWidget import SelectLdoWidget
from Component_Search.SelectSwitchWidget import SelectSwitchWidget
from Component_Search.AddComponentConsumer import AddComponentConsumer


class AddElement(QTabWidget):
    # This class loads the database, asks the user which element they want to add to their page (graphical widget) and
    # sends the page a copy of the chosen element

    # Signal
    dcdc_selected = QtCore.pyqtSignal(object)

    def __init__(self, parent=None):
        super(AddElement, self).__init__(parent)

        # 1 Import the database
        list_dcdc_database, list_psu_database, list_ldo_database, list_consumer_database, list_switch_database = loading_database()

        tab_dcdc = TabComponent(list_dcdc_database)
        tab_dcdc.component_selected.connect(self.send_element_selected)
        tab_psu = TabComponent(list_psu_database)
        tab_psu.component_selected.connect(self.send_element_selected)
        tab_switch = TabComponent(list_switch_database)
        tab_switch.component_selected.connect(self.send_element_selected)
        tab_ldo = TabComponent(list_ldo_database)
        tab_ldo.component_selected.connect(self.send_element_selected)

        # CONSUMER
        tab_consumer = AddComponentConsumer(list_consumer_database)
        tab_consumer.add_consumer.connect(self.send_element_selected)

        self.addTab(tab_dcdc, "DC/DC")
        self.addTab(tab_psu, "PSU")
        self.addTab(tab_ldo, "LDO")
        self.addTab(tab_switch, "SWITCH")
        self.addTab(tab_consumer, "CONSUMER")

        self.setWindowTitle("Add new element")

    def send_element_selected(self, element):
        self.dcdc_selected.emit(element)


class TabComponent(QScrollArea):
    # Signal
    component_selected = QtCore.pyqtSignal(object)

    def __init__(self, list_component_database, parent=None):
        super(TabComponent, self).__init__(parent)

        widget = QWidget()
        layout = QVBoxLayout()
        list_widget = []

        for component in list_component_database:
            if component.component == "DCDC":
                self.select_component_widget = SelectDcdcWidget(component)
            elif component.component == "LDO":
                self.select_component_widget = SelectLdoWidget(component)
            elif component.component == "SWITCH":
                self.select_component_widget = SelectSwitchWidget(component)
            elif component.component == "PSU":
                self.select_component_widget = SelectPsuWidget(component)

            self.select_component_widget.clicked_add_component.connect(self.send_component)
            layout.addWidget(self.select_component_widget)
        widget.setLayout(layout)
        self.setWidget(widget)

    def send_component(self, element):
        self.component_selected.emit(element)
