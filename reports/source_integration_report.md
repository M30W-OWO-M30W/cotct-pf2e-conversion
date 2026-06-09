# Source Integration Report (private-use layer)

How the original Adventure Path is made accessible **inside Foundry** for this
private, local table — as a **chapter-split PDF source layer** linked one-click
from the converted play layer. See `PRIVATE_USE_ONLY.md` for the boundary.

> Scope: Chapter 1 pilot (Old Fishery). The mechanism scales unchanged to Ch.2–6.

## Architecture (three linked layers)
- **Source layer** = the GM's own PDF, **split by chapter** (pypdf) into ~5–7 MB
  files (the full 50 MB / 482-page file lags in Foundry's PDF.js). Embedded as
  native Foundry **PDF journal pages**, GM-only.
- **Play layer** = the PF2e conversion (journals/actors/items/hazards/scenes) —
  original work; concise, runnable.
- **Interactive layer** = the Old Fishery scene with map-note pins → area pages →
  linked actors/hazards/treasure → 📖 chapter-PDF at the cited page.

## Status

| Item | Status |
|---|---|
| PDF found (GM-provided, owned) | **Yes** |
| PDF split into chapter files | **Yes** — 8 files (Intro/Ch.1–6/Appendices), 1.9–22 MB each, in `assets/private-source/chapters/` (**git-ignored**) |
| Chapter PDF embedded as a Foundry PDF page | **Yes (Ch.1)** — "Source — Ch.1: Edge of Anarchy (PDF · GM)"; Ch.2–6 split & link as converted |
| Per-area one-click source link | **Yes** — every area page's 📖 link → the Ch.1 chapter PDF at the cited printed page |
| Exact-page jump | via free **PDF Pager** module (set page offset −9 for the Ch.1 chapter PDF); else opens the chapter PDF + the page number |
| Navigation indexes | **Yes** — Indexes journal: Original Source · Area · NPC/Creature · Encounter · Treasure · Hazard (all links) |
| Source text reproduced into journals | **No** — the source is the embedded PDF; the repo contains **no verbatim AP text or art** (copyright). Converted pages carry original summaries + mechanics + the PDF link |
| Converted area pages | 20 (overview/scene/features + A1–A14 + NPC/treasure/conversion) |
| Pages linking to source | **20 / 20**; scene pins → area pages **14 / 14** |
| Broken links | **0** (validate.mjs: 108 links resolve) |
| GM-review flags | live PDF render check; scene pin/token positions (no map shipped) |

## Performance
Chapter PDFs are 1.9–7.5 MB (appendices 22 MB) vs the 50 MB monolith — each opens
responsively in Foundry's viewer. The full file is no longer embedded.

## Remaining GM-review items
- `NEEDS GM REVIEW` — confirm the chapter PDF renders in your Foundry v14.
- Optional: install **PDF Pager** for exact-page jumps (offset −9 on the Ch.1 PDF).
- Refresh install with Foundry closed: `bash scripts/install_to_foundry.sh`.
- Scene pin/token **positions** staged (no map shipped) — `NEEDS GM REVIEW`.
- Ch.2–6: run `scripts/split_pdf_by_chapter.py` (done) + convert each chapter
  (Phase 3) to extend the per-area links beyond Ch.1.
