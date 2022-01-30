from PyQt5.QtWidgets import QWidget, QGridLayout, QGraphicsScene, QGraphicsView
from PyQt5 import QtCore
from Dcdc import Dcdc
from Psu import Psu
from Consumer import Consumer
from DcdcWidget import DcdcWidget
from PsuWidget import PsuWidget
from ConsumerWidget import ConsumerWidget


class PagePowerPlan(QGraphicsView):
    # Signal
    element_received = QtCore.pyqtSignal(bool)

    def __init__(self, parent=None):
        super(PagePowerPlan, self).__init__(parent)

        # Widget for pagePowerPlan
        self.scene = QGraphicsScene()
        self.scene.setSceneRect(0, 0, 500, 500);

        self.setScene(self.scene)

        # Variables
        self.list_element_widget = []

        self.widget_parent = 0
        self.widget_child = 0
        self.index_widget = 0
        self.add_child_parent_connection = False

    def add_new_element(self, element):
        # Find which is the element
        if element.component == "DCDC":

            # Create a copy from a database dcdc
            dcdc = element
            new_dcdc = Dcdc(dcdc.ref_component, dcdc.supplier, dcdc.current_max, dcdc.equivalence_code,
                            dcdc.voltage_input_min, dcdc.voltage_input_max, dcdc.voltage_output_min,
                            dcdc.voltage_output_max)
            new_dcdc.voltage_input = dcdc.voltage_input
            new_dcdc.voltage_output = dcdc.voltage_output
            new_dcdc.name = dcdc.name

            # Create the graphical widget of dcdc
            new_element_widget = DcdcWidget(new_dcdc)

        elif element.component == "PSU":
            psu = element
            new_psu = Psu(psu.ref_component, psu.supplier, psu.equivalence_code, psu.current_max,
                          psu.voltage_input, psu.voltage_output, psu.jack)
            new_psu.name = psu.name

            # Create the graphical widget of dcdc
            new_element_widget = PsuWidget(new_psu)

        elif element.component == "Consumer":
            consumer = element
            new_consumer = Consumer(consumer.name, consumer.ref_component, consumer.info, consumer.equivalence_code,
                                    consumer.voltage_input, consumer.current_input)

            # Create the graphical widget of dcdc
            new_element_widget = ConsumerWidget(new_consumer)

        # Add the new element in the list
        self.list_element_widget.append(new_element_widget)

        new_element_widget.widget_selected.connect(self.get_clicked_widget)

        # Add the new element on the page
        self.scene.addItem(new_element_widget)

        # If element is received emit a signal to the main window to close the window
        self.element_received.emit(True)

    def set_add_child_parent_connection(self, state: bool):
        # This function is used to start or end a child/parent add
        # It is connected to "Supply" toolbar button on MainWindow
        self.add_child_parent_connection = state
        if self.add_child_parent_connection:
            print("DEBUG : START add child ...")
        elif not self.add_child_parent_connection:
            print("DEBUG : End add child ...")

    def get_clicked_widget(self, widget):
        # This function is used to create a connexion between two widgets if
        # the "supply" toolbar button has been clicked
        # It is called by a click on a widget (signal : widget_selected())
        if self.add_child_parent_connection:
            self.index_widget = self.index_widget + 1
            # First click : select the parent widget
            if self.index_widget == 1:
                self.widget_parent = widget
                print("Parent : " + str(widget))
            # Second click : select the child widget
            elif self.index_widget == 2 and widget != self.widget_parent:
                self.widget_child = widget
                self.index_widget = 0
                print("Child : " + str(widget))

                print("Run add child")
                for element in self.list_element_widget:
                    if element == self.widget_parent:
                        parent = element
                    elif element == self.widget_child:
                        child = element
                # If this connection doesn't already exist, add parent and child
                # TODO : Create the if, not functional for the moment
                parent.add_child(child)
                child.add_parent(parent)

                self.set_add_child_parent_connection(False)

            else:
                self.index_widget = 0
                self.widget_parent = 0
                self.widget_child = 0
                self.set_add_child_parent_connection(False)
                print("DEBUG : Reset parent & child")
