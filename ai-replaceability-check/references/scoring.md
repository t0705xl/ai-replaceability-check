# Scoring rules (v4)

`scripts/score.py` implements these rules, and every table lives in `scripts/config.json`. **The script is the source of truth; never compute scores by hand.** This file explains what the script does and why, so you can explain a result to the user.

## Outputs

| Output | Range | Meaning |
|---|---|---|
| Structural potential | 1–5 | How hard this *kind* of product can be to replace |
| Frontend score | 0–100 | How much of the frontend layer is actually achieved |
| Business score | 0–100 | How much of the business layer is actually achieved |
| Relation score | 0–100 | Share-weighted relation with AI clients across usage modes |
| **Level** | High risk / One moat / Hard to replace | **The verdict** |
| Diagnosis | one of four | Why the level came out as it did |
| Overall | 0–100 | For ranking several projects only; never the verdict |
| Nearest moats | 3 items | Where improvement pays off most |

## 1. Structural potential

| Type | Potential |
|---|---|
| Generate / advise, Retrieve / aggregate | 1 |
| Information community, Transaction front end | 2 |
| Tool / editor, Record / manage, Practice / habit | 3 |
| Merchant of record, Relationship community | 4 |

With a secondary type: potential = primary × 0.7 + secondary × 0.3.

No type gets 5: every type has an information layer that AI clients are absorbing.

## 2. Frontend layer (each aspect 0–5)

Class scores:

| Aspect | A | B | C | D | E | F |
|---|---|---|---|---|---|---|
| Input cost | 0 | 1 | 1 | 3 | 4 | 5 |
| Frequency & speed | 0 | 1 | 2 | 4 | 5 | |
| Precision control | 0 | 1 | 3 | 4 | 5 | |
| Seeking vs browsing | 0 | 1 | 3 | 4 | | |
| Read once vs monitor | 0 | 1 | 3 | 4 | 5 | |
| Context of use | 0 | 1 | 3 | 4 | 4 | |
| Device capability | 0 | 2 | 4 | 5 | | |
| Experience as the end | 0 | 1 | 3 | 4 | 5 | |

Trends are already folded into these numbers. For example, "pick among a few options" scores only 1 because AI clients now render cards, images, and maps.

Modifiers (each drops the class to the next lower score):

| Aspect | Condition | Result |
|---|---|---|
| Frequency | D/E and `automatable` | D → 2, E → 4 |
| Precision | E and `recurring: false` | → 1 (AI can write code for a one-off precise result) |
| Intent | C/D and `content_source: ai_or_scraped` | C → 1, D → 3 |
| Device | B/C/D and `platform_generic: true` | B → 0, C → 2, D → 4 |
| Experience | `chat_reproducible: true` | capped at 1 |

Aggregation:
- Mode-level aspects: Σ(mode share × class score)
- Step-level aspects: Σ(mode share × step share × class score)

## 3. Business layer

The level is the score: L0 = 0 … L5 = 5.

## 4. Weighted layer scores

Final weight = type weight × calibration factor. With a secondary type, type weights are blended 0.7 / 0.3.

**Type weights** give 3 to the realistic escape routes of each type. For example, a generate-type product can only escape through letting users shape the result by hand (input cost) or making the process itself worth having (experience), and in the business layer through data, state, and execution.

**Calibration factors** come from how well each item separated products that were replaced from those that were not:

| Factor | Items | Evidence |
|---|---|---|
| × 1.5 | Accumulated state | Strongest single predictor (ρ = 0.86) |
| × 1.25 | Input cost, Proprietary data, Workflow & distribution | ρ 0.55–0.8 |
| × 1.0 | Experience, Network, Frequency, Execution, Intent | ρ 0.4–0.55 |
| × 0.85 | Trust, Read once vs monitor | ρ 0.3–0.4 |
| × 0.6 | Precision control | No separation: winners and losers averaged the same |
| × 1.0 | Context of use, Device capability | Too few samples to calibrate |

Layer score = Σ(weight × score) ÷ (5 × Σ weight) × 100.

Quality gates: if any gate is `fail`, frontend score × 0.8.

## 5. Level (the verdict)

1. **Moat items.** Pool all 14 items (8 frontend + 6 business). Any item scoring **≥ 4** is a moat item.
   - Frontend aspects are share-weighted, so reaching 4 means the strength covers most of the core loop. A strength in a corner does not count.
   - **Deliverable check:** if `deliverable_ai_replaceable` is true, execution, network, and trust do not count as moat items. They protect the transaction, but AI already satisfies the demand.
2. **Relation score** = Σ(mode share × relation value), with A/B = 0, C = 25, F = 50, D/E = 100.
   - **≥ 75 (complement):** counts as one extra moat item. Being called by AI clients means they send you users.
   - **< 35 (substitute):** applied in step 4 below.
3. **Base level:** 0 moat items → High risk; 1 → One moat; 2+ → Hard to replace.
4. **Substitute:** if the relation score is < 35, drop one level.
5. **Search double exposure:** if `search_acquisition` is true **and** the relation score is < 35, drop one more level. AI replaced the function, and AI search cut the acquisition channel.

The level never goes below High risk.

**Why the level ignores the weighted scores:** a moat is about the highest bar, not the average. A product scoring 3 on everything has a respectable average and no defensible position.

**Why relation is judged per mode:** within one product, modes can relate to AI in opposite ways. Wix's "build a site" is replaceable; "run the site" (orders, bookings, payments) is a system AI cannot bypass.

**Why C is not neutral:** a data source has its data shown inside the AI client's interface, so users no longer open yours. Yelp's AI data-licensing revenue grew 82% while its ad clicks fell 8%.

## 6. Diagnosis

| | Has moat items | No moat items |
|---|---|---|
| **Potential ≥ 3** | Structure and execution agree | Right direction, moat not built yet (cold-start risk) |
| **Potential < 3** | Risky direction, held up by a single strength | The direction itself is easy to replace |

## 7. Overall score (ranking only)

Overall = 15% × potential/5×100 + 35% × business + 35% × frontend + 15% × relation score.

## 8. Nearest moats

Among items below 4: priority = weight ÷ (4 − score). Top 3. High weight and close to the line wins. The report must give concrete actions for each and say explicitly when reaching it would require changing the product's type.

## 9. Risk notes (not scored)

- `search_acquisition` true without triggering the downgrade: AI search is taking answer-seeking traffic; watch the share of direct visits.
- `ai_habit` C or D: target users rarely use AI today. That is a time window, not a moat.
- Failed quality gates, listed.

## Worked examples

Both produced by `scripts/score.py` (cards in `examples/`).

| | Travel itinerary generator | Team whiteboard with AI notes |
|---|---|---|
| Type | Generate + Tool | Tool |
| Potential | 1.6 | 3 |
| Relation by mode | Planning A (50%), During trip B (50%) → 0 | Collaboration D (100%) → 100 |
| Frontend / business | 27.2 / 39.0 | 38.1 / 56.0 |
| Moat items | none | Frequency & speed, Accumulated state, Complement |
| **Level** | **High risk** | **Hard to replace** |
| Diagnosis | The direction itself is easy to replace | Structure and execution agree |
| Overall | 28.0 | 56.9 |

## Accuracy

Verdicts are judged against outcomes with this compatibility table:

| Level | Compatible outcomes |
|---|---|
| High risk | Collapsed, Pressured |
| One moat | Pressured, Resilient |
| Hard to replace | Resilient, Benefiting |

- **In-sample** (41 products, v4): 40/41 compatible.
- **Out-of-sample** (predictions locked before outcomes were checked): about **75%** (10/14 and 10/13 in the two blind rounds).

Tell users the out-of-sample number, not the in-sample one.
