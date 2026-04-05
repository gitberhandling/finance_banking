"""Tests for auth endpoints: /auth/register and /auth/login."""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_success(client: AsyncClient):
    """POST /auth/register should return 201 with user_id."""
    resp = await client.post(
        "/api/v1/auth/register",
        json={"name": "Alice", "email": "alice@test.com", "password": "secret123"},
    )
    assert resp.status_code == 201
    body = resp.json()
    assert "user_id" in body
    assert body["message"] == "Registration successful"


@pytest.mark.asyncio
async def test_register_duplicate_email(client: AsyncClient):
    """Registering with an existing email should return 409."""
    payload = {"name": "Bob", "email": "bob@test.com", "password": "secret123"}
    await client.post("/api/v1/auth/register", json=payload)
    resp = await client.post("/api/v1/auth/register", json=payload)
    assert resp.status_code == 409


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient):
    """POST /auth/login with valid credentials should return access_token."""
    await client.post(
        "/api/v1/auth/register",
        json={"name": "Carol", "email": "carol@test.com", "password": "pass1234"},
    )
    resp = await client.post(
        "/api/v1/auth/login",
        json={"email": "carol@test.com", "password": "pass1234"},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert "access_token" in body
    assert body["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_wrong_password(client: AsyncClient):
    """POST /auth/login with wrong password should return 401."""
    await client.post(
        "/api/v1/auth/register",
        json={"name": "Dave", "email": "dave@test.com", "password": "correct"},
    )
    resp = await client.post(
        "/api/v1/auth/login",
        json={"email": "dave@test.com", "password": "wrong"},
    )
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_login_unknown_email(client: AsyncClient):
    """POST /auth/login with unknown email should return 401."""
    resp = await client.post(
        "/api/v1/auth/login",
        json={"email": "nobody@test.com", "password": "anything"},
    )
    assert resp.status_code == 401
