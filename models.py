from sqlalchemy import Boolean, Column, ForeignKey, String, Uuid
from sqlalchemy.orm import declarative_base, relationship
import uuid

Base = declarative_base()


class Users(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "config"}
    uuid = Column(Uuid, primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, nullable=False)
    permissions = relationship("_Permissions", back_populates="users")


class _Permissions(Base):
    __tablename__ = "permissions"
    __table_args__ = {"schema": "config"}
    user_uuid = Column(Uuid, ForeignKey("config.users.uuid"), primary_key=True)
    users = relationship("Users", back_populates="permissions")


def create_model_permissions(tables):
    columns = {}
    for table in tables:
        columns[table.name] = Column(table.name, Boolean, nullable=False)
    return type("Permissions", (_Permissions,), columns)
