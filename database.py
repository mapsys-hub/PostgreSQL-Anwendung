from marshmallow_sqlalchemy.schema import SQLAlchemyAutoSchemaMeta
from sqlalchemy.orm.decl_api import DeclarativeMeta


class Database:

    def __init__(self, database_manager):
        self.database_manager = database_manager
        self.tables: list[Database.Table] = []

    class Table:

        def __init__(self, schema_name: str,
                     name: str,
                     model_class: DeclarativeMeta,
                     schema_class: SQLAlchemyAutoSchemaMeta,
                     columns: ...,
                     rows: ...):
            self.schema_name: str = schema_name
            self.name: str = name
            self.model_class: DeclarativeMeta = model_class
            self.schema: SQLAlchemyAutoSchemaMeta = schema_class
            self.columns: ... = columns
            self.rows: ... = rows

    class Record:

        def __init__(self, table):
            self.table = table
            self.values = {}

        def update(self, new_values):
            ...

