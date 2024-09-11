from custom_model_converter import CustomModelConverter
from exceptions import InvalidDatabaseStructure
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy.orm.decl_api import DeclarativeMeta
from typing import Type


def check_table_structure(table_class: DeclarativeMeta):
    if not hasattr(table_class, "uuid"):
        message = f"Die Tabelle {table_class.__table__.name} hat keine Spalte 'uuid'."
        raise InvalidDatabaseStructure(message)
    else:
        column_object = getattr(table_class, "uuid")
    if not column_object.primary_key:
        message = f"Die Spalte 'uuid' ist nicht der Primärschlüssel der Tabelle {table_class.__table__.name}."
        raise InvalidDatabaseStructure(message)
    elif not column_object.type == "UUID":
        message = f"Die Spalte 'uuid' der Tabelle {table_class.__table__.name} ist nicht der Datentyp 'UUID'."
        raise InvalidDatabaseStructure(message)


def create_schema(table_class: DeclarativeMeta) -> Type[SQLAlchemyAutoSchema]:
    check_table_structure(table_class)

    class CustomSQLAlchemyAutoSchema(SQLAlchemyAutoSchema):
        class Meta:
            model: DeclarativeMeta = table_class
            load_instance: bool = True
            model_converter: CustomModelConverter = CustomModelConverter

    return CustomSQLAlchemyAutoSchema
