#!/usr/bin/env python3
"""Split the layout-extracted AP text into per-chapter working files.

Each output page is prefixed with a marker `[[PDF p.N]]` (PDF page index ==
printed page number for this hardcover, verified offset 0). Reusable &
deterministic: re-running reproduces identical output.

Input  : .work/text/full_layout.txt  (pdftotext -layout, form-feed delimited)
Output : .work/text/chapters/<slug>.txt
"""
from __future__ import annotations
import pathlib

BASE = pathlib.Path(__file__).resolve().parents[2]
SRC = BASE / ".work" / "text" / "full_layout.txt"
OUT = BASE / ".work" / "text" / "chapters"

# (slug, title, first_pdf_page, last_pdf_page)  inclusive, 1-indexed
CHAPTERS = [
    ("00-intro",       "Introduction",                  4,   9),
    ("01-edge-of-anarchy",       "Ch1: Edge of Anarchy",        10,  67),
    ("02-seven-days-to-the-grave","Ch2: Seven Days to the Grave",68, 131),
    ("03-escape-from-old-korvosa","Ch3: Escape from Old Korvosa",132,189),
    ("04-a-history-of-ashes",     "Ch4: A History of Ashes",    190, 255),
    ("05-skeletons-of-scarwall",  "Ch5: Skeletons of Scarwall", 256, 331),
    ("06-crown-of-fangs",         "Ch6: Crown of Fangs",        332, 391),
    ("07-appendices",             "Appendices",                 392, 482),
]


def main() -> None:
    text = SRC.read_text(encoding="utf-8", errors="replace")
    pages = text.split("\f")  # form-feed per page
    OUT.mkdir(parents=True, exist_ok=True)
    print(f"Loaded {len(pages)} pages from {SRC.name}")
    for slug, title, lo, hi in CHAPTERS:
        chunks = []
        for n in range(lo, hi + 1):
            idx = n - 1  # pages list is 0-indexed; page 1 -> idx 0
            if 0 <= idx < len(pages):
                chunks.append(f"[[PDF p.{n}]]\n{pages[idx].rstrip()}")
        out_path = OUT / f"{slug}.txt"
        out_path.write_text(f"# {title} (PDF pages {lo}-{hi})\n\n" + "\n\n".join(chunks) + "\n", encoding="utf-8")
        print(f"  wrote {out_path.name:34s} pages {lo:>3}-{hi:<3} ({hi-lo+1} pp, {out_path.stat().st_size//1024} KB)")


if __name__ == "__main__":
    main()
