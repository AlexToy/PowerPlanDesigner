from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView
from PyQt5 import QtCore
from Components.DcdcWidget import DcdcWidget
from Components.PsuWidget import PsuWidget
from Components.LdoWidget import LdoWidget
from Components.SwitchWidget import SwitchWidget
from Components.ConsumerWidget import ConsumerWidget
from Arrow import Arrow


class PagePowerPlan(QGraphicsView):
    # Signal
    element_received = QtCore.pyqtSignal(bool)

    def __init__(self, parent=None):
        super(PagePowerPlan, self).__init__(parent)

        # Widget for pagePowerPlan
        self.scene = QGraphicsScene()
        self.scene.setSceneRect(0, 0, 1000, 1000);

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
            new_dcdc = DcdcWidget(dcdc.ref_component, dcdc.supplier, dcdc.current_max, dcdc.mode, dcdc.equivalence_code,
                                  dcdc.voltage_input_min, dcdc.voltage_input_max, dcdc.voltage_output_min,
                                  dcdc.voltage_output_max, dcdc.formula_list)
            new_dcdc.voltage_input = dcdc.voltage_input
            new_dcdc.voltage_output = dcdc.voltage_output
            new_dcdc.name = dcdc.name
            new_dcdc.update_efficiency_value()

            new_element_widget = new_dcdc

        elif element.component == "PSU":
            psu = element
            new_psu = PsuWidget(psu.ref_component, psu.supplier, psu.equivalence_code, psu.current_max,
                                psu.voltage_input, psu.voltage_output, psu.jack)
            new_psu.name = psu.name

            new_element_widget = new_psu

        elif element.component == "LDO":

            # Create a copy from a database ldo
            ldo = element
            new_ldo = LdoWidget(ldo.ref_component, ldo.supplier, ldo.current_max, ldo.equivalence_code,
                                  ldo.voltage_input_min, ldo.voltage_input_max, ldo.voltage_output)
            new_ldo.voltage_input = ldo.voltage_input
            new_ldo.name = ldo.name

            new_element_widget = new_ldo

        elif element.component == "SWITCH":

            # Create a copy from a database switch
            switch = element
            new_switch = SwitchWidget(switch.switch_type, switch.current_max, switch.rds_on, switch.ref_component, switch.supplier,
                                      switch.equivalence_code, switch.voltage_input_min, switch.voltage_input_max,
                                      switch.voltage_bias_min, switch.voltage_bias_max)
            new_switch.voltage_input = switch.voltage_input
            new_switch.voltage_output = switch.voltage_input
            new_switch.name = switch.name

            new_element_widget = new_switch

        elif element.component == "Consumer":
            consumer = element
            new_consumer = ConsumerWidget(consumer.name, consumer.type, consumer.supplier, consumer.ref_component,
                                          consumer.equivalence_code, consumer.info, consumer.voltage_input,
                                          consumer.current_theoretical, consumer.current_min_measure,
                                          consumer.current_max_measure, consumer.current_peak)

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
                if parent.add_child(child) and child.add_parent(parent):
                    ### -------- ARROWS --------- ###
                    # Create and add Arrow on the scene
                    new_arrow = Arrow(parent.proxy_widget.updated_cursor_x, parent.proxy_widget.updated_cursor_y,
                                      parent.proxy_widget.width, parent.proxy_widget.height,
                                      child.proxy_widget.updated_cursor_x, child.proxy_widget.updated_cursor_y,
                                      child.proxy_widget.height)
                    self.scene.addItem(new_arrow)
                    # Add arrows on the arrows list
                    self.list_arrows.append(new_arrow)
                    # Connect the widget and the arrow to update the position
                    parent.proxy_widget.new_widget_position.connect(new_arrow.update_parent_position)
                    child.proxy_widget.new_widget_position.connect(new_arrow.update_child_position)
                    # Add the arrow to his parent
                    # TODO : warning, the dict can not be have two same key
                    parent.arrows.update({child: new_arrow})
                    print(parent.arrows)
                    ### -------- END OF ARROWS --------- ###

                # End off parent widget adds the child widget
                self.set_add_child_parent_connection(False)

            else:
                self.index_widget = 0
                self.widget_parent = 0
                self.widget_child = 0
                self.set_add_child_parent_connection(False)
                print("DEBUG : Reset parent & child")

        elif self.delete_element:
            print("Delete element and arrow")

            ### -------- ARROWS --------- ###
            # 1 Remove arrow for all children
            if len(widget.arrows) != 0:
                for arrow in widget.arrows.values():
                    self.list_arrows.remove(arrow)
                    self.scene.removeItem(arrow)
                # 2 Clear the dictionary
                widget.arrows.clear()
            # 3 Ask to the widget parent if it has one to remove the arrow
            if widget.parent != 0:
                self.scene.removeItem(widget.parent.arrows.get(widget))
                del widget.parent.arrows[widget]
            ### -------- END ARROWS --------- ###

            ### -------- WIDGET --------- ###
            # 1 Remove this widget as a parent to its children
            if widget.get_children() != 0:
                for child in widget.get_children():
                    child.remove_parent()
            # 2 Remove all children of the widget
            widget.remove_all_children()
            # 3 Remove this widget as a child to its parent
            if widget.get_parent() != 0:
                widget.get_parent().remove_child(widget)
            # 4 Remove its parent
            widget.remove_parent()
            # 5 Remove from the current widget list
            for element in self.list_element_widget:
                if element == widget:
                    self.list_element_widget.remove(element)
            # 6 Remove the ui of the widget from the scene
            self.scene.removeItem(widget.proxy_widget)
            ### -------- END WIDGET --------- ###

            self.set_delete_element(False)
