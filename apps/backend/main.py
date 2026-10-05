from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from apps.backend.database import engine, Base
from apps.backend.routers import demands


# 앱 시작 시 DB 테이블(demand_posts 등) 자동 생성
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    title="Korea-China Cross-Border Shopping Platform API",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API 라우터 등록
app.include_router(demands.router, prefix="/api/v1")


@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy", "service": "backend-api"}