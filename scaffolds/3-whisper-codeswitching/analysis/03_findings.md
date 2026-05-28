# 03 · Findings

*(Placeholder. Write this section after running the analysis. Below is the structure to fill in.)*

## Headline

> *One sentence with the most important quantitative finding.*

![Figure 1: Pre-switch WER vs monolingual WER, paired by speaker](../figures/fig01-paired-wer.png)

## 1. WER at switch boundaries is X times higher than in monolingual stretches

| Bucket | Tagalog–English | Spanish–English | Mandarin–English |
|--------|----------------|-----------------|------------------|
| `mono-L1` | _xx.x%_ | _xx.x%_ | _xx.x%_ |
| `mono-L2` | _xx.x%_ | _xx.x%_ | _xx.x%_ |
| `pre-switch` | _xx.x%_ | _xx.x%_ | _xx.x%_ |
| `post-switch` | _xx.x%_ | _xx.x%_ | _xx.x%_ |
| `intra-word` | _xx.x%_ | _xx.x%_ | _xx.x%_ |

*(Add the bootstrap 95% CIs in the actual write-up.)*

## 2. The most common failure mode is "language lock-in"

When Whisper has spent the last several seconds emitting one language, it tends to refuse to switch. Examples:

- *"yung new phone mo kanina"* → Whisper: *"yung new phone mocha mina"*
  - "mo kanina" gets parsed as English-sounding nonsense rather than Tagalog.

*(Add 4–6 more transcribed examples per language pair.)*

## 3. Phonological distance predicts switch-point WER

We hypothesized cognates (`computer / kompyuter`) would be easier than non-cognates because the language identity is ambiguous and the model can hedge. The data shows _support / no support / partial support_ for this.

![Figure 2: Switch-point WER as a function of phoneme edit distance between languages](../figures/fig02-phoneme-distance.png)

## 4. Direction matters

Switching *into* English from a non-English language is easier than the reverse. *(Quantify, then explain — is it because English is overrepresented in the training data, or because the switch itself is acoustically easier?)*

## What this means for practitioners

1. **If your bilingual users are switching, force the language hint to be the more frequent of the two.** Auto-detect is unreliable at switch boundaries.
2. **Expect a quality cliff at the first few words after a switch.** Whisper takes context windows to "notice" and re-calibrate. Post-process: re-decode the segment with the alternate language hint and pick whichever has higher confidence.
3. **Intra-word mixing is currently a lost cause.** Re-transcribe by hand or use a code-switching-aware model.

## Limitations

- Sample sizes for the custom Tagalog corpus are small (3 hours).
- Forced alignment is imperfect at switch boundaries; some "Whisper errors" may be alignment artifacts.
- Whisper updates frequently; results are tied to `large-v3` snapshot YYYY-MM-DD.

## What I'd do with more time

- Run the same protocol on `large-v3-turbo` and `seamless-m4t-v2-large`.
- Test whether prompt engineering (passing the user's known language pair) closes the gap.
- Train a tiny classifier on `pre-switch position + acoustic features` to predict which segments need a re-decode.
