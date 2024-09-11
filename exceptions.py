from PyQt6.QtWidgets import QMessageBox
from sys import exit


class CustomException(Exception):
    pass


class CriticalCustomException(CustomException):
    pass


class InvalidDatabaseStructure(CriticalCustomException):
    pass


def handle_exception(exception: Exception | str):
    ExceptionMessageBox(exception)
    if isinstance(exception, Exception):
        if isinstance(exception, CriticalCustomException):
            exit()


class ExceptionMessageBox(QMessageBox):

    def __init__(self, exception: Exception | str):
        super().__init__()
        self.exception: Exception | str = exception
        self.setWindowTitle("Fehler")
        self.setIcon(QMessageBox.Icon.Critical)
        self.setText(str(self.exception))
        if isinstance(exception, Exception):
            for attr in dir(exception.__traceback__):
                text = getattr(exception.__traceback__, attr)
                print(f"{attr}: {text}")
        self.setStandardButtons(QMessageBox.StandardButton.Ok)
        self.exec()
