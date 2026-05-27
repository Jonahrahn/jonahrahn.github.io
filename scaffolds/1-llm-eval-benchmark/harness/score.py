"""Score a model's predictions and emit a per-phenomenon breakdown.

Usage:
    python -m harness.score results/<model>.jsonl
"""
from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

from .types import Item, Prediction, ScoredItem

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def load_items() -> dict[str, Item]:
    items: dict[str, Item] = {}
    for path in sorted(DATA_DIR.glob("*.jsonl")):
        with path.open() as f:
            for line in f:
                if not line.strip():
                    continue
                d = json.loads(line)
                items[d["id"]] = Item(
                    id=d["id"],
                    phenomenon=d["phenomenon"],
                    target=d["target"],
                    paraphrase_a=d["paraphrase_a"],
                    paraphrase_b=d["paraphrase_b"],
                    gold=d["gold"],
                    rationale=d.get("rationale", ""),
                    tags=tuple(d.get("tags", [])),
                )
    return items


def load_predictions(path: Path) -> list[Prediction]:
    preds: list[Prediction] = []
    with path.open() as f:
        for line in f:
            if not line.strip():
                continue
            d = json.loads(line)
            preds.append(
                Prediction(
                    item_id=d["item_id"],
                    choice=d["choice"],
                    raw_output=d.get("raw_output", ""),
                    latency_ms=d.get("latency_ms"),
                )
            )
    return preds


def score(items: dict[str, Item], preds: list[Prediction]) -> list[ScoredItem]:
    scored: list[ScoredItem] = []
    for p in preds:
        if p.item_id not in items:
            continue
        item = items[p.item_id]
        correct = (
            item.gold == "either"
            or (p.choice == item.gold and p.choice != "abstain")
        )
        scored.append(ScoredItem(item=item, prediction=p, correct=correct))
    return scored


def summarize(scored: list[ScoredItem]) -> dict:
    overall = sum(s.correct for s in scored) / len(scored) if scored else 0.0
    by_phen: dict[str, list[bool]] = defaultdict(list)
    for s in scored:
        by_phen[s.item.phenomenon].append(s.correct)
    return {
        "overall": round(overall, 3),
        "n": len(scored),
        "by_phenomenon": {
            k: {"acc": round(sum(v) / len(v), 3), "n": len(v)}
            for k, v in sorted(by_phen.items())
        },
    }


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: python -m harness.score results/<model>.jsonl")
    path = Path(sys.argv[1])
    items = load_items()
    preds = load_predictions(path)
    scored = score(items, preds)
    summary = summarize(scored)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
