import sys
from loading_database import loading_database
from MainWindow import MainWindow
from PyQt5.QtWidgets import QApplication


def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    app.exec()
    dcdc_list, psu_list, consumer_list = loading_database()


main()