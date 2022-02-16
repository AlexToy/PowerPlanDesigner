import sys
from MainWindow import MainWindow
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QFile


def main():
    app = QApplication(sys.argv)
    load_stylesheet(app)
    main_window = MainWindow()
    main_window.show()
    app.exec()


def load_stylesheet(app, file = "style_sheet.css"):
    rc = QFile(file)
    rc.open(QFile.ReadOnly)
    content = rc.readAll().data()
    app.setStyleSheet(str(content, "UTF-8"))


main()