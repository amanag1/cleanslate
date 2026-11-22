"""Small, dependency-light data engine used by CleanSlate Lite."""
import re
import pandas as pd

EMAIL_RE = re.compile(r"^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$")

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
    return {"row_count": int(len(frame)), "column_count": int(len(frame.columns)),
            "duplicate_rows": int(frame.duplicated().sum()), "columns": columns}

def normalize_column_name(value: object) -> str:
    text = str(value).strip().lower()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    return re.sub(r"_+", "_", text).strip("_") or "column"

def clean_dataframe(frame: pd.DataFrame, *, normalize_columns: bool = True,
                    trim_text: bool = True, drop_duplicates: bool = False) -> tuple[pd.DataFrame, dict]:
    cleaned = frame.copy(deep=True)
    before_rows, before_cols = len(cleaned), list(cleaned.columns)
    if normalize_columns:
        names = [normalize_column_name(col) for col in cleaned.columns]
        seen, unique_names = {}, []
        for name in names:
            seen[name] = seen.get(name, 0) + 1
            unique_names.append(name if seen[name] == 1 else f"{name}_{seen[name]}")
        cleaned.columns = unique_names
    if trim_text:
        for col in cleaned.select_dtypes(include=["object", "string"]).columns:
            cleaned[col] = cleaned[col].map(lambda value: value.strip() if isinstance(value, str) else value)
    removed = 0
    if drop_duplicates:
        cleaned = cleaned.drop_duplicates().reset_index(drop=True)
        removed = before_rows - len(cleaned)
    return cleaned, {"rows_before": int(before_rows), "rows_after": int(len(cleaned)),
        "duplicates_removed": int(removed),
        "columns_renamed": bool(normalize_columns and before_cols != list(cleaned.columns))}

def validate_dataframe(frame: pd.DataFrame, rules: dict) -> dict:
    if not isinstance(rules, dict):
        raise ValueError("Rules must be a JSON object keyed by column name.")
    results = []
    supported = {"email", "integer", "number", "date", "category"}
    for column, rule in rules.items():
        if not isinstance(rule, dict) or rule.get("type") not in supported:
            raise ValueError(f"Invalid or unsupported rule for column '{column}'.")
        kind = rule["type"]
        if column not in frame.columns:
            results.append({"column": column, "valid": False, "error": "Column not found", "invalid_count": None})
            continue
        series = frame[column]
        blank = series.isna() | series.astype("string").str.strip().eq("").fillna(False)
        invalid = blank.copy() if rule.get("required", False) else pd.Series(False, index=series.index)
        candidate = ~blank
        if kind == "email":
            invalid |= candidate & ~series.astype("string").str.match(EMAIL_RE, na=False)
        elif kind in {"integer", "number"}:
            numeric = pd.to_numeric(series, errors="coerce")
            invalid |= candidate & numeric.isna()
            if kind == "integer": invalid |= candidate & (numeric % 1 != 0)
            if "min" in rule: invalid |= candidate & (numeric < rule["min"])
            if "max" in rule: invalid |= candidate & (numeric > rule["max"])
        elif kind == "date":
            invalid |= candidate & pd.to_datetime(series, errors="coerce").isna()
        elif kind == "category":
            allowed = rule.get("allowed", [])
            if not isinstance(allowed, list): raise ValueError(f"'allowed' must be a list for '{column}'.")
            invalid |= candidate & ~series.isin(set(allowed))
        results.append({"column": column, "valid": int(invalid.sum()) == 0,
                        "invalid_count": int(invalid.sum()), "type": kind})
    return {"valid": all(item["valid"] for item in results), "columns": results}
