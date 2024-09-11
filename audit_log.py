from sqlalchemy import Column, Integer, String, JSON, TIMESTAMP, text, event, Uuid
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import sessionmaker, Session
import uuid

Base = declarative_base()


class AuditLogger:

    def __init__(self, database_manager):
        self.database_manager = database_manager

    @staticmethod
    def audit_event(mapper, _, target, operation):
        session = Session.object_session(target)
        table_name = mapper.mapped_table.name
        old_data = {}
        new_data = {}

        for attr in mapper.attrs:
            if attr.history.has_changes():
                old_value = getattr(target, attr.key)
                new_value = session.dirty.get(target, {}).get(attr.key, old_value)
                old_data[attr.key] = old_value
                new_data[attr.key] = new_value

        audit_log = AuditLogger.AuditLog(
            table_name=table_name,
            column_name="",
            record_uuid="",
            operation=operation,
            old_data=old_data,
            new_data=new_data,
            user_uuid="system"
        )
        session.add(audit_log)

    class AuditLog(Base):
        __abstract__ = True
        transaction_uuid = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)

        table_name = Column(String, nullable=False)
        column_name = Column(String, nullable=False)
        record_uuid = Column(String, nullable=False)
        operation = Column(String, nullable=False)  # INSERT, DELETE, UPDATE
        old_data = Column(JSON, nullable=True)
        new_data = Column(JSON, nullable=True)
        changed_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), nullable=False)
        user_uuid = Column(String, nullable=False)

        # foreign key record_uuid, user_uuid
