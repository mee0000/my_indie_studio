from datetime import datetime
from decimal import Decimal
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, EmailStr
from .models import UserRole, DemandStatus, OfferStatus

# --- User Schemas ---
class UserBase(BaseModel):
    email: EmailStr
    role: UserRole = UserRole.USER

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

# --- DemandPost Schemas ---
class DemandPostCreate(BaseModel):
    title: str
    category: str
    target_price_krw: Decimal
    description: Optional[str] = None

class DemandPostResponse(BaseModel):
    id: int
    user_id: int
    title: str
    category: str
    target_price_krw: Decimal
    status: DemandStatus
    description: Optional[str]
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

# --- Offer Schemas ---
class OfferCreate(BaseModel):
    offered_price_rmb: Decimal

class OfferResponse(BaseModel):
    id: int
    demand_id: int
    buyer_id: int
    offered_price_rmb: Decimal
    status: OfferStatus
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)