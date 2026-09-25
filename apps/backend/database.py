
## `database.py` — Async engine & session setup

## Usage example in a route

from fastapi import APIRouter
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from apps.backend.deps import DBSession
from models import DemandPost, DemandStatus

router = APIRouter()


@router.get("/demands")
async def list_open_demands(db: DBSession):
    stmt = (
        select(DemandPost)
        .where(DemandPost.status == DemandStatus.OPEN)
        .options(selectinload(DemandPost.offers))
        .order_by(DemandPost.created_at.desc())
        .limit(50)
    )
    result = await db.execute(stmt)
    return result.scalars().all()

## Key design decisions
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

DATABASE_URL = "postgresql+asyncpg://user:password@localhost:5432/mydb"

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
