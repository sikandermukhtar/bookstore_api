from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime, date
from uuid import UUID


class BookRead(BaseModel):
    id: UUID
    title: str
    author: str
    price: float
    book_cover_image: Optional[str] = None
    published_date: date
    created_at: datetime
    updated_at: datetime
    owner_id: Optional[UUID] = None


class BookCreate(BaseModel):
    title: str = Field(..., max_length=120)
    author: str = Field(..., max_length=80)
    price: float = Field(..., gt=0)
    book_cover_image: Optional[str] = None
    published_date: date = Field(...)
    owner_id: UUID = Field(...)

    @field_validator("title", "author")
    def not_empty(cls, v):
        if not v.strip():
            raise ValueError("Field cannot be empty")
        return v
    
    @field_validator("published_date")
    def valid_date(cls, v):
        if not v:
            raise ValueError("Published date cannot be empty")
        return v


class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    price: Optional[float] = None
    book_cover_image: Optional[str] = None
    published_date: Optional[date] = None


class BookDelete(BaseModel):
    book: BookRead
    message: str


class PaginatedBookList(BaseModel):
    books: List[BookRead]
    next_page: Optional[str] = None
    prev_page: Optional[str] = None
    total_pages: int
    total_books: int

class UploadError(BaseModel):
    row: int
    error: str

class BookBulkUploadResponse(BaseModel):
    inserted: int
    skipped: int
    errors: List[UploadError] = []