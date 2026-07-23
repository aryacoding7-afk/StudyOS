from fastapi import FastAPI
from sqlalchemy import text

from app.api.router import api_router
from app.db.session import engine

app = FastAPI(
    title="StudyOS API",
    version="0.1.0",
    description="Backend API for StudyOS",
)

app.include_router(api_router)


@app.get("/")
async def root():
    return {
        "name": "StudyOS API",
        "version": "0.1.0",
        "status": "running",
    }


@app.get("/health")
async def health():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        database = "connected"

    except Exception as e:
        database = str(e)

    return {
        "status": "healthy",
        "database": database,
    }