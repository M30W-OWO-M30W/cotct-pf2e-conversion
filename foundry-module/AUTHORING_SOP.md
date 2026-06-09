# Authoring SOP — CotCT PF2e conversion

How we build the module, so every chapter comes out consistent. Standing *design*
decisions live in `CONVERSION_NOTES.md`; this file is the *how-to-author* checklist.
Everything is generated deterministically by `scripts/build_pilot.py` (per-chapter
build scripts will follow the same shape) using the shared helpers in
`scripts/pf2e_build.py`.

## 1. Linking (read-from-compendium safe)
The GM reads the journal **straight from the compendium** (no Adventure import), so
intra-module references MUST be **Compendium UUIDs**, not bare world UUIDs (bare
`@UUID[Actor.x]` only resolves after an import — it renders broken in the compendium).
- Actors → `act()`  → `@UUID[Compendium.cotct-pf2e-conversion.cotct-actors.Actor.<id>]`
- Hazards → `haz()` → `…cotct-hazards.Actor.<id>`
- Items → `itm()`  → `…cotct-items.Item.<id>`
- Scenes → `scn()` → `…cotct-scenes.Scene.<id>`
- Same-entry page jumps → `pg(pageId, label)` → relative `@UUID[.<pageId>]`
- Official SRD content → `mc()` etc. → `@UUID[Compendium.pf2e.<pack>.<Type>.<id>]`
`npm run validate` resolves every one of these against the built packs (bare
`Actor./Item./Scene.` links are a regression — there should be 0).

## 2. DCs are always `@Check` enrichers
Never leave a plain "DC 15" in text. Use `chk("type:thievery|dc:15")`. DCs are
**re-judged to PF2e** (level-based / simple), never transliterated from PF1e. DCs
found inside verbatim source prose are converted by `dcfix()` at build. `validate`
warns on any raw `DC \d+` not wrapped in `@Check`.

## 3. Actor stat blocks: mechanics in items, everything else in notes
- **Action/ability items = pure mechanics.** No tactics, no GM flavor, no "he flees
  at half HP" in an action description.
- **Role, tactics, behavior, morale, GM context → `system.details.publicNotes`.**
- Do **not** create pseudo-"actions" for behavior (no "Surrender & Inform", "Cower",
  "Reluctant Leaper"). If it isn't a mechanic, it's a note.

## 4. Conditional passives = sheet TOGGLES, not baked numbers
Don't bake conditional damage into a Strike's damage rolls. Implement it as a rules
element so it shows as a toggle on the actor sheet. Canonical pattern (see
`pf2e_build.sneak_attack()`):
```
RollOption  {domain:"all", option:"target:condition:off-guard", toggleable:"totm",
             label:"PF2E.SpecificRule.TOTMToggle.OffGuard"}
DamageDice  {selector:"strike-damage", category:"precision", diceNumber:N, dieSize:"d6",
             predicate:["target:condition:off-guard"]}
```
Reuse this shape for any "extra X when <condition>" passive (precision, weakness
exploit, etc.): a `RollOption` toggle + a predicated `DamageDice`/`FlatModifier`.
`B.action(..., rules=[...])` carries arbitrary rules elements.

## 5. Read-aloud & source text (verbatim, from the GM's own file)
- The GM reads boxed text **verbatim**, so it's pulled from the GM's local AP markdown
  at build time (`SRC_MD`), never hardcoded into the repo.
  - Per-area read-aloud: `box("A#", fallback)` via the `RABOX` start-anchors (`verbatim()`).
  - Multi-paragraph narrative (Background, Haunted Fortunes, Introduction): `apspan(start, stop)`.
- Each extractor cleans the two-column OCR: re-flows paragraphs split mid-sentence,
  fixes drop-caps ("T he"→"The"), drops image/page markers & all-caps captions, and
  pulls fused sidebar **handouts** out of the narrative (`_HANDOUTS`) into their own
  read-aloud boxes.
- Always supply an **original paraphrase fallback** so the build still works where
  `AP.md` is absent (CI / another machine) — only the GM's machine renders verbatim.
- After adding a chapter, run `validate` and **review its Content warnings** (split
  paragraphs / raw DCs) and fix per-section; sidebars/handouts often need a new
  `_HANDOUTS` entry.

## 6. Journal structure
- **Introduction** is a detached, root-level entry (`folder=None`), like Kingmaker.
- One **fat journal per chapter** in the *Adventure* folder; page per keyed area.
- Page titles are plain: **`A#. Location`** — no encounter tags ("E3"), no
  parentheticals/subtitles.
- Section vocabulary (styled by `styles/cotct-journal.css`): `description` (read-aloud),
  `secret` (GM-only), `encounter` (+ `aside.right.token` + `header.split`), `skill`,
  `treasure`, `milestone head`, `subhead`, `conversion`, `p.source`.
- **Encounter titles use `<span class="enc-name">`, never `<h3>`** — headings leak
  into the page navigation; encounters must not appear there.
- Module ships **no maps/art/tokens** (copyright); journal-aside token images are
  hidden by CSS.

## 7. IDs
Named docs get stable literal `_id`s (the `A`/`JID`/`SCN`/`ADV`/`INTRO_JID` registry).
Folders/pages/notes/tokens come from `B._idgen(424242)`; GM-secret block ids from a
separate `_idgen(987654)` stream so they never perturb the main pool.

## 8. Build → validate → sync workflow
1. `python3 scripts/build_pilot.py` — regenerate `_source` JSON (deterministic).
2. `npm run validate` — link resolution (0 problems) + Content warnings (review).
3. `npm run build` — compile `_source` → LevelDB.
4. **Sync to the local install:** close Foundry, then `scripts/sync_to_foundry.sh`
   (or the desktop **"Sync CotCT to Foundry.bat"**). The compendium DB is locked while
   Foundry runs, so it must be **closed**; the script detects this and aborts cleanly.
5. Reopen Foundry → read from the **CotCT: Journals** compendium (no import needed).
The installed module is a hand-copy, so GitHub pushes don't reach it — the sync script
is what updates Foundry.

## 9. Copyright / repo
Repo is **private** (personal use). Verbatim Paizo text exists only because it's
injected locally from the GM's own file; do not hardcode AP prose into the repo, and
ship no maps/art. PF2e mechanics are ORC-open; AP creative content stays summaries +
page citations except where pulled locally for the GM's table.
