from PyQt5.QtWidgets import QTabWidget, QScrollArea, QVBoxLayout, QWidget, QComboBox, QPushButton, QHBoxLayout, \
    QRadioButton, QButtonGroup, QDialog, QStackedWidget
from PyQt5 import QtCore, QtGui
from loading_database import loading_database
from Component_Search.SelectDcdcWidget import SelectDcdcWidget
from Component_Search.SelectPsuWidget import SelectPsuWidget
from Component_Search.SelectLdoWidget import SelectLdoWidget
from Component_Search.SelectSwitchWidget import SelectSwitchWidget
from Component_Search.AddComponentConsumer import AddComponentConsumer
import img


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
        self.setMinimumWidth(470)
        self.setMaximumWidth(470)

    def send_element_selected(self, element):
        self.dcdc_selected.emit(element)


class TabComponent(QScrollArea):
    # Signal
    component_selected = QtCore.pyqtSignal(object)

    def __init__(self, list_component_database, parent=None):
        super(TabComponent, self).__init__(parent)

        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)
        self.msg_box = QDialog()
        self.view_created = False
        self.dict_value_layout = {}

        # Init layout
        init_widget = QWidget()
        init_layout = QVBoxLayout()
        init_widget.setLayout(init_layout)

        # Add init layout in the tab component
        self.tab_component_widget = QStackedWidget()
        self.tab_component_widget.addWidget(init_widget)

        self.list_selected_widget = []
        self.button_grp = 0
        self.dict_filters = 0
        self.dict_idx_filter_name = {}

        button_filter = QPushButton()
        button_filter.setFixedSize(100, 30)
        button_filter.clicked.connect(self.view_filters)
        img_filter = QtGui.QPixmap("img/filter.png")
        icon_filter = QtGui.QIcon(img_filter)
        button_filter.setIcon(icon_filter)
        button_filter.setIconSize(img_filter.rect().size())

        self.select_filter = QComboBox()
        self.select_filter.currentIndexChanged.connect(self.value_filter_change)
        layout_filter = QHBoxLayout()
        layout_filter.addWidget(self.select_filter)
        layout_filter.addWidget(button_filter)
        layout.addLayout(layout_filter)
        layout.addWidget(self.tab_component_widget)

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

        self.setWidget(widget)

    def send_component(self, element):
        self.component_selected.emit(element)

    def view_filters(self):
        # This function create a QDialog where the user must choose a filter from a list.
        if not self.view_created:
            # Create widgets and layout
            layout = QVBoxLayout()
            self.button_grp = QButtonGroup()
            add_button = QPushButton("Add")
            add_button.clicked.connect(self.add_filter)

            # Get the list of filter (Request this information from the last added widget)
            self.dict_filters = self.select_component_widget.get_widget_filters()

            for idx, filter in enumerate(self.dict_filters):
                # For every filter, create a radio button
                button = QRadioButton()
                button.setText(filter)
                self.dict_idx_filter_name.update({idx: filter})
                self.button_grp.addButton(button, idx)
                layout.addWidget(button)

            layout.addWidget(add_button)
            self.msg_box.setLayout(layout)
            self.view_created = True
        self.msg_box.exec_()

    def add_filter(self):
        self.select_filter.clear()
        self.msg_box.close()
        list_different_value = []

        # Get the filter was selected
        filter_name_selected = self.dict_idx_filter_name[self.button_grp.checkedId()]

        # 1 : Find in list of component the different value for the selected filter
        # For every widget on the Tab Component (Ldo or DCDC or Switch ...)
        for selected_widget in self.list_selected_widget:

            # get the value of the filter
            filter_value_selected = selected_widget.get_widget_filters()[filter_name_selected]

            # if it doesn't exist
            if filter_value_selected not in list_different_value:
                # add the value
                list_different_value.append(filter_value_selected)
                self.select_filter.addItem(str(filter_value_selected))

        # 2 : For every different value, create a widget (QStackedWidget) and add every selected widget witch
        # correspond
        for value in list_different_value:

            # Create the page for the new value of the filter
            # If the page doesn't already exist, create it
            if value not in self.dict_value_layout:

                new_widget = QWidget()
                new_layout = QVBoxLayout()
                new_widget.setLayout(new_layout)

                for selected_widget in self.list_selected_widget:

                    if selected_widget.value_is_present(filter_name_selected, value):
                        new_layout.addWidget(selected_widget)

                self.tab_component_widget.addWidget(new_widget)

                # Add the value and his index in a dict
                self.dict_value_layout.update({str(value): new_widget})

        # print the good stackedLayout
        self.tab_component_widget.setCurrentWidget(self.dict_value_layout[str(value)])

        current_filter = str(self.select_filter.currentText())
        for value in self.dict_value_layout:
            if value == current_filter:
                current_widget = self.dict_value_layout[value]
                self.tab_component_widget.setCurrentWidget(current_widget)
        self.tab_component_widget.adjustSize()

    def value_filter_change(self, index):
        current_filter = str(self.select_filter.currentText())
        for value in self.dict_value_layout:
            if value == current_filter:
                current_widget = self.dict_value_layout[value]
                self.tab_component_widget.setCurrentWidget(current_widget)
        self.tab_component_widget.adjustSize()


