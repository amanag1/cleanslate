from fastapi import FastAPI
from cleanslate.api.routes import router
from cleanslate.database.session import Base, engine
from cleanslate.database import models  # register ORM metadata

app = FastAPI(
    title="CleanSlate API",
    description="Profile and clean CSV/Excel datasets using explicit, reproducible rules.",
    version="0.1.0",
)
app.include_router(router, prefix="/api/v1")


@app.get("/health", tags=["health"])
def health_check() -> dict[str, str]:
    return {"status": "ok", "service": "cleanslate"}


@app.on_event("startup")
def initialize_database() -> None:
    if engine is not None:
        Base.metadata.create_all(bind=engine)
