# Whisper on Code-Switched Speech

**A linguistically-rigorous look at where OpenAI's Whisper degrades when speakers switch between languages mid-utterance, and why.**

Code-switching — when bilingual speakers move between languages within a single conversation, often within a single sentence — is the norm in many speech communities. Production ASR systems mostly pretend it doesn't exist. This is a focused failure analysis of Whisper (`large-v3`) on three code-switching pairs: Tagalog–English, Spanish–English, and Mandarin–English.

## TL;DR

> *(One sentence with the headline finding, written after running the analysis. Placeholder while the data is being collected.)*

## Why this matters

The biggest deployed ASR systems are trained on monolingual or near-monolingual corpora. Bilingual users hit a quality cliff the moment they switch. That cliff has structure: it depends on the syntactic position of the switch, the phonological distance between the two languages, and which language carries the function words. Mapping that structure is the kind of analysis that informs both data collection and model design.

## Methodology

### Data

| Source | Pair | Audio | License |
|--------|------|-------|---------|
| SEAME | Mandarin–English (Singapore) | ~192 hours | LDC2015S04, restricted |
| Bangor Miami | Spanish–English | ~35 hours conversation | Open via Bangor TalkBank |
| Custom collection | Tagalog–English | ~3 hours, scripted | Released alongside the analysis |

Switch points are pre-annotated in the SEAME and Bangor corpora and re-checked by ear. For the custom Tagalog–English subset, scripts are designed to vary:

- **Switch position** (matrix-language function word vs lexical word)
- **Phonological similarity** (cognates vs non-cognates at the switch)
- **Switch direction** (Tagalog → English vs English → Tagalog)

### Pipeline

1. Run Whisper `large-v3` on each clip, no language hint.
2. Run again with language hint forced to the matrix language.
3. Compute Word Error Rate (WER), broken down by:
   - Whether the error word is at a switch boundary or within a monolingual stretch
   - The "type" of switch (inter-sentential, intra-sentential, intra-word)
   - The direction of the switch
4. Sample 20 worst errors per category and transcribe them by hand for a qualitative pass.

### Metrics

- **Switch-point WER** vs **monolingual-stretch WER**, paired by speaker
- **Phoneme deletion rate** at switch boundaries (was the word skipped, or replaced?)
- **Language-detection latency**: how many words after a switch does Whisper "notice" and adjust its conditioning?

## Repository layout

```
analysis/
  01_setup.md            Environment + data acquisition notes
  02_methodology.md      The protocol above, formalized
  03_findings.md         The write-up, with figures
notebooks/
  10_run_whisper.ipynb   Inference loop, batched
  20_align_and_wer.ipynb Alignment + per-bucket WER
  30_qualitative.ipynb   Hand-coded error typology
data/
  README.md              How to obtain each corpus
figures/
  (generated)
```

## How to reproduce

```bash
pip install -r requirements.txt
# Acquire each corpus per data/README.md
python -m analysis.run_whisper --corpus seame --out results/seame.jsonl
python -m analysis.align_and_wer results/seame.jsonl
```

## What I expect to find (pre-registration)

Three hypotheses, written before running anything, so the post-hoc reader can hold me honest:

1. **Switch-point WER will be at least 3x monolingual WER**, even when both languages are well-represented in Whisper's training data.
2. **Phonologically similar switches (cognates) will be easier**, because the model can hedge on the language ID.
3. **Switches into the dominant pretraining language (English) will be easier** than switches out, regardless of speaker dominance.

## Citation

```
@misc{rahn2026whisper,
  title  = {Where Whisper degrades on code-switched speech: a linguistic teardown},
  author = {Rahn, Jonah},
  year   = {2026},
  url    = {https://github.com/Jonahrahn/whisper-codeswitching}
}
```

## License

MIT for code. Each audio corpus inherits its source license; see `data/README.md`.
