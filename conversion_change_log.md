# Conversion Change Log — Curse of the Crimson Throne (PF1e → PF2e)

Every change from the original AP is recorded here, however small. Per-area
changes are also mirrored in the relevant Foundry journal's *Conversion Notes /
Changes from Original* section.

## Schema

Each entry records:

- **ID** — `CHG-NNNN` (stable, never reused).
- **Chapter / location** — where it applies (`GLOBAL` for standing decisions).
- **Original** — the PF1e element (summarized — no verbatim copyrighted text).
- **New / revised** — the PF2e version.
- **Source of change** — one of: *PF2e rules necessity · Balance correction ·
  Community recommendation · Foundry implementation need · Quality-of-life ·
  Continuity fix*.
- **Severity** — *Cosmetic · Minor · Moderate · Major (REQUIRES GM APPROVAL)*.
- **In journal?** — yes/no/n-a (is it reflected in a journal entry yet).
- **Foundry path** — journal/compendium location, when it exists.
- **GM review** — *none · pending · approved · rejected*.

> **Major story changes are never implemented silently.** They are added here
> marked `REQUIRES GM APPROVAL` with GM review = *pending* and are NOT written
> into the playable journals until approved.

---

## GLOBAL — standing decisions

These apply across the whole conversion and are detailed in
`foundry-module/CONVERSION_NOTES.md` and `PROJECT_PLAN.md`.

### CHG-0001 — Adopt PF2e Remaster ruleset
- **Chapter/location:** GLOBAL
- **Original:** PF1e (3.5-derived) rules; alignment-based mechanics; PF1e spell/condition names.
- **New:** PF2e **Remaster** — Player Core / GM Core / Monster Core. Off-guard (not flat-footed), holy/unholy & edicts/anathema (no alignment), no spell schools, remastered monster stat blocks where available.
- **Source:** PF2e rules necessity.
- **Severity:** Moderate (mechanical, not narrative).
- **In journal?** n-a (documented in Conversion Guide journal once built).
- **Foundry path:** `cotct-journals` → Conversion Guide (pending).
- **GM review:** none (standard).

### CHG-0002 — Party baseline 4 PCs, no Free Archetype / ABP
- **Chapter/location:** GLOBAL
- **Original:** PF1e assumed a 4-PC party using the standard wealth-by-level and the 15-point buy.
- **New:** PF2e encounter math built for **4 PCs** (Moderate budget 80 XP), standard ability boosts, **no** Free Archetype / Automatic Bonus Progression. Encounter records include 3/5/6-PC adjustments.
- **Source:** PF2e rules necessity.
- **Severity:** Minor.
- **In journal?** n-a.
- **Foundry path:** Conversion Guide (pending).
- **GM review:** **pending** — confirm party size & house rules with GM.

### CHG-0003 — Per-chapter PF2e level targets (default 1:1 mapping)
- **Chapter/location:** GLOBAL
- **Original:** PF1e levels — Ch1 1–4, Ch2 4–7, Ch3 7–9, Ch4 9–11, Ch5 11–14, Ch6 14–16.
- **New (CONFIRMED 2026-06-09):** Preserve the native **1 → 17** story unchanged, and additionally **stub an optional post-finale arc** from Appendix 1's "Continuing the Campaign" hooks (Kazavon Rises / Sorshen's Legacy / Rulers of Korvosa) that players can push into beyond the ending for higher-level play. Main conversion is **not** stretched to 20.
- **Source:** PF2e rules necessity + GM choice (story sanctity).
- **Severity:** Minor (main story); the post-game arc is new optional content (built after the main conversion).
- **In journal?** n-a (post-game arc → its own journal in a later phase).
- **Foundry path:** PROJECT_PLAN.md §2; Appendices journal (pending).
- **GM review:** resolved.

### CHG-0004 — Copyright firewall (summaries, not reproduction; no shipped art)
- **Chapter/location:** GLOBAL
- **Original:** Full AP prose, read-aloud text, maps, and art in the hardcover.
- **New:** Journals carry **summaries + page citations**, not verbatim read-aloud; **no maps/art shipped** (GM supplies legal copies). Source PDF & extracted text are git-ignored.
- **Source:** Foundry implementation need / legal (private-use constraint).
- **Severity:** Minor (presentation; no story change).
- **In journal?** n-a (policy).
- **Foundry path:** `foundry-module/README.md`, `assets/README.md`.
- **GM review:** none.

### CHG-0005 — Subsystem mapping framework  *(provisional — pending research)*
- **Chapter/location:** GLOBAL (applies Ch.1–6)
- **Original:** PF1e/AP-specific subsystems — the Harrowing, Blood Veil plague, Cinderlands travel, court intrigue / ally-gathering, factional standing, chases.
- **New (provisional):** Harrowing → PF2e Harrow reading; Blood Veil → PF2e disease + epidemic clock; Cinderlands → Hexploration + Survival; intrigue/allies → Influence; factional standing → Reputation; chases → Chase/Infiltration. Finalized per-subsystem after research; each finalized mapping gets its own `CHG-00xx` entry.
- **Source:** PF2e rules necessity / Quality-of-life.
- **Severity:** Moderate.
- **In journal?** n-a yet.
- **Foundry path:** per-chapter journals + Conversion Guide (pending).
- **GM review:** pending.

### CHG-0006 — Base text = 2016 Anniversary Edition (not 3.5 original)
- **Chapter/location:** GLOBAL
- **Original:** AP exists as 2008 3.5 (6 vols) and 2016 PF1e Anniversary HC.
- **New:** Convert from the **Anniversary HC** (our source), which already folds in community fixes (any-order Ch.4 Respect quests, return-to-Korvosa Deathhead mission, taniniver in the finale, Harrow points, new Gray Maiden content). We do **not** re-add these.
- **Source:** Community recommendation / continuity fix.  **Severity:** Cosmetic (baseline choice).  **In journal?** n-a.  **GM review:** none.

### CHG-0007 — Milestone leveling + per-chapter advancement track
- **Chapter/location:** GLOBAL
- **Original:** PF1e XP-by-encounter (documented as too slow; underleveling is the Scarwall TPK driver).
- **New:** **Milestone leveling**; each chapter journal opens with an assumed-level advancement track. XP budgets still computed per encounter for tuning only.
- **Source:** Balance correction / community consensus (Olliebird + forums).  **Severity:** Minor.  **In journal?** n-a (Conversion Guide + per-chapter).  **GM review:** none.

### CHG-0008 — Treasure fully rebuilt to PF2e Treasure-by-Level
- **Chapter/location:** GLOBAL
- **Original:** PF1e parcels/gp hoards (some enormous, e.g. Kazavon ~100k+); Olliebird's community conversion **omits treasure entirely**.
- **New:** Convert every parcel to PF2e Treasure-by-Level (GM Core); replace PF1e items with PF2e equivalents; preserve story items (Brooch, Harrow deck, Serithtial, Crown of Fangs). Output `reports/treasure_report.md`.
- **Source:** PF2e rules necessity (the biggest GM-prep gap).  **Severity:** Moderate.  **In journal?** n-a (per-chapter treasure pages + report).  **GM review:** none.

### CHG-0009 — Maps via Racooze's battlemap module (no shipped art)
- **Chapter/location:** GLOBAL
- **Original:** Copyrighted AP maps in the hardcover.
- **New:** Ship **no** maps; scene records reference **Racooze's CotCT Battlemaps** (free Foundry module, Community Use) by name + name the expected file; GM supplies legal copies. Author scene-planning notes where coverage is uncertain (esp. the Vivified Labyrinth's 4 states).
- **Source:** Foundry implementation need / legal.  **Severity:** Minor.  **In journal?** n-a.  **GM review:** **resolved (2026-06-09)** — GM approved depending on Racooze's free Community-Use battlemaps.

### Subsystem conversions (finalize CHG-0005 framework)

> All map to official PF2e **Remaster** subsystems per `research/research_index.md` §F. Each is built once and reused; full rules live in the Conversion-Guide journal + a helper macro/rolltable where useful. Severity Moderate unless noted; GM review *pending* until the relevant chapter is playtested.

- **CHG-0010 — Harrowing → Harrow Deck item + narrative reading**, reroll pool as **hero-point-style suit boons (CONFIRMED 2026-06-09)**; the Stolen Fate *Harrowing* ritual offered as an optional swap. Harrow Deck of Many Things = bespoke high-level item translating the 54 results. *Original:* PF1e 54-card Harrow + Harrow Points (App 3). *Review:* resolved.
- **CHG-0011 — Blood Veil → virulent PF2e disease** (Fort DC scaled to party level ~18–20; substitute drained/enfeebled/clumsy + HP for the PF1e Con+Cha damage). *Original:* PF1e fixed-DC Fort disease + % daily-exposure subsystem (Ch2/App 4). *Base disease build:* Severity Moderate; review none. **→ EXTENDED by CHG-0011b below.**
- **CHG-0011b — PERSISTENT plague overlay (Major) — APPROVED 2026-06-09.** Run Blood Veil as a **persistent background threat across Ch.2–6** (not resolved in Ch.2): an Epidemic Clock tied to city tiers + the canon "Blooding"/Everdawn Pool blood-harvest, the Ch.2 cure reframed as a *suppressant*, **plus a consequences/GM-options framework** (escalation by clock tier, PC-infection tones, lose-an-NPC/place/faction menu, villain-acceleration link to the Ch.6 timer, full player agency + removability hatch). *Source:* GM design choice / QoL. **Severity: MAJOR (GM-approved).** Full design: [`design/persistent_plague.md`](design/persistent_plague.md). *In journal?* implement with Ch.2 (Phase 3) + a campaign-state journal page for the clock. *GM review:* **approved.**
- **CHG-0012 — Korvosa settlement stat blocks (×5) → leveled item-availability table + city-state tiers** driven by Reputation; **Rumor Mill → rolltables**. *Original:* PF1e settlement stats (Base Value/Purchase Limit/etc., App 2).
- **CHG-0013 — Respect Points / Rebellion Points / faction standing → Reputation + Victory Points.** *Original:* bespoke PF1e point trackers (Ch4/Ch6).
- **CHG-0014 — Court/social influence → Influence subsystem** (per-NPC Influence blocks, DCs from level-based table). *Original:* PF1e Diplomacy ladders (Devargo, doctors' soiree, Emperor research, war council).
- **CHG-0015 — Cinderlands travel → light Hexploration + Survival/Subsist.** *Original:* PF1e overland/Survival tracking (Ch4).
- **CHG-0016 — Fugitive pursuits → Chase subsystem.** *Original:* PF1e GMG chase-card rules (Shingles/Trinia, etc.).
- **CHG-0017 — Castle Korvosa & Hospice approach → Infiltration subsystem** (Castle = surgical strike, not full clear). *Original:* PF1e free-form stealth (Ch2/Ch6). **Includes the QoL "don't full-clear the castle" fix.**
- **CHG-0018 — Minigames (knivesies, Blood Pig, Sredna, Trial of the Totem) → Victory-Point skill challenges** rebuilt for PF2e 3-action economy. *Original:* PF1e CMB/CMD-based minigames.
- **CHG-0019 — Scarwall spirit-anchor/chained-spirit/Curse → bespoke ritual+condition + complex hazards**; adopt the official **"A Swifter Scarwall"** streamlining (p.330) as the default build. *Original:* PF1e multi-layer curse + 4 anchors (Ch5). **Severity Major (scope) — REQUIRES GM APPROVAL on how much to streamline.**
- **CHG-0020 — Havero Noise Points → bespoke complex hazard / scaling reaction-creature.** *Original:* PF1e unkillable-CR24 noise-tracker tentacles (Ch4).
- **CHG-0021 — Campaign traits → PF2e custom backgrounds** ("Korvosa hooks"); pair with the "tie PCs to Korvosa, not just Lamm" QoL guidance. *Original:* PF1e campaign traits (Intro). **Severity Minor.**
- **CHG-0022 — Korvosan Guard org-influence + Blackjack succession → Reputation/Influence + archetype-style guidance.** *Original:* PF1e Ultimate Intrigue org rules + vigilante succession (App 6).

### CHG-0023 — Lore correction: Kazavon is a blue dragon; CR-25 form is a fail-state
- **Chapter/location:** Ch.6 / GLOBAL lore
- **Original:** (Common misremembering as "green"); Kazavon's reborn form is a CR-25 set-piece.
- **New:** Kazavon is canonically a **blue** dragon (per PathfinderWiki / AP text); the "Rise of the Dragon" Kazavon is an explicit **fail-state**, not a standard balanced fight. Build accordingly.
- **Source:** Continuity fix.  **Severity:** Cosmetic (fact).  **In journal?** n-a.  **GM review:** none.

### CHG-0024 — Foundry output restructured to Kingmaker-style Adventure module
- **Chapter/location:** GLOBAL (Foundry implementation)
- **Original:** (pilot v1) flat per-type compendium packs; many small journal entries.
- **New:** Emulate the official **pf2e-kingmaker** module UX — a one-click **Adventure pack** (`cotct-adventure`) bundling per-type **folders** + a **fat chapter journal** (one entry, one page per area, `title.level` outline, styled `section.*` blocks via shipped **CSS**, `@Check`/`@UUID` enrichers) + a **scene** with **map-note pins → journal pages** and **pre-staged hidden hostile tokens** + actors carrying **prototype tokens**/`publication`. Verified vs the GM-provided Kingmaker world export.
- **Source:** Foundry implementation need (GM requirement) / quality-of-life.
- **Severity:** Moderate (presentation/packaging; no story change).
- **In journal?** n-a (it *is* the journal structure).
- **Foundry path:** whole `foundry-module/`; audit `research/kingmaker_foundry_structure_audit.md` + `research/kingmaker_schema_notes.md`; conformance `reports/kingmaker_style_comparison_report.md`.
- **GM review:** **pending** — one live Adventure-import smoke test in Foundry v14 (the only step not self-verifiable headlessly).

---

## Per-area changes

*(Populated during Phase 2 pilot and Phase 3. Format: one `### CHG-NNNN` block
per change, grouped by chapter. Major narrative changes are added here with
`REQUIRES GM APPROVAL` before any journal implementation.)*

<!-- CH1 — Edge of Anarchy -->

### CH1 · Old Fishery (Phase-2 pilot)

Per-area changes for the pilot. Mirrored in the journal *Old Fishery — Conversion
Notes*. Foundry path: `cotct-journals` → "Old Fishery — …". No major
(approval-gated) story changes; plot/villain/flow/cliffhanger preserved.

- **CHG-0101 — Gaedren boss rebuilt as a credible Severe.** *Original:* CR-2 frail old man, anticlimactic solo ("Lamm is a Lamb"). *New:* L2 frail sniper + **Spur the Beast**/**Nimble Dodge**, paired with Gobblegut (Crocodile L2) for a **Severe (120 XP @L1)** fight where the gator is the threat. *Source:* Balance correction + community consensus + PF2e solo math. *Severity:* **Moderate.** *Journal:* yes (Areas A13, Encounters). *GM review:* **pending** (Severe @L1 vs run @L2).
- **CHG-0102 — Gobblegut & Bloo referenced as official Crocodile / Guard Dog** (not rebuilt). *Source:* Foundry/use-official-actor. *Severity:* Cosmetic. *Journal:* yes. *Review:* none.
- **CHG-0103 — All DCs re-derived** to PF2e level-based/simple (locked-door spam collapsed; Will 25→18, Perc 25→18, etc.). *Source:* PF2e rules necessity. *Severity:* Minor. *Journal:* yes (DCs noted per area; full table in `reports/dc_skill_report.md`). *Review:* none.
- **CHG-0104 — Treasure fully rebuilt** to PF2e level 1→2 (PF1e gp discarded; brooch/deck as story items). *Source:* PF2e rules necessity (CHG-0008). *Severity:* Moderate. *Journal:* yes (Treasure). *Review:* none.
- **CHG-0105 — Drain Spider Venom** PF1e Con-drain → PF2e 1-stage poison (Fort DC 15 + enfeebled); vermin-repellent auto-repel preserved. *Source:* PF2e rules necessity. *Severity:* Minor. *Journal:* yes (NPCs). *Review:* none.
- **CHG-0106 — Harrowing pilot stub** (Hero-Point-style suit boons via Zellara's deck; CHG-0010). *Source:* PF2e rules necessity. *Severity:* Moderate. *Journal:* yes (Overview). *Review:* pending (G-Q6 reroll style).
- **CHG-0107 — Orphans = explicit non-combatants** with Rally/Aid + Cower; never an XP-for-kill source. *Source:* QoL / safety. *Severity:* Cosmetic. *Journal:* yes (NPCs, Run Sheet). *Review:* none.
- **CHG-0108 — QoL run-framing surfaced** ("Gaedren is a connector", day/night alarm, rescue-the-orphans focus). *Source:* Community QoL consensus. *Severity:* Cosmetic. *Journal:* yes (Run Sheet). *Review:* none.
<!-- CH2 — Seven Days to the Grave -->
<!-- CH3 — Escape from Old Korvosa -->
<!-- CH4 — A History of Ashes -->
<!-- CH5 — Skeletons of Scarwall -->
<!-- CH6 — Crown of Fangs -->
