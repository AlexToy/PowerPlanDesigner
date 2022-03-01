from PyQt5.QtWidgets import QTabWidget, QScrollArea, QVBoxLayout, QGroupBox, QLabel, QHBoxLayout, QPushButton, QWidget
from PyQt5 import QtCore
from ConsumerWidget import ConsumerWidget


class AddComponentConsumer(QTabWidget):

    add_consumer = QtCore.pyqtSignal(object)

    def __init__(self, list_consumer, parent=None):
        super(AddComponentConsumer, self).__init__(parent)

        # SoC
        self.tab_soc = QScrollArea()
        self.widget_soc = QWidget(self.tab_soc)
        self.tab_soc_layout = QVBoxLayout()
        # eMMC
        self.tab_emmc = QScrollArea()
        self.widget_emmc = QWidget()
        self.tab_emmc_layout = QVBoxLayout()
        # DDR
        self.tab_ddr = QScrollArea()
        self.widget_ddr = QWidget()
        self.tab_ddr_layout = QVBoxLayout()
        # PHY
        self.tab_phy = QScrollArea()
        self.widget_phy = QWidget()
        self.tab_phy_layout = QVBoxLayout()
        # Wifi
        self.tab_wifi = QScrollArea()
        self.widget_wifi = QWidget()
        self.tab_wifi_layout = QVBoxLayout()
        # Front End
        self.tab_front_end = QScrollArea()
        self.widget_front_end = QWidget()
        self.tab_front_end_layout = QVBoxLayout()

        # List of equivalents codes
        self.list_code = []
        # List
        self.list_grp_by_equiv_code = []

        for consumer in list_consumer:

            # Creating a group box by equivalence code
            if consumer.equivalence_code not in self.list_code:
                # Adding the new code in the list
                self.list_code.append(consumer.equivalence_code)

                # Creating the group box for the equiv code and adding the group box to the good layout
                if consumer.name == "SoC":
                    self.group_supplier = GroupByEquivCode(consumer.supplier, consumer.ref_component,
                                                           consumer.equivalence_code)
                    self.tab_soc_layout.addWidget(self.group_supplier)
                elif consumer.name == "eMMC":
                    self.group_supplier = GroupByEquivCode(consumer.type, consumer.ref_component,
                                                           consumer.equivalence_code)
                    self.tab_emmc_layout.addWidget(self.group_supplier)
                elif consumer.name == "DDR":
                    self.group_supplier = GroupByEquivCode(consumer.type, consumer.ref_component,
                                                           consumer.equivalence_code)
                    self.tab_ddr_layout.addWidget(self.group_supplier)
                elif consumer.name == "PHY":
                    self.group_supplier = GroupByEquivCode(consumer.type, consumer.ref_component,
                                                           consumer.equivalence_code)
                    self.tab_phy_layout.addWidget(self.group_supplier)
                elif consumer.name == "WIFI":
                    self.group_supplier = GroupByEquivCode(consumer.type, consumer.ref_component,
                                                           consumer.equivalence_code)
                    self.tab_wifi_layout.addWidget(self.group_supplier)
                elif consumer.name == "Front End":
                    self.group_supplier = GroupByEquivCode(consumer.type, consumer.ref_component,
                                                           consumer.equivalence_code)
                    self.tab_front_end_layout.addWidget(self.group_supplier)

            # adding the group box to the list of group box
            self.list_grp_by_equiv_code.append(self.group_supplier)

            # Creating a group box by consumer
            self.grp_voltage = GroupVoltage(consumer)
            self.grp_voltage.clicked_add_consumer.connect(self.send_consumer_selected)

            # Adding consumer's group box in corresponding equivalence code group box
            self.list_grp_by_equiv_code[-1].add_voltage(self.grp_voltage)

        # Set widget and layout of each tab
        self.widget_soc.setLayout(self.tab_soc_layout)
        self.tab_soc.setWidget(self.widget_soc)
        self.widget_emmc.setLayout(self.tab_emmc_layout)
        self.tab_emmc.setWidget(self.widget_emmc)
        self.widget_ddr.setLayout(self.tab_ddr_layout)
        self.tab_ddr.setWidget(self.widget_ddr)
        self.widget_phy.setLayout(self.tab_phy_layout)
        self.tab_phy.setWidget(self.widget_phy)
        self.widget_wifi.setLayout(self.tab_wifi_layout)
        self.tab_wifi.setWidget(self.widget_wifi)
        self.widget_front_end.setLayout(self.tab_front_end_layout)
        self.tab_front_end.setWidget(self.widget_front_end)

        # Adding each tab in QTabWidget
        self.addTab(self.tab_soc, "SoC")
        self.addTab(self.tab_emmc, "eMMC")
        self.addTab(self.tab_ddr, "DDR")
        self.addTab(self.tab_phy, "PHY")
        self.addTab(self.tab_wifi, "Wifi")
        self.addTab(self.tab_front_end, "Front End")

    def send_consumer_selected(self, consumer):
        self.add_consumer.emit(consumer)


class GroupByEquivCode(QGroupBox):
    def __init__(self, title: str, core: str, equivalent_code, parent=None):
        super(GroupByEquivCode, self).__init__(parent)
        self.layout = QVBoxLayout()
        core_label = QLabel()
        core_label.setText(core)
        equiv_code_label = QLabel()
        equiv_code_label.setText(equivalent_code)
        self.layout.addWidget(core_label)
        self.layout.addWidget(equiv_code_label)
        self.setLayout(self.layout)
        self.setTitle(title)

    def add_voltage(self, group_voltage):
        self.layout.addWidget(group_voltage)


class GroupVoltage(QGroupBox):
    # Signal
    clicked_add_consumer = QtCore.pyqtSignal(object)

    def __init__(self, consumer: ConsumerWidget, parent=None):
        super(GroupVoltage, self).__init__(parent)

        self.consumer = consumer

        # creation of widget & layout
        layout = QHBoxLayout()
        voltage_label = QLabel()
        voltage_label.setText(str(self.consumer.voltage_input) + " V")
        current_label = QLabel()
        current_label.setText(str(self.consumer.current_input) + " mA")
        add_consumer_button = QPushButton("Add")

        # Layout
        layout.addWidget(voltage_label)
        layout.addWidget(current_label)
        layout.addWidget(add_consumer_button)

        # Widget settings
        add_consumer_button.clicked.connect(self.clicked_button_function)
        self.setTitle(self.consumer.info)
        self.setLayout(layout)

    def clicked_button_function(self):
        self.clicked_add_consumer.emit(self.consumer)
