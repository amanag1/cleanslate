from io import BytesIO
from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import StreamingResponse
import pandas as pd

from cleanslate.engine.cleaner import clean_dataframe
from cleanslate.engine.profiler import profile_dataframe
from cleanslate.services.file_service import read_upload

router = APIRouter()


@router.post("/profile", tags=["dataset"])
async def profile_file(file: UploadFile = File(...)):
    try:
        frame = await read_upload(file)
        return {"filename": file.filename, "profile": profile_dataframe(frame)}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/clean", tags=["dataset"])
async def clean_file(
    file: UploadFile = File(...),
    normalize_columns: bool = True,
    trim_text: bool = True,
    drop_duplicates: bool = False,
):
    try:
        frame = await read_upload(file)
        result, summary = clean_dataframe(
            frame,
            normalize_columns=normalize_columns,
            trim_text=trim_text,
            drop_duplicates=drop_duplicates,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    output = result.to_csv(index=False).encode("utf-8")
    filename = (file.filename or "dataset").rsplit(".", 1)[0] + "_cleaned.csv"
    return StreamingResponse(
        BytesIO(output),
        media_type="text/csv",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
            "X-CleanSlate-Summary": str(summary),
        },
    )
