from PyQt6.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QVBoxLayout, QMainWindow, \
    QLineEdit, QComboBox, QLabel, QDateEdit, QDateTimeEdit
from PyQt6.QtCore import QObject, pyqtSignal, QDate, QDateTime, QTime
from foo import return_widget, return_value, fill_widgets
from pprint import pprint


class EditWindow(QMainWindow):

    def __init__(self, database_manager, table, record: dict):
        super().__init__()
        self.database_manager = database_manager
        self.table = table
        self.setWindowTitle(self.table.name)
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.main_layout = self.MainLayout(self, record)
        self.main_widget.setLayout(self.main_layout)

    class MainLayout(QVBoxLayout, QObject):

        insert_request = pyqtSignal(object, dict)
        open_foreign_key_search_window_request = pyqtSignal(object)

        def __init__(self, window, record):
            print("MainLayout")
            QVBoxLayout.__init__(self)
            QObject.__init__(self)
            self.window = window
            self.sub_layouts = []
            self.record = record

            for column in self.window.table.columns:
                sub_layout = self.SubLayout(column, self.record[column.name])
                self.sub_layouts.append(sub_layout)
                self.addLayout(sub_layout)

            self.button_1 = QPushButton("Bearbeiten")
            self.button_1.clicked.connect(self.button_1_pushed)
            self.addWidget(self.button_1)
            self.button_2 = QPushButton("Zurücksetzen")
            self.button_2.clicked.connect(self.button_2_pushed)
            self.addWidget(self.button_2)

        def open_foreign_key_search_window(self, column):
            foreign_key = column.foreign_keys[0]  # needs documentation
            target_column = foreign_key.column
            target_table = target_column.table
            self.open_foreign_key_search_window_request.emit(target_table)

        def read_window(self):
            dic = {}
            for layout in self.sub_layouts:
                dic[layout.column.name] = layout.read_layout()
            pprint(dic)
            return dic

        def button_1_pushed(self):
            dic = self.read_window()
            table = self.window.table
            self.insert_request.emit(table, dic)

        def button_2_pushed(self):
            pass

        class SubLayout(QVBoxLayout):

            def __init__(self, column, value):
                super().__init__()
                self.column = column
                self.value = value
                self.label = QLabel(column.name)
                self.addWidget(self.label)
                self.widget = return_widget(column)
                if isinstance(self.widget, QPushButton):
                    self.widget.clicked.connect()
                fill_widgets(self.value, self.widget)
                self.addWidget(self.widget)

                if column.name == "uuid":
                    self.widget.setDisabled(True)


            def read_layout(self):
                return return_value(self.widget)
