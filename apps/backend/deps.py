from typing import AsyncGenerator
from typing_extensions import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.database import AsyncSessionLocal

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session

DBSession = Annotated[AsyncSession, Depends(get_db)]