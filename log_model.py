from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class LogModel(Base):
    __tablename__ = "log"
    __table_args__ = {"schema": "config"}
    log_id = Column(Integer, primary_key=True, nullable=False)
    record_id = Column(Integer, nullable=False)
    table_name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("config.user.user_id"), nullable=False)
    change_datetime = Column(DateTime, nullable=False)
    change_type = Column(Enum("add", "delete", "edit"), nullable=False)

    user = relationship("UserModel", back_populates="logs")



    def __init__(self, table_names):
        for table_name in table_names:
            column = Column(table_name, Integer, nullable=False)
            self.__table__.append_column(column)
            setattr(self, table_name, column)
