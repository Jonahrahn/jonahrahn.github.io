# 01 · Setup

## Environment

- Python 3.11
- `openai-whisper` (or `faster-whisper` if GPU memory is tight)
- `jiwer` for WER computation
- `pandas`, `matplotlib`
- A GPU is strongly recommended; `large-v3` inference on CPU is ~30x slower

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## Hardware notes

- T4 (Colab free tier): batch size 1, ~1 minute per 30-second clip
- A10G or better: batch size 8, ~5 seconds per clip
- M1/M2 with MPS: works via `faster-whisper`, slower than a small GPU but workable

## Whisper inference settings

For reproducibility, lock these:

```python
options = {
    "task": "transcribe",
    "language": None,            # let Whisper auto-detect; later runs force per-corpus
    "temperature": 0.0,
    "beam_size": 5,
    "best_of": 5,
    "no_speech_threshold": 0.6,
    "logprob_threshold": -1.0,
    "compression_ratio_threshold": 2.4,
    "condition_on_previous_text": False,  # critical: keeps clips independent
}
```

## Data preparation

All audio is resampled to 16 kHz mono before inference, since Whisper expects that. Use:

```bash
ffmpeg -i input.wav -ar 16000 -ac 1 -c:a pcm_s16le output.wav
```

## Code-switch annotation

The reference transcripts are annotated with a per-word language tag:

```
yung [tgl] new [eng] phone [eng] mo [tgl] kanina [tgl]
```

The alignment step lifts these tags through forced alignment with the audio so we can ask, of each Whisper-emitted word, "what is the gold language at this position?" and bucket errors accordingly.
