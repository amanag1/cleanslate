from io import BytesIO
import pandas as pd
from fastapi import UploadFile

SUPPORTED_EXTENSIONS = {".csv", ".xlsx"}


async def read_upload(upload: UploadFile) -> pd.DataFrame:
    filename = upload.filename or ""
    extension = "." + filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    if extension not in SUPPORTED_EXTENSIONS:
        raise ValueError("Unsupported file type. Upload a CSV or XLSX file.")
    raw = await upload.read()
    if not raw:
        raise ValueError("Uploaded file is empty.")
    try:
        if extension == ".csv":
            return pd.read_csv(BytesIO(raw))
        return pd.read_excel(BytesIO(raw), engine="openpyxl")
    except Exception as exc:
        raise ValueError("Could not read the uploaded file. Check that it is a valid CSV/XLSX.") from exc
