import io
import json
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Parquet to CSV & JSON", page_icon="🧾", layout="centered")
st.title("Parquet to CSV & JSON Converter")

uploaded = st.file_uploader("Upload a Parquet file", type=["parquet"])

def df_to_csv_bytes(df: pd.DataFrame) -> bytes:
    return df.to_csv(index=False).encode("utf-8")

def df_to_json_bytes(df: pd.DataFrame) -> bytes:
    return json.dumps(df.to_dict(orient="records"), ensure_ascii=False, indent=2).encode("utf-8")

if uploaded:
    try:
        df = pd.read_parquet(uploaded, engine="pyarrow")
    except Exception as e:
        st.error(f"Failed to read Parquet: {e}")
        st.info("Tip: Ensure 'pyarrow' is installed:  python -m pip install pyarrow")
        st.stop()

    st.success(f"Loaded Parquet → DataFrame shape {df.shape}")
    st.dataframe(df.head(100), use_container_width=True)

    st.subheader("Download Converted Formats")
    col1, col2 = st.columns(2)

    with col1:
        st.download_button(
            "Download CSV",
            data=df_to_csv_bytes(df),
            file_name="converted.csv",
            mime="text/csv"
        )

    with col2:
        st.download_button(
            "Download JSON",
            data=df_to_json_bytes(df),
            file_name="converted.json",
            mime="application/json"
        )
else:
    st.info("Upload a Parquet file to begin.")
