import unittest
import pandas as pd
from editions.lite.engine import clean_dataframe, profile_dataframe, validate_dataframe

class LiteEngineTests(unittest.TestCase):
    def test_profile_counts_missing_and_duplicates(self):
        frame = pd.DataFrame({"name": ["A", None, "A"], "score": [1, 2, 1]})
        result = profile_dataframe(frame)
        self.assertEqual(result["row_count"], 3)
        self.assertEqual(result["duplicate_rows"], 1)
        self.assertEqual(result["columns"][0]["missing"], 1)

    def test_clean_trims_normalizes_and_deduplicates(self):
        frame = pd.DataFrame({"Full Name": [" Alice ", " Alice "], "Age": [20, 20]})
        result, summary = clean_dataframe(frame, drop_duplicates=True)
        self.assertEqual(list(result.columns), ["full_name", "age"])
        self.assertEqual(result.iloc[0]["full_name"], "Alice")
        self.assertEqual(summary["duplicates_removed"], 1)

    def test_validation_reports_bad_email(self):
        frame = pd.DataFrame({"email": ["valid@example.com", "bad"]})
        result = validate_dataframe(frame, {"email": {"type": "email", "required": True}})
        self.assertFalse(result["valid"])
        self.assertEqual(result["columns"][0]["invalid_count"], 1)

if __name__ == "__main__":
    unittest.main()
