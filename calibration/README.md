# Calibration record

How the scoring rules were built and tested against 41 real products, and how to reproduce every number.

```bash
python3 calibration/run_calibration.py
```

## Method

1. **Round 1, calibration (14 products, in-sample).** Products with clear AI-era outcomes, from collapsed (Chegg, Stack Overflow, Tome) to benefiting (Figma, Canva, Notion). Each was decomposed as it looked when AI clients arrived, scored, and compared with its outcome. The rules were then adjusted. This is where the calibration factors and the practice type came from.
2. **Round 2, blind (14 products).** Picked to fill gaps: offline fulfillment, hardware, games, Chinese products, and marketplaces whose goods AI can produce. **Predictions were locked before any outcome was looked up**, with a SHA-256 fingerprint. Then outcomes were checked, misses analyzed, and the rules revised (v3).
3. **Round 3, blind (13 products).** Same protocol, targeting the areas v3 changed most: mixed information-and-community products and data-source products. Rules revised again (v4).

Outcome labels, fixed before checking:

- **Collapsed:** core business replaced, or down more than 30% from peak with AI as a major cause
- **Pressured:** core metric flat, declining, or sharply slowing, with AI cited as one cause
- **Resilient:** still growing
- **Benefiting:** growth accelerating, with AI explicitly a tailwind

Non-AI confounders (price wars, high prior-year base, post-pandemic decline) are flagged in the evidence.

Compatibility: High risk ↔ Collapsed or Pressured; One moat ↔ Pressured or Resilient; Hard to replace ↔ Resilient or Benefiting.

## Results

| | Rules when locked | Compatible | Rank correlation |
|---|---|---|---|
| Round 2 (blind) | v2 | **10/14** | 0.720 |
| Round 3 (blind) | v3 | **10/13** | 0.622 |
| All 41 with current rules (v4) | v4 | 40/41 | 0.790 |

**The honest number is the locked one: about 75% out of sample.** The 40/41 is in-sample, because v4 was built from these same misses.

## What each round taught

| Round | Misses | Rule changes |
|---|---|---|
| 1 | Pinterest, Canva | Added the practice / habit type; added the F (parallel) relation; complementary relations (D/E) count as a moat item; calibration factors (state ×1.5; precision ×0.6, which had no predictive power) |
| 2 | Xiaohongshu, Yelp, Wix (severe); Fiverr (mild) | Relation judged per usage mode; data source (C) is not neutral; deliverable check for marketplaces; hardware clarifications |
| 3 | Nextdoor, NerdWallet (severe); Tripadvisor (mild) | Information check before judging A; split in-product completion steps out of comparison products; search-dependent acquisition plus a substitute relation drops one more level |

Almost every change after round 1 concerned **the relation with AI clients**. The frontend and business weights have not moved since round 1. The remaining errors come mostly from decomposition, which is why the skill has a dedicated review step.

## Files

- `cards/round1`, `cards/round2`, `cards/round3`: all 41 decomposition cards in English, in the format `score.py` reads.
- `cards/round3_locked_original`: the round 3 cards exactly as locked. Two of them (Nextdoor, NerdWallet) were later corrected under the new v4 decomposition rules; the corrected versions are in `cards/round3`.
- `cards/outcomes.json`: outcome label, evidence, and the expected v4 result for every card.
- `source/`: the original research code and the two locked prediction files, unchanged, so the fingerprints can be recomputed. Comments and labels are in Chinese.
- `original-reports-zh/`: the three original round reports, in Chinese, as written at the time.

## Limitations

- 41 products, mostly listed companies or well-known startups, because they have public data.
- The cards were written by a model whose knowledge reached mid-2026, so some prior knowledge of outcomes was unavoidable. Locking only guarantees that cards were not changed after outcomes were checked.
- Only 3 products are labeled "Benefiting", so the framework's ability to tell "Resilient" from "Benefiting" is essentially untested. Canva, the one remaining miss, is exactly that case.
- Context of use and device capability are barely tested; only Strava and Oura exercise them.
