from datetime import datetime

from pydantic import BaseModel


class DeskBase(BaseModel):
    name: str
    position_x: int
    position_y: int
    room: str


class DeskCreate(DeskBase):
    pass


class DeskUpdate(BaseModel):
    name: str | None = None
    position_x: int | None = None
    position_y: int | None = None
    room: str | None = None
    rotation_deg: int | None = None


class DeskRead(DeskBase):
    id: int
    created_at: datetime
    rotation_deg: int = 0

    class Config:
        from_attributes = True

