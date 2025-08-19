from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


load_dotenv()

SYNC_DATABASE_URL = os.getenv("SYNC_DATABASE_URL")
ASYNC_DATABASE_URL = os.getenv("ASYNC_DATABASE_URL")

if SYNC_DATABASE_URL is None:
    SYNC_DATABASE_URL = "sqlite+pysqlite:///./blog_platform_api.db"
    sync_engine = create_engine(
        SYNC_DATABASE_URL, connect_args={"check_same_thread": False}
    )
else:
    sync_engine = create_engine(SYNC_DATABASE_URL, pool_size=5)

SessionLocal = sessionmaker(bind=sync_engine, autoflush=False, expire_on_commit=False)
if ASYNC_DATABASE_URL is None:
    ASYNC_DATABASE_URL = "sqlite+aiosqlite:///./blog_platform_api.db"
    async_engine = create_async_engine(
        ASYNC_DATABASE_URL, connect_args={"check_same_thread": False}
    )
else:
    async_engine = create_async_engine(ASYNC_DATABASE_URL)

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine, autoflush=False, expire_on_commit=False
)
