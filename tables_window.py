from PyQt6.QtWidgets import QWidget, QVBoxLayout, QListWidgetItem, QListWidget
from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtCore import Qt


class TablesWindow(QWidget, QObject):
    table_clicked = pyqtSignal(object)

    def __init__(self, database_manager):
        QWidget.__init__(self)
        QObject.__init__(self)
        self.database_manager = database_manager
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Tabellen")
        self.setGeometry(100, 100, 300, 150)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.tables_widget = QListWidget()
        self.layout.addWidget(self.tables_widget)
        self.tables_widget.itemDoubleClicked.connect(self.on_table_click)

    def on_table_click(self, item):
        table = item.table
        print(table)
        self.table_clicked.emit(table)

    def display_tables(self):
        for table in self.database_manager.database.tables:
            if table.schema_name == "public":
                item = CustomQListWidgetItem(table.name, table)
                if not self.database_manager.user.permissions[table.name]:
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsSelectable & ~Qt.ItemFlag.ItemIsEnabled)
                self.tables_widget.addItem(item)


class CustomQListWidgetItem(QListWidgetItem):
    def __init__(self, text, table):
        super().__init__(text)
        self.table = table
