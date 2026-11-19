---
name: ai-replaceability-check
description: Assess whether a product or project idea would be replaced by general AI clients (ChatGPT, Claude, Gemini, Doubao, etc.). Decomposes the product into usage modes, judges each mode's relation with AI clients, scores 8 frontend and 6 business moat dimensions with a calibrated script, and writes a verdict with a chart and where to build a moat. Use when someone describes a product, app, startup, or side-project idea and asks whether it is worth building, whether AI will kill it, whether it is "just a wrapper", where its moat is, or to compare several ideas. Also for 会不会被 AI 取代, 是不是套壳, 值不值得做, 护城河在哪.
---

# AI replaceability check

One question: **does a user have a reason not to just open an AI client instead of this product?**

The rules were calibrated on 41 real products (two blind rounds). Out of sample, about 3 in 4 verdicts matched what actually happened. Say so in every report.

## Workflow

Do the steps in order. Do not skip the review.

### 1. Decompose
Read `references/decompose.md` and follow it from Step 0:
- Ask at most 3 questions if key information is missing; otherwise continue with tagged assumptions.
- Split the product into usage modes and steps with shares.
- Determine the type with the removal test.
- Classify business levels and frontend classes. The tables there deliberately show no scores.
- Judge the relation with AI clients **per usage mode**, after the information check.
- Output the card as JSON. Save it to a file (e.g. `card.json`).

### 2. Review
Read `references/review.md`. If you can start an independent subagent, give it the user's description, the card, and that file, and ask it to find errors. Otherwise review the card yourself with the stance of someone trying to prove it wrong. Apply the corrections.

Most past errors were in per-mode relations and mode splitting, not in the formula. Spend your effort here.

### 3. Score
Run the scorer. It uses only the Python standard library:

```bash
python3 scripts/score.py card.json --svg chart.svg
```

Add `--json` for machine-readable output. Pass several cards to rank them. Use the script's numbers as they are. **Never compute or adjust scores by hand.** If code cannot run, say so and stop before giving a level; do not estimate one. `references/scoring.md` explains every rule if you need to explain a result.

### 4. Compare with calibration cases
Open `references/calibration.md` and find 1–2 real products with the same primary type and a similar relation pattern. Mention them in the report as reference points. If your result looks clearly more generous than a similar case that collapsed, go back to step 2.

### 5. Report
Follow `references/report.md`:
- Write in the user's language.
- Include the per-mode relation table, the verdict steps, the chart, the strongest case for "just use an AI client", and the 3 nearest moats with concrete actions.
- State the out-of-sample accuracy and that this is a structural analysis, not a market forecast.

## Principles

- **Structure, not subject matter.** "Input a need, get advice" is the most replaceable structure, whether it is travel, resumes, or recipes.
- **A moat is the highest bar, not the average.** Eight items at 3 lose to one item at 5.
- **Assume AI clients are strong.** They browse, read files, remember, render cards and maps, call apps, and run skills. Anything on that list earns nothing.
- **Do not inflate for an invested user.** The more someone loves an idea, the more strictly the rules apply.
