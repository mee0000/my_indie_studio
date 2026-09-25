
from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import List, Optional

from sqlalchemy import (
    BigInteger,
    DateTime,
    Enum as SAEnum,
    ForeignKey,
    Index,
    Numeric,
    String,
    Text,
    func,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)


# ---------------------------------------------------------------------------
# Base
# ---------------------------------------------------------------------------
class Base(DeclarativeBase):
    """Declarative base for all ORM models."""

    # Reusable timestamp columns via mixin below
    pass


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------
class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"
    MODERATOR = "moderator"


class DemandStatus(str, Enum):
    OPEN = "open"
    MATCHED = "matched"
    CLOSED = "closed"
    CANCELLED = "cancelled"


class OfferStatus(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"


# ---------------------------------------------------------------------------
# Timestamp mixin
# ---------------------------------------------------------------------------
class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )


# ---------------------------------------------------------------------------
# User
# ---------------------------------------------------------------------------
class User(TimestampMixin, Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(
        SAEnum(UserRole, name="user_role", native_enum=True),
        default=UserRole.USER,
        server_default=UserRole.USER.value,
        nullable=False,
    )

    # Relationships
    demand_posts: Mapped[List["DemandPost"]] = relationship(
        "DemandPost",
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    offers: Mapped[List["Offer"]] = relationship(
        "Offer",
        back_populates="buyer",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    def __repr__(self) -> str:
        return f"<User id={self.id} email={self.email!r} role={self.role.value}>"


# ---------------------------------------------------------------------------
# DemandPost
# ---------------------------------------------------------------------------
class DemandPost(TimestampMixin, Base):
    __tablename__ = "demand_posts"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    category: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    target_price_krw: Mapped[Decimal] = mapped_column(
        Numeric(14, 2), nullable=False
    )
    status: Mapped[DemandStatus] = mapped_column(
        SAEnum(DemandStatus, name="demand_status", native_enum=True),
        default=DemandStatus.OPEN,
        server_default=DemandStatus.OPEN.value,
        nullable=False,
        index=True,
    )
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="demand_posts")
    offers: Mapped[List["Offer"]] = relationship(
        "Offer",
        back_populates="demand",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    __table_args__ = (
        Index("ix_demand_posts_status_category", "status", "category"),
    )

    def __repr__(self) -> str:
        return (
            f"<DemandPost id={self.id} title={self.title!r} "
            f"status={self.status.value} target_price_krw={self.target_price_krw}>"
        )


# ---------------------------------------------------------------------------
# Offer
# ---------------------------------------------------------------------------
class Offer(TimestampMixin, Base):
    __tablename__ = "offers"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    demand_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("demand_posts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    buyer_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    offered_price_rmb: Mapped[Decimal] = mapped_column(
        Numeric(14, 2), nullable=False
    )
    status: Mapped[OfferStatus] = mapped_column(
        SAEnum(OfferStatus, name="offer_status", native_enum=True),
        default=OfferStatus.PENDING,
        server_default=OfferStatus.PENDING.value,
        nullable=False,
        index=True,
    )

    # Relationships
    demand: Mapped["DemandPost"] = relationship("DemandPost", back_populates="offers")
    buyer: Mapped["User"] = relationship("User", back_populates="offers")

    __table_args__ = (
        Index("ix_offers_demand_status", "demand_id", "status"),
    )

    def __repr__(self) -> str:
        return (
            f"<Offer id={self.id} demand_id={self.demand_id} "
            f"buyer_id={self.buyer_id} offered_price_rmb={self.offered_price_rmb} "
            f"status={self.status.value}>"
        )



## `deps.py` — FastAPI dependency
