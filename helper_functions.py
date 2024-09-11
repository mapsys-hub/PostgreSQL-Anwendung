from PyQt6.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QVBoxLayout, QMainWindow, \
    QLineEdit, QComboBox, QLabel, QDateEdit, QDateTimeEdit, QTimeEdit
from PyQt6.QtCore import QObject, pyqtSignal, QDate, QDateTime, QTime
from typing import Type
from custom_widgets import CustomQWidget


def remove_empty_values(d: dict) -> dict:
    return {k: v for k, v in d.items() if v}


def get_widget_data(widget):
    if isinstance(widget, QLineEdit):
        return widget.text()
    elif isinstance(widget, QComboBox):
        return widget.currentText()
    elif isinstance(widget, QDateEdit):
        return widget.date()
    elif isinstance(widget, QDateTimeEdit):
        return widget.dateTime()
    elif isinstance(widget, QTimeEdit):
        return widget.time()
    elif isinstance(widget, CustomQWidget):
        pass
    else:
        return None

def return_widget(data_type):
    pass
