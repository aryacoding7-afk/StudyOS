import logging

from app.core.exception_handlers import register_exception_handlers
from fastapi import FastAPI
from sqlalchemy import text

from app.core.logging import setup_logging

# Configure logging FIRST
setup_logging()

logger = logging.getLogger(__name__)
logger.info("Logging initialized")

from app.api.router import api_router
from app.db.session import engine
from app.utils.model_validator import validate_model


validate_model()

app = FastAPI(
    title="StudyOS API",
    version="0.1.0",
    description="Backend API for StudyOS",
)

register_exception_handlers(app)

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

    except Exception:
        logger.exception("Database health check failed")
        database = "disconnected"

    return {
        "status": "healthy",
        "database": database,
    }