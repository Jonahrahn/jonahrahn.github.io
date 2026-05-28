"""Agreement metrics: Cohen's kappa, Krippendorff's alpha, span F1."""
from __future__ import annotations

from collections import Counter
from typing import Iterable, Sequence


def cohens_kappa(a: Sequence[str], b: Sequence[str]) -> float:
    """Cohen's kappa for two raters on parallel token-level label sequences."""
    if len(a) != len(b) or not a:
        return 0.0
    n = len(a)
    labels = set(a) | set(b)
    po = sum(1 for x, y in zip(a, b) if x == y) / n
    ca = Counter(a)
    cb = Counter(b)
    pe = sum((ca[l] / n) * (cb[l] / n) for l in labels)
    if pe == 1.0:
        return 1.0
    return (po - pe) / (1 - pe)


def krippendorff_alpha(rater_labels: list[Sequence[str]]) -> float:
    """Nominal Krippendorff's alpha for >= 2 raters with equal-length sequences.

    Items where any rater is None are dropped.
    """
    if not rater_labels or any(len(rl) != len(rater_labels[0]) for rl in rater_labels):
        return 0.0
    units = list(zip(*rater_labels))
    units = [u for u in units if all(v is not None for v in u)]
    if not units:
        return 0.0

    # Observed disagreement
    from itertools import combinations

    do_num = 0
    do_den = 0
    for u in units:
        m = len(u)
        if m < 2:
            continue
        do_num += sum(1 for x, y in combinations(u, 2) if x != y) * 2
        do_den += m * (m - 1)
    do = do_num / do_den if do_den else 0.0

    # Expected disagreement
    counts: Counter = Counter()
    total = 0
    for u in units:
        for v in u:
            counts[v] += 1
            total += 1
    de_num = 0
    for x, cx in counts.items():
        for y, cy in counts.items():
            if x != y:
                de_num += cx * cy
    de = de_num / (total * (total - 1)) if total > 1 else 0.0
    if de == 0:
        return 1.0
    return 1 - do / de


def span_f1(
    pred_spans: Iterable[tuple[int, int, str]],
    gold_spans: Iterable[tuple[int, int, str]],
) -> dict[str, float]:
    """Exact-match span F1 over (start, end, label) triples."""
    pred = set(pred_spans)
    gold = set(gold_spans)
    if not pred and not gold:
        return {"precision": 1.0, "recall": 1.0, "f1": 1.0}
    tp = len(pred & gold)
    precision = tp / len(pred) if pred else 0.0
    recall = tp / len(gold) if gold else 0.0
    f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) else 0.0
    return {"precision": precision, "recall": recall, "f1": f1}
