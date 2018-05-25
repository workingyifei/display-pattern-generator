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


        patterns = {
            "Red": "solid_blue.bmp",
            "Green": "solid_green.bmp",
            "Blue": "solid_red.bmp"
        }

        icons = {
            "window": "./icon/window.png"
        }

        # Window
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowIcon(QIcon(icons["window"]))


        # Menu
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




        # red button
        redButton = QAction(QIcon('./pattern/solid_blue.bmp'), 'Red', self)
        redButton.setShortcut('Alt + 1')
        redButton.setStatusTip('Solid red')
        redButton.triggered.connect(lambda: self.on_click(patterns["Red"]))
        patternMenu.addAction(redButton)

        # green button
        greenButton = QAction(QIcon('./pattern/solid_green.bmp'), 'Green', self)
        greenButton.setShortcut('Alt + 2')
        greenButton.setStatusTip('Solid green')
        greenButton.triggered.connect(lambda: self.on_click(patterns["Green"]))
        patternMenu.addAction(greenButton)

        # blue button
        blueButton = QAction(QIcon('./pattern/solid_red.bmp'), 'Blue', self)
        blueButton.setShortcut('Alt + 1')
        blueButton.setStatusTip('Solid blue')
        blueButton.triggered.connect(lambda: self.on_click(patterns["Blue"]))
        patternMenu.addAction(blueButton)


        #
        # # blue button
        # blueButton = QAction(QIcon('./pattern/solid_blue.bmp'), 'Blue', self)
        # blueButton.setShortcut('Alt + 1')
        # blueButton.setStatusTip('Solid blue')
        # blueButton.triggered.connect(self.on_click)
        # patternMenu.addAction(blueButton)
        #
        # # blue button
        # blueButton = QAction(QIcon('./pattern/solid_blue.bmp'), 'Blue', self)
        # blueButton.setShortcut('Alt + 1')
        # blueButton.setStatusTip('Solid blue')
        # blueButton.triggered.connect(self.on_click)
        # patternMenu.addAction(blueButton)
        #
        # # blue button
        # blueButton = QAction(QIcon('./pattern/solid_blue.bmp'), 'Blue', self)
        # blueButton.setShortcut('Alt + 1')
        # blueButton.setStatusTip('Solid blue')
        # blueButton.triggered.connect(self.on_click)
        # patternMenu.addAction(blueButton)
        #
        # # blue button
        # blueButton = QAction(QIcon('./pattern/solid_blue.bmp'), 'Blue', self)
        # blueButton.setShortcut('Alt + 1')
        # blueButton.setStatusTip('Solid blue')
        # blueButton.triggered.connect(self.on_click)
        # patternMenu.addAction(blueButton)
        #
        # # blue button
        # blueButton = QAction(QIcon('./pattern/solid_blue.bmp'), 'Blue', self)
        # blueButton.setShortcut('Alt + 1')
        # blueButton.setStatusTip('Solid blue')
        # blueButton.triggered.connect(self.on_click)
        # patternMenu.addAction(blueButton)
        #
        # # blue button
        # blueButton = QAction(QIcon('./pattern/solid_blue.bmp'), 'Blue', self)
        # blueButton.setShortcut('Alt + 1')
        # blueButton.setStatusTip('Solid blue')
        # blueButton.triggered.connect(self.on_click)
        # patternMenu.addAction(blueButton)


        # save button

        # Label
        label = QLabel(self)


    def on_click(self, pattern):
        print("success")
        self.label = QLabel(self)
        image = QtGui.QImage(QtGui.QImageReader("./patterns/" + pattern).read())
        self.label.setPixmap(QPixmap(image))
        self.label.setGeometry(0,0,image.width(), image.height())
        self.label.show()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())