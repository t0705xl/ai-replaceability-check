# Writing the report

## Rules

- **Write in the language the user writes in.** This template is in English only so the model can read it; translate the headings.
- **Every number comes from `scripts/score.py`.** Never compute or adjust a score by hand.
- **No flattery and no encouragement padding.** The more invested the user is in the idea, the more the report must stick to the rules. Do not raise any classification to protect feelings.
- **Show the per-mode relation table.** It is the most predictive and most error-prone part, and the user is best placed to catch a wrong call there.
- **Separate facts from assumptions.** Keep the source tags (`[stated]`, `[inferred]`, `[assumed]`), translated.
- **State the accuracy honestly:** about 75% of out-of-sample verdicts were compatible with real outcomes. This is a structural analysis, not a market forecast.
- **Attach the chart** produced by `score.py --svg` when the environment can show or send files.

## Template

```markdown
# [Project name]: AI replaceability check

**Level: [High risk / One moat / Hard to replace]**: [diagnosis]
[One sentence: the single most important reason.]

## Core loop
Input: … → The product: … → Output: … → The user then: …
Value is realized: [in the product / elsewhere: where]

## Type
Primary: … | Secondary: … | Structural potential: …

## Relation with AI clients, by usage mode
| Usage mode | Share | Relation | Why |
|---|---|---|---|
| … | …% | A replaced directly / … | … |
Relation score: … → [substitute / neutral / complement]

## Frontend layer
| Aspect | Score | Evidence |
|---|---|---|
(8 rows; bold any score ≥ 4)

## Business layer
| Dimension | Level | Evidence |
|---|---|---|
(6 rows; bold any level ≥ L4)

## How the verdict was reached
[Copy the verdict steps from the script output: moat items, exclusions, relation adjustment, search adjustment.]

[Chart]

## Strongest case for "just use an AI client"
[2–3 sentences from the review step, stated as strongly as possible.]

## Where to build a moat
For each of the 3 nearest moats from the script:
- **[Item] (now …)**: 2–3 concrete changes, and the score each would likely reach.
- Say plainly if a change would turn the product into a different type (a pivot), and what the new type's potential would be.

## Risks
[Risk notes from the script, plus anything the review step flagged.]

## Key assumptions to verify
[The 2 most consequential assumptions, word for word from the card.]

## If you decide not to build it
[One sentence: the reason.]

---
This is a structural analysis, not a market forecast. It asks whether users have a reason not to just use an AI client. It does not ask whether anyone needs the product; only talking to real users answers that. In blind tests on real products, about three in four verdicts matched what actually happened.
```

## Comparing several projects

Score each card separately (`score.py a.json b.json c.json` ranks them by overall score). Write one short section per project, followed by a comparison table: project, level, potential, relation score, overall, and the biggest risk. Rank by level first, and use the overall score only to break ties within a level.

## When the user asks "how do I make it hard to replace?"

Start from "Where to build a moat". Do not invent a separate framework. If the only realistic route is a pivot, say so, and offer to run the check again on the pivoted version.
