import re
import pandas as pd

EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")

SUPPORTED_TYPES = {"email", "integer", "number", "date", "category"}

def validate_dataframe(frame: pd.DataFrame, rules: dict) -> dict:
    if not isinstance(rules, dict):
        raise ValueError("Validation rules must be a JSON object keyed by column name.")
    results = []
    for column, rule in rules.items():
        if not isinstance(rule, dict):
            raise ValueError(f"Rules for column '{column}' must be an object.")
        kind = rule.get("type")
        if kind not in SUPPORTED_TYPES:
            raise ValueError(f"Unsupported validation type for '{column}'.")
        if "min" in rule and "max" in rule and rule["min"] > rule["max"]:
            raise ValueError(f"Minimum cannot exceed maximum for '{column}'.")
        if kind == "category" and not isinstance(rule.get("allowed", []), list):
            raise ValueError(f"Allowed values for '{column}' must be a list.")
        if column not in frame.columns:
            results.append({"column": column, "valid": False, "error": "Column not found", "invalid_count": None})
            continue
        series = frame[column]
        blank = series.isna() | series.astype("string").str.strip().eq("").fillna(False)
        invalid = blank.copy() if rule.get("required", False) else pd.Series(False, index=series.index)
        candidate = ~blank
        if kind == "email":
            invalid |= candidate & ~series.astype("string").str.match(EMAIL_RE, na=False)
        elif kind == "integer":
            numeric = pd.to_numeric(series, errors="coerce")
            invalid |= candidate & (numeric.isna() | (numeric % 1 != 0))
        elif kind == "number":
            numeric = pd.to_numeric(series, errors="coerce")
            invalid |= candidate & numeric.isna()
            if "min" in rule: invalid |= candidate & (numeric < rule["min"])
            if "max" in rule: invalid |= candidate & (numeric > rule["max"])
        elif kind == "date":
            invalid |= candidate & pd.to_datetime(series, errors="coerce").isna()
        elif kind == "category":
            invalid |= candidate & ~series.isin(set(rule.get("allowed", [])))
        results.append({"column": column, "valid": int(invalid.sum()) == 0,
                        "invalid_count": int(invalid.sum()), "type": kind})
    return {"valid": all(item["valid"] for item in results), "columns": results}
