from faster_whisper import WhisperModel

print("Loading Whisper model...")

model = WhisperModel(
    "base",
    device="cpu",
    compute_type="int8"
)

print("Model loaded successfully.")

audio_file = input(
    "Enter the path to an audio file: "
).strip()

segments, info = model.transcribe(
    audio_file,
    beam_size=5
)

print()
print("Detected language:", info.language)
print(
    "Language probability:",
    round(info.language_probability, 3)
)

print()
print("===== TRANSCRIPT =====")

for segment in segments:

    print(
        f"[{segment.start:.2f}s - "
        f"{segment.end:.2f}s] "
        f"{segment.text.strip()}"
    )

print()
print("===== DONE =====")