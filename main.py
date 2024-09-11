from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QPalette, QColor
from sys import argv, exit
from dispatch import Dispatcher


class Main(QObject):
    app_started = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.app = QApplication(argv)
        self.app.setStyle("Fusion")
        print(self.app.style().objectName())
        self.dispatch = Dispatcher(self)

    def run_app(self):
        self.app_started.emit()
        exit(self.app.exec())


if __name__ == '__main__':
    main = Main()
    main.run_app()
