from PyQt5.QtWidgets import QTabWidget, QScrollArea, QVBoxLayout, QWidget, QComboBox, QPushButton, QHBoxLayout, \
    QRadioButton, QButtonGroup, QDialog, QStackedWidget
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

        # Init layout
        init_widget = QWidget()
        init_layout = QVBoxLayout()
        init_widget.setLayout(init_layout)

        # Add init layout in the tab component
        self.tab_component_widget = QStackedWidget()
        self.tab_component_widget.addWidget(init_widget)

        self.list_selected_widget = []
        self.view_filter = 0
        self.button_grp = 0
        self.list_filters = 0
        self.dict_idx_filter_name = {}

        button_filter = QPushButton()
        button_filter.clicked.connect(self.view_filters)
        self.select_filter = QComboBox()
        layout_filter = QHBoxLayout()
        layout_filter.addWidget(self.select_filter)
        layout_filter.addWidget(button_filter)
        init_layout.addLayout(layout_filter)

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
            self.list_selected_widget.append(self.select_component_widget)
            init_layout.addWidget(self.select_component_widget)

        self.setWidget(init_widget)

    def send_component(self, element):
        self.component_selected.emit(element)

    def view_filters(self):
        # This function create a QDialog where the user must choose a filter from a list.

        # Create widgets and layout
        layout = QVBoxLayout()
        self.button_grp = QButtonGroup()
        add_button = QPushButton("Add")
        add_button.clicked.connect(self.add_filter)

        # Get the list of filter (Request this information from the last added widget)
        self.list_filters = self.select_component_widget.get_widget_filters()

        for idx, filter in enumerate(self.list_filters):
            # For every filter, create a radio button
            button = QRadioButton()
            button.setText(filter)
            self.dict_idx_filter_name.update({idx: filter})
            self.button_grp.addButton(button, idx)
            layout.addWidget(button)

        layout.addWidget(add_button)
        msg_box = QDialog()
        msg_box.setLayout(layout)
        msg_box.exec_()

    def add_filter(self):

        list_value = []
        dict_filter_idx_layout = {}
        idx = 0

        # Get the filter was selected
        filter_selected = self.dict_idx_filter_name[self.button_grp.checkedId()]
        print("Filtre Selected : " + str(filter_selected))

        # For every widget on the Tab Component
        for selected_widget in self.list_selected_widget:
            print("selected_widget : " + str(selected_widget))
            # get the value of the filter
            value = selected_widget.get_widget_filters()[filter_selected]
            # if it doesn't exist, add the value to the combobox
            if value not in list_value:
                print("value : " + str(value))
                idx = idx + 1
                list_value.append(value)
                self.select_filter.addItem(str(value))
                # Create a dict with filter and index of stackedWidget
                dict_filter_idx_layout.update({value: idx})

        # For every value, create a new layout with the corresponding widget of the value
        for value in list_value:
            new_widget = QWidget()
            new_layout = QVBoxLayout()
            new_widget.setLayout(new_layout)
            self.tab_component_widget.addWidget(new_widget)

            for widget in self.list_selected_widget:
                # If the filter of the widget contens the value, add on the page
                if widget.get_widget().component == "DCDC":


        # print the good stackedLayout
        self.tab_component_widget.setCurrentIndex(dict_filter_idx_layout[value])