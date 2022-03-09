from PyQt5.QtWidgets import QGroupBox, QHBoxLayout, QGridLayout, QPushButton, QLineEdit, QLabel, QVBoxLayout, \
    QScrollArea, QWidget, QStackedWidget, QComboBox, QButtonGroup, QRadioButton, QDialog
from PyQt5.QtGui import QDoubleValidator
from PyQt5 import QtCore
from Components.LdoWidget import LdoWidget


class TabLdo(QScrollArea):
    # Signal
    component_selected = QtCore.pyqtSignal(object)

    def __init__(self, list_ldo_database, parent=None):
        super(TabLdo, self).__init__(parent)

        # Init layout
        init_widget = QWidget()
        init_layout = QVBoxLayout()
        init_widget.setLayout(init_layout)

        # Add init layout in the tab component
        self.tab_ldo_widget = QStackedWidget()
        self.tab_ldo_widget.addWidget(init_widget)

        # Button and Combobox filter
        button_select_filter = QPushButton()
        button_select_filter.clicked.connect(self.view_add_filters)
        self.select_filter_combobox = QComboBox()
        layout_widget_filter = QHBoxLayout()
        layout_widget_filter.addWidget(self.select_filter_combobox)
        layout_widget_filter.addWidget(button_select_filter)
        init_layout.addLayout(layout_widget_filter)
        self.list_filters = 0

        for ldo in list_ldo_database:
            self.select_ldo_widget = SelectLdoWidget(ldo)
            self.select_ldo_widget.clicked_add_component.connect(self.send_component)
            self.list_selected_ldo.append(self.select_ldo_widget)
            init_layout.addWidget(self.select_ldo_widget)

        self.tab_ldo_widget.setCurrentIndex(0)
        self.setWidget(self.tab_ldo_widget)

    def send_component(self, element):
        self.component_selected.emit(element)

    def view_add_filters(self):
        # This function create a QDialog where the user must choose a filter from a list.
        # Create widgets and layout
        layout = QVBoxLayout()
        button_grp = QButtonGroup()
        add_button = QPushButton("Add")
        add_button.clicked.connect(self.add_filter)

        # Get the list of filter (Request this information from the last added widget)
        self.list_filters = self.select_component_widget.get_widget_filters()

        for idx, filter in enumerate(self.list_filters):
            # For every filter, create a radio button
            button = QRadioButton()
            button.setText(filter)
            self.dict_idx_filter_name.update({idx: filter})
            button_grp.addButton(button, idx)
            layout.addWidget(button)

        layout.addWidget(add_button)
        msg_box = QDialog()
        msg_box.setLayout(layout)
        msg_box.exec_()

    def add_filter(self):

        list_value_filter = []
        dict_filter_idx_layout = {}
        idx = 0

        # Get the filter was selected with the current idx of button grp
        name_filter_selected = self.dict_idx_filter_name[self.button_grp.checkedId()]

        # For every widget on the Tab Component
        for selected_ldo in self.list_selected_ldo:
            # get the value of the filter
            value_filter = selected_ldo.get_widget_filters()[name_filter_selected]
            # if it doesn't exist, add the value to the combobox
            if value_filter not in list_value_filter:
                idx = idx + 1
                list_value_filter.append(value_filter)
                self.select_filter_combobox.addItem(str(value_filter))

                # TODO : Create a stacked widget

                # Create a dict with filter and index of stackedWidget
                dict_filter_idx_layout.update({value_filter: idx})


class FilteredLayoutWidget(QWidget):
    def __init__(self, list_selected_ldo, , parent=None):
        super(FilteredLayoutWidget, self).__init__(parent)

        layout = QVBoxLayout()



class SelectLdoWidget(QGroupBox):
    # Signal
    clicked_add_component = QtCore.pyqtSignal(object)

    def __init__(self, ldo: LdoWidget, parent=None):
        super(SelectLdoWidget, self).__init__(parent)

        # Get dcdc from database
        self.ldo_copy = ldo
        self.setObjectName("LDO_addElement_GrpBox")

        # creation of widget & layout
        self.layout = QHBoxLayout()
        self.layout_1 = QVBoxLayout()
        self.layout_2 = QGridLayout()
        self.add_ldo_button = QPushButton("Add")
        self.name_label = QLabel("Name : ")
        self.name = QLineEdit()
        self.v_in_label = QLabel("Vin : ")
        self.v_in = QLineEdit()
        self.equiv_code_label = QLabel(str(self.ldo_copy.equivalence_code))
        self.ref_label = QLabel(self.ldo_copy.ref_component)
        self.supplier_label = QLabel(self.ldo_copy.supplier)
        self.label_restriction = QDoubleValidator(0, 100, 2)

        # layout
        self.layout_2.addWidget(self.name_label, 0, 0)
        self.layout_2.addWidget(self.name, 0, 1)
        self.layout_2.addWidget(self.v_in_label, 1, 0)
        self.layout_2.addWidget(self.v_in, 1, 1)
        self.layout_2.addWidget(self.add_ldo_button, 2, 0, 1, 2)

        self.layout_1.addWidget(self.supplier_label)
        self.layout_1.addWidget(self.ref_label)
        self.layout_1.addWidget(self.equiv_code_label)

        self.layout.addLayout(self.layout_1)
        self.layout.addLayout(self.layout_2)

        # Widget settings
        self.add_ldo_button.clicked.connect(self.clicked_button_function)
        # self.add_dcdc_button.setFixedSize(150, 25)
        self.name.setFixedSize(150, 25)
        self.v_in.setFixedSize(150, 25)
        # self.v_in.setValidator(self.label_restriction)
        self.setTitle("LDO   " + str(self.ldo_copy.voltage_output) + " V   " +
                      str(self.ldo_copy.current_max * 1000) + " mA")
        self.setLayout(self.layout)

    def clicked_button_function(self):
        if self.name.displayText() != "" and self.v_in.displayText() != "":

            if float(self.ldo_copy.voltage_input_min) <= float(self.v_in.displayText()) <= float(
                    self.ldo_copy.voltage_input_max):

                # Add user parameters to the DC/DC
                self.ldo_copy.voltage_input = self.v_in.displayText()
                self.ldo_copy.name = self.name.displayText()

                # Send dcdc_selected signal
                self.clicked_add_component.emit(self.ldo_copy)

                # Clear parameters
                self.name.setText("")
                self.v_in.setText("")

            else:
                print("DEBUG : Input voltage is not in the DC/DC Scope !")
        else:
            print("DEBUG : Some fields are empty !")

    def get_widget_filters(self):
        return self.ldo_copy.list_filter
