from PyQt5.QtWidgets import QWidget, QGridLayout, QGraphicsScene, QGraphicsView, QGraphicsRectItem
from PyQt5 import QtCore
from DcdcWidget import DcdcWidget
from PsuWidget import PsuWidget
from ConsumerWidget import ConsumerWidget
from Arrow import Arrow


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
        self.list_arrows = []

        self.widget_parent = 0
        self.widget_child = 0
        self.index_widget = 0
        self.add_child_parent_connection = False
        self.delete_element = False

    def add_new_element(self, element):
        # Find which is the element
        if element.component == "DCDC":

            # Create a copy from a database dcdc
            dcdc = element
            new_dcdc = DcdcWidget(dcdc.ref_component, dcdc.supplier, dcdc.current_max, dcdc.equivalence_code,
                                  dcdc.voltage_input_min, dcdc.voltage_input_max, dcdc.voltage_output_min,
                                  dcdc.voltage_output_max)
            new_dcdc.voltage_input = dcdc.voltage_input
            new_dcdc.voltage_output = dcdc.voltage_output
            new_dcdc.name = dcdc.name

            new_element_widget = new_dcdc

        elif element.component == "PSU":
            psu = element
            new_psu = PsuWidget(psu.ref_component, psu.supplier, psu.equivalence_code, psu.current_max,
                                psu.voltage_input, psu.voltage_output, psu.jack)
            new_psu.name = psu.name

            new_element_widget = new_psu

        elif element.component == "Consumer":
            consumer = element
            new_consumer = ConsumerWidget(consumer.name, consumer.ref_component, consumer.info,
                                          consumer.equivalence_code, consumer.voltage_input, consumer.current_input)

            new_element_widget = new_consumer

        # Add the new element in the list
        self.list_element_widget.append(new_element_widget)

        new_element_widget.widget_selected.connect(self.get_clicked_widget)

        # Add the new element on the page
        self.scene.addItem(new_element_widget.ui_init())

        # If element is received emit a signal to the main window to close the window
        self.element_received.emit(True)

    def set_delete_element(self, state: bool):
        # This function is used to start or finish  deleting a widget
        # It is connected to "Delete" toolbar button on MainWindow
        self.delete_element = state
        # Two toolbar button can not be used at the same time
        if self.add_child_parent_connection:
            self.set_add_child_parent_connection(False)

        if self.delete_element:
            print("DEBUG : START delete element ...")
        elif not self.delete_element:
            print("DEBUG : END delete element ...")

    def set_add_child_parent_connection(self, state: bool):
        # This function is used to start or end a child/parent add
        # It is connected to "Supply" toolbar button on MainWindow
        self.add_child_parent_connection = state
        # Two toolbar button can not be used at the same time
        if self.delete_element:
            self.set_delete_element(False)

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

                # Parent widget adds the child widget
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

                # Create and add Arrow on the scene
                new_arrow = Arrow(parent.proxy_widget.updated_cursor_x, parent.proxy_widget.updated_cursor_y,
                                  parent.grpbox_height, parent.grpbox_width, child.proxy_widget.updated_cursor_x,
                                  child.proxy_widget.updated_cursor_y, child.grpbox_height)
                self.scene.addItem(new_arrow)
                self.list_arrows.append(new_arrow)
                parent.proxy_widget.new_widget_position.connect(new_arrow.update_parent_position)
                child.proxy_widget.new_widget_position.connect(new_arrow.update_child_position)

                # End off parent widget adds the child widget
                self.set_add_child_parent_connection(False)

            else:
                self.index_widget = 0
                self.widget_parent = 0
                self.widget_child = 0
                self.set_add_child_parent_connection(False)
                print("DEBUG : Reset parent & child")

        elif self.delete_element:
            print("Delete element")
            # 1 Remove all children of the widget
            widget.remove_all_children()
            # 2 Remove this widget as a child to its parent
            if widget.get_parent() != 0:
                widget.get_parent().remove_child(widget)
            # 3 Remove its parent
            widget.remove_parent()
            # 4 Remove from the current widget list
            for element in self.list_element_widget:
                if element == widget:
                    self.list_element_widget.remove(element)
            # 5 Remove the ui of the widget from the scene
            self.scene.removeItem(widget.proxy_widget)

            self.set_delete_element(False)