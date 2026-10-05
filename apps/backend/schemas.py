from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

from apps.backend.models import DemandStatus


class DemandPostBase(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    category: Literal["fashion", "beauty", "popup"]
    target_price_krw: int = Field(gt=0)
    description: Optional[str] = Field(default=None, max_length=2000)

    @field_validator("title", mode="before")
    @classmethod
    def strip_title(cls, value: object) -> object:
        if isinstance(value, str):
            return value.strip()
        return value

    @field_validator("description", mode="before")
    @classmethod
    def blank_description_to_none(cls, value: object) -> object:
        if value is None:
            return None
        if isinstance(value, str):
            stripped = value.strip()
            return stripped or None
        return value


class DemandPostCreate(DemandPostBase):
    pass


class DemandPostResponse(BaseModel):
    title: str
    category: str
    target_price_krw: int
    description: Optional[str] = None
    id: int
    user_id: int
    status: DemandStatus
    created_at: datetime

    # Pydantic v2 ORM Mode 설정
    model_config = ConfigDict(from_attributes=True)
