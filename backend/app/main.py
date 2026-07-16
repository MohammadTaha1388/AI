from fastapi import FastAPI

app = FastAPI(
    title="AI Startup Platform",
    version="0.1.0"
)

@app.get("/")
def root():
    return {
        "message": "Welcome to AI Startup Platform",
        "status": "running"
    }

@app.get("/health")
def health():
    return {
        "status": "ok"
    }