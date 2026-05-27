# Portfolio scaffolds

Three project starting-points, ordered by ROI for an Engineering Linguist role. Each is structured so the README is the artifact a recruiter sees first; the code is the proof-of-work.

## How to use these

Each subdirectory is a self-contained project. To start one:

```bash
# Copy out of this repo into its own
cp -r scaffolds/1-llm-eval-benchmark ../negation-scope-eval
cd ../negation-scope-eval
git init && git add . && git commit -m "Initial scaffold"
gh repo create negation-scope-eval --public --source=. --push
```

Then follow the `NEXT_STEPS.md` (where present) inside each scaffold.

## The three projects

### 1. [LLM evaluation benchmark](./1-llm-eval-benchmark/)

A curated forced-choice benchmark probing how well current LLMs handle a specific linguistic phenomenon (negation scope, in the scaffold; swap in whatever phenomenon you have strongest opinions on).

**Why it matters:** demonstrates evaluation craft + linguistics depth in one artifact. Updating the leaderboard when new models drop is a free recurring blog post.

**Effort:** 1–2 focused weeks for an initial release.

**Deliverable:** GitHub repo with data, harness, and a self-updating leaderboard.

---

### 2. [Annotation IAA dashboard](./2-annotation-iaa/)

A Streamlit app that turns two annotators' span-tagged JSONL files into a single scannable picture of agreement, with the actual disagreements highlighted in context.

**Why it matters:** this is the day-job of an Engineering Linguist made visible. Hiring managers see it and immediately know what role to slot you into.

**Effort:** 2–4 weeks to ship a polished version.

**Deliverable:** A live Streamlit URL plus the open-source repo.

---

### 3. [Whisper code-switching teardown](./3-whisper-codeswitching/)

A linguistically-rigorous failure analysis of OpenAI's Whisper on code-switched speech across three language pairs (Tagalog-English, Spanish-English, Mandarin-English).

**Why it matters:** the meta-skill of evaluating ML systems linguistically. This is what big-tech engineering linguists do all day, made into a public artifact.

**Effort:** 1–2 weeks (data acquisition is the long pole).

**Deliverable:** GitHub repo with notebooks, plus a long-form writeup linked from your portfolio.

---

## Common patterns across all three

Each scaffold is structured around the same recruiter-scannable shape:

1. **One-sentence pitch** at the top of the README.
2. **Methodology before results.** Shows rigor without needing the results to be in yet.
3. **A reproducibility-first quickstart**. `pip install -r requirements.txt && one command` runs the demo.
4. **A clear "next steps" section** so the work-in-progress state still reads as intentional, not abandoned.

## Recommended order

If you only ship one, ship #1. It's the highest leverage per hour, the most publishable, and the most current-sounding artifact. Once it's up, #3 is the next easiest because it reuses the evaluation-discipline mindset.
