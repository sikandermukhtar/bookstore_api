from utils.smtp_config import mail_config
from fastapi import (
    APIRouter,
    HTTPException,
    Depends,
    Response,
    status,
    UploadFile,
    File,
    Form,
    BackgroundTasks,
)
from fastapi_mail import FastMail, MessageSchema, MessageType
from database import get_db
from models import User, VerificationToken
from pydantic import EmailStr
from sqlalchemy.orm import Session
from utils.hashing import hash, authenticate_user
from utils.token import create_access_token, generate_secret_token
from datetime import datetime, timezone, timedelta
from schemas.user import UserRead, UserLogin, UserLoginSuccess
from utils.imagekit import upload_profile_img
from sqlalchemy.exc import IntegrityError

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/register", response_model=UserRead)
async def register_user(
    background_tasks: BackgroundTasks,
    email: str = Form(...),
    password: str = Form(...),
    profile_img: UploadFile = File(None),
    db: Session = Depends(get_db),
):
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already in use."
        )
    hashed_password = hash(password)
    if profile_img is not None:
        img_url = await upload_profile_img(profile_img)
    new_user = User(email=email, password=hashed_password, profile_img_url=img_url)
    db.add(new_user)
    db.flush()
    verification_token = generate_secret_token()
    new_token = VerificationToken(
        token=verification_token,
        user_id=new_user.id,
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=15),
    )
    db.add(new_token)

    message = MessageSchema(
        subject="Prime Bookstore Verification",
        recipients=[new_user.email],
        body=f"Follow the following link for verification:\n"
        + f"http://localhost:8000/auth/verify?token={verification_token}",
        subtype=MessageType.html,
    )

    fm = FastMail(mail_config)

    try:
        db.commit()
        db.refresh(new_user)
        db.refresh(new_token)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Intgerity error occured."
        )

    background_tasks.add_task(fm.send_message, message)
    return new_user


@router.post("/login", response_model=UserLoginSuccess)
def login_user(
    user_login: UserLogin, response: Response, db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == user_login.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Wrong credentials"
        )

    authenticated, new_hash = authenticate_user(user_login.password, user.password)
    if not authenticated:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong credentials."
        )

    if new_hash:
        user.password = new_hash
        db.add(user)
        db.commit()
        db.refresh(user)
    access_token, max_age = create_access_token(user.email, user.role)
    response.set_cookie(
        key="access_token",
        value=access_token,
        max_age=max_age,
        httponly=True,
        samesite="lax",
        secure=True,
    )

    return {
        "user": user,
        "message": "Successfully Logged In",
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.get("/verify", response_model=dict[str, str])
def verify_user_by_token(token: str, db: Session = Depends(get_db)):
    if not token:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Token not found."
        )

    existing_token = (
        db.query(VerificationToken)
        .filter(
            VerificationToken.token == token,
            VerificationToken.expires_at > datetime.now(timezone.utc),
            VerificationToken.is_used == False,
        )
        .first()
    )

    if not existing_token:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Token not found."
        )

    existing_user = db.query(User).filter(User.id == existing_token.user_id).first()

    if not existing_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found!")

    existing_token.is_used = True
    existing_user.is_verified = True

    db.add(existing_user)
    db.add(existing_token)
    try:
        db.commit()
        db.refresh(existing_user)
        db.refresh(existing_token)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bad request, integrity error.",
        )

    return {"message": "You are successfully verified."}

@router.post("/resend-verification-token", response_model=dict[str, str])
def resend_verification(email: EmailStr, background_tasks: BackgroundTasks, db:Session = Depends(get_db)):

    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found!")
    
    if user.is_verified:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request, already verified.")
    
    existing_token = db.query(VerificationToken).filter(VerificationToken.user_id == user.id).first()
    if existing_token:
        db.delete(existing_token)
        db.flush()

    verification_token = generate_secret_token()
    new_token = VerificationToken(
        token = verification_token,
        user_id= user.id,
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=15),
    )
    message = MessageSchema(
        subject="Prime Bookstore Verification",
        recipients=[email],
        body=f"Follow the following link for verification:\n"
        + f"http://localhost:8000/auth/verify?token={verification_token}",
        subtype=MessageType.html,
    )
    fm=FastMail(mail_config)
    db.add(new_token)
    try:
        db.commit()
        db.refresh(new_token)
        db.refresh(user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Intgerity error occured."
        )

    background_tasks.add_task(fm.send_message, message)
    return {"message": "New token issued."}
