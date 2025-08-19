from fastapi import (
    APIRouter,
    HTTPException,
    Depends,
    status
)
from database import get_db
from sqlalchemy.orm import Session
from models import User
from schemas.user import UserRead, UserDelete, UserUpdate
from sqlalchemy.exc import IntegrityError
from utils.user import allowed_role
from uuid import UUID

router = APIRouter(prefix="/users", tags=["users"])


@router.patch("/{user_id}", response_model=UserRead)
def update_user(
    user_id: UUID,
    user: UserUpdate,
    current_user: User = Depends(allowed_role("admin")),
    db: Session = Depends(get_db),
):
    existing_user = db.query(User).filter(User.id == user_id).first()

    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User couldn't be found."
        )

    if not user.role:
        user.role = "user"

    existing_user.role = user.role

    db.add(existing_user)
    try:
        db.commit()
        db.refresh(existing_user)
        return existing_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Integrity error occured."
        )


@router.delete("/{user_id}", response_model=UserDelete)
def delete_user(
    user_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(allowed_role("admin")),
):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    db.delete(user)
    db.refresh(user)

    return {"user": user, "message": "User successfully deleted."}
