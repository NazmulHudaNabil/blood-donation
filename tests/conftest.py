import os
import tempfile

# Must be set before anything imports app.config (which instantiates Settings
# at module load time), so these need to land before any `from app...` import.
_TEST_DB_FD, _TEST_DB_PATH = tempfile.mkstemp(suffix=".db")
os.close(_TEST_DB_FD)
os.environ.setdefault("DATABASE_URL", f"sqlite:///{_TEST_DB_PATH}")
os.environ.setdefault("SECRET_KEY", "test-secret-key-that-is-at-least-32-characters-long")
os.environ.setdefault("ALGORITHM", "HS256")
os.environ.setdefault("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
os.environ.setdefault("ENVIRONMENT", "test")

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.database import get_db
from app.main import app
from app.rate_limit import limiter

# File-based (not :memory:) SQLite — FastAPI's TestClient runs endpoint code in
# a worker thread, and an in-memory DB with StaticPool doesn't reliably share
# state across that thread boundary the way a real file on disk does.
engine = create_engine(f"sqlite:///{_TEST_DB_PATH}", connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def _override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = _override_get_db


@pytest.fixture(autouse=True)
def _fresh_schema_and_rate_limits():
    """Every test gets an empty schema and a clean rate-limit slate — tests
    shouldn't fail because an earlier test already used up the /auth/login
    quota for the shared TestClient "IP"."""
    Base.metadata.create_all(bind=engine)
    limiter.reset()
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture(scope="session", autouse=True)
def _cleanup_test_db_file():
    yield
    if os.path.exists(_TEST_DB_PATH):
        os.remove(_TEST_DB_PATH)
