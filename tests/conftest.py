"""Pytest configuration: async test fixtures using SQLite in-memory."""
import asyncio
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.main import app
from app.core.database import Base, get_db

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="session")
def event_loop():
    """Use a single event loop for the whole test session."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def db_session():
    """Create a fresh in-memory SQLite DB for each test."""
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with session_factory() as session:
        yield session
        await session.rollback()

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def client(db_session: AsyncSession):
    """HTTP test client wired to the in-memory DB session."""

    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c
    app.dependency_overrides.clear()


@pytest_asyncio.fixture(scope="function")
async def auth_headers(client: AsyncClient):
    """Register + login a regular user and return Bearer headers."""
    await client.post(
        "/api/v1/auth/register",
        json={"name": "Test User", "email": "test@example.com", "password": "password123"},
    )
    resp = await client.post(
        "/api/v1/auth/login",
        json={"email": "test@example.com", "password": "password123"},
    )
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest_asyncio.fixture(scope="function")
async def admin_headers(client: AsyncClient, db_session: AsyncSession):
    """Register + login an admin user and return Bearer headers."""
    from app.core.security import get_password_hash
    from app.models.user import User
    import uuid

    admin = User(
        id=uuid.uuid4(),
        name="Admin",
        email="admin@example.com",
        hashed_password=get_password_hash("adminpass"),
        role="admin",
        status="active",
    )
    db_session.add(admin)
    await db_session.flush()

    resp = await client.post(
        "/api/v1/auth/login",
        json={"email": "admin@example.com", "password": "adminpass"},
    )
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
