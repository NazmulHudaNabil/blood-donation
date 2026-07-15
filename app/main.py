from fastapi import FastAPI

from app.database import Base
from app.database import engine

import app.models

from app.routes.user_routes import router as user_router
from app.routes.auth_routes import router as auth_router
from app.routes.donor_routes import router as donor_router
from app.routes.request_route import router as request_router
from app.routes.location_routes import router as location_router
from app.routes.blood_group_routes import router as blood_group_router

app = FastAPI()

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

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