from fastapi import FastAPI
from .routers import demands

app = FastAPI(
    title="Korea-China Cross-Border Shopping Platform API",
    version="0.1.0",
)

# 挂载路由模块
app.include_router(demands.router, prefix="/api/v1")

@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy", "service": "backend-api"}