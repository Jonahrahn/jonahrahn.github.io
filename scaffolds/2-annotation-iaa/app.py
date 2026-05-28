"""Streamlit dashboard for span-annotation inter-rater agreement.

Run locally:
    streamlit run app.py
"""
from __future__ import annotations

import json
from io import StringIO

import pandas as pd
import streamlit as st

from iaa import (
    cohens_kappa,
    krippendorff_alpha,
    span_f1,
    spans_to_token_labels,
    align_documents,
)
from iaa.span_utils import find_disagreements

st.set_page_config(page_title="IAA Dashboard", layout="wide")
st.markdown(
    """
    <style>
      body { font-family: 'Inter', sans-serif; }
      .stMetric { border: 1px solid #111; padding: 12px; }
    </style>
    """,
    unsafe_allow_html=True,
)
st.title("§ Inter-Rater Agreement Dashboard")
st.caption(
    "Drag in two annotators' JSONL files. The disagreement table at the bottom "
    "tells you which items need clearer guidelines, not more annotators."
)


def load_jsonl(file) -> list[dict]:
    if file is None:
        return []
    text = file.read().decode("utf-8") if hasattr(file, "read") else file
    return [json.loads(line) for line in StringIO(text) if line.strip()]


col1, col2 = st.columns(2)
with col1:
    file_a = st.file_uploader("Annotator A (.jsonl)", type=["jsonl", "json"], key="a")
with col2:
    file_b = st.file_uploader("Annotator B (.jsonl)", type=["jsonl", "json"], key="b")

if not file_a or not file_b:
    st.info(
        "Need example data? See `data/sample/annotator_a.jsonl` and `annotator_b.jsonl`."
    )
    st.stop()

docs_a = load_jsonl(file_a)
docs_b = load_jsonl(file_b)
pairs = align_documents(docs_a, docs_b)

st.subheader("Corpus")
st.write(
    f"**{len(pairs)} aligned documents** between "
    f"`{docs_a[0].get('annotator', 'A')}` and `{docs_b[0].get('annotator', 'B')}`."
)

# --- Overall metrics ----------------------------------------------------------
seq_a: list[str] = []
seq_b: list[str] = []
all_pred: list[tuple[int, int, str]] = []
all_gold: list[tuple[int, int, str]] = []
for da, db in pairs:
    seq_a.extend(spans_to_token_labels(da["text"], da["spans"]))
    seq_b.extend(spans_to_token_labels(db["text"], db["spans"]))
    all_pred.extend((s["start"], s["end"], s["label"]) for s in da["spans"])
    all_gold.extend((s["start"], s["end"], s["label"]) for s in db["spans"])

kappa = cohens_kappa(seq_a, seq_b)
alpha = krippendorff_alpha([seq_a, seq_b])
f1 = span_f1(all_pred, all_gold)

st.subheader("Agreement")
m1, m2, m3, m4 = st.columns(4)
m1.metric("Cohen's κ", f"{kappa:.3f}")
m2.metric("Krippendorff's α", f"{alpha:.3f}")
m3.metric("Span F1", f"{f1['f1']:.3f}")
m4.metric("Spans (A / B)", f"{len(all_pred)} / {len(all_gold)}")

# --- Per-document --------------------------------------------------------------
st.subheader("Per-document agreement")
rows = []
for da, db in pairs:
    la = spans_to_token_labels(da["text"], da["spans"])
    lb = spans_to_token_labels(db["text"], db["spans"])
    rows.append(
        {
            "doc_id": da["doc_id"],
            "tokens": len(la),
            "spans_a": len(da["spans"]),
            "spans_b": len(db["spans"]),
            "kappa": round(cohens_kappa(la, lb), 3),
        }
    )
df = pd.DataFrame(rows).sort_values("kappa")
st.dataframe(df, use_container_width=True, hide_index=True)

# --- Disagreement detail -------------------------------------------------------
st.subheader("Span-level disagreements (where guidelines need help)")
all_disagree: list[dict] = []
for da, db in pairs:
    all_disagree.extend(find_disagreements(da, db))
if not all_disagree:
    st.success("No span-level disagreements. Either a calibrated team or a too-easy task.")
else:
    st.write(f"{len(all_disagree)} disagreement(s) across {len({d['doc_id'] for d in all_disagree})} document(s).")
    st.dataframe(pd.DataFrame(all_disagree), use_container_width=True, hide_index=True)
