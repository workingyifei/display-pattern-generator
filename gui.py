import sys
import os
import logging
from typing import Dict, Optional
from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget, QPushButton, 
                          QAction, QLabel, QMenu, QMessageBox, QDialog, QComboBox, 
                          QVBoxLayout, QHBoxLayout, QFormLayout, QLineEdit, QCheckBox,
                          QSpinBox)
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PyQt5.QtCore import Qt
from pattern_generator import PatternGenerator
import cv2
import numpy as np

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "Pattern Generator"
        self.left = 100
        self.top = 100
        self.width = 1280
        self.height = 240
        self.current_label: Optional[QLabel] = None
        
        # Pattern categories and their specific options
        self.pattern_categories = {
            "Solid Color": ["red", "green", "blue", "white", "black", "gray16", "gray32", "gray64", 
                          "gray128", "yellow", "magenta", "cyan"],
            "Grayscale": ["normal", "reversed"],
            "Crosstalk": [
                "white_black", "gray32_black", "black_blue", "black_cyan",
                "gray32_white", "black_gray32", "green_gray32", "magenta_gray32",
                "red_gray32", "yellow_gray32"
            ],
            "Grid": ["1x2", "1x16", "2x1", "3x32", "6x1", "6x16", "6x32"]
        }

        self.icons = {
            "window": "./icon/window.png",
            "exit": "./icon/exit.png",
            "about": "./icon/about.png"
        }

        self.initUI()

    def initUI(self):
        # Window setup
        self.showMaximized()
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        try:
            self.setWindowIcon(QIcon(self.icons["window"]))
        except Exception as e:
            logger.error(f"Failed to load window icon: {e}")

        # Menu setup
        self.setupMenus()

        # Main layout
        main_widget = QWidget()
        self.main_layout = QVBoxLayout()

        # Resolution input
        form_layout = QFormLayout()
        self.width_input = QLineEdit()
        self.width_input.setPlaceholderText("Enter width")
        self.height_input = QLineEdit()
        self.height_input.setPlaceholderText("Enter height")
        form_layout.addRow("Width:", self.width_input)
        form_layout.addRow("Height:", self.height_input)
        self.main_layout.addLayout(form_layout)

        # Pattern category selection
        self.category_dropdown = QComboBox()
        self.category_dropdown.addItems(self.pattern_categories.keys())
        self.category_dropdown.currentTextChanged.connect(self.on_category_changed)
        self.main_layout.addWidget(QLabel("Select Pattern Category:"))
        self.main_layout.addWidget(self.category_dropdown)

        # Container for dynamic options
        self.options_container = QWidget()
        self.options_layout = QVBoxLayout()
        self.options_container.setLayout(self.options_layout)
        self.main_layout.addWidget(self.options_container)

        # Display button
        display_button = QPushButton("Display Pattern")
        display_button.clicked.connect(self.display_selected_pattern)
        self.main_layout.addWidget(display_button)

        main_widget.setLayout(self.main_layout)
        self.setCentralWidget(main_widget)

        # Initialize the options for the first category
        self.on_category_changed(self.category_dropdown.currentText())

    def clear_options_layout(self):
        """Clear all widgets from the options layout"""
        while self.options_layout.count():
            child = self.options_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def on_category_changed(self, category):
        """Update the options based on the selected category"""
        self.clear_options_layout()

        if category == "Solid Color":
            self.options_layout.addWidget(QLabel("Select Color:"))
            color_dropdown = QComboBox()
            color_dropdown.addItems(self.pattern_categories[category])
            color_dropdown.setObjectName("color_dropdown")
            self.options_layout.addWidget(color_dropdown)

        elif category == "Grayscale":
            reversed_check = QCheckBox("Reversed")
            reversed_check.setObjectName("reversed_check")
            self.options_layout.addWidget(reversed_check)

        elif category == "Crosstalk":
            self.options_layout.addWidget(QLabel("Select Combination:"))
            combo_dropdown = QComboBox()
            combo_dropdown.addItems(self.pattern_categories[category])
            combo_dropdown.setObjectName("combo_dropdown")
            self.options_layout.addWidget(combo_dropdown)

        elif category == "Grid":
            self.options_layout.addWidget(QLabel("Select Grid Pattern:"))
            grid_dropdown = QComboBox()
            grid_dropdown.addItems(self.pattern_categories[category])
            grid_dropdown.setObjectName("grid_dropdown")
            self.options_layout.addWidget(grid_dropdown)

    def get_selected_options(self):
        """Get the currently selected options based on the pattern category"""
        category = self.category_dropdown.currentText()
        options = {}

        for i in range(self.options_layout.count()):
            widget = self.options_layout.itemAt(i).widget()
            if widget is None:
                continue

            if category == "Solid Color" and widget.objectName() == "color_dropdown":
                options["color"] = widget.currentText()
            elif category == "Grayscale" and widget.objectName() == "reversed_check":
                options["reversed"] = widget.isChecked()
            elif category == "Crosstalk" and widget.objectName() == "combo_dropdown":
                bg_color, fg_color = widget.currentText().split("_")
                options["background_color"] = bg_color
                options["box_color"] = fg_color
            elif category == "Grid" and widget.objectName() == "grid_dropdown":
                options["pattern"] = widget.currentText()

        return options

    def display_selected_pattern(self):
        width = self.width_input.text()
        height = self.height_input.text()

        if not width.isdigit() or not height.isdigit():
            QMessageBox.critical(self, "Error", "Please enter valid numeric values for width and height.")
            return

        width = int(width)
        height = int(height)

        try:
            # Create pattern generator
            generator = PatternGenerator(width=width, height=height)
            
            # Generate pattern based on category and options
            category = self.category_dropdown.currentText()
            options = self.get_selected_options()
            
            if category == "Solid Color":
                image = generator.generate_solid_color(options["color"], save=False)
            elif category == "Grayscale":
                image = generator.generate_grayscale(reversed=options.get("reversed", False), save=False)
            elif category == "Crosstalk":
                image = generator.generate_crosstalk(
                    background_color=options["background_color"],
                    box_color=options["box_color"],
                    save=False
                )
            elif category == "Grid":
                pattern = options["pattern"]
                rows, cols = map(int, pattern.split("x"))
                image = generator.generate_grid(
                    rows=rows,
                    cols=cols,
                    save=False
                )

            # Convert OpenCV image (BGR) to QImage (RGB)
            height, width, channel = image.shape
            bytes_per_line = 3 * width
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            qimage = QImage(image_rgb.data, width, height, bytes_per_line, QImage.Format_RGB888)

            # Create a new window to display the image
            image_window = QDialog(self)
            image_window.setWindowTitle("Pattern Display")
            image_window.setGeometry(200, 200, width, height)

            # Create and show new label in the new window
            image_label = QLabel(image_window)
            image_label.setPixmap(QPixmap.fromImage(qimage))
            image_label.setGeometry(0, 0, width, height)
            image_window.exec_()
            
            logger.info(f"Successfully displayed {category} pattern")
        except Exception as e:
            logger.error(f"Error displaying pattern: {e}")
            QMessageBox.critical(self, "Error", f"Failed to display pattern: {e}")

    def setupMenus(self):
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('File')
        helpMenu = mainMenu.addMenu('Help')

        # Exit button
        self.addMenuAction(fileMenu, 'Exit', self.icons["exit"], 'Ctrl+Q', 
                          'Exit application', self.close)

        # About button
        self.addMenuAction(helpMenu, 'About', self.icons["about"], None,
                          'About the application', self.popupMessage)

    def addMenuAction(self, menu, name, icon_path, shortcut, status_tip, callback):
        try:
            action = QAction(QIcon(icon_path) if icon_path else None, name, self)
            if shortcut:
                action.setShortcut(shortcut)
            action.setStatusTip(status_tip)
            action.triggered.connect(callback)
            menu.addAction(action)
        except Exception as e:
            logger.error(f"Failed to add menu action {name}: {e}")

    def popupMessage(self):
        QMessageBox.about(self, "About", 
                         "Display Pattern Generator\n\n"
                         "A tool for testing display functionality and performance.\n\n")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
        event.accept()

def main():
    try:
        app = QApplication(sys.argv)
        window = Window()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        logger.error(f"Application error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()