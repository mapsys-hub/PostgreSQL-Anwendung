from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class UserModel(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "config"}
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)

    #logs = relationship("LogModel", order_by=LogModel.log_id, back_populates="user")


class UserPrivilegesModel(Base):
    __tablename__ = "user_privileges"
    __table_args__ = {"schema": "config"}
    id = Column(Integer, primary_key=True, nullable=False)

    def __init__(self, table_names):
        for table_name in table_names:
            column = Column(table_name, Integer, nullable=False)
            self.__table__.append_column(column)
            setattr(self, table_name, column)


def compare_models(model_one, model_two):
    try:
        if not model_one.__table__.name == model_two.__table__.name:
            raise Exception
        elif not model_one.__table__.schema == model_two.__table__.schema:
            raise Exception
        elif not len(model_one.__table__.columns) == len(model_two.__table__.columns):
            raise Exception
        for i in range(len(model_one.__table__.columns)):
            column_model_one = model_one.__table__.columns[i]
            column_model_two = model_two.__table__.columns[i]
            if not column_model_one.name == column_model_two.name:
                raise Exception
            elif not str(column_model_one.type) == str(column_model_two.type):
                print(column_model_one.type)
                print(column_model_two.type)
                raise Exception
            elif not column_model_one.nullable == column_model_two.nullable:
                raise Exception
            elif not column_model_one.primary_key == column_model_two.primary_key:
                raise Exception
        return True
    except Exception as exception:
        print(exception)
        return False
