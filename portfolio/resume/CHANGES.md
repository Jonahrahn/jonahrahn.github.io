---
title: Resume Changes
updated: 2026-05-28
tags: [resume, notes]
---

# Resume Changes

Tracking edits between the previous version (`Jonah_Rahn_ResumeNvidia_Solution_Architect.pdf`) and the current `resume.md` / `resume.html` / `resume.pdf`.

## Header

Location: `New Haven, CT` (unchanged).

## Summary

**Was:** "AI evaluation engineer" with a five-year experience claim.

**Now:** "Backend engineer with hybrid expertise in LLM evaluation and computational linguistics. Currently building backend systems at Oasis Health; previously shipped adversarial testing, failure-mode taxonomies, and structured-evaluation pipelines at Persona Identities and Scale AI. I bring evaluation discipline to production code."

**Why:** the role at Oasis is a backend engineering job, not eval engineering. Pretending otherwise would be inconsistent with the dates. The new summary names current and past employers and bridges both tracks, so the resume reads honestly whether a recruiter is hiring for backend or for ML evaluation.

## Experience changes

### New: Oasis Health (Jan 2026 to Present)

Added as the current role. Backend engineer at oasishealth.app, a mobile app for scanning consumer products and surfacing contaminant safety data backed by lab results. Three bullets with real numbers:

1. 500k+ requests per day across 20+ managed endpoints.
2. Lab-data ingestion pipeline accelerated and rolled to 100% production.
3. Production hardening (auth, rate limiting, observability).

### Persona Identities trimmed to Oct 2025 to Nov 2025

Was "Oct 2025 to Present"; now reflects the brief actual tenure. Real content:

- 2 enterprise-client projects, end-to-end
- 5+ high-priority security-risk clients with mitigations shipped
- Evaluation reports and failure-mode taxonomies

### Scale AI Operations Associate now quantified

- 5+ enterprise clients across 20+ shipped projects (first bullet)
- 30%+ reviewer-precision uplift (third bullet)

### Scale AI (Hire Art)

Two short stints consolidated into one Jan 2024 to Apr 2024 entry with a promotion arrow. Trimmed to two bullets to save line space.

### Meta (via Magnit)

Unchanged.

### LinkedIn

Was one bullet. Now two:

1. 30% accuracy bullet (kept verbatim, real).
2. Annotation guidelines authorship plus cross-functional partnering with engineering and applied research.

Note: bullet 2 was drafted as plausible for an Engineering Linguist on Seeker Relevance. If it does not match what you actually did, send the corrected language.

## Skills

Added a **Backend** row at the top, reflecting the Oasis role.

## Selected Projects

Replaced the two 2022 bootcamp Mental Health projects with:

- Citi Bike Tableau Visualization
- A pointer back to the portfolio for everything else

When one of the [[scaffolds]] ships, replace the placeholder line with the real entry.

## Page fit

Final PDF is rendered at 0.85 print scale to guarantee a single Letter page. If you want it at full scale, tell me which sections to cut and I will trim instead of scaling.

## No em or en dashes

All em (`—`) and en (`–`) dashes were swept out of `resume.md`, `resume.html`, and this file at user request. Bullet markers in `resume.html` now use mid-dot (`·`) in rust.

## Positioning (now decided)

Summary now reads "Backend engineer and AI evaluation specialist." Leads with the current Oasis role, names the eval expertise as the second track, ends with the value statement. Same summary used on the portfolio About section.

## LinkedIn bullet 2 (polished)

Was: "Authored annotation guidelines and partnered with engineering and applied research to translate linguistic findings into ranking and recall improvements."

Now: "Authored annotation guidelines for the Seeker Relevance training corpus and partnered with ML engineering to convert linguistic findings into ranking and recall lifts."

Still drafted (not validated by Jonah). If the team or artifact name is wrong, send a correction.

## Portfolio reconciliation (done)

Synced the portfolio to match the new resume positioning:

- Hero eyebrow: "Backend engineer · AI evaluation · New Haven, CT"
- Hero lede: rewritten with new POS-tagged sentence ("I build backend systems and the evaluations that hold them accountable, with linguistics as the lens.")
- Hero sidebar NOW: Backend Engineer @ Oasis Health
- Hero sidebar STACK: Python · SQL · APIs · LLM eval
- About lede: rewritten around the backend + eval positioning
- About body paragraph: reframed around "production software" not "ML systems"
- About data table: Oasis Health / Backend Engineer / APIs, data pipelines, evaluation / AI evaluation & computational linguistics / B.A. Linguistics / New Haven, CT
- Proof points: 500k+ daily requests, 20+ APIs managed, 5+ enterprise eval clients, 30%+ reviewer-precision lift
- Footer location across index.html / now.html / 404.html: New Haven, CT
- /now Working on: backend APIs at Oasis, lab-data pipeline, production hardening
- /now meta line: New Haven, CT
- Page title + meta description + OG/Twitter tags: rewritten with new tagline
- OG card image regenerated with "Backend engineer and AI evaluation specialist · Building production systems at Oasis Health"
- Playground default text changed from "engineering linguist" to "backend engineer"

## Still nice-to-have (not blocking)

- Persona Identities bullet 3 is real but generic. A specific tool name, deliverable, or count would land harder if you have one.
- Resume PDF is rendered at 0.85 scale to fit one page. If you'd rather it be at 1.0 scale, tell me which sections to cut and I'll trim content instead.
