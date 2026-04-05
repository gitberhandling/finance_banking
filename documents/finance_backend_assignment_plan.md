# 📦 Finance Backend Project Documents (FastAPI + PostgreSQL + SQLAlchemy + JWT)

---

# 📄 Document 1: Project Architecture & Design

## 🏗️ Tech Stack
- Backend: FastAPI
- Database: PostgreSQL
- ORM: SQLAlchemy
- Authentication: JWT

## 📁 Folder Structure
```
app/
 ├── api/
 ├── core/
 ├── models/
 ├── schemas/
 ├── services/
 ├── db/
 ├── middlewares/
 └── main.py
```

## 🔄 Flow
Client → API → Service Layer → DB Layer → Response

## 🧠 Design Principles
- Separation of concerns
- Scalable modular structure
- Clean API contracts

---

# 📄 Document 2: Database Design (PostgreSQL)

## 👤 Users Table
```sql
id UUID PRIMARY KEY
name VARCHAR
email VARCHAR UNIQUE
password VARCHAR
role VARCHAR
status VARCHAR
created_at TIMESTAMP
```

## 💰 Financial Records Table
```sql
id UUID PRIMARY KEY
user_id UUID REFERENCES users(id)
amount NUMERIC
type VARCHAR
category VARCHAR
date DATE
notes TEXT
created_at TIMESTAMP
```

## 📊 Indexing
- index on user_id
- index on date
- index on category

---

# 📄 Document 3: API Specification

## 🔐 Auth APIs
- POST /auth/register
- POST /auth/login

## 👤 User APIs
- POST /users
- GET /users
- PATCH /users/{id}
- DELETE /users/{id}

## 💰 Records APIs
- POST /records
- GET /records
- GET /records/{id}
- PATCH /records/{id}
- DELETE /records/{id}

## 📊 Summary APIs
- GET /summary/total-income
- GET /summary/total-expense
- GET /summary/net-balance
- GET /summary/category-wise
- GET /summary/monthly-trends

## 🔎 Query Params
- ?start_date=
- ?end_date=
- ?category=
- ?type=

---

# 📄 Document 4: Development Guide & Implementation Plan

## ⚙️ Step 1: Setup
- Create virtual env
- Install dependencies
```
pip install fastapi uvicorn sqlalchemy psycopg2-binary python-jose passlib
```

## ⚙️ Step 2: Database Config
- Setup PostgreSQL
- Configure SQLAlchemy engine

## ⚙️ Step 3: Models & Schemas
- Create SQLAlchemy models
- Create Pydantic schemas

## ⚙️ Step 4: Authentication (JWT)
- Login endpoint
- Token generation
- Password hashing (bcrypt)

## ⚙️ Step 5: Role-Based Access
- Dependency injection in FastAPI
- Role validation

## ⚙️ Step 6: CRUD Implementation
- Users
- Financial Records

## ⚙️ Step 7: Summary APIs
- Aggregations using SQLAlchemy

## ⚙️ Step 8: Validation & Error Handling
- Pydantic validation
- Custom exception handlers

## ⚙️ Step 9: Testing
- Use Postman / Swagger (/docs)

## ⚙️ Step 10: Final Touch
- Clean code
- README
- Optional deployment

---

# 📄 Document 5: Code Quality & Engineering Guidelines

## 🎯 Objective
Ensure the backend is clean, maintainable, scalable, and production-ready in terms of structure and logic.

---

## 🧱 1. Project Structure & Separation of Concerns
- Keep layers independent:
  - **API (routes/controllers)** → handle request/response
  - **Service layer** → business logic
  - **Models (SQLAlchemy)** → DB structure
  - **Schemas (Pydantic)** → validation & serialization
- Never mix DB logic directly inside routes
- Use dependency injection for DB sessions and auth

---

## 🧾 2. Naming Conventions
- Use meaningful names:
  - `create_user`, not `func1`
  - `financial_record_service`, not `frs`
- Follow snake_case for Python variables and functions
- Use PascalCase for classes
- Keep endpoint paths RESTful and consistent

---

## 🔐 3. Security Best Practices
- Hash passwords using bcrypt
- Never store plain text passwords
- Use JWT securely:
  - Short expiry tokens
  - Use refresh tokens (optional)
- Validate all inputs (Pydantic)
- Avoid SQL injection (use ORM only)

---

## ⚙️ 4. Error Handling
- Use centralized exception handling
- Return consistent error format:
```json
{
  "error": "message",
  "status_code": 400
}
```
- Avoid exposing internal errors (no stack traces in response)

---

## 📊 5. Database Best Practices
- Use proper relationships (ForeignKey)
- Add indexes for frequent queries
- Avoid N+1 queries (use joins)
- Use transactions where needed

---

## 🚀 6. API Design Standards
- Follow REST principles
- Use proper HTTP methods:
  - GET → read
  - POST → create
  - PATCH → update
  - DELETE → delete
- Use pagination for large data
- Keep responses consistent

---

## 🧪 7. Testing & Validation
- Validate using Pydantic schemas
- Write unit tests for services
- Test edge cases (empty data, invalid input)

---

## 📈 8. Performance Optimization
- Use async endpoints where needed
- Optimize queries (aggregation at DB level)
- Avoid unnecessary loops in Python

---

## 📚 9. Documentation
- Use FastAPI Swagger (`/docs`)
- Add docstrings to functions
- Maintain clear README

---

## 🧹 10. Clean Code Principles
- Keep functions small and focused
- Avoid duplicate code (DRY)
- Write readable logic over clever tricks
- Add comments only where necessary

---

## 🔥 Pro Tips (To Impress Evaluators)
- Use dependency injection cleanly
- Separate config (env variables)
- Add logging
- Handle edge cases explicitly
- Keep commit history clean (if using GitHub)

---

# 📄 Document 6: Production-Grade FastAPI Boilerplate

## 📁 Structure
```
app/
 ├── api/v1/endpoints/
 │    ├── auth.py
 │    ├── users.py
 │    ├── records.py
 │    └── summary.py
 ├── core/
 │    ├── config.py
 │    ├── security.py
 │    └── logging.py
 ├── db/
 │    ├── base.py
 │    ├── session.py
 ├── models/
 ├── schemas/
 ├── services/
 ├── dependencies/
 └── main.py
```

---

## 🚀 main.py
```python
from fastapi import FastAPI
from app.core.logging import setup_logging

app = FastAPI()
setup_logging()

@app.get("/")
def root():
    return {"message": "API Running"}
```

---

# 📄 Document 7: JWT + Role-Based Access Control

## 🔐 security.py
```python
from jose import jwt
from datetime import datetime, timedelta

SECRET_KEY = "secret"
ALGORITHM = "HS256"


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=60)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
```

## 🔐 dependency
```python
from fastapi import Depends, HTTPException


def role_required(roles: list):
    def wrapper(user=Depends(get_current_user)):
        if user.role not in roles:
            raise HTTPException(status_code=403, detail="Forbidden")
        return user
    return wrapper
```

---

# 📄 Document 8: Logging & Config Management

## ⚙️ config.py
```python
from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str

settings = Settings()
```

## 🪵 logging.py
```python
import logging

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
```

---

# 📄 Document 9: Unit Testing & Test Structure

## 📁 tests/
```
tests/
 ├── test_auth.py
 ├── test_users.py
 ├── test_records.py
```

## 🧪 Example Test
```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
```

## 🧪 Run Tests
```
pytest
```

---

# ✅ Final Notes
- This setup is production-ready structure
- Focus on clean services + dependency injection
- Add more layers only if needed

