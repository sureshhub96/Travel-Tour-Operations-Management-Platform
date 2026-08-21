import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app


# ==================================================
# TEST DATABASE
# ==================================================

TEST_DATABASE_URL = "sqlite:///./test_travel.db"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={
        "check_same_thread": False
    }
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# ==================================================
# CREATE TEST DATABASE
# ==================================================

@pytest.fixture(scope="session", autouse=True)
def create_test_database():

    Base.metadata.create_all(
        bind=engine
    )

    yield

    Base.metadata.drop_all(
        bind=engine
    )


# ==================================================
# DATABASE SESSION
# ==================================================

@pytest.fixture
def db():

    session = TestingSessionLocal()

    try:
        yield session
    finally:
        session.close()


# ==================================================
# OVERRIDE DATABASE
# ==================================================

def override_get_db():

    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[
    get_db
] = override_get_db


# ==================================================
# TEST CLIENT
# ==================================================

@pytest.fixture
def client():

    return TestClient(app)