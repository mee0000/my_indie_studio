from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db

DBSession = Annotated[AsyncSession, Depends(get_db)]

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