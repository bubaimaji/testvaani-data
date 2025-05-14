import streamlit as st
import pandas as pd
import os
from PIL import Image

# --- Config ---
CSV_PATH = "gopalganj_sampled_200_cleaned.csv"
st.set_page_config(page_title="Vaani-Hindi Test Set Viewer", layout="wide")
st.title("Vaani-Hindi Test Set Viewer")

# --- Load Data ---
@st.cache_data
def load_data():
    df = pd.read_csv(CSV_PATH)
    df = df[df["image_path"].notna() & df["audio_path"].notna()]
    return df.reset_index(drop=True)

df = load_data()

# --- Sample Selector ---
total = len(df)
idx = st.number_input(f"Choose a sample (1 to {total})", min_value=1, max_value=total, value=1, step=1)
row = df.iloc[idx - 1]

# --- Path Existence ---
image_path = row["image_path"]
audio_path = row["audio_path"]
image_exists = os.path.exists(image_path)
audio_exists = os.path.exists(audio_path)

# --- Layout ---
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Image")
    if image_exists:
        st.image(Image.open(image_path), caption=os.path.basename(image_path), use_container_width=True)
    else:
        st.warning("Image not found.")

with col2:
    st.subheader("Resultant Caption")
    st.markdown(f"**Caption:** {row['caption']}")

    st.subheader("Audio")
    if audio_exists:
        with open(audio_path, "rb") as f:
            st.audio(f.read(), format="audio/wav")
    else:
        st.warning("Audio not found.")

    st.subheader("Transcriptions (Whisper Translate Models)")
    for model in ["tiny", "base", "small", "medium", "large"]:
        trans_col = f"{model}_transcription"
        sim_col = f"{model}_similarity"
        if trans_col in row and pd.notna(row[trans_col]):
            st.markdown(f"**Model ({model})**")
            st.markdown(f"- Text: `{row[trans_col]}`")
            sim_val = row[sim_col]
            sim_display = f"{sim_val:.2f}" if pd.notna(sim_val) else "N/A"
            st.markdown(f"- Similarity: `{sim_display}`")
            st.markdown("---")
