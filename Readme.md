A specialized Python library for generating [pupcaps!](https://github.com/hosuaby/PupCaps)-compatible caption files. It uses forced alignment to match your original text transcript to the audio, producing a highly accurate, time-synced text output ready for the pupcaps! system.

# Installation
`pip install -I git+https://github.com/akarca/caption-utils.git`

# Usage
```python
from caption_utils import generate_captions, split_captions, caption_format

original_text = "..."
audio_file = "<path_to_audio_file>"  # It should be created from original text using a tts library or match the original text.

captions_json = generate_captions(audio_file, original_text)
splitted = split_captions(captions_json, words_count=3, max_chars=20)  # Split into chunks of 3 words and max 20 characters each
pupcaps_captions = caption_format(splitted)
```
