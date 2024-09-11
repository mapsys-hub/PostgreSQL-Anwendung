from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QPushButton, QTableWidgetItem
from PyQt6.QtCore import QObject, pyqtSignal
from database import Database


class AddWindow(QWidget, QObject):
    add_request = pyqtSignal(Database.Table, list)

    def __init__(self, table: Database.Table):
        QWidget.__init__(self)
        QObject.__init__(self)

        self.table: Database.Table = table

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.setWindowTitle(self.table.name)

        self.input_table_widget = QTableWidget(1, len(self.table.columns))
        self.input_table_widget.setHorizontalHeaderLabels(column.name for column in self.table.columns)
        self.input_table_widget.resizeColumnsToContents()
        self.layout.addWidget(self.input_table_widget)

        self.search_button = QPushButton("Hinzufügen")
        self.layout.addWidget(self.search_button)
        self.search_button.clicked.connect(self.send_add_request)

        self.clear_button = QPushButton("Eingabe löschen")
        self.layout.addWidget(self.clear_button)
        self.clear_button.clicked.connect(self.clear_input_table_widget)

        for index, column in enumerate(self.table.columns):
            if column.type.enums:
                print("ENUM")
                #dropbox or some
            elif column.type == "DATE":
                print("DATE")
                #datewindow
            elif column.type == "BOOLEAN":
                print("BOOLEAN")
                #dropbox or some
            else:
                pass
            #normal widget


    def send_add_request(self):
        row: list = self.read_data()
        self.add_request.emit(self.table, row)

    def clear_input_table_widget(self):
        self.input_table_widget.setRowCount(0)
        self.input_table_widget.setRowCount(1)

    def read_data(self) -> list:
        row: list = []
        for n in range(len(self.table.columns)):
            try:
                item = self.input_table_widget.item(0, n)
                if item.text():
                    row.append(item.text())
                else:
                    row.append(None)
            except AttributeError:
                row.append(None)
        print(row)
        return row
