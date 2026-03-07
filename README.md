# Linguist - English Jumbled Sentence Exercise

This is an interactive English learning exercise where users can reconstruct jumbled sentences using drag-and-drop functionality.

## Features

## Exercises

1. **Jumbled Sentence Exercise** (`english_jumbled_sentence_exercise.html`)
   - Interactive drag-and-drop to reconstruct a jumbled sentence.
   - Uses an external MP3 asset plus a separate exercise data file for the syllable timeline.

2. **Reading Ordering Exercise** (`reading_ordering_exercise.html`)
   - Read a short text ("A Busy Morning") and organize the events in chronological order.
   - Interactive drag-and-drop list with visual feedback and confetti upon completion.

## Files

- `reading_ordering_exercise.html`: The reading and ordering exercise.
- `english_jumbled_sentence_exercise.html`: The jumbled sentence exercise.
- `english_jumbled_sentence_exercise.data.js`: External configuration for the phrase, audio source, and syllable timing.
- `phrase.mp3` / `phrase.b64`: Audio assets.
- `english_jumbled_sentence_exercise.png`: Screenshot or reference image.

## Whisper Alignment

The English jumbled sentence exercise now uses an external data file for timing and audio playback instead of embedding a base64 MP3 directly in the HTML.

The phrase timing was recalibrated with Whisper word timestamps using:

```bash
whisper phrase.mp3 \
  --model base \
  --model_dir "$HOME/.cache/whisper" \
  --language English \
  --task transcribe \
  --word_timestamps True \
  --output_format json \
  --output_dir /tmp/whisper_phrase
```

Whisper returned these word boundaries for `phrase.mp3`:

- `The`: `0.00 - 0.18`
- `weather`: `0.18 - 0.50`
- `is`: `0.50 - 0.76`
- `beautiful`: `0.76 - 1.22`
- `today`: `1.22 - 1.66`

The UI still highlights syllables, so multi-syllable words are subdivided inside each Whisper word window and stored in `english_jumbled_sentence_exercise.data.js`.

Files involved:

- `english_jumbled_sentence_exercise.data.js`: Whisper-based timing source used by the page.
- `english_jumbled_sentence_exercise.html`: Runtime fallback if the data file does not load.
- `tests/browser_suite.html`: Regression checks for the karaoke timing and audio source.
- `tests/run_browser_tests.sh`: Headless browser runner.

## How to run

Simply open `english_jumbled_sentence_exercise.html` in any modern web browser or run a local web server:

```bash
python3 -m http.server 8080
```

Then navigate to `http://localhost:8080/english_jumbled_sentence_exercise.html`.

To run the browser checks:

```bash
bash tests/run_browser_tests.sh
```
