"""Generate the Open Graph card (1200x630) in portfolio style.

Output: /home/user/jonahrahn.github.io/images/og-card.png
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

fig = plt.figure(figsize=(12, 6.3), dpi=100)
fig.text(0.05, 0.86, "B A C K E N D   E N G I N E E R   ·   A I   E V A L U A T I O N   ·   N E W   H A V E N ,   C T",
         fontproperties=MONO, fontsize=12, color=MUTED)
# Top hairline
fig.add_artist(plt.Line2D([0.05, 0.95], [0.81, 0.81], color=INK, linewidth=1, transform=fig.transFigure))

fig.text(0.05, 0.46, "Jonah Rahn",
         fontproperties=INTER, fontsize=110, color=INK, weight="bold")

fig.text(0.05, 0.28, "Backend engineer and AI evaluation specialist.",
         fontproperties=INTER, fontsize=22, color=INK)
fig.text(0.05, 0.21, "Building production systems at Oasis Health.",
         fontproperties=INTER, fontsize=22, color=MUTED)

# Bottom hairline + URL
fig.add_artist(plt.Line2D([0.05, 0.95], [0.10, 0.10], color=INK, linewidth=1, transform=fig.transFigure))
fig.text(0.05, 0.05, "JONAHRAHN.GITHUB.IO", fontproperties=MONO, fontsize=13, color=INK)
fig.text(0.95, 0.05, "§ PORTFOLIO", fontproperties=MONO, fontsize=13, color=MUTED, ha="right")

fig.savefig("/home/user/jonahrahn.github.io/images/og-card.png", dpi=100, bbox_inches=None, pad_inches=0)
print("done")
