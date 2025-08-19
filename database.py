from config.session import SessionLocal, AsyncSessionLocal


async def get_async_db():
    async with AsyncSessionLocal() as db:
        yield db


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
