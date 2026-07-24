import pytest

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.db.base import Base
from app.db.session import get_db
from app.main import app

from tests.database import (
    engine,
    TestingSessionLocal,
)


# -------------------------------------------------------------------
# Create tables once for the whole test session
# -------------------------------------------------------------------

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)

    yield

    Base.metadata.drop_all(bind=engine)


# -------------------------------------------------------------------
# Fresh database session for every test
# -------------------------------------------------------------------

@pytest.fixture()
def db():
    session = TestingSessionLocal()

    try:
        yield session
    finally:
        session.rollback()
        session.close()


# -------------------------------------------------------------------
# Override FastAPI dependency
# -------------------------------------------------------------------

@pytest.fixture()
def client(db: Session):
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()