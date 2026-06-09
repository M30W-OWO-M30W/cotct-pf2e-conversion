# Curse of the Crimson Throne — PF2e Conversion Foundry Module

A Foundry VTT module converting the Pathfinder **1e** Adventure Path
*Curse of the Crimson Throne* to Pathfinder **2e**.

## What's in here

| Pack | Foundry type | Contents |
|------|--------------|----------|
| `cotct-journals`   | JournalEntry | GM overview, per-chapter/area journals, conversion notes, indices |
| `cotct-actors`     | Actor (npc/creature) | Converted NPCs & monsters (or links to official pf2e compendium actors) |
| `cotct-hazards`    | Actor (hazard) | Converted traps, haunts, environmental hazards |
| `cotct-items`      | Item | Story-critical & custom magic items |
| `cotct-rolltables` | RollTable | Harrowing draws, random encounters, loot |
| `cotct-scenes`     | Scene | Scene planning placeholders (add maps for play) |
| `cotct-macros`     | Macro | Subsystem helpers (Harrow, plague tracking, influence) |

## Requirements

- **Foundry VTT** v12–v13  *(verify against your install — see `CONVERSION_NOTES.md` § Versions)*
- **Pathfinder 2e system** ≥ 6.0.0 (Remaster-era) *(verify)*
- Your own **map/art files** (none are shipped — see `assets/README.md`)

## Build the compendium packs

Pack contents are versioned as readable JSON (`packs/<pack>/_source/*.json`, one
document per file) and compiled to Foundry's LevelDB format at build time.

```bash
cd foundry-module
npm install                 # installs @foundryvtt/foundryvtt-cli
npm run validate            # structural + link checks (run before every build)
npm run build               # _source/*.json  ->  packs/<pack> (leveldb)
# npm run extract           # reverse: leveldb -> _source/*.json (after editing in Foundry)
```

## Install into Foundry

1. Build the packs (above).
2. Copy this `foundry-module/` folder into your Foundry `Data/modules/`
   directory, renamed to `cotct-pf2e-conversion/`
   (or symlink it), so `module.json` sits at
   `Data/modules/cotct-pf2e-conversion/module.json`.
3. Launch your PF2e world → **Manage Modules** → enable
   *"Curse of the Crimson Throne — PF2e Conversion"* (restart the
   server first so Foundry detects a newly-added module folder).
4. **One-click import (recommended):** open the **Compendium Packs** sidebar →
   *"Curse of the Crimson Throne (PF2e)"* folder → **`CotCT: Adventure (import
   this)`** → open the **Adventure** document → **Import**. This recreates the
   whole organized tree (folders, the chapter journal, the Old Fishery scene with
   map-note pins + staged tokens, the NPCs/hazards, and the treasure) with all
   internal links intact — the Kingmaker import model.
   *Piecemeal alternative:* browse the per-type packs (`cotct-journals`,
   `cotct-actors`, …) and drag individual documents.
5. **Maps:** install **Racooze's CotCT battlemaps**
   (or drop your own at `assets/maps/01-old-fishery.webp`), open the **Old
   Fishery** scene, set the background, and nudge the pins/tokens onto the map
   (they're staged + flagged `NEEDS GM REVIEW`). Then click a pin → it opens that
   area's journal page; reveal the hidden tokens to start the fight.

## How to read the conversion

Every area journal answers the project's quality-bar questions:
**What changed? Why? Where is it in Foundry? Is it balanced? Is it PF2e-native?
Is the treasure right? Is the story preserved? What needs GM review?**

Cross-document context lives in the project root (one level up):

- `conversion_audit.md` — full content map & risk assessment
- `PROJECT_PLAN.md` — phases, methodology, version targets
- `conversion_change_log.md` — every change, with severity & GM-approval flags
- `research/research_index.md` — sources & adoption decisions
- `reports/` — encounter balance, NPC/monster, treasure, DC/skill, Foundry validation
