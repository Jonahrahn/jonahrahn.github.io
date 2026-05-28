"""Run Whisper inference over a corpus and write per-clip hypotheses.

Run as a script rather than a notebook for reproducibility.

Usage:
    python notebooks/10_run_whisper.py \
        --corpus bangor \
        --audio-glob 'data/bangor/*.16k.wav' \
        --out results/bangor.jsonl
"""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import whisper


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", required=True)
    ap.add_argument("--audio-glob", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--model", default="large-v3")
    ap.add_argument("--language", default=None, help="Force this language code, or None for auto-detect.")
    args = ap.parse_args()

    model = whisper.load_model(args.model)
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    files = sorted(Path().glob(args.audio_glob))
    with out_path.open("w") as f:
        for p in files:
            t0 = time.time()
            result = model.transcribe(
                str(p),
                language=args.language,
                task="transcribe",
                temperature=0.0,
                beam_size=5,
                best_of=5,
                condition_on_previous_text=False,
                word_timestamps=True,
            )
            f.write(
                json.dumps(
                    {
                        "corpus": args.corpus,
                        "clip": p.name,
                        "model": args.model,
                        "forced_language": args.language,
                        "text": result["text"],
                        "language_detected": result.get("language"),
                        "segments": result.get("segments", []),
                        "wall_time_s": round(time.time() - t0, 2),
                    }
                )
                + "\n"
            )
            f.flush()
            print(f"{p.name:40s} {result.get('language')}  ({time.time() - t0:.1f}s)")


if __name__ == "__main__":
    main()
