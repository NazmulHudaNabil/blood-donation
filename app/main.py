import logging

from fastapi import FastAPI
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from app.config import settings
from app.database import SessionLocal
from app.rate_limit import limiter

import app.models

from app.routes.user_routes import router as user_router
from app.routes.auth_routes import router as auth_router
from app.routes.donor_routes import router as donor_router
from app.routes.request_route import router as request_router
from app.routes.location_routes import router as location_router
from app.routes.blood_group_routes import router as blood_group_router

logger = logging.getLogger("app")

app = FastAPI()

app.state.limiter = limiter


@app.exception_handler(RateLimitExceeded)
def handle_rate_limit_exceeded(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Too many attempts — please wait a moment and try again."},
    )


app.add_middleware(SlowAPIMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(IntegrityError)
def handle_integrity_error(request: Request, exc: IntegrityError):
    logger.warning("Integrity error on %s %s: %s", request.method, request.url.path, exc)
    return JSONResponse(
        status_code=400,
        content={"detail": "That value conflicts with an existing record (duplicate email/phone?)."},
    )


@app.exception_handler(Exception)
def handle_unexpected_error(request: Request, exc: Exception):
    logger.exception("Unhandled error on %s %s", request.method, request.url.path)
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


app.include_router(auth_router)
app.include_router(user_router)
app.include_router(donor_router)
app.include_router(request_router)
app.include_router(location_router)
app.include_router(blood_group_router)

@app.get("/")
def home():
    return {
        "message": "Blood Donation Backend Running"
    }


@app.get("/health")
def health():
    try:
        db = SessionLocal()
        try:
            db.execute(text("SELECT 1"))
        finally:
            db.close()
        return {"status": "ok", "database": "ok"}
    except Exception as exc:
        logger.exception("Health check DB connectivity failure")
        return JSONResponse(status_code=503, content={"status": "error", "database": str(exc)})