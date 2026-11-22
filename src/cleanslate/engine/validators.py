import re
import pandas as pd

EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")

def validate_dataframe(frame: pd.DataFrame, rules: dict) -> dict:
    results = []
    for column, rule in rules.items():
        if column not in frame.columns:
            results.append({"column": column, "valid": False, "error": "Column not found", "invalid_count": None})
            continue
        series = frame[column]
        invalid = pd.Series(False, index=series.index)
        kind = rule.get("type")
        if rule.get("required", False):
            invalid |= series.isna() | series.astype("string").str.strip().eq("").fillna(False)
        if kind == "email":
            invalid |= ~series.astype("string").str.match(EMAIL_RE, na=False)
        elif kind == "integer":
            numeric = pd.to_numeric(series, errors="coerce")
            invalid |= numeric.isna() | (numeric % 1 != 0)
        elif kind == "number":
            numeric = pd.to_numeric(series, errors="coerce")
            invalid |= numeric.isna()
            if "min" in rule: invalid |= numeric < rule["min"]
            if "max" in rule: invalid |= numeric > rule["max"]
        elif kind == "date":
            invalid |= pd.to_datetime(series, errors="coerce").isna()
        elif kind == "category":
            invalid |= ~series.isin(set(rule.get("allowed", [])))
        results.append({"column": column, "valid": int(invalid.sum()) == 0,
                        "invalid_count": int(invalid.sum()), "type": kind})
    return {"valid": all(item["valid"] for item in results), "columns": results}
