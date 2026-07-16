from fastapi import FastAPI

from app.auth.routes import router as auth_router


app = FastAPI(
    title="AI Startup Platform",
    version="0.2.0"
)


app.include_router(
    auth_router,
    prefix="/auth",
    tags=["Authentication"]
)


@app.get("/")
def root():
    return {
        "message": "Welcome to AI Startup Platform",
        "status": "running"
    }
