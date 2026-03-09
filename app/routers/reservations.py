from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, get_current_admin
from app.database.session import get_db
from app.models.reservation import Reservation
from app.models.user import User
from app.schemas.reservation import ReservationCreate, ReservationRead, ReservationWithDesk
from app.services.reservations import create_reservation as svc_create_reservation, delete_reservation as svc_delete_reservation


router = APIRouter(prefix="/reservations", tags=["reservations"])


@router.get("", response_model=list[ReservationWithDesk])
def list_reservations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    mine: bool = True,
):
    query = (
        db.query(
            Reservation.id,
            Reservation.user_id,
            Reservation.desk_id,
            Reservation.start_time,
            Reservation.end_time,
            Reservation.created_at,
        )
        .join(Reservation.desk)
    )

    if mine:
        query = query.filter(Reservation.user_id == current_user.id)

    rows = query.order_by(Reservation.start_time.desc()).all()

    # We need desk name and room as well, so query differently
    reservations = (
        db.query(Reservation)
        .join(Reservation.desk)
        .filter(Reservation.user_id == current_user.id if mine else True)
        .order_by(Reservation.start_time.desc())
        .all()
    )

    result: list[ReservationWithDesk] = []
    for r in reservations:
        result.append(
            ReservationWithDesk(
                id=r.id,
                user_id=r.user_id,
                desk_id=r.desk_id,
                desk_name=r.desk.name,
                room=r.desk.room,
                start_time=r.start_time,
                end_time=r.end_time,
                created_at=r.created_at,
            )
        )
    return result


@router.post("", response_model=ReservationRead, status_code=status.HTTP_201_CREATED)
def create_reservation(
    reservation_in: ReservationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    reservation = svc_create_reservation(db, current_user=current_user, reservation_in=reservation_in)
    return reservation


@router.delete("/{reservation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reservation(
    reservation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # admins can cancel any; regular users only theirs
    as_admin = current_user.role == "admin"
    svc_delete_reservation(db, reservation_id=reservation_id, current_user=current_user, as_admin=as_admin)
    return None

