"""Convert span annotations to token-level BIO label sequences, and align documents."""
from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass
class TokenSpan:
    start: int
    end: int
    text: str


def tokenize(text: str) -> list[TokenSpan]:
    """Simple whitespace + punctuation tokenizer that records character offsets."""
    spans: list[TokenSpan] = []
    for m in re.finditer(r"\w+|[^\w\s]", text):
        spans.append(TokenSpan(m.start(), m.end(), m.group()))
    return spans


def spans_to_token_labels(
    text: str,
    spans: list[dict],
    outside: str = "O",
) -> list[str]:
    """Project character-offset spans onto token-level BIO labels."""
    tokens = tokenize(text)
    labels = [outside] * len(tokens)
    for s in spans:
        ts, te, label = s["start"], s["end"], s["label"]
        first = True
        for i, tok in enumerate(tokens):
            if tok.start >= ts and tok.end <= te:
                labels[i] = ("B-" if first else "I-") + label
                first = False
    return labels


def align_documents(docs_a: list[dict], docs_b: list[dict]) -> list[tuple[dict, dict]]:
    """Pair two annotators' docs by doc_id. Skip docs missing in either set."""
    by_id_a = {d["doc_id"]: d for d in docs_a}
    by_id_b = {d["doc_id"]: d for d in docs_b}
    common = sorted(by_id_a.keys() & by_id_b.keys())
    return [(by_id_a[i], by_id_b[i]) for i in common]


def find_disagreements(
    doc_a: dict, doc_b: dict
) -> list[dict]:
    """Return per-span disagreements with surrounding text context."""
    text = doc_a["text"]
    a_spans = {(s["start"], s["end"]): s["label"] for s in doc_a["spans"]}
    b_spans = {(s["start"], s["end"]): s["label"] for s in doc_b["spans"]}
    all_keys = sorted(a_spans.keys() | b_spans.keys())
    rows: list[dict] = []
    for start, end in all_keys:
        la, lb = a_spans.get((start, end)), b_spans.get((start, end))
        if la == lb:
            continue
        ctx_start = max(0, start - 30)
        ctx_end = min(len(text), end + 30)
        rows.append(
            {
                "doc_id": doc_a["doc_id"],
                "start": start,
                "end": end,
                "text": text[start:end],
                "context": text[ctx_start:ctx_end],
                "annotator_a": doc_a.get("annotator", "A"),
                "annotator_b": doc_b.get("annotator", "B"),
                "label_a": la or "(none)",
                "label_b": lb or "(none)",
            }
        )
    return rows
