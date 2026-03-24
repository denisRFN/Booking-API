from datetime import datetime

from pydantic import BaseModel


class ReservationBase(BaseModel):
    desk_id: int
    start_time: datetime
    end_time: datetime


class ReservationCreate(ReservationBase):
    pass


class ReservationRead(ReservationBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class ReservationWithDesk(ReservationRead):
    desk_name: str
    room: str


class AvailabilityDesk(BaseModel):
    id: int
    name: str
    position_x: int
    position_y: int
    room: str
    rotation_deg: int = 0
    status: str  # available | occupied | mine
    booked_by_name: str | None = None
    booked_by_email: str | None = None
    booked_from: datetime | None = None
    booked_to: datetime | None = None

