from fastapi import APIRouter, HTTPException, Depends, status
from database import get_db
from datetime import datetime

router = APIRouter(
    prefix="/auth",
    tags=["users"]
)
