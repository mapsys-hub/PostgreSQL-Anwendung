from fields import UndefinedField
from marshmallow_sqlalchemy.convert import ModelConverter
from sqlalchemy.sql.sqltypes import NullType, TypeEngine
from typing import Callable, override, Type


class CustomModelConverter(ModelConverter):

    @override
    def _get_field_class_for_data_type(self, data_type: Type[TypeEngine]) -> Type[UndefinedField] | Callable:
        if isinstance(data_type, NullType):
            return UndefinedField
        else:
            return super()._get_field_class_for_data_type(data_type)
