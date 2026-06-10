#!/usr/bin/env python3
"""Shared pf2e v8 / Foundry v14 build helpers for the CotCT conversion.

Emits Foundry "unpacked" _source JSON (one file per primary doc) with correct
_key fields (primary + embedded compound keys), Kingmaker-style structure:
folders per type, fat journals with section-block pages, scenes with map-note
pins + staged tokens, and an Adventure bundle. Deterministic.

Schema verified against the decoded pf2e-kingmaker world export (.work/kingmaker_ref)
and real pf2e v8 sources (.work/schema_ref). See research/kingmaker_schema_notes.md.
"""
from __future__ import annotations
import json, pathlib

MOD = "cotct-pf2e-conversion"
ROOT = pathlib.Path(__file__).resolve().parents[1]            # foundry-module/
PACKS = ROOT / "packs"
PUB = {"title": "Pathfinder: Curse of the Crimson Throne (PF2e conversion, private)",
       "authors": "", "license": "OGL", "remaster": True}
STATS = {"systemId": "pf2e", "systemVersion": "8.2.0", "coreVersion": "14.363",
         "compendiumSource": None, "duplicateSource": None, "exportSource": None,
         "createdTime": 0, "modifiedTime": 0, "lastModifiedBy": None}
MELEE_IMG = "systems/pf2e/icons/default-icons/melee.svg"

# collection name per pack dir (for _key)
COLL = {"actors": "actors", "hazards": "actors", "items": "items", "journals": "journal",
        "scenes": "scenes", "rolltables": "tables", "macros": "macros", "adventure": "adventures"}

# pf2e condition compendium ids — reference conditions in descriptions via these
# links (renders the condition badge), exactly like official stat blocks.
CONDITIONS = {
    "off-guard": "AJh5ex99aV6VTggg", "enfeebled": "MIRkyAjyBeXivMa7", "wounded": "Yl48xTdMh3aeQYL2",
    "prone": "j91X7x0XSomq8d60", "sickened": "fesd1n5eVhpCSS18", "frightened": "TBSHQspnbcqxsmjL",
    "clumsy": "i3OJZU2nk64Df3xm", "drained": "4D2KBtexWXa6oUMR", "stunned": "dfCMdR4wnpbYNTix",
    "grabbed": "kWc1fhmv9LBiTuei", "immobilized": "eIcWbB5o3pP6OIMe", "slowed": "xYTAsEpcJE1Ccni3",
    "fleeing": "sDPxOjQ9kx2RZE8D", "dying": "yZRUzMqrMmfLu0V1", "deafened": "9PR9y0bi4JPKnHPR",
    "persistent damage": "lDVqvLKA6eF3Df60",
}
def cond(key, label=None):
    return f"@UUID[Compendium.pf2e.conditionitems.Item.{CONDITIONS[key]}]{{{label or key.title()}}}"

# pf2e equipment-srd ids for the gear our NPCs carry — used for inline item badges
# AND for embedding real inventory items (templates in scripts/srd_gear.json, which
# hold the mechanical data + a compendiumSource link back to the SRD).
EQUIP = {"acid-flask-lesser": "M1k5QQc1qQLxzyCK", "thunderstone-lesser": "Xnqglykl3Cif8rN9",
         "healing-potion-minor": "2RuepCemJhrpKKao"}
def isrd(key, label):
    return f"@UUID[Compendium.pf2e.equipment-srd.Item.{EQUIP[key]}]{{{label}}}"

import json as _json
_GEAR_PATH = ROOT / "scripts" / "srd_gear.json"
_GEAR = _json.loads(_GEAR_PATH.read_text(encoding="utf-8")) if _GEAR_PATH.exists() else {}
def gear(key, _id, qty=1):
    """Embed a real pf2e inventory item (copied SRD mechanics + compendiumSource link)."""
    it = json.loads(json.dumps(_GEAR[key]))   # deep copy
    it["_id"] = _id; it["sort"] = 0; it["ownership"] = {"default": 0}
    it["system"]["quantity"] = qty
    return it

# ---- deterministic ID pool (separate seed from the pilot registry) ----
def _idgen(seed: int):
    import random
    r = random.Random(seed)
    A = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    while True:
        yield "".join(r.choice(A) for _ in range(16))

# ---------- low-level item builders (NPC/hazard embedded) ----------
def strike(eid, name, bonus, dmg, dmgtype, traits, extra=None, img=MELEE_IMG, slug=None):
    # extra partials may be (dice, type) or (dice, type, category) where category is
    # "persistent" / "splash" / "precision" (e.g. bombs: base + persistent + splash).
    rolls = {"0": {"damage": dmg, "damageType": dmgtype}}
    if extra:
        for i, e in enumerate(extra, 1):
            roll = {"damage": e[0], "damageType": e[1]}
            if len(e) > 2 and e[2]:
                roll["category"] = e[2]
            rolls[str(i)] = roll
    return {"_id": eid, "img": img, "name": name, "sort": 0, "type": "melee",
            "system": {"attack": {"value": ""}, "attackEffects": {"value": []},
                       "bonus": {"value": bonus}, "damageRolls": rolls,
                       "description": {"value": ""}, "publication": PUB, "rules": [],
                       "slug": slug, "traits": {"rarity": "common", "value": traits}}}

_GLYPH = {None: "systems/pf2e/icons/default-icons/action.svg",
          "1": "systems/pf2e/icons/actions/OneAction.webp", "2": "systems/pf2e/icons/actions/TwoActions.webp",
          "3": "systems/pf2e/icons/actions/ThreeActions.webp", "reaction": "systems/pf2e/icons/actions/Reaction.webp",
          "free": "systems/pf2e/icons/actions/FreeAction.webp", "passive": "systems/pf2e/icons/actions/Passive.webp"}
def action(eid, name, glyph, desc, traits=None, category="offensive", rules=None):
    atype = {"passive": "passive", "reaction": "reaction", "free": "free"}.get(glyph, "action")
    acts = int(glyph) if glyph and glyph not in ("passive", "reaction", "free") else None
    return {"_id": eid, "img": _GLYPH.get(glyph, _GLYPH[None]), "name": name, "sort": 0, "type": "action",
            "system": {"actionType": {"value": atype}, "actions": {"value": acts}, "category": category,
                       "description": {"value": desc}, "publication": PUB, "rules": rules or [], "slug": None,
                       "traits": {"rarity": "common", "value": traits or []}}}

def sneak_attack(eid, dice=1, who="The creature"):
    """Sneak Attack authored exactly like an official pf2e stat block: a clean
    one-line description with the Off-Guard CONDITION LINK, plus the rules that
    make the precision a predicated DamageDice + an Off-Guard sheet toggle (so it
    is never baked into the Strikes). Reuse this shape for any conditional passive."""
    rules = [
        {"key": "DamageDice", "selector": "strike-damage", "category": "precision",
         "diceNumber": dice, "dieSize": "d6", "predicate": ["target:condition:off-guard"]},
        {"key": "RollOption", "domain": "all", "option": "target:condition:off-guard",
         "toggleable": "totm", "label": "PF2E.SpecificRule.TOTMToggle.OffGuard"},
    ]
    return action(eid, "Sneak Attack", "passive",
        f"<p>{who} deals {dice}d6 extra precision damage to {cond('off-guard','Off-Guard')} creatures.</p>",
        traits=["rogue"], rules=rules)

def lore(eid, name, mod):
    return {"_id": eid, "img": "systems/pf2e/icons/default-icons/lore.svg", "name": name, "sort": 0, "type": "lore",
            "system": {"description": {"value": ""}, "mod": {"value": mod}, "proficient": {"value": 0},
                       "publication": PUB, "rules": [], "slug": None}}

# ---------- prototype token (Kingmaker-style defaults) ----------
def prototoken(name, size="med", disposition=-1, actor_link=False, token_src=None,
               sight=False, has_hp=True):
    SCALE = {"tiny": 1, "sml": 1, "med": 1, "lg": 1, "huge": 1, "grg": 1}
    return {"name": name, "displayName": 20, "displayBars": 20, "disposition": disposition,
            "actorLink": actor_link, "width": 1, "height": 1, "lockRotation": False, "rotation": 0,
            "alpha": 1, "randomImg": False, "appendNumber": False, "prependAdjective": False,
            "texture": {"src": token_src or "icons/svg/mystery-man.svg", "scaleX": 1, "scaleY": 1,
                        "tint": "#ffffff", "anchorX": 0.5, "anchorY": 0.5, "fit": "contain",
                        "offsetX": 0, "offsetY": 0, "rotation": 0, "alphaThreshold": 0.75},
            "bar1": {"attribute": "attributes.hp" if has_hp else None}, "bar2": {"attribute": None},
            "sight": {"enabled": sight, "range": 0, "angle": 360, "visionMode": "basic", "color": None,
                      "attenuation": 0.1, "brightness": 0, "saturation": 0, "contrast": 0},
            "detectionModes": [], "light": {"alpha": 0.5, "angle": 360, "bright": 0, "dim": 0,
                      "color": None, "coloration": 1, "luminosity": 0.5, "attenuation": 0.5,
                      "animation": {"type": None, "speed": 5, "intensity": 5, "reverse": False},
                      "darkness": {"min": 0, "max": 1}},
            "flags": {"pf2e": {"linkToActorSize": True, "autoscale": True}} if has_hp else {}}

# ---------- actor / hazard ----------
def npc(_id, name, level, ac, hp, fort, ref, will, per, abil, speed, skills, traits, langs,
        items, notes, folder=None, senses=None, other_speeds=None, size="med", blurb="",
        token_src=None, actor_link=False, compendium_source=None):
    sys = {"abilities": {k: {"mod": v} for k, v in abil.items()},
           "attributes": {"ac": {"details": "", "value": ac}, "allSaves": {"value": ""},
                          "hp": {"details": "", "max": hp, "temp": 0, "value": hp},
                          "speed": {"otherSpeeds": other_speeds or [], "value": speed}},
           "details": {"blurb": blurb, "languages": {"details": "", "value": [l.lower() for l in langs]},
                       "level": {"value": level}, "privateNotes": "", "publicNotes": notes, "publication": PUB},
           "initiative": {"statistic": "perception"},
           "perception": {"details": "", "mod": per, "senses": senses or []},
           "resources": {}, "saves": {"fortitude": {"saveDetail": "", "value": fort},
                                       "reflex": {"saveDetail": "", "value": ref},
                                       "will": {"saveDetail": "", "value": will}},
           "skills": {k: {"base": v} for k, v in skills.items()},
           "traits": {"rarity": "common", "size": {"value": size}, "value": traits}}
    st = dict(STATS); st["compendiumSource"] = compendium_source
    return {"_id": _id, "name": name, "type": "npc", "img": "systems/pf2e/icons/default-icons/npc.svg",
            "items": items, "system": sys, "folder": folder, "sort": 0, "ownership": {"default": 0},
            "flags": {}, "_stats": st, "prototypeToken": prototoken(name, size, token_src=token_src, actor_link=actor_link)}

def hazard(_id, name, level, stealth, stealth_note, disable, desc, items, folder=None,
           ac=None, hardness=0, hp=0, fort=0, ref=0, will=0, traits=None, reset="", routine="", complex_=False):
    attr = {"emitsSound": "encounter", "hardness": hardness, "stealth": {"details": stealth_note, "value": stealth}}
    if hp:
        attr["hasHealth"] = True
        attr["hp"] = {"details": "", "max": hp, "temp": 0, "tempmax": 0, "value": hp}
        attr["immunities"] = [{"type": "critical-hits"}, {"type": "precision"}]
    if ac is not None:
        attr["ac"] = {"value": ac}
    for it in items:                       # hazard reactions/actions use a null category (official convention)
        if it.get("type") == "action":
            it["system"]["category"] = None
    return {"_id": _id, "name": name, "type": "hazard", "img": "systems/pf2e/icons/default-icons/hazard.svg",
            "items": items, "folder": folder, "sort": 0, "ownership": {"default": 0}, "flags": {}, "_stats": dict(STATS),
            "prototypeToken": prototoken(name, "med", disposition=-1, has_hp=bool(hp)),
            "system": {"attributes": attr, "creatureType": "",
                       "details": {"description": desc, "disable": disable, "isComplex": complex_,
                                   "level": {"value": level}, "publication": PUB, "reset": reset, "routine": routine},
                       "saves": {"fortitude": {"saveDetail": "", "value": fort}, "reflex": {"saveDetail": "", "value": ref},
                                 "will": {"saveDetail": "", "value": will}},
                       "statusEffects": [], "traits": {"rarity": "common", "size": {"value": "med"}, "value": traits or ["environmental"]}}}

def equipment(_id, name, level, price_gp, desc, traits=None, bulk=0.1, rarity="common", folder=None,
              img="systems/pf2e/icons/default-icons/equipment.svg"):
    return {"_id": _id, "img": img, "name": name, "type": "equipment", "folder": folder, "sort": 0,
            "ownership": {"default": 0}, "flags": {}, "_stats": dict(STATS),
            "system": {"baseItem": None, "bulk": {"value": bulk}, "containerId": None,
                       "description": {"value": desc}, "equipped": {"carryType": "worn", "handsHeld": 0, "invested": None},
                       "hardness": 0, "hp": {"max": 0, "value": 0}, "level": {"value": level},
                       "material": {"grade": None, "type": None}, "price": {"value": {"gp": price_gp}},
                       "publication": PUB, "quantity": 1, "rules": [], "size": "med", "slug": None,
                       "traits": {"rarity": rarity, "value": traits or []}, "usage": {"value": "worn"}}}

def background(_id, name, desc, boost_choice, trained_skill, lore, folder=None):
    """PF2e background item: a fixed choice of two ability boosts + a free boost,
    one trained skill, and a Lore. (Granted skill feat is recommended in `desc`;
    players add it.)"""
    return {"_id": _id, "name": name, "type": "background", "folder": folder, "sort": 0,
            "img": "systems/pf2e/icons/default-icons/background.svg",
            "ownership": {"default": 0}, "flags": {}, "_stats": dict(STATS),
            "system": {"description": {"value": desc},
                       "boosts": {"0": {"value": boost_choice},
                                  "1": {"value": ["str", "dex", "con", "int", "wis", "cha"]}},
                       "trainedSkills": {"value": [trained_skill], "lore": [lore]},
                       "items": {}, "rules": [], "slug": None, "publication": PUB,
                       "traits": {"rarity": "common", "value": []}}}

# ---------- folder ----------
def folder(_id, name, ftype, parent=None, sort=0, color=None, sorting="m"):
    return {"_id": _id, "name": name, "type": ftype, "folder": parent, "sorting": sorting,
            "sort": sort, "color": color, "description": "", "flags": {}, "_stats": dict(STATS),
            "_key": f"!folders!{_id}"}

# ---------- journal page + section-block HTML ----------
def page(_id, name, html, level=1, show=True, sort=0, ownership=None):
    return {"_id": _id, "name": name, "type": "text", "title": {"show": show, "level": level},
            "text": {"format": 1, "content": html, "markdown": ""}, "image": {},
            "video": {"controls": True, "volume": 0.5}, "src": None, "system": {}, "sort": sort,
            "ownership": ownership or {"default": -1}, "flags": {}, "category": None}

def s_desc(html): return f'<section class="description">{html}</section>'   # read-aloud / boxed text
s_read = s_desc                                                            # semantic alias
def s_gm(html): return f'<section class="gm-notes">{html}</section>'
def s_encounter(inner): return f'<section class="encounter">{inner}</section>'
def s_skill(html): return f'<section class="skill">{html}</section>'
def s_treasure(html): return f'<section class="treasure">{html}</section>'
def s_conv(html): return f'<section class="conversion">{html}</section>'

def s_secret(html, sid):
    """GM-hidden block. Foundry core hides section.secret from non-owners; our CSS
    tints it + badges it 'GM ONLY' so it also reads as hidden when the GM views it."""
    return f'<section class="secret" id="secret-{sid}">{html}</section>'

def s_milestone(html): return f'<section class="milestone head">{html}</section>'

def aside_token(items, img=None, porthole=False, flip=False):
    """Kingmaker-style creature sidebar: <aside class="right token|porthole"> with an
    optional token image and a <ul> of @UUID actor links. `items` = list of HTML <li> bodies."""
    cls = "right porthole" if porthole else "right token"
    im = f'<img class="{"flip" if flip else "token"}" src="{img}" />' if img else ""
    lis = "".join(f"<li>{it}</li>" for it in items)
    return f'<aside class="{cls}">{im}<ul>{lis}</ul></aside>'

def enc(title, budget, body, aside=""):
    """Full encounter block: optional aside, then a split header (name | XP budget), then body.
    The title is a <span>, NOT a heading — headings (h1-h3) leak into the journal's
    page navigation; encounters should not appear there (matches Kingmaker)."""
    return (f'<section class="encounter">{aside}'
            f'<header class="split"><span class="enc-name">{title}</span><span class="enc-budget">{budget}</span></header>'
            f'{body}</section>')

def journal_entry(_id, name, pages, folder=None, sort=0, default_own=0):
    for i, p in enumerate(pages, 1):
        p["sort"] = i * 100000
        p["_key"] = f"!journal.pages!{_id}.{p['_id']}"
    return {"_id": _id, "name": name, "pages": pages, "folder": folder, "sort": sort,
            "ownership": {"default": default_own}, "flags": {}, "_stats": dict(STATS),
            "categories": [], "_key": f"!journal!{_id}"}

# ---------- scene + note + token ----------
def note(_id, entry_id, page_id, text, x, y, icon="icons/svg/book.svg"):
    return {"_id": _id, "entryId": entry_id, "pageId": page_id, "text": text, "x": x, "y": y,
            "global": False, "iconSize": 40, "fontFamily": "Signika", "fontSize": 32,
            "textColor": "#ffffff", "textAnchor": 1, "elevation": 0, "sort": 0, "flags": {},
            "texture": {"src": icon, "tint": "#ffffff", "anchorX": 0.5, "anchorY": 0.5, "fit": "contain",
                        "scaleX": 1, "scaleY": 1, "offsetX": 0, "offsetY": 0, "rotation": 0, "alphaThreshold": 0.75}}

def token(_id, actor_id, name, x, y, token_src, disposition=-1, hidden=True):
    return {"_id": _id, "name": name, "actorId": actor_id, "actorLink": False, "x": x, "y": y,
            "width": 1, "height": 1, "disposition": disposition, "hidden": hidden,
            "displayName": 20, "displayBars": 20, "lockRotation": False, "rotation": 0, "alpha": 1,
            "texture": {"src": token_src, "scaleX": 1, "scaleY": 1, "tint": "#ffffff", "anchorX": 0.5,
                        "anchorY": 0.5, "fit": "contain", "offsetX": 0, "offsetY": 0, "rotation": 0, "alphaThreshold": 0.75},
            "bar1": {"attribute": "attributes.hp"}, "bar2": {"attribute": None},
            "sight": {"enabled": False, "range": 0, "angle": 360, "visionMode": "basic", "brightness": 0,
                      "saturation": 0, "contrast": 0, "attenuation": 0.1, "color": None},
            "detectionModes": [], "flags": {"pf2e": {"linkToActorSize": True, "autoscale": True}},
            "delta": None, "elevation": 0, "sort": 0}

def scene(_id, name, width, height, grid_px, bg_src, notes, tokens, folder=None,
          foreground=None, navName=None, sort=0):
    for n in notes: n["_key"] = f"!scenes.notes!{_id}.{n['_id']}"
    for t in tokens: t["_key"] = f"!scenes.tokens!{_id}.{t['_id']}"
    return {"_id": _id, "name": name, "folder": folder, "sort": sort, "navigation": True,
            "navName": navName or "", "navOrder": 0, "active": False, "ownership": {"default": 0},
            "flags": {"pf2e": {"rulesBasedVision": None, "hearingRange": None, "environmentTypes": [], "syncDarkness": "default"}},
            "_stats": dict(STATS), "_key": f"!scenes!{_id}",
            "background": {"src": bg_src, "anchorX": 0, "anchorY": 0, "offsetX": 0, "offsetY": 0,
                           "fit": "fill", "scaleX": 1, "scaleY": 1, "rotation": 0, "tint": "#ffffff", "alphaThreshold": 0},
            "foreground": foreground, "foregroundElevation": 20, "thumb": None,
            "width": width, "height": height, "padding": 0.25, "backgroundColor": "#000000",
            "grid": {"type": 1, "size": grid_px, "style": "solidLines", "thickness": 1, "color": "#000000",
                     "alpha": 0.2, "distance": 5, "units": "ft"},
            "initial": {"x": None, "y": None, "scale": None}, "tokenVision": True,
            "fog": {"exploration": True, "overlay": None, "colors": {"explored": None, "unexplored": None}},
            "environment": {"darknessLevel": 0, "darknessLock": False, "globalLight": {"enabled": True, "alpha": 0.5,
                            "bright": False, "color": None, "coloration": 1, "luminosity": 0, "saturation": 0,
                            "contrast": 0, "shadows": 0, "darkness": {"min": 0, "max": 1}},
                            "cycle": True, "base": {"hue": 0, "intensity": 0, "luminosity": 0, "saturation": 0, "shadows": 0},
                            "dark": {"hue": 0, "intensity": 0, "luminosity": -0.25, "saturation": 0, "shadows": 0}},
            "journal": None, "journalEntryPage": None, "playlist": None, "playlistSound": None,
            "weather": "", "navigation": True,
            "drawings": [], "tokens": tokens, "lights": [], "sounds": [], "templates": [],
            "notes": notes, "tiles": [], "walls": [], "regions": []}

# ---------- adventure bundle ----------
def adventure(_id, name, img, caption, folders, journals, scenes_, actors, items, tables=None, macros=None):
    return {"_id": _id, "name": name, "img": img, "caption": caption,
            "description": caption, "sort": 0, "flags": {}, "_stats": dict(STATS), "_key": f"!adventures!{_id}",
            "folders": folders, "journal": journals, "scenes": scenes_, "actors": actors,
            "items": items, "tables": tables or [], "macros": macros or [], "playlists": [], "cards": []}

# ---------- rolltable + macro ----------
def rolltable(_id, name, formula, results, desc="", folder=None, sort=0):
    """results: list of dicts with _id, range:[lo,hi], text (+ optional weight/type/img)."""
    out = []
    for r in results:
        out.append({"_id": r["_id"], "type": r.get("type", "text"), "text": r["text"],
                    "img": r.get("img", "icons/svg/d20-black.svg"), "weight": r.get("weight", 1),
                    "range": r["range"], "drawn": False,
                    "documentCollection": r.get("documentCollection"), "documentId": r.get("documentId"),
                    "flags": {}, "_key": f"!tables.results!{_id}.{r['_id']}"})
    return {"_id": _id, "name": name, "description": desc, "formula": formula,
            "replacement": True, "displayRoll": True, "img": "icons/svg/d20-grey.svg",
            "results": out, "folder": folder, "sort": sort, "ownership": {"default": 0},
            "flags": {}, "_stats": dict(STATS), "_key": f"!tables!{_id}"}

def macro(_id, name, command, img="icons/svg/dice-target.svg", folder=None, sort=0):
    return {"_id": _id, "name": name, "type": "script", "img": img, "scope": "global",
            "command": command, "author": None, "ownership": {"default": 0}, "folder": folder,
            "sort": sort, "flags": {}, "_stats": dict(STATS), "_key": f"!macros!{_id}"}

# ---------- writers ----------
def write(pack, slug, doc, embed_items=False, embed_pages=False):
    d = PACKS / pack / "_source"
    d.mkdir(parents=True, exist_ok=True)
    doc["_key"] = f"!{COLL[pack]}!{doc['_id']}"
    if embed_items:
        for it in doc.get("items", []):
            it["_key"] = f"!actors.items!{doc['_id']}.{it['_id']}"
    if embed_pages:
        for p in doc.get("pages", []):
            p["_key"] = f"!journal.pages!{doc['_id']}.{p['_id']}"
    (d / f"{slug}.json").write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return doc
