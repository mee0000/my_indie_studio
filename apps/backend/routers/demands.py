from typing import List
from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from apps.backend.deps import DBSession
from apps.backend.models import DemandPost, DemandStatus
from apps.backend.schemas import DemandPostCreate, DemandPostResponse

router = APIRouter(prefix="/demands", tags=["Demand Posts"])


@router.get("", response_model=List[DemandPostResponse])
async def list_demands(db: DBSession):
    """需求贴列表查询"""
    result = await db.execute(
        select(DemandPost).order_by(DemandPost.created_at.desc())
    )
    return result.scalars().all()


@router.get("/{demand_id}", response_model=DemandPostResponse)
async def get_demand(demand_id: int, db: DBSession):
    """需求贴单条详情查询"""
    result = await db.execute(
        select(DemandPost).where(DemandPost.id == demand_id)
    )
    demand = result.scalar_one_or_none()
    if not demand:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Demand post not found",
        )
    return demand


@router.post(
    "",
    response_model=DemandPostResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_demand(payload: DemandPostCreate, db: DBSession):
    """发布新的代购/Popup求购需求 ( MVP 阶段指定 mock user_id=1 )"""
    new_demand = DemandPost(
        user_id=1,  # Mock user ID
        title=payload.title,
        category=payload.category,
        target_price_krw=payload.target_price_krw,
        description=payload.description,
        status=DemandStatus.OPEN,
    )
    db.add(new_demand)
    await db.commit()
    await db.refresh(new_demand)
    return new_demand