import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QListWidget, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5.QtGui import QPixmap, QColor
class DragAndDrop(QWidget):

    def __init__(self):
        super().__init__()

        self.setAcceptDrops(True)
        self.label = QLabel(self)
        self.label.setGeometry(10, 10, 300, 300)

        # Create a list widget
        self.list_widget = QListWidget(self)
        self.list_widget.setMaximumWidth(150)

        # Create a label for the list widget title
        self.list_title = QLabel(self)
        self.list_title.setText("Geladene Bilder")
        self.list_title.setStyleSheet("color: white;")

        # Create a layout and add the label and list widget to it
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.list_title)
        self.layout.addWidget(self.list_widget)
        self.layout.addStretch(1)

        # Set dark gray background color for the list widget
        self.list_widget.setStyleSheet("background-color: rgb(40, 40, 40); color: white;")

        # Set the layout for the widget
        self.setLayout(self.layout)

        # Create a switch button to toggle the background color
        self.switch_button = QPushButton(self)
        self.switch_button.setText("Switch")
        self.switch_button.clicked.connect(self.toggle_background_color)
        self.switch_button.setGeometry(370, 10, 80, 25)

        self.setWindowTitle('Drag and Drop')
        self.setGeometry(300, 300, 470, 320)
        self.show()

        self.num_images = 0
        self.background_color = "rgb(40, 40, 40)"

    def dragEnterEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        self.num_images += 1
        self.set_image(event.mimeData().imageData())
        self.list_widget.addItem(f"Image {self.num_images}")

    def set_image(self, image):
        pixmap = QPixmap()
        pixmap.loadFromData(image)
        self.label.setPixmap(pixmap)

    def toggle_background_color(self):
        if self.background_color == "rgb(40, 40, 40)":
            self.background_color = "white"
            self.setStyleSheet(f"background-color: {self.background_color};")
            self.list_widget.setStyleSheet(f"background-color: {self.background_color}; color: black;")
            self.list_title.setStyleSheet("color: black;")
        else:
            self.background_color = "rgb(40, 40, 40)"
            self.setStyleSheet(f"background-color: {self.background_color};")
            self.list_widget.setStyleSheet(f"background-color: {self.background_color}; color: white;")
            self.list_title.setStyleSheet("color: white;")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DragAndDrop()
    sys.exit(app.exec_())
