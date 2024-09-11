from PyQt6.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QVBoxLayout, QMainWindow, \
    QLineEdit, QComboBox, QDateEdit, QDateTimeEdit, QTimeEdit
from PyQt6.QtCore import QObject, pyqtSignal, QDate
from datetime import datetime
from custom_widgets import QDateEditWithCheckBox, QTimeEditWithCheckBox, QDateTimeEditWithCheckBox, QWidgetWithCheckBox
from pprint import pprint
from exceptions import handle_exception


class TableWindow(QMainWindow):

    def __init__(self, database_manager, table):
        super().__init__()
        self.database_manager = database_manager
        self.table = table
        self.setWindowTitle(self.table.name)
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.main_layout = self.MainLayout(self)
        self.main_widget.setLayout(self.main_layout)

    class MainLayout(QVBoxLayout, QObject):

        open_insert_window = pyqtSignal(object)

        def __init__(self, window):
            QVBoxLayout.__init__(self)
            QObject.__init__(self)
            self.window = window
            self.top_layout = self.TopLayout(self)
            self.middle_layout = self.MiddleLayout(self)
            self.bottom_layout = self.BottomLayout(self)
            self.addLayout(self.top_layout)  # crashes here
            self.addLayout(self.middle_layout)
            self.addLayout(self.bottom_layout)
            self.button = QPushButton("Hinzufügen")
            self.button.clicked.connect(self.button_pushed)
            self.addWidget(self.button)

            # self.date_cell_widget = DateCellWidget()
            # self.addWidget(self.date_cell_widget)

        def button_pushed(self):
            print("Button pushed")
            table = self.window.table
            self.open_insert_window.emit(table)

        class TopLayout(QHBoxLayout, QObject):
            search_request = pyqtSignal(object, str)

            def __init__(self, main_layout):
                QHBoxLayout.__init__(self)
                QObject.__init__(self)
                self.main_layout = main_layout
                self.line_edit = QLineEdit()
                self.addWidget(self.line_edit)
                self.button = QPushButton("Suchen")
                self.button.clicked.connect(self.button_pushed)
                self.addWidget(self.button)

            def button_pushed(self):
                try:
                    table = self.main_layout.window.table
                    text = self.line_edit.text()
                    try:
                        datetime_object = datetime.strptime(text, "%d.%m.%Y")
                        text = datetime_object.strftime("%Y-%m-%d")
                    except ValueError:
                        pass
                    ...
                    self.search_request.emit(table, text)
                except Exception as exception:
                    print(exception)

        class MiddleLayout(QHBoxLayout, QObject):
            and_filter_request = pyqtSignal(object, dict)
            or_filter_request = pyqtSignal(object, dict)

            open_foreign_key_search_window_request = pyqtSignal(object)

            def __init__(self, main_layout):
                QHBoxLayout.__init__(self)
                QObject.__init__(self)
                self.main_layout = main_layout
                self.table = QTableWidget()
                self.table.setColumnCount(len(self.main_layout.window.table.columns) + 1)
                self.table.setHorizontalHeaderLabels([column.name for column in self.main_layout.window.table.columns])
                self.table.setRowCount(1)
                for i, column in enumerate(self.main_layout.window.table.columns):
                    print(dir(column))
                    if column.foreign_keys:
                        item = QPushButton("Fremdschlüssel suchen")
                        item.clicked.connect(lambda: self.open_foreign_key_search_window(column))
                    elif str(column.type) == "BOOLEAN":
                        item = QComboBox()
                        item.addItems(["True", "False"])
                        item.setCurrentIndex(-1)
                    elif str(column.type) == "DATE":  # DATE
                        item = QDateEditWithCheckBox()
                    elif str(column.type) == "ENUM":
                        item = QComboBox()
                        item.addItems([column.enums])
                        item.setCurrentIndex(-1)
                    elif str(column.type) == "TIME":
                        item = QTimeEditWithCheckBox()
                    elif str(column.type) == "TIMESTAMP":
                        item = QDateTimeEditWithCheckBox()
                    else:
                        item = QTableWidgetItem()
                    if isinstance(item, QTableWidgetItem):
                        self.table.setItem(0, i, item)
                    else:
                        self.table.setCellWidget(0, i, item)

                self.addWidget(self.table)
                self.button_1 = QPushButton("Und")
                self.button_1.clicked.connect(self.button_1_pushed)
                self.addWidget(self.button_1)
                self.button_2 = QPushButton("Oder")
                self.button_2.clicked.connect(self.button_2_pushed)
                self.addWidget(self.button_2)
                self.button_3 = QPushButton("Zurücksetzen")
                self.button_3.clicked.connect(self.button_3_pushed)
                self.table.setCellWidget(0, 11, self.button_3)

            def open_foreign_key_search_window(self, column):
                foreign_key = column.foreign_keys[0]  # needs documentation
                target_column = foreign_key.column
                target_table = target_column.table
                self.open_foreign_key_search_window_request.emit(target_table)

            def reset_table(self):
                table = self.main_layout.window.table

                for i, column in enumerate(table.columns):
                    item = self.table.item(0, i)
                    if not item:
                        item = self.table.cellWidget(0, i)
                    if isinstance(item, QTableWidgetItem):
                        item.setText("")
                    elif isinstance(item, QWidgetWithCheckBox):
                        item.reset()
                    elif isinstance(item, QComboBox):
                        item.setCurrentIndex(-1)

            def read_table(self):
                try:
                    filters = {}
                    table = self.main_layout.window.table
                    for i, column in enumerate(table.columns):
                        item = self.table.item(0, i)
                        if not item:
                            item = self.table.cellWidget(0, i)
                        if isinstance(item, QTableWidgetItem):
                            try:
                                text = item.text()
                            except AttributeError:
                                pass
                        elif isinstance(item, QComboBox):
                            text = item.currentText()
                        elif isinstance(item, QDateEditWithCheckBox):
                            item.read_date_edit()
                            text = item.text
                        elif isinstance(item, QTimeEditWithCheckBox):
                            item.read_time_edit()
                            text = item.text
                        elif isinstance(item, QDateTimeEditWithCheckBox):
                            item.read_date_time_edit()
                            text = item.text
                        filters[column.name] = text
                    return filters
                except Exception as exception:
                    handle_exception(exception)

            def button_1_pushed(self):  # Und
                filters = self.read_table()
                pprint(filters)
                table = self.main_layout.window.table
                self.and_filter_request.emit(table, filters)

            def button_2_pushed(self):  # Oder
                try:
                    filter_args = {}
                    table = self.main_layout.window.table
                    print("Button 2 pushed")  # Suchen
                    for i, column in enumerate(self.main_layout.window.table.columns):
                        item = self.table.item(0, i)
                        try:
                            text = item.text()
                            filter_args[column.name] = text
                        except AttributeError:
                            pass
                    self.or_filter_request.emit(table, filter_args)
                except Exception as exception:
                    print(exception)

            def button_3_pushed(self):  # resets the QTableWidget
                print("Button 3 pushed")  # placeholder
                self.reset_table()

        class BottomLayout(QHBoxLayout, QObject):

            open_edit_window = pyqtSignal(str)  # uuid

            def __init__(self, main_layout):
                QHBoxLayout.__init__(self)
                QObject.__init__(self)
                self.main_layout = main_layout
                self.table = QTableWidget()
                self.table.setColumnCount(len(self.main_layout.window.table.columns) + 1)
                self.table.setHorizontalHeaderLabels([column.name for column in self.main_layout.window.table.columns])
                self.addWidget(self.table)
                self.buttons = {}

            def button_pushed(self):
                sender = self.sender()
                index = self.table.indexAt(sender.pos())
                row_index = index.row()
                for n, column in enumerate(self.main_layout.window.table.columns):
                    item = self.table.item(row_index, n)
                    item_text = item.text()
                    if item_text == "uudi":
                        self.open_edit_window.emit(item_text)


                

                print("Button pushed")  # Bearbeiten

            def table_add_rows(self, rows):
                self.table.setRowCount(0)  # reset the table, or some like this
                for i, row in enumerate(rows):
                    self.table.insertRow(i)
                    for n, column in enumerate(self.main_layout.window.table.columns):
                        value = getattr(row, column.name)
                        self.table.setItem(i, n, QTableWidgetItem(str(value)))
                        button = QPushButton("Bearbeiten")
                        # self.buttons[button] = getattr(row, "uuid")
                        self.table.setCellWidget(i, 11, button)
