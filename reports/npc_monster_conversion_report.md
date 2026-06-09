# NPC / Monster Conversion Report

Method (per `research/research_index.md` §G.7): **two-tier** — link an official PF2e
actor when a clean match exists; build a custom PF2e NPC otherwise. All builds use
the pf2e v7 schema. Foundry actor paths are `packs/actors/_source/*.json`
(compiled to the `cotct-actors` pack).

> Scope: **Chapter 1 — Old Fishery (pilot)**. Later chapters append below.

| Original (PF1e) | PF2e build | Lvl | Role | Source | Why | Foundry actor | GM review |
|---|---|---|---|---|---|---|---|
| **Gaedren Lamm** (old human expert 4/rogue 2, CR 2) | **Custom NPC** | 2 | First villain; frail sniper | this module | No official "frail crime-lord sniper"; needs Limping Gait + Spur the Beast signature | `gaedren-lamm.json` | ⚠️ confirm Severe @L1 |
| **Yargin Balko** (human expert 3, CR 1) | **Custom NPC** | 1 | Acid-thrower fence; door-answerer | this module | Alchemist flavor (acid flasks) + flee-to-warn behavior | `yargin-balko.json` | ok |
| **Hookshanks Gruller** (gnome rogue 2, CR 1) | **Custom NPC** | 1 | Taskmaster; hides among orphans | this module | Gnome rogue w/ Sneak Attack + surrender/inform branch | `hookshanks-gruller.json` | ok |
| **Giggles** (half-orc fighter 2, CR 1) | **Custom NPC** | 1 | Bruiser; nonlethal capturer | this module | Bludgeoner (nonlethal) + Orc Ferocity | `giggles.json` | ok |
| **Gobblegut** (alligator = crocodile, CR 2) | **Official: Crocodile** (link) | 2 | Boss muscle | Monster Core (`pf2e.pathfinder-monster-core.Actor.2rMLYkUR47ZCQMUg`) | Exact match; Olliebird used the same; no rebuild | *(referenced — rename token "Gobblegut")* | ok |
| **Bloo** (dog, CR 1/3) | **Official: Guard Dog** (link) | −1 | Alarm dog | Monster Core (`...Actor.KHTYbQgR5hnFZdGL`) | Exact match | *(referenced)* | ok |
| **Drain spider** (CR 1/4) | **Custom NPC** (tiny) | −1 | Nest vermin (A10/A11) | this module | No clean tiny weak spider in MC; needs the vermin-repellent interaction + drain venom | `drain-spider.json` | ok |
| **Jigsaw shark** (CR 1) | **Custom NPC** (aquatic) | 1 | Under-fishery hazard-creature | this module | No reef/river shark in MC at L1; needs "only leaps if attacked" behavior | `jigsaw-shark.json` | ok |
| **Lamm's Lamb / orphan** (young human expert 1, CR 1/3) | **Custom NPC** (non-combatant) | −1 | Moral element; rally/aid | this module | Deliberately non-combatant; rescue is the story, not XP | `lamms-lamb.json` | ok |

## Build rationale & notes

- **Gaedren (L2)** is intentionally *below* L2 defensive benchmarks (HP 30, frail Fort) and *above* on Reflex/Will + a Nimble Dodge reaction — a glass-cannon sniper, not a tank. His danger is **Spur the Beast** (turning Gobblegut into a weapon), not his own attacks. This converts the design intent ("frail catalyst, scary pet") into PF2e rather than copying his weak PF1e numbers. *Drained from PF1e:* sneak attack, evasion, Limping Gait (Speed 15). *Added:* Nimble Dodge, Spur the Beast (action-economy/interest fix).
- **Gobblegut / Bloo** are **referenced, not rebuilt** — the canonical "use the official actor" path. The encounter/journal entries link the compendium actors and instruct the GM to rename the token. (Elite Crocodile is the 5-/6-PC scaling lever.)
- **Drain Spider** carries a 1-stage **Drain Spider Venom** (Fort DC 15) and the **vermin-repellent auto-repel** rule (PF1e "auto-fails save vs repellent" → PF2e "won't approach a coated creature"). This preserves the exploration reward (loot the repellent in A13 to trivialize the nest).
- **Jigsaw Shark** keeps the "only leaps onto the underpier if attacked first" restraint as a passive, so it stays an *avoidable* hazard-creature rather than a mandatory fight.
- **Orphans** are modeled as **non-combatants** with a **Rally to the Heroes** passive (Diplomacy DC 15 → Aid) and a **Cower** passive. **They are not an XP source for killing** — rescuing them is the chapter's heart (see Treasure/XP and Conversion Notes).

## Recurring-NPC forward links (build-once, reuse)
Gaedren's son **Rolth** (Ch.2 boss; appendix p.452) and the **Dead Warrens** cast are out of pilot scope but flagged: if the PCs leave Gaedren's body in A14, Rolth animates it as a zombie in D13 (track in the campaign state). Zellara (the Harrow spirit) is handled as a story NPC + the Harrow Deck item, not a stat block.

*(Later chapters append here.)*
