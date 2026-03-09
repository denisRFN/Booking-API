from pydantic import BaseModel
from uuid import UUID


class DeskCreate(BaseModel):

    name: str
    pos_x: int
    pos_y: int
    width: int
    height: int


class DeskResponse(BaseModel):

    id: UUID
    name: str
    pos_x: int
    pos_y: int
    width: int
    height: int

    class Config:
        orm_mode = True
