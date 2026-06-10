#!/usr/bin/env python3
"""Emit the Olliebird community docs that do NOT replace one of ours in place
(community_index.json entries without `replacedBy`) into the module packs,
keeping their original 16-char _ids so cmon() links are stable.

Chapter folder assignment: word-boundary greps of research/olliebird/ch*.txt,
hand-curated for the ambiguous ones (ledger below). Runs after the chapter
builders in sync_to_foundry.sh; order doesn't matter for pack sources."""
import json, pathlib, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import pf2e_build as B

# name -> chapter key; everything else falls back to the appendix folders.
# Curated: Piglet = Blood Pig stakes animal (ch3); Pudgyknuckles = named imp of
# the Old Korvosa imp war (ch3); Elite Red Mantis Assassin = RMA cell leader
# hunting Vencarlo (ch3); Wolverine = Cinderlands wildlife (ch4); Large Water
# Elemental = Vivified Labyrinth pools (ch3); Fiendish Water Elemental =
# Scarwall lake (ch5); war paints = Shoanti trial gear (ch4 has no item folder,
# so appendix); Everdawn Pool = campaign artifact (ch6 vault).
CHAPTER = {
    # npcs
    "Beggar": "ch1", "Bloo": "ch1", "Carrion Golem": "ch1", "Danse Macabre": "ch5",
    "Dero Stalker": "ch1", "Dero Strangler": "ch1", "Dream Spider": "ch1",
    "Giant Spider": "ch1", "Gobblegut": "ch1", "House Drake": "ch1",
    "Human Zombie": "ch1", "Necrophidius": "ch1", "Otyugh": "ch1",
    "Raktavarna Rakshasa": "ch1", "Reefclaw": "ch1",
    "Dire Rat": "ch2", "Human Skeleton": "ch2", "Juju Zombie": "ch2",
    "Leukodaemon": "ch2", "Rat Swarm": "ch2", "Ruan Mirukova": "ch2",
    "Skinshear": "ch2", "Vampire Spawn": "ch2", "Wererat": "ch2",
    "Avidexu": "ch3", "Blood Cobra": "ch3", "Elite Red Mantis Assassin": "ch3",
    "Emperor Cobra": "ch3", "Large Water Elemental": "ch3", "Marble Elephant": "ch3",
    "Piglet": "ch3", "Pudgyknuckles": "ch3",
    "Bulette": "ch4", "Catoblepas": "ch4", "Mogmora": "ch4", "Neverfar": "ch4",
    "Wolverine": "ch4",
    "Animated Taxidermic Wyvern": "ch5", "Anizora": "ch5", "Barbed Devil": "ch5",
    "Baykok": "ch5", "Bone Devil": "ch5", "Corpse Lotus": "ch5",
    "Festering Spirit": "ch5", "Fiendish Water Elemental": "ch5", "Geist": "ch5",
    "Greater Shadow": "ch5", "Gug": "ch5", "Imp": "ch5", "Iron Golem": "ch5",
    "Knurlott": "ch5", "Nessian Hell Hound": "ch5", "Nightmare": "ch5",
    "Polong": "ch5", "Skeleton Infantry": "ch5", "Specter": "ch5",
    "Tenebrous Worm": "ch5", "Wraith": "ch5",
    "Elite Erinys": "ch6", "Erinys": "ch6", "Shining Child": "ch6",
    "The Yallops": "ch6", "Zarmangarof": "ch6",
    # hazards
    "Lambs in the Fishery": "ch1", "Shrieker": "ch2", "Corrupted Pool": "ch3",
    "Yellow Mold": "ch3", "Green Slime": "ch5", "Obsession of Battle": "ch5",
    "Obsession of Servitude": "ch5", "Statue of Kazavon": "ch5",
}

NPC_FLD = {"ch1": "rBcjiaGq99bkJyYK", "ch2": "ch2CreaturesFld1", "ch3": "ch3CreaturesFld1",
           "ch4": "ch4CreaturesFld1", "ch5": "ch5CreaturesFld1", "ch6": "ch6CreaturesFld1",
           "app": "appCreaturesFld1"}
HAZ_FLD = {"ch1": "hf850cPYquAhv4Nz", "ch2": "ch2HazardsFld001", "ch3": "ch3HazardsFld001",
           "ch4": "ch4HazardsFld001", "ch5": "ch5HazardsFld001", "ch6": "ch6HazardsFld001",
           "app": "appHazardsFld001"}
ITEM_FLD = {"artifact": "campaignArtifct1", "app": "appItemFolder001"}
ITEM_OVERRIDE = {"Everdawn Pool": "artifact"}

def main():
    n = 0
    for key, meta in sorted(B.COMMUNITY.items()):
        if meta.get("replacedBy"):
            continue
        doc = B._json.loads((B.ROOT / "community" / meta["file"]).read_text(encoding="utf-8"))
        doc["ownership"] = {"default": 0}
        doc["_stats"] = dict(B.STATS)
        doc["sort"] = 0
        kind = meta["kind"]
        if kind == "item":
            pack = "items"
            doc["folder"] = ITEM_FLD[ITEM_OVERRIDE.get(doc["name"], "app")]
            B.write(pack, f"community-{meta['file'].split('/')[1][:-5]}", doc)
        else:
            pack = "actors" if kind == "npc" else "hazards"
            ch = CHAPTER.get(doc["name"], "app")
            doc["folder"] = (NPC_FLD if kind == "npc" else HAZ_FLD)[ch]
            # consistent token presentation with the rest of the module
            if kind == "npc":
                size = ((doc["system"].get("traits", {}).get("size") or {}).get("value")) or "med"
                doc["prototypeToken"] = B.prototoken(doc["name"], size)
            else:
                hp = ((doc["system"].get("attributes", {}).get("hp") or {}).get("max")) or 0
                doc["prototypeToken"] = B.prototoken(doc["name"], "med", has_hp=bool(hp))
            B.write(pack, f"community-{meta['file'].split('/')[1][:-5]}", doc, embed_items=True)
        n += 1
    print(f"[build_community] emitted {n} community-only docs")

if __name__ == "__main__":
    main()
