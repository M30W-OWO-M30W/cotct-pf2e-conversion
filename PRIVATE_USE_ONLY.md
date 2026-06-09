# PRIVATE USE ONLY — do not redistribute

This conversion is a **private, local Foundry VTT module for a single GM's table.**
It is **not** for publication, sale, upload, or redistribution in any form.

## Why
The local module integrates the **full original Adventure Path** so the GM can run
it without leaving Foundry: the GM's **own legally-owned PDF** of *Curse of the
Crimson Throne* (2016 Anniversary Edition) is embedded as a native **Foundry PDF
journal page** ("Original Adventure — Full Text"), and **every converted area page
links to it** with a printed page number (📖 *Open the original text*). The GM reads
the complete book — every word, sidebar, stat block, and map — inside Foundry.

The PDF is **© Paizo Inc.** Embedding a PDF you **own** in your personal local
module is a private-use format-shift. Sharing this module — or the
`assets/private-source/` PDF — with anyone who does not own the AP would be
copyright infringement.

## Hard rules (enforced by `.gitignore`)
These live **only** in your local Foundry install and are **never** committed or
pushed to git:
- `foundry-module/assets/private-source/*.pdf` — the original PDF
- `.work/**` — intermediate text extraction (page-tagged) from the PDF

The git repo (even though private) contains only **original work**: the PF2e
**conversion** (mechanics, paraphrased summaries, page citations, links), the
**build scripts**, and docs. The committed "Original Adventure (PDF)" journal holds
**only a file-path pointer** (no copyrighted text); on a machine without the PDF it
shows a missing file until you drop your own copy into `assets/private-source/`.
**No verbatim AP text is reproduced anywhere in this repository** — the full text
is read from your embedded PDF.

## Exact-page jumps (optional)
Install the free **PDF Pager** module to make the per-area links jump to the exact
PDF page. Without it, the link opens the PDF and the page number tells you where to
scroll (printed page = PDF page, offset 0).

## If you ever share this
Don't. If you distribute the converted *mechanics* (the non-source-text layers),
strip the `source-journals` pack and the `private-source` PDF first, and note that
the recipient must own the original AP. Better: keep it to your table.

## Provenance
- Original: *Pathfinder Adventure Path: Curse of the Crimson Throne* © 2016 Paizo Inc.
- PF2e mechanics: ORC License (open).
- This module: private derivative for the owner's personal table.
