"""Lint a data file: schema, uniqueness of IDs, balanced gold labels."""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path


REQUIRED = {"id", "phenomenon", "target", "paraphrase_a", "paraphrase_b", "gold"}
ALLOWED_GOLD = {"a", "b", "either"}


def lint(path: Path) -> int:
    errors: list[str] = []
    ids: list[str] = []
    golds: list[str] = []
    with path.open() as f:
        for n, line in enumerate(f, 1):
            if not line.strip():
                continue
            try:
                d = json.loads(line)
            except json.JSONDecodeError as e:
                errors.append(f"line {n}: invalid JSON: {e}")
                continue
            missing = REQUIRED - d.keys()
            if missing:
                errors.append(f"line {n} ({d.get('id', '?')}): missing {sorted(missing)}")
            if d.get("gold") not in ALLOWED_GOLD:
                errors.append(f"line {n} ({d.get('id', '?')}): bad gold={d.get('gold')!r}")
            ids.append(d.get("id", f"line-{n}"))
            golds.append(d.get("gold", "?"))

    dups = [i for i, c in Counter(ids).items() if c > 1]
    if dups:
        errors.append(f"duplicate ids: {dups}")

    gold_balance = Counter(golds)
    print(f"{path.name}: {len(ids)} items   gold balance: {dict(gold_balance)}")
    if gold_balance.get("a", 0) > 0 and gold_balance.get("b", 0) > 0:
        skew = abs(gold_balance["a"] - gold_balance["b"]) / (
            gold_balance["a"] + gold_balance["b"]
        )
        if skew > 0.2:
            errors.append(
                f"gold imbalance: a/b skew = {skew:.0%} (target < 20%)"
            )

    for e in errors:
        print("  ERROR:", e)
    return 0 if not errors else 1


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit("usage: python -m harness.validate <file.jsonl> [<file.jsonl> ...]")
    rc = 0
    for arg in sys.argv[1:]:
        rc |= lint(Path(arg))
    sys.exit(rc)


if __name__ == "__main__":
    main()
