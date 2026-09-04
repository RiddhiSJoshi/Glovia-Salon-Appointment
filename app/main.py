
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
    appointments,
)
from app.api.v1.salons import router as salon_router
from app.core.config import settings


app = FastAPI(
    title="Glōvia API",
    description="""
# Glōvia Salon Booking Platform API

Glōvia is a salon booking platform that allows customers to discover salons,
view services, select stylists, check availability, and manage appointments.

The platform provides APIs for:

- **Authentication** – Registration, login, logout and token management
- **Users** – Customer profile management
- **Salons** – Salon profile and salon management
- **Services** – Salon services, pricing and duration
- **Staff** – Stylists and staff management
- **Availability** – Working hours and staff leave
- **Appointments** – Booking, cancellation, rescheduling and status management
- **Reviews** – Customer reviews and ratings
- **Admin** – Platform administration and management

## Authentication

Most protected endpoints require a JWT access token.

Send the token using the HTTP Authorization header:

`Authorization: Bearer <access_token>`

You can obtain an access token using the **Authentication → Login** endpoint.

## User Roles

Glōvia supports three roles:

- `customer` – Can discover salons and manage appointments
- `salon` – Can manage salon information, services, staff, availability and appointments
- `admin` – Can manage the overall platform

## API Version

Current API version: **v1**

Base API path:

`/api/v1`
""",
    version="1.0.0",
    terms_of_service=None,
    contact={
        "name": "Glōvia Development Team",
    },
    license_info={
        "name": "Glōvia API",
    },
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.CORS_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# Authentication
# ============================================================

app.include_router(
    auth.router,
    prefix="/api/v1/auth",
    tags=["Authentication"],
)


# ============================================================
# Admin
# ============================================================

app.include_router(
    admin.router,
    prefix="/api/v1/admin",
    tags=["Admin"],
)


# ============================================================
# Salon Management
# ============================================================

app.include_router(
    salon_router,
    prefix="/api/v1/salon",
    tags=["Salon Management"],
)


# ============================================================
# Salon Services
# ============================================================

app.include_router(
    services.router,
    prefix="/api/v1/salon",
    tags=["Salon Services"],
)


# ============================================================
# Salon Staff
# ============================================================

app.include_router(
    staff.router,
    prefix="/api/v1/salon/{salon_id}/staff",
    tags=["Salon Staff"],
)


# ============================================================
# Salon Availability
# ============================================================

app.include_router(
    availability.router,
    prefix="/api/v1/availability",
    tags=["Salon Availability"],
)


# ============================================================
# Reviews
# ============================================================

app.include_router(
    reviews.router,
    prefix="/api/v1/reviews",
    tags=["Reviews"],
)


# ============================================================
# Appointments
# ============================================================

app.include_router(
    appointments.router,
    prefix="/api/v1/appointments",
    tags=["Appointments"],
)


# ============================================================
# Users
# ============================================================

app.include_router(
    users.router,
    prefix="/api/v1/users",
    tags=["Users"],
)


# ============================================================
# Root
# ============================================================

@app.get(
    "/",
    tags=["System"],
    summary="API Root",
    description="Returns a basic message confirming that the Glōvia API is running.",
)
async def root():
    return {
        "message": "Glōvia API is running"
    }


# ============================================================
# Health Check
# ============================================================

@app.get(
    "/health",
    tags=["System"],
    summary="Health Check",
    description="Returns the current health status of the API.",
)
async def health_check():
    return {
        "status": "healthy"
    }

