from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import (
    admin,
    auth,
    users,
    services,
    staff, 
    availability,
    reviews,
    appointments
)
from app.api.v1.salons import router as salon_router
from app.core.config import settings


app = FastAPI(
    title="Glōvia API",
    description="Salon booking platform API",
    version="1.0.0",
)


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.CORS_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Authentication
app.include_router(
    auth.router,
    prefix="/api/v1/auth",
    tags=["Authentication"],
)


# Admin
app.include_router(
    admin.router,
    prefix="/api/v1/admin",
    tags=["Admin"],
)


# Salon
app.include_router(
    salon_router,
    prefix="/api/v1/salon",
    tags=["Salon Management"],
)

# Services
app.include_router(
    services.router,
    prefix="/api/v1/salon",
    tags=["Salon Services"],
)

# Staff
app.include_router(
    staff.router,
    prefix="/salons/{salon_id}/staff",
    tags=["Salon Staff"],
)

# Reviews
app.include_router(
    reviews.router,
    prefix="/reviews",
    tags=["Reviews"],
)

# Availabily
app.include_router(
    availability.router,
    prefix="/availability",
    tags=["Salon Availability"],
)

# Appointment
app.include_router(
    appointments.router,
    prefix="/appointments",
    tags=["Appointments"],
)

# Users
app.include_router(
    users.router,
    prefix="/api/v1/users",
    tags=["Users"],
)


@app.get("/")
async def root():
    return {
        "message": "Glōvia API is running"
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy"
    }