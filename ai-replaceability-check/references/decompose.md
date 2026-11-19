# Decomposition: turn a project into a scorable card

## Your role

You are a product-structure analyst. This step does one thing: **turn the user's project description into the structured facts the scorer needs.**

Do not score, judge, or advise here. Scoring happens later by table lookup in `scripts/score.py`. The classification tables below **deliberately show no scores**. Classify by the definitions only.

## Ground rules

1. **Only what exists at launch.** Anything the user says will come "later" goes into `roadmap_features` and is never classified.
2. **Adjectives are not facts.** "Seamless experience", "proprietary algorithm", "powerful AI" count only if they map to a concrete feature, data source, or operation. Otherwise ignore them.
3. **Tag the source of every judgment:**
   - `[stated]`: the user said it explicitly
   - `[inferred]`: follows directly from what the user said
   - `[assumed]`: a conservative assumption made because information is missing
4. **When unsure, pick the earlier (more conservative) class.** Every table is ordered from most to least conservative.
5. **Structure, not subject matter.** "Travel", "health", "education" decide nothing on their own.
6. **A feature is not a type.** A booking button does not make a product transactional; a comment section does not make it a community. Only the removal test in Step 3 decides the type.

---

## Step 0: Information check

Before decomposing, you need all of the following:

- Who the target users are
- What users put in each time, what they get out, and what they do next
- Where the product's data comes from
- Whether transactions, bookings, or delivery happen inside the product, and whose supply it is
- In what situation and on what device people use it

If the user gave a URL, screenshots, or a PRD, read them first. If anything is still missing, ask **at most 3** of the most important questions at once. If the user does not answer or says "your call", continue with conservative assumptions and record them in `assumptions`.

## Step 1: Project summary

- `one_liner`: one sentence, about 20 words max. What it does, not how good it is.
- `target_users`
- `market`
- `rival_ai_clients`: the general-purpose AI clients users in this market actually use (e.g. ChatGPT, Claude, Gemini; for mainland China, Doubao, DeepSeek, Qwen).
- `acquisition`: where users mainly come from (search engines, app stores, social sharing, offline, sales team, partners).
- `search_acquisition`: `true` if the product mainly depends on search engines sending **answer-seeking** traffic, else `false`. Paid search that brings transactional traffic (e.g. hotel bookings) does not count.
- `launch_features`
- `roadmap_features` (never classified)

## Step 2: Usage modes and core steps

A **usage mode** is a distinct situation in which people use the product, e.g. "pre-trip planning" and "during the trip". Most products have 1 to 3.

For each mode:

- `share`: share of total usage, estimated by amount of activity, rounded to 10%. All modes sum to 100%.
- `steps`: each step as "input → what the product does → output", with its `share` within the mode (rounded to 10%, summing to 100%).
- `next`: where the user goes and what they do after this mode.

**Comparison and shopping-guide products need one more split:** if the product has steps **completed inside the product** (loan pre-qualification, a quote from a licensed insurance agent, booking a property tour), make that a separate mode. Do not merge it with "reading comparisons". The two modes usually relate to AI clients in opposite ways.

Finally, mark the **value realization point** `value_realization`:

- `in_product`: the user gets the benefit inside the product
- `elsewhere`: the benefit is realized somewhere else (say where)
- `mixed`: both (describe each)

## Step 3: Service type

The type is decided by the **core output**: what the user has in hand after using the product. Follow 3.1 → 3.4 in order.

### 3.1 Find each launch feature's output

For every item in `launch_features`, answer "what does the user have after using this?" and map it to a candidate type.

| Code | Type | Core output | Test question | Commonly confused with |
|---|---|---|---|---|
| `generate` | Generate / advise | Content **newly made for this request**: plans, advice, copy, images, code, chat replies | Did this content exist before the request? If not, this type | Content already existed and was only found → `retrieve` |
| `retrieve` | Retrieve / aggregate | Information that **already existed** and was found and organized: news, prices, policies, listings | Can the user find this information elsewhere? If yes, this type | The user places an order in your UI → see transactions |
| `tool` | Tool / editor | A work **made by the user's own hands**: designs, documents, videos, sheets | Who is the main author, the user or the product? If the user, this type | The product generates and the user only tweaks → `generate` |
| `record` | Record / manage | Records **accumulated over time**: books, logs, customer data, check-ins | Is the value in this one output, or in the accumulated history? If history, this type | A single output is valuable on its own → `tool` or `generate` |
| `transact_front` | Transaction front end | An order **placed in your UI**, but payment and after-sales are someone else's | Is the ordering flow completed in your UI? Who does the user pay? | Only a link out → not a transaction (see rules below) |
| `transact_own` | Merchant of record | An order **you close and are responsible for**: you take payment, you handle changes, refunds, and support. Supply may be owned or contracted | Who does the user pay, and who do they call when it goes wrong? If you, this type | Payment or support is elsewhere → `transact_front` |
| `community_info` | Information community | Answers and experience written **by other users** | Replacement test in 3.4 | Answers are generated by the product → `generate` |
| `community_social` | Relationship community | **Relationships and interaction** with other people | Replacement test in 3.4 | — |
| `practice` | Practice / habit | **A change in the user's own ability or habits**: learned it, got better, kept it up. Content and tools are only vehicles | Could someone else or an AI do this for the user? If not, this type | The user only wants the result (the answer, not the skill) → `generate` or `retrieve` |

Two special rules:

- **A link out is not a transaction.** A feature that only sends the user to another site or app to buy (shopping guides, price-comparison click-outs, affiliate links, "book on X" buttons) is not a transaction type. Treat it as `retrieve` or an accessory feature, and record execution as L1 in the business layer.
- **"AI generates, user edits" products** (e.g. AI-generated posters with manual tweaks): decide the primary type with the removal test in 3.2, not by impression.

### 3.2 Removal test: the primary type

For each candidate type from 3.1, ask: **if every feature of this type were removed, would the product still stand? Would users still have a reason to come?**

- The type whose removal breaks the product is `primary_type`.
- If several would break it (rare), pick the one users use first and most each time they open the product.
- Check against how the user describes the product: the primary type should match the core action ("helps you plan trips" → `generate`, "helps you track spending" → `record`). If it does not, redo the removal test and explain in `type_checks`.

### 3.3 Secondary type

A candidate becomes `secondary_type` (at most one) only if **both** hold:

- Removing it leaves the product standing but clearly worse
- It accounts for at least 20% of activity in the core loop

Otherwise it is an accessory feature, not a type.

### 3.4 Sub-type checks

Only when the primary or secondary type is a transaction or community type:

- **Transactions:** who does the user pay, and who handles refunds and support?
  - Both you → `transact_own`
  - Ordering happens in your UI but payment or support is elsewhere → `transact_front`
- **Transactions also need a deliverable check: can AI directly produce what the user buys here** (services, assets, courses, content)? If yes, set `deliverable_ai_replaceable: true`. Examples: simple design, copywriting, or translation gigs; stock images; recorded courses. However good the transaction layer is, once AI satisfies the demand itself, transaction moats are empty.
- **Communities, replacement test:** if other users' content were replaced with AI-generated content of the same quality, would users still come?
  - Yes (they want answers) → `community_info`
  - No (they want people) → `community_social`

### Common confusions

| Pair | How to tell |
|---|---|
| `generate` vs `tool` | Who is the main author; if unsure, run the removal test |
| `generate` vs `retrieve` | Did the content exist before the request? |
| `generate` vs `community_info` | Generated by the product, or written by other users? |
| `retrieve` vs `transact_front` | Is ordering completed in your UI? A link out is `retrieve` |
| `transact_front` vs `transact_own` | Who takes payment and who owns support |
| `tool` vs `record` | Value in this one work, or in accumulated history |
| `community_info` vs `community_social` | Replacement test |

### Reference classifications

| Product shape | Primary | Secondary | Why |
|---|---|---|---|
| Generates a travel itinerary from a destination, map editing, hotel booking links | `generate` | `tool` | Without generation the product breaks; map editing is a large share but removable; booking is only a link out |
| Price-comparison site that clicks out to stores | `retrieve` | — | Prices already exist; a click-out is not a transaction |
| Hotel booking platform that takes payment and handles changes | `transact_own` | `retrieve` | Users pay the platform and call it when things go wrong; contracted supply still counts |
| AI poster generator with manual text tweaks | `generate` | — | AI is the main author; tweaks are a small share |
| Online design tool with AI image fill | `tool` | `generate` (if AI fill ≥ 20% of activity) | Remove AI fill and the tool still stands |
| Expense tracker with automatic monthly reports | `record` | — | Value is in the accumulated books; reports are accessory |
| Programming Q&A community | `community_info` | — | Replacement test: with AI answers, users no longer need to come |
| Hobbyist community | `community_social` | — | Users come for like-minded people |
| AI companion chat app | `generate` | — | Every reply is newly generated for this conversation |
| Language-learning app with daily lessons and streaks | `practice` | — | Users want to learn it themselves; no one can do it for them |
| Flashcard app that also lets you search others' decks | `practice` | `retrieve` | Remove practice and it breaks; deck search is a large share but removable |
| Food-delivery front end that forwards orders to merchants who take payment | `transact_front` | `retrieve` | Ordering happens here; payment and support are the merchant's |

## Step 4: Business-layer facts

For each of the 6 business dimensions, write the facts (with source tags), then pick a level L0–L5 from Table A.

## Step 5: Frontend-layer classification

The frontend layer has 8 aspects, filled at two levels. Definitions are in Table B.

**Mode level** (once per usage mode):

| Field | Aspect | Extra field |
|---|---|---|
| `frequency` | Frequency & speed | If D or E, set `automatable`: `must_do_yourself` or `automatable` (the action exists only because nobody does it for the user). **Lookup actions (looking up words, answers, references, information) are always `automatable`**, even in paper-book settings |
| `intent` | Seeking vs browsing | If C or D, set `content_source`: `human_or_real` or `ai_or_scraped` |
| `scenario` | Context of use | — |
| `experience` | Experience as the end | Set `chat_reproducible`: could this exact experience happen in a chat box? (true/false) |
| `relation` | Relation with AI clients | From Table C, **judged separately for each mode** (Step 6) |

**Step level** (once per step):

| Field | Aspect | Extra field |
|---|---|---|
| `input` | Input cost | — |
| `precision` | Precision control | If E, set `recurring`: a system that runs on fixed rules repeatedly (true) or a one-off need (false) |
| `consumption` | Read once vs monitor | — |
| `device` | Device capability | If B, C or D, set `platform_generic`: does this capability come from a general platform that AI clients can also connect to? (true/false) |

Attach a one-line `evidence` to every classification naming the concrete feature or operation.

## Step 6: Relation with AI clients

**Judge each usage mode separately** with Table C and put the class in that mode's `relation`. Do not judge the whole product once: in the same product, "building a website" may be replaced outright while "running the site day to day" is a system AI cannot bypass. The scorer combines modes by share.

**Before judging A (replaced directly), run the information check: can an AI client get the information needed to answer?** Information that exists only inside your product, such as real-time, hyperlocal, or private data (what a neighbor just posted, what happened on this street last night, the user's own records), is out of AI's reach, so that mode is not A. Information that is widely available online (travel guides, encyclopedic knowledge, public reviews) can be A.

## Step 7: Target users' AI habits

Pick `ai_habit` from Table D. This is a risk note only; it is never scored.

## Step 8: Quality gates

Assess only if the user provided an existing product, demo, or screenshots; otherwise set all to `unknown`.

For visual, performance, stability, and accessibility, set `pass`, `fail`, or `unknown`. A `fail` must name the specific problem.

## Step 9: Self-check

Before output, check every line:

- [ ] Shares sum to 100% across modes and across steps within each mode
- [ ] Nothing in `roadmap_features` appears in any classification
- [ ] Every classification has `evidence` with a source tag
- [ ] The primary type came from the removal test and matches how the user describes the product
- [ ] No link out was treated as a transaction; sub-type checks were done only for transaction and community types
- [ ] The secondary type meets both "clearly worse without it" and "≥ 20% of activity"
- [ ] Intermittent products (travel, home renovation, job hunting) use annual-average frequency
- [ ] Taking photos, recording audio, or uploading files was not counted as device capability
- [ ] "Nice UI" or "smooth experience" was not used as evidence anywhere
- [ ] Every uncertain call took the more conservative class

## Output

Two parts:

1. **The decomposition card (JSON)**, schema as in the example at the end.
2. **A 3–5 line summary**: one-liner, primary type, core loop, value realization point, and the 2 most consequential assumptions. No evaluation.

Then hand the card to the review step (`references/review.md`). Do not compute any scores here.

---

## Table A: Business-layer levels (L0–L5)

### Proprietary data `data`
- **L0**: Only public information or the model's own knowledge
- **L1**: Has data, but an AI client can get it by browsing or from a user upload
- **L2**: A self-built dataset that someone else could assemble in a few weeks
- **L3**: Real-time or licensed data (inventory, prices, partner APIs) that requires business relationships
- **L4**: Data generated by users through use, and it clearly makes the product better
- **L5**: A data flywheel: more users → better data → more users

### Accumulated state `state`
- **L0**: Every use is independent; use and leave
- **L1**: Keeps history, but losing or exporting it does not matter
- **L2**: Personalization that an AI client's memory could also provide
- **L3**: Users accumulate things they keep maintaining (projects, itineraries, documents)
- **L4**: What accumulates is deeply structured; migrating out takes a lot of manual work
- **L5**: The product is the user's single source of truth in this domain

### Execution `action`
- **L0**: Gives advice only; the user acts elsewhere
- **L1**: Gives a link out to act elsewhere
- **L2**: Does simple actions for the user that an AI agent could also do (fill forms, send emails)
- **L3**: Completes transactions or bookings in-product via partner integrations
- **L4**: Involves money, fulfillment, or offline delivery requiring licenses, contracts, or a supply chain
- **L5**: Is the fulfiller itself (inventory, service, hardware, logistics)

> Clarification: execution asks **whether the user's task actually gets done here.** Selling hardware does not count by itself; for hardware products, look at the task the user accomplishes with it.

### Network & collaboration `network`
- **L0**: Single user
- **L1**: Results can be shared
- **L2**: Supports collaboration, but it is not the core scenario
- **L3**: The core scenario needs several people
- **L4**: Multi-sided: one side attracts the other (buyers and sellers, creators and audiences)
- **L5**: Strong network effects: more users make it more valuable for each user, and hard to leave

### Workflow & distribution `workflow`
- **L0**: A standalone site the user has to remember to open
- **L1**: Shallow plugins or integrations, or only available as a plugin inside an AI client
- **L2**: Connected to tools the user already uses, reducing switching
- **L3**: A fixed step in some process (approval, publishing, delivery)
- **L4**: Deeply embedded in business processes; replacing it breaks other systems
- **L5**: Owns channels general AI clients cannot reach (industry relationships, offline networks, preinstallation, exclusive partnerships)

> Cap: integrations embedded in someone else's platform (browser extensions, plugins, mini-apps inside another app) score **at most L2**. The platform owner can ship the same thing natively at any time.

### Trust & accountability `trust`
Only "who is accountable when it goes wrong". Whether results are deterministic and repeatable belongs to precision control in the frontend layer.
- **L0**: Errors don't matter; users judge for themselves
- **L1**: Errors are a minor nuisance
- **L2**: Errors cost money or time, but users can notice and fix them
- **L3**: Errors are costly and users need someone accountable (finance, legal, health, safety)
- **L4**: Requires licenses, certification, or professional endorsement, e.g. transactions completed by licensed people (insurance agents, loan brokers)
- **L5**: Brand trust is itself the reason to buy, built over a long time

---

## Table B: Frontend-layer classes

### Input cost `input` (step level)
What does the user have to put in to complete this step?
- **A. One-sentence instruction**: clear need, says it in one sentence. Photos, voice, or uploaded files as input also count here.
- **B. Multi-field entry**: several conditions, but the user knows them
- **C. Pick or compare a few**: choose among a few visible options, or compare a few
- **D. Visual scan of many**: scan dozens to hundreds of visual options and pick by feel
- **E. Continuous adjustment**: adjust while watching the result, converging step by step
- **F. Direct spatial manipulation**: position, shape, or layout is itself the input

### Frequency & speed `frequency` (mode level, annual average)
- **A. Rare**: monthly or less
- **B. Medium, long sessions**: a few times a week, 5+ minutes each
- **C. Medium, short sessions**: a few times a week, under a minute each
- **D. Frequent micro-actions**: several times a day, seconds to a minute each
- **E. Continuous micro-actions**: daily, dozens to hundreds of small decisions per session

### Precision control `precision` (step level)
- **A. Roughly right is fine**: wide tolerance; different results each time are fine
- **B. Precise but easy to state**: clear requirements that can be put in words
- **C. Local edit**: change one spot, everything else must stay exactly as is
- **D. Decide by seeing**: precise to the pixel, millisecond, or value, and you only know it is right when you see it
- **E. Deterministic and repeatable**: the same input must give the same output, every step traceable

### Seeking vs browsing `intent` (mode level)
- **A. A specific question**: comes with a question, wants an answer
- **B. A goal, exploring options**: knows what they want, not which one
- **C. Loose interest, decides while browsing**: vague direction, relies on browsing and serendipity
- **D. Pure leisure browsing**: no goal, scrolling for fun

### Read once vs monitor `consumption` (step level)
- **A. Read once**: done after reading
- **B. Occasionally revisited**: saved and maybe reopened later
- **C. Tracking a changing state**: the state updates, the user checks back now and then
- **D. Always visible, glanceable**: needs to stay in view or be one glance away
- **E. Real-time monitoring with immediate reaction**: changes by the second, needs action now

### Context of use `scenario` (mode level)
- **A. Focused, sitting at a screen**
- **B. Fragmented time on the move**
- **C. Hands busy, eyes available**: navigation, cycling, checking stats mid-workout. If both hands and eyes are busy and only voice works, choose A.
- **D. On site, offline**: the interface is part of an on-site process (scan-to-order, ticket check, pickup)
- **E. Dedicated device**: car, watch, TV, kiosk, point of sale

### Device capability `device` (step level)
- **A. None needed, or only a one-off photo, recording, or upload**
- **B. Notifications, widgets, lock screen**
- **C. Continuous background sensing**: continuous location, step counting, heart rate, live camera overlay
- **D. External hardware**: Bluetooth or NFC devices, smart home, medical devices, POS

> Clarification: if a phone plus an AI client can do the same hardware function (e.g. scan text and translate it, which a phone photo can do), classify it as A. Only capabilities a phone cannot provide (continuous heart rate or temperature, controlling dedicated equipment) count as C or D.

### Experience as the end `experience` (mode level)
- **A. Pure means**: only the result matters; the faster the better
- **B. Mostly means**: a good experience helps, but users take any shortcut
- **C. Growth and practice**: the user wants to get better; the result cannot be delegated
- **D. Aesthetics, collecting, ritual**: owning and appreciating is itself the value
- **E. Entertainment and games**: the process is the whole value

---

## Table C: Relation with AI clients `relation` (per mode)

Imagine the user brings up your domain inside an AI client. What happens next?
- **A. Replaced directly**: the AI can do what you do by itself
- **B. Callable but thin**: what you expose is public data or a generic capability; the AI can call someone else or search on its own
- **C. Data source**: the AI needs your data to answer, but the user's transaction or action does not happen with you, and the browsing layer moves into the AI client. For a frontend product this **leans toward substitution**, because users no longer need to open your interface
- **D. Executor**: the AI only initiates; the transaction or action is completed with you (payment happens with you, editing happens in your editor)
- **E. System of record**: you are the single source of truth; the AI must read and write your system to get anything done
- **F. Parallel**: the user must do this themselves and the AI can only assist (coach, quiz, advise), e.g. practice, exercise, browsing and collecting in person

## Table D: Target users' AI habits `ai_habit`

- **A. Heavy AI users**: developers, students, knowledge workers
- **B. Mainstream users who use AI occasionally**
- **C. Groups who rarely use AI**: older adults, some frontline workers
- **D. Environments where general AI is not allowed**: intranets, classified work, compliance restrictions

---

## Example card

A travel itinerary generator with map editing and hotel booking links. Format only; do not borrow its subject matter when classifying.

```json
{
  "project": {
    "one_liner": "Generates a travel itinerary for a destination and lets you adjust it on a map",
    "target_users": "Young independent travelers [stated]",
    "market": "Mainland China",
    "rival_ai_clients": ["Doubao", "DeepSeek"],
    "acquisition": "App stores and social sharing [assumed]",
    "search_acquisition": false
  },
  "launch_features": ["Itinerary generation", "Hotel list with live prices", "Drag-to-edit itinerary on a map", "Group voting with travel companions", "Link out to book hotels on a third-party platform", "Lock-screen itinerary card"],
  "roadmap_features": ["Own guesthouse inventory"],
  "assumptions": [
    "Hotel prices and availability come from a third-party platform API [assumed]",
    "Bookings are completed on the third-party platform [assumed]"
  ],
  "value_realization": {"type": "mixed", "note": "Itinerary management happens in the product; booking happens on the third-party platform"},
  "primary_type": "generate",
  "secondary_type": "tool",
  "type_checks": {
    "candidates": {"generate": "Itinerary generation", "retrieve": "Hotel list with live prices", "tool": "Drag-to-edit itinerary on a map"},
    "removal_test": {
      "generate": "Without it the product breaks: users come to get an itinerary",
      "retrieve": "Removable; 15% of activity, below the secondary threshold",
      "tool": "Removable but clearly worse; 45% of activity, so it is the secondary type"
    },
    "pitch_check": "The user describes it as 'plans your trip for you', consistent with generate [stated]",
    "not_transaction": "Booking is only a link out to a third-party platform",
    "subtype": null
  },
  "deliverable_ai_replaceable": false,
  "business": {
    "data": {"level": "L3", "evidence": "Live prices and availability require a partner API [assumed]"},
    "state": {"level": "L3", "evidence": "Users keep maintaining their itineraries [inferred]"},
    "action": {"level": "L1", "evidence": "Booking links out to a third-party platform [assumed]"},
    "network": {"level": "L3", "evidence": "Travel companions vote on itinerary changes together [stated]"},
    "workflow": {"level": "L0", "evidence": "Standalone app with no integrations [inferred]"},
    "trust": {"level": "L1", "evidence": "Users can fix itinerary mistakes themselves [inferred]"}
  },
  "modes": [
    {
      "name": "Pre-trip planning",
      "share": 0.5,
      "next": "Book hotels on the third-party platform",
      "relation": {"class": "A", "evidence": "AI clients can generate itineraries and call booking platforms directly for live prices [inferred]"},
      "frequency": {"class": "A", "evidence": "A few trips a year [inferred]"},
      "intent": {"class": "B", "evidence": "Knows the destination, needs to choose hotels and sights [inferred]"},
      "scenario": {"class": "A", "evidence": "Plans at home on phone or laptop [inferred]"},
      "experience": {"class": "B", "chat_reproducible": false, "evidence": "Planning with companions is fun, but it is mainly a means to travel [inferred]"},
      "steps": [
        {"desc": "Enter destination, dates, party size → generate itinerary → draft itinerary", "share": 0.2,
         "input": {"class": "A", "evidence": "One sentence is enough"},
         "precision": {"class": "A", "evidence": "A rough first draft is fine"},
         "consumption": {"class": "A", "evidence": "Read once, then move to editing"},
         "device": {"class": "A", "evidence": "No special capability"}},
        {"desc": "Browse hotel list with live prices → pick one → link out to book", "share": 0.3,
         "input": {"class": "C", "evidence": "Choose among a few hotels"},
         "precision": {"class": "B", "evidence": "Price and dates are easy to state"},
         "consumption": {"class": "A", "evidence": "Done once chosen"},
         "device": {"class": "A", "evidence": "No special capability"}},
        {"desc": "Drag sights and days on the map → updated itinerary", "share": 0.5,
         "input": {"class": "F", "evidence": "Drag points on the map to reorder [stated]"},
         "precision": {"class": "C", "evidence": "Change one day, leave the others untouched"},
         "consumption": {"class": "B", "evidence": "Revisited before departure"},
         "device": {"class": "A", "evidence": "No special capability"}}
      ]
    },
    {
      "name": "During the trip",
      "share": 0.5,
      "next": "Follow the itinerary",
      "relation": {"class": "B", "evidence": "AI clients can also keep and show an itinerary and adjust it on request [inferred]"},
      "frequency": {"class": "C", "evidence": "Intense during the trip but only medium on an annual average [inferred]"},
      "intent": {"class": "A", "evidence": "Check today's plan"},
      "scenario": {"class": "C", "evidence": "Glancing at the map while walking [inferred]"},
      "experience": {"class": "A", "chat_reproducible": false, "evidence": "Only to confirm plans"},
      "steps": [
        {"desc": "Check today's itinerary and order status", "share": 0.6,
         "input": {"class": "A", "evidence": "Open and look"},
         "precision": {"class": "A", "evidence": "Viewing only"},
         "consumption": {"class": "D", "evidence": "Lock-screen itinerary card [stated]"},
         "device": {"class": "B", "platform_generic": false, "evidence": "Lock-screen card and reminders"}},
        {"desc": "Adjust one day on the fly", "share": 0.4,
         "input": {"class": "F", "evidence": "Drag on the map"},
         "precision": {"class": "C", "evidence": "Only today changes"},
         "consumption": {"class": "B", "evidence": "Re-checked after the change"},
         "device": {"class": "A", "evidence": "No special capability"}}
      ]
    }
  ],
  "ai_habit": {"class": "B", "evidence": "Young users who use AI occasionally [inferred]"},
  "quality_gates": {"visual": "unknown", "performance": "unknown", "stability": "unknown", "accessibility": "unknown"}
}
```
