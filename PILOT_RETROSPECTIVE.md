# Pilot Retrospective — Old Fishery (Ch.1)

_After Phase 2, evaluate the conversion method before scaling to the full AP._

## What the pilot proved

A complete, **Foundry-importable** vertical slice of the opening dungeon:
21 documents / 30 journal pages, **0 validation problems**, all intra-module UUID
links resolve, and `npm run build` compiles the JSON `_source` to Foundry LevelDB
cleanly. The pf2e **v7 schema is confirmed correct** (verified against real system
sources, then round-tripped through the compiler).

The methodology — *extract intent → design to PF2e math (not PF1e numbers) →
serialize deterministically → validate → document every change* — works end to end
and produced GM-usable output (run sheet, area pages, balance/treasure/DC reports,
conversion notes), not just notes.

## What worked (keep)

1. **Deterministic Python build scripts** instead of hand-edited JSON. Shared
   helpers (`npc()`, `strike()`, `hazard()`, `page()`) guarantee schema
   consistency, fixed-seed IDs keep links stable across rebuilds, and re-running
   reproduces byte-identical files. This is the single biggest reliability win and
   scales directly to later chapters.
2. **Reference official actors when a clean match exists** (Crocodile→Gobblegut,
   Guard Dog→Bloo) — less JSON, canonical stats, rename-the-token in the journal.
3. **Reports as the design spec, journals as the run sheet.** Encoding the PF2e
   math/DC/treasure decisions in the four reports first, then linking them from
   concise area pages, kept the journals usable at the table and avoided
   duplicating big tables.
4. **`validate.mjs` as a gate.** Catching broken UUIDs / dup IDs / bad JSON before
   the LevelDB build is essential at scale.
5. **Design-intent fixes baked in, documented, GM-flagged** (the "Lamm is a Lamb"
   Severe rebuild; orphans as non-combatants) — exactly the "PF2e-native, not
   transliterated" goal, with every change traceable in the change log.

## Adjustments for Phase 3 (scaling)

1. **Promote the build helpers to a shared module.** Move `npc/strike/action/
   hazard/item/journal` helpers into `scripts/pf2e_build.py` and have per-chapter
   scripts import it. (Pilot duplicated them across `build_pilot*.py`.)
2. **Central ID registry file.** Generate and commit `scripts/ids.json` (one stable
   id per named document) instead of inlining the seed/pool per script — prevents
   any cross-chapter `_id` collision.
3. **Resolve official-actor IDs in bulk up front.** A small `gh`/cached lookup of
   Monster Core / NPC Core IDs for each chapter's referenced creatures, stored in
   a `monster_refs.json`, so journals link them without per-build API calls.
4. **Build the recurring subsystems next** (before deep chapter work): Harrow
   (CHG-0010), Korvosa city tiers + Reputation (CHG-0012/13), campaign-trait
   backgrounds (CHG-0021). They appear in every chapter; the pilot only stubbed
   Harrow.
5. **Use a workflow for fan-out** on big chapters (parallel area-page drafting /
   actor stat design), then serialize through the shared helpers — the pilot was
   small enough to author inline, but Scarwall (137 areas) and Castle Korvosa
   (~95 rooms) want parallel drafting.
6. **Scene records:** keep them as planning notes (done) until/unless the GM
   supplies maps; don't author Scene docs with invented geometry.

## Effort / cost signal

The pilot (one ~14-area dungeon) is a small fraction of the AP (~237 encounters,
~225 NPCs total). Scarwall and the finale will each dwarf it. Recommend converting
**one chapter per pass**, building shared subsystems first, and reusing recurring
NPC actors — and leaning on workflows for the large chapters.

## Verdict

**Methodology validated — proceed to Phase 3.** No structural changes needed;
the adjustments above are optimizations, not corrections.

## Outstanding GM decisions (do not block Phase 3, but resolve early)
- **Pilot:** confirm the boss as **Severe @ level 1** vs running it at level 2 (Moderate). *(default: as written)*
- **G-Q1** level cap 1→17 vs extend to 20 · **G-Q2** which Olliebird artifact you hold · **G-Q3** telegraph vs mystery (Blackjack/Arkona) · **G-Q4** plague structure · **G-Q5** OK to depend on Racooze's battlemaps · **G-Q6** Harrow reroll style. (See `research/research_index.md` §H.)
