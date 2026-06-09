# Conversion Notes — design stance for the CotCT PF2e conversion

This file records the **standing decisions** that apply across the whole
conversion. Per-area changes live in each area journal's *Conversion Notes*
section and are aggregated in `../conversion_change_log.md`.

## Versions  *(✅ corrected with GM, 2026-06-09)*

| Target | Value | Status |
|--------|-------|--------|
| Foundry VTT | **v14 (build 363)** | ✅ confirmed |
| PF2e system | **8.2.0** | ✅ confirmed |
| Ruleset | PF2e **Remaster** (Player Core / GM Core / Monster Core) | ✅ correct — pf2e 8.x is Remaster-era |

Actor/item/hazard/journal JSON is authored against the **pf2e v8 schema** — the
templates in `.work/schema_ref/` were pulled from the pf2e repo's `master`, which
is itself version **8.2.0** (Foundry 14.360–14.363), so the schema matches the
target exactly. `module.json` declares Foundry `verified: 14` and pf2e
`verified: 8.2.0`. If the system later jumps a major version, re-run
`npm run validate` and rebuild; the system migrates most field changes on import.

## Ruleset: Remaster

Conversion uses **Remaster** terminology and math:
- Remaster spell/condition names (e.g. *Inflict* → *Harm* where relevant; "flat-footed" → **off-guard**).
- Monster Core stat blocks preferred over Bestiary 1–3 where a remastered version exists.
- Alignment removed; holy/unholy and the new edict/anathema framing used for fiends, undead servitors of Urgathoa, etc.
- Schools of magic dropped from spell traits.

## Party assumptions  *(default — confirm)*

- **4 PCs**, standard ability boosts, no free archetype, no Automatic Bonus Progression.
- Encounter math uses the **4-player XP budget** (Trivial 40 / Low 60 / Moderate 80 / Severe 120 / Extreme 160).
- Each encounter record also notes adjustments for **3, 5, and 6 PCs** (±10/±20/±30/±40 per the party-size scaling table).
- If your table uses Free Archetype or a different size, every "Severe/Extreme" flag in the balance report should be re-checked.

## Conversion philosophy

1. **Story first.** Plot, villains, location flow, and major NPC roles are
   preserved. Changes are documented and, when major, flagged
   `REQUIRES GM APPROVAL`.
2. **PF2e-native, not transliterated.** We rebuild to PF2e encounter/treasure/DC
   math and action economy rather than copying PF1e numbers. Solo PF1e bosses get
   PF2e support (lieutenants, hazards, reactions) so they survive 4-action focus
   fire.
3. **Official equivalents preferred.** When an official PF2e Monster Core / NPC
   Core / Bestiary creature fits, we link the compendium actor instead of
   rebuilding. Custom actors only when no good match exists.
4. **Subsystems → official PF2e subsystems.** Harrowing → Harrow reading;
   Blood Veil → PF2e disease; Cinderlands → Hexploration/Survival; court &
   alliance building → Influence; Korvosan standing → Reputation. See
   `../research/research_index.md` and the relevant chapter journals.
5. **Traceability.** Every decision cites the PF1e AP (page), a PF2e rule, a
   research source, or is labeled *design judgment*. Unknowns are
   `NEEDS GM REVIEW`, never invented.

## Source reference convention

Area journals cite the original as:
`AP: Curse of the Crimson Throne (2016 HC), Ch.N "<Chapter>", Area <code> — p.<PDF page>`
(PDF page == printed page for this edition; verified offset 0.)
