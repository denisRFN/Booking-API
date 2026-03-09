from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.models.desk import Desk
from app.models.reservation import Reservation
from app.models.user import User
from app.schemas.reservation import ReservationCreate


def ensure_no_overlap(db: Session, desk_id: int, start_time: datetime, end_time: datetime) -> None:
    if start_time >= end_time:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="start_time must be before end_time")

    conflict = (
        db.query(Reservation)
        .filter(
            Reservation.desk_id == desk_id,
            and_(Reservation.start_time < end_time, Reservation.end_time > start_time),
        )
        .first()
    )
    if conflict:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Desk already reserved in this time interval",
        )


def create_reservation(db: Session, *, current_user: User, reservation_in: ReservationCreate) -> Reservation:
    desk = db.query(Desk).filter(Desk.id == reservation_in.desk_id).first()
    if not desk:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Desk not found")

    ensure_no_overlap(db, reservation_in.desk_id, reservation_in.start_time, reservation_in.end_time)

    reservation = Reservation(
        user_id=current_user.id,
        desk_id=reservation_in.desk_id,
        start_time=reservation_in.start_time,
        end_time=reservation_in.end_time,
    )
    db.add(reservation)
    db.commit()
    db.refresh(reservation)
    return reservation


def delete_reservation(db: Session, *, reservation_id: int, current_user: User, as_admin: bool = False) -> None:
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not reservation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reservation not found")

    if not as_admin and reservation.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can cancel only your own reservations",
        )

    db.delete(reservation)
    db.commit()

