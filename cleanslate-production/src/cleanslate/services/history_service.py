from cleanslate.database.session import SessionLocal
from cleanslate.database.models import ProcessingJob

def record_job(filename: str, operation: str, summary: dict) -> int | None:
    if SessionLocal is None: return None
    with SessionLocal() as session:
        job = ProcessingJob(original_filename=filename[:255], operation=operation, summary=summary)
        session.add(job)
        session.commit()
        session.refresh(job)
        return job.id

def list_jobs(limit: int = 50) -> list[dict]:
    if SessionLocal is None: return []
    with SessionLocal() as session:
        rows = session.query(ProcessingJob).order_by(ProcessingJob.created_at.desc()).limit(limit).all()
        return [{"id": row.id, "filename": row.original_filename, "operation": row.operation,
                 "status": row.status, "summary": row.summary, "created_at": row.created_at.isoformat()}
                for row in rows]
