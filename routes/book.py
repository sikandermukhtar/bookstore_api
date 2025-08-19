from fastapi import APIRouter, HTTPException, Depends, status, Form, UploadFile, File
from database import get_db
from datetime import datetime, date
from schemas.book import BookRead, BookCreate, BookDelete, PaginatedBookList, BookBulkUploadResponse
import uuid
from models import Book, User
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from utils.imagekit import upload_profile_img
from utils.user import allowed_role
from typing import List, Dict, Any
import io
import csv
import math
router = APIRouter(prefix="/books", tags=["books"])
"""
CRUD Endpoints:
○ POST /books → Create a book
○ GET /books/{id} → Get a single book
○ PUT /books/{id} → Update a book
○ DELETE /books/{id} → Delete a book
○ GET /books → List books with pagination and filtering by author/title
"""


@router.post("", response_model=BookRead)
async def create_book(
    title: str = Form(...),
    author: str = Form(...),
    price: float = Form(...),
    published_date: date = Form(...),
    book_cover_image: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(allowed_role("admin")),
):
    cover_image_url = ""
    if book_cover_image:
        cover_image_url = await upload_profile_img(book_cover_image)

    new_book = Book(
        title=title,
        author=author,
        price=price,
        published_date=published_date,
        owner_id=current_user.id,
        book_cover_image=cover_image_url,
    )
    db.add(new_book)

    try:
        db.commit()
        db.refresh(new_book)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Intgerity error occured."
        )

    return new_book


@router.get("/{book_id}", response_model=BookRead)
def get_book_by_id(book_id: uuid.UUID, db: Session = Depends(get_db)):
    existing_book = db.query(Book).filter(Book.id == book_id).first()

    if not existing_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found!"
        )

    return existing_book


@router.patch("/{book_id}", response_model=BookRead)
async def update_book(
    book_id: uuid.UUID,
    title: str | None = Form(None),
    author: str | None = Form(None),
    price: float | None = Form(None),
    published_date: date | None = Form(None),
    book_cover_image: UploadFile | None = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(allowed_role("admin")),
):
    existing_book = db.query(Book).filter(Book.id == book_id).first()
    if not existing_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found!"
        )

    if book_cover_image:
        cover_image_url = await upload_profile_img(book_cover_image)
        if not cover_image_url:
            cover_image_url = existing_book.book_cover_image
        existing_book.book_cover_image = cover_image_url

    if title is not None:
        existing_book.title = title
    if author is not None:
        existing_book.author = author
    if price is not None:
        existing_book.price = price
    if published_date is not None:
        existing_book.published_date = published_date

    db.add(existing_book)
    try:
        db.commit()
        db.refresh(existing_book)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Integrity error occurred."
        )
    return existing_book


@router.delete("/{book_id}", response_model=BookDelete)
def delete_book(
    book_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(allowed_role("admin")),
):
    existing_book = db.query(Book).filter(Book.id == book_id).first()

    if not existing_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found!"
        )

    db.delete(existing_book)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Integrity error occurred."
        )
    return {"book": existing_book, "message": "Book successfully deleted."}


@router.get("", response_model=PaginatedBookList)
def get_paginated_books(
    page: int = 1, per_page: int = 10, db: Session = Depends(get_db)
):
    total_books = db.query(Book).count()

    if total_books == 0:
        return {
            "books": [],
            "next_page": None,
            "prev_page": None,
            "total_pages": 0,
            "total_books": 0,
        }

    if per_page <= 0:
        per_page = 10
    elif per_page > 100:
        per_page = 100

    total_pages: int = math.ceil(total_books / per_page) if total_books else 1

    if page < 1:
        page = 1
    elif page > total_pages:
        page = total_pages

    offset: int = (page - 1) * per_page

    paginated_books = db.query(Book).offset(offset).limit(per_page).all()

    def make_link(p):
        return f"/books?page={p}&per_page={per_page}"

    return {
        "books": paginated_books,
        "next_page": make_link(page + 1) if page < total_pages else None,
        "prev_page": make_link(page - 1) if page > 1 else None,
        "total_pages": total_pages,
        "total_books": total_books,
    }

@router.post("/upload", response_model=BookBulkUploadResponse)
async def upload_books_using_csv(csv_file: UploadFile = File(...), db: Session = Depends(get_db), current_user: User = Depends(allowed_role("admin"))):

    if not csv_file or not csv_file.filename:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to upload file.")

    if not csv_file.filename.lower().endswith(".csv"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only CSV files are allowed."
        )

    content = await csv_file.read()
    csv_data = io.StringIO(content.decode('utf-8'))
    reader = csv.DictReader(csv_data)

    required_fields = {"title", "author", "price", "published_date"}

    missing_fields = required_fields - set(reader.fieldnames or [])
    if missing_fields:
        raise HTTPException(
            status_code=400,
            detail=f"Missing required columns: {', '.join(missing_fields)}"
        )
    
    inserted_count = 0
    skipped_count = 0
    errors: List[Dict[str, Any]] = []

    for i, row in enumerate(reader, start=2):
        try:
            book_data = BookCreate(
                title=row["title"].strip(),
                author=row["author"].strip(),
                price=float(row["price"].strip()),
                book_cover_image=row["book_cover_image"].strip(),
                published_date=datetime.strptime(row["published_date"].strip(), "%Y-%m-%d").date(),
                owner_id=current_user.id
            )

            book = Book(**book_data.model_dump())
            db.add(book)
            inserted_count +=1
        except Exception as e:
            skipped_count += 1
            errors.append({"row": 1, "error": str(e)})

    db.commit()

    return {
        "inserted": inserted_count,
        "skipped": skipped_count,
        "errors": errors
    }