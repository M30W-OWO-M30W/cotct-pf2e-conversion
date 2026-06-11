#!/usr/bin/env python3
"""Bake per-actor token art + portraits from the GM's own AP PDF extraction.

Inputs (all local-only, never committed — same firewall as AP.md):
  - /mnt/c/Users/maman/Downloads/cotct_art_extract/   (extract_art output PNGs)
  - scripts/token_art_index.json                      (committed: actor -> file/face data)

Outputs into the DEPLOYED module (not the repo):
  - Data/modules/cotct-pf2e-conversion/assets/tokens/<slug>.webp    (512px circular token, bronze ring)
  - Data/modules/cotct-pf2e-conversion/assets/art/portraits/<slug>.webp (portrait, max 800px)

The build (pf2e_build.write) points actor img/prototypeToken at these paths when
an index entry exists; missing files just render Foundry's default icon, so the
module still works on machines without the extraction. Run by sync_to_foundry.sh.

Requires Pillow (python3.12 user-site on this machine)."""
import json, os, re, sys

EXTRACT = "/mnt/c/Users/maman/Downloads/cotct_art_extract"
DEST = "/mnt/c/Users/maman/AppData/Local/FoundryVTT/Data/modules/cotct-pf2e-conversion/assets"
HERE = os.path.dirname(os.path.abspath(__file__))
INDEX = os.path.join(HERE, "token_art_index.json")

RING = (62, 45, 24)          # bronze
RING_W = 14                  # ring width at 512px
SIZE = 512

def slugify(name):
    s = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return s or "actor"

def bake_token(im, cx, cy):
    from PIL import Image, ImageDraw
    w, h = im.size
    # square crop around the face center; generous enough to read at table zoom
    side = int(min(w, h) * 0.62)
    side = max(side, 160)
    x0 = int(cx * w - side / 2); y0 = int(cy * h - side * 0.42)
    x0 = max(0, min(x0, w - side)); y0 = max(0, min(y0, h - side))
    crop = im.crop((x0, y0, x0 + side, y0 + side)).resize((SIZE, SIZE), Image.LANCZOS)
    out = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    mask = Image.new("L", (SIZE, SIZE), 0)
    d = ImageDraw.Draw(mask)
    d.ellipse([RING_W // 2, RING_W // 2, SIZE - RING_W // 2, SIZE - RING_W // 2], fill=255)
    out.paste(crop, (0, 0), mask)
    ring = ImageDraw.Draw(out)
    ring.ellipse([RING_W // 2, RING_W // 2, SIZE - RING_W // 2, SIZE - RING_W // 2],
                 outline=RING + (255,), width=RING_W)
    return out

def main():
    if not os.path.isdir(EXTRACT):
        print("[token_art] extraction folder missing — skipping (default icons stay)."); return
    if not os.path.exists(INDEX):
        print("[token_art] no token_art_index.json — skipping."); return
    try:
        from PIL import Image
    except ImportError:
        print("[token_art] Pillow unavailable — skipping."); return
    idx = json.load(open(INDEX, encoding="utf-8"))
    tok_dir = os.path.join(DEST, "tokens"); os.makedirs(tok_dir, exist_ok=True)
    por_dir = os.path.join(DEST, "art", "portraits"); os.makedirs(por_dir, exist_ok=True)
    made = skipped = 0
    for name, e in idx.items():
        src = os.path.join(EXTRACT, e["file"])
        if not os.path.exists(src):
            print(f"[token_art] missing {e['file']} for {name}"); skipped += 1; continue
        slug = slugify(name)
        tpath = os.path.join(tok_dir, slug + ".webp")
        ppath = os.path.join(por_dir, slug + ".webp")
        if os.path.exists(tpath) and os.path.getmtime(tpath) >= os.path.getmtime(src) \
                and os.path.getmtime(tpath) >= os.path.getmtime(INDEX):
            made += 1; continue
        im = Image.open(src).convert("RGB")
        bake_token(im, e.get("cx", 0.5), e.get("cy", 0.3)).save(tpath, "WEBP", quality=92)
        p = im.copy(); p.thumbnail((800, 800))
        p.save(ppath, "WEBP", quality=88)
        made += 1
    print(f"[token_art] {made} actors with art ({skipped} skipped) -> {DEST}")

if __name__ == "__main__":
    main()
