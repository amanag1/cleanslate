import re
import pandas as pd


def normalize_column_name(value: object) -> str:
    text = str(value).strip().lower()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    return re.sub(r"_+", "_", text).strip("_") or "column"


def clean_dataframe(
    frame: pd.DataFrame,
    *,
    normalize_columns: bool = True,
    trim_text: bool = True,
    drop_duplicates: bool = False,
) -> tuple[pd.DataFrame, dict]:
    cleaned = frame.copy(deep=True)
    before_rows = len(cleaned)
    before_cols = list(cleaned.columns)

    if normalize_columns:
        cleaned.columns = [normalize_column_name(col) for col in cleaned.columns]
        # Avoid collisions after normalization (e.g. "First Name" and "first-name").
        seen: dict[str, int] = {}
        unique_names = []
        for name in cleaned.columns:
            seen[name] = seen.get(name, 0) + 1
            unique_names.append(name if seen[name] == 1 else f"{name}_{seen[name]}")
        cleaned.columns = unique_names

    if trim_text:
        for col in cleaned.select_dtypes(include=["object", "string"]).columns:
            cleaned[col] = cleaned[col].map(lambda value: value.strip() if isinstance(value, str) else value)

    duplicates_removed = 0
    if drop_duplicates:
        cleaned = cleaned.drop_duplicates().reset_index(drop=True)
        duplicates_removed = before_rows - len(cleaned)

    summary = {
        "rows_before": int(before_rows),
        "rows_after": int(len(cleaned)),
        "duplicates_removed": int(duplicates_removed),
        "columns_renamed": bool(normalize_columns and before_cols != list(cleaned.columns)),
    }
    return cleaned, summary
