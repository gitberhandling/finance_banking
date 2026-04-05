"""Tests for financial records endpoints."""
import pytest
from httpx import AsyncClient

SAMPLE_RECORD = {
    "amount": "250.00",
    "type": "income",
    "category": "Salary",
    "date": "2026-01-15",
    "notes": "January salary",
}


@pytest.mark.asyncio
async def test_create_record(client: AsyncClient, admin_headers: dict):
    """POST /records should create a record and return 201."""
    resp = await client.post("/api/v1/records/", json=SAMPLE_RECORD, headers=admin_headers)
    assert resp.status_code == 201
    body = resp.json()
    assert body["category"] == "Salary"
    assert body["type"] == "income"
    assert "id" in body


@pytest.mark.asyncio
async def test_list_records(client: AsyncClient, admin_headers: dict):
    """GET /records should return a list of records."""
    await client.post("/api/v1/records/", json=SAMPLE_RECORD, headers=admin_headers)
    resp = await client.get("/api/v1/records/", headers=admin_headers)
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)
    assert len(resp.json()) >= 1


@pytest.mark.asyncio
async def test_get_single_record(client: AsyncClient, admin_headers: dict):
    """GET /records/{id} should return the record."""
    created = (
        await client.post("/api/v1/records/", json=SAMPLE_RECORD, headers=admin_headers)
    ).json()
    resp = await client.get(f"/api/v1/records/{created['id']}", headers=admin_headers)
    assert resp.status_code == 200
    assert resp.json()["id"] == created["id"]


@pytest.mark.asyncio
async def test_update_record(client: AsyncClient, admin_headers: dict):
    """PATCH /records/{id} should update the record."""
    created = (
        await client.post("/api/v1/records/", json=SAMPLE_RECORD, headers=admin_headers)
    ).json()
    resp = await client.patch(
        f"/api/v1/records/{created['id']}",
        json={"amount": "300.00", "notes": "Updated"},
        headers=admin_headers,
    )
    assert resp.status_code == 200
    assert resp.json()["notes"] == "Updated"


@pytest.mark.asyncio
async def test_delete_record(client: AsyncClient, admin_headers: dict):
    """DELETE /records/{id} should return 204."""
    created = (
        await client.post("/api/v1/records/", json=SAMPLE_RECORD, headers=admin_headers)
    ).json()
    resp = await client.delete(f"/api/v1/records/{created['id']}", headers=admin_headers)
    assert resp.status_code == 204


@pytest.mark.asyncio
async def test_get_deleted_record_returns_404(client: AsyncClient, admin_headers: dict):
    """After deletion, GET should return 404."""
    created = (
        await client.post("/api/v1/records/", json=SAMPLE_RECORD, headers=admin_headers)
    ).json()
    await client.delete(f"/api/v1/records/{created['id']}", headers=admin_headers)
    resp = await client.get(f"/api/v1/records/{created['id']}", headers=admin_headers)
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_filter_records_by_type(client: AsyncClient, admin_headers: dict):
    """GET /records?type=income should only return income records."""
    await client.post("/api/v1/records/", json=SAMPLE_RECORD, headers=admin_headers)
    await client.post(
        "/api/v1/records/",
        json={**SAMPLE_RECORD, "type": "expense", "category": "Food"},
        headers=admin_headers,
    )
    resp = await client.get("/api/v1/records/?type=income", headers=admin_headers)
    assert resp.status_code == 200
    for record in resp.json():
        assert record["type"] == "income"


@pytest.mark.asyncio
async def test_summary_net_balance(client: AsyncClient, admin_headers: dict):
    """GET /summary/net-balance should return income minus expense."""
    await client.post(
        "/api/v1/records/",
        json={**SAMPLE_RECORD, "amount": "1000.00", "type": "income"},
        headers=admin_headers,
    )
    await client.post(
        "/api/v1/records/",
        json={**SAMPLE_RECORD, "amount": "400.00", "type": "expense"},
        headers=admin_headers,
    )
    resp = await client.get("/api/v1/summary/net-balance", headers=admin_headers)
    assert resp.status_code == 200
    # net = 1000 - 400 = 600
    assert float(resp.json()["total"]) == pytest.approx(600.0)
