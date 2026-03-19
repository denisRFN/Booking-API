from datetime import date, datetime, time, timedelta

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.database.session import get_db
from app.models.desk import Desk
from app.models.desk_layout import DeskLayout
from app.models.reservation import Reservation
from app.models.user import User
from app.schemas.reservation import AvailabilityDesk


router = APIRouter(prefix="/availability", tags=["availability"])


@router.get("", response_model=list[AvailabilityDesk])
def get_availability(
    date_: date = Query(..., alias="date"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    start_dt = datetime.combine(date_, time.min)
    end_dt = datetime.combine(date_, time.max)

    desks = db.query(Desk).all()
    layouts = db.query(DeskLayout).all()
    by_desk_id = {l.desk_id: l.rotation_deg for l in layouts}
    reservations = (
        db.query(Reservation)
        .filter(
            and_(Reservation.start_time < end_dt, Reservation.end_time > start_dt),
        )
        .all()
    )

    by_desk: dict[int, list[Reservation]] = {}
    for r in reservations:
        by_desk.setdefault(r.desk_id, []).append(r)

    result: list[AvailabilityDesk] = []
    for d in desks:
        status = "available"
        res_for_desk = by_desk.get(d.id, [])
        if res_for_desk:
            if any(r.user_id == current_user.id for r in res_for_desk):
                status = "mine"
            else:
                status = "occupied"

        result.append(
            AvailabilityDesk(
                id=d.id,
                name=d.name,
                position_x=d.position_x,
                position_y=d.position_y,
                room=d.room,
                rotation_deg=by_desk_id.get(d.id, 0),
                status=status,
            )
        )
    return result

