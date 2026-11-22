import os
from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    max_upload_bytes: int = int(os.getenv("CLEANSLATE_MAX_UPLOAD_BYTES", 25 * 1024 * 1024))
    database_url: str | None = os.getenv("DATABASE_URL")

settings = Settings()
