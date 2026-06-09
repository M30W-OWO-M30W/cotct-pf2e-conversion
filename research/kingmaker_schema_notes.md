# Kingmaker Schema Notes — what we reuse, and how we adapt it

Companion to `kingmaker_foundry_structure_audit.md`. This is the concrete
"reuse → adapt" mapping that drives the CotCT build scripts.

| Kingmaker pattern | Reuse? | How we adapt it for CotCT |
|---|---|---|
| **Adventure compendium pack** (one Adventure doc bundling everything, links remapped on import) | ✅ adopt | Add a `cotct-adventure` pack (type `Adventure`); one Adventure doc embeds folders+journals+scenes+actors+items. One-click import. Keep the separate per-type packs too (for piecemeal use). |
| **Bare world-UUID** intra-adventure links; **Compendium UUID** only for SRD | ✅ adopt | Intra: `@UUID[Actor.<id>]`, `@UUID[JournalEntry.<id>.JournalEntryPage.<id>]`, relative `@UUID[.<pageId>]`, `@UUID[Scene.<id>]`. SRD: `@UUID[Compendium.pf2e.pathfinder-monster-core.Actor.<id>]` (Gobblegut/Bloo). |
| **Few fat JournalEntries, one page per area/encounter/NPC** | ✅ adopt | Replace the pilot's 6 small entries with **one fat entry per chapter** (`1. Edge of Anarchy`) whose pages are: overview/run-sheet/scene-setup, one page per area (A1–A14), NPC pages, treasure, conversion notes. (Map-key/appendix/handout get their own entries at chapter scale.) |
| **`page.title.level` outline** (1 Part / 2 group / 3 room) | ✅ adopt | Level 1 = section headers ("Part 1: The Old Fishery"), 2 = location groups, 3 = each `A#` room / NPC / encounter page. `title.show:true`. |
| **Styled `section.*` HTML blocks** (description/encounter/skill/treasure/action/dialogue) + asides | ✅ adopt | Author page HTML with these exact classes; **ship `styles/cotct-journal.css`** (module.json `styles`) so they render polished with the default sheet. Read-aloud → `section.description`; encounters → `section.encounter` w/ `aside.right.token`. |
| **`@Check[...]` / `@UUID[...]` / `[[/r XdY]]` enrichers** instead of prose DCs/tables | ✅ adopt | Convert our DC text to `@Check[type:thievery|dc:15|...]` etc.; all cross-refs as `@UUID`; ad-hoc rolls `[[/r ...]]`. No tables for stat data (use section blocks). |
| **GM vs player:** CSS class for read-aloud; **ownership only for handouts** | ✅ adopt | GM content pages `ownership {default:-1}`, entry default `0`; future player handouts get their own pages at `{default:2/0}`. |
| **Scene Notes** (`entryId`+`pageId`) link pins → pages; pre-placed `hidden` hostile tokens | ✅ adopt | Build scene placeholders whose notes point at the area pages and whose tokens reference our actors (`actorId`, `actorLink:false`, `disposition:-1`, `hidden:true`). |
| **v13 `background` object + `foreground` roof + `thumb`**, grid px/distance/units | ✅ adopt | Scene `background.src` → expected Racooze map path; grid `type:1,size:<px>,distance:5,units:"ft"`. Positions flagged `NEEDS GM REVIEW` until map assets are added. |
| **Folders per document type**, root = AP name, `N. Chapter`, category leaves, 3-color | ✅ adopt | One folder tree per type rooted at "Curse of the Crimson Throne"; chapters `1.`–`6.`; Actor leaves `Creatures/Characters/Hazards/Treasure` + location subfolders. Consistent casing (fix Kingmaker's drift). |
| **prototypeToken** defaults (displayName/Bars 20, disposition -1, actorLink, hp bar, pf2e autoscale flags) | ✅ adopt | Add a `prototypeToken` block to every actor (the pilot actors lack it — **fix**); set `texture.src` to a token path placeholder, `flags.pf2e:{linkToActorSize,autoscale}`. |
| **`system.details.publication`** for source; `_stats.compendiumSource` for provenance | ✅ adopt | Set `publication.title:"Pathfinder: Curse of the Crimson Throne"` on actors/items; set `compendiumSource` to the pf2e SRD UUID for reskins (Crocodile etc.), null for homebrew. |
| **RollTables** (text+document results, `documentUuid`, chaining) foldered by chapter; linked from journals | ✅ adopt (later) | CotCT analogs = Korvosa rumor mill, random street/sewer encounters, Harrow draws, plague exposure. Built as `1dN` tables; out of pilot scope but folders reserved. |
| **`_key`** primary + embedded compound keys | ✅ already | Already implemented + validator-checked (the empty-pack fix). Extend to folders/scenes/adventure/notes/tokens. |
| Custom **journal sheet module** (`KingmakerJournalSheet`) | ⚠️ partial | We do **not** ship a sheet class; instead ship CSS for the same classes. Degrades gracefully on the stock sheet. |
| **Scene Packer / world-explorer / pathmuncher / kingmaker-tools** flags | ❌ drop | Tooling/world artifacts — omit entirely. |
| **Kingdom / camping / army / hexploration** subsystems | ❌ N/A | CotCT doesn't use them. (Cinderlands uses light Hexploration as a *rules* reference, not the Kingmaker hex module.) |
| Kingmaker **maps/art/tokens/audio/prose** | ❌ never | Add maps separately; token art = placeholders. |

## Build implications (applied in the pilot rebuild)
1. New `scripts/pf2e_build.py` shared helpers: `folder()`, `journal_entry()`,
   `page()`, section-block emitters (`s_desc/s_encounter/s_skill/s_treasure`),
   `scene()`, `note()`, `token()`, `adventure()`, plus `_key` stamping.
2. Per-type **folders** for the AP + Ch.1.
3. Journals rebuilt: **one `1. Edge of Anarchy` entry**, Kingmaker page model +
   section CSS classes + `@Check`/`@UUID` enrichers + outline levels.
4. **prototypeToken** added to every actor; `publication`/`compendiumSource` set.
5. **Scene** placeholder(s) for the Old Fishery with notes→pages + staged tokens
   (`NEEDS GM REVIEW` positions).
6. **`cotct-adventure`** Adventure pack bundling it all; `module.json` gains the
   adventure pack + `styles`.
7. Validator extended: folders, scenes, notes (entryId/pageId resolve),
   adventure embeds, section-class presence.
