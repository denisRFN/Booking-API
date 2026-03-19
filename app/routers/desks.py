from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_admin
from app.database.session import get_db
from app.models.desk import Desk
from app.models.desk_layout import DeskLayout
from app.schemas.desk import DeskCreate, DeskUpdate, DeskRead


router = APIRouter(prefix="/desks", tags=["desks"])


@router.get("", response_model=list[DeskRead])
def list_desks(db: Session = Depends(get_db)):
    desks = db.query(Desk).order_by(Desk.room, Desk.name).all()
    layouts = db.query(DeskLayout).all()
    by_desk_id = {l.desk_id: l.rotation_deg for l in layouts}

    return [
        DeskRead(
            id=d.id,
            name=d.name,
            position_x=d.position_x,
            position_y=d.position_y,
            room=d.room,
            created_at=d.created_at,
            rotation_deg=by_desk_id.get(d.id, 0),
        )
        for d in desks
    ]


@router.post("", response_model=DeskRead, status_code=status.HTTP_201_CREATED)
def create_desk(
    desk_in: DeskCreate,
    db: Session = Depends(get_db),
    _: None = Depends(get_current_admin),
):
    desk = Desk(**desk_in.dict())
    db.add(desk)
    db.commit()
    db.refresh(desk)
    # Ensure there is always a layout row for rotation settings.
    db.add(DeskLayout(desk_id=desk.id, rotation_deg=0))
    db.commit()
    return DeskRead(
        id=desk.id,
        name=desk.name,
        position_x=desk.position_x,
        position_y=desk.position_y,
        room=desk.room,
        created_at=desk.created_at,
        rotation_deg=0,
    )


@router.put("/{desk_id}", response_model=DeskRead)
def update_desk(
    desk_id: int,
    desk_in: DeskUpdate,
    db: Session = Depends(get_db),
    _: None = Depends(get_current_admin),
):
    desk = db.query(Desk).filter(Desk.id == desk_id).first()
    if not desk:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Desk not found")

    data = desk_in.dict(exclude_unset=True)
    rotation_value = data.pop("rotation_deg", None)

    for field, value in data.items():
        setattr(desk, field, value)

    # Persist position/name changes.
    db.commit()
    db.refresh(desk)

    # Persist rotation changes (stored in a separate table to avoid migrations).
    if rotation_value is not None:
        layout = db.query(DeskLayout).filter(DeskLayout.desk_id == desk_id).first()
        if layout is None:
            layout = DeskLayout(desk_id=desk_id, rotation_deg=rotation_value)
            db.add(layout)
        else:
            layout.rotation_deg = rotation_value
        db.commit()

    rotation_current = (
        db.query(DeskLayout).filter(DeskLayout.desk_id == desk_id).first().rotation_deg
        if db.query(DeskLayout).filter(DeskLayout.desk_id == desk_id).first() is not None
        else 0
    )

    return DeskRead(
        id=desk.id,
        name=desk.name,
        position_x=desk.position_x,
        position_y=desk.position_y,
        room=desk.room,
        created_at=desk.created_at,
        rotation_deg=rotation_current,
    )


@router.delete("/{desk_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_desk(
    desk_id: int,
    db: Session = Depends(get_db),
    _: None = Depends(get_current_admin),
):
    desk = db.query(Desk).filter(Desk.id == desk_id).first()
    if not desk:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Desk not found")

    db.delete(desk)
    db.commit()
    return None

