#!/usr/bin/env python3
"""One-time importer: materialize the Olliebird community compendium exports
(NeDB .db modules shared on the conversion Reddit thread) into
foundry-module/community/ as individual JSON docs + scripts/community_index.json.

Usage: python3 scripts/import_community.py <actors.db> <items.db>

The build then uses these docs as the AUTHORITATIVE statblocks (GM directive
2026-06-10): pf2e_build.write() swaps any same-named (alias-aware) doc we build
for the community version in place (keeping our _id/folder so journal links
survive), and build_community.py emits the community-only docs."""
import json, re, sys, unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "community"

def norm(n):
    n = unicodedata.normalize("NFKD", n).encode("ascii", "ignore").decode()
    n = re.sub(r"[^a-z0-9 ]", "", n.lower())
    return re.sub(r"\s+", " ", n).strip()

def slug(n):
    s = re.sub(r"[^a-z0-9]+", "-", n.lower()).strip("-")
    return s or "doc"

def main(actors_db, items_db):
    docs = []
    for f, default_kind in ((actors_db, None), (items_db, "item")):
        for line in Path(f).read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            d = json.loads(line)
            kind = default_kind or ("hazard" if d["type"] == "hazard" else "npc")
            docs.append((kind, d))

    # the export contains one exact-duplicate pair (Greater Shadow) — keep first
    seen, index = set(), {}
    for kind, d in docs:
        key = (kind, norm(d["name"]))
        if key in seen:
            print(f"  [dup skipped] {kind}: {d['name']} ({d['_id']})")
            continue
        seen.add(key)
        sub = OUT / {"npc": "actors", "hazard": "hazards", "item": "items"}[kind]
        sub.mkdir(parents=True, exist_ok=True)
        fn = f"{slug(d['name'])}.json"
        (sub / fn).write_text(json.dumps(d, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        lvl = ((d.get("system", {}).get("details", {}) or {}).get("level") or {}).get("value")
        index[f"{kind}:{norm(d['name'])}"] = {
            "kind": kind, "name": d["name"], "id": d["_id"], "level": lvl,
            "file": f"{sub.name}/{fn}", "itemType": d["type"],
        }
    (ROOT / "scripts" / "community_index.json").write_text(
        json.dumps(index, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    print(f"materialized {len(index)} community docs -> {OUT}")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
