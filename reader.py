from PyQt6.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QVBoxLayout, QMainWindow, \
    QLineEdit, QComboBox, QLabel, QDateEdit, QDateTimeEdit
from PyQt6.QtCore import QObject, pyqtSignal, QDate, QDateTime, QTime

from typing import Type

def read(widgets: list):
    for widget in widgets:
        if isinstance(widget, QLineEdit):
            pass
        if isinstance(widget, )