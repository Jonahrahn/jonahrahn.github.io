"""Re-render the leaderboard table in README.md from results/*.jsonl."""
from __future__ import annotations

import json
import re
from pathlib import Path

from .score import load_items, load_predictions, score, summarize

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
START = "<!-- LEADERBOARD:START -->"
END = "<!-- LEADERBOARD:END -->"


def main() -> None:
    items = load_items()
    rows: list[dict] = []
    for path in sorted((ROOT / "results").glob("*.jsonl")):
        preds = load_predictions(path)
        summary = summarize(score(items, preds))
        rows.append({"model": path.stem, **summary})

    if not rows:
        print("no results yet")
        return

    phenomena = sorted({p for r in rows for p in r["by_phenomenon"]})
    headers = ["Model", "Overall"] + phenomena
    lines = ["| " + " | ".join(headers) + " |", "|" + "|".join(["---"] * len(headers)) + "|"]
    for r in rows:
        row = [r["model"], f"{r['overall']:.2f}"]
        for p in phenomena:
            cell = r["by_phenomenon"].get(p, {})
            row.append(f"{cell['acc']:.2f}" if cell else "—")
        lines.append("| " + " | ".join(row) + " |")
    table = "\n".join(lines)

    text = README.read_text()
    if START in text and END in text:
        text = re.sub(
            re.escape(START) + r".*?" + re.escape(END),
            START + "\n" + table + "\n" + END,
            text,
            flags=re.DOTALL,
        )
    else:
        text += f"\n\n{START}\n{table}\n{END}\n"
    README.write_text(text)
    print(table)


if __name__ == "__main__":
    main()
