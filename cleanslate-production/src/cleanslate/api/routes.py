from io import BytesIO
import json
from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import StreamingResponse
from cleanslate.engine.cleaner import clean_dataframe
from cleanslate.engine.profiler import profile_dataframe
from cleanslate.engine.validators import validate_dataframe
from cleanslate.services.file_service import read_upload
from cleanslate.services.history_service import list_jobs, record_job

router = APIRouter()

@router.post("/profile", tags=["dataset"])
async def profile_file(file: UploadFile = File(...)):
    try:
        frame = await read_upload(file)
        result = profile_dataframe(frame)
        record_job(file.filename or "upload", "profile", result)
        return {"filename": file.filename, "profile": result}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

@router.post("/clean", tags=["dataset"])
async def clean_file(file: UploadFile = File(...), normalize_columns: bool = True,
                     trim_text: bool = True, drop_duplicates: bool = False):
    try:
        frame = await read_upload(file)
        result, summary = clean_dataframe(frame, normalize_columns=normalize_columns,
                                          trim_text=trim_text, drop_duplicates=drop_duplicates)
        record_job(file.filename or "upload", "clean", summary)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    output = result.to_csv(index=False).encode("utf-8")
    filename = (file.filename or "dataset").rsplit(".", 1)[0] + "_cleaned.csv"
    return StreamingResponse(BytesIO(output), media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'})

@router.post("/validate", tags=["dataset"])
async def validate_file(file: UploadFile = File(...), rules: str = "{}"):
    try:
        frame = await read_upload(file)
        result = validate_dataframe(frame, json.loads(rules))
        record_job(file.filename or "upload", "validate", result)
        return result
    except (ValueError, json.JSONDecodeError) as exc:
        raise HTTPException(status_code=400, detail=f"Invalid input: {exc}") from exc

@router.get("/history", tags=["history"])
def processing_history(limit: int = 50):
    if not 1 <= limit <= 200: raise HTTPException(status_code=400, detail="limit must be between 1 and 200")
    return {"items": list_jobs(limit)}
