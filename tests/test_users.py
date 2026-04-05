"""Tests for user endpoints."""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_me(client: AsyncClient, auth_headers: dict):
    """GET /users/me should return the current user's profile."""
    resp = await client.get("/api/v1/users/me", headers=auth_headers)
    assert resp.status_code == 200
    body = resp.json()
    assert body["email"] == "test@example.com"
    assert "hashed_password" not in body


@pytest.mark.asyncio
async def test_update_own_user(client: AsyncClient, auth_headers: dict):
    """PATCH /users/{id} — user can update their own name."""
    me = (await client.get("/api/v1/users/me", headers=auth_headers)).json()
    resp = await client.patch(
        f"/api/v1/users/{me['id']}",
        json={"name": "Updated Name"},
        headers=auth_headers,
    )
    assert resp.status_code == 200
    assert resp.json()["name"] == "Updated Name"


@pytest.mark.asyncio
async def test_list_users_requires_admin(client: AsyncClient, auth_headers: dict):
    """GET /users/ should be forbidden for non-admin users."""
    resp = await client.get("/api/v1/users/", headers=auth_headers)
    assert resp.status_code == 403


@pytest.mark.asyncio
async def test_list_users_as_admin(client: AsyncClient, admin_headers: dict):
    """GET /users/ should work for admin users."""
    resp = await client.get("/api/v1/users/", headers=admin_headers)
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


@pytest.mark.asyncio
async def test_delete_user_requires_admin(client: AsyncClient, auth_headers: dict):
    """DELETE /users/{id} should be forbidden for non-admin users."""
    me = (await client.get("/api/v1/users/me", headers=auth_headers)).json()
    resp = await client.delete(f"/api/v1/users/{me['id']}", headers=auth_headers)
    assert resp.status_code == 403
