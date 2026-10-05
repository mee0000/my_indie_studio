from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

# SQLite 비동기 연결 (MVP용)
DATABASE_URL = "sqlite+aiosqlite:///./app.db"

engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # SQL 로그 출력 (개발 단계 모니터링용)
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# 👈 여기서 Base 클래스를 정의해 주어야 다른 파일에서 import할 수 있습니다.
class Base(DeclarativeBase):
    pass