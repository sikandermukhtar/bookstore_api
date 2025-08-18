from fastapi import HTTPException
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

ALGORITHM = os.getenv("ALGORITHM", "HS256")
SECRET_KEY = os.getenv("SECRET_KEY", "PLACEHOLDER_FOR_SECRET_KEY")
TOKEN_EXPIRE_MINUTES = int(os.getenv("TOKEN_EXPIRE_MINUTES", 60))

def create_access_token(email: str, role: str, expires_delta: Optional[timedelta] = None) -> tuple[str, int]:
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=TOKEN_EXPIRE_MINUTES))
    iat = datetime.now(timezone.utc)
    to_encode = {
        "sub": email,
        "role": role,
        "expire": expire,
        "iat": iat 
    }
    max_age = int((expire - datetime.now(timezone.utc)).total_seconds())
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt, max_age

def decode_token(token: str):
    try:
        payload=  jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )