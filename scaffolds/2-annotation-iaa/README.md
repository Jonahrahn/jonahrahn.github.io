# Inter-Rater Agreement Dashboard

**A focused tool that turns two annotators' span-tagged files into a single, scannable picture of where they disagree, and why.**

Most teams compute Cohen's κ once and move on. The interesting question is *which spans cause the disagreement* — those are the items that need clearer guidelines, not more annotators.

## What it does

- Loads two (or more) span-annotated JSONL files in a standard schema.
- Computes pair-level agreement metrics: Cohen's κ, Krippendorff's α, span-level F1.
- Visualizes per-document agreement so it's obvious which texts caused the trouble.
- Highlights the exact span-level disagreements in context, with a one-click "promote to guideline question" button that copies a templated note to clipboard.
- Tracks agreement drift over time when you feed it multiple batches.

## Why this matters

The standard κ → meeting → revised guidelines loop loses information at every step. By the time the team meets, nobody remembers which sentence sparked the disagreement. This tool keeps the data and the metric in the same view.

## Live demo

[Deploy to Hugging Face Spaces / Streamlit Cloud and put the URL here.]

## Quickstart

```bash
pip install -r requirements.txt
streamlit run app.py
```

Then drag and drop the two sample annotation files in `data/sample/`.

## Annotation schema

One annotation per line, JSONL. Each annotation covers one document:

```json
{
  "doc_id": "doc-001",
  "text": "the full text of the document",
  "annotator": "anna",
  "spans": [
    {"start": 12, "end": 24, "label": "PERSON"},
    {"start": 45, "end": 60, "label": "ORG"}
  ]
}
```

`start` and `end` are character offsets (Python slice convention).

## What's in the box

| Module | Purpose |
|--------|---------|
| `iaa/metrics.py` | Cohen's κ, Krippendorff's α, span-level F1 |
| `iaa/span_utils.py` | Token-level alignment of two annotators' spans |
| `app.py` | Streamlit UI |

## Roadmap

- [ ] Active-learning ranking: surface the items where annotator confidence is lowest *and* model confidence is lowest.
- [ ] Guideline-aware suggestions: when a disagreement looks like a known edge case, link to the relevant guideline excerpt.
- [ ] Drift detection: alert when an annotator's label distribution shifts week-over-week.

## License

MIT.
