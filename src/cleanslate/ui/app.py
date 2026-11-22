import json
import pandas as pd
import streamlit as st
from cleanslate.engine.cleaner import clean_dataframe
from cleanslate.engine.profiler import profile_dataframe
from cleanslate.engine.validators import validate_dataframe

st.set_page_config(page_title="CleanSlate", page_icon="🧹", layout="wide")
st.title("CleanSlate")
st.caption("Inspect, clean and validate CSV and Excel datasets. Source files are never overwritten.")
uploaded = st.file_uploader("Choose a CSV or XLSX file", type=["csv", "xlsx"])
if uploaded:
    try:
        frame = pd.read_csv(uploaded) if uploaded.name.lower().endswith(".csv") else pd.read_excel(uploaded)
        st.subheader("Preview")
        st.dataframe(frame.head(100), use_container_width=True)
        profile = profile_dataframe(frame)
        a, b, c = st.columns(3)
        a.metric("Rows", profile["row_count"])
        b.metric("Columns", profile["column_count"])
        c.metric("Duplicate rows", profile["duplicate_rows"])
        st.subheader("Column profile")
        st.dataframe(pd.DataFrame(profile["columns"]), use_container_width=True)
        st.subheader("Cleanup options")
        normalize = st.checkbox("Normalize column names", value=True)
        trim = st.checkbox("Trim text whitespace", value=True)
        dedupe = st.checkbox("Remove exact duplicate rows", value=False)
        if st.button("Clean dataset", type="primary"):
            cleaned, summary = clean_dataframe(frame, normalize_columns=normalize,
                                               trim_text=trim, drop_duplicates=dedupe)
            st.success("Cleanup completed.")
            st.json(summary)
            st.download_button("Download cleaned CSV", cleaned.to_csv(index=False).encode("utf-8"),
                               file_name=uploaded.name.rsplit(".", 1)[0] + "_cleaned.csv",
                               mime="text/csv")
        with st.expander("Validate columns using JSON rules"):
            rules_text = st.text_area("Rules", value='{"Email": {"type": "email", "required": true}}')
            if st.button("Run validation"):
                try:
                    st.json(validate_dataframe(frame, json.loads(rules_text)))
                except (ValueError, json.JSONDecodeError) as exc:
                    st.error("Invalid JSON rules: " + str(exc))
    except Exception as exc:
        st.error("Unable to process this file: " + str(exc))
