from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.models.reservation import Reservation
from app.schemas.reservation_schema import ReservationCreate

router = APIRouter(prefix="/reservations", tags=["reservations"])


@router.post("/reservations")
def create_reservation(
    data: ReservationCreate,
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    conflict = db.query(Reservation).filter(
        Reservation.desk_id == data.desk_id,
        Reservation.date == data.date,
        Reservation.start_time < data.end_time,
        Reservation.end_time > data.start_time
    ).first()

    if conflict:

        raise HTTPException(
            status_code=409,
            detail="Desk already reserved for this time"
        )

    reservation = Reservation(
    desk_id=data.desk_id,
    user_id=user["user_id"],
    date=data.date,
    start_time=data.start_time,
    end_time=data.end_time
)

    db.add(reservation)

    db.commit()

    db.refresh(reservation)

    return reservation
