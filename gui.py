import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLabel, QMenu
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PyQt5 import QtGui
from PyQt5.QtCore import QDateTime, QDate, QTime, Qt



class Window(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = "Pattern Generator"
        self.left = 100
        self.top = 100
        self.width = 1280
        self.height = 240

        self.initUI()


    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowIcon(QIcon("./img/icon.png"))  # didn't work

        # datetime = QDateTime.currentDateTime()
        # print(datetime.toString())
        # print(datetime.toString(Qt.ISODate))
        # print(datetime.toString(Qt.DefaultLocaleLongDate))
        # print("Local UTC time is:" + datetime.toUTC().toString())
        #
        #
        # time = QTime.currentTime()
        # print(time.toString())
        # print(time.toString(Qt.DefaultLocaleLongDate))


        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('File')
        patternMenu = mainMenu.addMenu('Pattern')
        aboutMenu = mainMenu.addMenu('About')


        # exit button
        exitButton = QAction(QIcon('./icon/exit.png'), 'Exit', self)
        exitButton.setShortcut('Ctrl+Q')
        exitButton.setStatusTip('Exit application')
        exitButton.triggered.connect(self.close)
        fileMenu.addAction(exitButton)

        # blue button
        blueButton = QAction(QIcon('./pattern/solid_blue.bmp'), 'Blue', self)
        blueButton.setShortcut('Alt + 1')
        blueButton.setStatusTip('Solid blue')
        blueButton.triggered.connect(self.on_click)
        patternMenu.addAction(blueButton)


        # save button

        # Label
        label = QLabel(self)


    def on_click(self):
        print("success")
        self.label = QLabel(self)
        image = QtGui.QImage(QtGui.QImageReader("./patterns/solid_blue.bmp").read())
        self.label.setPixmap(QPixmap(image))
        self.label.setGeometry(0,0,image.width(), image.height())
        self.label.show()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())