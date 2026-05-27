# Data sources

Three corpora cover the language pairs in scope.

## SEAME (Mandarin–English, Singapore)

- **Source**: NTU & I²R, distributed by LDC as `LDC2015S04`
- **Access**: LDC membership or one-time fee; the corpus is not public
- **Code-switch annotation**: included
- **What we use**: the development and test partitions, ~10 hours

If you don't have LDC access, the analysis here can be replicated on the smaller open `ASCEND` corpus instead. Note results will differ; document the substitution.

## Bangor Miami (Spanish–English, US)

- **Source**: Bangor University, distributed via TalkBank
- **URL**: https://talkbank.org/access/Bilingual/Miami.html
- **License**: CC-BY-NC-SA 3.0
- **Code-switch annotation**: gloss-level, requires preprocessing into per-word language tags

```bash
mkdir -p data/bangor && cd data/bangor
wget https://media.talkbank.org/bilingual/Miami/0wma.zip
unzip 0wma.zip
```

## Tagalog–English (custom)

A small, scripted corpus collected for this analysis. Released under CC-BY-4.0 alongside the writeup.

- 3 hours of read speech
- 8 speakers, balanced for dominance (4 Tagalog-dominant, 4 English-dominant)
- Scripts designed to vary switch position, phonological distance, and direction
- Stored as `data/tgl-eng/*.wav` with per-clip `meta.json`

The collection protocol, consent form, and speaker demographics are in `data/tgl-eng/PROTOCOL.md`.

## Preparing audio

All audio is resampled to 16 kHz mono WAV:

```bash
for f in data/**/*.{mp3,wav,flac}; do
  out="${f%.*}.16k.wav"
  ffmpeg -hide_banner -loglevel error -i "$f" -ar 16000 -ac 1 -c:a pcm_s16le "$out"
done
```
