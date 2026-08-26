from fastapi import FastAPI

from app.api.v1.auth import router as auth_router


app = FastAPI(
    title="Glōvia API",
    description="Salon booking platform API",
    version="1.0.0",
)


app.include_router(auth_router)

@app.get("/")
async def root():
    return {
        "message": "Glōvia API is running"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "ok"
    }