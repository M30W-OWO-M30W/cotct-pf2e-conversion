#!/usr/bin/env python3
"""Deterministically build the Phase-2 pilot Foundry JSON (Old Fishery / Ch.1).

Emits pf2e v7 `_source` documents (one file per doc) into
foundry-module/packs/<pack>/_source/. Re-running reproduces identical files.

Schema verified against real pf2e v7 sources in .work/schema_ref/
(npc_barkeep.json, hazard_spear.json, hazard_pit.json).

Design rationale (encounter math, DCs, treasure) is documented in
reports/encounter_balance_report.md, npc_monster_conversion_report.md,
treasure_report.md, dc_skill_report.md — this script is the serialization layer.

IDs come from the fixed registry (seed 20260609) so journal<->actor UUID links
stay stable across rebuilds.
"""
from __future__ import annotations
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]            # foundry-module/
PACKS = ROOT / "packs"
MOD = "cotct-pf2e-conversion"

# ---- ID registry (seed 20260609) ----
ID = {
 "act_gaedren":"RKfT6vJ5guinSBjo","act_yargin":"7uhbgkK2IOZOlJb3","act_hookshanks":"qH96VshE6CZqfajv",
 "act_giggles":"mHUhxeaalWkTU1h4","act_drainspider":"1M94tm3wnSRGcTG5","act_jigsawshark":"lsdWSvGJ81hDy4it",
 "act_orphan":"UQr3ApF78GW7eghw","haz_boardwalk":"6y55S5DpXqnF40WL","haz_rottendeck":"xMhIQZS6GokTsulZ",
}
# deterministic embedded-item id pool (stable across runs)
_POOL = ["imb6bFpeZx6SDdnE","jUAfT5lYds26rvLH","4f18kaZPNF2BiCyz","VIGFiF2D6AuHE8fb","TUH3tMGetdqEeZz9",
 "8hHsiHErihsqOllX","RTiU83EnMqrIW50A","6PuxBmLScqxay0Hq","pfnOQH3FMchkduas","YHHOLB9Lpw1BQBLA",
 "JToxyXFb1usrIxgL","xLikseaXiETYHEHG","08S4EaoF9tCUATLQ","lWBt6PwypcqRTPdV","4IvzUl3CcJJnNgqA",
 "D0Fmh162eHV2dxkE","6C2t30fwYRHENDUg","Kqvy5hroZYWXGZGi","PACmCmPuKsvoLtCM","4YkgOS2dCobRjRQ4",
 "ozpRFG53M9PA6au8","BugQKnKYSuRH4QD4","TolzUHbHJo2GV8Gi","OLx7GHLZEudI8mUc","NtOmInkK92Hhb3Xy",
 "MSEwelGcRqYipKWR","PIsDQTNnDUhhiPJ4","8eYZrtP4g9eLOuIQ","MTcGAMb0LMrC41hw","b8Rmu1ajRBPBjlgG",
 "GaDSPHFyVSjyutRT","Pl0jGy4iH3WIm06t","f16b6MRu4nQHYo4R","acshVw94XQa9eUIt","pHMoFU5LMyCDZ8dm",
 "LftCcvU2yoJrajMM","RM0j3UdCT9bBG5K3","GxMceD3vWfpePuH8","uiQyn4dpCBGYQRxY","H5H1wjkr2bnWFaun"]
_pool_i = 0
def eid() -> str:
    global _pool_i
    v = _POOL[_pool_i]; _pool_i += 1; return v

PUB = {"license":"ORC","remaster":True,"title":"CotCT PF2e Conversion (private)"}
MELEE_IMG = "systems/pf2e/icons/default-icons/melee.svg"

# ---------- item builders ----------
def strike(name, bonus, dmg, dmgtype, traits, extra_dmg=None, img=MELEE_IMG):
    rolls = {"0": {"damage": dmg, "damageType": dmgtype}}
    if extra_dmg:
        for i, (d, t) in enumerate(extra_dmg, start=1):
            rolls[str(i)] = {"damage": d, "damageType": t}
    return {"_id": eid(), "img": img, "name": name, "sort": 0,
            "system": {"attack": {"value": ""}, "attackEffects": {"value": []},
                       "bonus": {"value": bonus}, "damageRolls": rolls,
                       "description": {"value": ""}, "publication": PUB,
                       "rules": [], "slug": None, "traits": {"rarity": "common", "value": traits}},
            "type": "melee"}

GLYPH = {None:"systems/pf2e/icons/default-icons/action.svg",
         "1":"systems/pf2e/icons/actions/OneAction.webp","2":"systems/pf2e/icons/actions/TwoActions.webp",
         "3":"systems/pf2e/icons/actions/ThreeActions.webp","reaction":"systems/pf2e/icons/actions/Reaction.webp",
         "free":"systems/pf2e/icons/actions/FreeAction.webp","passive":"systems/pf2e/icons/actions/Passive.webp"}
def action(name, glyph, desc, traits=None, category="offensive"):
    if glyph == "passive":
        atype, acts = "passive", None
    elif glyph == "reaction":
        atype, acts = "reaction", None
    elif glyph == "free":
        atype, acts = "free", None
    else:
        atype, acts = "action", (int(glyph) if glyph else None)
    return {"_id": eid(), "img": GLYPH.get(glyph, GLYPH[None]), "name": name, "sort": 0,
            "system": {"actionType": {"value": atype}, "actions": {"value": acts},
                       "category": category, "description": {"value": desc}, "publication": PUB,
                       "rules": [], "slug": None, "traits": {"rarity": "common", "value": traits or []}},
            "type": "action"}

def lore(name, mod):
    return {"_id": eid(), "img": "systems/pf2e/icons/default-icons/lore.svg", "name": name, "sort": 0,
            "system": {"description": {"value": ""}, "mod": {"value": mod}, "proficient": {"value": 0},
                       "publication": PUB, "rules": [], "slug": None}, "type": "lore"}

# ---------- actor builder ----------
def npc(idkey, name, level, ac, hp, fort, ref, will, per, abilities, speed, skills,
        traits, languages, items, notes, senses=None, other_speeds=None, immunities=None,
        weaknesses=None, resistances=None, size="med", blurb=""):
    sys = {
        "abilities": {k: {"mod": v} for k, v in abilities.items()},
        "attributes": {
            "ac": {"details": "", "value": ac},
            "allSaves": {"value": ""},
            "hp": {"details": "", "max": hp, "temp": 0, "value": hp},
            "speed": {"otherSpeeds": other_speeds or [], "value": speed},
        },
        "details": {"blurb": blurb, "languages": {"details": "", "value": languages},
                    "level": {"value": level}, "privateNotes": "",
                    "publicNotes": notes, "publication": PUB},
        "initiative": {"statistic": "perception"},
        "perception": {"details": "", "mod": per, "senses": senses or []},
        "resources": {},
        "saves": {"fortitude": {"saveDetail": "", "value": fort},
                  "reflex": {"saveDetail": "", "value": ref},
                  "will": {"saveDetail": "", "value": will}},
        "skills": {k: {"base": v} for k, v in skills.items()},
        "traits": {"rarity": "common", "size": {"value": size}, "value": traits},
    }
    if immunities: sys["attributes"]["immunities"] = immunities
    if weaknesses: sys["attributes"]["weaknesses"] = weaknesses
    if resistances: sys["attributes"]["resistances"] = resistances
    return {"_id": ID[idkey], "img": "systems/pf2e/icons/default-icons/npc.svg",
            "name": name, "type": "npc", "items": items, "system": sys}

# ---------- hazard builder ----------
def hazard(idkey, name, level, stealth, stealth_note, disable, desc, items,
           ac=None, hardness=0, hp=0, fort=0, ref=0, will=0, traits=None,
           reset="", routine="", complex_=False):
    attr = {"emitsSound": "encounter", "hardness": hardness, "stealth": {"details": stealth_note, "value": stealth}}
    if hp:
        attr["hasHealth"] = True
        attr["hp"] = {"details": "", "max": hp, "temp": 0, "tempmax": 0, "value": hp}
        attr["immunities"] = [{"type": "critical-hits"}, {"type": "precision"}]
    if ac is not None:
        attr["ac"] = {"value": ac}
    return {"_id": ID[idkey], "img": "systems/pf2e/icons/default-icons/hazard.svg",
            "name": name, "type": "hazard", "items": items,
            "system": {"attributes": attr, "creatureType": "",
                       "details": {"description": desc, "disable": disable, "isComplex": complex_,
                                   "level": {"value": level}, "publication": PUB, "reset": reset, "routine": routine},
                       "saves": {"fortitude": {"saveDetail": "", "value": fort},
                                 "reflex": {"saveDetail": "", "value": ref},
                                 "will": {"saveDetail": "", "value": will}},
                       "statusEffects": [], "traits": {"rarity": "common", "size": {"value": "med"},
                                                       "value": traits or ["environmental"]}}}

def write(pack, slug, doc):
    d = PACKS / pack / "_source"
    d.mkdir(parents=True, exist_ok=True)
    (d / f"{slug}.json").write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"  actors/{pack}/{slug}.json  [{doc['type']}] {doc['name']}")

# =====================================================================
# ACTORS
# =====================================================================
print("Building pilot actors + hazards...")

# --- Gaedren Lamm (L2 frail skirmisher/sniper; Gobblegut is the real threat) ---
gaedren_items = [
 strike("Fine Dagger", 9, "1d4+1", "piercing", ["agile","finesse","versatile-s"],
        extra_dmg=[("1d6","precision")]),
 strike("Hand Crossbow", 9, "1d6", "piercing", ["range-increment-60","reload-1"],
        extra_dmg=[("1d6","precision")]),
 action("Sneak Attack", "passive",
        "<p>Gaedren deals an extra 1d6 precision damage to any creature that is off-guard to him "
        "(already included in his Strikes' damage when applicable).</p>", ["rogue"]),
 action("Limping Gait", "passive",
        "<p>An old leg wound has crippled Gaedren; his Speed is only 15 feet and he can't take the "
        "Stride-heavy tactics a younger rogue would. He compensates with ranged sniping from across "
        "the gator pool.</p>"),
 action("Nimble Dodge", "reaction",
        "<p><strong>Trigger</strong> A creature targets Gaedren with an attack and he can see the attacker.</p>"
        "<hr /><p><strong>Effect</strong> Gaedren gains a +2 circumstance bonus to AC against the triggering attack.</p>",
        ["mental"], category="defensive"),
 action("Spur the Beast", "1",
        "<p>Gaedren makes a Hand Crossbow Strike against Gobblegut (his pet crocodile). If it hits, the "
        "enraged crocodile gains a +2 status bonus to attack and damage rolls and must spend its next turn "
        "Striking the nearest creature other than Gaedren (Gaedren is immune to this forced target). This is "
        "his signature opening: he turns his own pet into a weapon, then snipes from cover.</p>", ["concentrate"]),
 lore("Underworld Lore", 8),
]
write("actors", "gaedren-lamm", npc("act_gaedren","Gaedren Lamm",2, 17, 30, 3, 9, 8, 8,
    {"str":-1,"dex":4,"con":0,"int":3,"wis":2,"cha":3}, 15,
    {"deception":10,"stealth":9,"thievery":9,"intimidation":8,"society":6,"acrobatics":9},
    ["humanoid","human"], ["Common","Varisian"], gaedren_items,
    notes=("<p><strong>Role</strong> The campaign's first villain and the emotional payoff of every PC's "
        "background hook — but deliberately <em>not</em> a tank. Build him as a frail, slippery sniper who "
        "weaponizes his crocodile, Gobblegut, rather than as a tough boss. The threat in this fight is the "
        "<em>gator</em>; Gaedren is the catalyst.</p>"
        "<p><strong>Tactics</strong> Round 1: Spur the Beast (shoot Gobblegut to enrage it), then snipe from "
        "across the pool where the walkways and the gator force the PCs to choose between reaching him and "
        "avoiding the water. Uses Nimble Dodge when focus-fired. <strong>Morale:</strong> at &le; 8 HP he tries "
        "to reach a skiff at the underpier (A12) and flee. <strong>If he escapes,</strong> he can recur via his "
        "son Rolth (Ch.2). <strong>If killed and the body is left here,</strong> Rolth animates it as a zombie in "
        "the Dead Warrens (D13) — track this.</p>"),
    blurb="Decrepit crime lord; first villain of the AP"))

# --- Yargin Balko (L1 alchemist-fence; acid thrower) ---
yargin_items = [
 strike("Acid Flask", 7, "1d6", "acid", ["range-increment-20","splash","alchemical","bomb"],
        extra_dmg=[("1","persistent-acid")]),
 strike("Light Crossbow", 5, "1d8", "piercing", ["range-increment-60","reload-1"]),
 strike("Dagger", 5, "1d4+1", "piercing", ["agile","finesse","versatile-s"]),
 action("Quick Acid", "1",
        "<p>Yargin draws and throws an Acid Flask in a single action (he keeps several looped on his belt). "
        "He carries 3 flasks.</p>", ["alchemical"]),
 lore("Alchemy Lore", 7),
]
write("actors", "yargin-balko", npc("act_yargin","Yargin Balko",1, 16, 20, 5, 5, 7, 6,
    {"str":1,"dex":2,"con":1,"int":3,"wis":2,"cha":1}, 25,
    {"crafting":7,"society":6,"deception":5,"thievery":5,"intimidation":6,"arcana":6},
    ["humanoid","human"], ["Common","Gnomish","Varisian"], yargin_items,
    notes=("<p><strong>Role</strong> Gaedren's accountant/fence; the fishery's public face. Answers the front "
        "door (A1) and fights from A6. <strong>Tactics:</strong> opens with thrown Acid Flasks, falls back to "
        "the light crossbow. <strong>Morale:</strong> flees down the hidden trapdoor (A6) to warn Gaedren the "
        "moment the fight turns against him — if he reaches Gaedren, the boss fight begins forewarned. Carries "
        "the brass key (opens all fishery doors).</p>"),
    blurb="Bitter alchemist-fence; Gaedren's right hand"))

# --- Hookshanks Gruller (L1 gnome rogue taskmaster, A7) ---
hook_items = [
 strike("Kukri", 7, "1d6+1", "slashing", ["agile","finesse","trip"], extra_dmg=[("1d6","precision")]),
 strike("Dagger", 7, "1d4+1", "piercing", ["agile","finesse","thrown-10","versatile-s"],
        extra_dmg=[("1d6","precision")]),
 action("Sneak Attack", "passive",
        "<p>+1d6 precision damage vs off-guard creatures (included in Strikes when applicable).</p>", ["rogue"]),
 action("Disguised as an Orphan", "passive",
        "<p>Hookshanks (a gnome) passes himself off as one of Lamm's Lambs at a glance. A PC actively "
        "studying the 'children' notices the imposter with a successful Perception check (DC 17) against his "
        "Deception. He uses this to set up a Sneak Attack or to slip away.</p>"),
 action("Surrender & Inform", "free",
        "<p>If reduced to fewer than half his HP or clearly losing, Hookshanks throws down his kukri and talks. "
        "He knows everything about the fishery and Gaedren's routine <em>except</em> the location of Gaedren's "
        "private den (A14). A captured, cooperative Hookshanks can shortcut the rest of the dungeon.</p>"),
 lore("Streetwise Lore", 6),
]
write("actors", "hookshanks-gruller", npc("act_hookshanks","Hookshanks Gruller",1, 16, 18, 4, 7, 5, 5,
    {"str":0,"dex":4,"con":1,"int":1,"wis":1,"cha":2}, 25,
    {"stealth":9,"deception":8,"thievery":7,"acrobatics":7,"society":4,"intimidation":5},
    ["humanoid","gnome"], ["Common","Gnomish"], hook_items,
    notes=("<p><strong>Role</strong> Cruel taskmaster overseeing the orphans in the Upper Workroom (A7). "
        "Hides among the children. Can surrender and become an information source.</p>"),
    size="sml", blurb="Gnome taskmaster who hides among the orphans"))

# --- Giggles (L1 half-orc bruiser, A8; nonlethal capturer) ---
gig_items = [
 strike("Flail", 7, "1d6+3", "bludgeoning", ["sweep","trip"]),
 strike("Fist", 7, "1d4+3", "bludgeoning", ["agile","nonlethal","unarmed"]),
 strike("Composite Longbow", 5, "1d6+3", "piercing", ["range-increment-100","deadly-d10","propulsive"]),
 action("Bludgeoner", "passive",
        "<p>Giggles enjoys beating captives senseless rather than killing them. He may deal nonlethal damage "
        "with his Flail without the usual penalty, and gains a +1 circumstance bonus to attack rolls when he "
        "makes a nonlethal melee Strike against a creature that is not yet at half HP.</p>"),
 action("Orc Ferocity", "reaction",
        "<p><strong>Trigger</strong> Giggles is reduced to 0 HP.</p><hr /><p><strong>Effect</strong> He stays at "
        "1 HP and is wounded 1 (or increases his wounded value). Once per day.</p>"),
 lore("Brawling Lore", 5),
]
write("actors", "giggles", npc("act_giggles","Giggles",1, 16, 24, 7, 5, 3, 5,
    {"str":3,"dex":1,"con":3,"int":0,"wis":1,"cha":0}, 25,
    {"athletics":7,"intimidation":5},
    ["humanoid","orc","human"], ["Common","Orcish"], gig_items,
    notes=("<p><strong>Role</strong> The fishery's muscle, working the main floor (A8). Tries to capture PCs "
        "nonlethally (Bludgeoner) for Gaedren rather than killing outright. <strong>Morale:</strong> fights to "
        "the death (Orc Ferocity). Carries 3 minor healing potions.</p>"),
    blurb="Half-orc brute; the fishery's muscle"))

# --- Drain Spider (L-1 tiny vermin; nest in A10/A11) ---
spider_items = [
 strike("Fangs", 7, "1d4", "piercing", ["finesse"], extra_dmg=[("1d4","poison")]),
 action("Drain Spider Venom", "passive",
        "<p><strong>Saving Throw</strong> Fortitude DC 15; <strong>Maximum Duration</strong> 4 rounds; "
        "<strong>Stage 1</strong> 1d4 poison damage and enfeebled 1 (1 round).</p>"
        "<p><em>Vermin repellent:</em> a drain spider that smells Gaedren's alchemical repellent (sold by the "
        "vial in his den) is sickened 1 and will not approach a creature coated in it — model as an automatic "
        "failure to close, no attack.</p>", ["poison"]),
 action("Lunge", "passive",
        "<p>The aggressive spider attacks the first creature to enter its lair, gaining the benefits of being "
        "off-guard against a surprised target.</p>"),
]
write("actors", "drain-spider", npc("act_drainspider","Drain Spider",-1, 15, 8, 3, 6, 2, 5,
    {"str":-2,"dex":4,"con":1,"int":-5,"wis":1,"cha":-4}, 25,
    {"stealth":6,"athletics":3},
    ["animal"], [], spider_items, senses=[{"type":"darkvision"},{"acuity":"imprecise","type":"tremorsense","range":30}],
    other_speeds=[{"type":"climb","value":25}],
    notes=("<p>Cat-sized sewer spiders nesting in the wrecked ship (A10 = 1; A11 = 4). Aggressive but trivially "
        "repelled by the vermin repellent the PCs can loot from A13. Treat the A11 nest as a single Low/Moderate "
        "encounter of four.</p>"),
    size="tiny", blurb="Aggressive cat-sized venomous spider"))

# --- Jigsaw Shark (L1 aquatic; under the fishery, avoidable) ---
shark_items = [
 strike("Jaws", 8, "1d8+3", "piercing", ["deadly-d8"]),
 action("Aquatic Ambush", "1",
        "<p><strong>Requirements</strong> The shark is hidden and in water. <strong>Effect</strong> It Swims up "
        "to its Speed toward a creature in the water and makes a Jaws Strike; the target is off-guard against it.</p>"),
 action("Reluctant Leaper", "passive",
        "<p>The shark attacks anything that falls into the water beneath the fishery, but only leaps onto the "
        "floating underpier (A12) to attack a creature there if it has already been attacked and damaged.</p>"),
]
write("actors", "jigsaw-shark", npc("act_jigsawshark","Jigsaw Shark",1, 16, 20, 7, 6, 3, 7,
    {"str":3,"dex":2,"con":2,"int":-4,"wis":2,"cha":-2}, 5,
    {"athletics":8},
    ["animal","aquatic"], [], shark_items, senses=[{"acuity":"imprecise","type":"scent","range":30}],
    other_speeds=[{"type":"swim","value":35}],
    notes=("<p>Scavenger lurking in the river under the fishery. The hazards (slippery boardwalk A3, rotten deck "
        "A9, hole in A8) all feed creatures into its water. Avoidable if the PCs stay dry; a real threat if they "
        "fall in. Standard PF2e drowning/aquatic-combat rules apply to PCs in the water.</p>"),
    blurb="River shark beneath the fishery"))

# --- Lamm's Lamb / Orphan (L-1 non-combatant; moral element) ---
orphan_items = [
 strike("Pitchfork (improvised)", 5, "1d6-1", "piercing", ["reach","improvised"]),
 strike("Dagger", 5, "1d4-1", "piercing", ["agile","finesse"]),
 action("Cower", "passive",
        "<p>An orphan who takes any damage flees toward the main floor (A8); if all the thugs are dead or out of "
        "sight, it flees the fishery entirely. Orphans invaded at night are too frightened to fight at all.</p>"),
 action("Rally to the Heroes", "passive",
        "<p>A PC can rally an orphan with a successful Diplomacy check (DC 15; Intimidation does not work). A "
        "rallied orphan can use the Aid reaction to help a PC's attack or skill check, or reveal what it knows "
        "about the fishery and Gaedren. <strong>Story:</strong> rescuing the orphans is the heart of this dungeon "
        "(see the Treasure/XP notes); one orphan is the payoff for a PC with the 'Missing Child' background hook.</p>"),
]
write("actors", "lamms-lamb", npc("act_orphan","Lamm's Lamb (Orphan)",-1, 15, 6, 2, 6, 3, 5,
    {"str":-2,"dex":3,"con":0,"int":0,"wis":-1,"cha":0}, 25,
    {"acrobatics":7,"thievery":7,"stealth":6},
    ["humanoid","human"], ["Common"], orphan_items,
    notes=("<p>Enslaved child pickpockets. <strong>Non-combatants and a deliberate moral pressure point — not "
        "an XP source for killing.</strong> 9 are present by day (spread through A7/A8); 26 sleep in A8 at night. "
        "They can be rallied to the PCs' side (Diplomacy DC 15) or, if ignored, may be forced to fight for the "
        "thugs. See the Conversion Notes journal for the rescue framing.</p>"),
    size="sml", blurb="Enslaved orphan ('Lamm's Lamb')"))

# =====================================================================
# HAZARDS
# =====================================================================
boardwalk_items = [
 action("Slip", "reaction",
   "<p><strong>Trigger</strong> A creature Strides more than 5 feet, Steps onto, or fights while on the slick "
   "boardwalk.</p><hr /><p><strong>Effect</strong> The creature must succeed at a DC 15 Reflex save (or Acrobatics "
   "check to Balance) or fall prone; on a critical failure it slides off and falls 13 feet into the river "
   "(@Damage[1[bludgeoning]] from the short fall into deep water) and into the hunting grounds of the Jigsaw "
   "Shark (A12). A creature that Steps (5 ft) or moves carefully is not affected.</p>"),
]
write("hazards", "slippery-boardwalk", hazard("haz_boardwalk","Slippery Boardwalk",1,
    0, "<p>Obvious — no check needed to notice the danger.</p>",
    "<p>@Check[acrobatics|dc:15|name:Cross Carefully] to move along it without risk, or shore up a stretch with "
    "rope/planks (Crafting or Survival, DC 15).</p>",
    "<p>A barnacle-slick boardwalk (A3) clings to the fishery 13 feet above shark-infested water; the old planks "
    "also groan under heavy loads (a creature heavier than Medium, or two creatures within 5 feet, may collapse a "
    "stretch — treat as the Rotten Ship Deck reaction).</p>",
    boardwalk_items, traits=["environmental"], reset="<p>Persistent terrain.</p>"))

deck_items = [
 action("Collapse", "reaction",
   "<p><strong>Trigger</strong> A Medium or larger creature moves onto the rotten foredeck of the Kraken's Folly "
   "(A9) toward the bow.</p><hr /><p><strong>Effect</strong> The creature must succeed at a DC 16 Reflex save or "
   "crash through to the hold (A11), taking @Damage[1d6[bludgeoning]] falling/debris damage and landing prone "
   "among the drain-spider nest. The stern (within 10 feet) is sound.</p>"),
]
write("hazards", "rotten-ship-deck", hazard("haz_rottendeck","Rotten Ship Deck",1,
    16, "<p>@Check[perception|dc:16|name:Spot the Rot] to notice the foredeck is unsafe before stepping on it.</p>",
    "<p>@Check[crafting|dc:16|name:Shore Up the Planks] to brace a path across, or simply avoid the bow and keep "
    "to the stern.</p>",
    "<p>The derelict ship Kraken's Folly (A9) has a rotten foredeck; only the stern holds weight.</p>",
    deck_items, traits=["environmental"], reset="<p>Once collapsed, that stretch is gone.</p>"))

print("Pilot actors + hazards built.")
