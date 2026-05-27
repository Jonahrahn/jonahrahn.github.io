"""Generate six case-study HTML pages under work/ from a shared template."""
from pathlib import Path
from textwrap import dedent

ROOT = Path("/home/user/jonahrahn.github.io")
OUT = ROOT / "work"
OUT.mkdir(exist_ok=True)

CASES = [
    {
        "slug": "citi-bike",
        "num": "01",
        "title": "Citi Bike Tableau Visualization",
        "tagline": "Surfacing who rides when, where, and how, across one month of NYC trip data.",
        "year": "2021",
        "role": "Data analyst / Designer",
        "stack": "Python · Tableau · Pandas",
        "image": "../images/projects/03-citi-bike.png",
        "image_alt": "Citi Bike trip volume by start hour, showing twin commuter peaks at 8am and 5pm",
        "live": ("Open in Tableau", "https://public.tableau.com/app/profile/jonah.rahn/viz/NYCBIke/NYCCitiBike"),
        "code": ("View code on GitHub", "https://github.com/Jonahrahn/BikeSharing"),
        "problem": (
            "Citi Bike publishes detailed trip data but no one had pulled August 2018 "
            "into a single, scannable picture for stakeholders. The brief: turn that month "
            "into a dashboard a non-analyst could read in 30 seconds."
        ),
        "approach": (
            "Cleaned the raw trip CSVs in Python to fix datatypes and shape, then built a "
            "six-tab Tableau Public dashboard covering trip duration, peak hours, "
            "user-type mix, and gender-segmented usage heatmaps."
        ),
        "result": (
            "Twin commuter peaks at 8 to 9am and 5 to 6pm; subscribers dominating over "
            "casual users; clear differences in trip duration between user segments. "
            "The dashboard is published on Tableau Public and embedded live on the home page."
        ),
        "prev": ("Earlier projects", "../#earlier"),
        "next": ("Mental Health Risk Predictor", "mental-health.html"),
    },
    {
        "slug": "mental-health",
        "num": "02",
        "title": "Mental Health Risk Predictor",
        "tagline": "Which socioeconomic and environmental signals predict community-level mental health risk?",
        "year": "2022",
        "role": "ML engineer",
        "stack": "Python · Scikit-Learn · SQLite · Tableau · Flask",
        "image": "../images/projects/01-mental-health.png",
        "image_alt": "Feature importance bar chart for the mental health risk model",
        "live": ("View notebook", "https://nbviewer.org/github/Jonahrahn/Mental_Health_Predictor/blob/main/MachineLearning_Shallow_and_Deep.ipynb"),
        "code": ("View code on GitHub", "https://github.com/Jonahrahn/Mental_Health_Predictor"),
        "problem": (
            "Mental health outcomes vary widely across communities, but it isn't obvious "
            "which signals matter most. The goal was to identify the strongest "
            "community-level predictors and quantify how much each one contributes."
        ),
        "approach": (
            "Merged socioeconomic and environmental datasets into a SQLite-backed feature "
            "table, trained a Random Forest classifier, and inspected per-feature "
            "importance to surface the drivers. Built a small Flask app and Tableau "
            "workbook to publish the result."
        ),
        "result": (
            "Standard deviation of income, not absolute income level, was the strongest "
            "predictor, contributing 41 percent of the total feature importance. Income "
            "inequality, in other words, mattered more than poverty per se."
        ),
        "prev": ("Citi Bike Tableau Visualization", "citi-bike.html"),
        "next": ("Neural Network Charity Analysis", "charity-nn.html"),
    },
    {
        "slug": "charity-nn",
        "num": "03",
        "title": "Neural Network Charity Analysis",
        "tagline": "Predicting charity-campaign success with a deep classifier, then pushing it past the target threshold.",
        "year": "2022",
        "role": "ML engineer",
        "stack": "Python · TensorFlow · Keras · Pandas",
        "image": "../images/projects/02-charity-nn.png",
        "image_alt": "Optimized neural network accuracy reaching 79%, exceeding the 75% target",
        "live": ("View notebook", "https://nbviewer.org/github/Jonahrahn/Neural_Network_Charity_Analysis/blob/main/AlphabetSoupCharity-Optimization.ipynb"),
        "code": ("View code on GitHub", "https://github.com/Jonahrahn/Neural_Network_Charity_Analysis"),
        "problem": (
            "Given a dataset of 34,000 prior charity grants and whether each was used "
            "effectively, predict the same for a new grant. The minimum bar set by the "
            "stakeholder was 75 percent classification accuracy."
        ),
        "approach": (
            "Built a feed-forward neural net in TensorFlow / Keras with two hidden layers. "
            "Iterated on preprocessing: binning rare categorical values, dropping noisy "
            "columns, and ultimately keeping the NAME feature (which earlier versions "
            "dropped) because it carried predictive signal."
        ),
        "result": (
            "The optimized run reached 79 percent accuracy with a 0.45 loss, clearing the "
            "75 percent target. The single largest contributor was re-introducing the NAME "
            "feature with proper grouping rather than dropping it as identifier noise."
        ),
        "prev": ("Mental Health Risk Predictor", "mental-health.html"),
        "next": ("Mission to Mars", "mission-to-mars.html"),
    },
    {
        "slug": "mission-to-mars",
        "num": "04",
        "title": "Mission to Mars",
        "tagline": "An end-to-end aggregator pulling Mars-mission data into a single Flask-served page.",
        "year": "2021",
        "role": "Full-stack developer",
        "stack": "Python · Splinter · BeautifulSoup · Flask · MongoDB",
        "image": "../images/projects/04-mission-to-mars.png",
        "image_alt": "Composition of the data the Mission to Mars app aggregates: news headline, hemispheres, and Mars facts",
        "live": ("View notebook", "https://nbviewer.org/github/Jonahrahn/Mission-to-Mars/blob/main/Mission_to_Mars_Challenge.ipynb"),
        "code": ("View code on GitHub", "https://github.com/Jonahrahn/Mission-to-Mars"),
        "problem": (
            "Mars-mission information is spread across NASA news, image archives, "
            "hemisphere photo pages, and reference tables. The brief: pull it together "
            "into a single page that refreshes on demand."
        ),
        "approach": (
            "Wrote a Python scraper using Splinter for browser-driven pages and "
            "BeautifulSoup for static parsing. Persisted the most recent scrape to "
            "MongoDB; rendered the result through a Flask app with a Bootstrap front end."
        ),
        "result": (
            "A working aggregator that scrapes on demand and persists to Mongo, useful as "
            "an end-to-end exercise spanning scraping, storage, and presentation across "
            "the full stack."
        ),
        "prev": ("Neural Network Charity Analysis", "charity-nn.html"),
        "next": ("Amazon Review Bias Analysis", "amazon-vine.html"),
    },
    {
        "slug": "amazon-vine",
        "num": "05",
        "title": "Amazon Review Bias Analysis",
        "tagline": "Does Amazon's paid Vine reviewer program produce measurably different ratings than the public?",
        "year": "2022",
        "role": "Data analyst",
        "stack": "Python · PySpark · PostgreSQL · Pandas",
        "image": "../images/projects/05-amazon-vine.png",
        "image_alt": "Proportion bar: 82 paid Vine reviews vs 24,742 unpaid public reviews in the automotive category",
        "live": ("View notebook", "https://nbviewer.org/github/Jonahrahn/Amazon_Vine_Analysis/blob/main/Vine_Reviews_ETL.ipynb"),
        "code": ("View code on GitHub", "https://github.com/Jonahrahn/Amazon_Vine_Analysis"),
        "problem": (
            "Amazon's Vine program gives selected reviewers free products in exchange for "
            "feedback. The question: do those paid reviewers rate products differently "
            "than the unpaid public, in ways that could bias purchase decisions?"
        ),
        "approach": (
            "ETL over the full Amazon automotive review dataset using PySpark, landing "
            "the cleaned table in PostgreSQL. Filtered for sufficient vote counts, then "
            "split into Vine and non-Vine populations and compared their rating "
            "distributions."
        ),
        "result": (
            "Only 0.33 percent of qualifying reviews were paid (82 of 24,824). That is a "
            "small enough slice that even a real bias effect would be hard to detect "
            "confidently; useful as a baseline for further category-by-category audits."
        ),
        "prev": ("Mission to Mars", "mission-to-mars.html"),
        "next": ("Ride-Share Analytics", "pyber.html"),
    },
    {
        "slug": "pyber",
        "num": "06",
        "title": "Ride-Share Analytics",
        "tagline": "Where does a ride-share company actually make its money? A four-month look across city types.",
        "year": "2021",
        "role": "Data analyst",
        "stack": "Python · Pandas · Matplotlib",
        "image": "../images/projects/06-pyber.png",
        "image_alt": "Weekly total fare by city type, January through April: urban dominates, suburban steady, rural minimal",
        "live": ("View notebook", "https://nbviewer.org/github/Jonahrahn/PyBer_Analysis/blob/main/PyBer_Challenge.ipynb"),
        "code": ("View code on GitHub", "https://github.com/Jonahrahn/PyBer_Analysis"),
        "problem": (
            "A hypothetical ride-share company wanted to understand how its January "
            "through April 2019 revenue split across urban, suburban, and rural "
            "city types, to inform resource allocation."
        ),
        "approach": (
            "Aggregated the trip and fare data by city type and week using Pandas, then "
            "produced comparative line charts in Matplotlib showing weekly total fares "
            "across the three segments over the four-month window."
        ),
        "result": (
            "Urban accounted for $2,000 to $2,500 in weekly fares, suburban held steady "
            "around $1,000, rural barely reached $500. The urban segment is where "
            "incremental investment pays off; rural is a thin tail worth keeping but not "
            "chasing."
        ),
        "prev": ("Amazon Review Bias Analysis", "amazon-vine.html"),
        "next": ("Back to portfolio", "../"),
    },
]


TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <title>{title} · Jonah Rahn</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{tagline}">
  <link rel="icon" type="image/svg+xml" href="../favicon.svg">
  <meta property="og:title" content="{title} · Jonah Rahn">
  <meta property="og:description" content="{tagline}">
  <meta property="og:image" content="https://jonahrahn.github.io/images/og-card.png">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../style.css">
</head>
<body class="case-body">

  <header class="nav" id="top">
    <a class="nav__brand" href="../">Jonah Rahn</a>
    <nav class="nav__links">
      <a href="../#about">About</a>
      <a href="../#capabilities">Capabilities</a>
      <a href="../#work">Selected Work</a>
      <a href="../#contact">Contact</a>
      <a class="nav__resume" href="../resume.pdf" target="_blank" rel="noopener">Resume ↗</a>
    </nav>
    <button class="nav__toggle" aria-label="Menu" aria-expanded="false">Menu</button>
  </header>

  <section class="case-hero">
    <div class="case-hero__inner">
      <p class="case-hero__crumb">
        <a href="../">Index</a>  <span>/</span>  <a href="../#work">Work</a>  <span>/</span>  <span>{title}</span>
      </p>
      <p class="eyebrow">§ {num}  ·  {stack}</p>
      <h1 class="case-hero__title">{title}</h1>
      <p class="case-hero__tagline">{tagline}</p>
    </div>
  </section>

  <section class="case">
    <aside class="case__meta">
      <dl>
        <div><dt>Year</dt><dd>{year}</dd></div>
        <div><dt>Role</dt><dd>{role}</dd></div>
        <div><dt>Stack</dt><dd>{stack}</dd></div>
        <div><dt>Live</dt><dd><a href="{live_href}" target="_blank" rel="noopener">{live_label} ↗</a></dd></div>
        <div><dt>Code</dt><dd><a href="{code_href}" target="_blank" rel="noopener">{code_label} ↗</a></dd></div>
      </dl>
    </aside>

    <div class="case__body">
      <figure class="case__figure">
        <img src="{image}" alt="{image_alt}">
      </figure>

      <article class="case__article">
        <section class="case__section">
          <h2><span class="case__section-num">01</span> Problem</h2>
          <p>{problem}</p>
        </section>
        <section class="case__section">
          <h2><span class="case__section-num">02</span> Approach</h2>
          <p>{approach}</p>
        </section>
        <section class="case__section">
          <h2><span class="case__section-num">03</span> Result</h2>
          <p>{result}</p>
        </section>
        <section class="case__cta">
          <a class="btn" href="{live_href}" target="_blank" rel="noopener">{live_label} ↗</a>
          <a class="btn btn--ghost" href="{code_href}" target="_blank" rel="noopener">{code_label} ↗</a>
        </section>
      </article>
    </div>
  </section>

  <nav class="case-nav">
    <a class="case-nav__prev" href="{prev_href}">
      <span class="case-nav__label">← Previous</span>
      <span class="case-nav__title">{prev_label}</span>
    </a>
    <a class="case-nav__next" href="{next_href}">
      <span class="case-nav__label">Next →</span>
      <span class="case-nav__title">{next_label}</span>
    </a>
  </nav>

  <footer class="footer">
    <div class="footer__row">
      <span>© <span id="year">2026</span> Jonah Rahn</span>
      <span>Santa Cruz, California</span>
      <a href="../#top">Back to top ↑</a>
    </div>
  </footer>

  <script src="../script.js"></script>
</body>
</html>
"""


for c in CASES:
    html = TEMPLATE.format(
        title=c["title"],
        tagline=c["tagline"],
        num=c["num"],
        year=c["year"],
        role=c["role"],
        stack=c["stack"],
        image=c["image"],
        image_alt=c["image_alt"],
        live_label=c["live"][0],
        live_href=c["live"][1],
        code_label=c["code"][0],
        code_href=c["code"][1],
        problem=c["problem"],
        approach=c["approach"],
        result=c["result"],
        prev_label=c["prev"][0],
        prev_href=c["prev"][1],
        next_label=c["next"][0],
        next_href=c["next"][1],
    )
    path = OUT / f"{c['slug']}.html"
    path.write_text(html)
    print(f"wrote {path}")
