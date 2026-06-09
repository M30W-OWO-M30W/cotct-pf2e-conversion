# Source Integration Report (private-use layer)

How the original Adventure Path is made accessible **inside Foundry** for this
private, local table. See `PRIVATE_USE_ONLY.md` for the boundary.

> Scope: Chapter 1 pilot (Old Fishery). The mechanism scales unchanged to Ch.2–6.

## Status

| Item | Status |
|---|---|
| PDF found (GM-provided, owned) | **Yes** — `/mnt/c/Users/maman/Downloads/Curse of the Crimson Throne AP.pdf` |
| PDF copied into local module | **Yes** — `foundry-module/assets/private-source/curse-of-the-crimson-throne.pdf` (50 MB, **git-ignored**) |
| PDF journal created (native Foundry PDF page) | **Yes** — "Original Adventure — Full Text (GM · private)" (`cotct-journals`), GM-only |
| Page links available | **Yes (page-numbered)** — every converted area page has a 📖 *Open the original text* link + printed page; **exact-page jump** requires the free **PDF Pager** module (printed page = PDF page, offset 0) |
| Source text reproduced into journals | **No, by design** — the full text is read from the embedded PDF; the repo contains **no verbatim AP text** (copyright + your own earlier rule). Converted pages carry paraphrased summaries + mechanics + the PDF link |
| Converted area pages | 14 (A1–A14) + overview/scene/features/NPCs/treasure/conversion = **20 pages** |
| Converted pages linking to the source PDF | **20 / 20** (via the `SR()` source line on every page) |
| Scene notes linked to converted pages | **14 / 14** (Old Fishery pins → area pages) |
| Areas missing source access | **0** (all link to the PDF) |
| Areas missing PF2e conversion | **0** for the Old Fishery; rest of Ch.1 (All the World's Meat, Eel's End, Dead Warrens, street events) pending Phase 3 |
| Broken source links | **0** (validate.mjs: 68 links resolve, incl. the PDF-journal links) |
| Extraction warnings / OCR | **N/A** — no text extraction performed (PDF embedded directly); the PDF is text-based (pdftotext succeeded earlier with no OCR needed) |
| GM-review flags | Live PDF render check (below); scene pin/token positions (no map shipped) |

## How it works (the no-flip chain)
1. Open the **Old Fishery** scene → click a lettered map-note pin (e.g. **A13**).
2. Foundry opens the **"1. Edge of Anarchy"** journal at that area page (converted
   mechanics, paraphrased read-aloud, linked actors/treasure/hazards).
3. The page's 📖 **Open the original text** link opens the embedded **PDF** at the
   cited page — the complete official text, art, and map, **inside Foundry**.
4. With **PDF Pager** installed, that link lands on the exact page automatically.

## Why PDF-embed instead of a text dump
- The embedded PDF is the **complete, authoritative** text — every sidebar, stat
  block, and map at full fidelity, with **zero OCR/extraction error**.
- It keeps the repo **free of reproduced copyrighted prose** (your original rule;
  copyright safety) while still meeting *"never leave Foundry."*
- It's the GM's **own owned file** — a clean private-use format-shift.

## Remaining GM-review items
- **`NEEDS GM REVIEW` — live render check:** confirm the PDF page renders in your
  Foundry v14 (native PDF pages work; large 482-page PDFs load fine in PDF.js).
- **Optional:** install **PDF Pager** for exact-page jumps.
- **Refresh the install with Foundry closed:** run
  `bash scripts/install_to_foundry.sh` (Foundry locks pack files while running).
- Scene pin/token **positions** are staged (no map shipped) — `NEEDS GM REVIEW`.
