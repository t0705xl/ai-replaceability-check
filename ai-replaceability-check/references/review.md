# Review: challenge the card before scoring

## Why this step exists

Across three calibration rounds (41 real products), almost every wrong verdict came from the **decomposition**, not from the scoring formula. Most of those errors were in one place: the **per-mode relation with AI clients**. The weights have barely changed since the first round; the review step is where accuracy is won or lost.

## How to run it

- **If you can start an independent subagent**, give it only three things: the user's original description, the card, and this file. Do not pass your reasoning. Ask it to find errors, not to agree.
- **Otherwise, review it yourself with a changed stance.** Your job now is to find what is wrong with the card, not to defend it.

## Checklist

Each item names the real miss that taught us to check it.

1. **Is any usage mode really two modes?** A mode that mixes answer-seeking with browsing or doing must be split, because the two relate to AI clients differently. *(Xiaohongshu: "browse the feed" survived while "search for travel guides" was taken by AI; time spent fell for the first time.)*

2. **Information check on every A.** For each mode judged A, can an AI client actually obtain the information needed to answer? Real-time, hyperlocal, or private information that exists only inside the product rules out A. *(Nextdoor: judged A for "ask neighbors", but what a neighbor posted last night is behind address verification; the product grew 14%.)*

3. **In-product completion steps split out?** For comparison and shopping-guide products, are pre-qualification, matching, quoting, or licensed-agent steps that happen inside the product their own mode? *(NerdWallet: treated as "read comparisons" only; its loan pre-qualification and licensed agents kept revenue growing 11%.)*

4. **A vs C vs D.** C means the AI shows your data in its own interface; D means the transaction or action is completed with you. A link out does not make a mode D. *(Tripadvisor's price click-outs are A, not D.)*

5. **Deliverable check.** For transaction types, can AI directly produce what users buy here? If yes, `deliverable_ai_replaceable` must be true. *(Fiverr: strong transaction mechanics, but simple gigs became AI-doable; active buyers -26%. Shutterstock: revenue -17%.)*

6. **Search acquisition flag.** Does the product mainly rely on search engines for answer-seeking traffic? *(Tripadvisor: AI replaced the function and AI search cut the channel; a $370M impairment.)*

7. **Hardware.** Selling hardware is not execution. A hardware function that a phone plus an AI client can replicate is device class A. *(Youdao Dictionary Pen: device revenue -31% to -43%.)*

8. **Lookups are automatable.** Looking up words, answers, or references is never `must_do_yourself`.

9. **Link outs are not transactions;** sub-type checks only for transaction and community types; secondary type meets both thresholds.

10. **Common inflation patterns:**
    - "Nice UI" or "smooth experience" used as evidence
    - Saved history scored above state L1
    - A public API scored as proprietary data
    - A "share" button scored above network L1
    - A plugin inside someone else's platform scored above workflow L2
    - Roadmap features classified

11. **Strongest counterargument, both ways.**
    - Write the strongest 2–3 sentence case that users could simply use an AI client instead. For every mode **not** judged A or B, check whether this argument defeats the judgment.
    - Then write the strongest case that AI clients cannot do what a mode judged A does. If it holds (usually through the information check), change the judgment.

12. **Compare with the closest calibration cases** in `references/calibration.md`. If the card is more generous than similar cases that actually collapsed or came under pressure, either name the concrete difference or downgrade.

## Output

- A list of changes: `field: old → new, reason`. If nothing changes, say so explicitly.
- The corrected card, ready for `scripts/score.py`.
