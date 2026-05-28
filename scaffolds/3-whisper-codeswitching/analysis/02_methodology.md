# 02 · Methodology

The high-level question is simple: **does Whisper degrade more at code-switch boundaries than elsewhere, and if so, can we predict where it will fail?**

To answer it cleanly, we need to control for a few things:

1. **Speaker.** Different speakers have different accents and switch styles. We pair switch-point errors against monolingual-stretch errors *within the same speaker*, not across speakers.
2. **Audio quality.** SEAME and Bangor Miami have different recording conditions. We normalize SNR within an acceptable range and drop clips below threshold rather than mixing levels.
3. **Switch type.** Inter-sentential ("I'm going. Yung asawa ko ay nandiyan.") is fundamentally different from intra-word morphological mixing ("nag-Zoom ako"). We score them separately.
4. **Reference quality.** Code-switched corpora have noisier gold transcripts than monolingual ones. We hand-verify the gold for the worst 100 utterances per corpus.

## Operationalization

For each utterance:

1. Compute Whisper hypothesis.
2. Force-align gold to audio using Montreal Forced Aligner with both monolingual acoustic models, then merge.
3. Project Whisper output onto gold word boundaries.
4. For each gold word, label:
   - Its language tag (`tgl`, `eng`, `mix` for intra-word)
   - Whether the immediately preceding word is in a different language (a "post-switch position")
   - Whether the immediately following word is in a different language (a "pre-switch position")
5. Compute per-word correctness (substitution / insertion / deletion / match).
6. Aggregate WER by switch-position bucket and by language pair.

## Buckets we report

| Bucket | Definition |
|--------|------------|
| `mono-L1` | Word and both neighbors in L1 |
| `mono-L2` | Word and both neighbors in L2 |
| `pre-switch` | Word is in L_x, next word is in L_y ≠ L_x |
| `post-switch` | Word is in L_x, previous word was in L_y ≠ L_x |
| `intra-word` | Morphological mixing (e.g., `nag-Zoom`) |

The headline number is `pre-switch WER / mono WER`, paired by speaker.

## Qualitative pass

For each bucket, we hand-code the 20 worst errors into types:

- **Phonetic confusion** — the word was misheard as a phonologically similar word in the other language
- **Language lock-in** — Whisper refused to switch language and produced a plausible-sounding hallucination in the previous language
- **Deletion** — the switch word is simply omitted from the hypothesis
- **Boundary smear** — the switch word is merged with its neighbor

That categorization is the real artifact. WER tells you something is wrong; the typology tells you *what*.

## Statistical reporting

- WER is a ratio, not a mean. We bootstrap 95% CIs over utterance-level resamples.
- For paired comparisons (pre-switch vs mono), we use a Wilcoxon signed-rank within speaker.
- We pre-register the analysis plan in the README so post-hoc explorations are clearly labeled.
