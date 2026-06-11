#!/usr/bin/env python3
"""Master campaign Adventure: bundles EVERY built document (folders, journals,
actors, hazards, items, scenes, rolltables, macros) into one importable
Adventure doc, so a single import gives a world where every prepared scene's
tokens resolve (token actorIds bind to world actors the import creates).

Runs LAST in sync_to_foundry.sh — it reads the other builders' _source output.
The Ch.1 pilot adventure remains for chapter-sized imports."""
import copy, json, pathlib, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import pf2e_build as B

ADV_ID = "cotctCampaign001"


def strip(doc):
    d = copy.deepcopy(doc)
    d.pop("_key", None)
    for coll in ("items", "pages", "notes", "tokens", "walls", "tiles", "lights", "results"):
        for x in d.get(coll, []) or []:
            if isinstance(x, dict):
                x.pop("_key", None)
    return d


def load_pack(pack):
    docs, folders = [], []
    src = B.PACKS / pack / "_source"
    if not src.is_dir():
        return docs, folders
    for p in sorted(src.glob("*.json")):
        d = json.loads(p.read_text(encoding="utf-8"))
        (folders if p.name.startswith("_folder_") else docs).append(d)
    return docs, folders


def main():
    journals, jf = load_pack("journals")
    actors, af = load_pack("actors")
    hazards, hf = load_pack("hazards")
    items, itf = load_pack("items")
    scenes, sf = load_pack("scenes")
    tables, tf = load_pack("rolltables")
    macros, mf = load_pack("macros")

    folders = {}
    for f in jf + af + hf + itf + sf + tf + mf:
        folders.setdefault(f["_id"], f)

    all_actors = actors + hazards
    # orphan-token guard across EVERY scene: a token whose actorId is not bundled
    # imports broken ("references an actor which no longer exists")
    actor_ids = {a["_id"] for a in all_actors}
    bad = []
    for sc in scenes:
        for t in sc.get("tokens", []):
            if t.get("actorId") not in actor_ids:
                bad.append(f"{sc['name']}: {t['name']} -> {t.get('actorId')}")
    if bad:
        print("  [WARN] orphaned scene tokens (not in campaign bundle):")
        for b in bad:
            print("     ", b)

    adv = B.adventure(
        ADV_ID,
        "Curse of the Crimson Throne — Complete Campaign",
        "modules/cotct-pf2e-conversion/assets/art/cover.webp",
        "<p>The full six-chapter campaign plus appendices: every journal, actor, "
        "hazard, item, rolltable, macro, and prepared scene in one import. "
        "Re-import after module updates to refresh (accept the overwrite prompt).</p>",
        [strip(f) for f in folders.values()],
        [strip(j) for j in journals],
        [strip(s) for s in scenes],
        [strip(a) for a in all_actors],
        [strip(i) for i in items],
        tables=[strip(t) for t in tables],
        macros=[strip(m) for m in macros],
    )
    B.write("adventure", "cotct-complete-campaign", adv)
    print(f"[build_adventure] campaign bundle: {len(folders)} folders, {len(journals)} journals, "
          f"{len(all_actors)} actors, {len(items)} items, {len(scenes)} scenes, "
          f"{len(tables)} tables, {len(macros)} macros"
          + (f" — {len(bad)} ORPHANED TOKENS" if bad else " — all scene tokens resolve"))


if __name__ == "__main__":
    main()
