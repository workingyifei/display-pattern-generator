import sys
from PyQt5 import QtWidgets, QtGui


def window():
    app = QtWidgets.QApplication(sys.argv)
    w = QtWidgets.QWidget()
    l1 = QtWidgets.QLabel(w)
    l2 = QtWidgets.QLabel(w)
    l1.setText("Hello World")
    l2.setPixmap(QtGui.QPixmap('./patterns/solid_red.bmp'))

    b = QtWidgets.QPushButton(w)
    b.setText("Generate Pattern")
    b.move(200, 50)
    w.setWindowTitle("Pattern Generator")
    w.setGeometry(200, 200, 1000, 600)
    l1.move(100, 20)
    w.show()
    sys.exit(app.exec_())


window()