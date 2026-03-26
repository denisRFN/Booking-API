from datetime import date, datetime, time

from fastapi import APIRouter, Depends, Query
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

    # Legacy data may contain multiple desks booked by same user in one day.
    # Keep only one desk as "mine" for the day; show others as "occupied".
    mine_reservations = [r for r in reservations if r.user_id == current_user.id]
    primary_mine_reservation = (
        sorted(mine_reservations, key=lambda r: (r.start_time, r.created_at))[0]
        if mine_reservations
        else None
    )

    result: list[AvailabilityDesk] = []
    for d in desks:
        status = "available"
        booked_by_name = None
        booked_by_email = None
        booked_from = None
        booked_to = None
        res_for_desk = by_desk.get(d.id, [])
        if res_for_desk:
            mine_res = [r for r in res_for_desk if r.user_id == current_user.id]
            if mine_res:
                if primary_mine_reservation and d.id == primary_mine_reservation.desk_id:
                    status = "mine"
                    active_res = primary_mine_reservation
                else:
                    status = "occupied"
                    active_res = sorted(mine_res, key=lambda r: (r.start_time, r.created_at))[0]
            else:
                status = "occupied"
                active_res = sorted(res_for_desk, key=lambda r: (r.start_time, r.created_at))[0]

            booking_user = db.query(User).filter(User.id == active_res.user_id).first()
            booked_by_name = booking_user.name if booking_user else None
            booked_by_email = booking_user.email if booking_user else None
            booked_from = active_res.start_time
            booked_to = active_res.end_time

        result.append(
            AvailabilityDesk(
                id=d.id,
                name=d.name,
                position_x=d.position_x,
                position_y=d.position_y,
                room=d.room,
                rotation_deg=by_desk_id.get(d.id, 0),
                status=status,
                booked_by_name=booked_by_name,
                booked_by_email=booked_by_email,
                booked_from=booked_from,
                booked_to=booked_to,
            )
        )
    return result

