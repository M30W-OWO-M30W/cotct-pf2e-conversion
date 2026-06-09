#!/usr/bin/env python3
"""Pilot items: story-critical + converted treasure (Old Fishery). Deterministic."""
from __future__ import annotations
import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / "packs" / "items" / "_source"
SRC.mkdir(parents=True, exist_ok=True)
PUB = {"license": "ORC", "remaster": True, "title": "CotCT PF2e Conversion (private)"}
ID = {"itm_brooch":"iNQaVcbkSM0VPXsa","itm_harrowdeck":"DPDen8gco6rznX9Y","itm_ledger":"I7HQNtjI9yPvQ4fA",
      "itm_garnet":"dK4hnpH7s67RYnNI","itm_coffer_shiver":"ymuRwMg6WfWIwkne","itm_gaedrendagger":"b04PLWVkmm3RM4nm"}

def equipment(idkey, name, level, price_gp, desc, traits=None, bulk=0.1, rarity="common", img="systems/pf2e/icons/default-icons/equipment.svg"):
    return {"_id": ID[idkey], "img": img, "name": name, "type": "equipment",
        "system": {"baseItem": None, "bulk": {"value": bulk}, "containerId": None,
            "description": {"value": desc}, "equipped": {"carryType": "worn", "handsHeld": 0, "invested": None},
            "hardness": 0, "hp": {"max": 0, "value": 0}, "level": {"value": level},
            "material": {"grade": None, "type": None}, "price": {"value": {"gp": price_gp}},
            "publication": PUB, "quantity": 1, "rules": [], "size": "med", "slug": None,
            "traits": {"rarity": rarity, "value": traits or []}, "usage": {"value": "worn"}}}

def write(slug, doc):
    (SRC / f"{slug}.json").write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"  items/{slug}.json  [{doc['type']}] {doc['name']}")

print("Building pilot items...")

# --- Queen Ileosa's Brooch (story item; the chapter's launching hook) ---
write("queen-ileosas-brooch", equipment("itm_brooch", "Queen Ileosa's Brooch", 0, 25,
    "<p><strong>Story item.</strong> A gold filigree brooch shaped like a house drake (or imp) with amethyst "
    "and emerald eyes and a broken clasp, looted from Gaedren's strongbox (A14). It belongs to Queen Ileosa. "
    "<strong>Returning it</strong> earns an audience with the queen and launches the rest of Chapter 1 (the "
    "queen's reward and the PCs' recruitment by the Korvosan Guard — see the Treasure report for the converted "
    "PF2e reward parcel).</p><p><em>Conversion note:</em> the PF1e brooch was valued at 2,000 gp; in PF2e its "
    "loot value is trivial (a minor art object) — its worth is entirely narrative. Do not let players sell it "
    "for level-breaking gold.</p>", traits=["art-object"], rarity="unique"))

# --- Zellara's Harrow Deck (story / Harrow subsystem anchor; CHG-0010) ---
write("zellaras-harrow-deck", equipment("itm_harrowdeck", "Zellara's Harrow Deck", 1, 0,
    "<p><strong>Story item — the Harrow subsystem anchor (see Conversion Notes CHG-0010).</strong> An heirloom "
    "harrow deck inhabited by the spirit of the murdered fortune-teller Zellara, recovered from her hatbox in "
    "A14 (beside her severed head). Through it, Zellara becomes a recurring guide, performing a <em>Harrowing</em> "
    "at the start of each chapter.</p>"
    "<hr /><p><strong>PF2e Harrowing (pilot stub).</strong> At the start of each chapter Zellara performs a "
    "reading (narrative foreshadowing). Each PC then gains a small pool of <strong>Harrow boons</strong> for that "
    "chapter — treat as extra Hero Points themed by harrow suit (Hammers→attack rerolls, Shields→Fortitude, "
    "Keys→Reflex, Stars→Will, Books→skill, Crowns→any), usable to reroll like a Hero Point. (Optional: use the "
    "official <em>Harrowing</em> ritual instead — GM decision G-Q6.) Full rules are built with the Conversion "
    "Guide journal; this pilot only needs the first reading.</p>"
    "<p><em>Foreshadowing:</em> base the first reading on Appendix 3; warn of coming unrest in the streets and "
    "that the PCs are fated to become heroes of Korvosa. Later (Ch.6) the deck becomes a Harrow Deck of Many "
    "Things. Uses the official <em>Harrow Deck</em> item flavor; the name 'Harrow' is retained post-Remaster.</p>",
    traits=["magical","divination"], rarity="unique", img="systems/pf2e/icons/equipment/other/harrow-deck.webp"))

# --- Gaedren's Coded Ledger (quest item / bounty) ---
write("gaedrens-coded-ledger", equipment("itm_ledger", "Gaedren's Coded Ledger", 0, 0,
    "<p><strong>Quest item.</strong> A moldy ledger atop the A14 strongbox recording Gaedren's crimes in a simple "
    "Varisian cipher. A PC who reads Varisian and succeeds at a <strong>Society check (DC 17)</strong> over a few "
    "hours deciphers it. Worth more to the Korvosan Guard than Gaedren's death: it closes dozens of cold cases.</p>"
    "<p><strong>Reward (converted):</strong> the Guard pays a bounty of <strong>15 gp</strong> for the ledger, or "
    "<strong>30 gp</strong> if the PCs also supply the cipher key (PF1e 250/500 gp, re-scaled to the level-1 "
    "treasure budget; see Treasure report). It also unlocks the 'Framed' background payoff.</p>",
    traits=["evidence"], rarity="unique"))

# --- Garnet amulet (Yargin) -> minor gem treasure ---
write("garnet-amulet", equipment("itm_garnet", "Garnet Amulet", 0, 8,
    "<p>A cheap garnet amulet worn by Yargin Balko. <em>Converted treasure:</em> a small gem worth <strong>8 gp</strong> "
    "(PF1e 100 gp, re-scaled). Sellable as coin.</p>", traits=["art-object"]))

# --- Darkwood coffer + shiver doses (A13) ---
write("coffer-of-shiver", equipment("itm_coffer_shiver", "Darkwood Coffer of Shiver", 1, 12,
    "<p>A latched darkwood coffer (worth ~10 gp as a fine container) from Gaedren's loot table (A13), holding "
    "20 doses of the drug <strong>shiver</strong> (distilled from dream-spider venom). Also on the table: 7 "
    "applications of <em>vermin repellent</em> (the alchemical paste that drives off the drain spiders — useful "
    "in A10/A11).</p>"
    "<p><strong>Conversion / Story:</strong> shiver is an addictive ingested drug — use PF2e drug/affliction "
    "rules. Destroying it (or turning it over to the Watch for a small reward) pays off a PC's 'Drug Addict' "
    "background hook. Do not treat the doses as sellable loot for good-aligned parties; the coffer + repellent "
    "are the tangible value (~12 gp). See Treasure report.</p>", traits=["alchemical"], rarity="uncommon"))

# --- Gaedren's +1 Dagger (boss loot) ---
write("plus-one-dagger", {"_id": ID["itm_gaedrendagger"], "img": "systems/pf2e/icons/equipment/weapons/dagger.webp",
    "name": "+1 Dagger (Gaedren's)", "type": "weapon",
    "system": {"baseItem": "dagger", "bonus": {"value": 0}, "bonusDamage": {"value": 0}, "bulk": {"value": 0.1},
        "category": "simple", "containerId": None,
        "damage": {"damageType": "piercing", "dice": 1, "die": "d4"},
        "description": {"value": "<p>Gaedren Lamm's prized magical dagger (PF1e '+1 dagger'). The boss's signature "
            "loot and an appropriate first permanent magic weapon for a level-1-2 party.</p><p><em>Converted:</em> a "
            "<strong>+1 weapon potency</strong> dagger (item level 2). His PF1e '+1 padded armor' similarly converts "
            "to a minor armor reward — see Treasure report.</p>"},
        "equipped": {"carryType": "worn", "handsHeld": 0, "invested": None}, "group": "knife", "hardness": 0,
        "hp": {"max": 0, "value": 0}, "level": {"value": 2}, "material": {"grade": None, "type": None},
        "price": {"value": {"gp": 35}}, "publication": PUB, "quantity": 1, "range": None,
        "reload": {"value": None}, "rules": [], "runes": {"potency": 1, "property": [], "striking": 0},
        "size": "med", "slug": None, "splashDamage": {"value": 0},
        "traits": {"rarity": "common", "value": ["agile", "finesse", "magical", "thrown-10", "versatile-s"]},
        "usage": {"value": "held-in-one-hand"}}})

print("Pilot items built.")
