"""Run the benchmark against an OpenAI-compatible chat model.

Usage:
    python -m evals.run_openai --model gpt-4o --out results/gpt-4o.jsonl
"""
from __future__ import annotations

import argparse
import json
import os
import time
from pathlib import Path

from openai import OpenAI

from harness.score import load_items

PROMPT = """\
You will be shown a target sentence and two paraphrases.
Pick the paraphrase (A or B) that preserves the meaning of the target,
paying close attention to the scope and effect of any negation.
Reply with exactly one character: A or B.

TARGET: {target}

A) {paraphrase_a}
B) {paraphrase_b}

ANSWER:"""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--limit", type=int, default=None, help="Run only the first N items.")
    args = ap.parse_args()

    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    items = list(load_items().values())
    if args.limit:
        items = items[: args.limit]

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with out_path.open("w") as f:
        for item in items:
            t0 = time.time()
            resp = client.chat.completions.create(
                model=args.model,
                messages=[
                    {
                        "role": "user",
                        "content": PROMPT.format(
                            target=item.target,
                            paraphrase_a=item.paraphrase_a,
                            paraphrase_b=item.paraphrase_b,
                        ),
                    }
                ],
                temperature=0,
                max_tokens=4,
            )
            raw = resp.choices[0].message.content or ""
            ms = int((time.time() - t0) * 1000)
            choice = "abstain"
            for c in raw.upper():
                if c in "AB":
                    choice = c.lower()
                    break
            f.write(
                json.dumps(
                    {
                        "item_id": item.id,
                        "choice": choice,
                        "raw_output": raw[:64],
                        "latency_ms": ms,
                    }
                )
                + "\n"
            )
            f.flush()
            print(f"{item.id:20s} {choice} ({ms} ms)")


if __name__ == "__main__":
    main()
