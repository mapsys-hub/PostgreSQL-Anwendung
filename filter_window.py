from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QPushButton, QTableWidgetItem, QComboBox
from PyQt6.QtCore import QObject, pyqtSignal
from database import Database
from custom_date_range_widget import DateRangeWidget

class SearchWindow(QWidget, QObject):
    search_request = pyqtSignal(Database.Table, list)

    def __init__(self, table: Database.Table):
        QWidget.__init__(self)
        QObject.__init__(self)

        self.table: Database.Table = table

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.setWindowTitle(self.table.name)

        self.search_table_widget = QTableWidget(1, len(self.table.columns))
        self.search_table_widget.setHorizontalHeaderLabels(column.name for column in self.table.columns)
        for index, column in enumerate(self.table.columns):
            if column.type.enums:
                print("ENUM")
                combo = QComboBox()
                combo.addItems(column.type.enums)
                self.search_table_widget.setCellWidget(1, index, combo)
            elif column.type == "DATE":
                print("DATE")
                date_range_widget = DateRangeWidget()
                self.search_table_widget.setCellWidget(1, index, date_range_widget)
            elif column.type == "BOOLEAN":
                print("BOOLEAN")
                combo = QComboBox()
                options = [True, False]
                combo.addItems(options)
                self.search_table_widget.setCellWidget(1, index, combo)
            else:
                item = QTableWidgetItem()
                self.search_table_widget.setItem(1, index, item)
        self.search_table_widget.resizeColumnsToContents()
        self.layout.addWidget(self.search_table_widget)

        self.search_button = QPushButton("Suchen")
        self.layout.addWidget(self.search_button)
        self.search_button.clicked.connect(self.send_search_request)

        self.clear_button = QPushButton("Eingabe löschen")
        self.layout.addWidget(self.clear_button)
        self.clear_button.clicked.connect(self.clear_search_table_widget)

        self.result_table_widget = QTableWidget(1, len(self.table.columns))
        self.result_table_widget.setHorizontalHeaderLabels(column.name for column in self.table.columns)
        self.result_table_widget.resizeColumnsToContents()
        self.layout.addWidget(self.result_table_widget)

    def send_search_request(self):
        row: list = self.read_data()
        self.search_request.emit(self.table, row)

    def clear_search_table_widget(self):
        self.search_table_widget.setRowCount(0)
        self.search_table_widget.setRowCount(1)

    def receive_search_results(self, rows: list):
        self.fill_result_table(rows)

    def receive_search_error(self):
        self.clear_search_table_widget()

    def clear_result_table_widget(self):
        self.result_table_widget.setRowCount(0)

    def fill_result_table(self, rows: list):
        self.clear_result_table_widget()
        for i, row in enumerate(rows):
            self.result_table_widget.insertRow(i)
            for n, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                self.result_table_widget.setItem(i, n, item)

    def read_data(self) -> list:
        row: list = []
        for n in range(len(self.table.columns)):
            try:
                item = self.search_table_widget.item(0, n)
                if item.text():
                    row.append(item.text())
                else:
                    row.append(None)
            except AttributeError:
                row.append(None)
        print(row)
        return row
