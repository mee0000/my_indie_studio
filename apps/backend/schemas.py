from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict
from apps.backend.models import DemandStatus


class DemandPostBase(BaseModel):
    title: str
    category: str
    target_price_krw: int
    description: Optional[str] = None


class DemandPostCreate(DemandPostBase):
    pass


class DemandPostResponse(DemandPostBase):
    id: int
    user_id: int
    status: DemandStatus
    created_at: datetime

    # Pydantic v2 ORM Mode 설정
    model_config = ConfigDict(from_attributes=True)