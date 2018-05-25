import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLabel, QMenu, QMessageBox, QDialog
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
            "Red": "./patterns/solid_blue.bmp",
            "Green": "./patterns/solid_green.bmp",
            "Blue": "./patterns/solid_red.bmp",
            "White": "./patterns/solid_white.bmp",
            "Gray64": "./patterns/img_gray64.bmp",
            "Gray32": "./patterns/img_gray32.bmp",
            "Gray16": "./patterns/img_gray16.bmp",
            "Crosstalk": "./patterns/crosstalk.bmp",
            "Crosstalk_black": "./patterns/crosstalk_black.bmp",
            "Grayscale": "./patterns/grayscale.bmp",
            "Grayscale_reversed": "./patterns/grayscale_reversed.bmp",
            "32X6A": "./patterns/32x6A.bmp",
            "32X6B": "./patterns/32x6B.bmp",
            "32X3A": "./patterns/32x3A.bmp",
            "32X3B": "./patterns/32x3B.bmp",
            "16X6A": "./patterns/16x6A.bmp",
            "16X6B": "./patterns/16x6B.bmp",
            "2X1A": "./patterns/2x1A.bmp",
            "2X1B": "./patterns/2x1B.bmp",
            "1X6A": "./patterns/1x6A.bmp",
            "1x6B": "./patterns/1x6B.bmp",
            "1X2A": "./patterns/1x2A.bmp",
            "1x2B": "./patterns/1x2B.bmp",
            "Skip_one_dot": "./patterns/skip_one_dot.bmp"
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
        helpMenu = mainMenu.addMenu('Help')

        # Exit button
        exitButton = QAction(QIcon('./icon/exit.png'), 'Exit', self)
        exitButton.setShortcut('Ctrl+Q')
        exitButton.setStatusTip('Exit application')
        exitButton.triggered.connect(self.close)
        fileMenu.addAction(exitButton)

        # About button
        about = QAction(QIcon('./icon/about.png'), "About", self)
        about.triggered.connect(self.popupMessage)
        helpMenu.addAction(about)


        # red button
        redButton = QAction(QIcon(patterns["Red"]), 'Red', self)
        redButton.setShortcut('Alt + 1')
        redButton.setStatusTip('Solid red')
        redButton.triggered.connect(lambda: self.on_click(patterns["Red"]))
        patternMenu.addAction(redButton)

        # green button
        greenButton = QAction(QIcon(patterns["Green"]), 'Green', self)
        greenButton.setShortcut('Alt + 2')
        greenButton.setStatusTip('Solid green')
        greenButton.triggered.connect(lambda: self.on_click(patterns["Green"]))
        patternMenu.addAction(greenButton)

        # blue button
        blueButton = QAction(QIcon(patterns["Blue"]), 'Blue', self)
        blueButton.setShortcut('Alt + 3')
        blueButton.setStatusTip('Solid blue')
        blueButton.triggered.connect(lambda: self.on_click(patterns["Blue"]))
        patternMenu.addAction(blueButton)

        # white button
        whiteButton = QAction(QIcon(patterns["White"]), 'White', self)
        whiteButton.setShortcut('Alt + 4')
        whiteButton.setStatusTip('Solid white')
        whiteButton.triggered.connect(lambda: self.on_click(patterns["White"]))
        patternMenu.addAction(whiteButton)

        # Gray64 button
        gray64Button = QAction(QIcon(patterns["Gray64"]), 'Gray64', self)
        gray64Button.setShortcut('Alt + 5')
        gray64Button.setStatusTip('Gray64')
        gray64Button.triggered.connect(lambda: self.on_click(patterns["Gray64"]))
        patternMenu.addAction(gray64Button)

        # Gray32 button
        gray32Button = QAction(QIcon(patterns["Gray32"]), 'Gray32', self)
        gray32Button.setShortcut('Alt + 6')
        gray32Button.setStatusTip('Gray32')
        gray32Button.triggered.connect(lambda: self.on_click(patterns["Gray32"]))
        patternMenu.addAction(gray32Button)

        # Gray16 button
        gray16Button = QAction(QIcon(patterns["Gray16"]), 'Gray16', self)
        gray16Button.setShortcut('Alt + 7')
        gray16Button.setStatusTip('Gray16')
        gray16Button.triggered.connect(lambda: self.on_click(patterns["Gray16"]))
        patternMenu.addAction(gray16Button)

        # Crosstalk button
        crosstalkButton = QAction(QIcon(patterns["Crosstalk"]), 'Crosstalk', self)
        crosstalkButton.setShortcut('Alt + 8')
        crosstalkButton.setStatusTip('Crosstalk')
        crosstalkButton.triggered.connect(lambda: self.on_click(patterns["Crosstalk"]))
        patternMenu.addAction(crosstalkButton)

        # Crosstalk_black button
        crosstalkblackButton = QAction(QIcon(patterns["Crosstalk_black"]), 'Crosstalk black', self)
        crosstalkblackButton.setShortcut('Alt + 9')
        crosstalkblackButton.setStatusTip('Crosstalk_black')
        crosstalkblackButton.triggered.connect(lambda: self.on_click(patterns["Crosstalk_black"]))
        patternMenu.addAction(crosstalkblackButton)

        # Grayscale button
        grayscaleButton = QAction(QIcon(patterns["Grayscale"]), 'Grayscale', self)
        grayscaleButton.setShortcut('Alt + 10')
        grayscaleButton.setStatusTip('Grayscale')
        grayscaleButton.triggered.connect(lambda: self.on_click(patterns["Grayscale"]))
        patternMenu.addAction(grayscaleButton)

        # Grayscale_reversed button
        grayscaleReversedButton = QAction(QIcon(patterns["Grayscale_reversed"]), 'Grayscale reversed', self)
        grayscaleReversedButton.setShortcut('Alt + 11')
        grayscaleReversedButton.setStatusTip('Grayscale_reversed')
        grayscaleReversedButton.triggered.connect(lambda: self.on_click(patterns["Grayscale_reversed"]))
        patternMenu.addAction(grayscaleReversedButton)



        # save button

        # Label
        label = QLabel(self)

    def on_click(self, pattern):
        print("success")
        self.label = QLabel(self)
        image = QtGui.QImage(QtGui.QImageReader(pattern).read())
        self.label.setPixmap(QPixmap(image))
        self.label.setGeometry(0, 0, image.width(), image.height())
        self.label.show()


    def popupMessage(self):
        QMessageBox.about(self, "About", "Developed by yifei.li@byton.com")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
