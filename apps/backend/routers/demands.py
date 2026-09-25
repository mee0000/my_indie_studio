from typing import List
from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select
from ..deps import DBSession
from ..models import DemandPost, DemandStatus
from ..schemas import DemandPostCreate, DemandPostResponse

router = APIRouter(prefix="/demands", tags=["Demand Posts"])

@router.get("", response_model=List[DemandPostResponse])
async def list_demands(db: DBSession, category: str = None):
    """获取求购需求列表（可按 category 筛选）"""
    stmt = select(DemandPost).where(DemandPost.status == DemandStatus.OPEN)
    if category:
        stmt = stmt.where(DemandPost.category == category)
    stmt = stmt.order_by(DemandPost.created_at.desc())
    
    result = await db.execute(stmt)
    return result.scalars().all()

@router.post("", response_model=DemandPostResponse, status_code=status.HTTP_201_CREATED)
async def create_demand(payload: DemandPostCreate, db: DBSession):
    """发布新的代购/Popup求购需求 ( MVP 阶段指定 mock user_id=1 )"""
    new_demand = DemandPost(
        user_id=1,  # JWT 鉴权完善前先 Mock 当前用户 ID
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