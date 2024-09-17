from PyQt6.QtCore import QObject
from login_window import LoginWindow
from database_manager import DatabaseManager
from tables_window import TablesWindow
from table_window import TableWindow
from insert_window import InsertWindow
from foreign_key_search_window import ForeignKeySearchWindow
from edit_window import EditWindow

class Dispatcher(QObject):

    def __init__(self, main):
        super().__init__()
        self.main = main
        self.database_manager = DatabaseManager()
        self.login_window = LoginWindow()
        self.tables_window = TablesWindow(self.database_manager)
        self.table_window = None
        self.insert_window = None
        self.foreign_key_search_window = None

        # slots
        self.main.app_started.connect(self.login_window.show)
        self.login_window.login_submitted.connect(self.database_manager.connect_to_database)
        self.database_manager.login_successful.connect(self.login_window.hide)
        self.database_manager.login_unsuccessful.connect(self.login_window.reset)
        self.database_manager.login_successful.connect(self.tables_window.display_tables)
        self.database_manager.login_successful.connect(self.tables_window.show)
        self.tables_window.table_clicked.connect(self.initialize_table_window)

    def initialize_table_window(self, table):
        self.table_window = TableWindow(self.database_manager, table)
        self.table_window.show()
        self.table_window.main_layout.top_layout.search_request.connect(self.database_manager.search)
        self.database_manager.search_response.connect(self.table_window.main_layout.bottom_layout.table_add_rows)
        self.table_window.main_layout.middle_layout.and_filter_request.connect(self.database_manager.and_filter)
        self.table_window.main_layout.middle_layout.or_filter_request.connect(self.database_manager.or_filter)
        self.database_manager.and_filter_response.connect(self.table_window.main_layout.bottom_layout.table_add_rows)
        self.database_manager.or_filter_response.connect(self.table_window.main_layout.bottom_layout.table_add_rows)
        self.table_window.main_layout.open_insert_window.connect(self.initialize_insert_window)
        self.table_window.main_layout.middle_layout.open_foreign_key_search_window_request.connect(self.initialize_foreign_key_search_window)

    def initialize_insert_window(self, table):
        print("Initializing insert window")
        self.insert_window = InsertWindow(self.database_manager, table)
        self.insert_window.show()
        self.insert_window.main_layout.insert_request.connect(self.database_manager.insert)

    def initialize_foreign_key_search_window(self, table):
        print("Initializing foreign key search window")
        self.foreign_key_search_window = ForeignKeySearchWindow(self.database_manager, table)
        self.foreign_key_search_window.show()
        self.foreign_key_search_window.main_layout.bottom_layout.foreign_key_return_request.connect(lambda: print("Hey"))


    def initialize_edit_window(self, table, uuid):
        print("Initializing edit window")
        record_dict = self.database_manager.return_one_record(table, uuid)
        self.edit_window = EditWindow(self.database_manager, table, record_dict)
