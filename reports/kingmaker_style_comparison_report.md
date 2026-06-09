# Kingmaker-Style Comparison Report — Pilot (Old Fishery)

Compares the rebuilt pilot against the Kingmaker reference
(`research/kingmaker_foundry_structure_audit.md`). Verdict at the bottom.

Pilot build (verified by round-trip extract): **Adventure pack bundling 11 folders
· 1 journal (20 pages) · 1 scene (14 map-note pins / 10 staged tokens) · 9 actors
· 6 items**; per-type supporting packs; ships CSS for the journal section styling.
`validate.mjs`: **0 problems, 53 links resolve**. `npm run build` compiles all
packs to LevelDB; round-trip extract confirms populated data.

## 1. What matches Kingmaker-style usability

| Dimension | Kingmaker | Pilot | Match |
|---|---|---|---|
| **One-click import** | `Adventure` pack bundling everything, links remapped | `cotct-adventure` Adventure pack (folders+journal+scene+actors+items) | ✅ |
| **Folder hierarchy** | per-type trees, `Root → N. Chapter → category`, 3-color | per-type trees rooted "Curse of the Crimson Throne" → "1. Edge of Anarchy" → Creatures/Hazards/Treasure, crimson 3-color | ✅ |
| **Fat journal, page-per-area** | one entry/chapter, page per keyed area | one "1. Edge of Anarchy" entry, 20 pages (overview/scene/features + A1–A14 + NPCs/treasure/conv) | ✅ |
| **Outline via `title.level`** | 1 Part / 2 group / 3 room | level-1 overview, level-2 groups, level-3 area pages | ✅ |
| **Styled section blocks** | `section.description/encounter/skill/treasure/...` + asides, rendered by sheet CSS | same classes + shipped `styles/cotct-journal.css` (works on default sheet) | ✅ |
| **Inline enrichers** | `@Check`, `@UUID`, `[[/r]]` | `@Check[...]` for all DCs; `@UUID` for all cross-refs | ✅ |
| **Scene map-note → journal page** | `note.entryId`+`pageId` | 14 pins, each `entryId`=the entry, `pageId`=its area page (verified resolvable) | ✅ |
| **Pre-placed hidden hostile tokens** | `actorId`, `actorLink:false`, `disposition:-1`, `hidden:true` | 10 staged tokens linking the converted actors, hostile+hidden | ✅ (positions flagged — see gaps) |
| **prototypeToken on actors** | full token config, pf2e autoscale | every actor has a `prototypeToken` (disposition, bars, `flags.pf2e.linkToActorSize/autoscale`) | ✅ |
| **GM vs player** | CSS class for read-aloud; ownership for handouts | `section.description` (read-aloud) vs `section.gm-notes`; entry GM-only | ✅ |
| **Actor notes model** | role/tactics in `publicNotes`, source in `publication` | tactics/role in `system.details.publicNotes`; `publication.title` set | ✅ |
| **Use official SRD actors** | link `Compendium.pf2e.*` | Gobblegut/Bloo → `Compendium.pf2e.pathfinder-monster-core.Actor.*` | ✅ |
| **Run a room from one page + scene** | yes | each A# page has read-aloud + GM + encounter (linked actors) + skills + treasure + conv | ✅ |
| **No appended raw source dumps** | concise pages | summaries + page refs only; **no raw PDF text** | ✅ |
| **`_key` (primary + embedded compound)** | required | implemented + validator-enforced | ✅ |
| **Local conversion notes** | — (Kingmaker has no PF1e origin) | per-area `section.conversion` + a Conversion Notes page + global change log | ✅ (exceeds) |

## 2. What intentionally differs (and why)

- **No custom journal sheet module.** Kingmaker registers
  `KingmakerJournalSheet`; we instead **ship CSS** for the same `section.*`
  classes. *Why:* avoids shipping a code module; renders polished on the stock
  pf2e sheet and degrades gracefully. Trade-off: layout is slightly simpler than
  Kingmaker's bespoke sheet.
- **No maps/art/tokens/audio shipped.** *Why:* copyright. Scenes reference
  expected map paths and **Racooze's free battlemaps**; token art = placeholder
  paths the GM supplies.
- **No kingdom/camping/army/hex subsystems** or their `pf2e-kingmaker-tools`
  flags. *Why:* CotCT doesn't use them (it uses Influence/Reputation/Chase/
  Infiltration/Harrow — see `research/research_index.md` §F).
- **Tooling flags dropped** (`scene-packer`, `world-explorer`, `pathmuncher`).
  *Why:* world/tooling artifacts, not content.
- **We keep per-type supporting packs** in addition to the Adventure pack (handy
  for dragging a single actor); Kingmaker leans almost entirely on the Adventure
  pack. Both import the same data.
- **`section.conversion` blocks + a Conversion Notes page** have no Kingmaker
  analog — added because this is a *conversion* (PF1e→PF2e traceability).

## 3. Gaps (need resolution; mostly map-dependent)

| Gap | Severity | Resolution |
|---|---|---|
| **Token/pin positions are staged in a grid, not on a real map** | Medium | No map shipped (copyright). Positions are `NEEDS GM REVIEW`; GM drops in Racooze's Old Fishery map and nudges pins/tokens. The *links* are correct; only x/y need the map. |
| **Gobblegut/Bloo not pre-placed as scene tokens** | Low | They're official compendium actors (not in our adventure), so a token can't reference them pre-import. The A13/A4 pages instruct the GM to drag the official Crocodile/Guard Dog and rename. |
| **One scene, not two floors** | Low | The fishery has two map levels; pilot ships one placeholder scene. Split into First/Lower floor scenes when the real map is added. |
| **No walls/lights** | Low | No map geometry to derive them from (we don't invent walls). Add after the map is placed. |
| **CSS look ≠ Kingmaker's bespoke sheet** | Low | Acceptable; our CSS covers the key blocks. Could be expanded. |
| **RollTables not yet built** | Low (out of pilot scope) | Korvosa rumor mill / random encounters / Harrow draws — folders reserved; build in Phase 3. |
| **Broken links / missing UUIDs** | None | `validate.mjs` = 0 problems; all 53 intra-module links + 14 note links + 10 token links resolve. |
| **Adventure-import smoke test in live Foundry** | Open | Compile + round-trip pass headlessly; a human still needs to click "Import" in Foundry v14 once to confirm UX (the one thing I can't run here). |

## 4. Required fixes before scaling to the full AP

1. **Live import smoke test** (GM): import `cotct-adventure` into a v14/pf2e-8.2.0
   world, confirm the folder tree, journal section styling, scene pins, and token
   placement render as expected. *(Only blocker I can't self-verify.)*
2. **Map workflow decision:** confirm Racooze coverage per location; standardize
   the scene-per-map split and the `assets/maps/<chapter>-<slug>.webp` naming so
   Phase-3 scenes are consistent.
3. **Promote the pilot build into reusable chapter tooling:** the shared
   `pf2e_build.py` + a per-chapter data file, so each chapter's actors/journal/
   scene/adventure are generated the same way (the pilot proved the helpers).
4. **Add the recurring subsystems** (Harrow, Reputation/Influence, plague clock)
   as journal pages + macros/rolltables, since they appear from Ch.1 onward.

## Verdict

**The pilot meets the Kingmaker-style usability standard** for everything that
does not require shipped maps: one-click Adventure import, foldered hierarchy,
fat section-styled journal, scene map-note→page links, pre-staged actor tokens,
prototype tokens, official-actor reuse, and zero broken links. The remaining gaps
are **map-dependent** (positions/walls/lights) and an **un-runnable-here live
import check** — both documented. **Cleared to scale to Phase 3** once the GM does
the one live-import smoke test.
