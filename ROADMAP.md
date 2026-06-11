# CotCT PF2e Conversion — Remaining Work Roadmap

*Updated 2026-06-11 (v0.6.0). **TIER 1 IS COMPLETE** — all 38 prepared scenes (466 pins, 554 staged tokens, walls/thumbs/backgrounds, per-chapter Prepared Scenes pages, Complete-Campaign Adventure) and the affliction/effect automation (Blood Veil staged effect + suppressant + war paints + artifact markers, boss rule elements) shipped, fleet-QA'd, and triple-audited.*

*Original framing: The conversion itself is complete (Ch.1–6 + appendices/postgame,
community DC + statblock authority, full token-art coverage). Everything below is
"make it play better at the table," ordered by value-per-effort.*

**Recently completed, for context:** prepared-scene pipeline pilot (Old Fishery: Racooze
walls/doors injected at build, true-position pins, 20 staged tokens) · full per-actor
token art (232/232: AP PDF extraction → AoN official art → game-icons glyphs, one-by-one
visual QA pass).

---

## Tier 1 — High value, high effort

### 1. The remaining 37 prepared scenes
The pipeline exists; what's left is per-scene room keying (pins at area centers, tokens
staged per encounter — now with proper art from the start). Natural batches:
- **Ch.1**: Eel's End, All the World's Meat, the Dead Warrens
- **Ch.2**: the Direption, Wererat Sewer Den, Racker's Alley, Carowyn Manor,
  Hospice + Temple of Urgathoa, Lavender/Vendra's apartment
- **Ch.3**: Arkona Palace, the **Vivified Labyrinth** (design problem: its four rotation
  states — candidate for four linked scenes or scene regions), Pilts's Palace,
  Vencarlo's home + Artist's Lair
- **Ch.4**: Acropolis of the Thrallkeepers, House of the Moon + Cindermaw's grounds,
  Flameford + Bolt Rock, Deathhead Vault
- **Ch.5**: Scarwall — barbican + 7 floors + guest wing + caverns (biggest cluster)
- **Ch.6**: Castle Korvosa's 7 levels, the Sunken Queen

Recommend chapter-sized batches ahead of play, Ch.1 first.

### 2. Affliction & effect automation
- **Blood Veil as a real pf2e affliction item** with stage rule elements (auto-applied
  drained/enfeebled icons, stage advancement) — the campaign's signature mechanic,
  currently rules-text only
- Effect items: Shoanti war paints, the suppressant, Ukwar's drain, the Crown of Fangs
  corruption clock, Serithtial's anti-Ileosa rider
- Rule elements on the ~30 most-fought community actors (auras, frightful presence,
  poison routines) — the 2022-era exports mostly lack them

---

## Tier 2 — High value, moderate effort

### 3. Patch backlog (one afternoon, closes every known wart)
- Community "Elite Erinys" export carries **base** erinys numbers — bake the elite
  adjustment or relabel
- Doubled gear from the treasure merge: Mavrokeras's two chains, Devargo's duplicate
  healing potions/keys, Amin's signet overlap, Giggles' bow
- Object-stat divergences vs the community docs: portcullis Hardness (ours 10/60 vs
  their 18/72), Sunken Queen walls (24/1,620 vs 36/216), G3 manacles valued 100 gp
  (AP: 1,000 gp/set)
- G14 vat-contact onset: community reads plain failure = skip onset (adopted as
  written); decide if the harsher crit-fail-only reading is wanted
- Convention-DC flags for GM preference: ch3 E21 cells (30 vs level-based 27),
  C12 Salvator's cell (20); Anizora L15 doc vs L14 prose

### 4. Mega-page splits
Per-area pages with prev/next navigation for the cluster pages (Scarwall B25–B37,
Castle Korvosa A12–A25 / A26–A44 / A67–A95, Deathhead Vault E-blocks). Mechanical,
zero design risk, big mid-session lookup win.

### 5. Encounter scaling aids
Pre-built Elite/Weak variants for the notorious spike fights (Ileosa's finale, the
Scarwall boss chain, Ch.2's Andaisin); per-encounter party-size sidebars beyond the
current 3/5/6-player notes; underleveled-party warnings at the chapter seams
(the classic Scarwall TPK driver).

---

## Tier 3 — Moderate value, low effort

### 6. GM-utility macros
- **Epidemic Clock tracker** — advance/recede buttons writing to a campaign-state journal
- **Survivor Count tally** for Ch.2
- **Harrowing dealer** — runs a full reading (role card, spread, suit boons) instead of
  raw rolltable draws
- Milestone/level-up checklist per chapter

### 7. Player-facing compendium
Handouts, campaign backgrounds, and player-knowledge pages in a separate journal with
player ownership defaults — shareable without spoiler risk. Optionally an assembled
spoiler-free Player's Guide page.

### 8. Session-prep pages
A "running Part X next session" checklist per chapter part: actors to have ready,
clocks that tick, handouts likely to come up, scene to preload.

### 9. Navigation & reference extras
Cross-linked dramatis personae / NPC relationship map; a campaign calendar/timeline
tracker page (ties into the Epidemic Clock's downtime weeks).

---

## Tier 4 — Speculative / bigger swings

### 10. Postgame fleshing
The three stub arcs (Kazavon Rises / Sorshen's Legacy / Rulers of Korvosa) authored
into fully keyed adventures. Only worth it if the table will play past 17.

### 11. Remaster polish on absorbed statblocks
The community exports predate the Remaster (legacy spells, alignment fields). pf2e's
runtime migrations handle correctness; a curation pass could swap legacy spells for
remastered equivalents. **Recommend waiting** — system migrations keep improving.

### 12. Scene mood lighting (rolled back, revisitable)
The grading experiment is dead, but authored lighting alone (no image edits) remains a
one-evening test — Scarwall at darkness 0.7 with cold point-lights is the candidate.

### 13. Audio
Ambient playlist compendium per region (Korvosa streets, Cinderlands, Scarwall) from
CC-licensed sources.

### 14. Distribution
GitHub Releases + a manifest URL so the second PC updates in-app instead of via
Desktop zips. (Private repo → needs a token-authenticated manifest or public releases
of the no-verbatim build — has IP implications, think first.)

### 15. Treasure audit refresh
Re-run the Treasure-by-Level audit post-statblock-merge (the gear dedup changed actor
inventories); add party-size wealth scaling notes.

### 16. Validator additions
Link-label vs document-name drift, dead-actor-id detection (the Danse Macabre dangling
link class), enricher label checks.

### 17. Live render smoke test
Drag community-era actors into a world, confirm pf2e migrations render sheets cleanly
(effectively happens through play).

---

**Recommended next bite:** Tier 2 #3 (patch backlog) as the quick win, then Tier 1 #1
chapter-by-chapter (Ch.1's three remaining scenes first), with Tier 1 #2 (Blood Veil
automation) before Chapter 2 hits the table.
