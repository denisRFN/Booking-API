from pydantic import BaseModel
from datetime import date, time
from uuid import UUID


class ReservationCreate(BaseModel):

    desk_id: UUID
    date: date
    start_time: time
    end_time: time
