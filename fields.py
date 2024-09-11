from datetime import datetime
from marshmallow import fields, ValidationError
from typing import override


class UndefinedField(fields.Field):

    @override
    def _deserialize(self, value, attr, data, **kwargs):
        return value

    @override
    def _serialize(self, value, attr, obj, **kwargs):
        return value
