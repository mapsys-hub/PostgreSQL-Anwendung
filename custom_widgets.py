from datetime import datetime, date, time
from PyQt6.QtCore import QDate, QDateTime, QTime
from PyQt6.QtWidgets import QCheckBox, QDateEdit, QDateTimeEdit, QHBoxLayout, QWidget, QTimeEdit
from typing import override

class CustomQWidget(QWidget):
    def __init__(self):
        super().__init__()

    def reset(self):
        pass

    def read(self):
        pass

class QWidgetWithCheckBox(QWidget):
    def __init__(self):
        super().__init__()

    def reset(self):
        pass


class QDateEditWithCheckBox(QWidgetWithCheckBox):

    def __init__(self):
        super().__init__()
        self.date: date | None = None
        self.text: str = ""
        self.layout = QHBoxLayout()
        self.date_edit = QDateEdit()
        self.date_edit.setEnabled(False)
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        self.check_box = QCheckBox()
        self.check_box.stateChanged.connect(self.toggle_date_edit)
        self.layout.addWidget(self.date_edit)
        self.layout.addWidget(self.check_box)
        self.setLayout(self.layout)

    def toggle_date_edit(self):
        self.date_edit.setEnabled(self.check_box.isChecked())

    def read_date_edit(self):
        if self.date_edit.isEnabled():
            self.date = self.date_edit.date()
            self.text = self.date.toString("yyyy-MM-dd")
        else:
            self.date = None
            self.text = ""

    @override
    def reset(self):
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setEnabled(False)
        self.check_box.setChecked(False)


class QTimeEditWithCheckBox(QWidgetWithCheckBox):

    def __init__(self):
        super().__init__()
        self.time: time | None = None
        self.text = ""
        self.layout = QHBoxLayout()
        self.time_edit = QTimeEdit()
        self.time_edit.setEnabled(False)
        self.time_edit.setTime(QTime.currentTime())
        self.check_box = QCheckBox()
        self.check_box.stateChanged.connect(self.toggle_time_edit)
        self.layout.addWidget(self.time_edit)
        self.layout.addWidget(self.check_box)
        self.setLayout(self.layout)

    def toggle_time_edit(self):
        self.time_edit.setEnabled(self.check_box.isChecked())

    def read_time_edit(self):
        if self.time_edit.isEnabled():
            self.time = self.time_edit.time()
            self.text = self.time.toString("HH:mm:ss")
        else:
            self.time = None
            self.text = ""

    @override
    def reset(self):
        self.time_edit.setDate(QDate.currentDate())
        self.time_edit.setEnabled(False)
        self.check_box.setChecked(False)


class QDateTimeEditWithCheckBox(QWidgetWithCheckBox):

    def __init__(self):
        super().__init__()
        self.date_time: datetime | None = None
        self.text: str = ""
        self.layout = QHBoxLayout()
        self.date_time_edit = QDateTimeEdit()
        self.date_time_edit.setEnabled(False)
        self.date_time_edit.setDateTime(QDateTime.currentDateTime())
        self.date_time_edit.setTime(QTime(0, 0, 0))
        self.date_time_edit.setCalendarPopup(True)
        self.check_box = QCheckBox()
        self.check_box.stateChanged.connect(self.toggle_date_time_edit)
        self.layout.addWidget(self.date_time_edit)
        self.layout.addWidget(self.check_box)
        self.setLayout(self.layout)

    def toggle_date_time_edit(self):
        self.date_time_edit.setEnabled(self.check_box.isChecked())

    def read_date_time_edit(self):
        if self.date_time_edit.isEnabled():
            self.date_time = self.date_time_edit.dateTime()
            self.text = self.date_time.toString("yyyy-MM-dd HH:mm:ss")
        else:
            self.date_time = None
            self.text = ""

    @override
    def reset(self):
        self.date_time_edit.setDate(QDate.currentDate())
        self.date_time_edit.setEnabled(False)
        self.check_box.setChecked(False)
