#!/usr/bin/env python3
"""Generate graded copies of Racooze battlemap images into the DEPLOYED module's
maps/ folder (never the repo — derivative images of all-rights-reserved art stay
on the GM's machine, same firewall as the AP.md read-aloud and the wall data).

Grade: gentle S-curve contrast, slight desaturation, teal-shadow/warm-highlight
split tone, corner vignette — fixes the flat palette without moving a pixel, so
Racooze's walls stay valid. If Pillow is unavailable the originals are copied
unchanged so scene tile paths always resolve.

Run by sync_to_foundry.sh; safe to re-run (skips up-to-date outputs)."""
import os, shutil, sys

RACOOZE = "/mnt/c/Users/maman/AppData/Local/FoundryVTT/Data/modules/racoozes-curse-of-the-crimson-throne-battlemaps/assets/map-images"
DEST = "/mnt/c/Users/maman/AppData/Local/FoundryVTT/Data/modules/cotct-pf2e-conversion/maps"

# racooze-relative source -> our output name (extend per scene as maps get wired)
MAPS = {
    "old-fishery/old-fishery-first-floor.webp": "old-fishery-first-floor.webp",
    "old-fishery/old-fishery-lower-floor.webp": "old-fishery-lower-floor.webp",
}

def grade(im):
    from PIL import Image, ImageEnhance, ImageDraw
    im = im.convert("RGB")
    # gentle S-curve + desaturate
    im = ImageEnhance.Contrast(im).enhance(1.10)
    im = ImageEnhance.Color(im).enhance(0.90)
    # split tone via channel curves: teal-tinted shadows, faintly warm highlights
    def curve(ch, lift_lo, lift_hi):
        return [max(0, min(255, int(v + lift_lo * (1 - v / 255.0) + lift_hi * (v / 255.0)))) for v in range(256)]
    r, g, b = im.split()
    r = r.point(curve(r, -6, +5)); g = g.point(curve(g, +2, +2)); b = b.point(curve(b, +7, -4))
    from PIL import Image as I
    im = I.merge("RGB", (r, g, b))
    # corner vignette (multiply, 14% at corners)
    w, h = im.size
    vig = I.new("L", (w, h), 255)
    d = ImageDraw.Draw(vig)
    steps = 24
    for i in range(steps):
        a = 255 - int(36 * (i / steps) ** 2)
        inset = int(min(w, h) * 0.5 * (1 - i / steps))
        d.rectangle([inset, inset, w - inset, h - inset], fill=a)
    vig = vig.resize((w, h))
    black = I.new("RGB", (w, h), (8, 10, 12))
    return I.composite(im, black, vig)

def main():
    os.makedirs(DEST, exist_ok=True)
    if not os.path.isdir(RACOOZE):
        print("[grade_maps] Racooze module not installed — skipping."); return
    try:
        from PIL import Image
        have_pil = True
    except ImportError:
        have_pil = False
        print("[grade_maps] Pillow unavailable — copying originals ungraded.")
    n = 0
    for rel, out in MAPS.items():
        src, dst = os.path.join(RACOOZE, rel), os.path.join(DEST, out)
        if not os.path.exists(src):
            print(f"[grade_maps] missing source {rel} — skipped"); continue
        if os.path.exists(dst) and os.path.getmtime(dst) >= os.path.getmtime(src) \
                and os.path.getmtime(dst) >= os.path.getmtime(__file__):
            n += 1; continue
        if have_pil:
            from PIL import Image
            grade(Image.open(src)).save(dst, "WEBP", quality=90)
        else:
            shutil.copyfile(src, dst)
        n += 1
        print(f"[grade_maps] {out}")
    print(f"[grade_maps] {n}/{len(MAPS)} maps ready in {DEST}")

if __name__ == "__main__":
    main()
