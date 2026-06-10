# Conversion Change Log — Curse of the Crimson Throne (PF1e → PF2e)

Every change from the original AP is recorded here, however small. Per-area
changes are also mirrored in the relevant Foundry journal's *Conversion Notes /
Changes from Original* section.

## Schema

Each entry records:

- **ID** — `CHG-NNNN` (stable, never reused).
- **Chapter / location** — where it applies (`GLOBAL` for standing decisions).
- **Original** — the PF1e element (summarized).
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

### CHG-0009 — Maps via Racooze's battlemap module
- **Chapter/location:** GLOBAL
- **Original:** AP maps in the hardcover.
- **New:** Map files are added separately; scene records reference **Racooze's CotCT Battlemaps** by name + name the expected file. Author scene-planning notes where coverage is uncertain (esp. the Vivified Labyrinth's 4 states).
- **Source:** Foundry implementation need.  **Severity:** Minor.  **In journal?** n-a.  **GM review:** **resolved (2026-06-09)** — GM approved depending on Racooze's battlemaps.

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

#### Pilot refinement pass (Foundry usability + source/community fidelity)

- **CHG-0109 — Intra-module links use Compendium UUIDs** (`@UUID[Compendium.cotct-pf2e-conversion.<pack>.<Type>.<id>]`) instead of bare world UUIDs, so actor/hazard/item/scene links resolve when the journal is read straight from the compendium (bare links only resolve post-import). *Source:* Foundry implementation need. *Severity:* Minor. *Review:* none. (SOP §1.)
- **CHG-0110 — NPC stat-block authoring standard.** Action/ability items are mechanics-only; role/tactics/behavior live in `publicNotes`; conditions are rendered as pf2e condition links (Off-Guard, Enfeebled, Wounded, Prone, Immobilized, Deafened); conditional passives (Sneak Attack, Bludgeoner) are **sheet toggles** (RollOption + predicated rule), not baked into Strikes. *Source:* Foundry usability / pf2e convention. *Severity:* Minor. *Review:* none. (SOP §3–4, §4b.)
- **CHG-0111 — NPC inventories populated + consumables made functional.** Every combatant carries real `equipment-srd` gear (weapons/armor/consumables) with a `compendiumSource` link; consumables (Acid Flask, Thunderstone, Healing Potion) carry clickable, correctly-typed `@Damage` so their effects work in Foundry; languages use lowercase pf2e slugs and ancestry senses (low-light/darkvision/tremorsense) are restored. *Source:* Foundry usability + source fidelity. *Severity:* Minor. *Review:* none. (SOP §4b–4c.)
- **CHG-0112 — Source-vs-build audit fidelity fixes** (9-creature adversarial audit vs PF1e source + our reports): Gaedren's full 9 source languages restored; Yargin Acid Flask ×3 + a **Scroll of Acidic Burst** standing in for his PF1e wand of acid splash; Hookshanks (gnome) + Giggles (half-orc, Remaster = low-light) vision senses; Drain Spider tremorsense 30→60 ft; Slippery Boardwalk fall damage **removed** (source: deep water = no falling damage). *Source:* Source fidelity / mechanical correction. *Severity:* Minor. *Review:* none.
- **CHG-0113 — Drain Spider gains a Web Trap** (ranged web Strike → Immobilized, Escape DC 15) and web-sense. *Original:* PF1e drain spider has **no web**; this is adopted from the **Olliebird community PF2e build** (homebrews a web onto the spider). *Source:* Community cross-reference / thematic. *Severity:* Minor. *Journal:* via NPC sheet. *Review:* none.
- **CHG-0114 — NPC damage tuning to PF2e role bands.** Giggles (the brute) → high Strike damage `1d6+5` / `1d4+5` (was moderate `+3`), matching Monster Core damage-by-role and the community build. *Source:* PF2e creature-building math. *Severity:* Cosmetic. *Review:* none.

#### Chapter 1, Part Two — A City Gone Mad (full conversion)

- **CHG-0115 — Bestiary-link infrastructure.** `scripts/extract_bestiary.mjs` indexes all 1,425 official Monster Core / Bestiary 1–3 creatures (slug → pack/id/level); `pf2e_build.mon()` links official monsters via `@UUID` instead of rebuilding them, and `mon_lvl()` feeds the difficulty math. Most AP encounters use official creatures, so this is the scalable backbone for the remaining chapters. *Source:* Foundry/PF2e implementation. *Severity:* Minor. *Review:* none. (SOP §1.)
- **CHG-0116 — Encounter XP-budget calculator.** `pf2e_build.encounter()` computes XP and band (Trivial→Extreme) from creature levels vs party level + size, so every encounter card's difficulty is **computed at build** — difficulty is sanity-checked per run, not transcribed. *Source:* PF2e GMC budget math. *Severity:* Minor. *Review:* none. (SOP §2.)
- **CHG-0117 — verbatim() robustness.** Read-aloud extraction now repairs OCR drop-caps ("T he"→"The") and spans `<!-- image -->` / page markers that split a sentence mid-flow, so boxed text renders complete. *Source:* OCR fidelity. *Severity:* Cosmetic. *Review:* none. (SOP §5.)
- **CHG-0118 — Part Two fully converted** (14 events as journal pages in the Ch.1 entry): the king's death + city-in-anarchy framing, Investigating-the-Queen checks, the rumor mill, and Events 1–14 (Zellara's home, the brooch, Mad Prophet, Imps & Dragons, Meet the Mob, the Drunken Guard, Otyugh Uprising, Long Live the Queen!, Welcome to the Guard, the Ambassador's Secret, the Queen's Scapegoat, Into the Shingles, A Missing Body, A Lovely Day for an Execution). All DCs are `@Check` badges (re-judged to PF2e); rewards/treasure called out per event. *Source:* faithful conversion. *Severity:* n/a (content). *Journal:* yes. *Review:* none.
- **CHG-0119 — Part Two NPCs built to PF2e.** Custom actors: **Mad Prophet** (L−1, Filth Fever vector), **Korvosan Rioter** (L−1 reusable riot mook, routs at first damage), **Amin Jalento** (L1 non-combatant noble), **Grau Soldado** (L4 drunken watch-sergeant = `Sickened 1` baked in; recurring ally, meant to be defused not killed), **Trinia Sabor** (L3 framed artist with wand of *daze monster* + illusion tricks; recurring ally). Official creatures linked: Imp, House Drake, Otyugh. Difficulty: E3 Trivial · E4 Low (scales to Severe) · E5 Moderate (routing mob) · E6 Low solo · E7 Moderate. *Source:* faithful conversion + PF2e creature math. *Severity:* n/a. *Review:* none. (SOP §3–4c.)
- **CHG-0120 — Shingles Chase as the PF2e Chase subsystem.** Event 12's 15 obstacles re-judged to PF2e skills + simple DCs (every cell a `@Check` badge), with fall/recovery rules and Trinia's head-start logic. *Source:* PF1e chase → PF2e subsystem. *Severity:* Minor. *Review:* none.

#### Chapter 1, Part Three — B. All the World's Meat (full conversion)

- **CHG-0121 — Area B fully converted** (9 pages: overview + B1–B8) into the Ch.1 journal. Verbatim read-aloud (local injection) for B1/B3/B4/B5/B6/B7/B8; GM-secret reveals for the humanoid-meat horror, the Arkona/Vimanda conspiracy, and the living silver dagger; the grate-to-sewer as an Athletics break (DC 22). All DCs are `@Check` badges. *Source:* faithful conversion. *Severity:* n/a (content). *Journal:* yes. *Review:* none.
- **CHG-0122 — Area B NPCs.** Custom: **Cow Hammer Boy** (L2 deserter-guard mook, longbow→club, reusable Northgate brigand) and **Verik Vancaskerkin** (L4 longbow-specialist sergeant; recurring NPC, surrenders to evidence/Intimidation, carries the area's permanent reward — a **+1 striking composite longbow**). Official links: Reefclaw (×3, sewer) and Raktavarna rakshasa (the dagger-spy). Difficulty @L3: B1/B4 Low, sewer Low, B8 Moderate (Extreme only if the whole gang stacks — which the source avoids). *Source:* faithful + PF2e creature math. *Severity:* n/a. *Review:* none.
- **CHG-0123 — Area B treasure re-scaled to PF2e** (the PF1e 500 gp ring → ~25 gp art object; the ~2,000 gp stash → ~70 gp coin+gems), consistent with the Old Fishery rebuild (CHG-0008); the meaningful reward is Verik's runed longbow. Murder evidence (cuts/finger/stash) flagged as the lever that breaks Verik without a fight. *Source:* PF2e wealth-by-level. *Severity:* Minor. *Review:* none.

#### Chapter 1, Part Three — C. Eel's End (full conversion)

- **CHG-0124 — Condition-link infrastructure.** `scripts/extract_conditions.mjs` → `conditions_index.json` (all 43 pf2e conditions); `pf2e_build.CONDITIONS` now merges the full map (so `cond()` covers stupefied, paralyzed, confused, doomed, blinded, etc. for the whole AP), keeping the hardcoded keys for back-compat. *Source:* Foundry implementation. *Severity:* Minor. *Review:* none. (SOP §4.)
- **CHG-0125 — verbatim()/gate accept quote-terminated read-aloud.** Boxed text ending in `.'`/`.'` no longer trips the "split?" heuristic, and `verbatim()` stops cleanly at a closing apostrophe. *Source:* OCR fidelity. *Severity:* Cosmetic. *Review:* none.
- **CHG-0126 — Area C fully converted** (13 pages: overview + C1–C7, C9, C13–C15, C17) into the Ch.1 journal, with verbatim read-aloud, GM secrets (Blackjack/Vencarlo, Devargo's open fate, the trap-door, Chittersnap as the real spider-master), the dream-spider smoke save, and the knivesies minigame. Devargo's social resolution is rebuilt as a PF2e Diplomacy challenge (Aid, bribe scaling, knivesies wins, re-scaled letter price) — **the letters, not Devargo's death, are the objective**, with a stealth route through C14. *Source:* faithful conversion. *Severity:* n/a (content). *Journal:* yes. *Review:* none.
- **CHG-0127 — Area C NPCs.** Custom: **Eel's End Enforcer** (L3 sap-wielding muscle, subdues rather than kills), **Devargo Barvasi** (L6 poisoner-rogue, +3d6 sneak, spider-venom gauntlets, trap-door, invisibility-potion escape; not a forced kill), **Chittersnap** (L4 custom ettercap — the Remaster has none — web trap + venom + Spider Master). Official links: House Drake (caged Majenko), Hunting Spider (Remaster's "giant spider"), Dream Spider. Hopeful Thugs reuse the L−1 Rioter mook; the Sodden Hold reuses the Jigsaw Shark. Difficulty @L4: C1 Severe, C2 Extreme (both avoidable by design), C7 Moderate solo, C15 Low. *Source:* faithful + PF2e creature math. *Severity:* n/a. *Review:* none.
- **CHG-0128 — Area C treasure re-scaled** (Devargo's sea chest, C13: PF1e ~1,300 gp gems → ~120 gp art + ring of feather fall, scroll of *blur*, elixir of love, 2× dust of appearance, ~60 gp). Shiver (C9) flagged as story contraband, not loot. *Source:* PF2e wealth-by-level. *Severity:* Minor. *Review:* none.

#### Chapter 1, Part Three — D. The Dead Warrens + Chapter Conclusion (full conversion)

- **CHG-0129 — Area D fully converted** (15 pages: overview + D1–D13 + Chapter Conclusion) into the Ch.1 journal, with verbatim read-aloud, GM secrets (Rolth absent, Vreeg in charge; Gaekhen's body in four parts across D4/D8/D11; the undead-Gaedren gut-punch in D13; Rolth's twin signature dagger), and the Returning-Gaekhen + execution + Blood-Veil-onset hand-off to Chapter 2. *Source:* faithful conversion. *Severity:* n/a (content). *Journal:* yes. *Review:* none.
- **CHG-0130 — Area D NPCs.** Custom (Remaster has no derro/stirge/ettercap): **Derro** (L2 insane minion), **Stirge** (L−1 blood-feeder), **Skeletal Owlbear** (L3 undead guardian), **Cabbagehead** (L4 ogrekin jailer), **Vreeg** (L7 derro-necromancer boss — Searing Ray / Vampiric Touch / Blindness / Force Missiles / Grave Touch / Conjure Shield, modelled as action+@Damage/@Check per the caster pattern; fly 30, sunlight-dazzled). Official links: Otyugh, Skeleton Guard, Necrophidius, Carrion Golem, Zombie Shambler (the human-zombie bodyguard = animated Gaedren if his body was left). New hazard: **Acid-Spraying Skulls** (L3 magic trap, 2-round delay, Reflex-basic acid). *Source:* faithful + PF2e creature math. *Severity:* n/a. *Review:* none.
- **CHG-0131 — Dead Warrens difficulty observed & addressed.** Per PF2e math a lone at-level creature is Trivial–Low for four PCs, so individual rooms compute light; rather than over-inflate, the dungeon is framed as an **attrition gauntlet** with the source's own reinforcement dynamic surfaced (derros converge via the crawl-spaces; pursuing skeletons), and the boss **Vreeg bumped L6→L7** so D13 lands a true **Severe** climax. *Source:* PF2e GMC budget + design fidelity. *Severity:* Minor. *Review:* none.
- **CHG-0132 — Area D treasure re-scaled to PF2e** (D4 ~350 gp necklace → ~35 gp; D10 book hoard → ~30 gp; D12 snuffbox → ~25 gp), with the meaningful rewards preserved as items: handy haversack of potions/scrolls (D7), wand of cure moderate wounds from rescued Tiora (D9), wand of spiritual weapon + ring of swimming + elixir of vision (D4). The plague-tomes in D10 foreshadow Blood Veil. *Source:* PF2e wealth-by-level. *Severity:* Minor. *Review:* none.
- **CHG-0133 — ✅ CHAPTER 1 "EDGE OF ANARCHY" COMPLETE** end-to-end: Old Fishery (pilot) + A City Gone Mad (14 events) + Blood and Bones (B/C/D) + Conclusion. One fat journal (80 pages), 22 actors, 3 hazards. All DCs `@Check`, every encounter difficulty build-computed, treasure on actors / documented, validate 0 problems + 0 content warnings.

<!-- CH2 — Seven Days to the Grave -->
#### Chapter 2 — Seven Days to the Grave (front matter — chapter started)

- **CHG-0134 — Per-chapter build architecture.** `verbatim()`/`_paras()`/`SRC_MD` (shared read-aloud) promoted into `pf2e_build.py`; cross-chapter container folders (`a_root`/`i_root`/`j_root`/`Adventure`/`s_root`) given **stable literal ids** so each chapter script nests under the same roots. New `scripts/build_ch2.py` (own journal "2. Seven Days to the Grave", distinct id seed `_idgen(220002)`, appends to the shared packs); added to `sync_to_foundry.sh`. *Source:* multi-chapter scaling. *Severity:* Minor. *Review:* none. (SOP §6–8.)
- **CHG-0135 — Ch.2 front matter built** (5 journal pages): Chapter Background (the full conspiracy — Kayltanya/Vorel's phage → Davaulus + Andaisin/Urgathoa + the vampire Ramoska → weaponized blood veil; tainted silver via a death's-head coffer; the *Direption* red-herring), Advancement & Running the Chapter (L4→8; the 7-day plague; the Second Harrowing tied to shields/Constitution), NPC Developments (Amin, Devargo/Chittersnap, Neolandus captured), Cressida's Concern (PCs cut loose from the Guard), Rise of the Gray Maidens. Explicitly wires the **Blood Veil Epidemic Clock** to start here. *Source:* faithful conversion. *Severity:* n/a (content). *Journal:* yes. *Review:* none.
- **CHG-0136 — Gray Maiden Foot Soldier** (L3) built — Ileosa's recurring elite enforcer (full plate + heavy shield + longsword/longbow, Shield Block, fights to the death), reused Ch.2–6. New gear template: full-plate. *Source:* faithful + PF2e creature math. *Severity:* n/a. *Review:* none.
- **CHG-0137 — Ch.2 Part 1 events + Ishani.** 3 journal pages (A Damsel in Distress — smuggle Trinia to Trots, rewards + her mithral dagger/wand; Yellow Lights & the First Symptoms — the *Direption* decoy, Grau's niece Brienna falls ill, **Epidemic Clock starts**, Blood Veil exposure Fort save; The Unwashed Masses — the Grand Vault under siege, the Missing Arbiter hook). New actor **Ishani Dhatri** (L5 Abadar healer ally — Heal font, Shield of Faith, Sanctuary, *remove disease*; the in-fiction Blood Veil cure). *Source:* faithful conversion. *Severity:* n/a (content). *Journal:* yes. *Review:* none.

- **CHG-0138 — Ch.2 Part 2 + Mission 1.** Pages: First, Do No Harm & the Queen's Physicians (Davaulus intro, the royal-decree handout, the masked cultist-doctors, the GM-secret that Davaulus is Red Mantis); Combating the Plague (mission framework + the un-preventable Old Korvosa quarantine that sets up Ch.3); Mission 1 — the Wreck of the Direption (underwater red-herring dungeon, A1 silt-eel nest / A2 Skinshear / A3 boss). New actors: **Queen's Physician** (L2 masked Urgathoan rogue-cultist), **Silt Eel** (L-1 venom swarm), **Yvicca** (L6 sea-hag druid boss — Horrific Appearance, Evil Eye, Tanglevine, Brackish Bolt; commands the reused Jigsaw Shark 'Skinshear'). Difficulty @L4: A1/A2 Trivial, A3 Moderate. *Source:* faithful conversion. *Severity:* n/a (content). *Journal:* yes. *Review:* none.

<!-- CH3 — Escape from Old Korvosa -->
<!-- CH4 — A History of Ashes -->
<!-- CH5 — Skeletons of Scarwall -->
<!-- CH6 — Crown of Fangs -->
