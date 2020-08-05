from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import *
from mainwindow_class import MainWindow

'''Reference Credits.
(1) Žiga Benko's Youtube series Python UI application with Qt designer (Videos 7-10) - https://www.youtube.com/watch?v=mBvpoNLb654&list=PLuTktZ8WcEGTdId-Kjbj6gsZTk65yudJh
(2) PyQt5 Documentation (https://doc.qt.io/)
(3) Python Documentation (https://docs.python.org/3.8/library/)
(4) SQLite Documentation (sqlite.org)
(5) PyQt Tutorials (https://www.tutorialspoint.com/pyqt/index.htm)
'''

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainscreen = MainWindow()
    sys.exit(app.exec_())
