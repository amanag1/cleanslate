import pandas as pd
from cleanslate.engine.cleaner import clean_dataframe, normalize_column_name


def test_normalize_column_name():
    assert normalize_column_name(" First Name / ID ") == "first_name_id"


def test_clean_trims_and_normalizes_columns():
    frame = pd.DataFrame({"First Name": [" Alice ", "Bob  "], "Age (Years)": [20, 30]})
    result, summary = clean_dataframe(frame)
    assert list(result.columns) == ["first_name", "age_years"]
    assert result["first_name"].tolist() == ["Alice", "Bob"]
    assert summary["rows_after"] == 2


def test_duplicate_normalized_columns_are_unique():
    frame = pd.DataFrame([[1, 2]], columns=["A-B", "A B"])
    result, _ = clean_dataframe(frame)
    assert list(result.columns) == ["a_b", "a_b_2"]


def test_drop_duplicates_counts_removed():
    frame = pd.DataFrame({"x": [1, 1, 2]})
    result, summary = clean_dataframe(frame, drop_duplicates=True)
    assert len(result) == 2
    assert summary["duplicates_removed"] == 1
