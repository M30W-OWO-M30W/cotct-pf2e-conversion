# Kingmaker Foundry Structure Audit

Reference: a Foundry **world export** of the official **pf2e-kingmaker** module
(`world.kingmaker….bak`, a ZIP of `data/` LevelDB + assets). Decoded to JSON
(structure only) at `.work/kingmaker_ref/` — **git-ignored; Kingmaker content ©
Paizo; no prose/art reused, schema/patterns only.** Target alignment: Foundry
**v13.351→v14**, pf2e system **7.x→8.x**.

Doc counts: **33 journals · 123 scenes · 779 actors · 76 items · 35 rolltables ·
257 folders · 79 macros · 367 playlist entries.**

---

## 1. Module manifest & pack structure

The export is a *world*, so no `module.json` is present, but provenance markers
(`_stats.compendiumSource`, asset paths) reveal how the shipped module packages:

- **Content split (critical):** the **module** ships the *adventure* — journals,
  scenes, maps, playlists, handout actors, and a **custom journal sheet** — while
  the **pf2e system** ships the mechanics (`kingmaker-features` 621 refs,
  `kingmaker-bestiary` 266 refs). Kingdom/camping live in a *separate* community
  module (`pf2e-kingmaker-tools`). Lesson: keep narrative (ours) separate from
  SRD mechanics (link to `pf2e.*` compendia).
- **Compat fields** (from world.json): `system:"pf2e"`, `compatibility:{minimum
  "13", verified "13.351"}`, `systemVersion "7.12.2"`. (Our build targets v14 /
  pf2e 8.2.0 — same shape, newer numbers.)
- **Pack format:** every doc is the fvtt-cli "unpacked" form with a `_key`
  (`!<collection>!<id>`; embedded `!<collection>.<embedded>!<parent>.<child>`),
  compiled to LevelDB. (We already use this.)
- **Custom journal sheet:** `flags.core.sheetClass =
  "pf2e-kingmaker.KingmakerJournalSheet"` registered by the module renders the
  styled adventure layout. → **We replicate the *look* by shipping a small CSS**
  (`module.json: styles`) that styles the same semantic `section.*` classes,
  rather than a custom sheet class.

## 2. Adventure document structure (the one-click import)

Kingmaker ships an **Adventure** compendium pack: a single `Adventure` document
that **bundles** folders + journals + scenes + actors + items + rolltables +
macros + playlists and, on import, **recreates the whole tree and rewrites all
bare world-UUIDs** (`Actor.<id>`, `JournalEntry.<id>`, note `entryId/pageId`,
`token.actorId`) to the importing world's fresh IDs while preserving every
cross-link. This is why intra-adventure links use **bare world UUIDs**, not
Compendium UUIDs (those are reserved for shared pf2e SRD content).

→ **Adopt:** a `cotct-adventure` pack of type `Adventure`; intra-module links use
bare `@UUID[Actor.<id>]` / `@UUID[JournalEntry.<id>.JournalEntryPage.<id>]` /
relative `@UUID[.<pageId>]`; SRD references use
`@UUID[Compendium.pf2e.<pack>.<Type>.<id>]`.

## 3. Journal structure

- **Few fat entries, many pages.** One `JournalEntry` per chapter (+ separate
  entries for map-keys, appendices, handouts); the **page** is the content unit —
  **one page per keyed location / encounter / NPC / handout** (a 70-page map-key
  entry exists). *Do not make an entry per room.*
- **Outline via `page.title.level`:** 1 = Part/section, 2 = location group, 3 =
  individual room/encounter/NPC; `title.show:true`. This builds the sidebar TOC.
- **Page schema:** `{name, type:"text"|"image"|"pdf"|"video", title:{level,show},
  text:{format:1, content:HTML, markdown:""}, image:{}, video:{controls,volume},
  src:null, system:{}, sort, ownership, flags, category:null, _id, _key}`.
- **Styled HTML section blocks** (rendered by the sheet CSS), not tables:
  `section.description` (boxed read-aloud), `section.encounter` (with
  `aside.right.token` portrait/token + `<ul><li>` creature line + `header.split`),
  `section.skill`, `section.action` (traits + `ul.outcomes`), `section.treasure`,
  `section.dialogue`, `section.milestone`; `aside.right.porthole` for NPC
  portraits. **Tables were not used.**
- **Inline enrichers:** `@Check[type:<skill>|dc:<N>|traits:action:<slug>]` (and
  `|basic:true`, `type:flat`); `@UUID[...]` for every cross-ref; `[[/r XdY]]` for
  ad-hoc rolls.
- **GM vs player:** read-aloud vs GM prose live in the **same page**, separated by
  CSS class (`section.description` vs plain `<p>`). **Per-page `ownership` is
  reserved for player handouts** (`default:2` = player-readable, `0` = hidden
  until revealed); GM content pages stay `{default:-1}` (inherit) and the entry
  default is `0` (GM-only).
- **Sort:** large spaced integers (~100000 steps), negatives to force order.
- **Folders:** `Kingmaker` → `Adventure` / `Hex Encounters` / `Appendices` /
  `Supplemental`.

## 4. Scene / map structure (the interactivity model)

- **Folders by chapter:** `Kingmaker` → `1. A Call For Heroes` → location
  sub-folders (`Aldori Manor`); plus `Settlements`, `Ancillary Maps`.
- **v13 background object:** `background:{src, fit:"fill", tint, …}` + pixel
  `width/height`; **no legacy `img`**. `thumb` auto-generated. Overhead/roof via
  scene-level **`foreground`** image + `foregroundElevation:20` (not roof tiles).
- **Grid:** battlemaps `grid:{type:1, size:<px-per-square>, distance:5,
  units:"ft"}`; regional hex map `type:2, size:275, distance:12, units:"miles"`.
- **Notes (map pins) — THE link:** each `note` has **`entryId`** (JournalEntry
  `_id`) + **`pageId`** (the specific page `_id`), `text` (room key e.g. "K1a"),
  `x/y`, `texture.src:"icons/svg/book.svg"`, `iconSize:40`, `fontSize:32`,
  `textAnchor:1`, `_key:"!scenes.notes!<scene>.<note>"`. All a dungeon's pins
  share one `entryId` and differ by `pageId`. **Click pin → opens that page.**
- **Tokens pre-placed:** encounter monsters staged as tokens (`actorId`,
  `actorLink:false`, `disposition:-1`, `hidden:true`, grid-aligned `x/y`,
  `flags.pf2e:{linkToActorSize,autoscale}`, a `delta` override); duplicates =
  multiple tokens sharing one `actorId`.
- **Walls/lights/sounds:** dungeons carry walls (100–700) + lights (torch
  animation); sounds sparse; **regions/templates/drawings ~unused**.
- **GM flow:** open Scene → see lettered pins → click pin → area page → reveal the
  pre-placed hidden hostile tokens → open each actor. **We replicate this chain.**

## 5. Actor / NPC structure

- **Flat files, logical folders:** `Root → "N. Chapter" → {Creatures, Characters,
  Hazards, Treasure}` (+ location subfolders), depth ≤4.
- **Types:** `npc` (522), `loot` (154, treasure caches, `actorLink:true`),
  `hazard` (49), `character` (40), one `party`.
- **prototypeToken:** `texture.src` = token art (separate from `img` portrait),
  `displayName:20`/`displayBars:20`, `disposition:-1`, `actorLink:false` for
  generics / `true` for recurring named + loot, `bar1.attribute:"attributes.hp"`,
  `sight.enabled:false` for npc/hazard, `flags.pf2e:{linkToActorSize,autoscale}`.
- **Notes:** GM role/tactics/recall-knowledge in `system.details.publicNotes`
  (HTML); short tagline in `blurb`; secrets in `privateNotes`. **No custom
  "tactics" field, no GM-only boolean** — visibility via ownership + the sheet's
  GM tab. Hazards use `details.{description,disable,routine,reset,isComplex}`.
- **Source:** `system.details.publication:{title,authors,license,remaster}` (the
  legacy `details.source` is unused). Official-vs-custom via
  `_stats.compendiumSource` (set to the SRD UUID for reskins, null for homebrew).
- **Linking:** journals → `@UUID[Actor.<id>]{label}`; scenes → `token.actorId`.

## 6. Item / hazard / encounter structure

- **Items** foldered `Root → "N. Chapter" → {Treasure, Effect}` (by chapter, not
  global type). pf2e item schema (`system.price.value.gp`, `traits.rarity`,
  `identification`, `publication`, `level`).
- **Hazards** are **Actors** (`type:"hazard"`), foldered under a chapter's
  `Hazards`.
- **Encounters are journal-driven** (a `section.encounter` page block linking the
  actors) **and scene-driven** (pre-placed hidden tokens) — there is **no separate
  "encounter" document**. Treasure is linked from the area page's
  `section.treasure` via `@UUID[...Item...]`.
- **RollTables** foldered `Root → Adventure → "N. Chapter"` + supplemental (`Zone
  Encounters`, `Weather`, `Rumors`). Results are `text` (with embedded `@UUID`) or
  `document` (`documentUuid` → Actor/Compendium/RollTable for chaining). Referenced
  from **journals** via `@UUID[RollTable.<id>]` (scenes carry none).

## 7. Accessibility & usability (what makes it run well)

- **Few clicks:** Scene → pin → area page (1 click) → linked actor (1 click). An
  area page is self-contained (read-aloud + GM + encounter + skills + treasure +
  links) so a room runs from **one page + the scene**.
- **GM/player separation** via CSS class (read-aloud vs GM prose) + ownership for
  handouts — no scattered duplicate docs.
- **Low clutter:** styled section blocks instead of walls of text or big tables;
  outline (`title.level`) makes the TOC scannable; consistent chapter foldering.
- **Adventure pack** = one import, links intact.

## 8. Technical patterns (verbatim formats to reuse)

- **_key:** `!journal!<id>`, `!journal.pages!<entry>.<page>`, `!scenes!<id>`,
  `!scenes.notes!<scene>.<note>`, `!scenes.tokens!<scene>.<token>`,
  `!actors!<id>`, `!actors.items!<actor>.<item>`, `!items!<id>`, `!tables!<id>`,
  `!tables.results!<table>.<result>`, `!folders!<id>`, `!adventures!<id>`.
- **UUID forms:** intra-adventure **bare** `@UUID[Actor.<id>]`,
  `@UUID[JournalEntry.<id>.JournalEntryPage.<id>]`, relative `@UUID[.<pageId>]`,
  `@UUID[Scene.<id>]`, `@UUID[RollTable.<id>]`; SRD `@UUID[Compendium.pf2e.<pack>.<Type>.<id>]`
  (legacy no-Type form also resolves); page-anchor `…#slug`.
- **Note link:** discrete `note.entryId` + `note.pageId` (not a UUID).
- **Token link:** `token.actorId` + `actorLink` + `delta`.
- **Flags:** `core.sheetClass` (custom sheet), `pf2e.*` (system: rulesBasedVision,
  hearingRange, editHazard, freeCrafting…), `pf2e-kingmaker:{simpleNPC}` (rare).
  Tooling flags (`scene-packer.hash`, `pathmuncher`, `world-explorer`,
  `pf2e-kingmaker-tools`) are **module/world artifacts → we OMIT them**.
- **_stats:** `{systemId:"pf2e", systemVersion, coreVersion, createdTime,
  modifiedTime, lastModifiedBy, compendiumSource, duplicateSource, exportSource}`.
- **Folders:** `{name, type, folder:<parent|null>, sorting:"a"|"m", sort,
  color, description:"", flags, _key}`; one tree **per document type**, each
  rooted at a folder named after the AP; 3-color scheme (root / chapter /
  supplemental); `#000000` for location subfolders.

---

## What we deliberately will NOT copy
- Kingmaker **maps, art, tokens, audio, prose** (copyright — we ship none; GM adds
  Racooze's free battlemaps).
- **Kingdom/camping/army/hex** subsystems & their `pf2e-kingmaker-tools` flags —
  CotCT has none of these (it uses Influence/Reputation/Chase/Infiltration/Harrow
  instead; see `research/research_index.md` §F).
- Tooling flags (`scene-packer`, `world-explorer`, `pathmuncher`) and Kingmaker's
  drifting folder capitalization (we normalize).
- A **custom journal sheet module** — we ship CSS for the same `section.*` classes
  instead (works with the default sheet; degrades gracefully).

*(Adaptation mapping → `kingmaker_schema_notes.md`. Pilot conformance →
`reports/kingmaker_style_comparison_report.md`.)*
