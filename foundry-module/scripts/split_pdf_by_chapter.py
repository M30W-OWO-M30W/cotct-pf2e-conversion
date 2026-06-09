#!/usr/bin/env python3
"""Split the GM's own AP PDF into per-chapter PDFs for fast loading in Foundry.

Purely mechanical page-range chunking of the owner's legally-owned file (pypdf) —
no content is altered or reproduced. Output goes to the git-ignored
assets/private-source/chapters/ so it never enters the repo (see
PRIVATE_USE_ONLY.md). A 482-page / 50 MB PDF is sluggish in Foundry's PDF.js;
per-chapter files load far faster.

Requires: pip install pypdf
Usage: python3 scripts/split_pdf_by_chapter.py [path-to-source.pdf]
"""
from __future__ import annotations
import sys, pathlib
from pypdf import PdfReader, PdfWriter

ROOT = pathlib.Path(__file__).resolve().parents[1]
DEFAULT_PDF = "/mnt/c/Users/maman/Downloads/Curse of the Crimson Throne AP.pdf"
SRC = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path(DEFAULT_PDF)
OUT = ROOT / "assets" / "private-source" / "chapters"

# (slug, first_printed_page, last_printed_page)  printed page == PDF page (offset 0)
CHAPTERS = [
    ("00-introduction",            4,   9),
    ("01-edge-of-anarchy",         10,  67),
    ("02-seven-days-to-the-grave", 68,  131),
    ("03-escape-from-old-korvosa", 132, 189),
    ("04-a-history-of-ashes",      190, 255),
    ("05-skeletons-of-scarwall",   256, 331),
    ("06-crown-of-fangs",          332, 391),
    ("07-appendices",              392, 482),
]

def main() -> None:
    if not SRC.exists():
        sys.exit(f"Source PDF not found: {SRC}")
    OUT.mkdir(parents=True, exist_ok=True)
    reader = PdfReader(str(SRC))
    print(f"Splitting {SRC.name} ({len(reader.pages)} pp) -> {OUT}/")
    for slug, lo, hi in CHAPTERS:
        w = PdfWriter()
        for i in range(lo - 1, hi):          # printed page N -> 0-indexed N-1
            w.add_page(reader.pages[i])
        try:
            w.compress_identical_objects(remove_identicals=True, remove_orphans=True)
        except Exception:
            pass
        dest = OUT / f"{slug}.pdf"
        with open(dest, "wb") as f:
            w.write(f)
        print(f"  {slug:30s} pp.{lo:>3}-{hi:<3}  ({hi-lo+1:>3} pp, {dest.stat().st_size/1e6:5.1f} MB)")
    print("done. (git-ignored; install_to_foundry.sh copies them into Foundry.)")

if __name__ == "__main__":
    main()
