# No-Friction GM Usability Report

Verifies that the GM can run the adventure **without leaving Foundry**. Any area
where the GM must use an external tool is flagged `FAILED NO-FRICTION REQUIREMENT`.

> Scope: Chapter 1 pilot — the Old Fishery (A1–A14). The mechanism scales to Ch.2–6.

## Per-area checklist (Old Fishery)

For every area page (A1–A14): ✅ = satisfied in the current build.

| Check | Result |
|---|---|
| GM can open the scene and click a map note | ✅ Old Fishery scene, 14 pins (one per area) |
| Map note opens the converted area journal page | ✅ each pin's `entryId`+`pageId` → the matching A# page (validated) |
| Converted page includes or one-click-links the original source | ✅ every page's 📖 *Open the original text* link → embedded PDF at the cited page |
| Actors linked | ✅ encounter blocks link the converted actors (+ official Crocodile/Guard Dog) |
| Hazards linked | ✅ A3/A9 link the Slippery Boardwalk / Rotten Ship Deck hazards |
| Treasure linked | ✅ A13/A14 + Treasure page link the item docs |
| PF2e mechanics visible without excessive scrolling | ✅ section blocks (encounter/skill/treasure) near the top; lore not buried |
| Original PDF reachable from the journal | ✅ via the per-area link and the "Original Adventure (PDF)" entry |
| Any info requiring external lookup | **None** — full text is in the embedded PDF inside Foundry |

**Result: no area is flagged `FAILED NO-FRICTION REQUIREMENT`.** Everything needed
to run the Old Fishery is reachable from the scene + the chapter journal + the
embedded PDF, all inside Foundry.

## The full GM loop (verified, headless)
Scene pin → converted area page (mechanics, paraphrased read-aloud, linked
actors/hazards/treasure) → 📖 link → embedded PDF at the cited page (complete
official text + maps) → back. Reveal the pre-staged hidden tokens to start combat.

## Navigation
Beyond scene pins, an **Indexes** journal (Original Source · Area · NPC · Encounter
· Treasure · Hazard) gives direct links to every converted area/actor/item/hazard
and the chapter source PDF — the GM never browses page-by-page.

## Caveats (not no-friction failures)
- **Source PDF is chapter-split** (~5–7 MB) so it opens fast; each area's 📖 link
  targets the chapter PDF at the cited page. **Exact-page jump** needs the free
  **PDF Pager** module (page offset −9 on the Ch.1 chapter PDF); without it the
  link opens the chapter PDF and the printed page number tells the GM where. Either
  way the GM stays in Foundry.
- **Maps**: none shipped (copyright). Pin/token *positions* are staged
  (`NEEDS GM REVIEW`) until the GM drops in a battlemap (Racooze's free CotCT
  maps). The *links/flow* work without the map; only placement needs the image.
- **Live render confirmation** of the PDF page in Foundry v14 is the one step not
  verifiable headlessly (`NEEDS GM REVIEW`).

## Required before scaling to the full AP
1. GM confirms (one-time) the embedded PDF renders and the Adventure imports in
   Foundry v14 / pf2e 8.2.0.
2. (Optional) install PDF Pager for exact-page links.
3. Apply the same per-area PDF-link + scene-pin pattern to Ch.2–6 (the build
   helpers already do this; it's data entry per chapter).
