import pandas as pd


def profile_dataframe(frame: pd.DataFrame) -> dict:
    columns = []
    for name in frame.columns:
        series = frame[name]
        columns.append({
            "name": str(name),
            "dtype": str(series.dtype),
            "rows": int(len(series)),
            "missing": int(series.isna().sum()),
            "missing_percent": round(float(series.isna().mean() * 100), 2),
            "unique": int(series.nunique(dropna=True)),
        })
    return {
        "row_count": int(len(frame)),
        "column_count": int(len(frame.columns)),
        "duplicate_rows": int(frame.duplicated().sum()),
        "columns": columns,
    }
