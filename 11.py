import os
import shutil
import pandas as pd

# --- Config ---
csv_path = r"C:\Users\CET_Pc\Desktop\speech-technology\gopalganj_trans_caption_all_whisper_updated.csv"
source_root = "."  # Folder where original Audio and Image folders are located
dest_audio_dir = "audios"
dest_image_dir = "images"

# --- Create destination folders ---
os.makedirs(dest_audio_dir, exist_ok=True)
os.makedirs(dest_image_dir, exist_ok=True)

# --- Load and sample CSV ---
df = pd.read_csv(csv_path)
sampled_df = df.sample(n=200, random_state=42).reset_index(drop=True)  # random 210

# --- Copy sampled files only ---
for _, row in sampled_df.iterrows():
    # Audio
    if pd.notna(row["audio_path"]):
        src_audio = os.path.join(source_root, row["audio_path"])
        dst_audio = os.path.join(dest_audio_dir, os.path.basename(src_audio))
        if os.path.exists(src_audio):
            shutil.copy(src_audio, dst_audio)
        else:
            print(f"Missing audio: {src_audio}")

    # Image
    if pd.notna(row["image_path"]):
        src_image = os.path.join(source_root, row["image_path"])
        dst_image = os.path.join(dest_image_dir, os.path.basename(src_image))
        if os.path.exists(src_image):
            shutil.copy(src_image, dst_image)
        else:
            print(f"Missing image: {src_image}")

# --- Save sampled CSV with updated paths ---
sampled_df["audio_path"] = sampled_df["audio_path"].apply(lambda x: os.path.join(dest_audio_dir, os.path.basename(x)) if pd.notna(x) else x)
sampled_df["image_path"] = sampled_df["image_path"].apply(lambda x: os.path.join(dest_image_dir, os.path.basename(x)) if pd.notna(x) else x)
sampled_df.to_csv("gopalganj_sampled_200.csv", index=False)

print(" Random 200 samples copied to 'audio/' and 'image/' and saved in 'gopalganj_sampled_210.csv'")
