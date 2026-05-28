"""Align Whisper hypotheses to per-word language-tagged gold, then compute
bucketed WER (mono-L1, mono-L2, pre-switch, post-switch, intra-word).

Usage:
    python notebooks/20_align_and_wer.py \
        --hyps results/bangor.jsonl \
        --gold data/bangor/gold.jsonl \
        --out results/bangor.wer.json
"""
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

import jiwer


def load_jsonl(path: Path) -> list[dict]:
    with path.open() as f:
        return [json.loads(line) for line in f if line.strip()]


def bucket_words(gold_words: list[dict]) -> list[str]:
    """Return per-gold-word bucket labels."""
    out: list[str] = []
    for i, w in enumerate(gold_words):
        lang = w.get("lang", "?")
        prev = gold_words[i - 1].get("lang") if i > 0 else None
        nxt = gold_words[i + 1].get("lang") if i + 1 < len(gold_words) else None
        if w.get("intra_word"):
            out.append("intra-word")
        elif prev and prev != lang:
            out.append("post-switch")
        elif nxt and nxt != lang:
            out.append("pre-switch")
        else:
            out.append(f"mono-{lang}")
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--hyps", required=True)
    ap.add_argument("--gold", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    hyps = {h["clip"]: h for h in load_jsonl(Path(args.hyps))}
    gold = {g["clip"]: g for g in load_jsonl(Path(args.gold))}

    per_bucket: dict[str, list[float]] = defaultdict(list)
    overall_refs: list[str] = []
    overall_hyps: list[str] = []

    for clip, g in gold.items():
        if clip not in hyps:
            continue
        ref = " ".join(w["text"] for w in g["words"])
        hyp = hyps[clip]["text"]
        overall_refs.append(ref)
        overall_hyps.append(hyp)

        buckets = bucket_words(g["words"])
        # For per-bucket WER, score each bucket's *substring* of the reference
        # against the aligned hypothesis tokens. Real impl: use a per-word
        # alignment from jiwer.process_words.
        alignment = jiwer.process_words(ref, hyp)
        # alignment.alignments is a list-of-lists; one inner list per pair.
        ref_words = ref.split()
        word_correct = [True] * len(ref_words)
        for chunk_list in alignment.alignments:
            for chunk in chunk_list:
                if chunk.type != "equal":
                    for i in range(chunk.ref_start_idx, chunk.ref_end_idx):
                        if i < len(word_correct):
                            word_correct[i] = False

        for w_idx, bucket in enumerate(buckets):
            if w_idx >= len(word_correct):
                break
            per_bucket[bucket].append(0.0 if word_correct[w_idx] else 1.0)

    summary = {
        "overall_wer": round(jiwer.wer(overall_refs, overall_hyps), 4),
        "buckets": {
            k: {"n": len(v), "error_rate": round(sum(v) / len(v), 4) if v else None}
            for k, v in sorted(per_bucket.items())
        },
    }
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
