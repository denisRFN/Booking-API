import uuid
from sqlalchemy import Column, String, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Desk(Base):

    __tablename__ = "desks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    name = Column(String, nullable=False)

    pos_x = Column(Integer)
    pos_y = Column(Integer)

    width = Column(Integer)
    height = Column(Integer)
