# Finance Backend API

A production-grade **FastAPI + PostgreSQL + SQLAlchemy (async) + JWT** backend for managing personal financial records.

---

## ⚙️ Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI |
| Database | PostgreSQL (asyncpg) |
| ORM | SQLAlchemy 2.0 (async) |
| Auth | JWT via python-jose + bcrypt |
| Config | pydantic-settings (.env) |
| Testing | pytest-asyncio + httpx + SQLite in-memory |

---

## 📁 Project Structure

```
app/
├── api/
│   ├── dependencies.py          # get_current_user, require_role
│   └── v1/
│       ├── router.py
│       └── endpoints/
│           ├── auth.py          # POST /auth/register, /auth/login
│           ├── users.py         # CRUD /users
│           ├── records.py       # CRUD /records
│           └── summary.py       # GET /summary/*
├── core/
│   ├── config.py                # Settings (pydantic-settings)
│   ├── database.py              # Async engine + get_db
│   ├── security.py              # JWT + bcrypt helpers
│   └── logging.py
├── models/
│   ├── user.py
│   └── financial_record.py
├── repositories/
│   ├── base_repository.py
│   ├── user_repository.py
│   └── record_repository.py
├── schemas/
│   ├── user.py
│   ├── auth.py
│   ├── financial_record.py
│   └── summary.py
├── services/
│   ├── auth_service.py
│   ├── user_service.py
│   ├── record_service.py
│   └── summary_service.py
└── main.py
tests/
├── conftest.py
├── test_auth.py
├── test_users.py
└── test_records.py
```

---

## 🚀 Quick Start

### 1. Clone & create virtual environment

```bash
cd Zoryny
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment

```bash
cp .env.example .env
# Edit .env — set DATABASE_URL and SECRET_KEY
```

### 4. Set up the database

Make sure PostgreSQL is running, then create the database:

```sql
CREATE DATABASE finance_db;
```

Run Alembic migrations *(or use `alembic revision --autogenerate` for initial)*:

> For a quick start without Alembic, you can auto-create tables by adding
> `await conn.run_sync(Base.metadata.create_all)` in the lifespan startup.

### 5. Run the server

```bash
uvicorn app.main:app --reload
```

Open **http://127.0.0.1:8000/docs** for interactive Swagger UI.

---

## 🔌 API Endpoints

### Auth
| Method | Path | Description |
|---|---|---|
| POST | `/api/v1/auth/register` | Register a new user |
| POST | `/api/v1/auth/login` | Login → get JWT token |

### Users *(requires auth)*
| Method | Path | Auth |
|---|---|---|
| POST | `/api/v1/users/` | Admin only |
| GET | `/api/v1/users/` | Admin only |
| GET | `/api/v1/users/me` | Any user |
| PATCH | `/api/v1/users/{id}` | Self or admin |
| DELETE | `/api/v1/users/{id}` | Admin only |

### Records *(requires auth)*
| Method | Path | Query Params |
|---|---|---|
| POST | `/api/v1/records/` | — |
| GET | `/api/v1/records/` | `?start_date` `?end_date` `?category` `?type` |
| GET | `/api/v1/records/{id}` | — |
| PATCH | `/api/v1/records/{id}` | — |
| DELETE | `/api/v1/records/{id}` | — |

### Summary *(requires auth)*
| Method | Path | Query Params |
|---|---|---|
| GET | `/api/v1/summary/total-income` | `?start_date` `?end_date` |
| GET | `/api/v1/summary/total-expense` | `?start_date` `?end_date` |
| GET | `/api/v1/summary/net-balance` | `?start_date` `?end_date` |
| GET | `/api/v1/summary/category-wise` | `?start_date` `?end_date` |
| GET | `/api/v1/summary/monthly-trends` | — |

---

## 🧪 Running Tests

Tests use SQLite in-memory — **no PostgreSQL required**:

```bash
pytest tests/ -v
```

---

## 🔐 Authentication Flow

1. `POST /api/v1/auth/register` — create account
2. `POST /api/v1/auth/login` — receive Bearer token
3. Add `Authorization: Bearer <token>` header to all protected routes
4. In Swagger UI → click **Authorize** button → paste token

---

## 🛡️ Security Notes

- Passwords hashed with **bcrypt** via passlib
- Tokens signed with **HS256 JWT**
- Store `SECRET_KEY` as a long random string in production
- Never commit `.env` to version control

---

## 📝 Assumptions & Tradeoffs (Assignment Notes)

As requested by the assignment, here are the key assumptions and tradeoffs made:

1. **Role-Based Multi-tenant Access:**
   The exact role behavior was left open. I chose a multi-tenant personal-record approach combined with hierarchical global roles:
   - `viewer` (Default upon registration): Read-only access to their own analytics dashboard.
   - `analyst`: Extends viewer with access to raw data (`GET /records`).
   - `admin`: Can create, update, and delete their own records, and has full CRUD over all users.
   *Tradeoff*: Instead of a single shared ledger where admins manage everyone's records, I assumed a personal finance dashboard where users own their data and roles dictate what they can do with it. This limits blast radius and provides strict isolation.

2. **Soft Deletes:**
   Instead of permanently removing financial records (`DELETE`), the endpoint hides them via an `is_deleted = True` flag. This satisfies compliance and audit-trail requirements typical in finance applications.

3. **In-Memory SQLite for Tests:**
   *Tradeoff*: For the sake of easy evaluation without Docker overhead, `conftest.py` spins up an async in-memory SQLite DB. This ensures tests are lightning fast and run completely isolated without requiring a local Postgres server.

4. **Database-Level Aggregation for Summaries:**
   Instead of pulling all records into Python memory to calculate the net-balance or trends, all dashboard analytics use exact SQLAlchemy formulas (e.g., `func.coalesce(func.sum)`). This optimizes performance.
