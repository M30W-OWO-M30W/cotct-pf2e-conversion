# Research Index — Curse of the Crimson Throne PF1e → PF2e

Compiled Phase 1 (2026-06-09) via 5 parallel research sweeps + the AP text.
Raw structured digest: `.work/digest_research.txt` (git-ignored).

**Source priority** (per project spec): 1) official PF2e rules/errata → 2) the
PF1e AP text (2016 Anniversary hardcover, our source) → 3) official PF2e
published equivalents → 4) strong community consensus → 5) GM-provided community
docs → 6) individual forum/reddit posts → 7) labeled design judgment.

**Reliability legend:** `OFFICIAL` · `CONSENSUS` (strong community) · `UNVERIFIED`
(useful but unconfirmed) · `LOW`.

---

## A. Primary community conversion — Olliebird (the GM-provided resource)

The Reddit thread the GM linked. Author **u/Olliebird**, ~2-year project, v1.0
posted ~June 2021 in r/Pathfinder2e, developed/playtested in Ediwir's *A Series
of Dice-Based Events* Discord. Delivered as **7 public Google Docs** (intro + one
per chapter), **keyed to the CotCT Anniversary Edition** — i.e. our exact source.

| # | Source | Reliability | Key content | Decision |
|---|--------|-------------|-------------|----------|
| A1 | [Reddit o34twp announcement](https://www.reddit.com/r/Pathfinder2e/comments/o34twp/full_mostly_conversion_of_the_curse_of_the/) — u/Olliebird, 2021-06 | CONSENSUS | Scope = "full (mostly)"; **only treasure deliberately not converted**; Harrow kept as-written (+1/+2 bonuses); playtested | **Adopt** as primary reference to read first |
| A2 | [Intro / methodology Google Doc](https://docs.google.com/document/d/1TR8s94mhT9N2yFUzVTeMLgrn4feAECYm2AMedq8s-KU/edit) | CONSENSUS | Requires Anniversary Ed.; **milestone leveling** + per-chapter advancement track; two-tier creature method (map to official 2e OR custom on monster.pf2.tools); DCs from Level-Based + Simple DC tables; **treasure = GM's job** (points to CRB Table 10-9) | **Adopt** methodology; **treasure gap is ours to fill** |
| A3 | [Ch1 Edge of Anarchy doc](https://docs.google.com/document/d/170X0H7rZH7dkgtANKF3k6gs_bQKm6sgNFW2PrpelBP4/edit) | CONSENSUS | Area-keyed (Zellara's, Old Fishery A1–A14). Swaps: Bloo=Guard Dog, Gobblegut=Crocodile, Jigsaw Shark=Razortoothed Shark (PFS 2-06); custom: Yargin, Hookshanks, Giggles, **Gaedren Lamm**, Drain Spider. Party→lvl 2 after Fishery | **Adopt** as pilot cross-ref |
| A4 | [Ch2 Seven Days doc](https://docs.google.com/document/d/17YX2kyfz-mqPtK9lieFlPg63DHgO_IgEMN_3IKRwwaA/edit) | CONSENSUS | **Blood Veil = native 2e staged disease** (Fort DC 24–30, crit-fail skips onset); Vat-of-Blood-Veil hazard (Hard 18/HP 72/BT 36); Physicians = 5 Missions; Queen's Physician=Surgeon (GMG 222) | **Adopt** (review DCs vs level) |
| A5 | [Ch3 Escape from Old Korvosa doc](https://docs.google.com/document/d/1CzybQx7hNVVK9IL4dPB2QZQHVYiCbZlsvDe-LNtS1wA/edit) | CONSENSUS | Red Mantis Assassin & **Laori Vaus** custom (recurs Bk5); Otyugh; Yellow Mold hazard; social = scaling skill DCs (19/22/24/29), not formal Influence | **Adopt**; layer Influence on top per our subsystem plan |
| A6 | [Ch4 A History of Ashes doc](https://docs.google.com/document/d/1vqrIpiCctLGcs5D49ffAL8ubDojcMiVJSTuMWrbGuNY/edit) | CONSENSUS | Cinderlands = Survival tracking DCs; **Trials of Respect = skill challenges + condition clocks** (Totem: Athletics DC15/6h, fatigued→enfeebled ladder) | **Partially adopt**; we'll formalize as Victory-Point subsystem |
| A7 | [Ch5 Skeletons of Scarwall doc](https://docs.google.com/document/d/19WIQNAvwJcG9HHsZ9NXMRQWHfQyQSznI--NeP6wTbjA/edit) | CONSENSUS | Largest doc; **Unhallow/Forbiddance preserved** (Ritual 7 @ lvl10, DC 34 Will); clustered weak encounters intentional (patrol+Unhallow interplay — don't rebalance in isolation) | **Adopt with GM review** |
| A8 | [Ch6 Crown of Fangs doc](https://docs.google.com/document/d/1X5OpUKSK_e4e3tBYrkjNteX05SIyWv5ms4AbYtl8GOA/edit) | CONSENSUS | Smallest doc; area-keyed finale; high-level builds credited to playtester MediumRare | **Adopt with GM review** (expect most original balancing/treasure work here) |
| A9 | [A Series of Dice-Based Events Discord](https://discord.gg/eEHAyHW) | UNVERIFIED | Dev/support hub; "Crimson Throne" channel; errata/Q&A | GM review — join for errata & treasure crowdsourcing |
| A10 | [Olliebird published guide (Pathfinder Infinite)](https://www.pathfinderinfinite.com/en/product/375718/Curse-of-the-Crimson-Throne-Second-Edition-Conversion-Guide) ~147pp | UNVERIFIED | Polished/compiled paid edition of the same work; advancement tracks render properly here | GM review — buy if you want the clean tracks |

> **Conversion gap to own:** Olliebird's "mostly" = **treasure is unconverted**.
> That is the single largest GM-prep burden and becomes a core deliverable of
> *this* project (`reports/treasure_report.md` + per-chapter treasure parcels to
> PF2e Treasure-by-Level). Also: his stat blocks live on external sites
> (monster.pf2.tools / template.pf2.tools); a few used the deprecated
> easytool.es domain → link-check + archive before relying on them.

## B. Other conversion resources

| Source | Reliability | Notes | Decision |
|--------|-------------|-------|----------|
| [A-Series-of-Dice-Based-Events/CurseOfTheCrimsonThrone (GitHub)](https://github.com/A-Series-of-Dice-Based-Events/CurseOfTheCrimsonThrone) | LOW | **Verified directly: an empty scaffold.** Root + all 6 book folders are identical RTF stub templates; real content only = Book 1 Foundry/pf2.tools JSON (VestOfHolding, 2022). Stale | **Reject** as content source; use Book 1 Foundry JSON for *format reference* only |
| [Curse of the Crimson Throne 2e Conversion Guide (Pathfinder Infinite, 3pp)](https://www.pathfinderinfinite.com/en/product/375718/curse-of-the-crimson-throne-second-edition-conversion-guide) | UNVERIFIED | Most complete paid conversion; **mostly retains 1e ELs** (so inherits 1e balance problems); converts mini-games (Knivesies, Blood Pig!, The Harrowing) | Cross-check only. Same work as A10 |
| [Steev42 CotCT conversion (Paizo rzs2lesl)](https://paizo.com/threads/rzs2lesl) | LOW | Conversion to **PF1e**, not PF2e | **Reject** for mechanics; flavor only |
| [Lost Omens World Guide — Saga Lands/Varisia](https://paizo.com/products/btq01zoj) (P2) | OFFICIAL | Canonical PF2e Varisia treatment; region backgrounds + archetype. **NOT** a Korvosa gazetteer; timeline advanced vs AP | Adopt selectively for PF2e-compatible backgrounds; reconcile dates |
| [Lost Omens Travel Guide](https://paizo.com/products/btq02c20) (P2) | OFFICIAL | PF2e-compatible cultural backgrounds/items | Optional flavor |
| [paizo.com/curseOfTheCrimsonThrone](https://paizo.com/curseOfTheCrimsonThrone) | OFFICIAL | **Confirms NO official PF2e version exists**; 2016 PFRPG Anniversary HC is the canonical base | Ground truth |

## C. Foundry / VTT resources

| Source | Reliability | Notes | Decision |
|--------|-------------|-------|----------|
| [Racooze's Curse of the Crimson Throne Battlemaps](https://foundryvtt.com/packages/racoozes-curse-of-the-crimson-throne-battlemaps) | CONSENSUS | Free Foundry module, **v11–v14**, updated ~Mar 2026; system-agnostic maps only; deletable roof tiles | **Adopt (maps only)** as a **soft dependency**. Verify per-chapter coverage |
| GitHub repo "Foundry Json Files" (Book 1) | LOW | Book 1 NPC JSON for Foundry v10 | Format reference only |

## D. Balance analysis (per-chapter problem corpus)

All CONSENSUS unless noted. Feeds `reports/encounter_balance_report.md` and the
audit risk register.

- [Overall CoCT Review (Paizo rzs2np7a)](https://paizo.com/threads/rzs2np7a) — richest per-encounter data: Bk2 plague near-lethal w/o curer; Bk3 rakshasa need magic weapons; Bk4 Flameford "utter rout"; Bk5 Scarwall TPK risks (spirit-anchor devils, demilich wails), underleveling.
- [Lamm is a bit of a Lamb (rzs2le1z)](https://paizo.com/threads/rzs2le1z) — **Gaedren Lamm deliberately trivial**; real threat is Gobblegut (croc). Will be flatter in PF2e.
- [Failed attempt at the Dead Warrens (rzs2uwc5)](https://paizo.com/threads/rzs2uwc5) — Bk2 attrition + Vreeg prepared ambush; module assumes no-rest clearing.
- [Skeletons of Scarwall GM Reference p.4 (rzs2huw7)](https://paizo.com/threads/rzs2huw7&page=4) — rest-cheese, Mithrodar anchoring broken-as-written, Brotherhood allies bog pacing, graveknight haversack edge cases, underleveling.
- [Help with Scarwall — first-time GM (rzs2u5ol)](https://paizo.com/threads/rzs2u5ol) — ~200-room slog; use built-in shortening levers.
- [Adjusting the final battle (rzs42vz2)](https://paizo.com/threads/rzs42vz2) — Ileosa too easy; phase her, recast as stronger caster, reactive simulacra, throne as terrain.
- [Arkona Issues (rzs2qjqc)](https://paizo.com/threads/rzs2qjqc) — **Vivified Labyrinth lets parties skip most of the Arkona dungeon**; missing maps for its 4 states.
- [CotCT Player Review (rzs2jmff)](https://paizo.com/threads/rzs2jmff) — Bk6 **combat saturation** (~12wk continuous combat); Ileosa nat-20-only DCs; Bk3 thin for 3 levels.
- [Juneberry — Escape from Old Korvosa](https://juneberryjournal.weebly.com/reviews/curse-of-the-crimson-throne-3-escape-from-old-korvosa-review) (UNVERIFIED) — Vivified Labyrinth bad UX; Blood Pig dull + fallback near-TPK; Pilts near-TPK.
- [Jhaeman — Bk4](http://jhaeman.blogspot.com/2023/04/pathfinder-adventure-path-curse-of.html) / [Bk6](http://jhaeman.blogspot.com/2025/02/pathfinder-adventure-path-curse-of.html) (UNVERIFIED) — "A Crowded Dungeon" 3-faction fight hard to run; Cindermaw swallow gimmick; **Castle Korvosa = surgical strike, not full clear**; Gray Maidens trivial (use Troop rules); Kazavon CR25 fail-state.
- [Of Dice and Pen review](https://www.ofdiceandpen.ca/2017/01/curse-of-crimson-throne.html) — Scarwall "weakest part" (tedium); Anniversary Ed. adds Korvosa interludes.
- [Against the Wicked City — condensation](http://udan-adan.blogspot.com/2017/01/condensation-in-action-part-3-curse-of.html) (UNVERIFIED) — linearity critique; plague resolves too early; sandbox rewrite (advanced/optional).

## E. Story / quality-of-life

- [Improved Initiative — 5 Tips (taking10)](https://taking10.blogspot.com/2021/08/5-tips-for-running-curse-of-crimson.html) — **Korvosa = Gotham**; prep players for bounty-hunter→watch-consultant role; consequences in recurring locations. **Adopt** (drives NPC/location journal "development" notes).
- [Paizo — Advice for running CotCT (rzs2q0i7)](https://paizo.com/threads/rzs2q0i7) — highest-density list: tie PCs to Korvosa not just Lamm; pre-build 3–5 contacts each; **don't foreshadow the plague**; emphasize Old Korvosa quarantine; interleave Scarwall w/ Korvosa.
- [EN World — New GM Advice](https://www.enworld.org/threads/new-gm-advice-curse-of-the-crimson-throne.357448/) (UNVERIFIED) — front-load city attachment; optional lead-in adventures.
- [Strange Assembly review](https://www.strangeassembly.com/2017/review-curse-of-the-crimson-throne-pathfinder-rpg) — first half brilliant, second half less cohesive (re-anchor to Korvosa); Harrow = boost + telegraph.
- [CotCT Player's Guide (Paizo blog)](https://paizo.com/blog/curse-of-the-crimson-throne-player-s-guide) — OFFICIAL: campaign traits + Harrow char-gen (1d6 no-deck fallback). **Adopt** as buy-in spine.
- [PathfinderWiki — CotCT](https://pathfinderwiki.com/wiki/Curse_of_the_Crimson_Throne) / [Cindermaw](https://pathfinderwiki.com/wiki/Cindermaw) — OFFICIAL lore: **Kazavon = blue dragon**, Fangs of Kazavon, deterioration timeline. **Adopt** for fact-checking foreshadowing.

## F. Official PF2e subsystem rules (the conversion targets)

All **OFFICIAL**, Remaster (cite **GM Core / Player Core**, not Gamemastery Guide):

| CotCT mechanic | PF2e target | Source |
|---|---|---|
| Court intrigue, swaying single NPCs, doctors' soiree, war council | **Influence** | [GM Core p.187](https://2e.aonprd.com/Rules.aspx?ID=1201) |
| Standing with Korvosa's people & factions (Guard, Shoanti tribes, Cerulean Society, the rebellion) | **Reputation** (−50…+50 tiers) | [GM Core p.199](https://2e.aonprd.com/Rules.aspx?ID=1234) |
| Cinderlands overland travel (Ch.4) | **Hexploration** (light) + Subsist/Survival | [GM Core p.207](https://2e.aonprd.com/Rules.aspx?ID=1265) |
| Blood Veil plague (Ch.2) | **Disease/affliction** (virulent), Fort DC scaled to level | [Player Core p.417/430](https://2e.aonprd.com/Rules.aspx?ID=2389) |
| Pursuits (fleeing cultists/doctors, Trinia manhunt, bridge flight) | **Chases** | [GM Core p.192](https://2e.aonprd.com/Rules.aspx?ID=1210) |
| Hospice / Castle Korvosa approach past Gray Maidens | **Infiltration** | [GM Core p.196](https://2e.aonprd.com/Rules.aspx?ID=3059) |
| Harrow readings (in-fiction foreshadowing) | **Harrow Deck** item (name retained post-remaster) + narrative reading | [Harrow / Stolen Fate](https://2e.aonprd.com/Rituals.aspx?ID=100) |
| 1e "Harrow Points" reroll pool | **Harrowing ritual** (Stolen Fate PG p.12, Ritual 1) suit-keyed rerolls, or hero-point-like pool | as above |
| Citywide epidemic spread | **No first-party subsystem** → narrative clock + per-PC daily flat-check exposure | community CONSENSUS |
| Shoanti Trials of Respect; Blood Pig / Knivesies mini-games | **Victory Points** skill challenges (GM Core) | [VP subsystem](https://2e.aonprd.com/Rules.aspx?ID=1196) |

---

## G. Synthesis — adopted conversion decisions

1. **Base text = 2016 Anniversary hardcover** (our PDF). It already folds in many
   community fixes (any-order Ch.4 quests, return-to-Korvosa strike mission,
   taniniver for Kazavon's presence, Harrow points, new Gray Maiden mission) — so
   we do **not** re-add those; we convert what's there. *(→ CHG-0006)*
2. **Leveling = milestone**, with a per-chapter assumed-level advancement track in
   each chapter journal (1e XP is too slow; underleveling is the Scarwall TPK
   driver). XP budgets are still computed per encounter for tuning. *(→ CHG-0007)*
3. **Level span = native 1 → 17** (Ch.6 ends ~16–17). Extending to 20 via an
   add-on module is **out of scope** unless the GM requests it. *(GM decision G-Q1)*
4. **Subsystems → official PF2e (Remaster)** per table F. Each gets its own
   change-log entry + a Conversion-Guide journal section + a helper macro/rolltable
   where useful. *(→ CHG-0005 finalized into CHG-0010…0017)*
5. **Treasure is ours to build** (Olliebird omits it): convert every parcel to
   PF2e Treasure-by-Level (GM Core), preserve story items, produce
   `reports/treasure_report.md`. *(→ CHG-0008)*
6. **Maps via Racooze's battlemap module** (soft dependency) instead of shipping
   art; our scene records reference its scenes / name the expected map. *(→ CHG-0009)*
7. **Creature method = two-tier** (official PF2e Monster Core/Bestiary actor when a
   good match exists; custom build otherwise) — same approach Olliebird used, but
   we re-derive to Remaster + PF2e encounter math rather than retaining 1e ELs
   (the paid guide's retain-EL approach inherits 1e's documented balance problems).
8. **Known fixes to bake in** (from D/E, as PF2e-native design): elevate the Lamm
   fight's stakes via Gobblegut rather than buffing the old man; add a rest-pressure
   affliction in Scarwall; run Castle Korvosa as Infiltration (surgical strike, not
   full clear); make Gray Maiden patrols matter via troop-style or grouped stat
   blocks; harden the Ileosa finale (phasing / reactive simulacra / throne terrain)
   and treat Kazavon's resurrection as an explicit fail-state. Each becomes a
   per-area change-log entry at conversion time, flagged for GM approval where it
   alters play.
9. **Lore correction:** Kazavon is a **blue** dragon (CR-25 fail-state form), not
   green. *(→ CHG, Ch.6)*

## H. Open questions / GM decisions needed

- **G-Q1 — Level cap:** native 1→17, or extend to 20 (e.g. Deathhead Vault add-on)? *(default: native)*
- **G-Q2 — Which Olliebird artifact do you have** — the free Google Docs or the paid Pathfinder Infinite PDF? (Affects whether advancement tracks/treasure guidance are already in hand.)
- **G-Q3 — Mystery vs telegraph** for Blackjack=Vencarlo and Glorio Arkona's rakshasa reveal (both widely considered "transparent"). *(default: keep as written)*
- **G-Q4 — Plague structure:** keep Blood Veil as a resolved Ch.2 arc (faithful) or run it as a persistent background threat (udan-adan rewrite, high-effort)? *(default: faithful)*
- **G-Q5 — Maps:** OK to take a dependency on Racooze's free battlemap module, or supply your own? *(default: reference Racooze)*
- **G-Q6 — Harrow reroll pool:** Stolen Fate *Harrowing* ritual vs a simpler hero-point-style suit pool? *(default: hero-point-style, lighter)*

*(These are tracked in `conversion_change_log.md` and surfaced in the final
GM-review list. None block the Chapter 1 pilot.)*

### Resolved with GM (2026-06-09)
- **G-Q1 (level cap):** Native **1→17 preserved** + an optional **post-finale arc** from Appendix 1 hooks (built after the main conversion). *(CHG-0003)*
- **G-Q2 (which Olliebird artifact):** GM has **neither** — rely on our own conversion + these research notes; cross-reference optional.
- **G-Q3 (telegraph vs mystery):** **Preserve the mystery** for Blackjack=Vencarlo & Glorio Arkona=rakshasa; journals add earnable GM hints, reveals stay player-discovered.
- **G-Q4 (plague structure):** **Persistent background threat — APPROVED** with consequences framework. *(CHG-0011b; `design/persistent_plague.md`)*
- **G-Q5 (maps):** **Reference Racooze's** free battlemaps. *(CHG-0009)*
- **G-Q6 (Harrow reroll):** **Hero-Point-style suit pool**; ritual optional. *(CHG-0010)*
- **Pilot boss:** **Severe @ level 1** confirmed. *(CHG-0101)*
