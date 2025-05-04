import streamlit as st
import pandas as pd
import os
from PIL import Image

CSV_PATH = "test_set_metadata.csv"  

st.set_page_config(page_title="Vaani-Hindi Test Set Viewer", layout="wide")
st.title("Vaani-Hindi Test Set Viewer")

@st.cache_data
def load_data():
    df = pd.read_csv(CSV_PATH)
    df = df[df["image_path"].notna() & df["audio_path"].notna()]
    return df.sample(n=min(500, len(df)), random_state=42).reset_index(drop=True)

df = load_data()

total = len(df)
idx = st.number_input("Choose a sample (1 to {})".format(total), min_value=1, max_value=total, value=1, step=1)
row = df.iloc[idx - 1]

image_exists = os.path.exists(row["image_path"])
audio_exists = os.path.exists(row["audio_path"])

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader(" Image")
    if image_exists:
        st.image(Image.open(row["image_path"]), caption=row["file_id"], use_container_width=True)
    else:
        st.warning(" Image not found.")

with col2:
    st.subheader(" Resultant Caption ")
    st.markdown(f"**Caption:** {row['caption']}")

    st.subheader(" Audio")
    if audio_exists:
        with open(row["audio_path"], "rb") as f:
            st.audio(f.read(), format="audio/wav")
    else:
        st.warning("Audio not found.")

    st.subheader(" Transcription (Whisper-tiny)")
    st.markdown(f"**Text:** {row['transcription']}")
    st.markdown(f"**Confidence:** {row['confidence']:.2f}" if pd.notna(row['confidence']) else "**Confidence:** N/A")

    
