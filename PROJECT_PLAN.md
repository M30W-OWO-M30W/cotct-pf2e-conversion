# PROJECT PLAN — Curse of the Crimson Throne, PF1e → PF2e

**Project root:** `/home/saber/pf2e-conversion/curse-of-the-crimson-throne/`
**Source:** *Pathfinder Adventure Path: Curse of the Crimson Throne* (2016 hardcover), 482 pp.
**Output:** private Foundry VTT module `foundry-module/` (id `cotct-pf2e-conversion`)
**Status:** Phase 1 in progress. *(This is a living document — sections tagged ⟳ are refined as research/audit data lands.)*

---

## 1. Goal

A complete, internally consistent, **PF2e-native** conversion of CotCT that
preserves the original story, structure, tone, and intended campaign arc while
rebuilding encounters, NPCs, hazards, treasure, DCs, and subsystems to PF2e
(Remaster) math and action economy — delivered as a Foundry-importable module
with full GM-facing documentation and traceable change tracking.

This is **not** a mechanical stat transliteration. PF1e numbers are discarded
when they don't serve PF2e; the *design intent* behind each scene is what we
preserve.

## 2. AP identification (summary — full content map in `conversion_audit.md`)

| | |
|---|---|
| Adventure Path | Curse of the Crimson Throne (single-volume hardcover, 2016) |
| Setting | Korvosa, Varisia (Golarion) |
| Chapters | 6 + Introduction + Appendices |
| PF1e level span | 1 → ~16 |
| Authors | Logue, Schneider, Pett, Kortes & Jacobs, Vaughan, Leati |

| # | Chapter | PDF pp. | PF1e levels | PF2e target ⟳ |
|---|---------|---------|-------------|----------------|
| — | Introduction | 4–9 | — | — |
| 1 | Edge of Anarchy | 10–67 | 1–4 | **1 → 4** |
| 2 | Seven Days to the Grave | 68–131 | 4–7 | **4 → 7** |
| 3 | Escape from Old Korvosa | 132–189 | 7–9 | **7 → 9** |
| 4 | A History of Ashes | 190–255 | 9–11 | **9 → 11** |
| 5 | Skeletons of Scarwall | 256–331 | 11–14 | **11 → 14** |
| 6 | Crown of Fangs | 332–391 | 14–16 | **14 → 16/17** |
| — | Appendices (gazetteer, class options, NPCs, bestiary) | 392–482 | — | — |

PF2e level targets above are the default 1:1 mapping, **cross-checked and confirmed**
against the community conversion (Olliebird targets the same span; e.g. party hits
level 2 after the Old Fishery) and PF2e XP pacing. Native span **1 → 17**; extending
to 20 is out of scope unless requested (GM decision G-Q1). PF2e's flatter math may
still let us compress a few redundant fights without changing the level a chapter
ends on; any such change is logged per-encounter.

## 3. Versions, ruleset, party assumptions

See `foundry-module/CONVERSION_NOTES.md` for the authoritative copy. In brief:

- **Foundry** v14 (build 363), **PF2e system** 8.2.0 — ✅ confirmed 2026-06-09. (Schema authored against pf2e `master` = 8.2.0, so it matches the target exactly.)
- **Ruleset: Remaster** (Player Core / GM Core / Monster Core). Off-guard, holy/unholy, no alignment, no spell schools.
- **Party: 4 PCs**, no Free Archetype / ABP (default). Encounter records also give 3/5/6-PC adjustments.

## 4. Phase breakdown

### Phase 1 — Audit & Research  *(complete)*
Deliverables:
- [x] `conversion_audit.md` — AP id, file inventory, full content map (~237 enc / ~225 NPC), risk areas, work plan
- [x] `research/research_index.md` — sources, reliability, adoption decisions
- [x] `conversion_change_log.md` — schema + 23 standing/subsystem decision entries
- [x] `PROJECT_PLAN.md` — this file
- [x] `foundry-module/` scaffold + tooling + git (committed)

Method: text extracted from the PDF (page-tagged, `.work/text/chapters/*.txt`),
mapped per-chapter by parallel analysis agents; web research across 5 angles
(community conversion(s), other resources, balance issues, story/QoL advice,
PF2e subsystem equivalents). Stop only if inputs are missing/unreadable.

### Phase 2 — Pilot conversion  *(next)*
**Pilot = Chapter 1 opening: the hunt for Gaedren Lamm, culminating in his lair,
the Old Fishery ("All the World's Meat").** Rationale in §6. Full vertical slice:
journals → encounters → NPCs/actors → hazards → treasure → DCs → change tracking
→ Foundry JSON → validation report. Then evaluate the method before scaling.

### Phase 3 — Full chapter conversion  *(one chapter at a time)*
For each chapter: extract structure → convert encounters → NPCs → hazards →
treasure → DCs → journals → Foundry data → update reports → validate → flag
unresolved issues.

### Phase 4 — Cross-chapter consistency
Recurring NPCs (Ileosa, Sabina, Vencarlo/Blackjack, Cressida Kroft, Laori Vaus,
Neolandus, the Shoanti, the Arkonas), foreshadowing (Kazavon, the curse),
treasure & level progression, subsystem continuity (Harrow, Reputation/Influence,
the Gray Maidens faction), changed story beats, journal links, importability.

### Phase 5 — Final QA
Top-down rules/balance/story/Foundry review → `FINAL_QA_REPORT.md` with remaining
GM-review items, known limitations, import instructions, playtest order.

## 5. Conversion methodology (per element)

1. **Extract original intent** — narrative & tactical purpose, intended
   difficulty, party level, environment, monster role, attrition role,
   mandatory/optional/avoidable, downstream implications.
2. **Design to PF2e** — pick an XP-budget difficulty (Trivial/Low/Moderate/
   Severe/Extreme) from the *intent*, not the CR; prefer official PF2e creatures;
   rebuild only when needed; give solo bosses lieutenants/hazards/reactions so
   PF2e action economy doesn't trivialize them; confirm XP matches intent and
   record the budget.
3. **NPCs** — decide stat block vs. hazard-threat vs. social DC vs. reskin vs.
   custom; build to PF2e NPC norms incl. tactics & morale.
4. **Hazards** — PF2e hazard format (Stealth/Disable DCs, routine, reset,
   counteract level if magical, XP).
5. **DCs** — PF2e level-based / simple / adjusted DCs; never transliterate; record
   old→new + basis.
6. **Treasure** — PF2e treasure-by-level; replace PF1e items with PF2e
   equivalents; preserve story items; per-chapter treasure audit.
7. **Subsystems** — map to official PF2e subsystems (see §7).

Every decision is **traceable** (AP page / PF2e rule / research source /
labeled design judgment). Unknowns → `NEEDS GM REVIEW`, never invented.

## 6. Pilot selection rationale

Chapter 1's opening is the right pilot because it is **self-contained, mandatory,
and exercises every conversion subsystem at small scale**:
- a low-level **dungeon** (the Old Fishery / Lamm's Lair) with mixed enemies
  (Lamm, thugs, the leucrotta "Gobblegut", child thieves as a *non-combatant
  moral* element);
- **traps/hazards** (the fishery's hazards) → PF2e hazard format;
- a **named villain** (Gaedren Lamm) needing a PF2e NPC build;
- **treasure** including a story item (the stolen goods / a PC hook item);
- **skill challenges & social** lead-in (gathering rumors on Lamm; the Harrowing);
- the **Harrowing** subsystem hook (campaign intro) for an early subsystem test.
It validates journal structure, actor JSON, hazard JSON, encounter math, treasure
math, DC conversion, and the change log in one slice before we scale.

## 7. Subsystem strategy *(finalized — research §F, change-log CHG-0010…0022)*

All map to official PF2e **Remaster** subsystems (GM Core / Player Core, page refs
in `research/research_index.md` §F). Built once, reused; full rules in the
Conversion-Guide journal + helper macros/rolltables.

| AP subsystem | PF2e target | CHG |
|---|---|---|
| Harrowing (54-card readings, Harrow Points, Deck of Many Things) | Harrow Deck item + narrative reading; reroll pool = hero-point-style (default) or *Harrowing* ritual | 0010 |
| Blood Veil plague + Survivor Count | virulent **disease** (Fort DC by level) + epidemic **clock/VP** + daily flat-check | 0011 |
| Korvosa settlement stat blocks (×5) + Rumor Mill | leveled item-availability + city tiers via **Reputation**; rumor rolltables | 0012 |
| Respect / Rebellion Points / faction standing | **Reputation** + **Victory Points** | 0013 |
| Court/social influence | **Influence** | 0014 |
| Cinderlands travel | light **Hexploration** + Survival/Subsist | 0015 |
| Fugitive pursuits (Shingles) | **Chase** | 0016 |
| Castle Korvosa / Hospice approach | **Infiltration** (surgical strike) | 0017 |
| Minigames (knivesies, Blood Pig, Sredna, Trial of the Totem) | Victory-Point skill challenges | 0018 |
| Scarwall spirit-anchor / Curse | bespoke ritual+condition + complex hazards; **"Swifter Scarwall"** default | 0019 |
| Havero Noise Points | bespoke complex hazard / scaling reaction-creature | 0020 |
| Campaign traits | PF2e **custom backgrounds** | 0021 |
| Korvosan Guard org-influence; Blackjack succession | Reputation/Influence + archetype guidance | 0022 |

**Priority build order** (these recur across many chapters, so build in/just after
the pilot): Harrow (0010), Korvosa city tiers + Reputation (0012/0013),
campaign-trait backgrounds (0021). Blood Veil (0011) lands with Ch.2.

## 8. Foundry output architecture

- **Packs** (`foundry-module/packs/<pack>/_source/*.json`, one doc per file,
  compiled to LevelDB by `npm run build`): journals, actors, hazards, items,
  rolltables, scenes, macros.
- **ID strategy:** every document gets a stable 16-char alphanumeric `_id` so
  links survive rebuilds. IDs are assigned deterministically by the build helper
  and never recycled.
- **Linking convention:** intra-module references use
  `@UUID[Compendium.cotct-pf2e-conversion.<pack>.<Type>.<id>]`; official content
  uses `@UUID[Compendium.pf2e.<pack>.<Type>.<id>]`. `npm run validate` resolves
  every intra-module link and reports dangling ones.
- **Journals:** hierarchy = AP → GM Overview / Conversion Guide → Chapter →
  Location → Area pages → NPCs / Encounters / Treasure / Conversion Notes →
  Appendices (indices + change log + GM-review items). Each area page carries the
  full required template (source ref, GM summary, mechanics, links, tactics,
  treasure, DCs, dev notes, conversion notes, story changes, GM flags).
- **Scenes:** planning placeholders only; map files are added separately. Each
  names the expected map file + suggested grid.
- **Backups:** existing Foundry data is never destructively overwritten; the
  build is additive and the JSON sources are the source of truth in git.

## 9. Repository policy

- Git source tracks generated JSON and build tooling. `.gitignore` keeps local
  working material (`.work/`) and asset binaries out of commits.

## 10. Risk register

Full register in [`conversion_audit.md` §4](conversion_audit.md). Headline pressure
points (all confirmed by research):
- **Solo-boss action economy** — the dominant risk, every chapter (Lamm → Vreeg →
  Andaisin → Pilts/Bahor → Cindermaw → Mithrodar+anchors+Kleestad → Ileosa CR21 +
  Kazavon CR25). Add lieutenants/minions/hazards/reactions or Elite; flag every
  PL+3/PL+4 solo.
- **No PF2e ability damage / negative levels** — Blood Veil (Con+Cha), drains,
  energy drain → drained/enfeebled/doomed.
- **Save-or-die / save-or-suck** → degrees of success + incapacitation trait.
- **Alignment-keyed effects** (forbiddance/unhallow/holy weapons/rakshasa DR) →
  holy/unholy traits + faction exemptions.
- **No-parity class builds** (vigilante Blackjack, summoner+eidolon Sial) → bespoke NPCs.
- **Attrition/scope monsters** — Scarwall slog (use "Swifter Scarwall"), Ch.6 combat
  saturation (surgical-strike Castle), Dead Warrens no-rest.
- **Treasure/level pacing** across a long 1→17 campaign (treasure is ours to build).
- **Foundry:** pf2e v7 schema validation, stable UUID links, map files added separately.

## 11. Quality bar (definition of done, per element)

Every converted area must answer: *What changed? Why? Where is it in Foundry?
Is the encounter balanced (XP budget shown)? Is the NPC PF2e-native? Is the
treasure level-appropriate? Is the story preserved? What still needs GM review?*
