from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.database import get_db

# AsyncSession을 FastAPI Dependency로 사용하는 타입 별칭
DBSession = Annotated[AsyncSession, Depends(get_db)]

