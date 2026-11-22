import pandas as pd
from cleanslate.engine.profiler import profile_dataframe


def test_profile_reports_missing_and_duplicates():
    frame = pd.DataFrame({"name": ["a", None, "a"], "score": [1, 2, 1]})
    result = profile_dataframe(frame)
    assert result["row_count"] == 3
    assert result["duplicate_rows"] == 1
    assert result["columns"][0]["missing"] == 1
