from fastapi import FastAPI
from config import engine, Base
import models
from routes.user import router as user_router
from routes.book import router as book_router

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(user_router)
app.include_router(book_router)
