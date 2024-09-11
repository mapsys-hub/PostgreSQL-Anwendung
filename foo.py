from sqlalchemy.sql.sqltypes import *
from PyQt6.QtWidgets import QLineEdit, QComboBox, QDateEdit, QDateTimeEdit, QTimeEdit, QPushButton
from PyQt6.QtCore import QDate, QDateTime, QTime
from PyQt6.QtGui import QIntValidator, QDoubleValidator
from uuid import uuid4
import datetime

def return_widget(column) -> Any:
    data_type = column.type
    foreign_keys = column.foreign_keys
    if foreign_keys:
        widget = QPushButton("Fremdschlüssel")
    elif isinstance(data_type, BigInteger):
        widget = QLineEdit()
        validator = QIntValidator()
        widget.setValidator(validator)
    elif isinstance(data_type, Boolean):
        widget = QComboBox()
        options = ["True", "False"]
        widget.addItems(options)
    elif isinstance(data_type, Date):
        widget = QDateEdit()
        widget.setDate(QDate.currentDate())
    elif isinstance(data_type, DateTime):
        widget = QDateTimeEdit()
        widget.setDateTime(QDateTime.currentDateTime())
    elif isinstance(data_type, Enum):
        widget = QComboBox()
        options = data_type.enums
        widget.addItems(options)
    elif isinstance(data_type, Float):
        widget = QLineEdit()
        validator = QDoubleValidator()
        widget.setValidator(validator)
    elif isinstance(data_type, Integer):
        widget = QLineEdit()
        validator = QIntValidator()
        widget.setValidator(validator)
    elif isinstance(data_type, Interval):
        widget = QLineEdit()
    elif isinstance(data_type, LargeBinary):
        widget = QLineEdit()
    elif isinstance(data_type, MatchType):
        widget = QLineEdit()
    elif isinstance(data_type, Numeric):
        widget = QLineEdit()
    elif isinstance(data_type, PickleType):
        widget = QLineEdit()
    elif isinstance(data_type, SchemaType):
        widget = QLineEdit()
    elif isinstance(data_type, SmallInteger):
        widget = QLineEdit()
        validator = QIntValidator()
        widget.setValidator(validator)
    elif isinstance(data_type, String):
        widget = QLineEdit()
        length = data_type.length
        widget.setMaxLength(length)
    elif isinstance(data_type, Text):
        widget = QLineEdit()
    elif isinstance(data_type, Time):
        widget = QTimeEdit()
        widget.setTime(QTime.currentTime())
    elif isinstance(data_type, Unicode):
        widget = QLineEdit()
    elif isinstance(data_type, UnicodeText):
        widget = QLineEdit()
    elif isinstance(data_type, Uuid):
        widget = QLineEdit()
        uuid = uuid4()
        widget.setText(uuid)
        widget.setDisabled(True)
    else:
        widget = QLineEdit()
    return widget


def fill_widgets(data, widget):
    if isinstance(widget, QLineEdit):
        widget.setText(data)
    elif isinstance(widget, QDateEdit):
        date_obj = QDate.fromString(data, "yyyy-MM-dd")
        widget.setDate(date_obj)
    elif isinstance(widget, QDateTimeEdit):
        datetime_obj = QDateTime.fromString(data, "yyyy-MM-dd HH:mm:ss")
        widget.setDateTime(datetime_obj)
    elif isinstance(widget, QTimeEdit):
        time_obj = QTime.fromString(data, "HH:mm:ss")
        widget.setTime(time_obj)
    elif isinstance(widget, QComboBox):
        widget.setCurrentText(data)


def return_value(widget):
    if isinstance(widget, QLineEdit):
        return widget.text()
    elif isinstance(widget, QDateEdit):
        return widget.date()
    elif isinstance(widget, QDateTimeEdit):
        test = widget.dateTime()
        datetime_obj = test.toPyDateTime()
        return datetime_obj
    elif isinstance(widget, QTimeEdit):
        return widget.time()
    elif isinstance(widget, QComboBox):
        return widget.currentText()
    else:
        return None
