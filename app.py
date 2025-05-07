import streamlit as st
import pandas as pd
import os
from PIL import Image

# ---- CONFIG ----
CSV_PATH = "test_set_metadata_hi_cleaned.csv"  # Use the cleaned file
st.set_page_config(page_title="Vaani-Hindi Test Set Viewer", layout="wide")
st.title("Vaani-Hindi Test Set Viewer")

# ---- Load CSV ----
@st.cache_data
def load_data():
    df = pd.read_csv(CSV_PATH)
    df = df[df["image_path"].notna() & df["audio_path"].notna()]
    return df.reset_index(drop=True)

df = load_data()

# ---- Sample selector ----
total = len(df)
idx = st.number_input(f"Choose a sample (1 to {total})", min_value=1, max_value=total, value=1, step=1)
row = df.iloc[idx - 1]

# ---- Path checking ----
image_exists = os.path.exists(row["image_path"])
audio_exists = os.path.exists(row["audio_path"])

# ---- Layout ----
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Image")
    if image_exists:
        st.image(Image.open(row["image_path"]), caption=row["file_id"], use_container_width=True)
    else:
        st.warning("Image not found.")

with col2:
    st.subheader("Resultant Caption")
    st.markdown(f"**Caption:** {row['caption']}")

    st.subheader("Audio")
    if audio_exists:
        with open(row["audio_path"], "rb") as f:
            st.audio(f.read(), format="audio/wav")
    else:
        st.warning("Audio not found.")

    st.subheader("Translate (Whisper Models)")
    for model in ["tiny", "base", "small", "medium", "large"]:
        trans_col = f"transcription_{model}"
        conf_col = f"confidence_{model}"
        if trans_col in row:
            st.markdown(f"**Model ({model})**")
            st.markdown(f"- Text: `{row[trans_col]}`")
            conf_val = row[conf_col]
            conf_display = f"{conf_val:.2f}" if pd.notna(conf_val) else "N/A"
            st.markdown(f"- Confidence: `{conf_display}`")
            st.markdown("---")
