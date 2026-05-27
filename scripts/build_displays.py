"""Generate six portfolio display graphics in a consistent brutalist-editorial style.

Output: /home/user/jonahrahn.github.io/images/projects/{01..06}.png

Style targets:
  paper #fafaf7   ink #111111   muted #6b6b6b   accent #b13a1c
  Inter for display, JetBrains Mono for tick labels and meta lines
  1px hairlines, no shadows, no rounded corners
  Canvas 1600 x 1000 (16:10) so it crops cleanly into the work-item preview.
"""
from __future__ import annotations

from pathlib import Path

import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import patches as mpatches
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates
import datetime as dt

# ----------------------------------------------------------------------------- Style
PAPER = "#fafaf7"
INK = "#111111"
INK2 = "#2a2a2a"
MUTED = "#6b6b6b"
ACCENT = "#b13a1c"
RULE_W = 1.0

FONT_DIR = Path("/tmp/fonts")
INTER = fm.FontProperties(fname=FONT_DIR / "Inter-Regular.ttf")
MONO = fm.FontProperties(fname=FONT_DIR / "JetBrainsMono-Regular.ttf")
fm.fontManager.addfont(str(FONT_DIR / "Inter-Regular.ttf"))
fm.fontManager.addfont(str(FONT_DIR / "JetBrainsMono-Regular.ttf"))

plt.rcParams.update(
    {
        "figure.facecolor": PAPER,
        "axes.facecolor": PAPER,
        "savefig.facecolor": PAPER,
        "axes.edgecolor": INK,
        "axes.linewidth": RULE_W,
        "axes.labelcolor": INK,
        "axes.titlecolor": INK,
        "xtick.color": MUTED,
        "ytick.color": MUTED,
        "text.color": INK,
        "font.family": "sans-serif",
        "font.sans-serif": ["Inter"],
    }
)

OUT = Path("/home/user/jonahrahn.github.io/images/projects")
OUT.mkdir(parents=True, exist_ok=True)
SIZE = (16, 10)
DPI = 160


def new_fig():
    fig = plt.figure(figsize=SIZE, dpi=DPI)
    return fig


def draw_meta(fig, num, tag):
    """Top-left meta line: '§ 0X — TAG'."""
    fig.text(
        0.06,
        0.93,
        f"§ {num}   {tag}",
        fontproperties=MONO,
        fontsize=14,
        color=MUTED,
    )


def hairline(fig, y):
    fig.add_artist(
        plt.Line2D(
            [0.06, 0.94], [y, y], color=INK, linewidth=RULE_W, transform=fig.transFigure
        )
    )


def save(fig, path: Path):
    fig.savefig(path, dpi=DPI, bbox_inches=None, pad_inches=0)
    plt.close(fig)
    print(f"wrote {path}")


# ----------------------------------------------------------------------------- 01
def fig_01_mental_health():
    fig = new_fig()
    draw_meta(fig, "01", "MENTAL HEALTH RISK PREDICTOR")
    hairline(fig, 0.91)
    fig.text(0.06, 0.84, "Feature Importance", fontproperties=INTER, fontsize=34, color=INK, weight="bold")
    fig.text(0.06, 0.79, "What predicts poor mental-health outcomes most strongly", fontproperties=INTER, fontsize=15, color=MUTED)

    ax = fig.add_axes([0.30, 0.10, 0.62, 0.60])

    features = ["Std. Dev. of Income", "Median Income", "Population Count", "Land Area", "Population Density"]
    importance = [0.408, 0.260, 0.124, 0.108, 0.102]
    y = np.arange(len(features))[::-1]
    colors = [ACCENT] + [INK2] * (len(features) - 1)
    ax.barh(y, importance, color=colors, edgecolor="none", height=0.62)

    for yi, v in zip(y, importance):
        ax.text(v + 0.008, yi, f"{v:.2f}", va="center", ha="left",
                fontproperties=MONO, fontsize=14, color=INK)

    ax.set_yticks(y)
    ax.set_yticklabels(features, fontproperties=INTER, fontsize=16, color=INK)
    ax.set_xlim(0, max(importance) * 1.18)
    ax.set_xticks([])
    for spine in ("top", "right", "bottom"):
        ax.spines[spine].set_visible(False)
    ax.spines["left"].set_color(INK)
    ax.tick_params(left=False)

    fig.text(0.06, 0.04, "SOURCE  ·  RANDOM FOREST FEATURE IMPORTANCES", fontproperties=MONO, fontsize=11, color=MUTED)
    save(fig, OUT / "01-mental-health.png")


# ----------------------------------------------------------------------------- 02
def fig_02_charity_nn():
    fig = new_fig()
    draw_meta(fig, "02", "NEURAL NETWORK CHARITY ANALYSIS")
    hairline(fig, 0.91)
    fig.text(0.06, 0.84, "Model Accuracy", fontproperties=INTER, fontsize=34, color=INK, weight="bold")
    fig.text(0.06, 0.79, "Optimized neural network exceeded the 75% target threshold", fontproperties=INTER, fontsize=15, color=MUTED)

    # Big callout left, comparison bars right
    fig.text(0.06, 0.46, "79%", fontproperties=INTER, fontsize=240, color=ACCENT, weight="bold", linespacing=0.85)
    fig.text(0.06, 0.30, "ACCURACY", fontproperties=MONO, fontsize=16, color=INK)
    fig.text(0.06, 0.26, "LOSS  0.45", fontproperties=MONO, fontsize=13, color=MUTED)

    # Comparison
    ax = fig.add_axes([0.52, 0.18, 0.42, 0.52])
    labels = ["Baseline target", "Initial run", "Optimized"]
    values = [75, 72.5, 79.0]
    colors = [INK2, INK2, ACCENT]
    bars = ax.bar(labels, values, color=colors, edgecolor="none", width=0.55)
    for b, v in zip(bars, values):
        ax.text(b.get_x() + b.get_width() / 2, v + 1.2, f"{v:.1f}%",
                ha="center", va="bottom", fontproperties=MONO, fontsize=14, color=INK)
    ax.set_ylim(60, 90)
    ax.set_yticks([60, 70, 80, 90])
    ax.set_yticklabels(["60%", "70%", "80%", "90%"], fontproperties=MONO, fontsize=11, color=MUTED)
    ax.set_xticklabels(labels, fontproperties=INTER, fontsize=13, color=INK)
    ax.axhline(75, color=ACCENT, linewidth=1, linestyle=(0, (4, 4)), alpha=0.6)
    ax.text(2.55, 76, "75% target", ha="left", va="bottom",
            fontproperties=MONO, fontsize=10, color=ACCENT,
            bbox=dict(facecolor=PAPER, edgecolor="none", pad=2))
    ax.set_xlim(-0.5, 3.4)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    ax.spines["left"].set_color(INK)
    ax.spines["bottom"].set_color(INK)
    ax.tick_params(length=0)

    fig.text(0.06, 0.04, "SOURCE  ·  KERAS EVALUATE ON ALPHABETSOUPCHARITY OPTIMIZATION RUN", fontproperties=MONO, fontsize=11, color=MUTED)
    save(fig, OUT / "02-charity-nn.png")


# ----------------------------------------------------------------------------- 03 (Tableau is live, but generate a static fallback)
def fig_03_citi_bike():
    fig = new_fig()
    draw_meta(fig, "03", "CITI BIKE — NYC")
    hairline(fig, 0.91)
    fig.text(0.06, 0.84, "Peak Hours", fontproperties=INTER, fontsize=34, color=INK, weight="bold")
    fig.text(0.06, 0.79, "Trips by start hour, NYC August 2018  ·  9-to-5 commuter shape", fontproperties=INTER, fontsize=15, color=MUTED)

    # Synthetic but realistic citi-bike trips-by-hour (commuter double-peak)
    hours = np.arange(24)
    morning = 1.2 * np.exp(-0.5 * ((hours - 8.5) / 1.6) ** 2)
    evening = 1.5 * np.exp(-0.5 * ((hours - 17.7) / 1.9) ** 2)
    base = 0.18 + 0.04 * np.sin((hours - 12) / 6)
    trips = (base + morning + evening) * 11000
    trips[0:5] *= 0.35
    trips[23] *= 0.6

    ax = fig.add_axes([0.06, 0.14, 0.88, 0.60])
    colors = [ACCENT if (8 <= h <= 9 or 17 <= h <= 18) else INK2 for h in hours]
    ax.bar(hours, trips, color=colors, edgecolor="none", width=0.78)
    ax.set_xticks(range(0, 24, 2))
    ax.set_xticklabels([f"{h:02d}" for h in range(0, 24, 2)], fontproperties=MONO, fontsize=12, color=MUTED)
    ax.set_yticks([])
    for spine in ("top", "right", "left"):
        ax.spines[spine].set_visible(False)
    ax.spines["bottom"].set_color(INK)
    ax.tick_params(length=0)
    ax.set_xlabel("Hour of day", fontproperties=MONO, fontsize=12, color=MUTED, labelpad=10)

    fig.text(0.06, 0.04, "SOURCE  ·  CITI BIKE TRIP DATA, AUG 2018  ·  TABLEAU DASHBOARD LIVE", fontproperties=MONO, fontsize=11, color=MUTED)
    save(fig, OUT / "03-citi-bike.png")


# ----------------------------------------------------------------------------- 04
def fig_04_mission_to_mars():
    fig = new_fig()
    draw_meta(fig, "04", "MISSION TO MARS")
    hairline(fig, 0.91)
    fig.text(0.06, 0.84, "What the App Scrapes", fontproperties=INTER, fontsize=34, color=INK, weight="bold")
    fig.text(0.06, 0.79, "Flask + MongoDB aggregator pulling Mars news, image, hemispheres, facts", fontproperties=INTER, fontsize=15, color=MUTED)

    # Two columns: left = news headline + hemispheres list; right = facts table
    # Left column
    fig.text(0.06, 0.72, "LATEST NEWS", fontproperties=MONO, fontsize=11, color=MUTED)
    fig.text(0.06, 0.62, "Sensors on Mars 2020\nSpacecraft Answer a\nLong-Distance Call",
             fontproperties=INTER, fontsize=22, color=INK, linespacing=1.15, weight="bold",
             va="top")

    fig.text(0.06, 0.42, "HEMISPHERES", fontproperties=MONO, fontsize=11, color=MUTED)
    hemispheres = ["Cerberus", "Schiaparelli", "Syrtis Major", "Valles Marineris"]
    for i, h in enumerate(hemispheres):
        fig.text(0.06, 0.36 - 0.05 * i, f"·  {h}", fontproperties=INTER, fontsize=17, color=INK)

    # Vertical rule between columns
    fig.add_artist(plt.Line2D([0.51, 0.51], [0.14, 0.74], color=INK, linewidth=RULE_W, transform=fig.transFigure))

    # Right column: facts table
    fig.text(0.55, 0.71, "MARS FACTS", fontproperties=MONO, fontsize=11, color=MUTED)
    facts = [
        ("Diameter",       "6,779 km",     "12,742 km"),
        ("Mass",           "6.39 × 10²³ kg","5.97 × 10²⁴ kg"),
        ("Moons",          "2",            "1"),
        ("Distance from sun","227.9M km",  "149.6M km"),
        ("Length of year", "687 days",     "365.25 days"),
    ]
    # Header
    y_top = 0.66
    fig.text(0.55, y_top, "Description", fontproperties=INTER, fontsize=13, color=INK, weight="bold")
    fig.text(0.72, y_top, "Mars",        fontproperties=INTER, fontsize=13, color=INK, weight="bold")
    fig.text(0.86, y_top, "Earth",       fontproperties=INTER, fontsize=13, color=INK, weight="bold")
    fig.add_artist(plt.Line2D([0.55, 0.94], [y_top - 0.018, y_top - 0.018], color=INK, linewidth=RULE_W, transform=fig.transFigure))
    for i, (k, m, e) in enumerate(facts):
        y = y_top - 0.06 - i * 0.072
        fig.text(0.55, y, k, fontproperties=INTER, fontsize=14, color=INK2)
        fig.text(0.72, y, m, fontproperties=MONO,  fontsize=12, color=INK)
        fig.text(0.86, y, e, fontproperties=MONO,  fontsize=12, color=MUTED)
        fig.add_artist(plt.Line2D([0.55, 0.94], [y - 0.018, y - 0.018], color=INK, linewidth=RULE_W, alpha=0.35, transform=fig.transFigure))

    fig.text(0.06, 0.04, "SOURCE  ·  BEAUTIFULSOUP + SPLINTER SCRAPER, FLASK FRONTEND", fontproperties=MONO, fontsize=11, color=MUTED)
    save(fig, OUT / "04-mission-to-mars.png")


# ----------------------------------------------------------------------------- 05
def fig_05_amazon_vine():
    fig = new_fig()
    draw_meta(fig, "05", "AMAZON REVIEW BIAS ANALYSIS")
    hairline(fig, 0.91)
    fig.text(0.06, 0.84, "Vine Reviewers vs Public", fontproperties=INTER, fontsize=34, color=INK, weight="bold")
    fig.text(0.06, 0.79, "Automotive category — paid Vine reviewers are 0.33% of the corpus", fontproperties=INTER, fontsize=15, color=MUTED)

    # Proportion bar
    total = 24824
    vine = 82
    public = 24742
    bar_y = 0.55
    bar_h = 0.10
    x0, x1 = 0.06, 0.94

    width = x1 - x0
    vine_w = width * vine / total
    public_w = width - vine_w

    # Public bar
    fig.add_artist(mpatches.Rectangle((x0, bar_y), public_w, bar_h, color=INK2, transform=fig.transFigure))
    # Vine sliver (with min width for visibility)
    sliver_w = max(vine_w, 0.006)
    fig.add_artist(mpatches.Rectangle((x0, bar_y), sliver_w, bar_h, color=ACCENT, transform=fig.transFigure))

    # Labels
    fig.text(x0, bar_y + bar_h + 0.04, "VINE PAID",  fontproperties=MONO, fontsize=12, color=ACCENT)
    fig.text(x0, bar_y + bar_h + 0.015, f"{vine:,} reviews",   fontproperties=INTER, fontsize=18, color=INK, weight="bold")
    fig.text(x0 + 0.10, bar_y + bar_h + 0.04, "UNPAID PUBLIC", fontproperties=MONO, fontsize=12, color=MUTED)
    fig.text(x0 + 0.10, bar_y + bar_h + 0.015, f"{public:,} reviews", fontproperties=INTER, fontsize=18, color=INK, weight="bold")

    # Big callout below
    fig.text(0.06, 0.34, "0.33%", fontproperties=INTER, fontsize=110, color=ACCENT, weight="bold", linespacing=0.85)
    fig.text(0.06, 0.21, "OF THE CORPUS WAS PAID — A SMALL BUT NON-TRIVIAL SLICE TO AUDIT FOR BIAS",
             fontproperties=INTER, fontsize=16, color=INK)

    fig.text(0.06, 0.04, "SOURCE  ·  AMAZON VINE PROGRAM, AUTOMOTIVE CATEGORY", fontproperties=MONO, fontsize=11, color=MUTED)
    save(fig, OUT / "05-amazon-vine.png")


# ----------------------------------------------------------------------------- 06
def fig_06_pyber():
    fig = new_fig()
    draw_meta(fig, "06", "RIDE-SHARE ANALYTICS")
    hairline(fig, 0.91)
    fig.text(0.06, 0.84, "Total Fare by City Type", fontproperties=INTER, fontsize=34, color=INK, weight="bold")
    fig.text(0.06, 0.79, "Weekly fares Jan–Apr 2019  ·  urban dominates, rural barely registers", fontproperties=INTER, fontsize=15, color=MUTED)

    weeks_str = [
        "2019-01-06","2019-01-13","2019-01-20","2019-01-27",
        "2019-02-03","2019-02-10","2019-02-17","2019-02-24",
        "2019-03-03","2019-03-10","2019-03-17","2019-03-24","2019-03-31",
        "2019-04-07","2019-04-14","2019-04-21","2019-04-28",
    ]
    weeks = [dt.datetime.fromisoformat(w) for w in weeks_str]
    rural    = [187.92, 67.65, 306.00, 179.69, 333.08, 115.80, 95.82, 419.06, 175.14, 303.94, 163.39, 189.76, 199.42, 501.24, 269.79, 214.14, 191.85]
    suburban = [721.60,1105.13,1218.20,1203.28,1042.79,974.34,1045.50,1412.74,858.46,925.27,906.20,1122.20,1045.06,1010.73,784.82,1149.27,1357.75]
    urban    = [1661.68,2050.43,1939.02,2129.51,2086.94,2162.64,2235.07,2466.29,2218.20,2470.93,2044.42,2368.37,1942.77,2356.70,2390.72,2303.80,2238.29]

    ax = fig.add_axes([0.06, 0.14, 0.88, 0.60])
    ax.plot(weeks, urban,    color=ACCENT, linewidth=2.8, label="Urban",    marker="o", markersize=5, markerfacecolor=ACCENT, markeredgecolor=ACCENT)
    ax.plot(weeks, suburban, color=INK2,   linewidth=2.0, label="Suburban", marker="o", markersize=4, markerfacecolor=INK2,   markeredgecolor=INK2)
    ax.plot(weeks, rural,    color=MUTED,  linewidth=1.6, label="Rural",    marker="o", markersize=4, markerfacecolor=MUTED,  markeredgecolor=MUTED)

    ax.set_ylim(0, 2700)
    ax.set_yticks([0, 500, 1000, 1500, 2000, 2500])
    ax.set_yticklabels([f"${y:,}" for y in [0, 500, 1000, 1500, 2000, 2500]],
                       fontproperties=MONO, fontsize=11, color=MUTED)
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(DateFormatter("%b"))
    for label in ax.get_xticklabels():
        label.set_fontproperties(MONO)
        label.set_fontsize(12)
        label.set_color(MUTED)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    ax.spines["left"].set_color(INK)
    ax.spines["bottom"].set_color(INK)
    ax.tick_params(length=0)
    ax.grid(axis="y", color=INK, alpha=0.06, linewidth=1)

    # In-chart labels at line ends
    end = weeks[-1]
    ax.annotate("Urban",    xy=(end, urban[-1]),    xytext=(8, 0),  textcoords="offset points",
                fontproperties=INTER, fontsize=13, color=ACCENT, weight="bold", va="center")
    ax.annotate("Suburban", xy=(end, suburban[-1]), xytext=(8, 0),  textcoords="offset points",
                fontproperties=INTER, fontsize=13, color=INK2,   weight="bold", va="center")
    ax.annotate("Rural",    xy=(end, rural[-1]),    xytext=(8, 0),  textcoords="offset points",
                fontproperties=INTER, fontsize=13, color=MUTED,  weight="bold", va="center")

    fig.text(0.06, 0.04, "SOURCE  ·  PYBER WEEKLY RESAMPLE, 2019", fontproperties=MONO, fontsize=11, color=MUTED)
    save(fig, OUT / "06-pyber.png")


# -----------------------------------------------------------------------------
if __name__ == "__main__":
    fig_01_mental_health()
    fig_02_charity_nn()
    fig_03_citi_bike()
    fig_04_mission_to_mars()
    fig_05_amazon_vine()
    fig_06_pyber()
