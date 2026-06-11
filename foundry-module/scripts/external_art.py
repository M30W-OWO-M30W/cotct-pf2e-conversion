#!/usr/bin/env python3
"""Bake token art for actors WITHOUT AP-PDF art, from free external sources:

  - "aon"       Archives of Nethys official Paizo creature/NPC art
                (Paizo Community Use Policy — free, non-commercial; downloaded
                 into the local cache, deployed-only, never committed)
  - "gameicons" game-icons.net glyphs (CC BY 3.0 — see README credit) rendered
                as white icons on theme-tinted discs; great for hazards.

Inputs:
  - scripts/external_art_index.json   (committed: actor -> source decision)
  - /mnt/c/Users/maman/Downloads/cotct_art_external/   (download cache +
    gameicons.zip with the full PNG set)

Outputs (deployed module only, same dirs as token_art.py):
  - assets/tokens/<slug>.webp, assets/art/portraits/<slug>.webp

Run by sync_to_foundry.sh after token_art.py. Safe to re-run (cached)."""
import io, json, os, re, sys, time, urllib.request, zipfile

CACHE = "/mnt/c/Users/maman/Downloads/cotct_art_external"
DEST = "/mnt/c/Users/maman/AppData/Local/FoundryVTT/Data/modules/cotct-pf2e-conversion/assets"
HERE = os.path.dirname(os.path.abspath(__file__))
INDEX = os.path.join(HERE, "external_art_index.json")
AON = "https://2e.aonprd.com"
SIZE = 512
RING = (62, 45, 24)
RING_W = 14

sys.path.insert(0, HERE)
from token_art import bake_token, bake_portrait, slugify   # reuse the AP-art bakes


def fetch(url, path):
    if os.path.exists(path) and os.path.getsize(path) > 0:
        return True
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "cotct-personal-module/1.0"})
        with urllib.request.urlopen(req, timeout=30) as r, open(path, "wb") as f:
            f.write(r.read())
        time.sleep(0.7)
        return True
    except Exception as e:
        print(f"[external_art] fetch failed {url}: {e}")
        if os.path.exists(path):
            os.remove(path)
        return False


def bake_disc(icon_png_bytes, tint):
    from PIL import Image, ImageDraw
    rgb = tuple(int(tint.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4))
    out = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    d = ImageDraw.Draw(out)
    d.ellipse([RING_W // 2, RING_W // 2, SIZE - RING_W // 2, SIZE - RING_W // 2], fill=rgb + (255,))
    # darker lower half for depth
    shade = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    ds = ImageDraw.Draw(shade)
    ds.ellipse([RING_W // 2, SIZE // 2, SIZE - RING_W // 2, SIZE + SIZE // 3], fill=(0, 0, 0, 60))
    mask = Image.new("L", (SIZE, SIZE), 0)
    ImageDraw.Draw(mask).ellipse([RING_W // 2, RING_W // 2, SIZE - RING_W // 2, SIZE - RING_W // 2], fill=255)
    out = Image.composite(Image.alpha_composite(out, shade), out, mask)
    icon = Image.open(io.BytesIO(icon_png_bytes)).convert("RGBA")
    # game-icons PNGs are black-on-transparent: recolor to white
    px = icon.load()
    for y in range(icon.height):
        for x in range(icon.width):
            r, g, b, a = px[x, y]
            px[x, y] = (245, 240, 230, a)
    isz = int(SIZE * 0.66)
    icon = icon.resize((isz, isz))
    out.alpha_composite(icon, ((SIZE - isz) // 2, (SIZE - isz) // 2))
    ImageDraw.Draw(out).ellipse([RING_W // 2, RING_W // 2, SIZE - RING_W // 2, SIZE - RING_W // 2],
                                outline=RING + (255,), width=RING_W)
    return out


def main():
    if not os.path.exists(INDEX):
        print("[external_art] no external_art_index.json — skipping."); return
    try:
        from PIL import Image
    except ImportError:
        print("[external_art] Pillow unavailable — skipping."); return
    os.makedirs(CACHE, exist_ok=True)
    tok_dir = os.path.join(DEST, "tokens"); os.makedirs(tok_dir, exist_ok=True)
    por_dir = os.path.join(DEST, "art", "portraits"); os.makedirs(por_dir, exist_ok=True)
    gi_zip = os.path.join(CACHE, "gameicons.zip")
    gi = zipfile.ZipFile(gi_zip) if os.path.exists(gi_zip) else None
    idx = json.load(open(INDEX, encoding="utf-8"))
    made = skipped = 0
    for name, e in idx.items():
        slug = slugify(name)
        tpath = os.path.join(tok_dir, slug + ".webp")
        ppath = os.path.join(por_dir, slug + ".webp")
        if os.path.exists(tpath) and os.path.getmtime(tpath) >= os.path.getmtime(INDEX):
            made += 1; continue
        if e["source"] == "aon" and e.get("aonImage"):
            cpath = os.path.join(CACHE, e["aonImage"].split("/")[-1])
            if not fetch(AON + e["aonImage"], cpath):
                skipped += 1; continue
            im = Image.open(cpath)
            bake_token(im, e.get("cx", 0.5), e.get("cy", 0.3), e.get("zoom", 1.0)).save(tpath, "WEBP", quality=92)
            bake_portrait(im).save(ppath, "WEBP", quality=88)
            made += 1
        elif e["source"] == "gameicons" and e.get("icon") and gi:
            member = f"icons/000000/transparent/1x1/{e['icon']}.png"
            try:
                data = gi.read(member)
            except KeyError:
                print(f"[external_art] icon missing in zip: {e['icon']} ({name})"); skipped += 1; continue
            disc = bake_disc(data, e.get("tint") or "#555c66")
            disc.save(tpath, "WEBP", quality=92)
            disc.resize((400, 400)).save(ppath, "WEBP", quality=88)
            made += 1
        else:
            skipped += 1
    print(f"[external_art] {made} baked, {skipped} skipped -> {DEST}")


if __name__ == "__main__":
    main()
