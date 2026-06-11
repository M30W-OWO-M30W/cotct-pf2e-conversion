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
import json, pathlib, os, re

# ---- shared verbatim read-aloud (pulled from the GM's local AP.md at build) ----
# Each chapter script passes its own start-anchor; AP prose is NEVER committed.
SRC_MD = os.environ.get("COTCT_AP_MD",
    "/mnt/c/Users/maman/Downloads/Curse of the Crimson Throne AP.md")
_PARAS_CACHE = None      # list of (normalized_text, start_line_number)
SCOPE = None             # (lo_line, hi_line) — set per chapter script so an anchor
                         # can NEVER match another chapter's text (two-column OCR
                         # plus generic anchors caused cross-chapter mis-injection)
def _paras():
    global _PARAS_CACHE
    if _PARAS_CACHE is None:
        try: raw = open(SRC_MD, encoding="utf-8").read()
        except OSError: raw = ""
        out, line = [], 1
        for block in re.split(r"\n\s*\n", raw):
            out.append((" ".join(block.split()), line))
            line += block.count("\n") + 2
        _PARAS_CACHE = out
    return _PARAS_CACHE
def _in_scope(lineno):
    return SCOPE is None or (SCOPE[0] <= lineno < SCOPE[1])
def parafy(text, target=550):
    """Split one long paragraph into several <p> blocks at sentence boundaries
    (~target chars each) — long verbatim read-aloud renders as a wall otherwise."""
    text = text.strip()
    if len(text) <= target * 1.5:
        return "<p>" + text + "</p>"
    sents = re.split(r"(?<=[.!?\u2019\u201d]) +", text)
    out, cur = [], ""
    for sent in sents:
        if cur and len(cur) + len(sent) > target:
            out.append(cur); cur = sent
        else:
            cur = (cur + " " + sent).strip()
    if cur:
        out.append(cur)
    # never let a chunk start lowercase (OCR mid-sentence periods) — merge back
    fixed = []
    for x in out:
        if fixed and x[:1].islower():
            fixed[-1] = fixed[-1] + " " + x
        else:
            fixed.append(x)
    return "".join("<p>" + x + "</p>" for x in fixed)


def _scrub_ocr(text):
    """Remove two-column OCR interleave artifacts from verbatim text: stranded
    stat tokens, running-header fragments, and ligature junk that the PDF's
    column layout injected mid-paragraph."""
    text = re.sub(r"\s*\b(?:CR|XP|hp)\s+[\d,/]+\b\s*", " ", text)
    text = re.sub(r"\s*\b(?:rff|ftfl|fffi|flff|ffft|flffft|fl|fi)\b\s*(?=[a-z]*\s*[A-Z])", " ", text)
    text = re.sub(r"\s*\bHANDOUT\s*#?[\d-]*\b.*$", "", text)        # cut at handout captions
    text = re.sub(r"\s*\b(?:CHAPTER BACKGROUND|PART \d:?|CHAPTER CONCLUSION)\b\s*", " ", text)
    text = re.sub(r"  +", " ", text).strip()
    if text and text[-1].isalpha():
        text += "."
    return text

def verbatim(anchor):
    """Return the AP paragraph that starts with (or contains) `anchor`, re-flowed
    across mid-sentence image/page markers, with leading OCR drop-caps repaired.
    Returns '' if the source file is absent — callers must supply a fallback."""
    a = " ".join(anchor.split())
    if not a: return ""
    paras = _paras()
    si = next((k for k, (p, ln) in enumerate(paras) if p.startswith(a) and _in_scope(ln)), None)
    if si is None:
        si = next((k for k, (p, ln) in enumerate(paras) if a in p and _in_scope(ln)), None)
    if si is None:
        if SCOPE is not None and any(p.startswith(a) or a in p for p, ln in paras):
            print(f"  [verbatim] anchor matches only OUTSIDE chapter scope {SCOPE}: {a[:50]!r} -> fallback used")
        return ""
    text, k = paras[si][0], si + 1
    while text and text[-1] not in '.!?:"”\'’)' and k < len(paras):
        nxt = paras[k][0]
        if nxt.startswith("#") or nxt.startswith("HANDOUT"): break
        # two-column OCR junk INSIDE a sentence: skip it and keep merging so the
        # sentence completes from the paragraph beyond the interleave
        if re.fullmatch(r"(?:CR|XP|hp)\s+[\d,/]+(?:\s+each)?", nxt) or (nxt.isupper() and len(nxt.split()) <= 6):
            k += 1; continue
        if (not nxt) or nxt.startswith("<!--"):
            k += 1; continue
        text, k = text + " " + nxt, k + 1
    return _scrub_ocr(re.sub(r'^([B-HJ-Z]) ([a-z])', r'\1\2', text))

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
# links (renders the condition badge), exactly like official stat blocks. The full
# 43-condition map is extracted by scripts/extract_conditions.mjs; the hardcoded
# entries below (incl. the space-keyed "persistent damage") are kept for back-compat.
import json as _json2, pathlib as _pl2
_COND_PATH = _pl2.Path(__file__).resolve().parents[1] / "scripts" / "conditions_index.json"
CONDITIONS = _json2.loads(_COND_PATH.read_text(encoding="utf-8")) if _COND_PATH.exists() else {}
CONDITIONS.update({
    "off-guard": "AJh5ex99aV6VTggg", "enfeebled": "MIRkyAjyBeXivMa7", "wounded": "Yl48xTdMh3aeQYL2",
    "prone": "j91X7x0XSomq8d60", "sickened": "fesd1n5eVhpCSS18", "frightened": "TBSHQspnbcqxsmjL",
    "clumsy": "i3OJZU2nk64Df3xm", "drained": "4D2KBtexWXa6oUMR", "stunned": "dfCMdR4wnpbYNTix",
    "grabbed": "kWc1fhmv9LBiTuei", "immobilized": "eIcWbB5o3pP6OIMe", "slowed": "xYTAsEpcJE1Ccni3",
    "fleeing": "sDPxOjQ9kx2RZE8D", "dying": "yZRUzMqrMmfLu0V1", "deafened": "9PR9y0bi4JPKnHPR",
    "persistent damage": "lDVqvLKA6eF3Df60",
})
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

# Official pf2e Bestiary index (slug -> {pack,id,level,name}), extracted from the
# installed system by scripts/extract_bestiary.mjs. Official monsters get @UUID
# links to the Bestiary instead of being rebuilt — higher fidelity + scalable.
_BEST_PATH = ROOT / "scripts" / "bestiary_index.json"
MONSTERS = _json.loads(_BEST_PATH.read_text(encoding="utf-8")) if _BEST_PATH.exists() else {}
def mon(slug, label=None):
    """@UUID link to an official Bestiary creature. Raises if the slug is unknown
    (so a typo is a build error, not a silently-broken link)."""
    m = MONSTERS[slug]
    return f"@UUID[Compendium.pf2e.{m['pack']}.Actor.{m['id']}]{{{label or m['name']}}}"
def mon_lvl(slug):
    """Official creature level, for encounter XP-budget math."""
    return MONSTERS[slug]["level"]

# ---- PF2e encounter difficulty (GMC budget) — sanity-check every encounter ----
# Creature XP by (creature level - party level). Below -4 contributes ~0.
_XP_BY_DELTA = {-4: 10, -3: 15, -2: 20, -1: 30, 0: 40, 1: 60, 2: 80, 3: 120, 4: 160}
# Threshold budgets and per-extra-player adjustment, for a baseline 4-player party.
_BANDS = [("Trivial", 40, 10), ("Low", 60, 20), ("Moderate", 80, 20),
          ("Severe", 120, 30), ("Extreme", 160, 40)]
def creature_xp(creature_level, party_level=1):
    d = creature_level - party_level
    if d < -4: return 0
    return _XP_BY_DELTA[min(4, d)]
def encounter(creature_levels, party_level=1, players=4):
    """Return {'xp':int,'band':str,'budget':int,'detail':str} for a fight.
    Budgets scale by player count per the GMC adjustment column."""
    xp = sum(creature_xp(cl, party_level) for cl in creature_levels)
    extra = players - 4
    band, budget = "Trivial", _BANDS[0][1] + _BANDS[0][2] * extra
    for name, base, per in _BANDS:
        thr = base + per * extra
        if xp >= thr:
            band, budget = name, thr
    # PF2e has no band below Trivial — a handful of mooks is simply Trivial.
    return {"xp": xp, "band": band, "budget": budget,
            "detail": f"{len(creature_levels)} creatures, levels {sorted(creature_levels)} vs party L{party_level}×{players} → {xp} XP = {band}"}

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

def token(_id, actor_id, name, x, y, token_src, disposition=-1, hidden=True, width=1, height=1):
    return {"_id": _id, "name": name, "actorId": actor_id, "actorLink": False, "x": x, "y": y,
            "width": width, "height": height, "disposition": disposition, "hidden": hidden,
            "displayName": 20, "displayBars": 20, "lockRotation": False, "rotation": 0, "alpha": 1,
            "texture": {"src": token_src, "scaleX": 1, "scaleY": 1, "tint": "#ffffff", "anchorX": 0.5,
                        "anchorY": 0.5, "fit": "contain", "offsetX": 0, "offsetY": 0, "rotation": 0, "alphaThreshold": 0.75},
            "bar1": {"attribute": "attributes.hp"}, "bar2": {"attribute": None},
            "sight": {"enabled": False, "range": 0, "angle": 360, "visionMode": "basic", "brightness": 0,
                      "saturation": 0, "contrast": 0, "attenuation": 0.1, "color": None},
            "detectionModes": [], "flags": {"pf2e": {"linkToActorSize": True, "autoscale": True}},
            "delta": None, "elevation": 0, "sort": 0}

def light(_id, x, y, bright, dim, color=None, alpha=0.2, animation=None,
          luminosity=0.5, angle=360, walls=True):
    """AmbientLight document (field set mirrors Racooze's v12 exports)."""
    anim = {"type": animation, "speed": 4, "intensity": 4, "reverse": False} if animation \
        else {"type": None, "speed": 5, "intensity": 5, "reverse": False}
    return {"_id": _id, "x": x, "y": y, "rotation": 0, "elevation": 0, "walls": walls,
            "vision": False, "hidden": False, "locked": False, "flags": {},
            "config": {"alpha": alpha, "angle": angle, "bright": bright, "dim": dim,
                       "coloration": 1, "attenuation": 0.5, "luminosity": luminosity,
                       "saturation": 0, "contrast": 0, "shadows": 0, "animation": anim,
                       "darkness": {"min": 0, "max": 1}, "color": color,
                       "negative": False, "priority": 0}}

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

# ---------- Racooze prepared scenes (shared machinery; pilot pattern generalized) ----------
# Geometry (walls/doors/tiles/lights/thumb) injects at build from the GM's locally
# installed battlemaps module via scripts/racooze_scenes.json (gitignored). Scene
# ids are stable md5-derived constants so links and adventure bundles never drift.
import hashlib as _hl2
_RAC_PATH = ROOT / "scripts" / "racooze_scenes.json"
RACOOZE = _json.loads(_RAC_PATH.read_text(encoding="utf-8")) if _RAC_PATH.exists() else {}
# 20 of Racooze's single-image scenes shipped with background:null (export bug) —
# committed fix map points each at its obvious map image in his module
_BGFIX_PATH = ROOT / "scripts" / "racooze_bg_fixes.json"
RACOOZE_BG = _json.loads(_BGFIX_PATH.read_text(encoding="utf-8")) if _BGFIX_PATH.exists() else {}

def scene_id(racooze_name):
    """Stable 16-char scene id derived from the Racooze scene name."""
    if racooze_name == "Old Fishery":
        return "PuUGEVunRqjIWFOj"          # pilot id, grandfathered (links exist)
    return _hl2.md5(f"cotct-scene:{racooze_name}".encode()).hexdigest()[:16]

def racooze_scene(racooze_name, name, folder, notes, tokens, navName=None, sort=0):
    """Prepared scene on Racooze geometry: his walls/doors/tiles/lights/thumb plus
    our pins and staged tokens. Falls back to a wall-less placeholder grid when
    the geometry JSON is absent (Racooze module not installed at build time)."""
    _id = scene_id(racooze_name)
    geo = RACOOZE.get(racooze_name)
    if not geo:
        print(f"  [scene] no Racooze geometry for {racooze_name!r} -> placeholder")
        sc = scene(_id, name, 2400, 1800, 100, None, notes, tokens,
                   folder=folder, navName=navName or name, sort=sort)
        return sc
    bg = geo.get("background") or RACOOZE_BG.get(racooze_name)
    gpx = ((geo.get("grid") or {}).get("size")) or 100   # Sunken Queen is 50px/5ft
    sc = scene(_id, name, geo["width"], geo["height"], gpx, bg,
               notes, tokens, folder=folder, navName=navName or name, sort=sort)
    if geo.get("padding") is not None:
        sc["padding"] = geo["padding"]
    sc["thumb"] = geo.get("thumb")
    for w in geo["walls"]:
        w = dict(w); w.pop("levels", None)
        w["_key"] = f"!scenes.walls!{_id}.{w['_id']}"
        sc["walls"].append(w)
    for t in geo["tiles"]:
        t = _json.loads(_json.dumps(t)); t.pop("levels", None)
        t["_key"] = f"!scenes.tiles!{_id}.{t['_id']}"
        sc["tiles"].append(t)
    for L in geo.get("lights", []):
        L = _json.loads(_json.dumps(L)); L.pop("levels", None)
        L["_key"] = f"!scenes.lights!{_id}.{L['_id']}"
        sc["lights"].append(L)
    return sc

def scene_origin(racooze_name):
    """Top-left of the map content in scene coords: Foundry offsets the scene rect
    by ceil(padding*dim/grid)*grid. Map-local grid coords (used for keying) add
    onto this origin."""
    import math as _m
    geo = RACOOZE.get(racooze_name)
    if not geo:
        return (0, 0)
    pad = geo.get("padding") or 0.25
    return (int(_m.ceil(geo["width"] * pad / 100)) * 100,
            int(_m.ceil(geo["height"] * pad / 100)) * 100)

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

# ---------- Olliebird community statblocks (authoritative — GM directive 2026-06-10) ----------
# The conversion thread's exported compendia live in foundry-module/community/
# (materialized by scripts/import_community.py). Any actor/hazard/item we build
# whose name (alias-aware, scripts/community_aliases.json) matches a community
# doc is swapped for the community version AT WRITE TIME, keeping our _id and
# folder so every journal link survives. Community docs are pf2e-4.4-era; the
# system migrates them on import/draw. Our authored GM notes and treasure
# inventory are MERGED in, never dropped.
import hashlib as _hashlib, unicodedata as _ud
_CIDX_PATH = ROOT / "scripts" / "community_index.json"
COMMUNITY = _json.loads(_CIDX_PATH.read_text(encoding="utf-8")) if _CIDX_PATH.exists() else {}
_CALIAS_PATH = ROOT / "scripts" / "community_aliases.json"
_CALIAS = _json.loads(_CALIAS_PATH.read_text(encoding="utf-8")) if _CALIAS_PATH.exists() else {}

def _cnorm(n):
    n = _ud.normalize("NFKD", n).encode("ascii", "ignore").decode()
    n = re.sub(r"[^a-z0-9 ]", "", n.lower())
    return re.sub(r"\s+", " ", n).strip()

def _cmeta(kind, name):
    target = _CALIAS.get(kind, {}).get(name, name)
    return COMMUNITY.get(f"{kind}:{_cnorm(target)}")

def community_doc(kind, name):
    """Deep-copied community doc for `name` (alias-aware), or None."""
    meta = _cmeta(kind, name)
    if not meta:
        return None
    return _json.loads((ROOT / "community" / meta["file"]).read_text(encoding="utf-8"))

def cmon(name, label=None, kind="npc"):
    """@UUID link to a community-only actor/hazard emitted by build_community.py
    (community-original _id). For in-place REPLACED docs keep linking our own id —
    this helper raises on those to make the mistake a build error."""
    meta = _cmeta(kind, name)
    if not meta:
        raise KeyError(f"cmon: no community doc named {name!r}")
    if meta.get("replacedBy"):
        raise KeyError(f"cmon: {name!r} replaces our {meta['replacedBy']!r} in place — link that id instead")
    pack = "cotct-actors" if kind == "npc" else "cotct-hazards"
    return f"@UUID[Compendium.{MOD}.{pack}.Actor.{meta['id']}]{{{label or meta['name']}}}"

def cmon_lvl(name, kind="npc"):
    """Community creature level, for encounter XP-budget math."""
    return _cmeta(kind, name)["level"]

_PHYS_TYPES = {"weapon", "armor", "equipment", "consumable", "treasure", "backpack", "shield"}

def _community_swap(pack, doc):
    kind = {"actors": "npc", "hazards": "hazard", "items": "item"}.get(pack)
    if not kind or doc.get("type") not in {"npc", "hazard", "equipment", "weapon",
                                           "armor", "consumable", "treasure"}:
        return doc
    out = community_doc(kind, doc["name"])
    if out is None:
        return doc
    out["_id"] = doc["_id"]
    # our names are AP-canonical (the community export has typos: "Caggagehead",
    # "Shaonti", "Bavarsi") and carry area codes / epithets the journals use
    out["name"] = doc["name"]
    out["folder"] = doc.get("folder")
    out["sort"] = doc.get("sort", 0)
    out["ownership"] = {"default": 0}
    out["_stats"] = dict(STATS)
    if pack == "actors":
        # merge our authored treasure/gear where the community actor lacks it
        have = {_cnorm(i["name"]) for i in out.get("items", []) if i.get("type") in _PHYS_TYPES}
        used_ids = {i["_id"] for i in out.get("items", [])}
        for it in doc.get("items", []):
            if it.get("type") in _PHYS_TYPES and _cnorm(it["name"]) not in have:
                if it["_id"] in used_ids:
                    it = _json.loads(_json.dumps(it))
                    it["_id"] = _hashlib.md5(f"{doc['_id']}.{it['_id']}".encode()).hexdigest()[:16]
                out.setdefault("items", []).append(it)
                have.add(_cnorm(it["name"])); used_ids.add(it["_id"])
        mine = (doc.get("system", {}).get("details", {}) or {}).get("publicNotes", "") or ""
        det = out["system"].setdefault("details", {})
        theirs = det.get("publicNotes", "") or ""
        if mine.strip() and mine.strip() not in theirs:
            det["publicNotes"] = (theirs + ("<hr />" if theirs.strip() else "")
                                  + "<h3>Conversion notes (this module)</h3>" + mine)
        size = ((out["system"].get("traits", {}).get("size") or {}).get("value")) or "med"
        ptok = doc.get("prototypeToken", {}) or {}
        out["prototypeToken"] = prototoken(out["name"], size,
                                           disposition=ptok.get("disposition", -1),
                                           actor_link=ptok.get("actorLink", False))
    elif pack == "hazards":
        mine = (doc.get("system", {}).get("details", {}) or {}).get("description", "") or ""
        det = out["system"].setdefault("details", {})
        theirs = det.get("description", "") or ""
        if mine.strip() and mine.strip() not in theirs:
            det["description"] = (theirs + ("<hr />" if theirs.strip() else "")
                                  + "<h3>Conversion notes (this module)</h3>" + mine)
        hp = ((out["system"].get("attributes", {}).get("hp") or {}).get("max")) or 0
        out["prototypeToken"] = prototoken(out["name"], "med", has_hp=bool(hp))
    else:  # items
        mine = ((doc.get("system", {}).get("description") or {}).get("value", "")) or ""
        desc = out["system"].setdefault("description", {})
        theirs = desc.get("value", "") or ""
        if mine.strip() and mine.strip() not in theirs:
            desc["value"] = (theirs + ("<hr />" if theirs.strip() else "")
                             + "<h3>Conversion notes (this module)</h3>" + mine)
    print(f"  [community] {pack}: {doc['name']}")
    return out

# ---------- per-actor token art (baked from the GM's own AP PDF by token_art.py) ----------
# token_art_index.json (committed) maps actor name -> source art + face center; the
# baked webp files live ONLY in the deployed module (never the repo). Missing files
# render as Foundry defaults, so builds stay portable.
_TART_PATH = ROOT / "scripts" / "token_art_index.json"
TOKEN_ART = _json.loads(_TART_PATH.read_text(encoding="utf-8")) if _TART_PATH.exists() else {}
# external (AoN / game-icons) art shares the same slug-addressed output files
_XART_PATH = ROOT / "scripts" / "external_art_index.json"
if _XART_PATH.exists():
    for _k, _v in _json.loads(_XART_PATH.read_text(encoding="utf-8")).items():
        TOKEN_ART.setdefault(_k, _v)

def _tart_slug(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")

def token_art(name):
    """Deployed token texture path for an actor with baked art, else None."""
    return f"modules/{MOD}/assets/tokens/{_tart_slug(name)}.webp" if name in TOKEN_ART else None

def _apply_token_art(pack, doc):
    if pack not in ("actors", "hazards") or doc.get("type") not in ("npc", "hazard"):
        return doc
    if doc["name"] not in TOKEN_ART:
        return doc
    doc["img"] = f"modules/{MOD}/assets/art/portraits/{_tart_slug(doc['name'])}.webp"
    tex = (doc.get("prototypeToken") or {}).get("texture")
    if tex is not None:
        tex["src"] = token_art(doc["name"])
    return doc

# ---------- writers ----------
def write(pack, slug, doc, embed_items=False, embed_pages=False):
    d = PACKS / pack / "_source"
    d.mkdir(parents=True, exist_ok=True)
    doc = _community_swap(pack, doc)
    doc = _apply_token_art(pack, doc)
    doc["_key"] = f"!{COLL[pack]}!{doc['_id']}"
    if embed_items:
        for it in doc.get("items", []):
            it["_key"] = f"!actors.items!{doc['_id']}.{it['_id']}"
    if embed_pages:
        for p in doc.get("pages", []):
            p["_key"] = f"!journal.pages!{doc['_id']}.{p['_id']}"
    (d / f"{slug}.json").write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return doc
