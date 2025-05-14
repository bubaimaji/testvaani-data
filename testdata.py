import json

input_file = "Vaani_IIsc_Artpark_Full_Data.json"
target_languages = {"English", "Hindi", "Bengali"}
samples_per_language = 20

# To handle both "Bangla" and "Bengali" as same group
language_map = {
    "Hindi": "Hindi",
    "Bengali": "Bengali",
    "English": "English"
}

# Storage for 20 samples each
language_samples = {
    "Hindi": [],
    "Bengali": [],
    "English": []
}

# Load the data
with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)

# Extract URLs per language
for item in data:
    meta = item.get("metadata", {})
    lang_raw = meta.get("assertLanguage", "").strip()
    lang = language_map.get(lang_raw)
    
    if lang and len(language_samples[lang]) < samples_per_language:
        audio_url = item.get("file_url")
        image_path = meta.get("imageFileName")
        if audio_url and image_path:
            image_url = f"https://vaani.iisc.ac.in/{image_path}"
            language_samples[lang].append((audio_url, image_url))

    # Stop if we have 20 for each
    if all(len(v) == samples_per_language for v in language_samples.values()):
        break

# Print results
for lang, samples in language_samples.items():
    print(f"\n ===== {lang.upper()} SAMPLES =====")
    for idx, (audio, image) in enumerate(samples, 1):
        print(f"{idx:02d}.  Audio: {audio}")
        print(f"     Image: {image}\n")

print("\n Done printing 20 samples each for English, Hindi, and Bangla.")
