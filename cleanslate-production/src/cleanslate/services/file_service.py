from io import BytesIO
from pathlib import Path
import pandas as pd
from fastapi import UploadFile
from cleanslate.core.config import settings

SUPPORTED_EXTENSIONS = {".csv", ".xlsx"}

async def read_upload(upload: UploadFile) -> pd.DataFrame:
    extension = Path(upload.filename or "").suffix.lower()
    if extension not in SUPPORTED_EXTENSIONS:
        raise ValueError("Unsupported file type. Upload a CSV or XLSX file.")
    raw = await upload.read(settings.max_upload_bytes + 1)
    if not raw: raise ValueError("Uploaded file is empty.")
    if len(raw) > settings.max_upload_bytes:
        raise ValueError("Uploaded file exceeds the configured size limit.")
    try:
        if extension == ".csv": return pd.read_csv(BytesIO(raw))
        return pd.read_excel(BytesIO(raw), engine="openpyxl")
    except Exception as exc:
        raise ValueError("Could not read the uploaded file. Check that it is a valid CSV/XLSX.") from exc
