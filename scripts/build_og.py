"""Generate the Open Graph card (1200x630) in portfolio style.

Output: images/og-card.png (repo root relative)
"""
from pathlib import Path
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt

PAPER = "#fafaf7"
INK = "#111111"
MUTED = "#6b6b6b"

INTER_REG = Path("/usr/share/fonts/truetype/macos/Inter-Regular.ttf")
INTER_BOLD = Path("/usr/share/fonts/truetype/macos/Inter-Bold.ttf")
MONO_PATH = Path("/usr/share/fonts/truetype/jetbrains-mono/JetBrainsMono-Regular.ttf")

for path in (INTER_REG, INTER_BOLD, MONO_PATH):
    fm.fontManager.addfont(str(path))

INTER = fm.FontProperties(fname=INTER_REG)
INTER_B = fm.FontProperties(fname=INTER_BOLD)
MONO = fm.FontProperties(fname=MONO_PATH)

plt.rcParams.update({
    "figure.facecolor": PAPER,
    "savefig.facecolor": PAPER,
    "font.family": "sans-serif",
    "font.sans-serif": ["Inter"],
})

fig = plt.figure(figsize=(12, 6.3), dpi=100)
fig.text(
    0.05,
    0.86,
    "B A C K E N D   E N G I N E E R   ·   A I   E V A L U A T I O N   ·   O R A N G E   C O U N T Y ,   C A",
    fontproperties=MONO,
    fontsize=11,
    color=MUTED,
)
fig.add_artist(plt.Line2D([0.05, 0.95], [0.81, 0.81], color=INK, linewidth=1, transform=fig.transFigure))

fig.text(0.05, 0.46, "Jonah Rahn", fontproperties=INTER_B, fontsize=110, color=INK)

fig.text(
    0.05,
    0.28,
    "Backend engineer and AI evaluation specialist.",
    fontproperties=INTER,
    fontsize=22,
    color=INK,
)
fig.text(
    0.05,
    0.21,
    "Recently at Oasis Health · Open to next role.",
    fontproperties=INTER,
    fontsize=22,
    color=MUTED,
)

fig.add_artist(plt.Line2D([0.05, 0.95], [0.10, 0.10], color=INK, linewidth=1, transform=fig.transFigure))
fig.text(0.05, 0.05, "JONAHRAHN.GITHUB.IO", fontproperties=MONO, fontsize=13, color=INK)
fig.text(0.95, 0.05, "§ PORTFOLIO", fontproperties=MONO, fontsize=13, color=MUTED, ha="right")

OUT = Path(__file__).resolve().parents[1] / "images" / "og-card.png"
fig.savefig(OUT, dpi=100, bbox_inches=None, pad_inches=0)
print(f"done → {OUT}")
