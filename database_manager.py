from typing import Any
import warnings
from database import Database
from models import Users, create_model_permissions
from PyQt6.QtCore import QObject, pyqtSignal
from sqlalchemy import create_engine, cast, String, and_, or_, MetaData, inspect
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from custom_model_converter import CustomModelConverter
from sys import exit
from sqlalchemy.exc import SAWarning
from user import User
from exceptions import handle_exception
from helper_functions import remove_empty_values
from pprint import pprint
import datetime


class DatabaseManager(QObject):
    login_successful = pyqtSignal()
    login_unsuccessful = pyqtSignal()
    tables_retrieved = pyqtSignal()

    search_response = pyqtSignal(list)
    and_filter_response = pyqtSignal(list)
    or_filter_response = pyqtSignal(list)

    search_error = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.database = Database(self)
        self.engine = None
        self.inspector = None
        self.metadata = None
        self.base = None
        self.session = None
        self.user = None

    def connect_to_database(self, user, password, host, name):
        try:
            url = f"postgresql://{user}:{password}@{host}/{name}"
            self.engine = create_engine(url)
            self.metadata = MetaData()
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", category=SAWarning)
                self.metadata.reflect(bind=self.engine)
            self.base = automap_base(metadata=self.metadata)
            self.base.prepare()
            Session = sessionmaker(bind=self.engine)
            self.session = Session()
            self.initialize_tables()
            self.initialize_user(user)
            self.login_successful.emit()
        except Exception as exception:
            self.login_unsuccessful.emit()
            handle_exception(exception)
            exit()

    def initialize_user(self, user_name: str):
        user = self.session.query(Users).filter(Users.name == user_name).first()
        user_uuid: str = user.uuid
        permissions = create_model_permissions(self.database.tables)
        user_permissions_object = self.session.query(permissions).filter(permissions.user_uuid == user_uuid).first()
        user_permissions = {}
        for table in self.database.tables:
            user_permissions[table.name] = getattr(user_permissions_object, table.name)
        self.user = User(user_uuid, user_name, user_permissions)

    def initialize_tables(self):
        for table_name, table in self.metadata.tables.items():
            table_schema_name = table.schema
            if not table_schema_name:
                table_schema_name = "public"
            table_model_class = self.base.classes[table_name]
            table_schema_class = self.create_schema(table_model_class)
            table_columns = table.columns
            table_rows = self.session.query(table).all()
            table = Database.Table(table_schema_name, table_name, table_model_class, table_schema_class,
                                   table_columns, table_rows)
            self.database.tables.append(table)

    @staticmethod
    def validate(table: Database.Table, data: dict) -> True | False:
        processed_data: dict = remove_empty_values(data)
        try:
            Schema = table.schema_class
            schema = Schema()
            for key, value in processed_data.items():
                field = schema.fields[key]
                field.deserialize(value)
            return True
        except Exception as exception:
            handle_exception(exception)
            return False

    def search(self, table: Database.Table, text: str):
        try:
            filters = [cast(column, String).like(f"%{text}%") for column in table.columns]
            query = self.session.query(table.model_class).filter(or_(*filters))
            results = query.all()
            self.search_response.emit(results)
        except Exception as exception:
            handle_exception(exception)

    def and_filter(self, table: Database.Table, filters: dict[str: str]):
        if self.validate(table, filters):
            try:
                query = self.session.query(table.model_class).filter(and_(*self.build_search_query(filters, table.model_class)))
                results = query.all()
                print(results)
                self.and_filter_response.emit(results)
            except Exception as exception:
                handle_exception(exception)

    def or_filter(self, table: Database.Table, filters: dict[str: str]):
        if self.validate(table, filters):
            try:
                query = self.session.query(table.model_class).filter(or_(*self.build_search_query(filters, table.model_class)))
                results = query.all()
                print(results)
                self.or_filter_response.emit(results)
            except Exception as exception:
                handle_exception(exception)

    def return_one_record(self, table: Database.Table, uuid: str) -> dict[str: Any]:
        ...
    @staticmethod
    def build_search_query(filters, model):
        conditions = []
        for key, value in filters.items():
            column = getattr(model, key)
            conditions.append(cast(column, String).like(f"%{value}%"))
        return conditions

    @staticmethod
    def create_schema(model_class):
        class CustomSchema(SQLAlchemyAutoSchema):
            class Meta:
                model = model_class
                load_instance = True
                model_converter = CustomModelConverter
        return CustomSchema

    def fix_dic(self, dic: dict):
        new_dic = {}
        for key, value in dic.items():
            if isinstance(value, datetime.datetime):
                new_dic[key] = value.strftime("%Y-%m-%d %H:%M:%S")
            else:
                new_dic[key] = value
        return new_dic

    def insert(self, table: Database.Table, data: dict):
        new_dic = self.fix_dic(data)
        pprint(new_dic)
        try:
            #self.session.begin()
            schema_class = table.schema_class
            schema_instance = schema_class()
            validation_errors = schema_instance.validate(data=new_dic, session=self.session)
            if validation_errors:
                print("Invalid")
                for key, value in validation_errors.items():
                    print(f"{key}: {value}")
                raise Exception
            else:
                print("Valid")
                model_class = table.model_class
                serialized_data = schema_instance.dump(data)
                model_instance = model_class(**serialized_data)
                self.session.add(model_instance)
        except Exception as exception:
            self.session.rollback()
            handle_exception(exception)
        else:
            self.session.rollback()

    def update(self, table: Database.Table, primary_key, changes: dict):
        record = self.session.query(table.model_class).filter_by(uuid=primary_key).first()
        if not record:
            print("Record not found")

