from pathlib import Path
import json
import pandas as pd
import streamlit as st
from engine import clean_dataframe, profile_dataframe, validate_dataframe

st.set_page_config(page_title="CleanSlate Lite", page_icon="🧹", layout="wide")
st.title("CleanSlate Lite")
st.caption("A lightweight local edition. Files stay on your computer; nothing is uploaded to a CleanSlate server.")
uploaded = st.file_uploader("Choose a CSV or Excel workbook", type=["csv", "xlsx"])
if uploaded:
    try:
        frame = pd.read_csv(uploaded) if uploaded.name.lower().endswith(".csv") else pd.read_excel(uploaded, engine="openpyxl")
        st.subheader("Preview")
        st.dataframe(frame.head(100), use_container_width=True)
        profile = profile_dataframe(frame)
        col1, col2, col3 = st.columns(3)
        col1.metric("Rows", profile["row_count"])
        col2.metric("Columns", profile["column_count"])
        col3.metric("Duplicate rows", profile["duplicate_rows"])
        st.subheader("Column profile")
        st.dataframe(pd.DataFrame(profile["columns"]), use_container_width=True)
        st.download_button("Download profile JSON", json.dumps(profile, indent=2),
                           file_name="cleanslate_profile.json", mime="application/json")
        st.subheader("Clean dataset")
        normalize = st.checkbox("Normalize column names", value=True)
        trim = st.checkbox("Trim text whitespace", value=True)
        dedupe = st.checkbox("Remove exact duplicate rows", value=False)
        if st.button("Run cleanup", type="primary"):
            cleaned, summary = clean_dataframe(frame, normalize_columns=normalize,
                trim_text=trim, drop_duplicates=dedupe)
            st.success("Cleanup completed. Original upload was not modified.")
            st.json(summary)
            st.download_button("Download cleaned CSV", cleaned.to_csv(index=False).encode("utf-8"),
                file_name=f"{Path(uploaded.name).stem}_cleaned.csv", mime="text/csv")
            xlsx = __import__("io").BytesIO()
            with pd.ExcelWriter(xlsx, engine="openpyxl") as writer:
                cleaned.to_excel(writer, index=False, sheet_name="Cleaned data")
            st.download_button("Download cleaned Excel", xlsx.getvalue(),
                file_name=f"{Path(uploaded.name).stem}_cleaned.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        with st.expander("Validate data with rules"):
            rule_text = st.text_area("JSON rules", value='{"Email": {"type": "email", "required": true}}')
            if st.button("Validate dataset"):
                try:
                    result = validate_dataframe(frame, json.loads(rule_text))
                    st.json(result)
                    st.download_button("Download validation JSON", json.dumps(result, indent=2),
                        file_name="cleanslate_validation.json", mime="application/json")
                except (ValueError, json.JSONDecodeError) as exc:
                    st.error(str(exc))
    except Exception as exc:
        st.error(f"Could not read this file: {exc}")
