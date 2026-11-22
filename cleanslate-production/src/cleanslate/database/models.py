from datetime import datetime, timezone
from sqlalchemy import DateTime, Integer, String, JSON
from sqlalchemy.orm import Mapped, mapped_column
from cleanslate.database.session import Base

class ProcessingJob(Base):
    __tablename__ = "processing_jobs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    original_filename: Mapped[str] = mapped_column(String(255))
    operation: Mapped[str] = mapped_column(String(32))
    status: Mapped[str] = mapped_column(String(24), default="completed")
    summary: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
