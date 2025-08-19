from fastapi import Depends, Request, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from models import User
from database import get_db
from .token import decode_token

oauth_scheme = OAuth2PasswordBearer(tokenUrl="")


def get_current_user(
    request: Request, token: str = Depends(oauth_scheme), db: Session = Depends(get_db)
):
    cookie_token = request.cookies.get("access_token")
    if cookie_token:
        token = cookie_token

    payload = decode_token(token)
    email = payload["sub"]
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="No user found!")
    return user


def allowed_role(allowed_role: str):
    async def role_checker(current_user=Depends(get_current_user)):
        if current_user.role != allowed_role:
            raise HTTPException(
                status_code=403, detail="Access forbidden: insufficient permissions"
            )
        return current_user

    return role_checker
