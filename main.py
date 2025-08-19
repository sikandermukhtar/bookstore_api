from fastapi import FastAPI
import models
from routes.auth import router as auth_router
from routes.book import router as book_router
from routes.user import router as user_router
from contextlib import asynccontextmanager
from config.session import AsyncSessionLocal
from sqlalchemy import select
from utils.hashing import hash
from config.session import async_engine, sync_engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with AsyncSessionLocal() as session:
        async with session.begin():
            result = await session.execute(
                select(models.User).filter(models.User.email == "admin@gmail.com")
            )
            user = result.scalar_one_or_none()
            if not user:
                hashed_password = hash("admin123")
                user = models.User(
                    email="admin@gmail.com",
                    password=hashed_password,
                    role="admin",
                    is_verified=True,
                )
                session.add(user)
                await session.commit()
    yield

    await async_engine.dispose()
    sync_engine.dispose()


app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(book_router)
