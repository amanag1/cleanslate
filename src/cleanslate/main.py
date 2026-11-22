from fastapi import FastAPI
from cleanslate.api.routes import router

app = FastAPI(
    title="CleanSlate API",
    description="Profile and clean CSV/Excel datasets using explicit, reproducible rules.",
    version="0.1.0",
)
app.include_router(router, prefix="/api/v1")


@app.get("/health", tags=["health"])
def health_check() -> dict[str, str]:
    return {"status": "ok", "service": "cleanslate"}
