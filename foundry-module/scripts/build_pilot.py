#!/usr/bin/env python3
"""Build the Phase-2 pilot (Old Fishery) in Kingmaker-style Foundry structure.

Produces: per-type folders, actors (with prototype tokens), hazards, items, ONE
fat chapter journal ("1. Edge of Anarchy") with section-block pages + @Check/@UUID
enrichers, a scene placeholder with map-note pins -> pages and staged tokens, and
an Adventure bundle that imports the whole tree in one click.

Run: python3 scripts/build_pilot.py   (deterministic; safe to re-run)
"""
from __future__ import annotations
import copy, json, os, re
import pf2e_build as B

# ---- stable IDs (pilot registry; keep links stable) ----
A = {"gaedren":"RKfT6vJ5guinSBjo","yargin":"7uhbgkK2IOZOlJb3","hookshanks":"qH96VshE6CZqfajv",
     "giggles":"mHUhxeaalWkTU1h4","drainspider":"1M94tm3wnSRGcTG5","jigsawshark":"lsdWSvGJ81hDy4it",
     "orphan":"UQr3ApF78GW7eghw","boardwalk":"6y55S5DpXqnF40WL","rottendeck":"xMhIQZS6GokTsulZ",
     "brooch":"iNQaVcbkSM0VPXsa","harrowdeck":"DPDen8gco6rznX9Y","ledger":"I7HQNtjI9yPvQ4fA",
     "garnet":"dK4hnpH7s67RYnNI","coffer":"ymuRwMg6WfWIwkne","dagger":"b04PLWVkmm3RM4nm"}
JID = "aO3z6QTqmYZCZYkw"   # the fat Ch.1 journal entry
SCN = "PuUGEVunRqjIWFOj"   # Old Fishery scene
ADV = "OmdAPBg10luB7GUr"   # Adventure doc
MC = {"crocodile":"2rMLYkUR47ZCQMUg","guarddog":"KHTYbQgR5hnFZdGL"}
TOK = lambda slug: f"modules/cotct-pf2e-conversion/assets/tokens/{slug}.webp"

ids = B._idgen(424242)           # folders, pages, notes, tokens
def nid(): return next(ids)
sids = B._idgen(987654)          # GM-secret block ids (separate stream; doesn't perturb the pool)
def sid(): return next(sids)

# UUID link helpers (bare world-UUIDs intra-adventure; Compendium for SRD)
MODID = "cotct-pf2e-conversion"
# Compendium UUIDs (resolve when the journal is read straight from the compendium,
# AND after an Adventure import — bare world-UUIDs only resolve post-import).
def act(k,label): return f"@UUID[Compendium.{MODID}.cotct-actors.Actor.{A[k]}]{{{label}}}"
def haz(k,label): return f"@UUID[Compendium.{MODID}.cotct-hazards.Actor.{A[k]}]{{{label}}}"
def itm(k,label): return f"@UUID[Compendium.{MODID}.cotct-items.Item.{A[k]}]{{{label}}}"
def scn(sid,label): return f"@UUID[Compendium.{MODID}.cotct-scenes.Scene.{sid}]{{{label}}}"
def mc(k,label): return f"@UUID[Compendium.pf2e.pathfinder-monster-core.Actor.{MC[k]}]{{{label}}}"
def pg(pid,label): return f"@UUID[.{pid}]{{{label}}}"          # same-entry page jump
def chk(s): return f"@Check[{s}]"

# ---------------------------------------------------------------------------
# Verbatim read-aloud: the GM reads the boxed text exactly as written. We do NOT
# hardcode that text here (it's the GM's own legally-owned source); instead the
# build reads the AP markdown the GM supplies locally and pulls each area's
# read-aloud paragraph by a short start-anchor. If the file is absent, each
# box() falls back to an original paraphrase, so the build still works anywhere.
# Whitespace is normalised per paragraph to absorb OCR quirks.
# ---------------------------------------------------------------------------
SRC_MD = os.environ.get("COTCT_AP_MD",
    "/mnt/c/Users/maman/Downloads/Curse of the Crimson Throne AP.md")
_PARAS = None
def _paras():
    global _PARAS
    if _PARAS is None:
        try: raw = open(SRC_MD, encoding="utf-8").read()
        except OSError: raw = ""
        _PARAS = [" ".join(p.split()) for p in re.split(r"\n\s*\n", raw)]
    return _PARAS
def verbatim(anchor):
    a = " ".join(anchor.split())
    if not a: return ""
    paras = _paras()
    si = next((k for k, p in enumerate(paras) if p.startswith(a)), None)
    if si is None:
        si = next((k for k, p in enumerate(paras) if a in p), None)
    if si is None: return ""
    text, k = paras[si], si + 1
    # re-flow a box the two-column OCR split mid-sentence (text doesn't end on
    # sentence punctuation) by appending following paragraphs until it completes
    while text and text[-1] not in '.!?:"”)' and k < len(paras):
        nxt = paras[k]
        if not nxt or nxt.startswith(("<!--", "#")): break
        text, k = text + " " + nxt, k + 1
    return text
# start-anchors (short identifying snippets) for each area's boxed read-aloud
RABOX = {
 "A1":"The reek of brine and the stink of week-dead fish",
 "A2":"A fifteen-foot-wide loading dock abuts",
 "A3":"A slippery boardwalk clings to the side of the fishery",
 "A4":"A single desk sits in the middle of this room",
 "A5":"A pair of bunk beds sit against the far wall",
 "A6":"A wooden desk sits in one corner of this room",
 "A7":"The stink in this room, a mixture of fish and sweat",
 "A8":"The floor here is slick with river water",
 "A9":"The rotten deck of this ancient sailing ship",
 "A10":"The air in this room is thick and musty",
 "A11":"Dark and dank, the ship's hold smells of mildew",
 "A12":"A narrow space exists under the fishery",
 "A13":"The air in this large room is chilly and stinks of the river",
 "A14":"This foul-smelling room seems to be a combination",
}
def box(code, fallback_html):
    """Read-aloud section: exact AP text if the source file is present, else paraphrase."""
    t = verbatim(RABOX.get(code, ""))
    return B.s_read(f"<p>{t}</p>") if t else B.s_read(fallback_html)

def _tc(s):  # title-case that respects apostrophes ("ZELLARA'S HOME" -> "Zellara's Home")
    return re.sub(r"[A-Za-z][A-Za-z']*", lambda m: m.group(0)[0].upper()+m.group(0)[1:].lower(), s)

# Convert PF1e DC references that appear inside the verbatim source prose into
# PF2e @Check enrichers (clickable). PF1e skills/saves -> PF2e equivalents; DCs
# re-judged to PF2e, not transliterated. Extend as new chapters surface more.
_DCFIX = [
    (r"a successful DC\s*12\s*Knowledge \(local\) check", "a successful @Check[type:society|dc:12] check"),
    (r"a DC\s*25\s*Will save",                            "a @Check[type:will|dc:18|basic:false] save"),
]
def dcfix(html):
    for pat, rep in _DCFIX:
        html = re.sub(pat, rep, html)
    return html

# Player-handout sidebar text the two-column OCR fused into the GM narrative
# (start-phrase, end-phrase). Pulled out of the prose so it stops splitting
# sentences, then re-emitted as its own read-aloud block.
_HANDOUTS = [
    ("I know what Gaedren has done to you", "justice must be done."),
    ("Thank you for coming. I had to step out", "drink for you."),
]

def apspan(start, stop):
    """Verbatim MULTI-paragraph extract from the GM's AP source: from the paragraph
    containing `start` up to (not including) the one containing `stop`. Cleans the
    OCR/layout noise (image & page markers, stray page numbers, all-caps captions,
    leading drop-caps), keeps sub-headings as bold leads. Empty if the file is absent."""
    paras = _paras()
    si = next((k for k, p in enumerate(paras) if start in p), None)
    if si is None: return ""
    ei = next((k for k, p in enumerate(paras) if k > si and stop in p), len(paras))
    items = []  # ("sub"|"body", text)
    for p in paras[si:ei]:
        if not p or p.startswith("<!--"): continue           # image / page markers
        if p.startswith("#"):                                # surviving heading -> bold lead
            t = p.lstrip("# ").strip()
            if t: items.append(("sub", _tc(t)))
            continue
        if re.fullmatch(r"\d+", p): continue                 # stray page numbers
        if p.isupper() and len(p.split()) <= 4: continue     # captions ("QUEEN ILEOSA")
        p = re.sub(r"^([A-Z]) ([a-z])", r"\1\2", p)          # drop-cap "T he" -> "The"
        items.append(("body", p))
    # Pull handout sidebar text the OCR fused into the GM narrative, so it stops
    # splitting sentences; collect it to re-emit as its own block afterwards.
    handouts, cleaned = [], []
    for kind, txt in items:
        if kind != "body":
            cleaned.append((kind, txt)); continue
        for hs, he in _HANDOUTS:
            i = txt.find(hs)
            if i >= 0:
                j = txt.find(he, i)
                j = j + len(he) if j >= 0 else len(txt)
                handouts.append(txt[i:j].strip())
                txt = (txt[:i] + " " + txt[j:]).strip()
        if txt:
            cleaned.append(("body", txt))
    # Re-flow paragraphs the two-column OCR split: join the next body block when
    # the previous doesn't end on sentence punctuation OR the next starts lower-case
    # (a clear continuation of the prior sentence).
    merged = []
    for kind, txt in cleaned:
        if (kind == "body" and merged and merged[-1][0] == "body"
                and (merged[-1][1][-1] not in '.!?:"”)' or txt[:1].islower())):
            merged[-1] = ("body", merged[-1][1] + " " + txt)
        else:
            merged.append((kind, txt))
    out = []
    for kind, txt in merged:
        out.append(f'<p class="subhead"><strong>{txt}</strong></p>' if kind == "sub" else f"<p>{dcfix(txt)}</p>")
    for h in handouts:                                    # handouts as read-aloud boxes
        out.append(B.s_read(f'<p class="subhead"><strong>Player Handout</strong></p><p>{dcfix(h)}</p>'))
    return "".join(out)

# =====================================================================
# FOLDERS (one tree per document type; Kingmaker palette)
# =====================================================================
F = {k: nid() for k in ["a_root","a_ch1","a_creatures","a_hazards","i_root","i_ch1","i_treasure",
                        "j_root","j_adventure","s_root","s_ch1"]}
ROOTC, CHC, SUPC = "#5a0b0b", "#8a1a1a", "#b3541e"   # crimson theme: root / chapter / supplemental
folders = [
 B.folder(F["a_root"],"Curse of the Crimson Throne","Actor",None,100000,ROOTC),
 B.folder(F["a_ch1"],"1. Edge of Anarchy","Actor",F["a_root"],100000,CHC),
 B.folder(F["a_creatures"],"Creatures","Actor",F["a_ch1"],100000,None,"a"),
 B.folder(F["a_hazards"],"Hazards","Actor",F["a_ch1"],200000,None,"a"),
 B.folder(F["i_root"],"Curse of the Crimson Throne","Item",None,100000,ROOTC),
 B.folder(F["i_ch1"],"1. Edge of Anarchy","Item",F["i_root"],100000,CHC),
 B.folder(F["i_treasure"],"Treasure","Item",F["i_ch1"],100000,None,"a"),
 B.folder(F["j_root"],"Curse of the Crimson Throne","JournalEntry",None,100000,ROOTC),
 B.folder(F["j_adventure"],"Adventure","JournalEntry",F["j_root"],100000,SUPC),
 B.folder(F["s_root"],"Curse of the Crimson Throne","Scene",None,100000,ROOTC),
 B.folder(F["s_ch1"],"1. Edge of Anarchy","Scene",F["s_root"],100000,CHC),
]
# folders live in each relevant per-type pack
for f in folders:
    pack = {"Actor":"actors","Item":"items","JournalEntry":"journals","Scene":"scenes"}[f["type"]]
    # hazards pack mirrors the actor hazard folder too
    B.write(pack, "_folder_"+f["name"].lower().replace(" ","-").replace(".","")+"-"+f["type"][:3].lower(), copy.deepcopy(f))
# (hazards pack stays flat — the Actor folder tree organizes them in the Adventure import)

# =====================================================================
# ACTORS (ported stats + prototype tokens + folders)
# =====================================================================
actors = []
def AW(slug, doc):
    actors.append(copy.deepcopy(doc)); B.write("actors", slug, doc, embed_items=True)

AW("gaedren-lamm", B.npc(A["gaedren"],"Gaedren Lamm",2,17,30,3,9,8,8,
  {"str":-1,"dex":4,"con":0,"int":3,"wis":2,"cha":3},15,
  {"deception":10,"stealth":9,"thievery":9,"intimidation":8,"society":6,"acrobatics":9},
  ["humanoid","human"],["Common","Dwarven","Gnomish","Goblin","Halfling","Infernal","Orcish","Shoanti","Varisian"],
  [B.strike(nid(),"Fine Dagger",9,"1d4+1","piercing",["agile","finesse","versatile-s"]),
   B.strike(nid(),"Hand Crossbow",9,"1d6","piercing",["range-increment-60","reload-1"]),
   B.sneak_attack(nid(),1,"Gaedren"),
   B.action(nid(),"Nimble Dodge","reaction","<p><strong>Trigger</strong> A creature he can see attacks him.</p><hr /><p><strong>Effect</strong> +2 circumstance bonus to AC against that attack.</p>",["mental"],"defensive"),
   B.action(nid(),"Spur the Beast","1","<p>Gaedren makes a Hand Crossbow Strike against Gobblegut; on a hit, the enraged crocodile gains a +2 status bonus to attack and damage rolls until the end of its next turn and must use a single action to Strike the nearest creature other than Gaedren on its next turn.</p>",["concentrate"]),
   B.lore(nid(),"Underworld Lore",8),
   B.gear("hand-crossbow",nid()), B.gear("dagger",nid()), B.gear("padded-armor",nid())],
  notes="<p><strong>Role:</strong> the AP's first villain and every PC's revenge payoff — a frail catalyst, not a tank. The real threat is the crocodile; Gaedren weaponizes it.</p>"
        "<p><strong>Tactics:</strong> an old leg wound caps his Speed at 15 ft, so he holds the far side of the gator pool and snipes rather than kiting. Round 1 <em>Spur the Beast</em> to enrage Gobblegut, then Strikes from cover; <em>Nimble Dodge</em> when focus-fired; flees to the A12 skiffs at &le;8 HP.</p>"
        "<p><strong>If killed and left in A14,</strong> his son Rolth animates the body in the Dead Warrens at the chapter's end — track it.</p>",
  folder=F["a_creatures"], blurb="Decrepit crime lord; first villain of the AP", token_src=TOK("gaedren-lamm"), actor_link=True))

AW("yargin-balko", B.npc(A["yargin"],"Yargin Balko",1,16,20,5,5,7,6,
  {"str":1,"dex":2,"con":1,"int":3,"wis":2,"cha":1},25,
  {"crafting":7,"society":6,"deception":5,"thievery":5,"intimidation":6,"arcana":6},
  ["humanoid","human"],["Common","Gnomish","Varisian"],
  [B.strike(nid(),"Acid Flask",7,"1","acid",["range-increment-20","splash","alchemical","bomb"],[("1d6","acid","persistent"),("1","acid","splash")]),
   B.strike(nid(),"Thunderstone",7,"1d4","sonic",["range-increment-20","splash","alchemical","bomb"],[("1","sonic","splash")]),
   B.strike(nid(),"Light Crossbow",5,"1d8","piercing",["range-increment-60","reload-1"]),
   B.strike(nid(),"Dagger",5,"1d4+1","piercing",["agile","finesse","versatile-s"]),
   B.action(nid(),"Quick Acid","1","<p>Yargin Interacts to draw an "+B.isrd("acid-flask-lesser","Acid Flask (Lesser)")+", then Strikes with it.</p>",["alchemical"]),
   B.lore(nid(),"Alchemy Lore",7),
   B.gear("acid-flask-lesser",nid(),3), B.gear("thunderstone-lesser",nid(),1),
   B.gear("crossbow",nid()), B.gear("dagger",nid()), B.gear("leather-armor",nid()),
   B.equipment(nid(),"Scroll of Acidic Burst",1,4,"<p>A spell scroll holding a 1st-rank burst of acid (his PF1e wand of acid splash, re-cast as a scroll). Yargin is no spellcaster, so he must Trick the scroll ("+chk("type:arcana|dc:15")+", Trick Magic Item); on a success he spends 2 actions to Cast it, dealing @Damage[2d6[acid]] in a 10-foot burst ("+chk("type:reflex|dc:18|basic:true")+").</p>",traits=["scroll","magical","acid","consumable"])],
  notes="<p><strong>Role:</strong> Gaedren's fence; answers the front door, fights from A6. Opens with thrown Acid Flasks, falls back to crossbow. <strong>Flees down the hidden trapdoor to warn Gaedren if losing.</strong> Carries the brass key (all fishery doors).</p>",
  folder=F["a_creatures"], blurb="Bitter alchemist-fence; Gaedren's right hand", token_src=TOK("yargin-balko")))

AW("hookshanks-gruller", B.npc(A["hookshanks"],"Hookshanks Gruller",1,16,18,4,7,5,5,
  {"str":0,"dex":4,"con":1,"int":1,"wis":1,"cha":2},25,
  {"stealth":9,"deception":8,"thievery":7,"acrobatics":7,"society":4,"intimidation":5},
  ["humanoid","gnome"],["Common","Gnomish"],
  [B.strike(nid(),"Kukri",7,"1d6+1","slashing",["agile","finesse","trip"]),
   B.strike(nid(),"Dagger",7,"1d4+1","piercing",["agile","finesse","thrown-10","versatile-s"]),
   B.sneak_attack(nid(),1,"Hookshanks"),
   B.action(nid(),"Disguised as an Orphan","passive","<p>Passes as one of Lamm's Lambs; "+chk("type:perception|dc:17")+" against his Deception DC to spot him before he Sneak Attacks.</p>"),
   B.lore(nid(),"Streetwise Lore",6),
   B.gear("kukri",nid()), B.gear("dagger",nid()), B.gear("studded-leather",nid())],
  notes="<p><strong>Role:</strong> gnome taskmaster over the orphans in A7; dresses as one of them and hides in their midst.</p>"
        "<p><strong>Behavior:</strong> orders the orphans to attack and opens the A4 door to loose Bloo. At less than half HP he surrenders and tells the PCs everything he knows about the fishery and Gaedren's routine — except what lies in the den (A14).</p>",
  folder=F["a_creatures"], size="sml", senses=[{"type":"low-light-vision"}], blurb="Gnome taskmaster who hides among the orphans", token_src=TOK("hookshanks-gruller")))

AW("giggles", B.npc(A["giggles"],"Giggles",1,16,24,7,5,3,5,
  {"str":3,"dex":1,"con":3,"int":0,"wis":1,"cha":0},25,
  {"athletics":7,"intimidation":5},["humanoid","orc","human"],["Common","Orcish"],
  [B.strike(nid(),"Flail",7,"1d6+5","bludgeoning",["sweep","trip"],slug="flail"),
   B.strike(nid(),"Fist",7,"1d4+5","bludgeoning",["agile","nonlethal","unarmed"]),
   B.strike(nid(),"Composite Longbow",5,"1d6+3","piercing",["range-increment-100","deadly-d10","propulsive"]),
   B.action(nid(),"Bludgeoner","passive","<p>Giggles can deal nonlethal damage with his Flail without taking a penalty, and gains a +1 circumstance bonus to the attack roll when he does so.</p>",rules=[
     {"key":"RollOption","domain":"all","option":"bludgeoner","toggleable":True},
     {"key":"AdjustStrike","mode":"add","property":"weapon-traits","value":"nonlethal","definition":["item:slug:flail"],"predicate":["bludgeoner"]},
     {"key":"FlatModifier","selector":"flail-attack","type":"circumstance","value":1,"predicate":["bludgeoner"]}]),
   B.action(nid(),"Orc Ferocity","reaction","<p><strong>Trigger</strong> Giggles is reduced to 0 HP.</p><hr /><p><strong>Effect</strong> He stays at 1 HP and becomes "+B.cond("wounded","Wounded 1")+" (or increases his wounded value by 1). Once per day.</p>"),
   B.lore(nid(),"Brawling Lore",5),
   B.gear("healing-potion-minor",nid(),3),
   B.gear("flail",nid()), B.gear("composite-longbow",nid()), B.gear("chain-mail",nid())],
  notes="<p><strong>Role:</strong> muscle on the main floor (A8); tries to <strong>capture</strong> PCs nonlethally for Gaedren, then fights to the death. Carries 3 "+B.isrd("healing-potion-minor","Minor Healing Potions")+".</p>",
  folder=F["a_creatures"], senses=[{"type":"low-light-vision"}], blurb="Half-orc brute; the fishery's muscle", token_src=TOK("giggles")))

AW("drain-spider", B.npc(A["drainspider"],"Drain Spider",-1,15,8,3,6,2,5,
  {"str":-2,"dex":4,"con":1,"int":-5,"wis":1,"cha":-4},25,
  {"stealth":6,"athletics":3},["animal"],[],
  [B.strike(nid(),"Fangs",7,"1d4","piercing",["finesse"],[("1d4","poison")]),
   B.action(nid(),"Drain Spider Venom","passive","<p><strong>Saving Throw</strong> "+chk("type:fortitude|dc:15")+"; <strong>Maximum Duration</strong> 6 rounds; <strong>Stage 1</strong> 1d4 poison damage and "+B.cond("enfeebled","Enfeebled 1")+" (1 round).</p>",["poison"]),
   B.action(nid(),"Web Trap","1","<p>The drain spider makes a ranged web Strike (attack +7, range increment 10 feet) against one creature. On a hit, the target is "+B.cond("immobilized","Immobilized")+" — stuck to the nearest surface until it Escapes ("+chk("type:athletics|dc:15")+" or "+chk("type:acrobatics|dc:15")+") — and is exposed to Drain Spider Venom.</p>",["attack"])],
  notes="<p>Cat-sized vermin nesting in the wreck — 1 in A10, 4 in A11. It lunges at the first creature to enter its lair (off-guard to the surprised target).</p>"
        "<p>A creature smelling of the vermin repellent looted in A13 auto-repels them, trivializing the A11 nest.</p>",
  folder=F["a_creatures"], senses=[{"type":"darkvision"},{"acuity":"imprecise","type":"tremorsense","range":60}],
  other_speeds=[{"type":"climb","value":25}], size="tiny", blurb="Aggressive venomous spider", token_src=TOK("drain-spider")))

AW("jigsaw-shark", B.npc(A["jigsawshark"],"Jigsaw Shark",1,16,20,7,6,3,7,
  {"str":3,"dex":2,"con":2,"int":-4,"wis":2,"cha":-2},5,
  {"athletics":8},["animal","aquatic"],[],
  [B.strike(nid(),"Jaws",8,"1d8+3","piercing",["deadly-d8"]),
   B.action(nid(),"Aquatic Ambush","1","<p>While hidden in water, the shark Swims up to its Speed and makes a Jaws Strike; the target is "+B.cond("off-guard","Off-Guard")+" to it.</p>")],
  notes="<p>Scavenger beneath the fishery; avoidable if the PCs stay dry. It attacks anything that falls into the water, but only leaps onto the underpier (A12) if it is first attacked and damaged. The boardwalk and rotten-deck hazards exist to feed it.</p>",
  folder=F["a_creatures"], senses=[{"acuity":"imprecise","type":"scent","range":30}],
  other_speeds=[{"type":"swim","value":35}], blurb="River shark beneath the fishery", token_src=TOK("jigsaw-shark")))

AW("lamms-lamb", B.npc(A["orphan"],"Lamm's Lamb (Orphan)",-1,15,6,2,6,3,5,
  {"str":-2,"dex":3,"con":0,"int":0,"wis":-1,"cha":0},25,
  {"acrobatics":7,"thievery":7,"stealth":6},["humanoid","human"],["Common"],
  [B.strike(nid(),"Pitchfork (improvised)",5,"1d6-1","piercing",["reach","improvised"]),
   B.gear("dagger",nid())],
  notes="<p>Enslaved child pickpockets — 9 toiling by day across A7/A8, all 26 asleep in A8 at night. <strong>The moral core of the dungeon, and never an XP-for-kill source.</strong></p>"
        "<p><strong>Behavior:</strong> an orphan that takes damage flees to A8, or out into the slums once the thugs are down; those invaded at night are too frightened to fight. A PC can rally one with "+chk("type:diplomacy|dc:15")+" (Intimidation fails) to Aid or reveal information. Rescuing them pays off a 'Missing Child' background.</p>",
  folder=F["a_creatures"], size="sml", blurb="Enslaved orphan ('Lamm's Lamb')", token_src=TOK("orphan")))

# =====================================================================
# HAZARDS (Actor type=hazard; in the hazards pack, Hazards folder)
# =====================================================================
hazards = []
def HW(slug, doc):
    hazards.append(copy.deepcopy(doc)); B.write("hazards", slug, doc, embed_items=True)

HW("slippery-boardwalk", B.hazard(A["boardwalk"],"Slippery Boardwalk",1,0,
  "<p>Obvious — no check needed to notice.</p>",
  "<p>"+chk("type:acrobatics|dc:15")+" to cross carefully, or brace a stretch ("+chk("type:crafting|dc:15")+").</p>",
  "<p>A barnacle-slick boardwalk (A3) 13 ft above shark water; the planks also groan under heavy loads.</p>",
  [B.action(nid(),"Slip","reaction","<p><strong>Trigger</strong> A creature Strides &gt;5 ft or fights on it.</p><hr /><p><strong>Effect</strong> "+chk("type:reflex|dc:15")+" or fall "+B.cond("prone","Prone")+"; on a critical failure, slide off and fall 13 ft into the river and the Jigsaw Shark's water (A12) — the water is deep enough and the fall short enough that the creature takes no falling damage.</p>")],
  folder=F["a_hazards"], traits=["environmental"], reset="<p>Persistent terrain.</p>"))

HW("rotten-ship-deck", B.hazard(A["rottendeck"],"Rotten Ship Deck",1,16,
  "<p>"+chk("type:perception|dc:16")+" to spot the unsafe foredeck first.</p>",
  "<p>"+chk("type:crafting|dc:16")+" to shore up a path, or keep to the sound stern.</p>",
  "<p>The derelict Kraken's Folly (A9) has a rotten foredeck; only the stern holds weight.</p>",
  [B.action(nid(),"Collapse","reaction","<p><strong>Trigger</strong> A Medium+ creature moves onto the foredeck toward the bow.</p><hr /><p><strong>Effect</strong> "+chk("type:reflex|dc:16|basic:true")+" or crash to the hold (A11) for @Damage[1d6[bludgeoning]] and land "+B.cond("prone","Prone")+" among the drain spiders.</p>")],
  folder=F["a_hazards"], traits=["environmental"], reset="<p>Once collapsed, that stretch is gone.</p>"))

# =====================================================================
# ITEMS (Treasure folder)
# =====================================================================
items = []
def IW(slug, doc):
    items.append(copy.deepcopy(doc)); B.write("items", slug, doc)

IW("queen-ileosas-brooch", B.equipment(A["brooch"],"Queen Ileosa's Brooch",0,25,
  "<p><strong>Story item.</strong> A gold filigree house-drake brooch (broken clasp) from Gaedren's strongbox (A14); Queen Ileosa's. Returning it earns an audience with the queen and launches the rest of Chapter 1. <em>Loot value trivial; narrative value high — don't let players sell it for level-breaking gold.</em></p>",
  traits=["art-object"], rarity="unique", folder=F["i_treasure"]))
IW("zellaras-harrow-deck", B.equipment(A["harrowdeck"],"Zellara's Harrow Deck",1,0,
  "<p><strong>Story item — the Harrow subsystem anchor (CHG-0010).</strong> Inhabited by the spirit of the murdered fortune-teller Zellara; recovered in A14. Anchors the recurring Harrowing (hero-point-style suit boons). Becomes the Harrow Deck of Many Things in Ch.6.</p>",
  traits=["magical","divination"], rarity="unique", folder=F["i_treasure"]))
IW("gaedrens-coded-ledger", B.equipment(A["ledger"],"Gaedren's Coded Ledger",0,0,
  "<p><strong>Quest item.</strong> Records Gaedren's crimes in a Varisian cipher. "+chk("type:society|dc:17")+" (must read Varisian) to decode. Guard bounty: 15 gp (30 gp with the cipher key). Unlocks the 'Framed' background payoff.</p>",
  traits=["evidence"], rarity="unique", folder=F["i_treasure"]))
IW("garnet-amulet", B.equipment(A["garnet"],"Garnet Amulet",0,8,
  "<p>A cheap garnet amulet (Yargin). Converted treasure: ~8 gp gem (PF1e 100 gp, re-scaled).</p>",
  traits=["art-object"], folder=F["i_treasure"]))
IW("coffer-of-shiver", B.equipment(A["coffer"],"Darkwood Coffer of Shiver",1,12,
  "<p>A darkwood coffer (~10 gp) from A13 holding 20 doses of <strong>shiver</strong> and 7 applications of <em>vermin repellent</em> (drives off the A10/A11 drain spiders). Shiver is a story drug, not loot; destroying it pays off a 'Drug Addict' background hook.</p>",
  traits=["alchemical"], rarity="uncommon", folder=F["i_treasure"]))
IW("plus-one-dagger", {"_id":A["dagger"],"img":"systems/pf2e/icons/equipment/weapons/dagger.webp",
  "name":"+1 Dagger (Gaedren's)","type":"weapon","folder":F["i_treasure"],"sort":0,"ownership":{"default":0},
  "flags":{},"_stats":dict(B.STATS),
  "system":{"baseItem":"dagger","bonus":{"value":0},"bonusDamage":{"value":0},"bulk":{"value":0.1},
    "category":"simple","containerId":None,"damage":{"damageType":"piercing","dice":1,"die":"d4"},
    "description":{"value":"<p>Gaedren's prized magical dagger — the boss's signature loot and a fitting first permanent magic weapon for a level 1-2 party. (His PF1e '+1 padded armor' similarly converts to a minor armor reward — see the Treasure page.)</p>"},
    "equipped":{"carryType":"worn","handsHeld":0,"invested":None},"group":"knife","hardness":0,"hp":{"max":0,"value":0},
    "level":{"value":2},"material":{"grade":None,"type":None},"price":{"value":{"gp":35}},"publication":B.PUB,
    "quantity":1,"range":None,"reload":{"value":None},"rules":[],"runes":{"potency":1,"property":[],"striking":0},
    "size":"med","slug":None,"splashDamage":{"value":0},
    "traits":{"rarity":"common","value":["agile","finesse","magical","thrown-10","versatile-s"]},
    "usage":{"value":"held-in-one-hand"}}})

# =====================================================================
# JOURNAL — one fat "1. Edge of Anarchy" entry, Kingmaker page model
# =====================================================================
SR = lambda area,p: f'<p class="source"><em>Source: CotCT (2016 HC), Ch.1, {area} — p.{p}.</em></p>'
def RA(html): return B.s_read(html)                      # read-aloud / boxed text
def SEC(html): return B.s_secret(html, sid())            # GM-hidden reveal block
PAGE_KEYS=["background","overview","hook","scene","features","A1","A2","A3","A4","A5","A6","A7","A8","A9","A10",
           "A11","A12","A13","A14","npcs","treasure","conv"]
P={k:nid() for k in PAGE_KEYS}   # pre-assign so forward relative links resolve
def newpage(key,name,html,level=3):
    return B.page(P[key],name,html,level=level)

pages=[]
# 0. Chapter Background --------------------------------------------------------
_bg = apspan("he city of Korvosa was founded in 4407", "HAUNTED FORTUNES")
_bg_fallback = "<p><strong>For the GM.</strong> Korvosa was raised atop a site the Shoanti guarded — beneath Castle Korvosa lie the fangs of Kazavon, a long-dead dragon-tyrant whose evil the city never suspected. Aging King Eodred II rules without an heir; his young queen Ileosa was corrupted by the fangs and has secretly engineered his murder (a Red Mantis poison via his half-brother Venster), silenced the seneschal Neolandus, and allied with the Red Mantis and the cult of Urgathoa. As the chapter opens the king is days from death and the city teeters on anarchy.</p>"
pages.append(newpage("background","Chapter Background",
  (_bg or _bg_fallback)
  +B.s_milestone("<p><strong>Advancement (milestone — CHG-0007):</strong> begin at 1st level · reach <strong>2nd</strong> after the Old Fishery · 3rd before Eel's End · 4th before the Dead Warrens · well into 4th by the chapter's end.</p>"),
  level=1))
# 1. Overview & Run Sheet ------------------------------------------------------
pages.append(newpage("overview","Overview",
  RA("<p>A harrow card finds its way to each of you — and a hand-inked message naming a man you each have cause to hate: <strong>Gaedren Lamm</strong>. The fortune-teller Zellara knows where he dens, and asks you to end him.</p>")
  +"<p>Zellara's reading (see "+pg(P["hook"],"Haunted Fortunes")+") draws the party together and points them at the <strong>Old Fishery</strong>, where crime-lord Gaedren Lamm hides with his thugs, his pet crocodile "+mc("crocodile","Gobblegut")+", and a workforce of enslaved orphans. In his den the PCs recover "+itm("brooch","Queen Ileosa's stolen brooch")+", "+itm("ledger","Gaedren's coded ledger")+", and "+itm("harrowdeck","Zellara's haunted harrow deck")+" — and as they step back into the street, the king dies and Korvosa erupts into the riots of <em>A City Gone Mad</em>.</p>"
  +B.s_milestone("<p><strong>Advancement:</strong> the party should reach <strong>2nd level</strong> after dealing with Gaedren. Milestone leveling (CHG-0007).</p>")
  +"<p><strong>Party:</strong> 4 PCs, level 1 → 2. <strong>System:</strong> PF2e Remaster (Foundry v14 / pf2e 8.2.0).</p>"
  +"<p><strong>Run it like Gotham.</strong> Tell players up front that Gaedren is a <em>connector</em>, not a campaign villain — this defuses the classic 'Lamm is a Lamb' let-down. By <strong>day</strong> 9 orphans toil, the thugs patrol, and the A7 doors stand open; by <strong>night</strong> every door locks, 26 orphans sleep in "+pg(P["A8"],"A8")+", and "+mc("guarddog","Bloo")+" prowls as a living alarm. The orphans are non-combatants — rescuing them is the heart of the dungeon.</p>"
  +SEC("<p><strong>The twist the players don't have yet:</strong> Zellara is already dead. Gaedren murdered her and fed her to Gobblegut; her spirit haunts her stolen deck. The PCs only learn this when they find her head in "+pg(P["A14"],"A14")+" — so play her in the intro as a warm, desperate ally, not a mystery.</p>"),level=1))

# 2. Haunted Fortunes — the hook ----------------------------------------------
_hf = apspan("Curse of the Crimson Throne provides the PCs with a shared nemesis", "OLD FISHERY")
_hf_fallback = "<p>A harrow card reaches each PC, naming Gaedren Lamm and an address — 3 Lancet Street. There the fortune-teller Zellara gathers them, recounts how Gaedren's thugs murdered her son over her stolen harrow deck, and asks them to bring him to justice; she performs a harrowing to prepare them. Zellara is in fact a haunt — already dead — though the PCs need not learn this until they find her head in Gaedren's den.</p>"
pages.append(newpage("hook","Haunted Fortunes",
  SR("Part 1: Haunted Fortunes","14-16")
  +(_hf or _hf_fallback)
  +B.s_skill("<p><strong>First Harrowing → PF2e (CHG-0010).</strong> Run the reading as foreshadowing (a coming time of unrest; the PCs are fated heroes), then grant each PC a small pool of <strong>hero-point-style suit boons</strong> via "+itm("harrowdeck","Zellara's deck")+" — the recurring subsystem from here on. The illusions in her home are "+chk("type:will|dc:18")+" to disbelieve.</p>")
  ,level=2))

# 3. Scene Setup ---------------------------------------------------------------
pages.append(newpage("scene","Scene Setup",
  "<p><strong>No maps are shipped</strong> (copyright). Open the "+scn(SCN,"Old Fishery scene")+" — its map-note pins already link to each area page below, and its tokens reference the converted actors.</p>"
  +"<p>Drop in a battlemap (Racooze's free CotCT set, or your own at <code>assets/maps/01-old-fishery.webp</code>), then nudge the pins and tokens onto it — positions are staged in a grid for now (<strong>NEEDS GM REVIEW</strong>); the <em>links</em> are already correct. Drag "+mc("crocodile","Crocodile")+" (rename 'Gobblegut') into "+pg(P["A13"],"A13")+" and "+mc("guarddog","Guard Dog")+" ('Bloo') into "+pg(P["A4"],"A4")+"/"+pg(P["A8"],"A8")+" from the pf2e Monster Core compendium.</p>"
  +SEC("<p>The fishery is two map levels — an upper floor (A1–A9) and the waterline understructure (A10–A14). When you add the real map, split this into two scenes and re-pin; the area pages are already ordered for that split.</p>"),level=2))

# 4. Fishery Features ----------------------------------------------------------
pages.append(newpage("features","Fishery Features",
  SR("A. Old Fishery","17")
  +RA("<p>A creaking, mold-mottled building of boarded windows and solid old doors, perched on pilings over the Jeggare River. It still renders 'dock-dumpling' slurry from spoiled fish — a cover for the crime-lord who dens beneath it.</p>")
  +"<p>The fishery sits on a 13-ft embankment ("+chk("type:athletics|dc:15")+" to climb the slick bank). Doors are hardness 5 / 10 HP ("+chk("type:thievery|dc:15")+" to pick, or "+chk("type:athletics|dc:15")+" to force); Yargin's brass key opens them all. Standing hazards: the "+haz("boardwalk","Slippery Boardwalk")+" ("+pg(P["A3"],"A3")+") and the "+haz("rottendeck","Rotten Ship Deck")+" ("+pg(P["A9"],"A9")+") — either can dump a PC into "+act("jigsawshark","the shark's")+" water ("+pg(P["A12"],"A12")+").</p>"
  +"<p><strong>Day vs. night.</strong> The encounters assume a daytime raid (9 orphans working, thugs at their posts). At night every door is locked, Yargin sleeps in "+pg(P["A5"],"A5")+", Giggles and Hookshanks run roving patrols (≈9pm / midnight / 3am), and "+mc("guarddog","Bloo")+" wanders "+pg(P["A8"],"A8")+" — his bark wakes the whole building.</p>"
  +B.s_skill("<p><strong>The orphans ('Lamm's Lambs').</strong> 9 work the fishery by day; all 26 sleep in "+pg(P["A8"],"A8")+" at night. Rally them with "+chk("type:diplomacy|dc:15")+" (Intimidation fails — they're inured to it); won over, they feed information or lend a hand. They know nothing past "+pg(P["A9"],"A9")+" — those sent below never return.</p>")
  +SEC("<p>They are <strong>non-combatants and never an XP-for-kill source</strong> (CHG-0107). Invaded at night they're too frightened to fight and flee into the slums once the thugs fall. Treat a rescued orphan as a 'Missing Child' background payoff, not a stat block.</p>"),level=2))

# Area pages A1-A14 ------------------------------------------------------------
def area(code,name,page_html): pages.append(newpage(code,f"{code}. {name}",page_html))

area("A1","Front Door", SR("A1","18")
  +box("A1","<p>Weathered double doors stand shut in the fishery's flank, a broken signboard swinging from a length of rusted chain above them. Brine and the stink of week-dead fish hang thick in the air.</p>")
  +"<p>The main doors are locked ("+chk("type:thievery|dc:15")+"). Most business runs through "+pg(P["A7"],"A7")+", so a knock — or a noisy attempt on the lock — brings "+act("yargin","Yargin")+" up from "+pg(P["A6"],"A6")+" to answer.</p>")

area("A2","Loading Dock", SR("A2","18")
  +box("A2","<p>A fifteen-foot loading dock juts from the building. Carts wait half-laden with tar-caked barrels, each daubed with a red, fish-shaped splotch. A rickety stair drops to a second door barely three feet above the river.</p>")
  +"<p>By day the doors into "+pg(P["A7"],"A7")+" stand open for the daily slurry shipment; the door to "+pg(P["A8"],"A8")+" is always locked ("+chk("type:thievery|dc:15")+"). The orphans do the heavy hauling under Hookshanks' eye.</p>")

area("A3","Back Alley", SR("A3","18-20")
  +box("A3","<p>A slippery boardwalk clings to the south wall on barnacle-eaten pilings, worn thin below the waterline. It runs about thirteen feet above the river, sloping down toward the derelict ship to the east.</p>")
  +"<p>The "+haz("boardwalk","Slippery Boardwalk")+" hazard: a careful pace is safe, but moving fast or fighting on it risks a fall into "+act("jigsawshark","the shark's")+" water ("+pg(P["A12"],"A12")+"); the planks also groan and give under heavy loads. The door into "+pg(P["A6"],"A6")+" is locked.</p>"
  +SEC("<p>Despite its state, this boardwalk is Gaedren's own private way in and out of his den ("+pg(P["A13"],"A13")+") — he uses it only a few times a month, spending days or weeks below to avoid being seen.</p>"))

area("A4","Front Room", SR("A4","19")
  +box("A4","<p>A single desk and a moldering chair stand in the middle of this disused room. A nest of ratty furs and straw is heaped beneath the desk.</p>")
  +"<p>In theory Yargin meets new customers here — a rarity. Any real noise in this room quickly brings both "+act("yargin","Yargin")+" and "+act("hookshanks","Hookshanks")+" to investigate.</p>"
  +B.enc("Bloo","Trivial · 20 XP",
     "<p>"+mc("guarddog","Bloo")+", Yargin's foul-tempered cur, sleeps under the desk and attacks any unfamiliar scent on sight. While he lives, a thug gets a circumstance bonus to bully the orphans into fighting.</p>"
     +B.s_skill("<p>Silence him fast — "+chk("type:stealth|dc:15")+" to slip past, "+chk("type:nature|dc:15")+" to calm, or a quick kill — before the barking rouses the fishery.</p>"),
     B.aside_token([mc("guarddog","Bloo — Guard Dog (−1)")])))

area("A5","Barracks", SR("A5","20")
  +box("A5","<p>Two sets of bunks flank a boarded-over window. Three are slept-in; the fourth stands bare.</p>")
  +"<p>The thugs — Yargin, Hookshanks, and Giggles — share this room. They distrust one another and keep nothing of value here.</p>")

area("A6","Yargin's Office", SR("A6","19-21")
  +box("A6","<p>A desk wedged into one corner — its bulk blocking the western door — overflows with chalk-scrawled slate boards. A slouching cabinet leans against the east wall.</p>")
  +"<p>The fishery's 'books': slates of transactions and addresses, compiled monthly into scrolls in the cabinet — cover paperwork for any Guard inspection. "+act("yargin","Yargin Balko")+" works here and carries the brass key.</p>"
  +SEC("<p>A floorboard behind the chair is a <strong>hidden, barred trapdoor</strong> ("+chk("type:perception|dc:18")+" to spot; "+chk("type:athletics|dc:17")+" or break to force) dropping straight into the boss's chamber ("+pg(P["A13"],"A13")+"). A meal-pulley rig makes the climb down trivial — a flanking route onto Gaedren that skips the whole lower floor.</p>")
  +B.enc("Yargin Balko","Low · 40 XP",
     "<p>Opens with thrown <strong>Acid Flasks</strong>, then falls back to his crossbow; he's terrified of melee.</p>"
     +SEC("<p><strong>Morale:</strong> at the first melee hit (or once his acid is spent) Yargin panics and flees down the trapdoor to warn Gaedren — and may lead the PCs right onto the boss. If he reaches the den, start the "+pg(P["A13"],"A13")+" fight with Gobblegut already enraged.</p>"),
     B.aside_token([act("yargin","Yargin Balko (1)")], img=TOK("yargin-balko"))))

area("A7","Upper Workroom", SR("A7","20-22")
  +box("A7","<p>The reek of fish and sweat stings the eyes. A great trough of half-rancid fish and brine drains through wooden chutes into a larger room beyond; a desk and a tall cabinet sit opposite.</p>")
  +"<p>Four orphans feed the chutes here. The floor around the trough is slick ("+chk("type:acrobatics|dc:15")+" if moving faster than a Step). The cabinet holds petty cash, locked ("+chk("type:thievery|dc:15")+"; Yargin's key).</p>"
  +"<p>"+act("hookshanks","Hookshanks Gruller")+", a gnome taskmaster, oversees the work — and dresses as one of the orphans, passing for one until a PC beats his Deception with "+chk("type:perception|dc:17")+" (gnome PCs get a bonus).</p>"
  +B.enc("Hookshanks + 4 orphans","Low · 40 XP",
     "<p>Hookshanks orders the orphans to attack, then opens the "+pg(P["A4"],"A4")+" door to loose "+mc("guarddog","Bloo")+" and raise the alarm; he fights with a kukri.</p>"
     +B.s_skill("<p>Rally the kids ("+chk("type:diplomacy|dc:15")+") and an older boy, Kester, blinds Hookshanks with a faceful of rancid fish. Hookshanks surrenders at low HP and tells all — except what lies in the den ("+pg(P["A14"],"A14")+").</p>"),
     B.aside_token([act("hookshanks","Hookshanks Gruller (1)"), "4× "+act("orphan","Lamm's Lamb")+" <em>(non-combatant)</em>"], img=TOK("hookshanks-gruller"))))

area("A8","Fishery Floor", SR("A8","21-22")
  +box("A8","<p>The main floor is slick with river water, weed, and fish blood. Catwalks ring an eight-foot tar-caulked slurry vat; a wide hole in the south floor opens straight onto the river below. Rows of small hammocks hang beneath the walks.</p>")
  +"<p>The heart of the operation. "+act("giggles","Giggles")+", a half-orc brute, oversees 5 orphans by day; all 26 sleep here at night. The hole drops to the river and "+act("jigsawshark","the jigsaw shark")+" — the thugs toss scraps through it to keep the shark close and the children terrified.</p>"
  +B.enc("Giggles [+ Bloo at night]","Low · 40 XP (60 with Bloo)",
     "<p>Giggles uses Bludgeoner to <strong>capture</strong> PCs nonlethally for Gaedren, switching to lethal below half HP and quaffing healing potions; then he fights to the death (Orc Ferocity).</p>"
     +SEC("<p><strong>Night raid:</strong> this floor is wall-to-wall sleeping children — a fight here endangers them. The river-hole is also the quiet route down to the underpier ("+pg(P["A12"],"A12")+") and the den, bypassing the front rooms entirely.</p>"),
     B.aside_token([act("giggles","Giggles (1)"), "5× "+act("orphan","orphans")+" <em>(non-combatant)</em>"], img=TOK("giggles"))))

area("A9","Kraken's Folly", SR("A9","23-24")
  +box("A9","<p>A derelict ship lies lashed to the pilings by layers of rotting rope, its hull furred with weed and barnacles. A narrow walkway runs along the starboard rail to an aft-cabin door marked with a daubed red fish.</p>")
  +"<p>No longer seaworthy — Gaedren's route to the den. The "+haz("rottendeck","Rotten Ship Deck")+" hazard: everything but the stern is rotten, and a Medium+ creature moving toward the bow crashes through into the hold ("+pg(P["A11"],"A11")+"). Stairs in the cabin lead down to the spider nest.</p>")

area("A10","Spider Nest", SR("A10","24")
  +box("A10","<p>The air is thick and musty. Sheets of cobweb drape the walls; mounds of blanket, cushion, and straw clutter the floor. A narrow stair drops into the ship's hold.</p>")
  +"<p>The cabin is the lair of a single cat-sized "+act("drainspider","drain spider")+" that lunges at the first creature through the door.</p>"
  +B.enc("Drain Spider","Trivial · 20 XP",
     "<p>One drain spider, off-guard against the surprised intruder it lunges at.</p>"
     +B.s_skill("<p>The spiders can't abide the <strong>vermin repellent</strong> looted from "+itm("coffer","Gaedren's coffer")+" ("+pg(P["A13"],"A13")+") — a coated creature auto-repels them.</p>"),
     B.aside_token([act("drainspider","Drain Spider (−1)")], img=TOK("drain-spider"))))

area("A11","Kraken's Hold", SR("A11","24")
  +box("A11","<p>Dark and dank, the hold smells of mildew. Crates and barrels lie stacked among puddles of standing river water.</p>")
  +"<p>Four more "+act("drainspider","drain spiders")+" infest the hold.</p>"
  +SEC("<p>Gaedren built a <strong>secret door into the hull</strong> ("+chk("type:perception|dc:17")+") opening to the underpier ("+pg(P["A12"],"A12")+") and the boss. Spotting his tracks in the filth ("+chk("type:survival|dc:15")+") grants a circumstance bonus to find it.</p>")
  +B.enc("Drain Spider nest","Moderate · 80 XP (trivial with repellent)",
     "<p>Four drain spiders swarm anything that enters. Pair this with the "+haz("rottendeck","Rotten Deck")+" collapse from "+pg(P["A9"],"A9")+" for a single nasty moment.</p>",
     B.aside_token(["4× "+act("drainspider","Drain Spider (−1)")], img=TOK("drain-spider"))))

area("A12","Underpier", SR("A12","24-25")
  +box("A12","<p>A narrow space runs beneath the fishery, three feet of headroom above the foamy river. Moss and rusted chain hang between the pilings, and a floating walkway threads west to a tiny two-and-a-half-foot door.</p>")
  +"<p>Gaedren's escape skiffs are tied along the walkway. The squat door ("+chk("type:thievery|dc:17")+") leads into the den ("+pg(P["A13"],"A13")+"); a Medium creature must stoop to squeeze through.</p>"
  +B.enc("Jigsaw Shark","Low · 40 XP · avoidable",
     "<p>The shark scavenges scraps drifting from above. It attacks anything that falls into the water, but only leaps onto the walkway if it is first attacked and damaged.</p>"
     +B.s_skill("<p>Stay dry and it stays a hazard, not a fight — though the "+haz("boardwalk","boardwalk")+" and "+haz("rottendeck","rotten deck")+" above exist precisely to feed it victims.</p>"),
     B.aside_token([act("jigsawshark","Jigsaw Shark (1)")], img=TOK("jigsaw-shark"))))

area("A13","Gaedren's Playground", SR("A13","24-26")
  +box("A13","<p>A chill chamber opens over a pit of black river water, crossed by two five-foot walkways. Rusted manacles dangle from mossy ropes above the pool. On the far side, cabinets and lockboxes spill dingy 'treasures' across three cluttered tables. Something heavy shifts in the water below.</p>")
  +"<p>"+mc("crocodile","Gobblegut")+" lurks in the pit; "+act("gaedren","Gaedren Lamm")+" sorts the day's haul at his tables across it. <strong>Reaching him means crossing the gator's water.</strong></p>"
  +SEC("<p>Those manacles are where Gaedren feeds doomed orphans to Gobblegut for sport — the PCs may arrive mid-'feeding,' a child dangling over the snapping jaws. Anyone who names <strong>Zellara</strong> earns a leering reply that 'she's in the next room' — her head waits in "+pg(P["A14"],"A14")+". <strong>Tactics:</strong> Gaedren opens with <em>Spur the Beast</em> to enrage Gobblegut, snipes from across the pool, <em>Nimble Dodges</em> focus fire, and flees to the "+pg(P["A12"],"A12")+" skiffs at &le;8 HP — though the abused gator may take him first.</p>")
  +B.enc("BOSS — Gaedren + Gobblegut","SEVERE · 120 XP @ level 1 (Moderate @ level 2)",
     "<p>The crocodile is the real threat; Gaedren is a frail catalyst who weaponizes it and snipes from cover.</p>"
     +"<p><strong>Scaling:</strong> 3 PCs → Weak Crocodile · 5–6 PCs → Elite Crocodile and/or pull a drain spider from the pool · if Yargin reached Gaedren first, Gobblegut starts pre-enraged.</p>",
     B.aside_token([act("gaedren","Gaedren Lamm (2)"), mc("crocodile","Gobblegut — Crocodile (2)")], img=TOK("gaedren-lamm")))
  +B.s_treasure("<p>On the tables: "+itm("coffer","a darkwood coffer — 20 doses of shiver + 7 applications of vermin repellent")+".</p>")
  +B.s_conv("<p><strong>⚠ Track what the PCs do with the body.</strong> Left here, Gaedren's son Rolth animates it — the PCs meet an undead Gaedren in the Dead Warrens at the chapter's end. See "+pg(P["conv"],"Conversion Notes")+".</p>"))

area("A14","Gaedren's Den", SR("A14","26-28")
  +box("A14","<p>A squalid bedroom-study: a lumpy bed against one wall, a table heaped with rotting food and scuttling roaches, a sagging dresser. At the foot of the bed sits a locked strongbox, a moldy ledger resting on its lid. A fly-blown hatbox sits atop the dresser.</p>")
  +"<p>Gaedren's private quarters. The strongbox opens to the rusty iron key he carries, or "+chk("type:thievery|dc:15")+".</p>"
  +SEC("<p><strong>The reveal.</strong> The hatbox holds <strong>Zellara's severed head</strong>, crudely made up to mimic life ("+chk("type:medicine|dc:14")+": dead for weeks) — confirming the woman who hired the party has been dead all along. Beneath it lies "+itm("harrowdeck","her haunted harrow deck")+", still inhabited by her spirit. Atop the strongbox is "+itm("ledger","Gaedren's coded ledger")+"; inside, "+itm("brooch","Queen Ileosa's Brooch")+" and the hoard. A key-shaped masterwork dagger among the loot is a gift from Gaedren's estranged son <strong>Rolth</strong> — foreshadowing the next chapter ("+chk("type:society|dc:20")+" recognizes the killer's signature blade).</p>")
  +B.s_treasure("<p>Full parcel on the "+pg(P["treasure"],"Treasure")+" page.</p>"))

# NPCs index -------------------------------------------------------------------
pages.append(newpage("npcs","NPCs",
  "<p>Click any creature to open its sheet. Build rationale: <code>reports/npc_monster_conversion_report.md</code>.</p>"
  +"<ul>"
   "<li>"+act("gaedren","Gaedren Lamm")+" (L2) — "+pg(P["A13"],"A13")+" boss · "+act("yargin","Yargin Balko")+" (L1) — "+pg(P["A6"],"A6")+" · "+act("hookshanks","Hookshanks Gruller")+" (L1) — "+pg(P["A7"],"A7")+" · "+act("giggles","Giggles")+" (L1) — "+pg(P["A8"],"A8")+"</li>"
   "<li>"+mc("crocodile","Gobblegut")+" = Crocodile (L2) · "+mc("guarddog","Bloo")+" = Guard Dog (L−1) · "+act("drainspider","Drain Spider")+" (L−1) · "+act("jigsawshark","Jigsaw Shark")+" (L1) · "+act("orphan","Lamm's Lambs")+" <em>(non-combatant)</em></li>"
   "<li><strong>Zellara</strong> — the harrow-spirit guide, bound to "+itm("harrowdeck","her deck")+" (story NPC, no stat block).</li>"
   "</ul>",level=2))

# Treasure ---------------------------------------------------------------------
pages.append(newpage("treasure","Treasure",
  "<p>Rebuilt to PF2e level 1→2 (the PF1e gp hoard is discarded; CHG-0008). Full table: <code>reports/treasure_report.md</code>.</p>"
  +B.s_treasure("<ul>"
   "<li>"+itm("dagger","+1 Dagger (Gaedren's)")+" — boss loot, a fitting first permanent magic weapon · +1 armor potency (his padded armor) · A14 hoard → a 1st-rank scroll + ~50 gp gems.</li>"
   "<li>"+itm("garnet","Garnet amulet")+" (~8 gp) · "+itm("coffer","Coffer + vermin repellent")+" (~12 gp) · 2× Acid Flask + Thunderstone (Yargin) · 3× minor Healing Potion (Giggles) · ~30 gp coin.</li>"
   "<li>"+itm("ledger","Coded ledger")+" → Korvosan Guard bounty 15 gp (30 gp with the cipher key).</li>"
   "</ul>")
  +SEC("<p><strong>Story items — do not let players cash these out for level-breaking gold.</strong> "+itm("brooch","Queen Ileosa's Brooch")+" launches the queen's audience and the chapter's main reward; "+itm("harrowdeck","Zellara's Harrow Deck")+" is the Harrow subsystem anchor (CHG-0010). The original PF1e parcel (a 2,000 gp brooch, gold ingot, etc.) is deliberately <em>not</em> restored.</p>"),level=2))

# Conversion Notes -------------------------------------------------------------
pages.append(newpage("conv","Conversion Notes",
  B.s_conv("<p>Mirrors <code>conversion_change_log.md</code> (CHG-0101…0108). Story, villain, flow, and the closing cliffhanger are all preserved; nothing here is an approval-gated change.</p>"
   "<ul>"
   "<li><strong>Gaedren rebuilt as a credible Severe</strong>, with Gobblegut as the real threat — fixes the 'Lamm is a Lamb' anticlimax and PF2e solo-boss math. Added <em>Spur the Beast</em> / <em>Nimble Dodge</em>; kept <em>Limping Gait</em>. ⚠ Confirm Severe @L1 vs running it @L2.</li>"
   "<li><strong>Gobblegut & Bloo</strong> referenced as the official Crocodile / Guard Dog (no rebuild).</li>"
   "<li><strong>DCs re-derived</strong> to PF2e level-based / simple values (the PF1e locked-door spam collapsed to a single 'pick = 15' line).</li>"
   "<li><strong>Treasure rebuilt</strong> to PF2e level 1→2 (CHG-0008).</li>"
   "<li><strong>Drain Spider Venom</strong>: PF1e Con-drain → PF2e 1-stage poison + enfeebled.</li>"
   "<li><strong>Harrowing</strong> → hero-point-style suit pool (CHG-0010).</li>"
   "<li><strong>Orphans</strong> = explicit non-combatants (Rally / Cower); never an XP-for-kill source (CHG-0107).</li>"
   "<li><strong>Forward hooks:</strong> leaving Gaedren's body → undead Gaedren in the Dead Warrens; the Brooch → the queen's audience; the deck → recurring Harrowings.</li>"
   "</ul>"),level=2))

journal = B.journal_entry(JID,"1. Edge of Anarchy",pages,folder=F["j_adventure"])
B.write("journals","01-edge-of-anarchy",copy.deepcopy(journal),embed_pages=True)

# =====================================================================
# INTRODUCTION — detached top-level journal (root, like Kingmaker's "Introduction")
# =====================================================================
INTRO_JID = "cotctIntro000001"
_premise  = apspan("Korvosa, the Jewel of Varisia, has long sparkled", "USING THIS BOOK")
_synopsis = apspan("Curse of the Crimson Throne begins as a group of diverse characters", "CAMPAIGN TRAITS")
intro_pages = [
  B.page(nid(), "Long Live the Queen!", _premise or
    "<p>Korvosa, the Jewel of Varisia, lies under the shadow of the Curse of the Crimson Throne — no monarch has died of old age or produced an heir while ruling. King Eodred II's grip is firm but tenuous, and the city waits for the curse to claim him.</p>", level=1),
  B.page(nid(), "Campaign Synopsis", _synopsis or
    "<p>The PCs are drawn together to take revenge on the crime-lord Gaedren Lamm; as they do, the king dies and Queen Ileosa seizes Korvosa. Recruited to restore order, they uncover her hand behind a plague and worse — she has taken on the mantle of the dragon Kazavon via the Crown of Fangs. Only the blade that slew Kazavon, recovered from haunted Castle Scarwall, can end her, in a final reckoning at the Sunken Queen.</p>", level=1),
]
intro_journal = B.journal_entry(INTRO_JID, "Introduction", intro_pages, folder=None)
B.write("journals", "00-introduction", copy.deepcopy(intro_journal), embed_pages=True)

# =====================================================================
# SCENE — Old Fishery placeholder with map-note pins -> area pages + staged tokens
# =====================================================================
GRID=100; W=2400; H=1800
# notes for each keyed area, laid out in a grid (NEEDS GM REVIEW positions, no map)
area_codes=["A1","A2","A3","A4","A5","A6","A7","A8","A9","A10","A11","A12","A13","A14"]
notes=[];
for i,code in enumerate(area_codes):
    col=i%5; row=i//5
    notes.append(B.note(nid(),JID,P[code],code, 300+col*400, 300+row*400))
# staged hostile tokens (my actors) near sensible areas — positions NEEDS GM REVIEW
tok=[]
def place(actor_key,name,code):
    n=next(x for x in notes if x["text"]==code)
    tok.append(B.token(nid(),A[actor_key],name,n["x"],n["y"]+120,TOK(actor_key)))
place("yargin","Yargin Balko","A6"); place("hookshanks","Hookshanks Gruller","A7")
place("giggles","Giggles","A8"); place("drainspider","Drain Spider","A10")
for _ in range(4): place("drainspider","Drain Spider","A11")
place("jigsawshark","Jigsaw Shark","A12"); place("gaedren","Gaedren Lamm","A13")
sc = B.scene(SCN,"Old Fishery",W,H,GRID,"modules/cotct-pf2e-conversion/assets/maps/01-old-fishery.webp",
             notes,tok,folder=F["s_ch1"],
             foreground="modules/cotct-pf2e-conversion/assets/maps/01-old-fishery-roof.webp",
             navName="Old Fishery")
B.write("scenes","01-old-fishery",copy.deepcopy(sc))

# =====================================================================
# ADVENTURE bundle (one-click import; embeds copies WITHOUT _key)
# =====================================================================
def strip(doc):
    d=copy.deepcopy(doc); d.pop("_key",None)
    for it in d.get("items",[]): it.pop("_key",None)
    for p in d.get("pages",[]): p.pop("_key",None)
    for n in d.get("notes",[]): n.pop("_key",None)
    for t in d.get("tokens",[]): t.pop("_key",None)
    return d
adv = B.adventure(ADV,"Curse of the Crimson Throne — Ch.1: Edge of Anarchy (pilot)",
  "modules/cotct-pf2e-conversion/assets/art/cover.webp",
  "<p>Phase-2 pilot: the Old Fishery (the hunt for Gaedren Lamm). Imports the chapter journal, the Old Fishery scene (map-note pins + staged tokens), the converted NPCs/hazards, and the treasure — organized into folders. Supply your own maps (Racooze's free CotCT battlemaps).</p>",
  [strip(f) for f in folders], [strip(intro_journal), strip(journal)], [strip(sc)],
  [strip(a) for a in actors]+[strip(h) for h in hazards], [strip(i) for i in items])
B.write("adventure","cotct-edge-of-anarchy",copy.deepcopy(adv))

print(f"Pilot (Kingmaker-style) built: {len(folders)} folders, {len(actors)} actors, {len(hazards)} hazards, "
      f"{len(items)} items, 1 journal ({len(pages)} pages), 1 scene ({len(notes)} notes / {len(tok)} tokens), 1 adventure.")
