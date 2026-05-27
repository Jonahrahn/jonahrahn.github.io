"""Generate one OG card per case study under images/og/.

Each card matches the editorial system: paper bg, ink type, rust accent,
JetBrains Mono meta strip, Inter big title, project headline finding below.
"""
from pathlib import Path
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt

PAPER = "#fafaf7"
INK = "#111111"
MUTED = "#6b6b6b"
ACCENT = "#b13a1c"

FONT_DIR = Path("/tmp/fonts")
INTER = fm.FontProperties(fname=FONT_DIR / "Inter-Regular.ttf")
MONO = fm.FontProperties(fname=FONT_DIR / "JetBrainsMono-Regular.ttf")
fm.fontManager.addfont(str(FONT_DIR / "Inter-Regular.ttf"))
fm.fontManager.addfont(str(FONT_DIR / "JetBrainsMono-Regular.ttf"))

plt.rcParams.update({
    "figure.facecolor": PAPER,
    "savefig.facecolor": PAPER,
    "font.family": "sans-serif",
    "font.sans-serif": ["Inter"],
})

OUT = Path("/home/user/jonahrahn.github.io/images/og")
OUT.mkdir(parents=True, exist_ok=True)

CASES = [
    ("citi-bike",         "01", "CITI BIKE TABLEAU",                "Citi Bike",                "Twin commuter peaks tell the whole story."),
    ("mental-health",     "02", "MENTAL HEALTH RISK PREDICTOR",     "Mental Health",            "Income inequality, not income level."),
    ("charity-nn",        "03", "NEURAL NETWORK CHARITY ANALYSIS",  "Charity NN",               "Optimized run hit 79%, past the 75% target."),
    ("mission-to-mars",   "04", "MISSION TO MARS",                  "Mission to Mars",          "Flask + Mongo aggregator for Mars-mission data."),
    ("amazon-vine",       "05", "AMAZON REVIEW BIAS ANALYSIS",      "Vine Bias Analysis",       "Vine reviewers are 0.33% of the corpus."),
    ("pyber",             "06", "RIDE-SHARE ANALYTICS",             "Ride-Share Analytics",     "Urban dominates. Suburban steady. Rural minimal."),
]

for slug, num, header, big, sub in CASES:
    fig = plt.figure(figsize=(12, 6.3), dpi=100)
    # eyebrow / meta strip
    fig.text(0.05, 0.86, f"§ {num}    {header}", fontproperties=MONO, fontsize=14, color=MUTED)
    fig.add_artist(plt.Line2D([0.05, 0.95], [0.81, 0.81], color=INK, linewidth=1, transform=fig.transFigure))

    # Big title
    fig.text(0.05, 0.52, big, fontproperties=INTER, fontsize=88, color=INK, weight="bold")

    # Sub line (the finding)
    fig.text(0.05, 0.30, sub, fontproperties=INTER, fontsize=24, color=INK)

    # Bottom strip
    fig.add_artist(plt.Line2D([0.05, 0.95], [0.16, 0.16], color=INK, linewidth=1, transform=fig.transFigure))
    fig.text(0.05, 0.08, "JONAHRAHN.GITHUB.IO  ·  CASE STUDY", fontproperties=MONO, fontsize=12, color=INK)
    fig.text(0.95, 0.08, "§ J.R.", fontproperties=MONO, fontsize=12, color=ACCENT, ha="right")

    path = OUT / f"{slug}.png"
    fig.savefig(path, dpi=100, bbox_inches=None, pad_inches=0)
    plt.close(fig)
    print(f"wrote {path}")
