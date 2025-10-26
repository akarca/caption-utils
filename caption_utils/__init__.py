from functools import reduce
from big_phoney import BigPhoney
from Levenshtein import distance
from tools import split_sentences, format_time_from_seconds, transcribe

phoney = BigPhoney()

WORDS_CACHE = {}


def cached_phonize(word):
    if word in WORDS_CACHE:
        return WORDS_CACHE[word]
    WORDS_CACHE[word] = phoney.phonize(word)
    return WORDS_CACHE[word]


def getter(obj, *args, default=None):
    for arg in args:
        arg = "%s" % arg
        try:
            return reduce(
                lambda a, b: (
                    a[int(b)]
                    if b.isdigit()
                    else (getattr(a, b) if hasattr(a, b) else a[b])
                ),
                arg.split("."),
                obj,
            )
        except Exception:
            continue
    return default


def normalize(word):
    return (
        word.lower()
        .replace("ı", "i")
        .replace("ğ", "g")
        .replace("ç", "c")
        .replace("ş", "s")
        .replace("ö", "o")
        .replace("ü", "u")
        .strip(".,!? ")
    )


def fix_subtitles(sentence, words):
    needs_merge = len(sentence) != len(words)
    result = []
    for i, word in enumerate(sentence):
        original = normalize(word)
        subtitle = normalize(words[i]["word"])
        index_distance = distance(original, subtitle)
        if index_distance < 1:
            result.append(
                {"word": word, "start": words[i]["start"], "end": words[i]["end"]}
            )
            continue

        original = cached_phonize(original)
        subtitle = cached_phonize(subtitle)
        index_distance = distance(original, subtitle)

        next = None
        if needs_merge and getter(words, i + 1):
            next = cached_phonize(normalize(words[i + 1]["word"]))

        if next:
            merge_distance = distance(original, subtitle + next)
        else:
            merge_distance = 100

        if index_distance < merge_distance:
            result.append(
                {"word": word, "start": words[i]["start"], "end": words[i]["end"]}
            )
        else:
            result.append(
                {
                    "word": word,
                    "start": words[i]["start"],
                    "end": words[i + 1]["end"],
                }
            )
            j = i + 2
            for w in words[j:]:
                result.append({"word": w["word"], "start": w["start"], "end": w["end"]})
            return fix_subtitles(sentence, result)

    return result


def brackets(word, other_word):
    if word == other_word:
        return f"[{other_word}]"
    else:
        return other_word


def generate_captions(audio_file, original_text):
    segments = transcribe(audio_file)
    sentences = split_sentences(original_text)

    results = []
    for i, segment in enumerate(segments):
        sentence = sentences[i]
        original_words = sentence.split()

        subtitles = [
            {"word": word.word.strip(), "start": word.start, "end": word.end}
            for word in segment.words
        ]
        results.extend(fix_subtitles(original_words, subtitles))

    return results


def split_captions(captions, words_count=3, max_chars=20):
    results = []
    current_words = 0
    current_chars = 0
    current_batch = []

    for caption in captions:
        current_batch.append(caption)
        word = caption["word"]
        current_words += 1
        current_chars += len(word)

        if current_words == words_count or current_chars > max_chars:
            results.append(current_batch)
            current_chars = 0
            current_words = 0
            current_batch = []

    if current_batch:
        results.append(current_batch)

    return results


def caption_format(captions):
    results = []
    i = 0
    for split_captions in captions:
        for word in split_captions:
            i += 1
            start_time = format_time_from_seconds(word["start"])
            end_time = format_time_from_seconds(word["end"])
            results.append(i)
            results.append(f"{start_time} --> {end_time}")
            results.append(
                " ".join([brackets(word["word"], w["word"]) for w in split_captions])
            )
            results.append("")

    return results
