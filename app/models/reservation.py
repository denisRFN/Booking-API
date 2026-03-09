import uuid
from sqlalchemy import Column, Date, Time, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.desk import Base


class Reservation(Base):

    __tablename__ = "reservations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    desk_id = Column(UUID(as_uuid=True), ForeignKey("desks.id"))

    user_id = Column(UUID(as_uuid=True))

    date = Column(Date)

    start_time = Column(Time)
    end_time = Column(Time)

    desk = relationship("Desk")
