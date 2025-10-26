from faster_whisper import WhisperModel
from sentence_splitter import SentenceSplitter


def transcribe(audio_file):
    # 1. Initialize the model
    # Choose a model size (e.g., "small", "medium", "large-v3").
    # Use a smaller model like "base" or "small" for faster inference.
    # device="cuda" uses GPU, device="cpu" uses CPU.
    model_size = "base"
    model = WhisperModel(
        model_size, device="cpu", compute_type="int8"
    )  # Use "int8" for CPU for best speed/accuracy balance

    segments, _ = model.transcribe(audio_file, word_timestamps=True, language="en")

    return segments


def split_sentences(txt):
    splitter = SentenceSplitter(language="en")
    return splitter.split(text=txt)


def format_time_from_seconds(total_seconds: float) -> str:
    """
    Translates a total duration in seconds (float) into a human-readable time
    string in the format HH:MM:SS,mmm.

    Args:
        total_seconds: The duration in seconds as a float (e.g., 51.98).

    Returns:
        A formatted time string (e.g., "00:00:51,980").
    """
    if total_seconds < 0:
        # Handle negative duration gracefully, perhaps raising an error or returning a fixed string.
        # For this example, we'll treat it as 0
        total_seconds = 0.0

    # --- 1. Separate Seconds and Milliseconds ---
    # The integer part of the seconds
    integer_seconds = int(total_seconds)

    # The fractional part, multiplied by 1000 and rounded to get milliseconds
    # We use round to handle floating point imprecision, ensuring the value is an integer between 0 and 999.
    milliseconds = round((total_seconds - integer_seconds) * 1000)

    # Check if rounding pushed us to 1000ms (which is 1 second).
    if milliseconds >= 1000:
        integer_seconds += 1
        milliseconds = 0

    # --- 2. Calculate H, M, S from Integer Seconds ---
    # 1 hour = 3600 seconds
    hours = integer_seconds // 3600

    # Remaining seconds after accounting for hours
    seconds_remainder = integer_seconds % 3600

    # 1 minute = 60 seconds
    minutes = seconds_remainder // 60

    # Remaining seconds after accounting for minutes
    seconds = seconds_remainder % 60

    # --- 3. Format the Output String ---
    # Use f-strings for efficient formatting:
    # :02d ensures two digits with a leading zero if necessary (e.g., 5 -> 05)
    # :03d ensures three digits for milliseconds (e.g., 98 -> 098, 980 -> 980)
    formatted_time = f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"

    return formatted_time
