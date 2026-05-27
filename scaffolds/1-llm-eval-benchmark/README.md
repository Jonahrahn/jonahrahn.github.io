# Negation Scope Eval

**A benchmark for how current LLMs handle negation scope across natural-language reasoning tasks.**

Negation looks easy until it isn't. *"Not all swans are white"* means something very different from *"all swans are not white,"* even though the words barely change. This benchmark probes whether modern LLMs handle that distinction reliably, plus a dozen other linguistically-grounded negation patterns.

## Phenomena covered

| ID | Phenomenon | Example |
|----|------------|---------|
| `neg-scope-quantifier` | Scope of negation with quantifiers | *"Not all swans are white"* vs *"All swans are not white"* |
| `neg-scope-only` | Scope with focus particles | *"Only Mary didn't leave"* vs *"Mary didn't only leave"* |
| `neg-implicature` | Negation cancelling scalar implicature | *"I don't have three children — I have four"* |
| `neg-raising` | Neg-raising predicates | *"I don't think he came"* (= *I think he didn't come*) |
| `neg-double` | Double negation in negative concord vs standard English | *"I ain't got no money"* |
| `neg-rhetorical` | Rhetorical questions with negation | *"Who hasn't made that mistake?"* |
| `neg-presupp` | Negation under presupposition triggers | *"John stopped smoking" → "John didn't stop smoking"* |

Each phenomenon has 30–60 hand-crafted minimal pairs.

## Current leaderboard

| Model | Overall | scope-quant | scope-only | implicature | neg-raising | double | rhetorical | presupp |
|-------|---------|-------------|------------|-------------|-------------|--------|------------|---------|
| _Add results to_ `results/` | — | — | — | — | — | — | — | — |

Re-rendered from `results/*.jsonl` by `make leaderboard`.

## Methodology

Each item is a forced-choice between two paraphrases of a target sentence: one that preserves the intended meaning of the negation, one that flips it. The model is shown the target plus both candidates and asked which one preserves meaning. We score exact match against the gold label, then break results down by phenomenon and by paraphrase direction (to catch position-bias artifacts).

For ambiguous items (some negation phenomena have genuinely contested readings), we mark both candidates as acceptable and report a softer metric.

## How to run

```bash
pip install -r requirements.txt
export OPENAI_API_KEY=...        # or ANTHROPIC_API_KEY
python -m evals.run_openai --model gpt-4o --out results/gpt-4o.jsonl
python -m harness.score results/gpt-4o.jsonl
make leaderboard
```

## Adding a new phenomenon

1. Create `data/<phenomenon-id>.jsonl` with one item per line. Schema in `harness/types.py`.
2. Add a sentence-level rationale in `prompts/phenomena.md`.
3. Run `python -m harness.validate data/<phenomenon-id>.jsonl` to lint.

## Contributing

The benchmark is small on purpose. Quality of items matters more than quantity. PRs that add a single well-justified item are welcome.

## Citation

```
@misc{rahn2026negation,
  title  = {Negation Scope Eval: a linguistically-curated benchmark for LLM negation handling},
  author = {Rahn, Jonah},
  year   = {2026},
  url    = {https://github.com/Jonahrahn/negation-scope-eval}
}
```

## License

CC-BY-4.0 for the data; MIT for the code.
