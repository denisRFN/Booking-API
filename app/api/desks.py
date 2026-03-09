from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.desk import Desk
from app.schemas.desk_schema import DeskCreate

router = APIRouter()


@router.post("/desks")
def create_desk(data: DeskCreate, db: Session = Depends(get_db)):

    desk = Desk(**data.dict())

    db.add(desk)
    db.commit()
    db.refresh(desk)

    return desk


@router.get("/desks")
def get_desks(db: Session = Depends(get_db)):

    desks = db.query(Desk).all()

    return desks


@router.delete("/desks/{desk_id}")
def delete_desk(desk_id: str, db: Session = Depends(get_db)):

    desk = db.query(Desk).filter(Desk.id == desk_id).first()

    if desk:
        db.delete(desk)
        db.commit()

    return {"status": "deleted"}
