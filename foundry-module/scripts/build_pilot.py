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
     "garnet":"dK4hnpH7s67RYnNI","coffer":"ymuRwMg6WfWIwkne","dagger":"b04PLWVkmm3RM4nm",
     "bg_betrayed":"bgBetrayed000001","bg_drugaddict":"bgDrugAddict0001","bg_framed":"bgFramed00000001",
     "bg_lovelost":"bgLoveLost000001","bg_missingchild":"bgMissingChild01","bg_unhappy":"bgUnhappyChild01",
     # Part Two — A City Gone Mad (custom NPCs)
     "mad_prophet":"madProphet000001","rioter":"korvosanRioter01","amin":"aminJalento00001",
     "grau":"grauSoldado00001","trinia":"triniaSabor00001","trinia_wand":"triniaWand000001",
     # Part Three — Blood and Bones, area B (All the World's Meat)
     "cowhammer":"cowHammerBoy0001","verik":"verikVancask0001","verik_bow":"verikLongbow0001",
     # Part Three — area C (Eel's End)
     "enforcer":"eelsEndEnforce01","devargo":"devargoBarvasi01","devargo_armor":"devargoArmor0001",
     "chittersnap":"chittersnap00001",
     # Part Three — area D (The Dead Warrens)
     "skelowlbear":"skeletalOwlbr001","derro":"derroMinion00001","stirge":"stirgeFeeder0001",
     "cabbagehead":"cabbageheadOgr01","vreeg":"vreegDerroNec001","acidskulls":"acidSkullTrap001"}
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
    while text and text[-1] not in '.!?:"”\'’)' and k < len(paras):
        nxt = paras[k]
        if nxt.startswith("#"): break                 # real section header = stop
        if (not nxt) or nxt.startswith("<!--"):        # blank / image / page marker
            k += 1; continue                           # skip — read-aloud often spans these
        text, k = text + " " + nxt, k + 1
    # repair OCR drop-caps at the start ("T he"->"The", "S lippery"->"Slippery");
    # exclude the real one-letter words A / I so "A fifteen-foot" is left alone.
    text = re.sub(r'^([B-HJ-Z]) ([a-z])', r'\1\2', text)
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
 # Part Two read-aloud (mid-phrase anchors dodge OCR drop-caps)
 "CGM":"sight of smoke rising on the horizon",
 "E12FLAT":"one-room flat combines all the amenities",
 # Part Three, area B — All the World's Meat
 "B1":"sign bearing the image of a fat, smiling cow",
 "B3":"air in this room is stale, stinking of day-old meat",
 "B4":"floor of this grim chamber is strewn",
 "B5":"foul-smelling animal pens take up the majority",
 "B6":"large cattle pen is open to the air",
 "B7":"round table sits in this room, surrounded by four wooden chairs",
 "B8":"single large desk stands in the eastern part",
 # Part Three, area C — Eel's End
 "C1":"sound of carousing booms from the elegantly painted",
 "C2":"large ship tied off to the pier bears the name",
 "C4":"hut-like structures sit atop this barge",
 "C5":"single long structure sits atop the main deck",
 "C6":"once-proud vessel, the Dragon's Breath",
 "C7":"large room, once a captain's cabin, has been converted into a throne room",
 "C13":"single low desk sits against the wall of this room",
 "C15":"dark chamber is riddled with dizzying tunnels",
 "C17":"old cargo bay is partially collapsed",
 # Part Three, area D — The Dead Warrens
 "D1":"large room is supported by four wide pillars of stone",
 "D4":"majority of this room contains a nasty-looking stretch of mud",
 "D5":"Three wooden tables stand in the middle of this room",
 "D7":"wooden tables here are stacked with vials, beakers",
 "D9":"foul-smelling cavern is bordered on three sides",
 "D10":"Two wide, freestanding bookshelves furnish this room",
 "D11":"nauseating mixture of decay and strange chemicals",
 "D12":"chamber holds a large four-poster bed and a simple writing desk",
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
F = {k: nid() for k in ["a_root","a_ch1","a_creatures","a_hazards","i_root","i_ch1","i_treasure","i_bg",
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
 B.folder(F["i_bg"],"Campaign Backgrounds","Item",F["i_root"],200000,None,"a"),
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

# ---- Part Two: A City Gone Mad (custom NPCs) ----
AW("mad-prophet", B.npc(A["mad_prophet"],"Mad Prophet",-1,14,12,5,3,7,5,
  {"str":1,"dex":1,"con":2,"int":-1,"wis":3,"cha":0},25,
  {"athletics":5,"intimidation":5,"religion":5,"society":3},
  ["humanoid","human"],["common"],
  [B.strike(nid(),"Filthy Grasp",5,"1d4+1","bludgeoning",["agile"]),
   B.action(nid(),"Diseased Grab","1","<p>The prophet makes an Athletics check to Grab a creature he is touching. A creature he "+B.cond("grabbed","Grabs")+" is exposed to <strong>Filth Fever</strong> ("+chk("type:fortitude|dc:16")+"): on a failure it is "+B.cond("sickened","Sickened 1")+" (Sickened 2 and "+B.cond("enfeebled","Enfeebled 1")+" on a critical failure); the disease advances daily until cured.</p>",["disease","manipulate"]),
   B.action(nid(),"Doomsaying","1","<p>The prophet shrieks a prophecy at one creature, who must succeed at a "+chk("type:will|dc:14")+" or be "+B.cond("frightened","Frightened 1")+" (Frightened 2 on a critical failure).</p>",["auditory","emotion","fear","mental"])],
  notes="<p><strong>Role:</strong> a doomsayer, not a real fight — the danger is the <strong>Filth Fever</strong> he carries, contracted if he Grabs a PC. Most prophets are harmless street-corner prognosticators; this one has fixated on a PC.</p>"
        "<p><strong>Behavior:</strong> raves and reaches for the PC he is obsessed with; flees or collapses once struck. Curing his disease (or his madness) is a Good deed, not an XP-for-kill.</p>",
  folder=F["a_creatures"], blurb="Plague-touched doomsayer", token_src=TOK("mad-prophet")))

AW("korvosan-rioter", B.npc(A["rioter"],"Korvosan Rioter",-1,15,14,5,2,2,3,
  {"str":3,"dex":1,"con":2,"int":-1,"wis":0,"cha":0},25,
  {"athletics":6,"intimidation":5},
  ["humanoid","human"],["common"],
  [B.strike(nid(),"Club",6,"1d6+3","bludgeoning",[]),
   B.strike(nid(),"Improvised Thrown",6,"1d6+3","bludgeoning",["range-increment-10"]),
   B.gear("club",nid())],
  notes="<p><strong>Role:</strong> a fragile mob mook — a laborer with a chair-leg, not a soldier. Reuse this stat block for any riot in the AP.</p>"
        "<p><strong>Tactics:</strong> swarms the nearest target, or focuses any obviously well-to-do socialite. <strong>Morale:</strong> a rioter flees as soon as it takes any damage — a mob this size routs fast once blooded.</p>",
  folder=F["a_creatures"], blurb="Angry laborer in the riots", token_src=TOK("korvosan-rioter")))

AW("amin-jalento", B.npc(A["amin"],"Amin Jalento",1,16,18,4,6,7,5,
  {"str":1,"dex":3,"con":1,"int":0,"wis":1,"cha":2},25,
  {"diplomacy":6,"society":6,"deception":4,"acrobatics":6},
  ["humanoid","human"],["common"],
  [B.strike(nid(),"Rapier",7,"1d6+1","piercing",["deadly-d8","disarm","finesse"]),
   B.action(nid(),"Fight Defensively","1","<p>Amin focuses entirely on defense, gaining a +1 circumstance bonus to AC until the start of his next turn. He has never been in a real fight and avoids attacking if he can flee instead.</p>",["concentrate"]),
   B.gear("leather-armor",nid()), B.gear("healing-potion-minor",nid(),2),
   B.equipment(nid(),"Signet Ring & 12 pp",0,12,"<p>A young nobleman's signet ring and purse — about 12 pp.</p>",traits=["art-object"])],
  notes="<p><strong>Role:</strong> a beardless young noble cornered by the mob in Event 5 — a quest-giver, not a combatant. If the PCs disperse the mob ("+chk("type:diplomacy|dc:18")+" or "+chk("type:intimidation|dc:18")+") or fight it off, Amin escapes.</p>"
        "<p><strong>Behavior:</strong> fights defensively only if cornered; flees at the first chance. <strong>Reward:</strong> if saved, he gratefully gives the party a gold ring worth 250 gp (award XP as if defeated).</p>",
  folder=F["a_creatures"], blurb="Rescued young nobleman (Event 5)", token_src=TOK("amin-jalento")))

AW("grau-soldado", B.npc(A["grau"],"Grau Soldado",4,21,62,11,11,5,9,
  {"str":3,"dex":3,"con":4,"int":0,"wis":0,"cha":1},25,
  {"athletics":10,"acrobatics":12,"intimidation":9,"deception":8},
  ["humanoid","human"],["common"],
  [B.strike(nid(),"+1 Striking Mithral Longsword",13,"2d8+6","slashing",["magical","versatile-p"],slug="grau-longsword"),
   B.sneak_attack(nid(),1,"Grau"),
   B.action(nid(),"Power Attack","2","<p>Grau makes a Longsword Strike that deals an extra @Damage[1d8[slashing]] on a hit (he always uses this while drunk and belligerent). On a failure he is "+B.cond("off-guard","Off-Guard")+" until the start of his next turn.</p>",["flourish"]),
   B.action(nid(),"Drunk","passive","<p>Grau fights "+B.cond("sickened","Sickened 1")+" while intoxicated; this −1 penalty is already included in his statistics. He makes poor tactical choices, ignoring openings for Sneak Attack and provoking reactions as he stumbles between foes.</p>",category="defensive"),
   B.lore(nid(),"Korvosa Lore",6),
   B.gear("chain-mail",nid()), B.gear("steel-shield",nid())],
  notes="<p><strong>Role:</strong> a recurring NPC — a well-liked Korvosan Guard watch sergeant (Vencarlo Orisini's expelled student) drowning his despair in drink. This 'fight' is meant to be survived and <strong>defused</strong>, not a kill.</p>"
        "<p><strong>Defusing him:</strong> commiserate ("+chk("type:diplomacy|dc:20")+", or a Deception vs. his Perception) and he sobers up; "+chk("type:society|dc:18")+" recognizes the sergeant he was. A lesser restoration sobers him instantly. Escorted to Citadel Volshyenek, his fellow guards clean him up and he becomes a grateful ally.</p>"
        "<p><strong>If he duels:</strong> he limits attacks to the PC who accepted the duel; if another PC strikes him he cries 'Foul!' and flails at random foes. <strong>Morale:</strong> surrenders rather than dies. Award XP as if defeated whether he is beaten or talked down.</p>",
  folder=F["a_creatures"], blurb="Drunken watch sergeant; future ally", token_src=TOK("grau-soldado"), actor_link=True))

AW("trinia-sabor", B.npc(A["trinia"],"Trinia Sabor",3,18,36,6,11,9,7,
  {"str":0,"dex":3,"con":1,"int":2,"wis":1,"cha":3},25,
  {"acrobatics":11,"crafting":8,"deception":9,"stealth":11,"society":6,"arcana":7},
  ["humanoid","human"],["common","varisian"],
  [B.strike(nid(),"Dagger",9,"1d4","piercing",["agile","finesse","thrown-10","versatile-s"]),
   B.action(nid(),"Wand of Daze Monster","1","<p>Trinia Activates her <strong>wand of daze monster</strong> against the closest pursuer, who must succeed at a "+chk("type:will|dc:17")+" or be "+B.cond("stunned","Stunned 1")+" (Stunned 3 on a critical failure) — she uses it to break up a chase.</p>",["concentrate","magical"]),
   B.action(nid(),"Figment","2","<p>Trinia conjures a minor illusion — most often an image of herself asleep in her bed, which she abandons (the figment lingers ~2 rounds) as she slips out the window. A creature that Seeks against it disbelieves with a "+chk("type:will|dc:17")+".</p>",["concentrate","illusion","manipulate"]),
   B.action(nid(),"Fit of Laughter","2","<p>One creature on Trinia's space must succeed at a "+chk("type:will|dc:17")+" or be overcome with laughter — "+B.cond("slowed","Slowed 1")+" and unable to act usefully for 1 round (it falls "+B.cond("prone","Prone")+" on a critical failure).</p>",["emotion","incapacitation","mental"]),
   {"_id":A["trinia_wand"],"img":"systems/pf2e/icons/default-icons/consumable.svg","name":"Wand of Daze Monster","type":"weapon","sort":0,"ownership":{"default":0},"flags":{},"_stats":dict(B.STATS),
    "system":{"baseItem":None,"bonus":{"value":0},"bonusDamage":{"value":0},"bulk":{"value":0.1},"category":"simple","containerId":None,"damage":{"damageType":"mental","dice":0,"die":""},"description":{"value":"<p>A slim birch wand. Once per day it can stun a target ("+chk("type:will|dc:17")+"); Trinia uses it to slow pursuit in the Shingles chase.</p>"},"equipped":{"carryType":"held","handsHeld":1},"group":None,"hardness":0,"hp":{"max":0,"value":0},"level":{"value":1},"material":{"grade":None,"type":None},"price":{"value":{"gp":60}},"publication":B.PUB,"quantity":1,"range":None,"reload":{"value":None},"rules":[],"runes":{"potency":0,"property":[],"striking":0},"size":"med","slug":None,"splashDamage":{"value":0},"traits":{"rarity":"common","value":["magical","wand"]},"usage":{"value":"held-in-one-hand"}}}],
  notes="<p><strong>Role:</strong> the innocent young painter Queen Ileosa frames for the king's murder — a recurring NPC, <strong>not</strong> an enemy. She avoids combat entirely, fleeing through the Shingles (Event 12). She is telling the truth: she did not kill the king.</p>"
        "<p><strong>In the chase:</strong> she moves one obstacle at a time while she holds a lead, uses her wand on the closest PC, favors Acrobatics, and takes risks to gain ground when a PC closes. Cornered, she uses <em>Fit of Laughter</em> and weeps that she has been set up.</p>",
  folder=F["a_creatures"], blurb="Framed artist; recurring ally", token_src=TOK("trinia-sabor"), actor_link=True))

# ---- Part Three: area B — All the World's Meat (custom NPCs) ----
AW("cow-hammer-boy", B.npc(A["cowhammer"],"Cow Hammer Boy",2,18,30,8,6,4,6,
  {"str":3,"dex":3,"con":2,"int":0,"wis":0,"cha":1},25,
  {"athletics":7,"intimidation":6,"stealth":6},
  ["humanoid","human"],["common"],
  [B.strike(nid(),"Composite Longbow",9,"1d8+3","piercing",["deadly-d10","propulsive","range-increment-100","reload-0","volley-30"]),
   B.strike(nid(),"Club",8,"1d6+3","bludgeoning",[]),
   B.gear("composite-longbow",nid()), B.gear("club",nid()), B.gear("studded-leather",nid())],
  notes="<p><strong>Role:</strong> a deserter-guard thug (one of Verik's four 'Cow Hammer Boys'), reusable as a Northgate brigand. Opens with the longbow, closes to the club only if forced.</p>"
        "<p><strong>Tactics &amp; morale:</strong> two guard the front (B1), two work the killing floor (B4). A boy at low HP flees into the city; once two are dead, the rest abandon Verik and run. They do <strong>not</strong> let anyone up to Verik — they hide their murder-for-hire side business from him.</p>",
  folder=F["a_creatures"], blurb="Deserter-guard thug ('Cow Hammer Boy')", token_src=TOK("cow-hammer-boy")))

AW("verik-vancaskerkin", B.npc(A["verik"],"Verik Vancaskerkin",4,21,60,11,11,8,8,
  {"str":4,"dex":4,"con":2,"int":0,"wis":0,"cha":2},25,
  {"athletics":10,"intimidation":10,"acrobatics":10,"nature":6},
  ["humanoid","human"],["common"],
  [{"_id":A["verik_bow"],"img":"systems/pf2e/icons/equipment/weapons/composite-longbow.webp",
    "name":"+1 Striking Composite Longbow","type":"weapon","sort":0,"ownership":{"default":0},"flags":{},"_stats":dict(B.STATS),
    "system":{"baseItem":"composite-longbow","bonus":{"value":1},"bonusDamage":{"value":0},"bulk":{"value":1},"category":"martial","containerId":None,"damage":{"damageType":"piercing","dice":2,"die":"d8"},"description":{"value":"<p>Verik's prized Korvosan Guard composite longbow, etched with a +1 potency rune and a striking rune — the AP's area-B permanent magic reward.</p>"},"equipped":{"carryType":"held","handsHeld":2},"group":"bow","hardness":0,"hp":{"max":0,"value":0},"level":{"value":4},"material":{"grade":None,"type":None},"price":{"value":{"gp":160}},"publication":B.PUB,"quantity":1,"range":100,"reload":{"value":"0"},"runes":{"potency":1,"property":[],"striking":1},"size":"med","slug":None,"splashDamage":{"value":0},"traits":{"rarity":"common","value":["deadly-d10","magical","propulsive","volley-30"]},"usage":{"value":"held-in-two-hands"}}},
   B.strike(nid(),"+1 Striking Composite Longbow",14,"2d8+4","piercing",["deadly-d10","magical","propulsive","range-increment-100","reload-0","volley-30"],slug="verik-bow-strike"),
   B.strike(nid(),"Spear",12,"1d6+4","piercing",["thrown-20"]),
   B.action(nid(),"Precise Shot","passive","<p>Verik ignores the lesser cover and "+B.cond("off-guard","Off-Guard")+" circumstance that ranged attackers normally suffer in melee, and never takes the −2 for shooting into a crowd.</p>",category="offensive"),
   B.lore(nid(),"Korvosan Guard Lore",8),
   B.gear("chain-mail",nid()), B.gear("spear",nid()), B.gear("healing-potion-minor",nid(),3)],
  notes="<p><strong>Role:</strong> deserter watch sergeant fronting the slaughterhouse — a recurring NPC, not a die-hard villain. He believes his Vudrani lover 'Meliya' (secretly the rakshasa Vimanda) is just feeding the poor; he has no idea his men murder for hire.</p>"
        "<p><strong>Tactics:</strong> fights from range with the longbow, switching to the spear only if engaged in melee. He hesitates several rounds before joining a fight below (fearing the Guard has come for him), often arriving as it ends.</p>"
        "<p><strong>Surrender:</strong> he gives up if dropped below ~1/4 HP, or instantly if shown hard evidence of the murders (the severed finger, the buried stash, or a thug's confession). "+chk("type:intimidation|dc:18")+" cows him (he then flees if unbound); a near-impossible Diplomacy makes him helpful. <strong>Story award</strong> for taking him alive without combat. His silver dagger is the "+B.mon("raktavarna","raktavarna")+" spy.</p>",
  folder=F["a_creatures"], blurb="Deserter watch sergeant; Arkona dupe", token_src=TOK("verik-vancaskerkin"), actor_link=True))

# ---- Part Three: area C — Eel's End (custom NPCs) ----
AW("eels-end-enforcer", B.npc(A["enforcer"],"Eel's End Enforcer",3,20,45,9,7,8,9,
  {"str":3,"dex":2,"con":3,"int":0,"wis":1,"cha":-1},25,
  {"athletics":9,"intimidation":7},
  ["humanoid","human"],["common"],
  [B.strike(nid(),"Sap",11,"1d6+3","bludgeoning",["agile","nonlethal"]),
   B.strike(nid(),"Crossbow",9,"1d8","piercing",["range-increment-120","reload-1"]),
   B.gear("leather-armor",nid()), B.gear("buckler",nid()), B.gear("crossbow",nid())],
  notes="<p><strong>Role:</strong> one of Devargo's dozen hired muscle — washed-out soldiers and sailors kept sober by fear of the King of Spiders. They prefer <strong>saps</strong>: troublemakers are knocked out, not killed, then fed to Chittersnap below.</p>"
        "<p><strong>Tactics &amp; morale:</strong> 4 work the pier (C1), 6 the deck (C2). They fight until reduced to a sliver of HP, then flee. Once Devargo raises the alarm, more arrive at one per round. Bluff/Diplomacy gets past them far more cheaply than a fight.</p>",
  folder=F["a_creatures"], blurb="Devargo's sap-wielding muscle", token_src=TOK("eels-end-enforcer")))

AW("devargo-barvasi", B.npc(A["devargo"],"Devargo Barvasi",6,23,100,12,16,12,14,
  {"str":1,"dex":5,"con":3,"int":1,"wis":0,"cha":3},25,
  {"acrobatics":16,"stealth":16,"deception":14,"intimidation":14,"thievery":14,"society":12,"crafting":12},
  ["humanoid","human"],["common"],
  [{"_id":A["devargo_armor"],"img":"systems/pf2e/icons/equipment/armor/studded-leather-armor.webp",
    "name":"+1 Studded Leather","type":"armor","sort":0,"ownership":{"default":0},"flags":{},"_stats":dict(B.STATS),
    "system":{"baseItem":"studded-leather","bonus":{"value":0},"category":"light","containerId":None,"description":{"value":"<p>Devargo's spider-motif studded leather, etched with a +1 armor potency rune.</p>"},"equipped":{"carryType":"worn","inSlot":True},"group":"leather","hardness":0,"hp":{"max":0,"value":0},"level":{"value":4},"material":{"grade":None,"type":None},"price":{"value":{"gp":160}},"publication":B.PUB,"quantity":1,"runes":{"potency":1,"property":[],"resilient":0},"size":"med","slug":None,"traits":{"rarity":"common","value":["magical"]},"usage":{"value":"wornarmor"}}},
   B.strike(nid(),"Poisoned Spiked Gauntlet",16,"1d4+5","piercing",["agile","versatile-b"],slug="devargo-gauntlet"),
   B.strike(nid(),"Hand Crossbow",16,"1d6","piercing",["range-increment-60","reload-1"]),
   B.sneak_attack(nid(),3,"Devargo"),
   B.action(nid(),"Prepare Spider Venom","passive","<p>Before a fight Devargo coats both gauntlets with spider venom. A creature he hits with a gauntlet is exposed to it: "+chk("type:fortitude|dc:24")+", a 1-stage poison inflicting "+B.cond("clumsy","Clumsy 2")+" and "+B.cond("enfeebled","Enfeebled 1")+" for 1 round (Clumsy 2 + Enfeebled 2 for 4 rounds on a critical failure).</p>",category="offensive"),
   B.action(nid(),"Spring the Throne","free","<p><strong>Trigger</strong> Devargo's turn begins.</p><hr /><p><strong>Effect</strong> He flips the hidden switch in his throne, opening the trap door beneath the petitioner's spot. A creature on it must succeed at a "+chk("type:reflex|dc:25")+" or fall into the Spider's Web (C15) — and Chittersnap.</p>",["manipulate"]),
   B.lore(nid(),"Underworld Lore",14),
   B.gear("studded-leather",nid()), B.gear("hand-crossbow",nid()), B.gear("healing-potion-minor",nid(),1),
   B.equipment(nid(),"Potion of Invisibility",4,12,"<p>Devargo quaffs this to flee when reduced below ~10% HP, vanishing down to his quarters (C14).</p>",traits=["potion","magical","consumable","illusion"])],
  notes="<p><strong>Role:</strong> the self-styled <strong>King of Spiders</strong> — a poisoner-rogue and blackmailer, <strong>not</strong> a forced boss fight. The PCs only need the ambassador's letters; the intended path is social (Diplomacy + bribes / a game of knivesies), and the Guard won't prosecute if he <em>is</em> killed.</p>"
        "<p><strong>Tactics:</strong> opens by springing the throne trap door, then wades in with poisoned gauntlets and Sneak Attacks; his enforcers don't respond until he raises the alarm or a thug flees. <strong>Morale:</strong> below ~10 HP he calls for help, drinks his potion of invisibility, and flees to C14.</p>"
        "<p><strong>His secret:</strong> he can't truly command spiders — the ettercap "+act("chittersnap","Chittersnap")+" in C15 does, in exchange for victims. Kill Chittersnap and every spider on Eel's End turns feral, Devargo included.</p>",
  folder=F["a_creatures"], blurb="The King of Spiders; blackmailer of Eel's End", token_src=TOK("devargo-barvasi"), actor_link=True))

AW("chittersnap", B.npc(A["chittersnap"],"Chittersnap",4,21,70,12,10,8,12,
  {"str":4,"dex":3,"con":4,"int":-1,"wis":2,"cha":-1},25,
  {"athletics":12,"stealth":10},
  ["aberration"],[],
  [B.strike(nid(),"Jaws",14,"2d6+6","piercing",[],[("1d6","poison")]),
   B.strike(nid(),"Claw",14,"2d6+6","slashing",["agile"]),
   B.strike(nid(),"Web",12,"","bludgeoning",["range-increment-30"]),
   B.action(nid(),"Web Trap","1","<p>Chittersnap looses a gout of sticky web at one creature within 30 feet ("+chk("type:reflex|dc:21")+"). On a failure the target is "+B.cond("immobilized","Immobilized")+" (Escape or "+chk("type:athletics|dc:21")+" to break free; "+B.cond("grabbed","Grabbed")+" only on a critical failure).</p>",["manipulate"]),
   B.action(nid(),"Ettercap Venom","passive","<p>A creature damaged by Chittersnap's Jaws is exposed to its venom: "+chk("type:fortitude|dc:23")+", a 1-stage poison dealing @Damage[1d6[poison]] and "+B.cond("enfeebled","Enfeebled 2")+" for 1 round (4 rounds on a critical failure).</p>",category="offensive"),
   B.action(nid(),"Spider Master","passive","<p>Chittersnap commands every spider on Eel's End — the true source of Devargo's 'control.' While it lives, the dream spiders and giant spider act on its initiative. If it dies, all of them revert to feral hunting, attacking the nearest creature (Devargo included).</p>",category="defensive")],
  notes="<p><strong>Role:</strong> Devargo's hidden secret — a bloated ettercap lairing in the webbed hold (C15) below the throne, fed a steady diet of Devargo's victims. It views Devargo almost as a father.</p>"
        "<p><strong>Tactics:</strong> webs prey at range, then closes with poisoned jaws and claws. It rarely leaves its web-choked den, where every square is difficult, poisonous terrain (a "+chk("type:reflex|dc:10")+" each round to avoid the dream-spider webs).</p>",
  folder=F["a_creatures"], senses=[{"type":"darkvision"},{"acuity":"imprecise","type":"tremorsense","range":30}],
  blurb="Bloated ettercap; the real King of Spiders", token_src=TOK("chittersnap")))

# ---- Part Three: area D — The Dead Warrens (custom NPCs) ----
AW("skeletal-owlbear", B.npc(A["skelowlbear"],"Skeletal Owlbear",3,18,40,9,7,5,7,
  {"str":5,"dex":2,"con":3,"int":-5,"wis":0,"cha":0},25,
  {"athletics":11},
  ["undead","skeleton","mindless"],[],
  [B.strike(nid(),"Beak",12,"1d8+5","piercing",[]),
   B.strike(nid(),"Claw",12,"1d6+5","slashing",["agile"])],
  notes="<p><strong>Role:</strong> one of Rolth's animated guardians in "+"the ossuary. <strong>Undead:</strong> negative healing; immune to death effects, disease, paralysis, poison, and unconscious; mindless (immune to mental). It clatters up from the bone pit to attack and pursues throughout the warrens, but never up into Potter's Ward above.</p>",
  folder=F["a_creatures"], senses=[{"type":"darkvision"}], size="lg",
  blurb="Rolth's animated owlbear skeleton", token_src=TOK("skeletal-owlbear")))

AW("derro", B.npc(A["derro"],"Derro",2,18,30,6,8,4,6,
  {"str":1,"dex":3,"con":2,"int":0,"wis":-1,"cha":2},25,
  {"acrobatics":8,"stealth":8,"intimidation":6},
  ["humanoid","dwarf"],["common","undercommon"],
  [B.strike(nid(),"Hooked Hammer",8,"1d6+1","bludgeoning",["trip","versatile-p"]),
   B.strike(nid(),"Repeating Crossbow",9,"1d6","piercing",["range-increment-60","reload-0"]),
   B.action(nid(),"Insane Shriek","1","<p>The derro looses a burst of mad gibbering; one creature within 30 feet must succeed at a "+chk("type:will|dc:16")+" or be "+B.cond("sickened","Sickened 1")+" by the psychic noise.</p>",["auditory","emotion","mental"]),
   B.gear("crossbow",nid())],
  notes="<p><strong>Role:</strong> one of Vreeg's insane subterranean kin guarding the warrens for Rolth (who took Vreeg on as an apprentice). <strong>Tactics:</strong> attacks on sight, then flees through the secret crawl-tunnels ("+chk("type:perception|dc:20")+" to find) to warn the others.</p>",
  folder=F["a_creatures"], senses=[{"type":"darkvision"}], size="sml",
  blurb="Insane derro minion of Vreeg", token_src=TOK("derro")))

AW("stirge", B.npc(A["stirge"],"Stirge",-1,16,6,3,9,3,6,
  {"str":-3,"dex":5,"con":1,"int":-5,"wis":1,"cha":-3},10,
  {"acrobatics":9,"stealth":7},
  ["animal"],[],
  [B.strike(nid(),"Proboscis",9,"1d6","piercing",["finesse"]),
   B.action(nid(),"Blood Drain","1","<p><strong>Requirement</strong> The stirge's last action was a Proboscis hit.</p><hr /><p><strong>Effect</strong> The stirge attaches and drains blood, dealing @Damage[1d4[bleed]] and gaining that many temporary Hit Points. While attached it moves with its victim; a creature can pull it off with an "+chk("type:athletics|dc:14")+".</p>",["manipulate"])],
  notes="<p><strong>Role:</strong> a blood-feeder from Rolth's draining hutch. Darts in, attaches, and gorges. Fragile — a single hit usually drops it.</p>",
  folder=F["a_creatures"], senses=[{"type":"darkvision"},{"type":"low-light-vision"}],
  other_speeds=[{"type":"fly","value":40}], size="sml", blurb="Blood-draining vermin", token_src=TOK("stirge")))

AW("cabbagehead", B.npc(A["cabbagehead"],"Cabbagehead",3,19,55,11,6,9,9,
  {"str":5,"dex":1,"con":4,"int":-1,"wis":2,"cha":-2},25,
  {"athletics":11,"intimidation":7},
  ["humanoid","human","giant"],["common"],
  [B.strike(nid(),"Powerful Fist",12,"1d8+5","bludgeoning",["agile","nonlethal"]),
   B.action(nid(),"Pummel","2","<p>Cabbagehead makes two Powerful Fist Strikes against the same target; if both hit, the target is also pushed 5 feet and must succeed at a "+chk("type:fortitude|dc:20")+" or be "+B.cond("clumsy","Clumsy 1")+" until the end of its next turn.</p>",["flourish"])],
  notes="<p><strong>Role:</strong> a deformed ogrekin jailer, charmed long ago by Rolth and now doglike-loyal, who tends and torments the prisoners in the pits. He fights bare-fisted, shrieking taunts. <strong>Morale:</strong> fights to the death.</p>",
  folder=F["a_creatures"], senses=[{"type":"low-light-vision"}],
  blurb="Deformed ogrekin jailer", token_src=TOK("cabbagehead"), actor_link=True))

AW("vreeg", B.npc(A["vreeg"],"Vreeg",7,24,105,13,16,17,14,
  {"str":0,"dex":4,"con":2,"int":5,"wis":1,"cha":3},25,
  {"arcana":18,"occultism":16,"deception":15,"intimidation":13,"stealth":14},
  ["humanoid","dwarf"],["common","undercommon","necril"],
  [B.strike(nid(),"Dagger",13,"1d4","piercing",["agile","finesse","thrown-10","versatile-s"]),
   B.sneak_attack(nid(),1,"Vreeg"),
   B.action(nid(),"Searing Ray","2","<p>Vreeg looses a ray of fire, making a spell attack (+16) against one creature within 60 feet for @Damage[4d6[fire]] (double on a critical hit).</p>",["concentrate","fire","manipulate"]),
   B.action(nid(),"Vampiric Touch","2","<p>Vreeg's touch (or a 30-foot spectral hand) drains life: "+chk("type:fortitude|dc:24|basic:true")+" against @Damage[3d6[void]]; Vreeg gains temporary Hit Points equal to half the damage dealt.</p>",["concentrate","manipulate","void"]),
   B.action(nid(),"Blindness","2","<p>One creature within 30 feet must succeed at a "+chk("type:fortitude|dc:24")+" or be "+B.cond("blinded","Blinded")+" for 1 minute (permanently on a critical failure, until restored).</p>",["concentrate","manipulate","necromancy"]),
   B.action(nid(),"Force Missiles","2","<p>Three darts of force unerringly strike up to three creatures Vreeg can see, dealing @Damage[1d4+1[force]] each (no save, no attack roll).</p>",["concentrate","force","manipulate"]),
   B.action(nid(),"Grave Touch","1","<p>One creature within 30 feet must succeed at a "+chk("type:fortitude|dc:24")+" or be "+B.cond("enfeebled","Enfeebled 2")+" for 1 round (1 minute on a critical failure).</p>",["concentrate","manipulate","void"]),
   B.action(nid(),"Conjure Shield","1","<p>A shimmering force shield wards Vreeg, granting a +2 circumstance bonus to AC until the start of his next turn; he can Shield Block with it (Hardness 10).</p>",["concentrate","manipulate"],"defensive"),
   B.lore(nid(),"Necromancy Lore",16),
   B.gear("dagger",nid())],
  notes="<p><strong>Role:</strong> the boss of the Dead Warrens — Rolth's gifted, insane derro apprentice, scheming to one day replace his master. <strong>Rolth himself is absent</strong> (away securing a scroll; he returns <em>after</em> the PCs leave, to find his lair in ruins — see Chapter 2).</p>"
        "<p><strong>Tactics:</strong> opens with Conjure Shield and False Life (his HP already includes it), then kites with Searing Ray, Force Missiles, and Vampiric Touch, saving Blindness for a martial threat. <strong>Weakness:</strong> dazzled in bright light (derro sunlight vulnerability). His attendant zombie covers his retreat.</p>",
  folder=F["a_creatures"], senses=[{"type":"darkvision"}], other_speeds=[{"type":"fly","value":30}], size="sml",
  blurb="Derro necromancer; the warrens' master", token_src=TOK("vreeg"), actor_link=True))

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

HW("acid-spraying-skulls", B.hazard(A["acidskulls"],"Acid-Spraying Skulls",3,25,
  "<p>"+chk("type:perception|dc:25")+" to notice the faint magical aura on the wall-mounted skulls before they fire.</p>",
  "<p>"+chk("type:thievery|dc:25")+" to disarm a skull (or <em>dispel magic</em> vs. a 3rd-rank effect).</p>",
  "<p>Several skulls set into the walls of the necrophidius corridor (D6) are a magical trap. Rolth and the derros slip through before it triggers.</p>",
  [B.action(nid(),"Acid Spray","reaction","<p><strong>Trigger</strong> A creature has been in the corridor for 2 rounds.</p><hr /><p><strong>Effect</strong> Every creature in the hall is sprayed with acid, taking @Damage[3d6[acid]] ("+chk("type:reflex|dc:22|basic:true")+"). The trap resets automatically after 10 minutes.</p>")],
  folder=F["a_hazards"], traits=["magical","trap"], reset="<p>Automatic, after 10 minutes.</p>", complex_=False))

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
           "A11","A12","A13","A14","npcs","treasure","conv",
           # Part Two — A City Gone Mad
           "cgm","e1","e2","e3","e4","e5","e6","e7","e8","e9","e10","e11","e12","e13","e14",
           # Part Three — Blood and Bones: B. All the World's Meat
           "bmeat","B1","B2","B3","B4","B5","B6","B7","B8",
           # Part Three — C. Eel's End
           "cend","C1","C2","C3","C4","C5","C6","C7","C9","C13","C14","C15","C17",
           # Part Three — D. The Dead Warrens + Chapter Conclusion
           "dwarrens","D1","D2","D3","D4","D5","D6","D7","D8","D9","D10","D11","D12","D13","dconc"]
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

# =====================================================================
# PART TWO — A CITY GONE MAD (street events, run in any order)
# =====================================================================
def xpb(levels, pl):
    e = B.encounter(levels, party_level=pl); return f"{e['band']} · {e['xp']} XP @ L{pl}"
def ev(key, title, html): pages.append(newpage(key, title, html))

ev("cgm","A City Gone Mad",
  B.s_milestone("<p><strong>Part Two.</strong> The PCs emerge from the fishery to find King Eodred II dead and Korvosa in flames. Run these events in any order, across the ~month the chapter spans — there is no fixed schedule. No maps are provided: each event happens wherever the party is.</p>")
  +box("CGM","<p>Smoke rises on the horizon (or, by night, the flicker of fires); alarm bells clang over screams, the clash of steel, and the periodic detonation of arcane power. A wing of Sable Company hippogriff riders sweeps toward Castle Korvosa; one wounded mount crashes into a statue. A herald cries 'The king is dead! Long live the queen!' — answered by 'Hang the queen!' The city has gone mad.</p>")
  +"<p>Use the <strong>Korvosa (Anarchy)</strong> city statistics now — see the Conversion Guide journal → <em>Korvosa: Reputation &amp; City Tiers</em>. Korvosa stays in turmoil until the PCs begin Part Three.</p>"
  +SEC("<p><strong>How the king really died (GM only).</strong> Ileosa had her stepbrother-in-law Venster coat the king's playing cards with <em>fool's leprosy</em>, a Red Mantis poison that mimics a fast leprosy and so <strong>resists</strong> <em>remove disease</em>. No one realized it was poison, not sickness; a <em>neutralize poison</em> would have saved him. The body is sealed in the royal crypt and crumbles too fast for <em>speak with dead</em>; by the time anyone could attempt <em>resurrection</em>, his soul is judged and beyond mortal magic. These stay mysteries for now.</p>")
  +B.s_skill("<p><strong>Investigating the Queen.</strong> "+chk("type:society|dc:15")+" or "+chk("type:diplomacy|dc:20")+" (gather information) recalls common knowledge: Ileosa Arvanxi, born in Chelish Westcrown, scandalized her family to marry the aging Eodred II after a short courtship, and openly disdains Korvosa as 'a backwater colonial village.' Her true feelings — and her crimes — stay hidden this early. See the rumor table in your AP book (Appendix 2).</p>")
  +B.s_conv("<p>Before Event 11, make sure the PCs have heard rumors that the king was murdered — these rile the city and set up the Queen's Scapegoat.</p>"))

ev("e1","Event 1. A Return to Zellara's Home",
  "<p>If the PCs return to Zellara's home, they find it abandoned for weeks — furniture in dust-covered pieces, no sign of the woman or her belongings. (They already found her severed head in "+pg(P["A14"],"A14")+".)</p>"
  +SEC("<p>If the PCs carry "+itm("harrowdeck","Zellara's harrow deck")+", now is the moment for her spirit to manifest via the deck's <em>major image</em>, explain the truth of her death, and reveal the deck's powers — the recurring <strong>Harrowing</strong> (Conversion Guide journal → <em>The Harrowing</em>). If they lack the deck, she manifests one last image to steer them back to the fishery to recover it. Going forward she speaks only through the deck.</p>"))

ev("e2","Event 2. The Mysterious Brooch",
  "<p>When the PCs investigate "+itm("brooch","the brooch")+" from Gaedren's stash, "+chk("type:society|dc:15")+" recognizes it as the queen's. Any merchant they approach knows it instantly — it is registered with the Korvosan Guard as stolen, and the queen has offered a reward. The merchant advises returning it to Castle Korvosa to claim <strong>1,200 gp</strong>.</p>"
  +B.s_conv("<p>Following this up triggers "+pg(P["e8"],"Event 8: Long Live the Queen!")+" — the PCs' first audience with their future archenemy.</p>"))

ev("e3","Event 3. The Mad Prophet",
  "<p>A wild-haired, sick-looking lunatic fixates on one PC, screaming that the character will 'near death during a time of great sickness' in Korvosa's darkest hour. His ravings are nonsense — but the disease he carries is not.</p>"
  +B.enc("The Mad Prophet",xpb([-1],2),
     "<p>One "+act("mad_prophet","mad prophet")+". If he Grabs the PC he is obsessed with, that PC is exposed to <strong>Filth Fever</strong> ("+chk("type:fortitude|dc:16")+"). This is a disease vector, not a real fight.</p>",
     B.aside_token([act("mad_prophet","Mad Prophet (−1)")], img=TOK("mad-prophet"))))

ev("e4","Event 4. Imps and Dragons",
  "<p>Imps loosed by failed Acadamae summonings are a constant Korvosan menace, kept in check by the native house drakes. In the chaos, a pair of "+B.mon("imp","imps")+" swoops down to rob and savage the PCs. On the second round, four "+B.mon("house-drake","house drakes")+" arrive to attack the imps — likely saving the party.</p>"
  +B.enc("Imps (house drakes intervene)",xpb([B.mon_lvl("imp"),B.mon_lvl("imp")],2),
     "<p>2 "+B.mon("imp","imps")+" attack; the 4 "+B.mon("house-drake","house drakes")+" are <strong>allies</strong> that arrive round 2 and rarely linger. A saved drake may heal a PC as thanks.</p>"
     +"<p><strong>Scaling:</strong> repeat freely — add imps or delay the drakes for a harder fight (3–4 imps → "+xpb([B.mon_lvl("imp")]*3,2)+" to "+xpb([B.mon_lvl("imp")]*4,2)+").</p>",
     B.aside_token(["2× "+B.mon("imp","Imp (1)"), "4× "+B.mon("house-drake","House Drake (1)")+" (allied)"])))

ev("e5","Event 5. Meet the Mob",
  "<p>Rioting laborers roam in mobs, battering anyone in finery with cries of 'Die, dandy!' and 'Death to the false queen!' The PCs come on a mob surrounding "+act("amin","Amin Jalento")+", a young nobleman. A burly woman jeers about her brother's dock-crushed arm — 'Wanna know what it feels like?' If the PCs do not intervene, the mob attacks Amin.</p>"
  +B.s_skill("<p>"+chk("type:diplomacy|dc:18")+" or "+chk("type:intimidation|dc:18")+" disperses the mob long enough for Amin to escape — otherwise it is a fight against six rioters.</p>")
  +B.enc("Riot mob + Amin Jalento",xpb([-1]*6,2),
     "<p>6 "+act("rioter","rioters")+" (fragile mooks — each flees the instant it takes damage; the mob routs fast). "+act("amin","Amin")+" is a non-combatant who fights only defensively and flees when he can.</p>"
     +B.s_treasure("<p><strong>Reward:</strong> save Amin and he gives the party a gold ring worth <strong>250 gp</strong> (award XP as if the mob were defeated).</p>"),
     B.aside_token(["6× "+act("rioter","Rioter (−1)"), act("amin","Amin Jalento (1, non-combatant)")], img=TOK("korvosan-rioter"))))

ev("e6","Event 6. The Drunken Guard",
  "<p>The PCs run across "+act("grau","Grau Soldado")+" — a Korvosan Guard watch sergeant, once Vencarlo Orisini's prize student, now drunk and despondent in a tavern or staggering the streets. He bemoans the end of Korvosa; the king's death hit him hard, the riots harder.</p>"
  +B.s_skill("<p>"+chk("type:society|dc:18")+" recognizes the well-liked sergeant he was. Commiserate ("+chk("type:diplomacy|dc:20")+", or Deception vs. his Perception) and he sobers; a <em>lesser restoration</em> does it instantly. The right move is to escort him to Citadel Volshyenek, where the Guard cleans him up. If the PCs mock him, he challenges them to a duel (he relocates to a back alley if asked; the Guard breaks up a public fight in 3d6 rounds).</p>")
  +B.enc("Grau Soldado (duel — defuse, don't kill)",xpb([4],3),
     "<p>A single, skilled but "+B.cond("sickened","Sickened")+"-drunk duelist. He limits attacks to the PC who accepted the duel; if another PC strikes him he cries 'Foul!' and flails at random foes, provoking reactions. <strong>Morale:</strong> surrenders rather than dies.</p>"
     +B.s_treasure("<p><strong>Reward:</strong> get him back to the Guard intact and he becomes a grateful recurring ally (award XP as if defeated). His +1 striking mithral longsword is the only thing of value he still owns.</p>"),
     B.aside_token([act("grau","Grau Soldado (4)")], img=TOK("grau-soldado"))))

ev("e7","Event 7. Otyugh Uprising",
  "<p>Something has driven a filth-feeder up from the sewers into an alley, thoroughfare, or shop basement where the PCs happen to be.</p>"
  +B.enc("Otyugh",xpb([B.mon_lvl("otyugh")],2),
     "<p>A single "+B.mon("otyugh","otyugh")+" lashes out with its tentacles, grabbing and dragging prey toward its filthy maw (beware its disease).</p>",
     B.aside_token([B.mon("otyugh","Otyugh (4)")])))

ev("e8","Event 8. Long Live the Queen!",
  "<p>Returning "+itm("brooch","the brooch")+" (or otherwise seeking an audience) brings the PCs to Castle Korvosa, locked tight and bristling with crossbows. "+chk("type:diplomacy|dc:18")+" smooths their approach; mentioning the queen's missing brooch speeds things along.</p>"
  +"<p>The PCs are granted a brief audience with <strong>Queen Ileosa</strong> and her bodyguard <strong>Sabina Merrin</strong> — the party's first look at their future archenemy. Ileosa is gracious in public.</p>"
  +B.s_treasure("<p><strong>Reward:</strong> Sabina hands over a silver chest (worth 50 gp) holding 12 gold ingots stamped with the royal seal — 100 gp each (<strong>1,200 gp</strong> total). Grant <strong>800 XP</strong> for meeting the queen and returning the brooch.</p>")
  +B.s_conv("<p>This audience is the linchpin: the queen now knows the PCs by face. Everything from "+pg(P["e9"],"Event 9")+" onward flows from the Korvosan Guard noticing capable heroes.</p>"))

ev("e9","Event 9. Welcome to the Guard",
  "<p>As the PCs prove themselves on the streets, <strong>Field Marshal Cressida Kroft</strong> of the Korvosan Guard summons them to <strong>Citadel Volshyenek</strong>. Overstretched and cut off from her scattered officers, she enlists the party as trusted free agents — the relationship that drives the rest of the chapter.</p>"
  +B.s_conv("<p>Cressida is the PCs' patron and quest-giver for "+pg(P["e10"],"Event 10")+", "+pg(P["e11"],"Event 11")+", and "+pg(P["e13"],"Event 13")+". Establish her as sympathetic, principled, and stretched thin.</p>"))

ev("e10","Event 10. The Ambassador's Secret",
  "<p>Cressida needs leverage: scandalous letters held by <strong>Devargo Barvasi</strong>, the 'King of Spiders,' at his floating den <strong>Eel's End</strong>. She hands the PCs a pouch of <strong>1,000 gp</strong> to buy them; "+chk("type:diplomacy|dc:24")+" talks her up to 1,500 gp. Vencarlo Orisini offers to escort the party as far as Old Korvosa.</p>"
  +B.s_treasure("<p><strong>Reward:</strong> deliver the letters and Cressida adds <strong>500 gp</strong>. If the King of Spiders is dead, she can't legally pay more — instead she awards each PC the <em>drake's mark</em>, a medal worth 400 gp that grants a <strong>+2 circumstance bonus to Diplomacy</strong> with citizens of Korvosa when worn openly.</p>")
  +B.s_conv("<p>This is the hook into Part Three's Eel's End (area C). The bribe money matters — it is the PCs' lever on Devargo.</p>"))

ev("e11","Event 11. The Queen's Scapegoat",
  "<p>To bury the regicide rumors, Ileosa picks a scapegoat: "+act("trinia","Trinia Sabor")+", a young artist who painted the king's portrait weeks before his death. A tortured guard's false confession (and the guard's subsequent 'suicide,' propelled by Sabina) sets a city-wide hunt and fresh riots — this time crying for the 'assassin's' death.</p>"
  +SEC("<p><strong>GM:</strong> Trinia is innocent; Ileosa's jealousy (amplified by Kazavon's wrath) chose her. This is also the seed of the <strong>Gray Maidens</strong>, Ileosa's coming order of warrior-women.</p>")
  +"<p>Cressida, alone among the officers doubting the confession, begs the PCs to reach Trinia <em>first</em> — before the mob, the Hellknights of the Order of the Nail, or the queen's guards — and bring her in safely for a fair, magical interrogation. Her last known address: a flat in <strong>Midland, 42 Moon Street</strong>, in the slum-tangle of the Shingles. Reward: <strong>1,000 gp</strong>.</p>"
  +B.s_conv("<p>Proceed to "+pg(P["e12"],"Event 12: Into the Shingles")+".</p>"))

# --- Event 12: the Shingles chase (PF2e Chase subsystem) ---
_OBST = [
 ("Cluttered rooftop","acrobatics",15,"athletics",18),("Crumbling rooftop","athletics",18,"acrobatics",20),
 ("Gap in the wall","acrobatics",18,"athletics",20),("Hidden shortcut","perception",18,"acrobatics",20),
 ("Narrow hole in a wall","athletics",20,"acrobatics",23),("Narrow rooftop leap","acrobatics",18,"athletics",20),
 ("Burst of stirges","intimidation",18,"perception",20),("Tightrope shortcut","acrobatics",20,"athletics",23),
 ("Very hidden shortcut","perception",23,"athletics",25),("Very steep roof","athletics",15,"acrobatics",18),
 ("Avoid a drain-spider nest","survival",18,"nature",20),("Surly rooftop vagrant","intimidation",15,"deception",18),
 ("Jagged nails","perception",15,"acrobatics",18),("Cranky rooftop tomcat","nature",15,"diplomacy",18),
 ("Tangle of debris","thievery",15,"athletics",18)]
_obst_rows = "".join(f"<tr><td>{i}</td><td>{n}</td><td>{chk(f'type:{s1}|dc:{d1}')} or {chk(f'type:{s2}|dc:{d2}')}</td></tr>"
                     for i,(n,s1,d1,s2,d2) in enumerate(_OBST,1))
ev("e12","Event 12. Into the Shingles",
  "<p>The PCs slip into Midland and reach 42 Moon Street. Trinia's neighbors shelter her and send up an alarm when the party is spotted (each of 2d6 neighbors can be won over with Deception vs. their Perception +3). Her third-floor flat is barricaded: "+chk("type:athletics|dc:18")+" forces the door — every round of delay is a head start.</p>"
  +box("E12FLAT","<p>A one-room flat — bedroom, kitchen, and painter's studio in one. Bread and cheese sit by full waterskins; an easel holds a half-finished painting of an imp and a house drake fighting atop a church steeple. A single window looks out over the tangled rooftops, a low bed beneath it.</p>")
  +SEC("<p>Warned, "+act("trinia","Trinia")+" casts a <em>Figment</em> of herself asleep in bed and creeps out the window — "+chk("type:perception|dc:17")+" to notice her slipping away (+2 circumstance if looking out the window); 4 unnoticed rounds and she escapes outright. Caught unbarricaded but warned, "+chk("type:perception|dc:13")+" spots her grabbing her dagger and wand before she leaps. Surprised in her sleep, she flees empty-handed.</p>")
  +"<p><strong>The Shingles Chase</strong> (PF2e Chase subsystem). Run 15 obstacles; each PC attempts the listed skill on their turn to advance a chase point. "+act("trinia","Trinia")+" starts with a 0/3/5-obstacle lead depending on how thoroughly she was warned. A PC who fails badly <strong>falls to the street</strong>: take @Damage[2d6[bludgeoning]] and either "+chk("type:athletics|dc:16")+" to climb back, or "+chk("type:athletics|dc:16")+" / "+chk("type:reflex|dc:16")+" through the alleys to advance one obstacle. Catch her on the same obstacle and Grapple to end the chase; she escapes if she clears obstacle 15.</p>"
  +"<table><thead><tr><th>#</th><th>Obstacle</th><th>Overcome</th></tr></thead><tbody>"+_obst_rows+"</tbody></table>"
  +B.s_treasure("<p><strong>Rewards:</strong> catching Trinia earns XP as if defeated, however the PCs then choose to handle her. Turn her over to Cressida → <strong>1,000 gp</strong>; hide her or let her go (Cressida quietly approves) → <strong>2,000 gp</strong> paid later, folded into the "+pg(P["e13"],"Event 13")+" reward to hide the money trail; hand her to the queen → 200 pp and an invitation to her execution.</p>")
  +B.s_conv("<p>Trinia is innocent and a recurring ally. If she is hidden (Cressida calls in Vencarlo to spirit her to Old Korvosa), she is safe for the rest of the chapter, and the queen simply announces that another 'captured assassin' has been apprehended instead.</p>"))

ev("e13","Event 13. A Missing Body",
  "<p>With the scapegoat in hand, the city calms — but a group of racist thugs murdered a young Shoanti during the unrest. Their elder, the visionary <strong>Thousand Bones</strong>, comes to Citadel Volshyenek to demand his grandson Gaekhen's body be recovered and returned, or Shoanti–Korvosan tensions will boil over.</p>"
  +B.s_treasure("<p><strong>Reward:</strong> 1,000 gp (Cressida folds Trinia's deferred 2,000 gp in here too, if applicable). Recovering the body is a gesture of good will that pays off across the campaign.</p>")
  +B.s_conv("<p>Thousand Bones and the Shoanti debt seeded here pay off in Chapter 4 (A History of Ashes). Build the relationship now.</p>"))

ev("e14","Event 14. A Lovely Day for an Execution",
  "<p>The chapter's climax: once all other plots resolve, the queen stages the public execution of her scapegoat (Trinia, or another). Set the date so the PCs can finish Part Three (the Dead Warrens) first — there is wiggle room.</p>"
  +SEC("<p>Whether the PCs disrupt the execution, attend it, or let it proceed, this is the hand-off to the <strong>Chapter Conclusion</strong> and Chapter 2. As the chapter ends, the first cases of <strong>Blood Veil</strong> appear in the gutters — see the Conversion Guide journal → <em>Blood Veil &amp; the Epidemic Clock</em>.</p>")
  +B.s_conv("<p>This is the natural seam to begin the persistent-plague overlay: the Epidemic Clock starts in Chapter 2, seeded by how the city fared here.</p>"))

# =====================================================================
# PART THREE — BLOOD AND BONES: B. All the World's Meat (22 Stirge St.)
# Party ~L3. Cow Hammer Boys L2 · Verik L4 · Reefclaw/Raktavarna official L1.
# =====================================================================
ev("bmeat","B. All the World's Meat",
  B.s_milestone("<p><strong>Part Three.</strong> The chapter's three investigation sites — a butcher's shop (B), Eel's End (C), and the Dead Warrens (D). <strong>All the World's Meat</strong> is an abandoned butcher's shop at 22 Stirge Street, seized by deserter sergeant "+act("verik","Verik Vancaskerkin")+" and four "+act("cowhammer","Cow Hammer Boys")+" who front 'free meat for the hungry' while secretly murdering marks-for-hire and butchering the bodies into the next day's handouts.</p>")
  +B.s_skill("<p>"+chk("type:diplomacy|dc:15")+" (gather information) on the street learns the gang calls itself the Cow Hammer Boys and hires out as muscle — ask for 'the night's special cuts' (50 gp per beating).</p>")
  +SEC("<p><strong>GM:</strong> Verik is a dupe. His 'Vudrani lover Meliya Arkona' is the rakshasa <strong>Vimanda</strong>, infiltrating Korvosa for the Arkona family (who scheme to topple Ileosa with a puppet prince). The silver dagger in "+pg(P["B8"],"B8")+" is her "+B.mon("raktavarna","raktavarna")+" spy. Taking Verik alive and chasing 'Meliya' seeds the Arkona arc of Chapter 3 — Glorio/Bahor begins watching the PCs.</p>"))

area("B1","Shop Front", SR("B1","46")
  +box("B1","<p>A sign bearing the image of a fat, smiling cow hangs above the entrance. A long counter runs over half the room; beyond it a door stands ajar. A low bench sits against the east wall, and a marble-topped table to the north displays cuts of meat before a grimy window, flies circling above.</p>")
  +"<p>Two "+act("cowhammer","Cow Hammer Boys")+" — Baldrago and Malder — hand out meat by day. Unless the PCs pose as needy locals they are gruffly told to 'kick off'; 'the night's special cuts' ends the hostility and opens the mercenary pitch. They never let anyone up to Verik. Push past them and they raise longbows and shout to "+pg(P["B4"],"B4")+" for help.</p>"
  +B.enc("Cow Hammer Boys (front)",xpb([2,2],3),
     "<p>2 "+act("cowhammer","Cow Hammer Boys")+" open with longbows, closing to clubs only if forced. Reinforced by the two in "+pg(P["B4"],"B4")+" if the alarm goes up.</p>",
     B.aside_token(["2× "+act("cowhammer","Cow Hammer Boy (2)")], img=TOK("cow-hammer-boy"))))

area("B2","Hall", SR("B2","46")
  +"<p>A short hall; the stairs lead up to the "+pg(P["B7"],"break room (B7)")+".</p>")

area("B3","Meat Locker", SR("B3","46")
  +box("B3","<p>The air is stale, stinking of day-old meat and blood. Straw litters the floor beneath meat hooks affixed to walls and ceiling. A blood-stained table and two salt barrels stand to the north; double doors to the south are barred by an iron bar that runs along the ceiling to a floor-to-ceiling pole.</p>")
  +SEC("<p><strong>The horror.</strong> Salted meat hangs overnight here. Among the pork and beef, "+chk("type:medicine|dc:20")+" or "+chk("type:nature|dc:20")+" confirms at least a half-dozen cuts are not from animals at all — they are <strong>humanoid</strong>. Hard proof of the murders that breaks Verik (see "+pg(P["B8"],"B8")+").</p>"))

area("B4","Killing Floor", SR("B4","47")
  +box("B4","<p>The floor of this grim chamber is strewn with blood-stained straw, and the reek of slaughter is overpowering. Meat hooks ride a ceiling track; a great hammer rests on a permanent bloodstain in the northwest corner. A bloodstained grate covers a hole in the floor to the south, flanked by two vats of water — one boiling, one cold — with butcher blocks and a reeking cast-off vat beyond.</p>")
  +"<p>By day there is a 75% chance the other two "+act("cowhammer","Cow Hammer Boys")+" — Parns (a sadistic ex-butcher) and jittery Karralo — are here; otherwise they tend livestock in "+pg(P["B5"],"B5")+"/"+pg(P["B6"],"B6")+". The rusty grate (Hardness 10, HP 15; "+chk("type:athletics|dc:22")+" to pry/break) drops into a half-flooded sewer tunnel running east to the river.</p>"
  +B.enc("Cow Hammer Boys (killing floor)",xpb([2,2],3),
     "<p>2 "+act("cowhammer","Cow Hammer Boys")+" at work. They flee at low HP; once two of the four are dead, the rest abandon Verik.</p>",
     B.aside_token(["2× "+act("cowhammer","Cow Hammer Boy (2)")], img=TOK("cow-hammer-boy")))
  +B.enc("Reefclaws (sewer below)",xpb([B.mon_lvl("reefclaw")]*3,3),
     "<p>3 "+B.mon("reefclaw","reefclaws")+" scavenge the grisly leftovers in the tunnel. Well-fed, they attack only intruders who disturb the remains (e.g. searching for the finger). Beware a reefclaw's death-frenzy and venom.</p>",
     B.aside_token(["3× "+B.mon("reefclaw","Reefclaw (1)")]))
  +B.s_treasure("<p>"+chk("type:perception|dc:20")+" in the sewer finds a severed human finger wedged above the waterline, still wearing a fine silver-and-obsidian ring (~25 gp re-scaled) — and damning evidence of the murders.</p>"))

area("B5","Holding Pens", SR("B5","47")
  +box("B5","<p>Two foul-smelling animal pens take up most of the room, each a fenced gate around a long water trough and heaps of filthy hay. The floor is hard-packed earth.</p>")
  +B.s_treasure("<p>"+chk("type:perception|dc:20")+" finds the gang's buried mercenary stash under the southern trough: re-scaled to PF2e, about <strong>40 gp</strong> in mixed coin plus a small clutch of jewelry and gems (~30 gp). The stash itself is evidence that breaks Verik.</p>"))

area("B6","Cattle Pen", SR("B6","47")
  +box("B6","<p>This large open-air cattle pen reeks of manure and animal despite the breeze through the stockade fence. A roofed shed to the south holds a straw-filled wagon.</p>")
  +"<p>Each morning 1d6−3 cows and 1d4−2 pigs arrive (sometimes none). The skittish animals are harmless.</p>")

area("B7","Break Room", SR("B7","47")
  +box("B7","<p>A round table sits in this room, surrounded by four wooden chairs, a deck of cards on its top. An open cabinet to the southwest spills dirty clothes and blankets; four thin bedrolls lie rolled against the north wall. Stairs descend to "+pg(P["B2"],"B2")+".</p>")
  +"<p>The Cow Hammer Boys relax and sleep here. By night they play cards before flopping down where they can.</p>")

area("B8","Slaughterhouse Office", SR("B8","48")
  +box("B8","<p>A single large desk stands in the eastern part of this office, made over into a bed with a bedroll, blankets, and pillows; a chamber pot beneath it. A table and three chairs sit to the west, papers strewn across the table — one pinned down by an exquisite silver dagger.</p>")
  +"<p>Verik's quarters. He drinks and sleeps here, paranoid the Guard will come for him. He still wears his Korvosan Guard armor. If he hears fighting below he dithers for several rounds before joining — often arriving as it ends.</p>"
  +SEC("<p><strong>Verik surrenders</strong> if dropped below ~1/4 HP, "+chk("type:intimidation|dc:18")+", or — instantly — if shown the "+pg(P["B3"],"humanoid cuts")+", "+pg(P["B4"],"severed finger")+", or "+pg(P["B5"],"stash")+". Broken, he lets himself be arrested and (if made helpful) admits 'Meliya' put him up to it, though he can't say why an Arkona would care.</p>"
       "<p><strong>The silver dagger is alive.</strong> It is a "+B.mon("raktavarna","raktavarna rakshasa")+", Vimanda's shapeshifted spy. It plays dead as a normal (non-magical, non-silver) dagger, hoping a PC loots it so it can later report on them. Exposed for what it is, it reverts and fights for 1d3 rounds before Vimanda severs the link and abandons it to die.</p>")
  +B.enc("Verik Vancaskerkin + the dagger-spy",xpb([4,B.mon_lvl("raktavarna")],3),
     "<p>"+act("verik","Verik")+" fights from range with his longbow, switching to the spear only in melee. The "+B.mon("raktavarna","raktavarna")+" joins only if discovered. <strong>This fight is often skipped entirely</strong> — bring evidence and Verik folds.</p>",
     B.aside_token([act("verik","Verik Vancaskerkin (4)"), B.mon("raktavarna","Raktavarna (1, hidden)")], img=TOK("verik-vancaskerkin")))
  +B.s_treasure("<p>Loot: "+act("verik","Verik's")+" +1 striking composite longbow (the area-B permanent magic reward), chain mail, spear, and 3 minor healing potions. The silver 'dagger' is the raktavarna — do not let it travel with the party unnoticed.</p>")
  +B.s_conv("<p><strong>Story award</strong> for taking Verik alive without combat. Spared and turned, Verik can resurface as an ally; his brother <strong>Orik</strong> appears in Chapter 3. Pursuing 'Meliya' opens the Arkona thread (Ch.3).</p>"))

# =====================================================================
# PART THREE — C. EEL'S END (Devargo's floating den). Party ~L4.
# Enforcer L3 · Devargo L6 · Chittersnap L4 · thugs = Rioter L-1.
# =====================================================================
ev("cend","C. Eel's End",
  B.s_milestone("<p><strong>C. Eel's End</strong> — a warship and four moored barges of vice ruled by "+act("devargo","Devargo Barvasi")+", the self-styled King of Spiders. Cressida sends the PCs to recover blackmail letters proving the Chelish ambassador Amprei's misdeeds. <strong>The goal is the letters, not Devargo's head</strong> — the intended path is social (please him with bribes and entertainment), though stealth or force are possible (force is dangerous at this level).</p>")
  +SEC("<p><strong>A Walk with Vencarlo.</strong> Vencarlo Orisini escorts the PCs to Old Korvosa — develop him as a likable mentor; he is secretly the folk-hero <strong>Blackjack</strong> and is quietly assessing the party as a potential heir. He recurs throughout the campaign.</p>")
  +SEC("<p><strong>Devargo's fate is open.</strong> He pays his vice taxes and polices Eel's End, so the Guard leaves him be — but if the PCs kill him, the Guard quietly thanks them (no charges). <strong>Burning the barges</strong>, however, destroys the evidence and brings arson/murder prosecution. The easiest win is Diplomacy in "+pg(P["C7"],"the throne room (C7)")+".</p>")
  +B.s_skill("<p>Eel's End welcomes nearly everyone; only obvious Korvosan Guard, Hellknights, or Sable Company are turned away. Claiming Guard business but professing interest in a <em>hideout</em> (not Devargo) grants a large circumstance bonus to talk past the guards.</p>"))

area("C1","Eel's End Pier", SR("C1","50")
  +box("C1","<p>The sound of carousing booms from the elegantly painted barges moored to this long pier. Painted signs in several languages hang from ropes and pilings: 'The Twin Tigers,' 'Welcome to the Goldenhawk,' 'Dragon's Breath Corridor,' and 'The House of Clouds.' Only the largest vessel — an old warship to the south — bears no sign. Rope bridges and gangplanks link the decks.</p>")
  +"<p>The pier is the approach to "+act("devargo","Devargo's")+" floating empire. Four "+act("enforcer","Eel's End enforcers")+" loiter as security; they shake down well-dressed visitors but cave to greed.</p>"
  +B.enc("Eel's End Enforcers (pier)",xpb([3,3,3,3],4),
     "<p>4 "+act("enforcer","enforcers")+" with saps. They would much rather fleece the PCs than fight — talking past them is far cheaper than a brawl.</p>",
     B.aside_token(["4× "+act("enforcer","Enforcer (3)")], img=TOK("eels-end-enforcer"))))

area("C2","Eel's End Deck", SR("C2","51")
  +box("C2","<p>The large ship tied off to the pier bears the name <em>Eel's End</em>; its figurehead is a coiling eel with a woman's head. Drunkards and revelers dance on the open main deck, while the aft deck is clear. A pair of double doors painted with a complex spider open into the stern.</p>")
  +"<p>Four "+act("enforcer","enforcers")+" sleep in the rigging; two more guard the doors to "+pg(P["C7"],"C7")+", barring the unexpected. "+chk("type:deception|dc:20")+" (claim Devargo expects you), "+chk("type:diplomacy|dc:24")+", or "+chk("type:intimidation|dc:18")+" (the guards then nervously escort you in) gets past them.</p>"
  +B.enc("Eel's End Enforcers (deck)",xpb([3]*6,4),
     "<p>All 6 deck "+act("enforcer","enforcers")+" if a fight erupts — an <strong>Extreme</strong> brawl at this level. The whole point of Eel's End is to <em>avoid</em> this by talking or sneaking.</p>",
     B.aside_token(["6× "+act("enforcer","Enforcer (3)")], img=TOK("eels-end-enforcer"))))

area("C3","The Goldenhawk", SR("C3","51")
  +"<p>A floating flophouse (4 sp/night) run by a lisping, walleyed gnome named <strong>Tuggins</strong>, who hoards a jingling ring of keys (he has forgotten what most open). Devargo's presence keeps it relatively safe; in a fight, Tuggins hides under a bunk.</p>")

area("C4","The Twin Tigers", SR("C4","51")
  +box("C4","<p>Two hut-like structures sit atop this barge; raucous laughter and periodic roars of victory sound from within.</p>")
  +"<p>A gambling barge of dice and card games. A fine place to win (or lose) the bribe money, or to overhear rumors.</p>")

area("C5","The House of Clouds", SR("C5","51")
  +box("C5","<p>A single long structure sits atop the main deck, double doors open onto a room of throw rugs and pillows, the air thick with incense and red lantern-light. Braziers shaped as serpents and hunting birds breathe anise, rosewater, and cinnamon. Scantily clad men and women loiter on deck.</p>")
  +"<p>A brothel run by the half-elf madam <strong>Halvara</strong> (5 gp a turn; 100 gp for her personal company), rumored to be Devargo's sometime lover — so few patrons dare cause trouble.</p>")

area("C6","Dragon's Breath Corridor", SR("C6","52")
  +box("C6","<p>This once-proud vessel, the <em>Dragon's Breath</em>, has been painted gaudy red. A sign at the aft entrance reads simply, 'Pass into the Dreams of the Dragon.'</p>")
  +"<p>A dream-spider-smoke den run by <strong>Bezzeraty</strong> (5 gp entry), and the home of <strong>knivesies</strong> — Devargo's favorite blood-sport.</p>"
  +B.s_skill("<p><strong>The smoke:</strong> a minute in the haze forces a "+chk("type:fortitude|dc:18")+" or the fumes leave you "+B.cond("clumsy","Clumsy 1")+" and "+B.cond("stupefied","Stupefied 1")+" for 1 hour (no further effect for 24 hours). Bezzeraty robs anyone who passes out.</p>")
  +B.s_skill("<p><strong>Knivesies.</strong> Two players, right hands strapped down, a dagger stuck in the table between them; on a 10-count (bettors toss gold) both roll initiative and lunge. Run it as a quick contest of "+chk("type:athletics")+" or unarmed Strikes for the blade, then a Strike — first to draw blood or disarm wins. Winning games for Devargo raises your standing in "+pg(P["C7"],"C7")+".</p>"))

area("C7","Throne of Spiders", SR("C7","52-54")
  +box("C7","<p>This converted captain's cabin is a throne room, its walls thick with webs in which scuttle dozens of spiders that never leave their silk. Two oaken tables and chairs fill the floor; aft, a cobwebbed leather chair sits on a low stage. A narrow door to port hangs ajar over stairs leading below. An iron birdcage hangs from the ceiling like a chandelier.</p>")
  +"<p>"+act("devargo","Devargo Barvasi")+" holds court here from noon to a few hours past dusk, evaluating six hopeful thugs over a feast. The caged "+B.mon("house-drake","house drake")+" <strong>Majenko</strong> is his tormented plaything (he will sell it for an absurd 5,000 gp; freed — cage "+chk("type:athletics|dc:22")+" or "+chk("type:thievery|dc:25")+" — it serves its rescuer for a year). A hidden trap door before the throne ("+chk("type:perception|dc:20")+" to spot, again to find the throne-arm switch) drops a petitioner into "+pg(P["C15"],"C15")+".</p>"
  +SEC("<p><strong>Winning the letters (social).</strong> Have one PC plead the case (standing — note — on the trap door) and roll "+chk("type:diplomacy|dc:24")+"; others may Aid ("+chk("type:diplomacy|dc:18")+"). Devargo despises Intimidation (it starts a fight). Outcomes: <strong>fail badly</strong> → he springs the trap and attacks; <strong>partial</strong> → he wants gold/entertainment (bribes raise his attitude ~+1 per 10 gp; each knivesies win is worth a big step); <strong>success</strong> → he sells the last two letters for ~150 gp (a second "+chk("type:diplomacy|dc:24")+" knocks it to ~100 gp); <strong>critical</strong> → delighted, he hands them over and wishes the PCs well. <strong>Story award</strong> for getting the letters without combat.</p>")
  +B.enc("Devargo + hopeful thugs (if it turns violent)",xpb([6]+[-1]*6,4),
     "<p>"+act("devargo","Devargo")+" springs the trap door, then fights with poisoned gauntlets and Sneak Attack; he flees (invisible) below ~10 HP. The 6 hopeful "+act("rioter","thugs")+" are cowards who flee at the first damage and trip over each other. Enforcers from "+pg(P["C2"],"C2")+" arrive one per round once the alarm sounds.</p>",
     B.aside_token([act("devargo","Devargo Barvasi (6)"), "6× "+act("rioter","Hopeful Thug (−1)"), B.mon("house-drake","Majenko — caged")], img=TOK("devargo-barvasi")))
  +B.s_conv("<p>Releasing Majenko earns a story award and a loyal, information-gathering house-drake ally. The real goal remains the letters — turn them over to Cressida (Event 10 reward).</p>"))

area("C9","Shiver Brewery", SR("C9","54")
  +"<p>Cauldrons boil alcohol, water, and dream-spider venom down into <strong>shiver</strong> for the Arkonas — Devargo's standing arrangement that keeps his vice taxes paid.</p>"
  +B.s_treasure("<p>Among the empty vials sit six doses of shiver (~25 gp each in 1e; story contraband, not loot — destroying it pays off a 'Drug Addict' background hook).</p>"))

area("C13","Meeting Room", SR("C13","54")
  +box("C13","<p>A single low desk sits against the wall of this room. A large wooden door marked with a painting of a spider stands in the southern wall.</p>")
  +B.s_treasure("<p>Devargo's sea chest (his key, or "+chk("type:thievery|dc:30")+") holds his favourite treasures, re-scaled to PF2e: a jasper-studded amulet and an emerald gold necklace (art objects, ~120 gp the pair), a <strong>ring of feather fall</strong> with a jade-dragonfly cameo, a <strong>scroll of <em>blur</em></strong>, an <strong>elixir of love</strong>, two doses of <strong>dust of appearance</strong>, a mother-of-pearl horn (~10 gp), and ~60 gp in coin.</p>"))

area("C14","Devargo's Quarters", SR("C14","54")
  +"<p>Devargo retires here after midnight to read the day's slate reports and sleep — the <strong>best time to infiltrate</strong> Eel's End. <strong>The ambassador's blackmail letters are here</strong> (in his footlocker), the entire object of the mission. A stealth route avoids the throne-room confrontation entirely.</p>"
  +B.s_conv("<p>However the PCs obtain them, the two letters go to Cressida Kroft for the Event 10 reward (and her leverage over Ambassador Amprei).</p>"))

area("C15","The Spider's Web", SR("C15","54-55")
  +box("C15","<p>This dark chamber is riddled with dizzying tunnels of thick cobweb. The floor is a sticky mass of webbing and hundreds of bones — many of them humanoid. Some webs shimmer and dance, almost reflecting rainbows.</p>")
  +"<p>The lair of "+act("chittersnap","Chittersnap")+", the ettercap who is the true source of Devargo's 'spider control,' beneath the throne's trap door. The shimmering strands are dream-spider webs: every square is difficult terrain and a "+chk("type:reflex|dc:10")+" each round avoids their contact poison.</p>"
  +B.enc("Chittersnap's den",xpb([4,B.mon_lvl("hunting-spider"),B.mon_lvl("dream-spider"),B.mon_lvl("dream-spider")],4),
     "<p>"+act("chittersnap","Chittersnap")+" (ettercap), one "+B.mon("hunting-spider","giant spider")+", and two "+B.mon("dream-spider","dream spiders")+". Kill the ettercap and every spider on Eel's End turns feral — even on Devargo.</p>",
     B.aside_token([act("chittersnap","Chittersnap (4)"), B.mon("hunting-spider","Giant Spider (1)"), "2× "+B.mon("dream-spider","Dream Spider (0)")], img=TOK("chittersnap")))
  +B.s_treasure("<p>Chittersnap hoards what falls down with its meals — the GM may seed a few coins and a minor trinket among the bones.</p>"))

area("C17","Sodden Hold", SR("C17","55")
  +box("C17","<p>This old cargo bay is partially collapsed; only a soggy section of hull remains in the center, the rest open to the river.</p>")
  +B.enc("Jigsaw Shark",xpb([1],4),
     "<p>A "+act("jigsawshark","jigsaw shark")+" (the same river-scavenger species from the Old Fishery) prowls the flooded hold — a hazard for anyone dumped through the "+pg(P["C7"],"trap door")+" who drifts down here.</p>",
     B.aside_token([act("jigsawshark","Jigsaw Shark (1)")], img=TOK("jigsaw-shark"))))

# =====================================================================
# PART THREE — D. THE DEAD WARRENS (Rolth's lab, run by Vreeg). Party ~L4.
# Derro L2 · Skeletal Owlbear L3 · Cabbagehead L3 · Vreeg L6 · Stirge L-1.
# Official: Otyugh L4, Skeleton Guard L-1, Necrophidius L3, Carrion Golem L4,
# Zombie Shambler L-1.
# =====================================================================
ev("dwarrens","D. The Dead Warrens",
  B.s_milestone("<p><strong>D. The Dead Warrens</strong> — a derro-infested undercity laboratory beneath Potter's Field, the last chapter site (the PCs recover the murdered Shoanti boy Gaekhen's body here for Event 13). Tracks at the surface ("+chk("type:perception|dc:15")+", "+chk("type:nature|dc:20")+" to read them as derro) lead to a trap-door in a mausoleum.</p>")
  +SEC("<p><strong>GM:</strong> This is one of several labs kept by the necromancer <strong>Rolth</strong> (Gaedren Lamm's estranged son, the 'Key-Lock Killer'). <strong>Rolth is absent</strong> — away securing a scroll — and is <em>not</em> scheduled to appear; he returns after the PCs leave to find his lair wrecked, and hunts them in Chapter 2. In his stead the warrens are run by his derro apprentice "+act("vreeg","Vreeg")+".</p>")
  +SEC("<p><strong>Gaekhen's body is in four parts</strong> (Rolth harvested only the head): the legs in the corpse dump ("+pg(P["D4"],"D4")+"), the torso + right arm animated in the stitchery ("+pg(P["D11"],"D11")+"), the left arm clutched by the carrion golem ("+pg(P["D8"],"D8")+"), and the head stitched to the flesh-golem in "+pg(P["D11"],"D11")+". Thousand Bones needs all four parts, not a whole body.</p>")
  +B.s_conv("<p><strong>Running the difficulty.</strong> In PF2e a lone at-level creature reads as <em>Trivial–Low</em> for four PCs, so most warren rooms are individually easy — the dungeon is an <strong>attrition gauntlet</strong>, not a string of set-piece fights. Lean into the design's own reinforcement: a "+act("derro","derro")+" who spots the party flees the "+pg(P["D2"],"crawl-spaces")+" to pull its kin (combine "+pg(P["D3"],"D3")+"/"+pg(P["D5"],"D5")+"/"+pg(P["D7"],"D7")+" derros into one Low–Moderate fight), and the "+pg(P["D1"],"ossuary")+" skeletons <em>pursue</em> — add them to a later room. The climax — "+act("vreeg","Vreeg")+" in "+pg(P["D13"],"D13")+" — is a true <strong>Severe</strong> boss.</p>"))

area("D1","Ossuary", SR("D1","56")
  +box("D1","<p>This large room is supported by four wide pillars of stone beneath a twenty-foot dome. The walls are caked with skeletons set in mud — mostly adult human bones, with smaller ones here and there. Fifteen-foot-square bone-pits sit east and west; a crude hole gouged in the south wall opens a tunnel.</p>")
  +"<p>An abandoned ossuary. Rolth animated guardians in the bone pits — four "+B.mon("skeleton-guard","human skeletons")+" (west) and a "+act("skelowlbear","skeletal owlbear")+" (east), spotted before they rise with "+chk("type:perception|dc:15")+". The skeletons pursue throughout the warrens but never up into Potter's Ward.</p>"
  +B.enc("Animated guardians",xpb([3,-1,-1,-1,-1],4),
     "<p>The "+act("skelowlbear","skeletal owlbear")+" and 4 "+B.mon("skeleton-guard","human skeletons")+" clatter up to attack.</p>",
     B.aside_token([act("skelowlbear","Skeletal Owlbear (3)"), "4× "+B.mon("skeleton-guard","Human Skeleton (−1)")], img=TOK("skeletal-owlbear"))))

area("D2","Crawl Spaces", SR("D2","56")
  +"<p>Cramped secret tunnels the derros use to flit between rooms. Each concealed door is found with "+chk("type:perception|dc:20")+". They let the derros flank, ambush, and flee to raise the alarm.</p>")

area("D3","Derro Cave", SR("D3","56")
  +"<p>The derros' filthy rest-and-mess room. Two "+act("derro","derros")+" are usually here, playing a cruel game of 'Rat Squish.' They snatch up weapons and attack the instant they notice intruders.</p>"
  +B.enc("Derros at rest",xpb([2,2],4),
     "<p>2 "+act("derro","derros")+". Others may arrive via "+pg(P["D2"],"the crawl spaces")+" if the alarm goes up.</p>",
     B.aside_token(["2× "+act("derro","Derro (2)")], img=TOK("derro"))))

area("D4","Corpse Dump", SR("D4","56-57")
  +box("D4","<p>The majority of this room contains a nasty-looking stretch of mud — a partially collapsed sinkhole kept damp by seeping water. A patch of solid ground forms an island heaped with a reeking pile of body parts. A rickety wheelbarrow lies on its side to the north.</p>")
  +"<p>An "+B.mon("otyugh","otyugh")+" Rolth lured here to dispose of the derros' grisly discards wallows in the mud. It cries 'Warm food!' and lumbers out to attack.</p>"
  +B.enc("Otyugh",xpb([B.mon_lvl("otyugh")],4),
     "<p>One "+B.mon("otyugh","otyugh")+" — grab-and-drag, plus its filth-borne disease.</p>",
     B.aside_token([B.mon("otyugh","Otyugh (4)")]))
  +B.s_treasure("<p>Among the body parts: <strong>Gaekhen's tattooed legs and hips</strong> (one of four body parts). "+chk("type:perception|dc:25")+" sifting the mud also turns up trinkets — an amber necklace (~35 gp re-scaled), a silver dagger, a sealed <strong>elixir of vision</strong>, a <strong>wand of spiritual weapon</strong>, and a <strong>ring of swimming</strong>.</p>"))

area("D5","Exsanguination Chamber", SR("D5","57")
  +box("D5","<p>Three wooden tables stand in the middle of this room, their surfaces stained red. To the east, a ten-foot-wide hutch with wicker doors opens onto a straw-lined cage.</p>")
  +"<p>A lone "+act("derro","derro")+" drains a fresh corpse with Rolth's blood-tools — a hutch of "+act("stirge","stirges")+". She shrieks, flings open the hutch, and flees through "+pg(P["D2"],"the crawl spaces")+" to warn "+pg(P["D3"],"D3")+". Four gorged stirges on the body ignore the PCs; two hungry ones attack.</p>"
  +B.enc("Derro + stirges",xpb([2,-1,-1],4),
     "<p>1 "+act("derro","derro")+" (flees to raise the alarm) + 2 hungry "+act("stirge","stirges")+".</p>",
     B.aside_token([act("derro","Derro (2)"), "2× "+act("stirge","Stirge (−1)")], img=TOK("stirge"))))

area("D6","Necrophidius Corridor", SR("D6","57")
  +"<p>A corridor lined with skulls. Two of them are the heads of "+B.mon("necrophidius","necrophidiuses")+" — silent skeletal serpents Rolth crafted from old victims — coiled motionless in the walls until the room's trap springs, then striking with surprise.</p>"
  +"<p>The "+haz("acidskulls","Acid-Spraying Skulls")+" trap fires two rounds after a creature enters; Rolth and the derros dart through before it triggers (door to "+pg(P["D7"],"D7")+" ↔ secret door to "+pg(P["D2"],"D2")+").</p>"
  +B.enc("Necrophidiuses (+ acid trap)",xpb([B.mon_lvl("necrophidius"),B.mon_lvl("necrophidius")],4),
     "<p>2 "+B.mon("necrophidius","necrophidiuses")+" (their dance can stun) plus the "+haz("acidskulls","acid-skull")+" trap raking the whole hall.</p>",
     B.aside_token(["2× "+B.mon("necrophidius","Necrophidius (3)"), haz("acidskulls","Acid-Spraying Skulls (3)")])))

area("D7","Alchemy Lab", SR("D7","58")
  +box("D7","<p>The wooden tables here are stacked with vials, beakers, and alchemical gear; the southern one is heaped with broken glass and leans on a hastily repaired leg. Three cauldrons sit against the east wall, one upended, its rancid rendered-fat contents spilled across the floor.</p>")
  +"<p>The fourth "+act("derro","derro")+" minion cleans up after a "+pg(P["D8"],"carrion golem")+" smashed through earlier. He dithers in confusion for a round, unsure whether to fight or run for help.</p>"
  +B.enc("Lone derro",xpb([2],4),
     "<p>1 "+act("derro","derro")+", caught off balance.</p>",
     B.aside_token([act("derro","Derro (2)")], img=TOK("derro")))
  +B.s_treasure("<p>"+chk("type:perception|dc:20")+" (10 minutes' search) recovers usable salvage: an alchemist's lab, 3 doses of <strong>vermin repellent</strong> (Rolth is Gaedren's source for it), 2 tanglefoot bags, 4 doses of black adder venom, a hybridization funnel, 2 doses of silversheen, and a <strong>handy haversack</strong> holding 3 potions of healing, a lesser restoration potion, a potion of invisibility, 2 scrolls of <em>false life</em>, and a scroll of <em>dispel magic</em>.</p>"))

area("D8","Store Room", SR("D8","58")
  +"<p>A locked store room. Early this morning Rolth's newest "+B.mon("carrion-golem","carrion golem")+" went berserk, tore from its table, and rampaged through "+pg(P["D7"],"D7")+" before he trapped it in here — the delay is why he is absent today. Open the door and it attacks at once, still clutching a tattooed severed arm.</p>"
  +B.enc("Carrion Golem",xpb([B.mon_lvl("carrion-golem")],4),
     "<p>One berserk "+B.mon("carrion-golem","carrion golem")+" — a patchwork construct of rotting parts.</p>",
     B.aside_token([B.mon("carrion-golem","Carrion Golem (4)")]))
  +B.s_treasure("<p>The arm the golem clutches is <strong>Gaekhen's left arm</strong> (a third body part), marked with Shoanti tattoos.</p>"))

area("D9","Prisoner Pits", SR("D9","58-59")
  +box("D9","<p>This foul-smelling cavern is bordered on three sides by ten-foot-deep pits reeking of excrement and decay. Each holds moldy straw, a trough of filthy water, rotting body parts — and a couple of still-living prisoners.</p>")
  +"<p>Six malnourished captives await Rolth's experiments. Their jailer is the ogrekin "+act("cabbagehead","Cabbagehead")+", who torments them to please his 'father' Rolth and fights to the death.</p>"
  +B.enc("Cabbagehead",xpb([3],4),
     "<p>The ogrekin "+act("cabbagehead","Cabbagehead")+" — a bare-fisted brute.</p>",
     B.aside_token([act("cabbagehead","Cabbagehead (3)")], img=TOK("cabbagehead")))
  +B.s_treasure("<p>Among the freed prisoners is the cutpurse <strong>Tiora</strong>; within a day she seeks out the PCs and gratefully gives them a <strong>wand of cure moderate wounds</strong> (34 charges).</p>"))

area("D10","Library", SR("D10","59")
  +box("D10","<p>Two wide, freestanding bookshelves furnish this room, filled with carefully arranged tomes and scrolls.</p>")
  +B.s_treasure("<p>Mostly necromancy and golem-craft treatises — plus a surprising number of books on <strong>disease and plague</strong> (a +2 circumstance bonus to relevant Recall Knowledge while using them; ominous foreshadowing of Chapter 2). The collection is worth ~30 gp re-scaled; tucked in an anatomy folio are a scroll of <em>identify</em> and a scroll of <em>command undead</em>.</p>"))

area("D11","Stitchery", SR("D11","59")
  +box("D11","<p>The nauseating mixture of decay and strange chemicals fills this room. Saws, pliers, long needles, and surgical tools line the shelves. On a sturdy central table lies a patchwork humanoid stitched from dozens of bodies — nearly seven feet tall.</p>")
  +SEC("<p>Rolth's workshop. The strapped-down flesh golem is unfinished; the small head stitched to it — brown hair, a scar on the left cheek — is <strong>Gaekhen's head</strong> (the fourth and last body part). The torso + right arm Vreeg claimed and crudely animated (2 HP, +0 unarmed for 1d3 nonlethal, 50% miss from blindness; harmed by vitality) — it thrashes if handled.</p>")
  +B.s_treasure("<p>On the desk: a broken <strong>key-shaped dagger</strong> — Rolth's signature blade, twin to the one in "+pg(P["A14"],"Gaedren's den (A14)")+", confirming the connection. The PCs may not grasp its meaning until they meet Rolth in Chapter 2.</p>"))

area("D12","Rolth's Room", SR("D12","59")
  +box("D12","<p>This chamber holds a large four-poster bed and a simple writing desk, with a full-length mirror propped against an earthen wall.</p>")
  +SEC("<p>Rolth keeps little here. "+chk("type:perception|dc:20")+" (automatic if a PC looks behind the mirror) reveals a hidden niche: masterwork thieves' tools, a pearl-and-silver snuffbox (~25 gp re-scaled) holding a dose of <strong>dust of disappearance</strong>, and a <strong>sustaining spoon</strong>. His spellbooks are not here — he carries them.</p>"))

area("D13","Vreeg's Chamber", SR("D13","59-61")
  +box("D13","<p>This chamber is part cluttered study, part nest — borrowed library books, half-finished necromantic tinkering, and the lingering chill of worked death magic.</p>")
  +"<p>"+act("vreeg","Vreeg")+" the derro necromancer lairs here, attended by a single "+B.mon("zombie-shambler","human zombie")+" bodyguard left by Rolth. He kites with rays and force missiles and saves Blindness for the front line.</p>"
  +SEC("<p><strong>The gut-punch.</strong> If the PCs left "+act("gaedren","Gaedren Lamm's")+" body in the fishery, this zombie <em>is</em> Gaedren — recovered and animated by his son Rolth. Mindless, it won't know them, but its appearance should unsettle the party and raise the question of <em>who</em> wanted the old man back in undeath.</p>")
  +B.enc("BOSS — Vreeg + zombie",xpb([6,B.mon_lvl("zombie-shambler")],4),
     "<p>"+act("vreeg","Vreeg")+" (the warrens' master) and his "+B.mon("zombie-shambler","zombie")+" guard. Bright light leaves Vreeg dazzled (derro sunlight vulnerability) — a real lever for the PCs.</p>",
     B.aside_token([act("vreeg","Vreeg (6)"), B.mon("zombie-shambler","Human Zombie / undead Gaedren (−1)")], img=TOK("vreeg")))
  +B.s_conv("<p>With Vreeg down and the four body parts gathered, the warrens are cleared. Rolth returns later to the ruin and becomes a Chapter 2 antagonist (CHG: his vendetta).</p>"))

ev("dconc","Chapter Conclusion",
  B.s_milestone("<p><strong>Chapter Conclusion.</strong> With the Dead Warrens cleared and the scapegoat's fate resolved, 'Edge of Anarchy' ends. The PCs should be well into 4th level.</p>")
  +"<p><strong>Returning Gaekhen.</strong> Deliver Gaekhen's four body parts to "+pg(P["e13"],"Thousand Bones")+" (Event 13). The grateful Shoanti elder's goodwill becomes important in Chapter 4 (A History of Ashes). Cressida pays the recovery reward (folding in Trinia's deferred coin if applicable).</p>"
  +"<p><strong>The execution.</strong> Queen Ileosa's public execution of her scapegoat ("+pg(P["e14"],"Event 14")+") is the chapter's final beat — disrupt it, attend it, or let it stand. Either way the city quiets, and the PCs are now known to the queen.</p>"
  +SEC("<p><strong>Into Chapter 2 — and the Blood Veil.</strong> As order returns, the first cases of a new plague appear in the gutters. This is where the persistent-plague overlay begins: start the <strong>Epidemic Clock</strong> (Conversion Guide journal → <em>Blood Veil &amp; the Epidemic Clock</em>) seeded by how the city fared here. Rolth, returning to his ruined lair, becomes a recurring hunter (Chapter 2).</p>")
  +B.s_conv("<p><strong>Threads carried forward:</strong> Rolth's vendetta · the Arkona/Vimanda watch (from "+pg(P["B8"],"Verik")+") · Trinia &amp; Vencarlo/Blackjack · Grau and the Korvosan Guard · the Shoanti debt · and the queen, who now has the PCs' measure.</p>"))

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
# HARROW SUBSYSTEM (CHG-0010) — mechanical overlay only; the 54 card meanings
# come from the GM's own Harrow deck (we ship no card text).
# =====================================================================
CG_JID="cotctGuide000001"; HARROW_TBL_ID="cotctHarrowTbl01"; HARROW_MAC_ID="cotctHarrowMac01"
HARROW_SUITS=[("Hammers","Strength"),("Keys","Dexterity"),("Shields","Constitution"),
              ("Books","Intelligence"),("Stars","Wisdom"),("Crowns","Charisma")]
harrow_rows=[{"_id":nid(),"range":[i+1,i+1],
              "text":f"<strong>{s}</strong> → grants a Harrow Point: reroll one <strong>{ab}</strong> check or save this chapter."}
             for i,(s,ab) in enumerate(HARROW_SUITS)]
harrow_tbl=B.rolltable(HARROW_TBL_ID,"Harrow Reading — Suit Draw","1d6",harrow_rows,
  desc="<p>Draw a suit for a PC when not dealing from a physical Harrow deck (each suit = one ability score).</p>")
B.write("rolltables","harrow-suit-draw",copy.deepcopy(harrow_tbl))

HARROW_CMD = """const suits=[['Hammers','Strength'],['Keys','Dexterity'],['Shields','Constitution'],['Books','Intelligence'],['Stars','Wisdom'],['Crowns','Charisma']];
const sel=(canvas&&canvas.tokens&&canvas.tokens.controlled)?canvas.tokens.controlled:[];
let b=`<p><strong>The Harrowing.</strong> Deal each PC a card from Zellara's Harrow deck. Each card's suit grants that PC a <em>Harrow Point</em> — one reroll this chapter on a check or save using that suit's ability score. Foreshadow events; don't spoil.</p>`;
b+=`<p><strong>Suit → ability:</strong> Hammers→Str · Keys→Dex · Shields→Con · Books→Int · Stars→Wis · Crowns→Cha.</p>`;
if(sel.length){b+='<p><strong>Random draw:</strong></p><ul>';for(const t of sel){const s=suits[Math.floor(Math.random()*6)];b+=`<li>${t.name}: <strong>${s[0]}</strong> → reroll ${s[1]} checks</li>`;}b+='</ul>';}
else{b+=`<p><em>Select PC tokens and re-run to auto-draw a suit for each, or roll the “Harrow Reading — Suit Draw” table.</em></p>`;}
ChatMessage.create({content:b,speaker:{alias:'Zellara'}});"""
harrow_mac=B.macro(HARROW_MAC_ID,"Harrow Reading",HARROW_CMD,img="icons/sundries/gaming/playing-cards.webp")
B.write("macros","harrow-reading",copy.deepcopy(harrow_mac))

# Campaign-trait backgrounds (CHG-0021) — PF2e custom backgrounds tying PCs to Korvosa
BG=[
 ("bg_betrayed","Betrayed (Korvosa)",["wis","cha"],"deception","Underworld","<p>Someone you trusted handed you to Gaedren Lamm. You learned to read people and never be caught off guard twice. <em>Recommended skill feat: Lengthy Diversion.</em></p>"),
 ("bg_drugaddict","Drug Addict (Korvosa)",["con","int"],"medicine","Drug","<p>Gaedren's shiver dens sank their hooks into you; clean or not, you know the trade and its cost. <em>Recommended skill feat: Battle Medicine.</em></p>"),
 ("bg_framed","Framed (Korvosa)",["int","cha"],"society","Korvosa","<p>Gaedren framed you for a crime you didn't commit. Clearing your name means knowing how Korvosa's law and streets really work. <em>Recommended skill feat: Streetwise.</em></p>"),
 ("bg_lovelost","Love Lost (Korvosa)",["wis","cha"],"diplomacy","Korvosa","<p>Gaedren took someone you loved. Grief sharpened into resolve — and a knack for moving people. <em>Recommended skill feat: Group Impression.</em></p>"),
 ("bg_missingchild","Missing Child (Korvosa)",["con","wis"],"survival","Korvosa","<p>A child of yours is among Lamm's Lambs. You've scoured Korvosa's underbelly searching, and learned to survive it. <em>Recommended skill feat: Forager.</em></p>"),
 ("bg_unhappy","Unhappy Childhood (Korvosa)",["dex","wis"],"thievery","Underworld","<p>You came up a street-rat under Gaedren's thumb and got out — the skills he beat into you never left. <em>Recommended skill feat: Subtle Theft.</em></p>"),
]
bgs=[]
for key,bname,boosts,skill,lore,bdesc in BG:
    _bg=B.background(A[key],bname,bdesc,boosts,skill,lore,folder=F["i_bg"])
    bgs.append(copy.deepcopy(_bg)); B.write("items",key.replace("bg_","background-"),_bg)

cg_pages=[B.page(nid(),"The Harrowing",
  B.s_desc("<p>“The cards know more than they tell.” At the start of each chapter, Zellara — and, after the Old Fishery, her haunted deck — deals the party a Harrow reading.</p>")
  +"<p><strong>What it is.</strong> A short narrative reading that <em>foreshadows</em> the chapter (a coming time of unrest; the PCs are fated heroes) and grants each PC a small luck boon. Read the omens; don't spoil concrete events.</p>"
  +"<p><strong>How to run it.</strong> Deal each PC one card from a real Harrow deck (your own — we ship no card text), or use the <strong>Harrow Reading</strong> macro / the <em>Harrow Reading — Suit Draw</em> rolltable to assign a suit. Each card's <strong>suit</strong> maps to one ability score:</p>"
  +"<ul><li><strong>Hammers</strong> → Strength · <strong>Keys</strong> → Dexterity · <strong>Shields</strong> → Constitution · <strong>Books</strong> → Intelligence · <strong>Stars</strong> → Wisdom · <strong>Crowns</strong> → Charisma</li></ul>"
  +B.s_skill("<p><strong>The boon (CHG-0010 — hero-point-style).</strong> The reading grants each PC one <strong>Harrow Point</strong> for the chapter: spend it like a Hero Point to <strong>reroll a check or save that uses the card-suit's ability score</strong> (keep the new result). Unspent Harrow Points fade at the next reading.</p>")
  +"<p><strong>Optional swap.</strong> Groups wanting a deeper subsystem can run the <em>Stolen Fate</em> Harrowing ritual instead; the suit-boon default above keeps it light.</p>"
  +B.s_conv("<p>Anchor item: "+itm("harrowdeck","Zellara's Harrow Deck")+" (recovered in the Old Fishery, inhabited by her spirit). It becomes the <strong>Harrow Deck of Many Things</strong> in Chapter 6. We ship the <em>mechanics</em> only; the 54 card meanings come from your own Harrow deck.</p>"),level=1),
 B.page(nid(),"Korvosa — Reputation, Influence & City Tiers",
  "<p>Korvosa's many point-trackers and its five settlement stat blocks all map to three official PF2e subsystems (GM Core) — built once, reused from Ch.1 on.</p>"
  +B.s_skill("<p><strong>Reputation (CHG-0013).</strong> Track the party's standing with Korvosa and each faction (Korvosan Guard, the Crown, Old Korvosa's bosses, the Shoanti, later the Gray Maidens). Deeds move Victory Points along a Reputation track (Ignored → Liked → Admired → Revered, or Disliked → Hated); standing gates favors, backup, prices, and access.</p>")
  +"<p><strong>City tiers (CHG-0012).</strong> The five Korvosa settlement stat blocks become a Reputation- and chapter-state-driven item-availability table: as the city slides (anarchy → plague → martial law) and your Reputation shifts, the level and quantity of buyable items change. The framework is Reputation tier → available item level / purchase limit; set specifics per chapter.</p>"
  +B.s_skill("<p><strong>Influence (CHG-0014).</strong> Court and social set-pieces (the doctors' soiree, dealing with Devargo, the war council, researching the queen) run as Influence encounters: each key NPC gets an Influence block — Influence DC, Discovery DCs, and thresholds → outcomes, with Resistances/Weaknesses. Built per-encounter in their chapters.</p>")
  +B.s_conv("<p><strong>Victory Points (CHG-0013):</strong> Respect / Rebellion / faction trackers → VP clocks. <strong>Rumor Mill (CHG-0012):</strong> the Korvosan rumor table is a rolltable to populate from your own Appendix 2 (we ship no rumor text) — a few entries are plot hooks, most are flavor.</p>"),level=1),
 B.page(nid(),"Campaign Backgrounds",
  "<p><strong>Tie each PC to Korvosa, not just to Gaedren (CHG-0021).</strong> The AP's campaign traits convert to six PF2e <strong>custom backgrounds</strong> — each grants ability boosts, a trained skill, a Korvosa-themed Lore, and a recommended skill feat, with a built-in hook into the city. Every PC should also carry a personal grudge against Gaedren (the shared reason Zellara's reading draws them together).</p>"
  +"<ul>"
   "<li>"+itm("bg_betrayed","Betrayed")+" — Deception + Underworld Lore</li>"
   "<li>"+itm("bg_drugaddict","Drug Addict")+" — Medicine + Drug Lore</li>"
   "<li>"+itm("bg_framed","Framed")+" — Society + Korvosa Lore</li>"
   "<li>"+itm("bg_lovelost","Love Lost")+" — Diplomacy + Korvosa Lore</li>"
   "<li>"+itm("bg_missingchild","Missing Child")+" — Survival + Korvosa Lore</li>"
   "<li>"+itm("bg_unhappy","Unhappy Childhood")+" — Thievery + Underworld Lore</li>"
   "</ul>"
  +B.s_conv("<p>Drag a background onto a PC to apply its boosts / trained skill / Lore; then add the recommended skill feat. Mechanics are ours (PF2e); the original trait flavor stays in your AP book.</p>"),level=1),
 B.page(nid(),"Blood Veil — Persistent Plague & Epidemic Clock",
  B.s_desc("<p>Blood Veil is the front end of Ileosa's blood harvest — the canon <em>Blooding</em> and the Everdawn Pool. The Chapter 2 cure <strong>suppresses</strong> the acute outbreak; the cult keeps re-seeding it at a slow burn, and it only truly ends when Ileosa falls (Ch.6). This is CHG-0011b (APPROVED, Major); it is <strong>removable</strong> at any chapter break.</p>")
  +"<p><strong>Epidemic Clock (0–10)</strong> — a single campaign-state tracker. Set its Ch.2 start from the Survivor Count (more saved → lower). It <strong>advances +1</strong> per in-city downtime week (and an extra +1 while the PCs are away in Ch.4/Ch.5), and <strong>recedes −1</strong> when they act against it (distribute the suppressant, burn a cult cell, expose a Blooding site, fund the church). It drives the Korvosa city tier (see the Reputation page): <strong>≥7 → Plagued</strong>; <strong>≤3 → recovering</strong>.</p>"
  +"<table><thead><tr><th>Clock</th><th>State</th><th>What the table feels</th></tr></thead><tbody>"
   "<tr><td>0–3</td><td>Receding</td><td>Flavor only; markets recover; grateful NPCs — the PCs' wins show.</td></tr>"
   "<tr><td>4–6</td><td>Simmering</td><td>Checkpoints; some goods scarce; minor attitude drag; one personal hook (a known NPC falls ill).</td></tr>"
   "<tr><td>7–8</td><td>Spreading (Plagued)</td><td>Harsher prices/availability; a district quarantined; lose an NPC or place; Guard support thins.</td></tr>"
   "<tr><td>9</td><td>Crisis (Martial Law)</td><td>Riots/crackdowns; a district lost; a safe haven unusable; allies pressure the party.</td></tr>"
   "<tr><td>10</td><td>Catastrophe</td><td><strong>Point of no return:</strong> the Everdawn Pool gains charges early — the Ch.6 ritual timer shortens — and/or a mass-death beat darkens the denouement.</td></tr>"
   "</tbody></table>"
  +B.s_skill("<p><strong>GM options menu</strong> (pick what hurts <em>this</em> table; telegraph one tier early): <strong>A</strong> PC infection (the disease below; Gritty/Heroic/Grim tones — always an out) · <strong>B</strong> lose an NPC (throwaway→named by tier) · <strong>C</strong> lose a place (safe house/shop/district, reversible) · <strong>D</strong> faction cost (Korvosan Guard / Abadar aid thins — ties to Reputation) · <strong>E</strong> accelerate the villain (shorter Ch.6 timer) · <strong>F</strong> moral pressure (plague vs. politics — no wrong answer).</p>")
  +"<p><strong>Blood Veil (disease).</strong> "+chk("type:fortitude|dc:20")+" (scale the DC to the chapter's level; ~20 in Ch.2). <strong>Onset</strong> 1 day. <strong>Stage 1</strong> "+B.cond("enfeebled","Enfeebled 1")+" (1 day); <strong>Stage 2</strong> "+B.cond("enfeebled","Enfeebled 2")+" and "+B.cond("drained","Drained 1")+" (1 day); <strong>Stage 3</strong> "+B.cond("enfeebled","Enfeebled 2")+" and "+B.cond("drained","Drained 2")+" (1 day); <strong>Stage 4</strong> "+B.cond("drained","Drained 3")+" and "+B.cond("enfeebled","Enfeebled 3")+". The PF1e Con+Cha damage becomes drained/enfeebled; the suppressant halts progression and steps the stage down rather than curing outright.</p>"
  +"<p><strong>Persistent in-city exposure</strong> (atmosphere, not attrition): while in Plagued-tier Korvosa, a character attempts a flat check each downtime week — "+chk("type:flat|dc:5")+" at a low clock, up to "+chk("type:flat|dc:11")+" at a high clock — on a failure, save against Blood Veil at a reduced DC. Keep it light; make the clock respond to player action.</p>"
  +B.s_conv("<p>Track the clock + city tier on this page across chapters. <strong>Removability hatch:</strong> at any chapter break the GM may rule the suppressant became a true cure (revert to faithful) with zero downstream breakage. Full design: <code>design/persistent_plague.md</code>.</p>"),level=1)]
cg_journal=B.journal_entry(CG_JID,"Conversion Guide",cg_pages,folder=None)
B.write("journals","00-conversion-guide",copy.deepcopy(cg_journal),embed_pages=True)

# =====================================================================
# ADVENTURE bundle (one-click import; embeds copies WITHOUT _key)
# =====================================================================
def strip(doc):
    d=copy.deepcopy(doc); d.pop("_key",None)
    for it in d.get("items",[]): it.pop("_key",None)
    for p in d.get("pages",[]): p.pop("_key",None)
    for n in d.get("notes",[]): n.pop("_key",None)
    for t in d.get("tokens",[]): t.pop("_key",None)
    for r in d.get("results",[]): r.pop("_key",None)
    return d
adv = B.adventure(ADV,"Curse of the Crimson Throne — Ch.1: Edge of Anarchy (pilot)",
  "modules/cotct-pf2e-conversion/assets/art/cover.webp",
  "<p>Phase-2 pilot: the Old Fishery (the hunt for Gaedren Lamm). Imports the chapter journal, the Old Fishery scene (map-note pins + staged tokens), the converted NPCs/hazards, and the treasure — organized into folders. Supply your own maps (Racooze's free CotCT battlemaps).</p>",
  [strip(f) for f in folders], [strip(intro_journal), strip(cg_journal), strip(journal)], [strip(sc)],
  [strip(a) for a in actors]+[strip(h) for h in hazards], [strip(i) for i in items]+[strip(b) for b in bgs],
  tables=[strip(harrow_tbl)], macros=[strip(harrow_mac)])
B.write("adventure","cotct-edge-of-anarchy",copy.deepcopy(adv))

print(f"Pilot (Kingmaker-style) built: {len(folders)} folders, {len(actors)} actors, {len(hazards)} hazards, "
      f"{len(items)} items, 1 journal ({len(pages)} pages), 1 scene ({len(notes)} notes / {len(tok)} tokens), 1 adventure.")
