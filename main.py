from faster_whisper import WhisperModel

# 1. Initialize the model
# Choose a model size (e.g., "small", "medium", "large-v3").
# Use a smaller model like "base" or "small" for faster inference.
# device="cuda" uses GPU, device="cpu" uses CPU.
model_size = "medium"
model = WhisperModel(
    model_size, device="cpu", compute_type="int8"
)  # Use "int8" for CPU for best speed/accuracy balance

audio_file = "audio.wav"  # Replace with your audio file path

# 2. Transcribe the audio with word-level timestamps
print("Transcribing audio...")
segments, info = model.transcribe(
    audio_file,
    word_timestamps=True,  # Key argument for word-level timestamps
    # Optional: specify language if known to improve speed/accuracy
    # language="en"
)

# 3. Process and print the results
print(
    f"Detected language: {info.language} with probability {info.language_probability}"
)
print("--- Word Timestamps ---")

# Iterate through all segments and then through the words in each segment
for segment in segments:
    # Print the segment's text for context
    print(f"\n[Segment: {segment.start:.2f}s - {segment.end:.2f}s]")

    if segment.words:
        for word in segment.words:
            # Each 'word' object contains start time, end time, and the word text
            print(f"[{word.start:.2f}s -> {word.end:.2f}s] {word.word}")
