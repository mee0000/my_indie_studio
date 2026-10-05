from typing import List

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.deps import DBSession
from apps.backend.models import DemandPost, DemandStatus, User, UserRole
from apps.backend.schemas import DemandPostCreate, DemandPostResponse

router = APIRouter(prefix="/demands", tags=["Demand Posts"])

MOCK_USER_ID = 1
MOCK_USER_EMAIL = "mock-user-1@example.com"


async def _mock_user_exists(db: AsyncSession) -> bool:
    result = await db.execute(select(User.id).where(User.id == MOCK_USER_ID))
    return result.scalar_one_or_none() is not None


async def _next_demand_id(db: AsyncSession) -> int:
    # SQLite 把 BigInteger 主键建成 BIGINT，不会自增，未指定 id 时会 NOT NULL 失败。
    result = await db.execute(select(func.coalesce(func.max(DemandPost.id), 0) + 1))
    return int(result.scalar_one())


async def ensure_mock_user(db: AsyncSession) -> None:
    """MVP 阶段没有登录，发布需求固定挂在 id=1。缺用户时补一条开发用户，避免外键 500。"""
    if await _mock_user_exists(db):
        return

    db.add(
        User(
            id=MOCK_USER_ID,
            email=MOCK_USER_EMAIL,
            hashed_password="mock-not-for-login",
            role=UserRole.USER,
        )
    )
    try:
        await db.flush()
    except IntegrityError:
        await db.rollback()
        if not await _mock_user_exists(db):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Mock user (id=1) is unavailable",
            )


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
    await ensure_mock_user(db)
    new_demand = DemandPost(
        id=await _next_demand_id(db),
        user_id=MOCK_USER_ID,
        title=payload.title,
        category=payload.category,
        target_price_krw=payload.target_price_krw,
        description=payload.description,
        status=DemandStatus.OPEN,
    )
    db.add(new_demand)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Mock user (id=1) is unavailable",
        )
    await db.refresh(new_demand)
    return new_demand
