"""FastAPI application entry point."""
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import get_settings
from app.core.logging import setup_logging
from app.api.v1.router import api_router

settings = get_settings()
setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: startup and shutdown events."""
    # On startup — tables are created via Alembic migrations in production.
    # For development convenience, you can run: alembic upgrade head
    yield
    # Cleanup if needed


app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description=(
        "Finance Backend API — manage users, financial records, "
        "and analytics with JWT-based auth and role-based access."
    ),
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

# ── CORS ──────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(api_router, prefix=settings.API_V1_STR)


# ── Global exception handler ──────────────────────────────────────────────────
@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    """Return a clean JSON error for any unhandled exception."""
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "status_code": 500},
    )


@app.get("/", tags=["Health"])
async def root():
    """Health-check endpoint."""
    return {"message": "Finance Backend API is running 🚀", "version": "1.0.0"}


@app.get("/health", tags=["Health"])
async def health():
    """Detailed health status."""
    return {"status": "ok", "api_version": "1.0.0"}
