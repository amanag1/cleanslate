import pandas as pd
from cleanslate.engine.validators import validate_dataframe

def test_email_validation_and_required():
    frame = pd.DataFrame({"email": ["good@example.com", "bad", None]})
    result = validate_dataframe(frame, {"email": {"type": "email", "required": True}})
    assert result["valid"] is False
    assert result["columns"][0]["invalid_count"] == 2

def test_missing_column_is_reported():
    result = validate_dataframe(pd.DataFrame({"x": [1]}), {"y": {"type": "integer"}})
    assert result["columns"][0]["error"] == "Column not found"

def test_integer_rejects_fractional_values():
    result = validate_dataframe(pd.DataFrame({"age": [2, 2.5]}), {"age": {"type": "integer"}})
    assert result["columns"][0]["invalid_count"] == 1
