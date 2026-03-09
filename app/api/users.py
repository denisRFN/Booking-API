from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me")
def get_me(
    user_data=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(User.id == user_data["user_id"]).first()

    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role
    }
