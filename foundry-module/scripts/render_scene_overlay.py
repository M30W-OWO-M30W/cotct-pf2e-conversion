#!/usr/bin/env python3
"""Render a Racooze scene composite for keying and QA (run with python3.12 — needs Pillow).

Modes:
  python3.12 render_scene_overlay.py "Eel's End" out.png                # raw map + grid labels
  python3.12 render_scene_overlay.py "Eel's End" out.png --scene packs/scenes/_source/x.json
                                                                        # + pins/tokens overlay
  ... --crop 0,0,20,15      crop to a grid-square rect (x0,y0,x1,y1) before scaling
  ... --max 1500            output max dimension (default 1500)

Tiles resolve from the Foundry Data dir; hidden tiles are skipped. Coordinates in
the render are MAP-LOCAL grid squares (origin = top-left tile), matching the
gx/gy values used for keying. Scene-origin offset is applied automatically when
overlaying a built scene's pins/tokens."""
import json, os, sys

DATA = "/mnt/c/Users/maman/AppData/Local/FoundryVTT/Data/"
HERE = os.path.dirname(os.path.abspath(__file__))


def load_geo(name):
    geo = json.load(open(os.path.join(HERE, "racooze_scenes.json")))[name]
    if not geo.get("background"):
        fixes = json.load(open(os.path.join(HERE, "racooze_bg_fixes.json")))
        geo["background"] = fixes.get(name)
    return geo


def render(name, out, scene_json=None, crop=None, maxdim=1500, grid_labels=True):
    from PIL import Image, ImageDraw
    import math
    geo = load_geo(name)
    tiles = [t for t in geo["tiles"] if not t.get("hidden")]
    pad = geo.get("padding") or 0.25
    ox = math.ceil(geo["width"] * pad / 100) * 100
    oy = math.ceil(geo["height"] * pad / 100) * 100
    W, H = geo["width"], geo["height"]
    canvas = Image.new("RGB", (W, H), (15, 15, 22))
    if geo.get("background"):
        bsrc = os.path.join(DATA, geo["background"])
        if os.path.exists(bsrc):
            bim = Image.open(bsrc).convert("RGBA")
            if bim.size != (W, H):
                bim = bim.resize((W, H))
            canvas.paste(bim, (0, 0), bim)
        else:
            print(f"[render] missing background {geo['background']}")
    for t in sorted(tiles, key=lambda t: (t.get("sort", 0), t.get("elevation", 0))):
        src = os.path.join(DATA, t["texture"]["src"])
        if not os.path.exists(src):
            print(f"[render] missing tile {t['texture']['src']}"); continue
        im = Image.open(src).convert("RGBA")
        if im.size != (t["width"], t["height"]):
            im = im.resize((t["width"], t["height"]))
        canvas.paste(im, (t["x"] - ox, t["y"] - oy), im)
    d = ImageDraw.Draw(canvas)
    if grid_labels:
        for gx in range(0, W + 1, 100):
            d.line([(gx, 0), (gx, H)], fill=(255, 70, 70), width=2)
        for gy in range(0, H + 1, 100):
            d.line([(0, gy), (W, gy)], fill=(255, 70, 70), width=2)
        for gx in range(0, W, 200):
            for gy in range(0, H, 200):
                d.text((gx + 4, gy + 2), f"{gx//100},{gy//100}", fill=(255, 255, 0))
    if scene_json:
        sc = json.load(open(scene_json))
        for n in sc.get("notes", []):
            x, y = n["x"] - ox, n["y"] - oy
            d.ellipse([x - 24, y - 24, x + 24, y + 24], fill=(255, 215, 0), outline=(0, 0, 0), width=3)
            d.text((x - 18, y - 7), n["text"].split(".")[0], fill=(0, 0, 0))
        for t in sc.get("tokens", []):
            x, y = t["x"] - ox, t["y"] - oy
            w = t["width"] * 100
            col = (220, 40, 40) if t.get("disposition", -1) == -1 else (60, 160, 220)
            d.rectangle([x, y, x + w, y + w], outline=col, width=6)
            d.text((x + 4, y + w + 2), t["name"][:14], fill=(255, 255, 255))
    if crop:
        x0, y0, x1, y1 = [int(v) * 100 for v in crop.split(",")]
        canvas = canvas.crop((x0, y0, min(x1, W), min(y1, H)))
    canvas.thumbnail((maxdim, maxdim))
    canvas.save(out)
    print(f"[render] {name} -> {out} ({canvas.size[0]}x{canvas.size[1]}, map {W//100}x{H//100} squares)")


if __name__ == "__main__":
    args = sys.argv[1:]
    name, out = args[0], args[1]
    kw = {}
    if "--scene" in args: kw["scene_json"] = args[args.index("--scene") + 1]
    if "--crop" in args: kw["crop"] = args[args.index("--crop") + 1]
    if "--max" in args: kw["maxdim"] = int(args[args.index("--max") + 1])
    render(name, out, **kw)
