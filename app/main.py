from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import (
    admin,
    auth,
    salons,
    users,
)
from app.core.config import settings


app = FastAPI(
    title="Glōvia API",
    description="Salon booking platform API",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.CORS_ORIGIN,
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(salons.router)
app.include_router(users.router)


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