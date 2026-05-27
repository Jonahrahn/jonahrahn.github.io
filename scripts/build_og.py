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
fig.text(0.05, 0.86, "E N G I N E E R I N G   L I N G U I S T   ·   S A N T A   C R U Z ,   C A",
         fontproperties=MONO, fontsize=14, color=MUTED)
# Top hairline
fig.add_artist(plt.Line2D([0.05, 0.95], [0.81, 0.81], color=INK, linewidth=1, transform=fig.transFigure))

# Draw "Jonah Rahn" then a rust dot to its right
title = fig.text(0.05, 0.46, "Jonah Rahn",
                 fontproperties=INTER, fontsize=110, color=INK, weight="bold")
# Position the dot using a transform-aware text after layout
fig.canvas.draw()
bbox = title.get_window_extent()
xinv, yinv = fig.transFigure.inverted().transform((bbox.x1, bbox.y0)).tolist()
fig.text(xinv + 0.005, 0.46, ".",
         fontproperties=INTER, fontsize=110, color=ACCENT, weight="bold")

fig.text(0.05, 0.28, "Bridging human language and machine intelligence.",
         fontproperties=INTER, fontsize=22, color=INK)
fig.text(0.05, 0.21, "Linguistics + ML model optimization @ LinkedIn.",
         fontproperties=INTER, fontsize=22, color=MUTED)

# Bottom hairline + URL
fig.add_artist(plt.Line2D([0.05, 0.95], [0.10, 0.10], color=INK, linewidth=1, transform=fig.transFigure))
fig.text(0.05, 0.05, "JONAHRAHN.GITHUB.IO", fontproperties=MONO, fontsize=13, color=INK)
fig.text(0.95, 0.05, "§ PORTFOLIO", fontproperties=MONO, fontsize=13, color=MUTED, ha="right")

fig.savefig("/home/user/jonahrahn.github.io/images/og-card.png", dpi=100, bbox_inches=None, pad_inches=0)
print("done")
