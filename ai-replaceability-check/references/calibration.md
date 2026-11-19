# Calibration cases

41 real products scored with rules v4 and compared with what actually happened between 2023 and 2026. Rounds 2 and 3 were blind tests: predictions were locked before outcomes were checked. Full cards, evidence, and the locked prediction files are in the repository's `calibration/` folder.

## How to use this table

Before writing the report, find 1–2 cases with the **same primary type and a similar relation pattern**. If your card is more generous than a similar case that collapsed or came under pressure, either name the concrete difference or downgrade (see `review.md`, item 12).

Outcomes: **Collapsed** (core business replaced), **Pressured** (growth stalled or traffic fell, with AI cited as a cause), **Resilient** (still growing), **Benefiting** (AI became a tailwind).

| Product | Round | Type | Relation by mode | v4 level | Outcome | Lesson |
|---|---|---|---|---|---|---|
| Chegg (homework answers) | 1 (in-sample) | Retrieve / aggregate | A 100% | High risk | Collapsed | Pure answer lookup; every frontend aspect near 0, and AI gives the answer faster. |
| Stack Overflow | 1 (in-sample) | Information community | A 80%, A 20% | High risk | Collapsed | The network protected content production, which AI absorbed; asking itself moved into the IDE. |
| Tome (AI slide generation) | 1 (in-sample) | Generate / advise + Tool / editor | A 100% | High risk | Collapsed | Classic generate-type ending: rare use, no state, no export, no workflow. |
| Jasper (early AI copywriting) | 1 (in-sample) | Generate / advise | A 100% | High risk | Collapsed | Survived only by moving to brand voice (state) and marketing workflows. |
| Quizlet (flashcards) | 1 (in-sample) | Practice / habit + Retrieve / aggregate | A 40%, F 60% | High risk | Pressured | The practice half held up; the look-up half was taken by AI. |
| Grammarly | 1 (in-sample) | Generate / advise | B 100% | High risk | Pressured | Embedding inside other platforms and precise local edits did not protect it. |
| Duolingo | 1 (in-sample) | Practice / habit | F 100% | Hard to replace | Resilient | Daily practice no one can do for you, plus data and streaks. |
| Pinterest | 1 (in-sample) | Retrieve / aggregate + Record / manage | F 60%, F 40% | One moat | Resilient | Proprietary taste graph; people come to browse, not to ask. |
| Booking.com | 1 (in-sample) | Merchant of record + Retrieve / aggregate | D 60%, D 40% | Hard to replace | Resilient | Its moats are all in the business layer; AI calls it and the booking stays with it. |
| Strava | 1 (in-sample) | Record / manage + Relationship community | E 50%, F 50% | Hard to replace | Resilient | Near-max business layer; workouts must be done yourself; system of record for athletes. |
| Reddit | 1 (in-sample) | Relationship community + Information community | F 60%, C 40% | Hard to replace | Resilient | People keep the browsing half alive; the answer half feeds AI. |
| Figma | 1 (in-sample) | Tool / editor | D 80%, E 20% | Hard to replace | Benefiting | Continuous direct manipulation plus system of record; AI output is edited in Figma. |
| Canva | 1 (in-sample) | Tool / editor + Retrieve / aggregate | D 100% | One moat | Benefiting | No item reaches 4; it benefits because AI-generated designs get edited in Canva. The one remaining mild miss. |
| Notion | 1 (in-sample) | Record / manage + Tool / editor | E 60%, E 40% | Hard to replace | Benefiting | The team's source of truth; AI agents work inside it. |
| Uber (rides) | 2 (blind) | Merchant of record | D 100% | Hard to replace | Resilient | Real-world fulfillment and live tracking; AI clients call it. |
| Meituan food delivery | 2 (blind) | Merchant of record | D 100% | Hard to replace | Resilient | Own delivery fleet; the order dip came from a subsidy war, not AI. |
| Roblox | 2 (blind) | Relationship community | F 80%, F 20% | Hard to replace | Resilient | Play is the value; the dip came from an exceptional prior year. |
| Spotify | 2 (blind) | Retrieve / aggregate + Record / manage | D 100% | Hard to replace | Resilient | Listening is the end; playback happens in Spotify even when AI picks the song. |
| Oura Ring | 2 (blind) | Record / manage + Practice / habit | E 100% | Hard to replace | Resilient | Sensors a phone cannot replicate plus years of body data. |
| Youdao Dictionary Pen | 2 (blind) | Retrieve / aggregate + Generate / advise | A 100% | High risk | Pressured | A phone plus AI does the same scan-and-translate. |
| Zhihu | 2 (blind) | Information community | A 60%, F 40% | High risk | Pressured | Public answers absorbed by AI; the browsing half alone is not enough. |
| Xiaohongshu (RedNote) | 2 (blind) | Relationship community + Information community | F 60%, A 40% | One moat | Pressured | Browsing holds, but the guide-search half shifted to AI; first decline in time spent. |
| Fiverr (freelance marketplace) | 2 (blind) | Merchant of record + Retrieve / aggregate | A 100% | High risk | Collapsed | A strong marketplace, but simple gigs became AI-doable and SEO traffic dried up. |
| Shutterstock (stock images) | 2 (blind) | Retrieve / aggregate + Merchant of record | A 100% | High risk | Pressured | Licensing trust did not protect demand for generic images. |
| Yelp (local reviews) | 2 (blind) | Information community | C 100% | High risk | Pressured | A data source for AI: licensing grew while ad clicks fell. |
| Udemy (video courses) | 2 (blind) | Practice / habit + Merchant of record | A 100% | High risk | Pressured | Recorded courses were replaced by AI tutoring on the consumer side. |
| Keep (follow-along workouts) | 2 (blind) | Practice / habit + Retrieve / aggregate | F 70%, F 30% | High risk | Pressured | Practice type but no moat; the decline predates AI. |
| Wix (website builder) | 2 (blind) | Tool / editor | B 40%, E 60% | One moat | Resilient | AI replaced building the site, not running it. |
| Bilibili | 3 (blind) | Relationship community + Information community | F 70%, A 30% | Hard to replace | Resilient | Creators and community carry it; the learning-video half is exposed but small. |
| LinkedIn | 3 (blind) | Relationship community + Retrieve / aggregate | F 40%, D 35%, E 25% | Hard to replace | Resilient | Professional identity as system of record; applications complete there. |
| Nextdoor (neighborhood network) | 3 (blind) | Relationship community + Information community | F 60%, F 40% | One moat | Resilient | Hyperlocal, real-time information AI cannot reach. |
| Substack (paid newsletters) | 3 (blind) | Relationship community | F 70%, F 30% | One moat | Resilient | People pay for specific writers. |
| Discord | 3 (blind) | Relationship community | F 80%, F 20% | Hard to replace | Resilient | Friends and groups; the chat itself is the experience. |
| Quora | 3 (blind) | Information community | A 80%, F 20% | High risk | Pressured | Answers reached from search, absorbed by AI. |
| SMZDM (deal-sharing community) | 3 (blind) | Information community + Retrieve / aggregate | A 60%, A 40% | High risk | Pressured | The legacy deal feed shrank; it now sells its data to AI agents. |
| Wikipedia (readers) | 3 (blind) | Information community | C 90%, F 10% | High risk | Pressured | AI answers from its content; human pageviews fell 8%. |
| Tripadvisor (reviews site) | 3 (blind) | Information community + Retrieve / aggregate | C 70%, A 30% | High risk | Collapsed | Function replaced and search channel cut at the same time. |
| Glassdoor (company reviews) | 3 (blind) | Information community | C 100% | High risk | Pressured | Public review data; folded into Indeed. |
| NerdWallet (financial product comparison) | 3 (blind) | Retrieve / aggregate | C 50%, D 30%, B 20% | One moat | Resilient | Pre-qualification and licensed agents inside the product carried growth. |
| Zillow (listings) | 3 (blind) | Retrieve / aggregate + Transaction front end | C 70%, D 30% | Hard to replace | Resilient | Home browsing people want to do themselves; agent contact happens in Zillow. |
| Etsy (handmade marketplace) | 3 (blind) | Merchant of record + Retrieve / aggregate | C 70%, D 30% | Hard to replace | Resilient | Physical handmade goods AI cannot make; purchases complete on Etsy. |

## Patterns worth remembering

- **Answer-seeking modes are where products lose.** Chegg, Stack Overflow, Quora, Zhihu, Wikipedia, and the search halves of Xiaohongshu and Reddit.
- **Being the place where things get done protects.** Booking, Uber, Figma, Canva, Notion, LinkedIn, and Wix's operations side.
- **People and practice protect:** Duolingo, Strava, Discord, Substack, Nextdoor.
- **A strong marketplace does not protect a demand AI can meet directly:** Fiverr, Shutterstock, Udemy.
- **Search dependence plus a substitute relation is the worst combination:** Tripadvisor, Fiverr, Chegg.
- **Non-AI forces still dominate some outcomes** (subsidy wars, an exceptional prior year, post-pandemic fitness decline). The framework does not measure them.
