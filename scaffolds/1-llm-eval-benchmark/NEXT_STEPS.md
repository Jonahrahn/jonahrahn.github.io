# Next steps — how to ship this in two focused weeks

## Week 1: data

1. **Pick 3–4 phenomena to launch with.** Quality beats coverage. Start with the ones you have strong linguistic opinions on.
2. **Write 30–60 items per phenomenon.** Use minimal pairs where you can. Run each through `make validate`.
3. **Read each item out loud.** If it's ambiguous to you, it's ambiguous; mark it `"gold": "either"`.
4. **Have one linguist friend review.** Twenty minutes of cross-check saves weeks of credibility.

## Week 2: harness + leaderboard

5. **Run against three models.** Suggested: GPT-4o, Claude Sonnet 4.6, Llama 3.1 70B (via Groq or together.ai).
6. **`make leaderboard` updates the README table** from `results/*.jsonl`. Commit those JSONLs.
7. **Write a 500-word post on the most surprising finding.** Publish on a personal site or LinkedIn. Link from the README.
8. **Add a 'Reading' section** to the README pointing at the literature you drew from (Horn 1989, Sauerland & Yatsushiro 2009, etc.).

## What makes this credible

- Items are **hand-written**, not synthetic.
- **`gold: "either"` is used** for genuinely ambiguous cases. Recruiters can tell a benchmark that's been engineered for high disagreement.
- **Rationales are visible.** A linguist reviewer can validate every item.
- **The leaderboard updates** as you add models. Recency signals maintenance.

## Common failure modes to avoid

- Inflating the dataset with paraphrases of the same item (the model only needs to learn one trick).
- Making A always the right answer (run `make validate` to catch).
- Using vague rationales like "negation flipped the meaning" — be precise about scope, presupposition, focus.

## After launch

- File a CFP for an HCI/NLP workshop demo if you want to push it further.
- Cross-link from your portfolio's case study page.
- Re-run quarterly as new models drop. Each re-run is a free blog post.
