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
B.SCOPE = (234, 2695)   # Ch.1 AP.md line range (anchor scoping)

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
# Hyphen/em-dash drops the two-column OCR fused at line breaks ("tar-caked" ->
# "tarcaked", "mud — adult" -> "mudadult"); applied to every verbatim pull.
_OCRFIX = [("tarcaked","tar-caked"),("bargethe","barge — the"),("mudadult","mud — adult"),
           ("Fifteenfoot-square","Fifteen-foot-square"),("strawlined","straw-lined"),
           ("tenfoot-deep","ten-foot-deep"),("resultsyet","results — yet"),
           ("Acharacter","A character")]
def _ocrfix(text):
    for bad, good in _OCRFIX:
        text = text.replace(bad, good)
    return text

def verbatim(anchor):
    """Chapter-scoped verbatim pull (B.SCOPE) + local OCR hyphen repairs."""
    return _ocrfix(B.verbatim(anchor))

def rawpara(anchor):
    """ONE source paragraph, normalized, chapter-scoped, with drop-cap repair but
    NO reflow merging and NO trailing-period synthesis — for stitching the
    two-column interleave back together by hand. '' if absent/unmatched."""
    a = " ".join(anchor.split())
    if not a: return ""
    paras = B._paras()
    hit = next((p for p, ln in paras if p.startswith(a) and B._in_scope(ln)), None)
    if hit is None:
        hit = next((p for p, ln in paras if a in p and B._in_scope(ln)), None)
    if hit is None:
        if B.SCOPE is not None and any(a in p for p, ln in paras):
            print(f"  [verbatim] anchor matches only OUTSIDE chapter scope {B.SCOPE}: {a[:50]!r} -> fallback used")
        return ""
    return _ocrfix(re.sub(r'^([B-HJ-Z]) ([a-z])', r'\1\2', hit))

def vbox(anchors, fallback_html, label=None):
    """Multi-paragraph speech/read-aloud box: each anchor pulls one verbatim
    paragraph (reflow-merged); falls back to an original paraphrase if any is
    missing. `label` renders as a bold lead inside the box."""
    parts = [verbatim(a) for a in anchors]
    head = f'<p class="subhead"><strong>{label}</strong></p>' if label else ""
    if all(parts):
        return B.s_read(head + "".join(B.parafy(dcfix(p)) for p in parts))
    return B.s_read(head + fallback_html)
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
 "C9":"Two large wood-burning stoves are built into",
 "C10":"foul-smelling room is empty, save for a mound",
 "C12":"Crates and barrels, and furniture in need",
 "C13":"single low desk sits against the wall of this room",
 "C14":"wooden chamber is clean and dry",
 "C15":"dark chamber is riddled with dizzying tunnels",
 "C16":"water floods this filthy bilge",
 "C17":"old cargo bay is partially collapsed",
 # Part Three, area D — The Dead Warrens
 "D1":"large room is supported by four wide pillars of stone",
 "D3":"Rank with the stink of sweat and mud",
 "D4":"majority of this room contains a nasty-looking stretch of mud",
 "D5":"Three wooden tables stand in the middle of this room",
 "D6":"walls and ceiling of this tall hallway",
 "D7":"wooden tables here are stacked with vials, beakers",
 "D8":"room, once a pantry, is in shambles",
 "D9":"foul-smelling cavern is bordered on three sides",
 "D10":"Two wide, freestanding bookshelves furnish this room",
 "D11":"nauseating mixture of decay and strange chemicals",
 "D12":"chamber holds a large four-poster bed and a simple writing desk",
 "D13":"dry, well-kept chamber contains a narrow bed",
}
def box(code, fallback_html):
    """Read-aloud section: exact AP text if the source file is present, else paraphrase."""
    t = verbatim(RABOX.get(code, ""))
    return B.s_read(B.parafy(t)) if t else B.s_read(fallback_html)

def _tc(s):  # title-case that respects apostrophes ("ZELLARA'S HOME" -> "Zellara's Home")
    return re.sub(r"[A-Za-z][A-Za-z']*", lambda m: m.group(0)[0].upper()+m.group(0)[1:].lower(), s)

# OLLIEBIRD DC ALIGNMENT (research/olliebird/ch1.txt + ch2.txt Blood Veil = DC authority):
# applied 49 rulings (48 ch1 DC sets — 8 more already matched — + the Blood Veil
# Fort 24–30 band w/ crit-fail-skips-onset in the Conversion Guide), added 13 new
# checks, skipped 5: hardness/HP/BT figures (not DCs); Grau "Make an Impression/
# Lie" has no DC; C7 bribe-attitude framework has no DC; creature/template
# substitutions out of scope; C6 smoke "Stupefied 2" is an effect, not a DC.
# Convert PF1e DC references that appear inside the verbatim source prose into
# PF2e @Check enrichers (clickable). PF1e skills/saves -> PF2e equivalents; DCs
# re-judged to PF2e, not transliterated. Extend as new chapters surface more.
_DCFIX = [
    (r"a successful DC\s*12\s*Knowledge \(local\) check", "a successful @Check[type:society|dc:15] check"),
    (r"a DC\s*25\s*Will save",                            "a @Check[type:will|dc:20|basic:false] save"),
    (r"a successful DC 20 Diplomacy check",               "a successful @Check[type:diplomacy|dc:20] check"),
    # PF1e-isms / alignment-isms surfaced by the audit (patterns match source text;
    # replacements are ours) — keep each matched run ≤ 8 source words.
    (r"spends 1d3 hours asking around",                   "spends a few hours Gathering Information"),
    (r"54 possible combinations of ability score and alignment",
     "54 cards, each tied to an ability score and a temperament (PF2e drops alignment)"),
    (r"that PCs' alignment and highest ability score",    "that PC's outlook and highest ability score"),
    (r"As Zellara was neutral in life[^.<]*\.",
     "Zellara's spirit is benign — no PF2e divination here reads as malevolent."),
    (r"see Handout #1-1 on page 15",                      "see the Player Handout #1-1 box below"),
    (r"appear in Handout #1-2",                           "appear in the Player Handout #1-2 box below"),
]
def dcfix(html):
    html = _ocrfix(html)
    for pat, rep in _DCFIX:
        html = re.sub(pat, rep, html)
    return html

# OLLIEBIRD STATBLOCK RESYNC (community export = statblock authority; write()-swap 2026-06-10).
# - C7 Devargo: community export's level FIELD was a pf2.tools truncation bug (1 with L5 stats);
#   community/actors/devargo-bavarsi.json patched to L5 upstream, C7 budget/aside use 5.
# Levels re-synced into encounter math + journal level labels:
#   Amin 1->3 (E5 label) · Grau 4->6 (E6) · Cow Hammer Boy 2->-1 (B1/B4) · Verik 4->3 (B8)
#   · Enforcer 3->2 (C1/C2) · Devargo 6->5 (C7; see truncation-bug note above) · Chittersnap 4->3
#   (C15) · Skeletal Owlbear 3->2 (D1) · Cabbagehead 3->4 (D9) · Vreeg 7->5 (D13; enc math
#   had said 6 — conv note no longer claims "Severe") · Acid-Spraying Skulls 3->1 (D6 label).
#   Trinia 3->5 needed no edits (chase subsystem, no XP math or level text).
# Rewired to community-only named pets via B.cmon: Gobblegut + Bloo (Monster Core drag-in
#   instructions retired with them; MC/mc helper removed).
# Gear dedup vs community inventories (same-parcel doubles): Gaedren's +1 Dagger removed
#   (community "+1 Key-Bladed Dagger" is that parcel) · Trinia's Wand of Daze Monster removed
#   (community Wand of Color Spray) · Yargin's scroll + Devargo's invisibility potion renamed
#   to the community item names, and Grau chain mail->full plate, Verik spear->"Longspear",
#   Enforcer leather->studded leather likewise, so the write()-merge drops ours (keeps the
#   nid() stream — and thus every page id — stable). KEPT as treasure the community omitted:
#   Grau's +1 striking mithral longsword, Verik's +1 striking composite longbow, Gaedren's
#   +1 padded armor, Devargo's +1 studded leather / venom / keys & purse, Giggles' potions
#   + composite longbow, Amin's ring & purse, Vreeg's robe/wand/ring, Cow Hammer Boy kit.
# NOT rewired (kept official B.mon per remaster-same-creature rule): Otyugh, Imp, House
#   Drake, Reefclaw, Raktavarna, Necrophidius, Carrion Golem, Hunting/Dream Spider, Skeleton
#   Guard, Zombie Shambler. NOT rewired (our kept custom actors, not B.mon substitutes):
#   Derro (community offers a Strangler/Elite-Stalker choice), Mad Prophet (community used a
#   generic GMG Beggar), Lamm's Lambs (community models them as a hazard; CHG-0107 keeps
#   them non-combatant NPCs here) — Beggar/Dero docs still ship via build_community.py.
# MISSING-CHECK SWEEP (2026-06-10): badged gated interactions the prose left checkless —
#   Cbelow intro: standing below-decks pick rule, Thievery 20 (olliebird silent; GM Core
#   simple lock per the community's own 15/20/30 convention, party L4) · C9 brewery door:
#   pick 20 inline (key-only, but Devargo's key ring is obtainable loot) · D6: secret door
#   to D2, Perception 21 inline (mirrors D2's existing badge / olliebird ruling) · A13:
#   rusted manacles Thievery 17 (GM Core poor manacles) for the mid-'feeding' child rescue ·
#   B3: barred south double doors, Athletics 22 to Force Open from outside (matches
#   olliebird's B4 grate Force Open 22 at the same site). No existing DC changed. Judged
#   narrative/no-check: Ch.Background treasury secret door (Ileosa backstory) · E8 Castle
#   Korvosa 'locked tight' (figurative; entry is the audience) · Conclusion's Blackjack
#   climb/leap (cut-scene) · C17 shark, A5 boarded window, A12 rusted chains, A13 lockbox
#   clutter (set dressing) · conv-note "'pick = 15' line" (meta-commentary; NB the features
#   page's actual standing rule is pick 18 — text left untouched per no-DC-changes rule).

# Player-handout sidebar text the two-column OCR fused into the GM narrative
# (start-phrase, end-phrase, label). Pulled out of the prose so it stops
# splitting sentences, then re-emitted as its own read-aloud block. Handouts are
# verbatim BY DESIGN — exempted exactly like read-aloud boxes (see the
# Conversion Guide journal -> "Source Text, Read-Alouds & Handouts"): the text is
# injected at build time from the GM's local AP.md, never hardcoded here.
_HANDOUTS = [
    ("I know what Gaedren has done to you", "justice must be done.", "Player Handout #1-1 — The Harrow Card"),
    ("Thank you for coming. I had to step", "drink for you.", "Player Handout #1-2 — The Note on the Table"),
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
        for hs, he, hl in _HANDOUTS:
            i = txt.find(hs)
            if i >= 0:
                j = txt.find(he, i)
                j = j + len(he) if j >= 0 else len(txt)
                handouts.append((hl, txt[i:j].strip()))
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
        out.append(f'<p class="subhead"><strong>{txt}</strong></p>' if kind == "sub" else B.parafy(dcfix(txt)))
    for hl, h in handouts:                                # handouts as read-aloud boxes
        out.append(B.s_read(f'<p class="subhead"><strong>{hl}</strong></p><p>{dcfix(h)}</p>'))
    return "".join(out)

# =====================================================================
# FOLDERS (one tree per document type; Kingmaker palette)
# =====================================================================
F = {k: nid() for k in ["a_root","a_ch1","a_creatures","a_hazards","i_root","i_ch1","i_treasure","i_bg",
                        "j_root","j_adventure","s_root","s_ch1"]}
# Cross-chapter container folders get STABLE literal ids so later per-chapter
# scripts (build_ch2.py …) can nest their chapter folders under the same roots.
F["a_root"]="cotctActorRoot01"; F["i_root"]="cotctItemRoot001"; F["j_root"]="cotctJrnlRoot001"
F["j_adventure"]="cotctAdvFolder01"; F["s_root"]="cotctSceneRoot01"
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
 B.folder("ch2SceneFolder01","2. Seven Days to the Grave","Scene",F["s_root"],200000,CHC),
 B.folder("ch3SceneFolder01","3. Escape from Old Korvosa","Scene",F["s_root"],300000,CHC),
 B.folder("ch4SceneFolder01","4. A History of Ashes","Scene",F["s_root"],400000,CHC),
 B.folder("ch5SceneFolder01","5. Skeletons of Scarwall","Scene",F["s_root"],500000,CHC),
 B.folder("ch6SceneFolder01","6. Crown of Fangs","Scene",F["s_root"],600000,CHC),
]
# folders live in each relevant per-type pack
for f in folders:
    pack = {"Actor":"actors","Item":"items","JournalEntry":"journals","Scene":"scenes"}[f["type"]]
    # hazards pack mirrors the actor hazard folder too
    B.write(pack, "_folder_"+f["name"].lower().replace(" ","-").replace(".","")+"-"+f["type"][:3].lower(), copy.deepcopy(f))
# Mirror the folder chain into the hazards pack so the hazards COMPENDIUM shows
# the same per-chapter tree (folders are per-pack documents in Foundry).
for hf in [B.folder(F["a_root"],"Curse of the Crimson Throne","Actor",None,100000,ROOTC),
           B.folder(F["a_ch1"],"1. Edge of Anarchy","Actor",F["a_root"],100000,CHC),
           B.folder(F["a_hazards"],"Hazards","Actor",F["a_ch1"],200000,None,"a")]:
    B.write("hazards", "_folder_hz1-"+hf["name"].lower().replace(" ","-").replace(".",""), copy.deepcopy(hf))

# =====================================================================
# ACTORS (ported stats + prototype tokens + folders)
# =====================================================================
actors = []
def AW(slug, doc):
    actors.append(copy.deepcopy(doc)); B.write("actors", slug, doc, embed_items=True)

def runed(key, _id, name, desc, potency=1, striking=0, price_gp=0, level=0):
    """Clone an SRD gear template and etch runes onto it — for the named magic
    arms the page text promises (+1 dagger, +1 striking mithral longsword, …)."""
    it = B.gear(key, _id)
    it["name"] = name
    it["system"]["description"] = {"value": desc}
    rs = it["system"]["runes"]; rs["potency"] = potency
    if "striking" in rs: rs["striking"] = striking
    if striking: it["system"]["damage"]["dice"] = 1 + striking
    it["system"]["price"] = {"value": {"gp": price_gp}}
    it["system"]["level"] = {"value": level}
    tv = it["system"]["traits"]["value"]
    if "magical" not in tv: tv.append("magical")
    return it

AW("gaedren-lamm", B.npc(A["gaedren"],"Gaedren Lamm",2,17,30,3,9,8,8,
  {"str":-1,"dex":4,"con":0,"int":3,"wis":2,"cha":3},15,
  {"deception":10,"stealth":9,"thievery":9,"intimidation":8,"society":6,"acrobatics":9},
  ["humanoid","human"],["Common","Dwarven","Gnomish","Goblin","Halfling","Infernal","Orcish","Shoanti","Varisian"],
  [B.strike(nid(),"+1 Dagger",10,"1d4+1","piercing",["agile","finesse","magical","versatile-s"]),
   B.strike(nid(),"Hand Crossbow",9,"1d6","piercing",["range-increment-60","reload-1"]),
   B.sneak_attack(nid(),1,"Gaedren"),
   B.action(nid(),"Nimble Dodge","reaction","<p><strong>Trigger</strong> A creature he can see attacks him.</p><hr /><p><strong>Effect</strong> +2 circumstance bonus to AC against that attack.</p>",["mental"],"defensive"),
   B.action(nid(),"Spur the Beast","1","<p>Gaedren makes a Hand Crossbow Strike against Gobblegut; on a hit, the enraged crocodile gains a +2 status bonus to attack and damage rolls until the end of its next turn and must use a single action to Strike the nearest creature other than Gaedren on its next turn.</p>",["concentrate"]),
   B.lore(nid(),"Underworld Lore",8),
   B.gear("hand-crossbow",nid()),
   # (our embedded "+1 Dagger" retired: the community statblock carries the same parcel
   #  as "+1 Key-Bladed Dagger"; the Treasure-folder world copy keeps the journal anchor)
   runed("padded-armor","ch1GaedrenPad001","+1 Padded Armor",
     "<p>Gaedren's grimy padded armor carries a +1 armor potency rune — his PF1e '+1 padded armor', kept as the minor armor reward the Treasure page promises. His AC already includes it.</p>",
     potency=1, price_gp=160, level=5)],
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
   # named to match the community's copy exactly so the write()-merge keeps theirs (dedup)
   B.equipment(nid(),"Scroll of Acidic Burst (Level 1)",1,4,"<p>A spell scroll holding a 1st-rank burst of acid (his PF1e wand of acid splash, re-cast as a scroll). Yargin is no spellcaster, so he must Trick the scroll ("+chk("type:arcana|dc:15")+", Trick Magic Item); on a success he spends 2 actions to Cast it, dealing @Damage[2d6[acid]] in a 10-foot burst ("+chk("type:reflex|dc:18|basic:true")+").</p>",traits=["scroll","magical","acid","consumable"])],
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
  notes="<p><strong>Role:</strong> a beardless young noble cornered by the mob in Event 5 — a quest-giver, not a combatant. If the PCs disperse the mob ("+chk("type:diplomacy|dc:16")+" or "+chk("type:intimidation|dc:19")+") or fight it off, Amin escapes.</p>"
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
   runed("longsword","ch1GrauSword0001","+1 Striking Mithral Longsword",
     "<p>Grau's Orisini-school dueling blade, mithral (dawnsilver)-light and etched with +1 potency and striking runes — the last thing of value he owns, and the Event 6 page's named loot. Light for its kind (Bulk reduced by the mithral).</p>",
     potency=1, striking=1, price_gp=160, level=4),
   # community Grau wears Full Plate — same name here so the write()-merge dedups his armor
   B.gear("full-plate",nid()), B.gear("steel-shield",nid())],
  notes="<p><strong>Role:</strong> a recurring NPC — a well-liked Korvosan Guard watch sergeant (Vencarlo Orisini's expelled student) drowning his despair in drink. This 'fight' is meant to be survived and <strong>defused</strong>, not a kill.</p>"
        "<p><strong>Defusing him:</strong> commiserate ("+chk("type:diplomacy|dc:19")+", or a Deception vs. his Perception) and he sobers up; "+chk("type:society|dc:18")+" recognizes the sergeant he was. A lesser restoration sobers him instantly. Escorted to Citadel Volshyenek, his fellow guards clean him up and he becomes a grateful ally.</p>"
        "<p><strong>If he duels:</strong> he limits attacks to the PC who accepted the duel; if another PC strikes him he cries 'Foul!' and flails at random foes. <strong>Morale:</strong> surrenders rather than dies. Award XP as if defeated whether he is beaten or talked down.</p>",
  folder=F["a_creatures"], blurb="Drunken watch sergeant; future ally", token_src=TOK("grau-soldado"), actor_link=True))

AW("trinia-sabor", B.npc(A["trinia"],"Trinia Sabor",3,18,36,6,11,9,7,
  {"str":0,"dex":3,"con":1,"int":2,"wis":1,"cha":3},25,
  {"acrobatics":11,"crafting":8,"deception":9,"stealth":11,"society":6,"arcana":7},
  ["humanoid","human"],["common","varisian"],
  [B.strike(nid(),"Dagger",9,"1d4","piercing",["agile","finesse","thrown-10","versatile-s"]),
   B.action(nid(),"Wand of Daze Monster","1","<p>Trinia Activates her <strong>wand of daze monster</strong> against the closest pursuer, who must succeed at a "+chk("type:will|dc:17")+" or be "+B.cond("stunned","Stunned 1")+" (Stunned 3 on a critical failure) — she uses it to break up a chase.</p>",["concentrate","magical"]),
   B.action(nid(),"Figment","2","<p>Trinia conjures a minor illusion — most often an image of herself asleep in her bed, which she abandons (the figment lingers ~2 rounds) as she slips out the window. A creature that Seeks against it disbelieves with a "+chk("type:will|dc:17")+".</p>",["concentrate","illusion","manipulate"]),
   B.action(nid(),"Fit of Laughter","2","<p>One creature on Trinia's space must succeed at a "+chk("type:will|dc:17")+" or be overcome with laughter — "+B.cond("slowed","Slowed 1")+" and unable to act usefully for 1 round (it falls "+B.cond("prone","Prone")+" on a critical failure).</p>",["emotion","incapacitation","mental"])],
   # (our embedded "Wand of Daze Monster" retired: the community statblock carries her wand
   #  parcel as "Wand of Color Spray (Level 1)"; the chase tactic reads the same — "her wand")
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
   # the spear is renamed to the community's "Longspear" so the write()-merge dedups his polearm
   B.gear("chain-mail",nid()), {**B.gear("spear",nid()),"name":"Longspear"}, B.gear("healing-potion-minor",nid(),3)],
  notes="<p><strong>Role:</strong> deserter watch sergeant fronting the slaughterhouse — a recurring NPC, not a die-hard villain. He believes his Vudrani lover 'Meliya' (secretly the rakshasa Vimanda) is just feeding the poor; he has no idea his men murder for hire.</p>"
        "<p><strong>Tactics:</strong> fights from range with the longbow, switching to the longspear only if engaged in melee. He hesitates several rounds before joining a fight below (fearing the Guard has come for him), often arriving as it ends.</p>"
        "<p><strong>Surrender:</strong> he gives up if dropped below ~1/4 HP, or instantly if shown hard evidence of the murders (the severed finger, the buried stash, or a thug's confession). "+chk("type:intimidation|dc:16")+" cows him (he then flees if unbound); a near-impossible Diplomacy ("+chk("type:diplomacy|dc:27")+" to Make an Impression) makes him helpful. <strong>Story award</strong> for taking him alive without combat. His silver dagger is the "+B.mon("raktavarna","raktavarna")+" spy.</p>",
  folder=F["a_creatures"], blurb="Deserter watch sergeant; Arkona dupe", token_src=TOK("verik-vancaskerkin"), actor_link=True))

# ---- Part Three: area C — Eel's End (custom NPCs) ----
AW("eels-end-enforcer", B.npc(A["enforcer"],"Eel's End Enforcer",3,20,45,9,7,8,9,
  {"str":3,"dex":2,"con":3,"int":0,"wis":1,"cha":-1},25,
  {"athletics":9,"intimidation":7},
  ["humanoid","human"],["common"],
  [B.strike(nid(),"Sap",11,"1d6+3","bludgeoning",["agile","nonlethal"]),
   B.strike(nid(),"Crossbow",9,"1d8","piercing",["range-increment-120","reload-1"]),
   # community enforcers wear Studded Leather — same name here so the write()-merge dedups
   B.gear("studded-leather",nid()), B.gear("buckler",nid()), B.gear("crossbow",nid())],
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
   B.action(nid(),"Spring the Throne","free","<p><strong>Trigger</strong> Devargo's turn begins.</p><hr /><p><strong>Effect</strong> He flips the hidden switch in his throne, opening the trap door beneath the petitioner's spot. A creature on it must succeed at a "+chk("type:reflex|dc:17")+" to cling to the sides or fall into the Spider's Web (C15) — and Chittersnap.</p>",["manipulate"]),
   B.lore(nid(),"Underworld Lore",14),
   B.gear("spiked-gauntlet",nid(),2), B.gear("hand-crossbow",nid()), B.gear("healing-potion-minor",nid(),1),
   B.equipment("ch1DevargoVenom1","Spider Venom (4 Doses)",1,4,
     "<p>4 doses, milked from Chittersnap's brood. <strong>Poison (injury):</strong> a creature hit by a coated weapon attempts a "+chk("type:fortitude|dc:24")+"; on a failure it is "+B.cond("clumsy","Clumsy 2")+" and "+B.cond("enfeebled","Enfeebled 1")+" for 1 round (Clumsy 2 and Enfeebled 2 for 4 rounds on a critical failure). Devargo's <em>Prepare Spider Venom</em> assumes both gauntlets are coated.</p>",
     traits=["alchemical","consumable","injury","poison"]),
   B.equipment("ch1DevargoKeys01","Devargo's Keys & Purse",0,79,
     "<p>An iron ring with two keys — the shiver brewery (C9) and the sea chest in his quarters (C14) — plus a belt purse of 79 gp.</p>",
     traits=["evidence"]),
   # named to match the community's "Invisibility Potion" so the write()-merge keeps theirs
   B.equipment(nid(),"Invisibility Potion",4,12,"<p>Devargo quaffs this to flee when reduced below ~10% HP, vanishing down to his quarters (C14).</p>",traits=["potion","magical","consumable","illusion"])],
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
        "<p><strong>Tactics:</strong> webs prey at range, then closes with poisoned jaws and claws. It rarely leaves its web-choked den, where every square is difficult, poisonous terrain (a "+chk("type:reflex|dc:15")+" each round to avoid the dream-spider webs).</p>",
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
  notes="<p><strong>Role:</strong> one of Vreeg's insane subterranean kin guarding the warrens for Rolth (who took Vreeg on as an apprentice). <strong>Tactics:</strong> attacks on sight, then flees through the secret crawl-tunnels ("+chk("type:perception|dc:21")+" to find) to warn the others.</p>",
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
   B.action(nid(),"Robe of Bones","2","<p><strong>Frequency</strong> 4 fetishes remain.</p><hr /><p><strong>Effect</strong> Vreeg plucks an animated-bone fetish from his robe and hurls it to an empty square within 20 feet, where it springs up as a "+B.mon("skeleton-guard","human skeleton")+" under his command. It acts on his initiative and crumbles after 1 minute. (His PF1e <em>robe of bones</em>.)</p>",["magical","manipulate","void"]),
   B.action(nid(),"Wand of Ghoulish Touch","2","<p>Vreeg Activates his bone wand and makes a melee spell attack (+16) against one creature. On a hit, the target takes @Damage[2d6[void]] and must succeed at a "+chk("type:fortitude|dc:24")+" or be "+B.cond("paralyzed","Paralyzed")+" for 1 round (on a critical failure, 1 minute — new save at the end of each of its turns). He saves this for foes who corner him in melee. (His PF1e <em>wand of ghoul touch</em>.)</p>",["magical","manipulate","void"]),
   B.lore(nid(),"Necromancy Lore",16),
   B.equipment("ch1VreegRobe0001","Robe of Bones",5,55,
     "<p>A grave-dust robe sewn with tiny bone fetishes (4 remain), each of which Vreeg can hurl to raise a temporary skeleton (see his <em>Robe of Bones</em> activity). In a PC's hands, each fetish can be expended once the wearer learns the command word ("+chk("type:occultism|dc:22")+" to puzzle it out); the skeleton is uncontrolled unless commanded.</p>",
     traits=["invested","magical","necromancy"]),
   B.equipment("ch1VreegWand0001","Wand of Ghoulish Touch",6,250,
     "<p>A carved knucklebone wand, Vreeg's arcane bond. Activates the paralyzing touch in his stat block; many charges remain (treat as a 2nd-rank wand for PC use, 1/day).</p>",
     traits=["magical","wand","void"]),
   B.equipment("ch1VreegRing0001","Ring of Protection (+1)",6,100,
     "<p>A tarnished silver band that wards its wearer (his PF1e <em>ring of protection +1</em> — Vreeg's AC already includes it). Rings don't grant AC in PF2e: let a PC pry the warding rune free and transfer it to armor as a <strong>+1 armor potency rune</strong>, or sell the ring (~100 gp).</p>",
     traits=["invested","magical"]),
   B.gear("dagger",nid())],
  notes="<p><strong>Role:</strong> the boss of the Dead Warrens — Rolth's gifted, insane derro apprentice, scheming to one day replace his master. <strong>Rolth himself is absent</strong> (away securing a scroll; he returns <em>after</em> the PCs leave, to find his lair in ruins — see Chapter 2).</p>"
        "<p><strong>Tactics:</strong> opens with Conjure Shield and False Life (his HP already includes it), then flies out of reach, kiting with Searing Ray, Force Missiles, and Vampiric Touch and hurling skeletons from his <em>Robe of Bones</em>; he saves Blindness for a martial threat and the <em>Wand of Ghoulish Touch</em> for anyone who corners him. <strong>Morale:</strong> fights to the death. <strong>Weakness:</strong> dazzled in bright light (derro sunlight vulnerability). His attendant zombie covers his retreat.</p>",
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
  "<p>"+chk("type:acrobatics|dc:14")+" to Balance across, or brace a stretch ("+chk("type:crafting|dc:15")+").</p>",
  "<p>A barnacle-slick boardwalk (A3) 13 ft above shark water; the planks also groan under heavy loads.</p>",
  [B.action(nid(),"Slip","reaction","<p><strong>Trigger</strong> A creature Strides &gt;5 ft or fights on it.</p><hr /><p><strong>Effect</strong> "+chk("type:reflex|dc:15")+" or fall "+B.cond("prone","Prone")+"; on a critical failure, slide off and fall 13 ft into the river and the Jigsaw Shark's water (A12) — the water is deep enough and the fall short enough that the creature takes no falling damage.</p>")],
  folder=F["a_hazards"], traits=["environmental"], reset="<p>Persistent terrain.</p>"))

HW("rotten-ship-deck", B.hazard(A["rottendeck"],"Rotten Ship Deck",1,16,
  "<p>"+chk("type:perception|dc:16")+" to spot the unsafe foredeck first.</p>",
  "<p>"+chk("type:crafting|dc:16")+" to shore up a path, or keep to the sound stern.</p>",
  "<p>The derelict Kraken's Folly (A9) has a rotten foredeck; only the stern holds weight.</p>",
  [B.action(nid(),"Collapse","reaction","<p><strong>Trigger</strong> A Medium+ creature moves onto the foredeck toward the bow.</p><hr /><p><strong>Effect</strong> "+chk("type:reflex|dc:15|basic:true")+" or crash to the hold (A11) for @Damage[1d6[bludgeoning]] and land "+B.cond("prone","Prone")+" among the drain spiders.</p>")],
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
  "<p><strong>Quest item.</strong> Records Gaedren's crimes in a Varisian cipher. "+chk("type:society|dc:16")+" (Decipher Writing; must read Varisian) to decode. Guard bounty: 15 gp (30 gp with the cipher key). Unlocks the 'Framed' background payoff.</p>",
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
           "dwarrens","D1","D2","D3","D4","D5","D6","D7","D8","D9","D10","D11","D12","D13","dconc",
           # late additions live at the END of this list so the ids of every page
           # declared before them stay stable (display order = pages-list order):
           "Cbelow"]
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
  +"<p>Zellara's reading (see "+pg(P["hook"],"Haunted Fortunes")+") draws the party together and points them at the <strong>Old Fishery</strong>, where crime-lord Gaedren Lamm hides with his thugs, his pet crocodile "+B.cmon("Gobblegut")+", and a workforce of enslaved orphans. In his den the PCs recover "+itm("brooch","Queen Ileosa's stolen brooch")+", "+itm("ledger","Gaedren's coded ledger")+", and "+itm("harrowdeck","Zellara's haunted harrow deck")+" — and as they step back into the street, the king dies and Korvosa erupts into the riots of <em>A City Gone Mad</em>.</p>"
  +B.s_milestone("<p><strong>Advancement:</strong> the party should reach <strong>2nd level</strong> after dealing with Gaedren. Milestone leveling (CHG-0007).</p>")
  +"<p><strong>Party:</strong> 4 PCs, level 1 → 2. <strong>System:</strong> PF2e Remaster (Foundry v14 / pf2e 8.2.0).</p>"
  +"<p><strong>Run it like Gotham.</strong> Tell players up front that Gaedren is a <em>connector</em>, not a campaign villain — this defuses the classic 'Lamm is a Lamb' let-down. By <strong>day</strong> 9 orphans toil, the thugs patrol, and the A7 doors stand open; by <strong>night</strong> every door locks, 26 orphans sleep in "+pg(P["A8"],"A8")+", and "+B.cmon("Bloo")+" prowls as a living alarm. The orphans are non-combatants — rescuing them is the heart of the dungeon.</p>"
  +SEC("<p><strong>The twist the players don't have yet:</strong> Zellara is already dead. Gaedren murdered her and fed her to Gobblegut; her spirit haunts her stolen deck. The PCs only learn this when they find her head in "+pg(P["A14"],"A14")+" — so play her in the intro as a warm, desperate ally, not a mystery.</p>"),level=1))

# 2. Haunted Fortunes — the hook ----------------------------------------------
# (restructured per audit: sectioned, home read-aloud + Zellara's tale boxed,
#  PF1e-isms and OCR fusions repaired via dcfix)
def _sub(t): return f'<p class="subhead"><strong>{t}</strong></p>'
_hf_fallback = "<p>A harrow card reaches each PC, naming Gaedren Lamm and an address — 3 Lancet Street. There the fortune-teller Zellara gathers them, recounts how Gaedren's thugs murdered her son over her stolen harrow deck, and asks them to bring him to justice; she performs a harrowing to prepare them. Zellara is in fact a haunt — already dead — though the PCs need not learn this until they find her head in Gaedren's den.</p>"
_hf1 = apspan("Curse of the Crimson Throne provides the PCs with a shared nemesis", "ZELLARA'S HOME")
_hf2 = apspan("The first PC to arrive at Zellara's home", "Zellara appears as she did in life")
_hf3 = apspan("Zellara appears as she did in life", "'Thank you for coming, my friends")
_hf4 = apspan("Once her tale is done, Zellara tells", "OLD FISHERY")
_hf_home_box = vbox(["interior of this small, humble home"],
  "<p>A single cozy chamber hazed with incense; brocaded tapestries of harrow imagery drape the walls, bright rugs cover the floor, and a red-clothed table waits with exactly enough tall-backed chairs. A cloth-covered basket sits beneath the table.</p>")
_hf_speech_box = vbox(["'Thank you for coming, my friends",
                       "'I sought help from the Korvosan Guard",
                       "'But I need your help. I cannot hope"],
  "<p>Zellara thanks the PCs for indulging her secretive summons, names Gaedren Lamm as the man who wronged them all, and tells her own story: his pickpockets stole her heirloom harrow deck; her son Eran got it back and was murdered for it. The Guard turned her away, so she bribed and divined until she found where Gaedren dens — an old fishery north of here at Westpier 17, where he trains stolen children as pickpockets. She cannot face him herself; it is time for him to pay.</p>",
  label="Zellara's Tale")
_hf_body = ((_hf1 + _sub("Zellara's Home") + _hf_home_box + _hf2
             + _sub("Zellara Manifests") + _hf3 + _hf_speech_box
             + _sub("The First Harrowing") + _hf4)
            if _hf1 else (_hf_fallback + _hf_home_box + _hf_speech_box))
pages.append(newpage("hook","Haunted Fortunes",
  SR("Part 1: Haunted Fortunes","14-16")
  +_hf_body
  +B.s_skill("<p><strong>First Harrowing → PF2e (CHG-0010).</strong> Run the reading as foreshadowing (a coming time of unrest; the PCs are fated heroes), then grant each PC a small pool of <strong>hero-point-style suit boons</strong> via "+itm("harrowdeck","Zellara's deck")+" — the recurring subsystem from here on. The illusions in her home are "+chk("type:will|dc:20")+" to disbelieve.</p>")
  ,level=2))

# 3. Scene Setup ---------------------------------------------------------------
pages.append(newpage("scene","Scene Setup",
  "<p>Open the "+scn(SCN,"Old Fishery scene")+" — it is built on <strong>Racooze's battlemap geometry</strong>: his walls, doors, and floor art come from your locally installed <em>Racooze's CotCT Battlemaps</em> module (install it free; nothing of his is redistributed).</p>"
  +"<p><strong>Layout:</strong> the left half of the canvas is the first floor (A1–A9, the ship docked at top); the right half is the waterline level (A10–A14 — the hold, the underpier, and Gaedren's den around Gobblegut's pool). Map-note pins link every area page below; all hostile tokens are pre-placed and <strong>hidden</strong> — reveal them as the raid unfolds. "+B.cmon("Gobblegut")+" (2×2, in the pool) and "+B.cmon("Bloo")+" (roaming "+pg(P["A8"],"A8")+") are staged from the community statblocks.</p>"
  +SEC("<p><strong>Import via the Adventure, not the scene compendium.</strong> The staged tokens reference actors by id; importing the <em>CotCT: Edge of Anarchy</em> Adventure creates those actors in the world alongside the scene, so every token resolves. Dragging the scene alone from the compendium — or using an Adventure import from an older module version — leaves tokens showing <em>'references an actor which no longer exists'</em>; fix by re-importing the Adventure (accept the overwrite prompt).</p>"
  +"<p>If the Racooze module is not installed at build time, this scene falls back to a placeholder grid (pins + staged tokens, no map). Day-shift staging is assumed per the area texts: Yargin in his office, Hookshanks at the loading dock, Giggles + 5 orphans on the fishery floor, 4 orphans at the trough, Bloo under the front-room desk. At night, move Yargin to "+pg(P["A5"],"A5")+" and start Hookshanks and Giggles on patrol routes.</p>"),level=2))

# 4. Fishery Features ----------------------------------------------------------
pages.append(newpage("features","Fishery Features",
  SR("A. Old Fishery","17")
  +RA("<p>A creaking, mold-mottled building of boarded windows and solid old doors, perched on pilings over the Jeggare River. It still renders 'dock-dumpling' slurry from spoiled fish — a cover for the crime-lord who dens beneath it.</p>")
  +"<p>The fishery sits on a 13-ft embankment ("+chk("type:athletics|dc:14")+" to climb the slick bank). Doors are hardness 5 / 10 HP ("+chk("type:thievery|dc:18")+" to pick, or "+chk("type:athletics|dc:15")+" to force); Yargin's brass key opens them all. Standing hazards: the "+haz("boardwalk","Slippery Boardwalk")+" ("+pg(P["A3"],"A3")+") and the "+haz("rottendeck","Rotten Ship Deck")+" ("+pg(P["A9"],"A9")+") — either can dump a PC into "+act("jigsawshark","the shark's")+" water ("+pg(P["A12"],"A12")+").</p>"
  +"<p><strong>Day vs. night.</strong> The encounters assume a daytime raid (9 orphans working, thugs at their posts). At night every door is locked, Yargin sleeps in "+pg(P["A5"],"A5")+", Giggles and Hookshanks run roving patrols (≈9pm / midnight / 3am), and "+B.cmon("Bloo")+" wanders "+pg(P["A8"],"A8")+" — his bark wakes the whole building.</p>"
  +B.s_skill("<p><strong>The orphans ('Lamm's Lambs').</strong> 9 work the fishery by day; all 26 sleep in "+pg(P["A8"],"A8")+" at night. Rally them with "+chk("type:diplomacy|dc:15")+" (Intimidation fails — they're inured to it); won over, they feed information or lend a hand. They know nothing past "+pg(P["A9"],"A9")+" — those sent below never return.</p>")
  +SEC("<p>They are <strong>non-combatants and never an XP-for-kill source</strong> (CHG-0107). Invaded at night they're too frightened to fight and flee into the slums once the thugs fall. Treat a rescued orphan as a 'Missing Child' background payoff, not a stat block.</p>"),level=2))

# Area pages A1-A14 ------------------------------------------------------------
def area(code,name,page_html): pages.append(newpage(code,f"{code}. {name}",page_html))

area("A1","Front Door", SR("A1","18")
  +box("A1","<p>Weathered double doors stand shut in the fishery's flank, a broken signboard swinging from a length of rusted chain above them. Brine and the stink of week-dead fish hang thick in the air.</p>")
  +"<p>The main doors are locked ("+chk("type:thievery|dc:18")+"). Most business runs through "+pg(P["A7"],"A7")+", so a knock — or a noisy attempt on the lock — brings "+act("yargin","Yargin")+" up from "+pg(P["A6"],"A6")+" to answer.</p>")

area("A2","Loading Dock", SR("A2","18")
  +box("A2","<p>A fifteen-foot loading dock juts from the building. Carts wait half-laden with tar-caked barrels, each daubed with a red, fish-shaped splotch. A rickety stair drops to a second door barely three feet above the river.</p>")
  +"<p>By day the doors into "+pg(P["A7"],"A7")+" stand open for the daily slurry shipment; the door to "+pg(P["A8"],"A8")+" is always locked ("+chk("type:thievery|dc:18")+"). The orphans do the heavy hauling under Hookshanks' eye.</p>")

area("A3","Back Alley", SR("A3","18-20")
  +box("A3","<p>A slippery boardwalk clings to the south wall on barnacle-eaten pilings, worn thin below the waterline. It runs about thirteen feet above the river, sloping down toward the derelict ship to the east.</p>")
  +"<p>The "+haz("boardwalk","Slippery Boardwalk")+" hazard: a careful pace is safe, but moving fast or fighting on it risks a fall into "+act("jigsawshark","the shark's")+" water ("+pg(P["A12"],"A12")+"); the planks also groan and give under heavy loads. The door into "+pg(P["A6"],"A6")+" is locked ("+chk("type:thievery|dc:18")+").</p>"
  +SEC("<p>Despite its state, this boardwalk is Gaedren's own private way in and out of his den ("+pg(P["A13"],"A13")+") — he uses it only a few times a month, spending days or weeks below to avoid being seen.</p>"))

area("A4","Front Room", SR("A4","19")
  +box("A4","<p>A single desk and a moldering chair stand in the middle of this disused room. A nest of ratty furs and straw is heaped beneath the desk.</p>")
  +"<p>In theory Yargin meets new customers here — a rarity. Any real noise in this room quickly brings both "+act("yargin","Yargin")+" and "+act("hookshanks","Hookshanks")+" to investigate.</p>"
  +B.enc("Bloo","Trivial · 20 XP",
     "<p>"+B.cmon("Bloo")+", Yargin's foul-tempered cur, sleeps under the desk and attacks any unfamiliar scent on sight. While he lives, a thug gets a circumstance bonus to bully the orphans into fighting.</p>"
     +B.s_skill("<p>Silence him fast — "+chk("type:stealth|dc:15")+" to slip past, "+chk("type:nature|dc:15")+" to calm, or a quick kill — before the barking rouses the fishery.</p>"),
     B.aside_token([B.cmon("Bloo","Bloo — Guard Dog (−1)")])))

area("A5","Barracks", SR("A5","20")
  +box("A5","<p>Two sets of bunks flank a boarded-over window. Three are slept-in; the fourth stands bare.</p>")
  +"<p>The thugs — Yargin, Hookshanks, and Giggles — share this room. They distrust one another and keep nothing of value here.</p>")

area("A6","Yargin's Office", SR("A6","19-21")
  +box("A6","<p>A desk wedged into one corner — its bulk blocking the western door — overflows with chalk-scrawled slate boards. A slouching cabinet leans against the east wall.</p>")
  +"<p>The fishery's 'books': slates of transactions and addresses, compiled monthly into scrolls in the cabinet — cover paperwork for any Guard inspection. "+act("yargin","Yargin Balko")+" works here and carries the brass key. The desk-blocked western door from "+pg(P["A4"],"A4")+" can be slipped past with "+chk("type:acrobatics|dc:18")+" to Squeeze.</p>"
  +SEC("<p>A floorboard behind the chair is a <strong>hidden, barred trapdoor</strong> ("+chk("type:perception|dc:22")+" to spot; "+chk("type:athletics|dc:18")+" or break to force) dropping straight into the boss's chamber ("+pg(P["A13"],"A13")+"). The hole is tight — "+chk("type:acrobatics|dc:28")+" for a Medium creature to Squeeze through ("+chk("type:acrobatics|dc:16")+" for Small) — but a meal-pulley rope makes the climb down easy ("+chk("type:athletics|dc:11")+"): a flanking route onto Gaedren that skips the whole lower floor.</p>")
  +B.enc("Yargin Balko","Low · 40 XP",
     "<p>Opens with thrown <strong>Acid Flasks</strong>, then falls back to his crossbow; he's terrified of melee.</p>"
     +SEC("<p><strong>Morale:</strong> at the first melee hit (or once his acid is spent) Yargin panics and flees down the trapdoor to warn Gaedren — and may lead the PCs right onto the boss. If he reaches the den, start the "+pg(P["A13"],"A13")+" fight with Gobblegut already enraged.</p>"),
     B.aside_token([act("yargin","Yargin Balko (1)")], img=TOK("yargin-balko"))))

area("A7","Upper Workroom", SR("A7","20-22")
  +box("A7","<p>The reek of fish and sweat stings the eyes. A great trough of half-rancid fish and brine drains through wooden chutes into a larger room beyond; a desk and a tall cabinet sit opposite.</p>")
  +"<p>Four orphans feed the chutes here. The floor around the trough is slick ("+chk("type:acrobatics|dc:14")+" to Balance if moving faster than a Step). The desk is locked ("+chk("type:thievery|dc:18")+"), as is the cabinet of petty cash ("+chk("type:thievery|dc:18")+"; Yargin's key).</p>"
  +"<p>"+act("hookshanks","Hookshanks Gruller")+", a gnome taskmaster, oversees the work — and dresses as one of the orphans, passing for one until a PC beats his Deception with "+chk("type:perception|dc:17")+" (gnome PCs get a bonus).</p>"
  +B.enc("Hookshanks + 4 orphans","Low · 40 XP",
     "<p>Hookshanks orders the orphans to attack, then opens the "+pg(P["A4"],"A4")+" door to loose "+B.cmon("Bloo")+" and raise the alarm; he fights with a kukri.</p>"
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
  +SEC("<p>Gaedren built a <strong>secret door into the hull</strong> ("+chk("type:perception|dc:18")+") opening to the underpier ("+pg(P["A12"],"A12")+") and the boss. Spotting his tracks in the filth ("+chk("type:survival|dc:16")+") grants a +5 circumstance bonus to find it.</p>")
  +B.enc("Drain Spider nest","Moderate · 80 XP (trivial with repellent)",
     "<p>Four drain spiders swarm anything that enters. Pair this with the "+haz("rottendeck","Rotten Deck")+" collapse from "+pg(P["A9"],"A9")+" for a single nasty moment.</p>",
     B.aside_token(["4× "+act("drainspider","Drain Spider (−1)")], img=TOK("drain-spider"))))

area("A12","Underpier", SR("A12","24-25")
  +box("A12","<p>A narrow space runs beneath the fishery, three feet of headroom above the foamy river. Moss and rusted chain hang between the pilings, and a floating walkway threads west to a tiny two-and-a-half-foot door.</p>")
  +"<p>Gaedren's escape skiffs are tied along the walkway. The squat door ("+chk("type:thievery|dc:18")+") leads into the den ("+pg(P["A13"],"A13")+"); a Medium creature must stoop to Squeeze through ("+chk("type:acrobatics|dc:18")+"). A swimmer could instead Squeeze between the pilings straight into the den ("+chk("type:acrobatics|dc:28")+").</p>"
  +B.enc("Jigsaw Shark","Low · 40 XP · avoidable",
     "<p>The shark scavenges scraps drifting from above. It attacks anything that falls into the water, but only leaps onto the walkway if it is first attacked and damaged.</p>"
     +B.s_skill("<p>Stay dry and it stays a hazard, not a fight — though the "+haz("boardwalk","boardwalk")+" and "+haz("rottendeck","rotten deck")+" above exist precisely to feed it victims.</p>"),
     B.aside_token([act("jigsawshark","Jigsaw Shark (1)")], img=TOK("jigsaw-shark"))))

area("A13","Gaedren's Playground", SR("A13","24-26")
  +box("A13","<p>A chill chamber opens over a pit of black river water, crossed by two five-foot walkways. Rusted manacles dangle from mossy ropes above the pool. On the far side, cabinets and lockboxes spill dingy 'treasures' across three cluttered tables. Something heavy shifts in the water below.</p>")
  +"<p>"+B.cmon("Gobblegut")+" lurks in the pit; "+act("gaedren","Gaedren Lamm")+" sorts the day's haul at his tables across it. <strong>Reaching him means crossing the gator's water.</strong></p>"
  +SEC("<p>Those manacles are where Gaedren feeds doomed orphans to Gobblegut for sport — the PCs may arrive mid-'feeding,' a child dangling over the snapping jaws ("+chk("type:thievery|dc:17")+" to pick the rusted manacles free, or simply cut the rope). Anyone who names <strong>Zellara</strong> earns a leering reply that 'she's in the next room' — her head waits in "+pg(P["A14"],"A14")+". <strong>Tactics:</strong> Gaedren opens with <em>Spur the Beast</em> to enrage Gobblegut, snipes from across the pool, <em>Nimble Dodges</em> focus fire, and flees to the "+pg(P["A12"],"A12")+" skiffs at &le;8 HP — though the abused gator may take him first.</p>")
  +B.enc("BOSS — Gaedren + Gobblegut","SEVERE · 120 XP @ level 1 (Moderate @ level 2)",
     "<p>The crocodile is the real threat; Gaedren is a frail catalyst who weaponizes it and snipes from cover.</p>"
     +"<p><strong>Scaling:</strong> 3 PCs → Weak Crocodile · 5–6 PCs → Elite Crocodile and/or pull a drain spider from the pool · if Yargin reached Gaedren first, Gobblegut starts pre-enraged.</p>",
     B.aside_token([act("gaedren","Gaedren Lamm (2)"), B.cmon("Gobblegut","Gobblegut — Crocodile (2)")], img=TOK("gaedren-lamm")))
  +B.s_treasure("<p>On the tables: "+itm("coffer","a darkwood coffer — 20 doses of shiver + 7 applications of vermin repellent")+".</p>")
  +B.s_conv("<p><strong>⚠ Track what the PCs do with the body.</strong> Left here, Gaedren's son Rolth animates it — the PCs meet an undead Gaedren in the Dead Warrens at the chapter's end. See "+pg(P["conv"],"Conversion Notes")+".</p>")
  +SEC("<p><strong>What if Gaedren escapes?</strong> Unlikely — his ruined leg is slow and his own abused gator may take him — but if surviving minions slow pursuit and he slips away, he lies low in Korvosa's back alleys. Options to bring him back:</p>"
   "<ul><li><strong>Gaedren's son:</strong> he seeks out Rolth. Either Rolth takes the old man in — the PCs face Gaedren again <em>at Rolth's side in Chapter 2</em> — or Rolth simply murders him and hands the body to his derro ally Vreeg (the zombie in "+pg(P["D13"],"D13")+" is then Gaedren after all).</li>"
   "<li><strong>Into Old Korvosa:</strong> he calls in old favors — perhaps sheltering at Eel's End with Devargo Barvasi, a fellow shiver peddler — or lies low until Chapter 3, resurfacing as an <em>advisor to the Emperor of Old Korvosa</em>.</li></ul>"))

area("A14","Gaedren's Den", SR("A14","26-28")
  +box("A14","<p>A squalid bedroom-study: a lumpy bed against one wall, a table heaped with rotting food and scuttling roaches, a sagging dresser. At the foot of the bed sits a locked strongbox, a moldy ledger resting on its lid. A fly-blown hatbox sits atop the dresser.</p>")
  +"<p>Gaedren's private quarters. The strongbox opens to the rusty iron key he carries, or "+chk("type:thievery|dc:18")+".</p>"
  +SEC("<p><strong>The reveal.</strong> The hatbox holds <strong>Zellara's severed head</strong>, crudely made up to mimic life ("+chk("type:medicine|dc:10")+": dead for weeks) — confirming the woman who hired the party has been dead all along. Beneath it lies "+itm("harrowdeck","her haunted harrow deck")+", still inhabited by her spirit. Atop the strongbox is "+itm("ledger","Gaedren's coded ledger")+"; inside, "+itm("brooch","Queen Ileosa's Brooch")+" ("+chk("type:society|dc:16")+" recognizes it as the queen's) and the hoard. A key-shaped masterwork dagger among the loot is a gift from Gaedren's estranged son <strong>Rolth</strong> — foreshadowing the next chapter ("+chk("type:society|dc:18")+" recognizes the killer's signature blade).</p>")
  +B.s_treasure("<p>Full parcel on the "+pg(P["treasure"],"Treasure")+" page.</p>")
  +B.s_milestone("<p><strong>Campaign-background closure (story awards — milestone credit, CHG-0021):</strong></p>"
   "<ul><li><strong>Framed:</strong> decoding "+itm("ledger","the ledger")+" surfaces written proof that Gaedren orchestrated the crime the PC was framed for — their name can finally be cleared.</li>"
   "<li><strong>Betrayed, Love Lost, Unhappy Childhood:</strong> bringing Gaedren to justice (death or arrest) at last gives these PCs a measure of closure — mark the beat at the table.</li>"
   "<li><strong>Drug Addict:</strong> destroying the shiver from "+pg(P["A13"],"A13")+" (or turning it over to the Guard, who destroy it and pay a 50 gp bounty) closes that wound.</li>"
   "<li><strong>Missing Child:</strong> a rescued orphan pays off this hook (see "+pg(P["features"],"Fishery Features")+").</li></ul>"))

# NPCs index -------------------------------------------------------------------
pages.append(newpage("npcs","NPCs",
  "<p>Click any creature to open its sheet. Build rationale: <code>reports/npc_monster_conversion_report.md</code>.</p>"
  +"<ul>"
   "<li>"+act("gaedren","Gaedren Lamm")+" (L2) — "+pg(P["A13"],"A13")+" boss · "+act("yargin","Yargin Balko")+" (L1) — "+pg(P["A6"],"A6")+" · "+act("hookshanks","Hookshanks Gruller")+" (L1) — "+pg(P["A7"],"A7")+" · "+act("giggles","Giggles")+" (L1) — "+pg(P["A8"],"A8")+"</li>"
   "<li>"+B.cmon("Gobblegut")+" = Crocodile (L2) · "+B.cmon("Bloo")+" = Guard Dog (L−1) · "+act("drainspider","Drain Spider")+" (L−1) · "+act("jigsawshark","Jigsaw Shark")+" (L1) · "+act("orphan","Lamm's Lambs")+" <em>(non-combatant)</em></li>"
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
   "<li><strong>Gobblegut & Bloo</strong> ship as the community conversion's named statblocks (a Crocodile / Guard Dog re-skin; no rebuild of ours).</li>"
   "<li><strong>DCs aligned</strong> to the community conversion where it rules, PF2e level-based / simple values where it is silent (the PF1e locked-door spam collapsed to a single 'pick = 18' standing line).</li>"
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
  SR("Part 2: A City Gone Mad","29-30")
  +B.s_milestone("<p><strong>Part Two.</strong> The PCs emerge from the fishery to find King Eodred II dead and Korvosa in flames. Run these events in any order, across the ~month the chapter spans — there is no fixed schedule. No maps are provided: each event happens wherever the party is.</p>")
  +box("CGM","<p>Smoke rises on the horizon (or, by night, the flicker of fires); alarm bells clang over screams, the clash of steel, and the periodic detonation of arcane power. A wing of Sable Company hippogriff riders sweeps toward Castle Korvosa; one wounded mount crashes into a statue. A herald cries 'The king is dead! Long live the queen!' — answered by 'Hang the queen!' The city has gone mad.</p>")
  +"<p>Use the <strong>Korvosa (Anarchy)</strong> city statistics now — see the Conversion Guide journal → <em>Korvosa: Reputation &amp; City Tiers</em>. Korvosa stays in turmoil until the PCs begin Part Three.</p>"
  +SEC("<p><strong>How the king really died (GM only).</strong> Ileosa had her stepbrother-in-law Venster coat the king's playing cards with <em>fool's leprosy</em>, a Red Mantis poison that mimics a fast leprosy and so <strong>resists</strong> <em>remove disease</em>. No one realized it was poison, not sickness; a <em>neutralize poison</em> would have saved him. The body is sealed in the royal crypt and crumbles too fast for <em>speak with dead</em>; by the time anyone could attempt <em>resurrection</em>, his soul is judged and beyond mortal magic. These stay mysteries for now.</p>")
  +B.s_skill("<p><strong>Investigating the Queen.</strong> "+chk("type:society|dc:15")+" or "+chk("type:diplomacy|dc:19")+" (gather information) recalls common knowledge: Ileosa Arvanxi, born in Chelish Westcrown, scandalized her family to marry the aging Eodred II after a short courtship, and openly disdains Korvosa as 'a backwater colonial village.' Her true feelings — and her crimes — stay hidden this early. See the rumor table in your AP book (Appendix 2).</p>")
  +B.s_conv("<p>Before Event 11, make sure the PCs have heard rumors that the king was murdered — these rile the city and set up the Queen's Scapegoat.</p>"))

ev("e1","Event 1. A Return to Zellara's Home",
  SR("Event 1","31")
  +"<p>If the PCs return to Zellara's home, they find it abandoned for weeks — furniture in dust-covered pieces, no sign of the woman or her belongings. (They already found her severed head in "+pg(P["A14"],"A14")+".)</p>"
  +SEC("<p>If the PCs carry "+itm("harrowdeck","Zellara's harrow deck")+", now is the moment for her spirit to manifest via the deck's <em>major image</em>, explain the truth of her death, and reveal the deck's powers — the recurring <strong>Harrowing</strong> (Conversion Guide journal → <em>The Harrowing</em>). If they lack the deck, she manifests one last image to steer them back to the fishery to recover it. Going forward she speaks only through the deck.</p>"))

ev("e2","Event 2. The Mysterious Brooch",
  SR("Event 2","31")
  +"<p>When the PCs investigate "+itm("brooch","the brooch")+" from Gaedren's stash, "+chk("type:society|dc:16")+" recognizes it as the queen's. Any merchant they approach knows it instantly — it is registered with the Korvosan Guard as stolen, and the queen has offered a reward. The merchant advises returning it to Castle Korvosa to claim <strong>1,200 gp</strong>.</p>"
  +B.s_conv("<p>Following this up triggers "+pg(P["e8"],"Event 8: Long Live the Queen!")+" — the PCs' first audience with their future archenemy.</p>"))

ev("e3","Event 3. The Mad Prophet",
  SR("Event 3","31-32")
  +"<p>A wild-haired, sick-looking lunatic fixates on one PC, screaming that the character will 'near death during a time of great sickness' in Korvosa's darkest hour. His ravings are nonsense — but the disease he carries is not.</p>"
  +B.enc("The Mad Prophet",xpb([-1],2),
     "<p>One "+act("mad_prophet","mad prophet")+". If he Grabs the PC he is obsessed with, that PC is exposed to <strong>Filth Fever</strong> ("+chk("type:fortitude|dc:16")+"). This is a disease vector, not a real fight.</p>",
     B.aside_token([act("mad_prophet","Mad Prophet (−1)")], img=TOK("mad-prophet"))))

ev("e4","Event 4. Imps and Dragons",
  SR("Event 4","32")
  +"<p>Imps loosed by failed Acadamae summonings are a constant Korvosan menace, kept in check by the native house drakes. In the chaos, a pair of "+B.mon("imp","imps")+" swoops down to rob and savage the PCs. On the second round, four "+B.mon("house-drake","house drakes")+" arrive to attack the imps — likely saving the party.</p>"
  +B.enc("Imps (house drakes intervene)",xpb([B.mon_lvl("imp"),B.mon_lvl("imp")],2),
     "<p>2 "+B.mon("imp","imps")+" attack; the 4 "+B.mon("house-drake","house drakes")+" are <strong>allies</strong> that arrive round 2 and rarely linger. A saved drake may heal a PC as thanks.</p>"
     +"<p><strong>Scaling:</strong> repeat freely — add imps or delay the drakes for a harder fight (3–4 imps → "+xpb([B.mon_lvl("imp")]*3,2)+" to "+xpb([B.mon_lvl("imp")]*4,2)+").</p>",
     B.aside_token(["2× "+B.mon("imp","Imp (1)"), "4× "+B.mon("house-drake","House Drake (1)")+" (allied)"])))

ev("e5","Event 5. Meet the Mob",
  SR("Event 5","32-35")
  +"<p>Rioting laborers roam in mobs, battering anyone in finery with cries of 'Die, dandy!' and 'Death to the false queen!' The PCs come on a mob surrounding "+act("amin","Amin Jalento")+", a young nobleman. A burly woman jeers about her brother's dock-crushed arm — 'Wanna know what it feels like?' If the PCs do not intervene, the mob attacks Amin.</p>"
  +B.s_skill("<p>"+chk("type:diplomacy|dc:16")+" or "+chk("type:intimidation|dc:19")+" disperses the mob long enough for Amin to escape — otherwise it is a fight against six rioters.</p>")
  +B.enc("Riot mob + Amin Jalento",xpb([-1]*6,2),
     "<p>6 "+act("rioter","rioters")+" (fragile mooks — each flees the instant it takes damage; the mob routs fast). "+act("amin","Amin")+" is a non-combatant who fights only defensively and flees when he can.</p>"
     +B.s_treasure("<p><strong>Reward:</strong> save Amin and he gives the party a gold ring worth <strong>250 gp</strong> (award XP as if the mob were defeated).</p>"),
     B.aside_token(["6× "+act("rioter","Rioter (−1)"), act("amin","Amin Jalento (3, non-combatant)")], img=TOK("korvosan-rioter"))))

ev("e6","Event 6. The Drunken Guard",
  SR("Event 6","35-37")
  +"<p>The PCs run across "+act("grau","Grau Soldado")+" — a Korvosan Guard watch sergeant, once Vencarlo Orisini's prize student, now drunk and despondent in a tavern or staggering the streets. He bemoans the end of Korvosa; the king's death hit him hard, the riots harder.</p>"
  +B.s_skill("<p>"+chk("type:society|dc:18")+" recognizes the well-liked sergeant he was. Commiserate ("+chk("type:diplomacy|dc:19")+", or Deception vs. his Perception) and he sobers; a <em>lesser restoration</em> does it instantly. The right move is to escort him to Citadel Volshyenek, where the Guard cleans him up. If the PCs mock him, he challenges them to a duel (he relocates to a back alley if asked; the Guard breaks up a public fight in 3d6 rounds).</p>")
  +B.enc("Grau Soldado (duel — defuse, don't kill)",xpb([6],3),
     "<p>A single, skilled but "+B.cond("sickened","Sickened")+"-drunk duelist. He limits attacks to the PC who accepted the duel; if another PC strikes him he cries 'Foul!' and flails at random foes, provoking reactions. <strong>Morale:</strong> surrenders rather than dies.</p>"
     +B.s_treasure("<p><strong>Reward:</strong> get him back to the Guard intact and he becomes a grateful recurring ally (award XP as if defeated). His +1 striking mithral longsword is the only thing of value he still owns.</p>"),
     B.aside_token([act("grau","Grau Soldado (6)")], img=TOK("grau-soldado"))))

ev("e7","Event 7. Otyugh Uprising",
  SR("Event 7","37")
  +"<p>Something has driven a filth-feeder up from the sewers into an alley, thoroughfare, or shop basement where the PCs happen to be.</p>"
  +B.enc("Otyugh",xpb([B.mon_lvl("otyugh")],2),
     "<p>A single "+B.mon("otyugh","otyugh")+" lashes out with its tentacles, grabbing and dragging prey toward its filthy maw (beware its disease).</p>",
     B.aside_token([B.mon("otyugh","Otyugh (4)")])))

ev("e8","Event 8. Long Live the Queen!",
  SR("Event 8","37-39")
  +"<p>Returning "+itm("brooch","the brooch")+" (or otherwise seeking an audience) brings the PCs to Castle Korvosa, locked tight atop its ancient Thassilonian pyramid and bristling with swords and crossbows. Nervous guards demand their business; any reasonable answer keeps them from being chased off, and mentioning the queen's missing brooch — or "+chk("type:diplomacy|dc:20")+" — gets things moving faster.</p>"
  +"<p><strong>Weapons stay at the stairs.</strong> Before the PCs may ascend, all obvious weapons must be left with the guards at the base of the stairs — no one armed enters the queen's company. A PC who refuses is simply not admitted; those who comply get everything back the moment their business is done. A crossbow-armed escort then walks them up to the third floor, where the Crimson Throne waits.</p>"
  +SEC("<p><strong>Why so easy?</strong> The invitation isn't courtesy: Ileosa has ordered that any trustworthy-seeming adventurers asking for work be admitted to introduce themselves. The Korvosan Guard thinks this unwise — but the queen's orders are orders.</p>")
  +"<p>At the top of the stairs waits <strong>Sabina Merrin</strong> — the queen's handmaiden, bodyguard, and closest companion, stern in magnificent full plate. She asks whether they truly carry something of the queen's; shown the brooch, she smiles, dismisses the escort ('These heroes pose no threat to the queen.'), asks how the PCs wish to be introduced, and announces them into the throne room.</p>"
  +vbox(["Queen Ileosa sits upon the Crimson Throne"],
     "<p>Ileosa — a vision of beauty in black mourning dress and veil, a small silver coffer in her lap — receives them in a strangely empty, vaulted throne room: stained-glass kings and queens along the east wall, crimson tapestries, an immense fireplace, a silk carpet arching to the throne. Sabina takes the brooch, presents it to her queen with a flourish, and takes up her post at the throne's left side.</p>",
     label="The Throne Room")
  +vbox(["'This brooch was stolen from me some",
         "'I love Korvosa, as my husband did",
         "'The Korvosan Guard is stretched thin"],
     "<p>Ileosa calls the brooch's return more than an honorable deed — inspiration and hope on her darkest day. She mourns her husband, vows not to see his legacy or her city destroyed by riots, and offers the heroes more: an escort to Citadel Volshyenek, and word sent ahead to Field Marshal Cressida Kroft that they are coming. Then, pleading grief, she withdraws.</p>",
     label="Queen Ileosa's Address")
  +B.s_treasure("<p><strong>Reward:</strong> Sabina hands over the small silver chest (itself worth 50 gp): inside, on red velvet, lie 12 gold ingots stamped with the royal seal — 100 gp each (<strong>1,200 gp</strong> total). <strong>Story award</strong> (milestone credit; the AP's 800 XP) for meeting the queen and returning the brooch.</p>")
  +SEC("<p><strong>GM only — the misdirection.</strong> Ileosa is playing the PCs; her only honest emotion is delight at the brooch's return. She stands under a standing <em>misdirection</em> effect: <strong>any attempt to read her aura instead reads Sabina's</strong> — the readings of an honorable, lawful-minded human bodyguard, nothing amiss. This is the real reason Sabina is never allowed far from the queen's side in public: she is the shield against prying divinations. The PCs should leave with no reason to suspect a thing.</p>")
  +B.s_conv("<p><strong>City state:</strong> from this event until Event 11, the first riots are quelled — switch Korvosa from <em>Anarchy</em> to <em>Unrest</em> (Conversion Guide journal → city tiers). This audience is the linchpin: the queen now knows the PCs by face, and everything from "+pg(P["e9"],"Event 9")+" onward flows from it.</p>"))

# Event 9's two boxed briefings: the two-column OCR interleaved them, so they are
# re-stitched from raw source paragraphs at the documented fusion points.
def _e9_boxes():
    p1 = rawpara("'Ah, yes-you are the ones sent by")        # box1 head + box2 tail, fused
    f1 = rawpara("you helps. If you're willing")              # box1 tail (stranded fragment)
    f2 = rawpara("'Korvosa's got enough troubles as it is")   # box2 head (stranded fragment)
    p2 = rawpara("'Vancaskerkin and his followers have holed up")
    if p1 and f1 and f2 and p2 and "citizens like" in p1 and "now, we've got" in p1:
        cut = p1.index("citizens like") + len("citizens like")
        b1 = B._scrub_ocr(p1[:cut] + " " + f1)
        b2 = B._scrub_ocr(f2 + " " + p1[p1.index("now, we've got"):])
        return (B.s_read("<p class=\"subhead\"><strong>Cressida's Greeting</strong></p>"+B.parafy(b1)),
                B.s_read("<p class=\"subhead\"><strong>The Vancaskerkin Briefing</strong></p>"+B.parafy(b2)+B.parafy(B._scrub_ocr(p2))))
    return (B.s_read("<p class=\"subhead\"><strong>Cressida's Greeting</strong></p><p>Cressida greets the PCs as the heroes the queen sent word of — exactly what Korvosa needs. They have walked the streets and know how bad it is; every bit of aid from upstanding citizens helps, and she would like to retain them as well-paid agents of the Guard.</p>"),
            B.s_read("<p class=\"subhead\"><strong>The Vancaskerkin Briefing</strong></p><p>Many guards have deserted — most for family, some for profit. One, <strong>Verik Vancaskerkin</strong>, has convinced a knot of fellow guards that the queen will ruin the city; with a crisis on her hands Cressida can spare no patrols, wants no further guards exposed to his secessionist talk, and no patriot killing him outright. She needs impartial, skilled talent.</p><p>Vancaskerkin and his followers hold an abandoned Northgate butcher's shop called 'All the World's Meat.' Avoid killing the deserters if possible; capture Verik <strong>alive</strong> for interrogation (his body will do if he makes that impossible) — and find out <em>why</em> he deserted. If there is more to it than personal politics, she must know immediately. <strong>Bounty: 500 gp alive, 250 gp dead.</strong></p>"))
_e9b1, _e9b2 = _e9_boxes()
ev("e9","Event 9. Welcome to the Guard",
  SR("Event 9","39")
  +"<p><strong>Citadel Volshyenek</strong> (Midland, overlooking Jeggare Harbor) runs on a skeleton crew — every able guard is out holding the city together. The PCs are expected: the two nervous gate guards wave them through, and an escort leads them into the central keep, where a harried, exhausted woman in red armor rises from her desk — <strong>Field Marshal Cressida Kroft</strong>. She hasn't slept since the king died (a priest of Abadar's <em>lesser restoration</em> keeps her on her feet), but she bears it well. She bids the PCs sit.</p>"
  +_e9b1
  +"<p>Assuming the PCs agree to hear her out, she lays out the job:</p>"
  +_e9b2
  +B.s_skill("<p><strong>The fine print:</strong> capture Verik <strong>alive</strong> if at all possible (<strong>500 gp</strong>; half that for his body), avoid killing the deserters, and above all <strong>learn why he deserted</strong> — that thread (see "+pg(P["B8"],"B8")+") is what seeds the Arkona arc.</p>")
  +B.s_treasure("<p><strong>The Citadel barracks:</strong> Cressida offers the party room and board at the Citadel for as long as they serve the Guard — a free, safe place to sleep, eat, and retreat to between adventures. She has worked with adventurers before and treats them well.</p>")
  +B.s_conv("<p>Cressida is the PCs' patron and quest-giver for "+pg(P["e10"],"Event 10")+", "+pg(P["e11"],"Event 11")+", and "+pg(P["e13"],"Event 13")+", and one of their strongest allies for the whole campaign. Establish her as sympathetic, principled, and stretched thin. Once the PCs head out, continue with "+pg(P["bmeat"],"B. All the World's Meat")+".</p>"))

ev("e10","Event 10. The Ambassador's Secret",
  SR("Event 10","39-40")
  +"<p>Once Verik is behind bars (or in a coffin) and the bounty paid, Cressida invites the PCs back — and this time she isn't alone. A handsome man rises and bows: <strong>Vencarlo Orisini</strong>, one of Korvosa's most respected fencing masters ("+chk("type:society|dc:15")+" to recognize him). An outspoken critic of the government, he is nonetheless Cressida's old friend and trusted ear on the city's mood. He's gallant and gregarious — kissing hands, offering his chair, congratulating the PCs ('If Korvosa had more fine folk like you…') — until Cressida gently cuts him off:</p>"
  +vbox(["'As much as I would enjoy continuing",
         "'Fortunately, the ambassador has his foibles"],
     "<p>Vencarlo has learned of something that could spiral into sanctions, embargo, or even war with Cheliax: Ambassador <strong>Darvayne Gios Amprei</strong>, whose contempt for Korvosa is well documented, means to recommend trade sanctions — <em>deliberately</em>. His real scheme is to strangle Korvosa's economy until desperate landholders sell him huge tracts of the city cheap, then have his Chelish allies lift the sanctions once he is positioned in power. Killing him would only make a martyr; leverage is needed. Fortunately the ambassador has foibles: he has been making regular visits to <strong>Eel's End</strong>, the vice den of Devargo Barvasi — the 'King of Spiders' — who pays his vice taxes, keeps his business on his five moored ships, and may be the one man holding proof.</p>",
     label="Cressida — The Embargo Scheme")
  +vbox(["'Devargo would never let someone he recognizes"],
     "<p>Devargo would never admit a known ally of the Guard — but the PCs are unknowns. Visit Eel's End, win an audience, learn what Devargo knows of Amprei, and bring back proof of any illicit dealings; Cressida will use it to spike any embargo push. Devargo won't part with information cheaply — she supplies bribe gold, and whatever is left over the PCs keep. He is dangerous; if things turn violent, she won't mourn him.</p>",
     label="Cressida — The Mission")
  +B.s_treasure("<p>Cressida hands over a pouch of <strong>1,000 gp</strong> in bribe money ("+chk("type:diplomacy|dc:23")+" talks her up to 1,500 gp) — whatever isn't spent on Devargo, the PCs keep. As she gives the address, Vencarlo offers to escort the party as far as Old Korvosa — he was headed to his academy anyway.</p>")
  +SEC("<p><strong>Development:</strong> when the PCs deliver the letters, Cressida blushes as she reads them — they are <em>quite</em> salacious love letters to Amprei from <strong>Verania Tvastiox</strong>, young wife of one of his superiors in Cheliax (see "+pg(P["C14"],"C14")+") — then passes them to a clerk: perfect leverage. She pays a further <strong>500 gp</strong>. If word reached her that the King of Spiders is dead, she is quietly pleased but can't legally pay for it — instead she awards each PC the <em>drake's mark</em>, a medal worth 400 gp granting a <strong>+2 circumstance bonus to Diplomacy</strong> with citizens of Korvosa when worn openly.</p>")
  +B.s_conv("<p>This is the hook into Part Three's "+pg(P["cend"],"Eel's End (area C)")+". The bribe money matters — it is the PCs' lever on Devargo — and the walk with Vencarlo is the campaign's first long look at the man who is secretly Blackjack.</p>"))

ev("e11","Event 11. The Queen's Scapegoat",
  SR("Event 11","40-41")
  +"<p>To bury the regicide rumors, Ileosa picks a scapegoat: "+act("trinia","Trinia Sabor")+", a young artist who painted the king's portrait weeks before his death. A tortured guard's false confession (and the guard's subsequent 'suicide,' propelled by Sabina) sets a city-wide hunt and fresh riots — this time crying for the 'assassin's' death. Use the Korvosa (Anarchy) city state again.</p>"
  +SEC("<p><strong>GM:</strong> Trinia is innocent; Ileosa's jealousy (amplified by Kazavon's wrath) chose her. This is also the seed of the <strong>Gray Maidens</strong>, Ileosa's coming order of warrior-women.</p>")
  +"<p>Cressida — alone among the officers in doubting the confession — takes the PCs into the privacy of her office, away from prying ears, with a third mission:</p>"
  +vbox(["'You've doubtless heard the stories that",
         "'Before Trinia is captured and executed",
         "'I'm sure you can see where this"],
     "<p>The way the queen broadcast Trinia's name looks to Cressida like she <em>wants</em> the riots back; the girl will be lynched long before any trial, and if she's innocent the real killer walks free behind the distraction. Cressida has Trinia's last known address — a flat in Midland at 42 Moon Street — but the rest of the Guard, the mob, and Hellknights of the Order of the Nail will have it soon too; word is the queen, unsatisfied with the Guard, is even readying a new order of specialized guards and may disband the Sable Company. The PCs must get in quietly, catch Trinia, and deliver her safe to Cressida's loyal agents for a magical interrogation — before anyone else reaches her.</p>",
     label="Cressida — The Trinia Brief")
  +B.s_treasure("<p><strong>Reward: 1,000 gp</strong> for delivering Trinia safe and sound to a member of the Korvosan Guard. Every minute of delay is another minute for the Midland mob to grow.</p>")
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
  SR("Event 12","41-43")
  +"<p>The PCs slip into Midland and reach 42 Moon Street. Trinia's neighbors shelter her and send up an alarm when the party is spotted (each of 2d6 neighbors can be won over with Deception vs. their Perception +3). Her third-floor flat is barricaded: "+chk("type:athletics|dc:20")+" forces the door — every round of delay is a head start.</p>"
  +box("E12FLAT","<p>A one-room flat — bedroom, kitchen, and painter's studio in one. Bread and cheese sit by full waterskins; an easel holds a half-finished painting of an imp and a house drake fighting atop a church steeple. A single window looks out over the tangled rooftops, a low bed beneath it.</p>")
  +SEC("<p>Warned, "+act("trinia","Trinia")+" casts a <em>Figment</em> of herself asleep in bed and creeps out the window — "+chk("type:perception|dc:17")+" to notice her slipping away (+2 circumstance if looking out the window); 4 unnoticed rounds and she escapes outright. Caught unbarricaded but warned, "+chk("type:perception|dc:13")+" spots her grabbing her dagger and wand before she leaps. Surprised in her sleep, she flees empty-handed.</p>")
  +"<p><strong>The Shingles Chase</strong> (PF2e Chase subsystem). Run 15 obstacles; each PC attempts the listed skill on their turn to advance a chase point. "+act("trinia","Trinia")+" starts with a 0/3/5-obstacle lead depending on how thoroughly she was warned. A PC who fails badly <strong>falls to the street</strong>: take @Damage[2d6[bludgeoning]] and either "+chk("type:athletics|dc:19")+" to climb back into the chase, or "+chk("type:athletics|dc:16")+" / "+chk("type:reflex|dc:16")+" through the alleys to advance one obstacle. Catch her on the same obstacle and Grapple to end the chase; she escapes if she clears obstacle 15.</p>"
  +"<table><thead><tr><th>#</th><th>Obstacle</th><th>Overcome</th></tr></thead><tbody>"+_obst_rows+"</tbody></table>"
  +B.s_treasure("<p><strong>Rewards:</strong> catching Trinia earns XP as if defeated, however the PCs then choose to handle her. Turn her over to Cressida → <strong>1,000 gp</strong>; hide her or let her go (Cressida quietly approves) → <strong>2,000 gp</strong> paid later, folded into the "+pg(P["e13"],"Event 13")+" reward to hide the money trail; hand her to the queen → 200 pp and an invitation to her execution.</p>")
  +B.s_conv("<p>Trinia is innocent and a recurring ally. If she is hidden (Cressida calls in Vencarlo to spirit her to Old Korvosa), she is safe for the rest of the chapter, and the queen simply announces that another 'captured assassin' has been apprehended instead.</p>"))

ev("e13","Event 13. A Missing Body",
  SR("Event 13","43")
  +"<p>With the scapegoat in hand (or 'in hand'), the city calms — but during the riots a band of racist thugs used the unrest as cover to beat a young Shoanti to death. When the PCs next visit Citadel Volshyenek, the guards are jumpy: 'One of those Shoanti kids went and got himself killed' — and the Field Marshal is in her office with the Shoanti ambassador, asking for the PCs by name.</p>"
  +"<p>With Cressida sits an elderly Shoanti of 60 winters: <strong>Thousand Bones</strong>, visionary shaman of the Skoan-Quah — the Clan of the Skull — who has spent years brokering coexistence between his people and a city that mostly despises them. He regards the PCs sternly as Cressida explains the mob killing, then speaks, deep-voiced, his words carefully chosen and his anger barely held:</p>"
  +vbox(["'My people have worked hard to understand",
         "'Our ways are not as yours",
         "'With this knowledge, I could surely lead"],
     "<p>His grandson <strong>Gaekhen</strong> is dead, beaten by cowards in a Korvosan street — and his son and kin are not as forgiving as he: they would return to the Cinderlands and rally the Sklar-Quah to war. Only sending Gaekhen whole to the fires of the ancestors will stay their wrath — but the body was stolen from where he fell, sold by a corpse-peddler to the necromancer <strong>Rolth</strong>, and carried to a place beneath the graveyard the spirits name the <strong>Dead Warrens</strong>. Shoanti warriors retrieving it themselves would read as an act of aggression; it falls to the PCs to make amends — or his people will come for the body, and they will not be gentle.</p>",
     label="Thousand Bones Speaks")
  +"<p>Thousand Bones then rises, nods curtly to Cressida, and leaves to await his grandson's body. Cressida apologizes for his brusqueness but agrees with every word: someone tied to Korvosa must recover the dead Shoanti and return him as a gesture of good will. She can answer questions before the PCs set out:</p>"
  +vbox(["Who is Rolth? ' Ahh... Rolth Lamm"],
     "<p><strong>Who is Rolth?</strong> A failed Acadamae student — expelled, quietly and without charges, when the school discovered he was butchering vagrants and strays to stitch a golem from the parts — and trouble ever since; Cressida suspects him in a decade of mutilation-murders but has never pinned evidence on him. He is also <strong>Gaedren Lamm's only surviving son</strong>. If the PCs admit their history with Gaedren, she congratulates them (off the record — the Guard can't condone vigilantism) and warns them: Rolth may well know what hand they had in his father's fate. Anything found below that could lead to his arrest is welcome.</p>")
  +vbox(["What are the Dead Warrens? 'Korvosa's graveyards"],
     "<p><strong>What are the Dead Warrens?</strong> The Gray District's burial grounds are riddled with tunnels — ghoul-dug, monster-made, or remnants of ancient Shoanti burial vaults. The church of Pharasma patrols what it can, but for every necromancer rooted out two spring up, worst of all under <strong>Potter's Ward</strong>, where the poor are buried. Thousand Bones says the Dead Warrens were one of his people's burial vaults; they lie beneath Potter's Ward.</p>")
  +vbox(["How do we enter the Dead Warrens?"],
     "<p><strong>How do we enter?</strong> The corpse-peddler who sold Gaekhen's body — a simpleton named <strong>Elkaris</strong>, now in custody, who spilled everything — wheelbarrowed it to a <strong>partially collapsed mausoleum</strong> deep in Potter's Ward near its southern edge, marked by a <strong>toppled, headless statue of a sword-wielding gargoyle</strong>; he was told to leave the body behind the gargoyle. That matches where Thousand Bones places the old burial vaults: start there.</p>")
  +vbox(["How will we recognize Gaekhen's body? 'Thousand"],
     "<p><strong>How will we recognize Gaekhen?</strong> About <strong>18 years old</strong>, short brown hair, a distinctive <strong>firepelt-claw scar on his left cheek</strong>, and large Shoanti tribal <strong>tattoos across his arms and torso</strong>. No other freshly dead Shoanti should be down there — a dead giveaway.</p>")
  +B.s_treasure("<p><strong>Reward:</strong> 1,000 gp (Cressida folds Trinia's deferred 2,000 gp in here too, if applicable). <strong>Story award</strong> (milestone credit) for returning the body to Thousand Bones — a gesture of good will that pays off across the campaign.</p>")
  +B.s_conv("<p>Thousand Bones and the Shoanti debt seeded here pay off in Chapter 4 (A History of Ashes). Build the relationship now. Proceed to "+pg(P["dwarrens"],"D. The Dead Warrens")+".</p>"))

ev("e14","Event 14. A Lovely Day for an Execution",
  SR("Event 14","43-44")
  +"<p>The chapter's climax: once all other plots resolve, the queen stages the public execution of her scapegoat (Trinia — or, if the PCs hid her, an equally innocent look-alike). <strong>Set the date yourself</strong> so the PCs can finish Part Three (the Dead Warrens) first; if the execution lands before they're done, that's fine too — there is plenty of wiggle room between chapters before the plague begins to spread.</p>"
  +"<p><strong>The announcement.</strong> As the PCs emerge from the Dead Warrens, the news racing through the city is that Trinia Sabor's 'trial' has concluded: the assassin dies <strong>at sunset</strong>, and Queen Ileosa has invited Korvosa's nobles, military officers, and anyone of any import to Castle Korvosa's public courtyard to witness it. <strong>Cressida wants the PCs there</strong> — the whole affair sits wrong with her, and she fears it could spark another riot.</p>"
  +"<p><strong>Run the full set-piece</strong> — guillotine, procession, Ileosa's address, and Blackjack's rescue — from the "+pg(P["dconc"],"Chapter Conclusion")+" page: it is an interactive cut-scene, not a combat encounter.</p>"
  +SEC("<p>Whether the PCs disrupt the execution, aid the rescue, or let events run, this is the hand-off to the <strong>Chapter Conclusion</strong> and Chapter 2. As the chapter ends, the first cases of <strong>Blood Veil</strong> appear in the gutters — see the Conversion Guide journal → <em>Blood Veil &amp; the Epidemic Clock</em>.</p>")
  +B.s_conv("<p>This is the natural seam to begin the persistent-plague overlay: the Epidemic Clock starts in Chapter 2, seeded by how the city fared here.</p>"))

# =====================================================================
# PART THREE — BLOOD AND BONES: B. All the World's Meat (22 Stirge St.)
# Party ~L3. Cow Hammer Boys L-1 · Verik L3 · Reefclaw/Raktavarna official L1.
# =====================================================================
ev("bmeat","B. All the World's Meat",
  B.s_milestone("<p><strong>Part Three.</strong> The chapter's three investigation sites — a butcher's shop (B), Eel's End (C), and the Dead Warrens (D). <strong>All the World's Meat</strong> is an abandoned butcher's shop at 22 Stirge Street, seized by deserter sergeant "+act("verik","Verik Vancaskerkin")+" and four "+act("cowhammer","Cow Hammer Boys")+" who front 'free meat for the hungry' while secretly murdering marks-for-hire and butchering the bodies into the next day's handouts.</p>")
  +B.s_skill("<p>"+chk("type:diplomacy|dc:15")+" (gather information) on the street learns the gang calls itself the Cow Hammer Boys and hires out as muscle — ask for 'the night's special cuts' (50 gp per beating).</p>")
  +SEC("<p><strong>GM:</strong> Verik is a dupe. His 'Vudrani lover Meliya Arkona' is the rakshasa <strong>Vimanda</strong>, infiltrating Korvosa for the Arkona family (who scheme to topple Ileosa with a puppet prince). The silver dagger in "+pg(P["B8"],"B8")+" is her "+B.mon("raktavarna","raktavarna")+" spy. Taking Verik alive and chasing 'Meliya' seeds the Arkona arc of Chapter 3 — Glorio/Bahor begins watching the PCs.</p>"))

area("B1","Shop Front", SR("B1","46")
  +box("B1","<p>A sign bearing the image of a fat, smiling cow hangs above the entrance. A long counter runs over half the room; beyond it a door stands ajar. A low bench sits against the east wall, and a marble-topped table to the north displays cuts of meat before a grimy window, flies circling above.</p>")
  +"<p>Two "+act("cowhammer","Cow Hammer Boys")+" — Baldrago and Malder — hand out meat by day. Unless the PCs pose as needy locals they are gruffly told to 'kick off'; 'the night's special cuts' ends the hostility and opens the mercenary pitch. They never let anyone up to Verik. Push past them and they raise longbows and shout to "+pg(P["B4"],"B4")+" for help.</p>"
  +B.s_skill("<p>"+chk("type:perception|dc:22")+" or "+chk("type:butchery-lore|dc:16")+" (or a similar trade Lore) notices far more meat going out the door than the pens' livestock could ever supply.</p>")
  +B.enc("Cow Hammer Boys (front)",xpb([-1,-1],3),
     "<p>2 "+act("cowhammer","Cow Hammer Boys")+" open with longbows, closing to clubs only if forced. Reinforced by the two in "+pg(P["B4"],"B4")+" if the alarm goes up.</p>",
     B.aside_token(["2× "+act("cowhammer","Cow Hammer Boy (−1)")], img=TOK("cow-hammer-boy"))))

area("B2","Hall", SR("B2","46")
  +"<p>A short hall; the stairs lead up to the "+pg(P["B7"],"break room (B7)")+".</p>")

area("B3","Meat Locker", SR("B3","46")
  +box("B3","<p>The air is stale, stinking of day-old meat and blood. Straw litters the floor beneath meat hooks affixed to walls and ceiling. A blood-stained table and two salt barrels stand to the north; double doors to the south are barred by an iron bar that runs along the ceiling to a floor-to-ceiling pole.</p>")
  +"<p>The barred southern double doors open freely from inside (lift the bar via the pole); from outside they take "+chk("type:athletics|dc:22")+" to Force Open.</p>"
  +SEC("<p><strong>The horror.</strong> Salted meat hangs overnight here. Among the pork and beef, "+chk("type:medicine|dc:19")+" or "+chk("type:nature|dc:19")+" confirms at least a half-dozen cuts are not from animals at all — they are <strong>humanoid</strong>. Hard proof of the murders that breaks Verik (see "+pg(P["B8"],"B8")+").</p>"))

area("B4","Killing Floor", SR("B4","47")
  +box("B4","<p>The floor of this grim chamber is strewn with blood-stained straw, and the reek of slaughter is overpowering. Meat hooks ride a ceiling track; a great hammer rests on a permanent bloodstain in the northwest corner. A bloodstained grate covers a hole in the floor to the south, flanked by two vats of water — one boiling, one cold — with butcher blocks and a reeking cast-off vat beyond.</p>")
  +"<p>By day there is a 75% chance the other two "+act("cowhammer","Cow Hammer Boys")+" — Parns (a sadistic ex-butcher) and jittery Karralo — are here; otherwise they tend livestock in "+pg(P["B5"],"B5")+"/"+pg(P["B6"],"B6")+". The rusty grate (Hardness 10, HP 15; "+chk("type:athletics|dc:22")+" to pry/break) drops into a half-flooded sewer tunnel running east to the river.</p>"
  +B.enc("Cow Hammer Boys (killing floor)",xpb([-1,-1],3),
     "<p>2 "+act("cowhammer","Cow Hammer Boys")+" at work. They flee at low HP; once two of the four are dead, the rest abandon Verik.</p>",
     B.aside_token(["2× "+act("cowhammer","Cow Hammer Boy (−1)")], img=TOK("cow-hammer-boy")))
  +B.enc("Reefclaws (sewer below)",xpb([B.mon_lvl("reefclaw")]*3,3),
     "<p>3 "+B.mon("reefclaw","reefclaws")+" scavenge the grisly leftovers in the tunnel. Well-fed, they attack only intruders who disturb the remains (e.g. searching for the finger). Beware a reefclaw's death-frenzy and venom.</p>",
     B.aside_token(["3× "+B.mon("reefclaw","Reefclaw (1)")]))
  +B.s_treasure("<p>"+chk("type:perception|dc:19")+" in the sewer finds a severed human finger wedged above the waterline, still wearing a fine silver-and-obsidian ring (~25 gp re-scaled) — and damning evidence of the murders.</p>"))

area("B5","Holding Pens", SR("B5","47")
  +box("B5","<p>Two foul-smelling animal pens take up most of the room, each a fenced gate around a long water trough and heaps of filthy hay. The floor is hard-packed earth.</p>")
  +B.s_treasure("<p>"+chk("type:perception|dc:19")+" finds the gang's buried mercenary stash under the southern trough: re-scaled to PF2e, about <strong>40 gp</strong> in mixed coin plus a small clutch of jewelry and gems (~30 gp). The stash itself is evidence that breaks Verik.</p>"))

area("B6","Cattle Pen", SR("B6","47")
  +box("B6","<p>This large open-air cattle pen reeks of manure and animal despite the breeze through the stockade fence. A roofed shed to the south holds a straw-filled wagon.</p>")
  +"<p>Each morning 1d6−3 cows and 1d4−2 pigs arrive (sometimes none). The skittish animals are harmless.</p>")

area("B7","Break Room", SR("B7","47")
  +box("B7","<p>A round table sits in this room, surrounded by four wooden chairs, a deck of cards on its top. An open cabinet to the southwest spills dirty clothes and blankets; four thin bedrolls lie rolled against the north wall. Stairs descend to "+pg(P["B2"],"B2")+".</p>")
  +"<p>The Cow Hammer Boys relax and sleep here. By night they play cards before flopping down where they can.</p>")

area("B8","Slaughterhouse Office", SR("B8","48")
  +box("B8","<p>A single large desk stands in the eastern part of this office, made over into a bed with a bedroll, blankets, and pillows; a chamber pot beneath it. A table and three chairs sit to the west, papers strewn across the table — one pinned down by an exquisite silver dagger.</p>")
  +"<p>Verik's quarters. He drinks and sleeps here, paranoid the Guard will come for him. He still wears his Korvosan Guard armor. If he hears fighting below he dithers for several rounds before joining — often arriving as it ends.</p>"
  +SEC("<p><strong>Verik surrenders</strong> if dropped below ~1/4 HP, "+chk("type:intimidation|dc:16")+" to Coerce, "+chk("type:diplomacy|dc:27")+" to Make an Impression, or — instantly — if shown the "+pg(P["B3"],"humanoid cuts")+", "+pg(P["B4"],"severed finger")+", or "+pg(P["B5"],"stash")+". Broken, he lets himself be arrested and (if made helpful) admits 'Meliya' put him up to it, though he can't say why an Arkona would care.</p>"
       "<p><strong>The silver dagger is alive.</strong> It is a "+B.mon("raktavarna","raktavarna rakshasa")+", Vimanda's shapeshifted spy. It plays dead as a normal (non-magical, non-silver) dagger, hoping a PC loots it so it can later report on them. Exposed for what it is, it reverts and fights for 1d3 rounds before Vimanda severs the link and abandons it to die.</p>")
  +B.enc("Verik Vancaskerkin + the dagger-spy",xpb([3,B.mon_lvl("raktavarna")],3),
     "<p>"+act("verik","Verik")+" fights from range with his longbow, switching to the longspear only in melee. The "+B.mon("raktavarna","raktavarna")+" joins only if discovered. <strong>This fight is often skipped entirely</strong> — bring evidence and Verik folds.</p>",
     B.aside_token([act("verik","Verik Vancaskerkin (3)"), B.mon("raktavarna","Raktavarna (1, hidden)")], img=TOK("verik-vancaskerkin")))
  +B.s_treasure("<p>Loot: "+act("verik","Verik's")+" +1 striking composite longbow (the area-B permanent magic reward), chain mail, longspear, and 3 minor healing potions. The silver 'dagger' is the raktavarna — do not let it travel with the party unnoticed.</p>")
  +B.s_conv("<p><strong>Story award</strong> for taking Verik alive without combat. Spared and turned, Verik can resurface as an ally; his brother <strong>Orik</strong> appears in Chapter 3. Pursuing 'Meliya' opens the Arkona thread (Ch.3).</p>"))

# =====================================================================
# PART THREE — C. EEL'S END (Devargo's floating den). Party ~L4.
# Enforcer L2 · Devargo L1 (community sheet level; its stats read ~L5) · Chittersnap L3 ·
# thugs = Rioter L-1.
# =====================================================================
ev("cend","C. Eel's End",
  B.s_milestone("<p><strong>C. Eel's End</strong> — a warship and four moored barges of vice ruled by "+act("devargo","Devargo Barvasi")+", the self-styled King of Spiders. Cressida sends the PCs to recover blackmail letters proving the Chelish ambassador Amprei's misdeeds. <strong>The goal is the letters, not Devargo's head</strong> — the intended path is social (please him with bribes and entertainment), though stealth or force are possible (force is dangerous at this level).</p>")
  +SEC("<p><strong>A Walk with Vencarlo.</strong> Vencarlo Orisini escorts the PCs to Old Korvosa — develop him as a likable mentor; he is secretly the folk-hero <strong>Blackjack</strong> and is quietly assessing the party as a potential heir. He recurs throughout the campaign. "+chk("type:society|dc:20")+" recalls hearing of the old scandal binding Grau, Vencarlo, and Sabina — both were his students before the falling-out.</p>")
  +SEC("<p><strong>Devargo's fate is open.</strong> He pays his vice taxes and polices Eel's End, so the Guard leaves him be — but if the PCs kill him, the Guard quietly thanks them (no charges). <strong>Burning the barges</strong>, however, destroys the evidence and brings arson/murder prosecution. The easiest win is Diplomacy in "+pg(P["C7"],"the throne room (C7)")+".</p>")
  +B.s_skill("<p>Eel's End welcomes nearly everyone; only obvious Korvosan Guard, Hellknights, or Sable Company are turned away. Claiming Guard business but professing interest in a <em>hideout</em> (not Devargo) grants a large circumstance bonus to talk past the guards.</p>"))

area("C1","Eel's End Pier", SR("C1","50")
  +box("C1","<p>The sound of carousing booms from the elegantly painted barges moored to this long pier. Painted signs in several languages hang from ropes and pilings: 'The Twin Tigers,' 'Welcome to the Goldenhawk,' 'Dragon's Breath Corridor,' and 'The House of Clouds.' Only the largest vessel — an old warship to the south — bears no sign. Rope bridges and gangplanks link the decks.</p>")
  +"<p>The pier is the approach to "+act("devargo","Devargo's")+" floating empire. Four "+act("enforcer","Eel's End enforcers")+" loiter as security; they shake down well-dressed visitors but cave to greed.</p>"
  +B.enc("Eel's End Enforcers (pier)",xpb([2,2,2,2],4),
     "<p>4 "+act("enforcer","enforcers")+" with saps. They would much rather fleece the PCs than fight — talking past them is far cheaper than a brawl.</p>",
     B.aside_token(["4× "+act("enforcer","Enforcer (2)")], img=TOK("eels-end-enforcer"))))

area("C2","Eel's End Deck", SR("C2","51")
  +box("C2","<p>The large ship tied off to the pier bears the name <em>Eel's End</em>; its figurehead is a coiling eel with a woman's head. Drunkards and revelers dance on the open main deck, while the aft deck is clear. A pair of double doors painted with a complex spider open into the stern.</p>")
  +"<p>Four "+act("enforcer","enforcers")+" sleep in the rigging; two more guard the doors to "+pg(P["C7"],"C7")+", barring the unexpected. "+chk("type:deception|dc:20")+" (claim Devargo expects you), "+chk("type:diplomacy|dc:27")+" (only "+chk("type:diplomacy|dc:18")+" if the PCs say they're on Guard business hunting a hiding man), or "+chk("type:intimidation|dc:17")+" (the guards then nervously escort you in) gets past them.</p>"
  +B.enc("Eel's End Enforcers (deck)",xpb([2]*6,4),
     "<p>All 6 deck "+act("enforcer","enforcers")+" if a fight erupts — a <strong>Severe</strong> brawl at this level. The whole point of Eel's End is to <em>avoid</em> this by talking or sneaking.</p>",
     B.aside_token(["6× "+act("enforcer","Enforcer (2)")], img=TOK("eels-end-enforcer"))))

area("C3","The Goldenhawk", SR("C3","51")
  +"<p>A floating flophouse (4 sp/night) run by a lisping, walleyed gnome named <strong>Tuggins</strong>, who hoards a jingling ring of keys (he has forgotten what most open). Devargo's presence keeps it relatively safe; in a fight, Tuggins hides under a bunk.</p>")

area("C4","The Twin Tigers", SR("C4","51")
  +box("C4","<p>Two hut-like structures sit atop this barge; raucous laughter and periodic roars of victory sound from within.</p>")
  +"<p>A gambling barge — packed tables of dice, cards, and spinning wheels, with <strong>knivesies</strong> (see "+pg(P["C6"],"C6")+") a house favorite. A fine place to win (or lose) the bribe money, or to overhear rumors. Fights break out here more than anywhere else on Eel's End, so one of the four pier "+act("enforcer","enforcers")+" is always posted inside; brawlers go over the side — and on lucky nights the jigsaw sharks and reefclaws aren't waiting.</p>"
  +"<p><strong>The masters:</strong> twin Vudrani brothers wrapped in red veils. <strong>Anpugit</strong>, garrulous, does the talking; <strong>Rajeek</strong> hangs back, quietly watching for cheaters — and for chances to tilt a game the house's way. Both are always hunting new games for their floor (a PC with an exotic gambling game can earn real goodwill here).</p>")

area("C5","The House of Clouds", SR("C5","51")
  +box("C5","<p>A single long structure sits atop the main deck, double doors open onto a room of throw rugs and pillows, the air thick with incense and red lantern-light. Braziers shaped as serpents and hunting birds breathe anise, rosewater, and cinnamon. Scantily clad men and women loiter on deck.</p>")
  +"<p>A brothel run by the half-elf madam <strong>Halvara</strong> (5 gp a turn; 100 gp for her personal company), rumored to be Devargo's sometime lover — so few patrons dare cause trouble.</p>")

area("C6","Dragon's Breath Corridor", SR("C6","52")
  +box("C6","<p>This once-proud vessel, the <em>Dragon's Breath</em>, has been painted gaudy red. A sign at the aft entrance reads simply, 'Pass into the Dreams of the Dragon.'</p>")
  +"<p>A dream-spider-smoke den run by <strong>Bezzeraty</strong> (5 gp entry), and the home of <strong>knivesies</strong> — Devargo's favorite blood-sport.</p>"
  +B.s_skill("<p><strong>The smoke:</strong> a minute in the haze forces a "+chk("type:fortitude|dc:17")+" or the fumes leave you "+B.cond("clumsy","Clumsy 1")+" and "+B.cond("stupefied","Stupefied 1")+" for 1 hour (no further effect for 24 hours). Bezzeraty robs anyone who passes out.</p>")
  +B.s_skill("<p><strong>Knivesies</strong> — Riddleport's blood-sport, beloved of Devargo. Two contestants stand on opposite ends of a long table, <strong>right hands strapped to their sides</strong> with boiled leather, a belt pouch at each waist and a dagger stuck in the tabletop between them. During a count of ten, bettors toss gold onto the table — roll [[/r 3d6+20]]{3d6+20 gp} for the pot — and stand at the end held by their chosen fighter. Then both contestants roll initiative.</p>"
   "<p><strong>Playing it in PF2e.</strong> Each turn a contestant can (one free hand only!): <strong>Snatch coins</strong> — a single Interact action that grabs [[/r 1d10]]{1d10 coins} but lets the opponent make a Ready-style Strike or Trip against you; <strong>grab the dagger</strong> (Interact — the round-1 lunge); Strike; or Shove/Trip ("+chk("type:athletics")+") to force the opponent off the table. Falling, touching the ground, or going unconscious loses instantly; otherwise the game ends when no coins remain on the table (or one is knocked off), and whoever pouched more coins wins. <strong>Payout:</strong> the winner takes half the pot; the rest is split among the bettors at the winner's end.</p>"
   "<p>Winning games for Devargo's amusement raises your standing in "+pg(P["C7"],"C7")+" — each win is a big step toward the letters.</p>"))

area("C7","Throne of Spiders", SR("C7","52-54")
  +box("C7","<p>This converted captain's cabin is a throne room, its walls thick with webs in which scuttle dozens of spiders that never leave their silk. Two oaken tables and chairs fill the floor; aft, a cobwebbed leather chair sits on a low stage. A narrow door to port hangs ajar over stairs leading below. An iron birdcage hangs from the ceiling like a chandelier.</p>")
  +"<p>"+act("devargo","Devargo Barvasi")+" holds court here from noon to a few hours past dusk, evaluating six hopeful thugs over a feast — a tall, muscular man with shaggy black hair and a fierce glare, black leather accented by a steel spider-shaped baldric, blade-knuckled gauntlets glistening with poison, and live spiders wandering his skin unremarked. (After midnight he retires below to "+pg(P["C14"],"C14")+" — the best hours to infiltrate.) The caged "+B.mon("house-drake","house drake")+" <strong>Majenko</strong> is his tormented plaything (he will sell it for an absurd 5,000 gp; freed — cage "+chk("type:athletics|dc:25")+" to Force Open or "+chk("type:thievery|dc:23")+" to pick — it serves its rescuer for a year). A hidden trap door before the throne ("+chk("type:perception|dc:20")+" to spot, again to find the throne-arm switch) drops a petitioner into "+pg(P["C15"],"C15")+" — "+chk("type:reflex|dc:17")+" to cling to the sides if it springs.</p>"
  +SEC("<p><strong>Winning the letters (social).</strong> Have one PC plead the case (standing — note — on the trap door) and roll "+chk("type:diplomacy|dc:24")+"; others may Aid ("+chk("type:diplomacy|dc:18")+"). Devargo despises Intimidation (it starts a fight). Outcomes: <strong>fail badly</strong> → he springs the trap and attacks; <strong>partial</strong> → he wants gold/entertainment (bribes raise his attitude ~+1 per 10 gp; each knivesies win is worth a big step); <strong>success</strong> → he sells the last two letters for ~150 gp (a second "+chk("type:diplomacy|dc:23")+" knocks it to ~100 gp); <strong>critical</strong> → delighted, he hands them over and wishes the PCs well. <strong>Story award</strong> for getting the letters without combat.</p>")
  +B.enc("Devargo + hopeful thugs (if it turns violent)",xpb([5]+[-1]*6,4),
     "<p>"+act("devargo","Devargo")+" springs the trap door, then fights with poisoned gauntlets and Sneak Attack; he flees (invisible) below ~10 HP. The 6 hopeful "+act("rioter","thugs")+" are cowards who flee at the first damage and trip over each other. Enforcers from "+pg(P["C2"],"C2")+" arrive one per round once the alarm sounds.</p>",
     B.aside_token([act("devargo","Devargo Barvasi (5)"), "6× "+act("rioter","Hopeful Thug (−1)"), B.mon("house-drake","Majenko — caged")], img=TOK("devargo-barvasi")))
  +SEC("<p><strong>Critical success — Devargo's confession.</strong> Delighted (a critical "+chk("type:diplomacy|dc:24")+", or enough bribes and knivesies wins to charm him outright), Devargo claps his hands, calls four enforcers to mind the PCs, fetches the letters himself from below, and gleefully tells the whole story: hearing rumors of <strong>Amprei's affair</strong> with the wife of an important Chelish noble, he paid the ambassador a 'friendly' visit — a gift of shiver vials and an offer of a Cheliax trade line. Amprei had him thrown out, so Devargo <strong>pickpocketed the man's house key on the way</strong>, returned that night to put the key back — and left with a sheaf of the ambassador's love letters. Since then he has been <strong>selling them back one every few weeks</strong>, savoring Amprei's squirming on each visit; that the ambassador buys quietly instead of going to the Guard says everything about how ruinous the contents are. He hands over the last two letters — 'Pleasure doing business with you!' — and expects the PCs gone before he gets bored.</p>")
  +B.s_conv("<p>Releasing Majenko earns a story award and a loyal, information-gathering house-drake ally. The real goal remains the letters — turn them over to Cressida (Event 10 reward). <strong>Loot if he falls:</strong> his runed armor, gauntlets, venom, potions — and his key ring and 79 gp purse (see his sheet); the keys open the brewery ("+pg(P["C9"],"C9")+") and the sea chest ("+pg(P["C14"],"C14")+").</p>"))

pages.append(newpage("Cbelow","C8-C12 & C16. Below Decks", SR("C8-C12, C16","54")
  +"<p>The stairs behind the throne room ("+pg(P["C7"],"C7")+") drop into the old warship's working guts. Everything here is locked or guarded by habit rather than men (a locked below-decks door is "+chk("type:thievery|dc:20")+" to pick; Devargo's key ring opens them all) — Devargo's people rarely come below except to brew ("+pg(P["C9"],"C9")+") or to dump a body to Chittersnap ("+pg(P["C15"],"C15")+").</p>"
  +'<p class="subhead"><strong>C8. Privies</strong></p>'
  +"<p>Three narrow privies line the wall, their befouled chutes opening straight into the river below. The chutes are an entrance of last resort: nothing larger than <strong>Tiny</strong> fits, and even a Tiny creature must Squeeze through with a successful "+chk("type:acrobatics|dc:28")+".</p>"
  +'<p class="subhead"><strong>C10. Brig</strong></p>'
  +box("C10","<p>The room is empty and foul-smelling save for a mound of filthy straw seething with vermin.</p>")
  +"<p>Most troublemakers go straight down the trap door to Chittersnap — but when Devargo needs someone kept <em>alive</em>, they're stashed in this brig. It is currently empty (a ready-made cell if the GM needs one, or a place for captured PCs to wake).</p>"
  +'<p class="subhead"><strong>C11. Bilge Access</strong></p>'
  +"<p>A hatch-opening drops 7 feet into the flooded bilge ("+'C16'+" below). A slimy knotted rope dangles over the lip ("+chk("type:athletics|dc:14")+" to Climb).</p>"
  +'<p class="subhead"><strong>C12. Hold</strong></p>'
  +box("C12","<p>Crates, barrels, and broken furniture awaiting repair crowd this cramped hold.</p>")
  +"<p>Food, water, and firewood — little of actual value, but plenty of cover for sneaking PCs.</p>"
  +'<p class="subhead"><strong>C16. Bilge</strong></p>'
  +box("C16","<p>Murky water floods the filthy bilge, its surface dark and calm.</p>")
  +"<p>The bilge leaks terribly — only the old pier pilings propping the hull from below keep <em>Eel's End</em> afloat. The water stands <strong>2 feet deep</strong> (difficult terrain); Devargo stores nothing down here anymore. It connects the knotted rope ("+'C11'+") with the web-choked den ("+pg(P["C15"],"C15")+") and the sodden hold ("+pg(P["C17"],"C17")+") — a dark, wet backdoor through the ship.</p>"))

area("C9","Shiver Brewery", SR("C9","54")
  +box("C9","<p>Two big wood stoves are set into the curve of the hull, iron bars across each hung with cauldrons; firewood is mounded to the north, and dozens of empty glass vials crowd the stove mantles.</p>")
  +"<p>The locked door answers to Devargo's key (or "+chk("type:thievery|dc:20")+" to pick). A strange, bitter smell: the cauldrons boil alcohol, water, and dream-spider venom down into <strong>shiver</strong> for the Arkonas — a few hours' work a week (with Chittersnap's 'help') that keeps Devargo's vice taxes paid.</p>"
  +B.s_treasure("<p>Among the empty vials sit six doses of shiver (~25 gp each in 1e; story contraband, not loot — destroying it pays off a 'Drug Addict' background hook).</p>"))

area("C13","Meeting Room", SR("C13","54")
  +box("C13","<p>A single low desk sits against the wall of this room. A large wooden door marked with a painting of a spider stands in the southern wall.</p>")
  +"<p>Where Devargo receives his rare <em>important</em> guests — so rarely that he has moved both chairs up to the throne room ("+pg(P["C7"],"C7")+") to seat more sycophants. The spider-painted door leads to his quarters ("+pg(P["C14"],"C14")+"); his sea chest and treasures are in there, not here.</p>")

area("C14","Devargo's Quarters", SR("C14","54")
  +box("C14","<p>A clean, dry wooden chamber: a four-poster bed with carved posts and gauzy drapes against the far wall, a dresser, a round table and chair — and a wooden sea chest at the foot of the bed.</p>")
  +"<p>Devargo retires here after midnight to read the day's slate reports and sleep — the <strong>best time to infiltrate</strong> Eel's End — and flees here if the throne room ("+pg(P["C7"],"C7")+") goes badly for him.</p>"
  +B.s_treasure("<p><strong>The sea chest</strong> opens to the key Devargo carries or "+chk("type:thievery|dc:28")+". His favourite treasures, re-scaled to PF2e: a jasper-studded amulet and an emerald-set gold necklace (art objects, ~120 gp the pair), a <strong>ring of feather fall</strong> with a jade-dragonfly cameo, a <strong>scroll of <em>blur</em></strong>, an <strong>elixir of love</strong>, two pouches of <strong>dust of appearance</strong>, a mother-of-pearl horn (~10 gp), and ~60 gp in coin.</p>")
  +SEC("<p><strong>And the prize:</strong> the chest also holds <strong>the last two scandalous letters</strong> to Ambassador Amprei from <strong>Verania Tvastiox</strong> — the young wife of one of Amprei's superiors back in Cheliax. The details are salacious and <em>exacting</em>, leaving no room for misinterpretation; made public, they would end the ambassador. This is the entire object of the mission — a stealth route to this chest skips the throne-room confrontation completely.</p>")
  +B.s_conv("<p>However the PCs obtain them, the two letters go to Cressida Kroft for the Event 10 reward (and her leverage over Ambassador Amprei).</p>"))

area("C15","The Spider's Web", SR("C15","54-55")
  +box("C15","<p>This dark chamber is riddled with dizzying tunnels of thick cobweb. The floor is a sticky mass of webbing and hundreds of bones — many of them humanoid. Some webs shimmer and dance, almost reflecting rainbows.</p>")
  +"<p>The lair of "+act("chittersnap","Chittersnap")+", the ettercap who is the true source of Devargo's 'spider control,' beneath the throne's trap door. The shimmering strands are dream-spider webs: every square is difficult terrain and a "+chk("type:reflex|dc:15")+" each round avoids their contact poison.</p>"
  +B.enc("Chittersnap's den",xpb([3,B.mon_lvl("hunting-spider"),B.mon_lvl("dream-spider"),B.mon_lvl("dream-spider")],4),
     "<p>"+act("chittersnap","Chittersnap")+" (ettercap), one "+B.mon("hunting-spider","giant spider")+", and two "+B.mon("dream-spider","dream spiders")+". Kill the ettercap and every spider on Eel's End turns feral — even on Devargo.</p>",
     B.aside_token([act("chittersnap","Chittersnap (3)"), B.mon("hunting-spider","Giant Spider (1)"), "2× "+B.mon("dream-spider","Dream Spider (0)")], img=TOK("chittersnap")))
  +B.s_treasure("<p>Chittersnap hoards what falls down with its meals — the GM may seed a few coins and a minor trinket among the bones.</p>"))

area("C17","Sodden Hold", SR("C17","55")
  +box("C17","<p>This old cargo bay is partially collapsed; only a soggy section of hull remains in the center, the rest open to the river.</p>")
  +B.enc("Jigsaw Shark",xpb([1],4),
     "<p>A "+act("jigsawshark","jigsaw shark")+" (the same river-scavenger species from the Old Fishery) prowls the flooded hold — a hazard for anyone dumped through the "+pg(P["C7"],"trap door")+" who drifts down here.</p>",
     B.aside_token([act("jigsawshark","Jigsaw Shark (1)")], img=TOK("jigsaw-shark"))))

# =====================================================================
# PART THREE — D. THE DEAD WARRENS (Rolth's lab, run by Vreeg). Party ~L4.
# Derro L2 · Skeletal Owlbear L2 · Cabbagehead L4 · Vreeg L5 · Stirge L-1.
# Official: Otyugh L4, Skeleton Guard L-1, Necrophidius L3, Carrion Golem L4,
# Zombie Shambler L-1.
# =====================================================================
ev("dwarrens","D. The Dead Warrens",
  B.s_milestone("<p><strong>D. The Dead Warrens</strong> — a derro-infested undercity laboratory beneath Potter's Ward, the last chapter site (the PCs recover the murdered Shoanti boy Gaekhen's body here for Event 13). <strong>The entrance</strong> matches Elkaris's testimony ("+pg(P["e13"],"Event 13")+"): a partially collapsed mausoleum near the ward's southern edge, a toppled, headless sword-wielding gargoyle statue in the dirt before it. Wheelbarrow tracks at the surface ("+chk("type:perception|dc:15")+", "+chk("type:nature|dc:21")+" to read the small bare footprints around them as derro) lead behind the gargoyle to a poorly hidden trap-door inside ("+chk("type:perception|dc:15")+").</p>")
  +SEC("<p><strong>GM:</strong> This is one of several labs kept by the necromancer <strong>Rolth</strong> (Gaedren Lamm's estranged son, the 'Key-Lock Killer'). <strong>Rolth is absent</strong> — away securing a scroll — and is <em>not</em> scheduled to appear; he returns after the PCs leave to find his lair wrecked, and hunts them in Chapter 2. In his stead the warrens are run by his derro apprentice "+act("vreeg","Vreeg")+".</p>")
  +SEC("<p><strong>Gaekhen's body is in four parts</strong> (Rolth harvested only the head): the <strong>legs</strong> in the corpse dump ("+pg(P["D4"],"D4")+"), the <strong>left arm</strong> clutched by the carrion golem ("+pg(P["D8"],"D8")+"), the <strong>head</strong> stitched to the flesh golem in the stitchery ("+pg(P["D11"],"D11")+"), and the <strong>torso + right arm</strong> — crudely animated by Vreeg — twitching on the bench in his chamber ("+pg(P["D13"],"D13")+"). Thousand Bones needs all four parts, not a whole body.</p>")
  +B.s_conv("<p><strong>Running the difficulty.</strong> In PF2e a lone at-level creature reads as <em>Trivial–Low</em> for four PCs, so most warren rooms are individually easy — the dungeon is an <strong>attrition gauntlet</strong>, not a string of set-piece fights.</p>"
   "<ul>"
   "<li>A "+act("derro","derro")+" who spots the party flees the "+pg(P["D2"],"crawl-spaces")+" to pull its kin — combine "+pg(P["D3"],"D3")+"/"+pg(P["D5"],"D5")+"/"+pg(P["D7"],"D7")+" into one Low–Moderate fight.</li>"
   "<li>The "+pg(P["D1"],"ossuary")+" skeletons <em>pursue</em> — add them to a later room.</li>"
   "<li>The climax — "+act("vreeg","Vreeg")+" in "+pg(P["D13"],"D13")+" — is the warrens' set-piece boss.</li>"
   "</ul>"))

area("D1","Ossuary", SR("D1","56")
  +box("D1","<p>This large room is supported by four wide pillars of stone beneath a twenty-foot dome. The walls are caked with skeletons set in mud — mostly adult human bones, with smaller ones here and there. Fifteen-foot-square bone-pits sit east and west; a crude hole gouged in the south wall opens a tunnel.</p>")
  +"<p>An abandoned ossuary. Rolth animated guardians in the bone pits — four "+B.mon("skeleton-guard","human skeletons")+" (west) and a "+act("skelowlbear","skeletal owlbear")+" (east), spotted before they rise with "+chk("type:perception|dc:19")+". The skeletons pursue throughout the warrens but never up into Potter's Ward.</p>"
  +B.enc("Animated guardians",xpb([2,-1,-1,-1,-1],4),
     "<p>The "+act("skelowlbear","skeletal owlbear")+" and 4 "+B.mon("skeleton-guard","human skeletons")+" clatter up to attack. (The owlbear squeezes between the pillars and treats the narrow stairs as difficult terrain; unlike the skeletons it never leaves this room.)</p>",
     B.aside_token([act("skelowlbear","Skeletal Owlbear (2)"), "4× "+B.mon("skeleton-guard","Human Skeleton (−1)")], img=TOK("skeletal-owlbear")))
  +SEC("<p><strong>Foreshadowing (campaign):</strong> the ossuary was abandoned when the church of Pharasma moved its primary ossuary beneath the new cathedral. <strong>Later in the campaign the Pharasmins secretly ally with the growing rebellion against Queen Ileosa</strong> and offer the Dead Warrens — this room in particular — as a safe place for the rebellion to meet and plan. Clearing it now literally clears the rebellion's future war room; remind the players of this place when it returns.</p>"))

area("D2","Crawl Spaces", SR("D2","56")
  +"<p>Cramped secret tunnels the derros use to flit between rooms. Each concealed door is found with "+chk("type:perception|dc:21")+". They let the derros flank, ambush, and flee to raise the alarm.</p>")

area("D3","Derro Cave", SR("D3","56")
  +box("D3","<p>Rank with sweat and mud, the cavern holds four filthy straw pallets and a low table littered with dice and a miniature maze of carved clay.</p>")
  +"<p>The derros' filthy rest-and-mess room. Two of Vreeg's four "+act("derro","derros")+" are here at any time, playing <strong>Rat Squish</strong> — a complex, cruel game involving a live rat, the clay maze, numbered stones, a hammer, and a pair of pliers. They snatch up weapons and attack the instant they notice intruders.</p>"
  +B.enc("Derros at rest",xpb([2,2],4),
     "<p>2 "+act("derro","derros")+". Others may arrive via "+pg(P["D2"],"the crawl spaces")+" if the alarm goes up.</p>",
     B.aside_token(["2× "+act("derro","Derro (2)")], img=TOK("derro"))))

area("D4","Corpse Dump", SR("D4","56-57")
  +box("D4","<p>The majority of this room contains a nasty-looking stretch of mud — a partially collapsed sinkhole kept damp by seeping water. A patch of solid ground forms an island heaped with a reeking pile of body parts. A rickety wheelbarrow lies on its side to the north.</p>")
  +"<p>An "+B.mon("otyugh","otyugh")+" Rolth lured here to dispose of the derros' grisly discards wallows in the mud. It cries 'Warm food!' and lumbers out to attack.</p>"
  +B.enc("Otyugh",xpb([B.mon_lvl("otyugh")],4),
     "<p>One "+B.mon("otyugh","otyugh")+" — grab-and-drag, plus its filth-borne disease.</p>",
     B.aside_token([B.mon("otyugh","Otyugh (4)")]))
  +B.s_treasure("<p>Among the body parts: <strong>Gaekhen's tattooed legs and hips</strong> (one of four body parts). "+chk("type:perception|dc:23")+" sifting the mud also turns up trinkets — an amber necklace (~35 gp re-scaled), a silver dagger, a sealed <strong>elixir of vision</strong>, a <strong>wand of spiritual weapon</strong>, and a <strong>ring of swimming</strong>.</p>"))

area("D5","Exsanguination Chamber", SR("D5","57")
  +box("D5","<p>Three wooden tables stand in the middle of this room, their surfaces stained red. To the east, a ten-foot-wide hutch with wicker doors opens onto a straw-lined cage.</p>")
  +"<p>A lone "+act("derro","derro")+" drains a fresh corpse with Rolth's blood-tools — a hutch of "+act("stirge","stirges")+". She shrieks, flings open the hutch, and flees through "+pg(P["D2"],"the crawl spaces")+" to warn "+pg(P["D3"],"D3")+". Four gorged stirges on the body ignore the PCs; two hungry ones attack.</p>"
  +B.enc("Derro + stirges",xpb([2,-1,-1],4),
     "<p>1 "+act("derro","derro")+" (flees to raise the alarm) + 2 hungry "+act("stirge","stirges")+".</p>",
     B.aside_token([act("derro","Derro (2)"), "2× "+act("stirge","Stirge (−1)")], img=TOK("stirge"))))

area("D6","Necrophidius Corridor", SR("D6","57")
  +box("D6","<p>The walls and ceiling of this tall hallway are encrusted with dozens of yawning skulls, their mouths opening into dark holes in the walls.</p>")
  +"<p>Two of the skulls are the heads of "+B.mon("necrophidius","necrophidiuses")+" — silent skeletal serpents Rolth crafted from the skulls of two old Key-Lock Killer victims — housed motionless in the walls, one at each far end, until the room's trap springs; they then slither out and strike with surprise unless a PC hears the telltale rattle of ribs against stone.</p>"
  +"<p>The "+haz("acidskulls","Acid-Spraying Skulls")+" trap fires two rounds after a creature enters; Rolth and the derros dart through before it triggers (door to "+pg(P["D7"],"D7")+" ↔ secret door to "+pg(P["D2"],"D2")+", "+chk("type:perception|dc:21")+" to find).</p>"
  +B.enc("Necrophidiuses (+ acid trap)",xpb([B.mon_lvl("necrophidius"),B.mon_lvl("necrophidius")],4),
     "<p>2 "+B.mon("necrophidius","necrophidiuses")+" (their dance can stun) plus the "+haz("acidskulls","acid-skull")+" trap raking the whole hall.</p>",
     B.aside_token(["2× "+B.mon("necrophidius","Necrophidius (3)"), haz("acidskulls","Acid-Spraying Skulls (1)")])))

area("D7","Alchemy Lab", SR("D7","58")
  +box("D7","<p>The wooden tables here are stacked with vials, beakers, and alchemical gear; the southern one is heaped with broken glass and leans on a hastily repaired leg. Three cauldrons sit against the east wall, one upended, its rancid rendered-fat contents spilled across the floor.</p>")
  +"<p>The fourth "+act("derro","derro")+" minion cleans up after a "+pg(P["D8"],"carrion golem")+" smashed through earlier. He dithers in confusion for a round, unsure whether to fight or run for help.</p>"
  +B.enc("Lone derro",xpb([2],4),
     "<p>1 "+act("derro","derro")+", caught off balance.</p>",
     B.aside_token([act("derro","Derro (2)")], img=TOK("derro")))
  +B.s_treasure("<p>"+chk("type:perception|dc:20")+" (10 minutes' search) recovers usable salvage: an alchemist's lab, 3 doses of <strong>vermin repellent</strong> (Rolth is Gaedren's source for it), 2 tanglefoot bags, 4 doses of black adder venom, a hybridization funnel, 2 doses of silversheen, and a <strong>handy haversack</strong> holding 3 potions of healing, a lesser restoration potion, a potion of invisibility, 2 scrolls of <em>false life</em>, and a scroll of <em>dispel magic</em>.</p>"))

area("D8","Store Room", SR("D8","58")
  +"<p><strong>The door is boarded over:</strong> break it down ("+chk("type:athletics|dc:23")+") or pry the boards off — easy, but a noisy few minutes of work that announces the party to anything listening.</p>"
  +box("D8","<p>The one-time pantry is in shambles — broken crates and shelves strewn about, foodstuffs, firewood, and other supplies scattered across the floor.</p>")
  +"<p>Early this morning Rolth's newest "+B.mon("carrion-golem","carrion golem")+" went berserk, tore from its table in "+pg(P["D11"],"D11")+", and rampaged through "+pg(P["D7"],"D7")+" before he trapped it in here to 'simmer' — the delay (and the shopping list of smashed glassware) is why Rolth is absent today, and why he doesn't return until the PCs are gone. Open the door and the golem attacks at once, still clutching a tattooed severed arm.</p>"
  +B.enc("Carrion Golem",xpb([B.mon_lvl("carrion-golem")],4),
     "<p>One berserk "+B.mon("carrion-golem","carrion golem")+" — a patchwork construct of rotting parts.</p>",
     B.aside_token([B.mon("carrion-golem","Carrion Golem (4)")]))
  +B.s_treasure("<p>The arm the golem clutches is <strong>Gaekhen's left arm</strong> (a third body part), marked with Shoanti tattoos.</p>"))

area("D9","Prisoner Pits", SR("D9","58-59")
  +box("D9","<p>This foul-smelling cavern is bordered on three sides by ten-foot-deep pits reeking of excrement and decay. Each holds moldy straw, a trough of filthy water, rotting body parts — and a couple of still-living prisoners.</p>")
  +"<p>Six malnourished captives await Rolth's experiments. Their jailer is the ogrekin "+act("cabbagehead","Cabbagehead")+", who torments them to please his 'father' Rolth and fights to the death.</p>"
  +B.enc("Cabbagehead",xpb([4],4),
     "<p>The ogrekin "+act("cabbagehead","Cabbagehead")+" — a bare-fisted brute.</p>",
     B.aside_token([act("cabbagehead","Cabbagehead (4)")], img=TOK("cabbagehead")))
  +B.s_treasure("<p>Among the freed prisoners is the cutpurse <strong>Tiora</strong>; within a day she seeks out the PCs and gratefully gives them a <strong>wand of cure moderate wounds</strong> (34 charges).</p>"))

area("D10","Library", SR("D10","59")
  +box("D10","<p>Two wide, freestanding bookshelves furnish this room, filled with carefully arranged tomes and scrolls.</p>")
  +B.s_treasure("<p>Mostly necromancy and golem-craft treatises — plus a surprising number of books on <strong>disease and plague</strong> (a +2 circumstance bonus to relevant Recall Knowledge while using them; ominous foreshadowing of Chapter 2). The collection is worth ~30 gp re-scaled; tucked in an anatomy folio are a scroll of <em>identify</em> and a scroll of <em>command undead</em>.</p>"))

area("D11","Stitchery", SR("D11","59")
  +box("D11","<p>The nauseating mixture of decay and strange chemicals fills this room. Saws, pliers, long needles, and surgical tools line the shelves. On a sturdy central table lies a patchwork humanoid stitched from dozens of bodies — nearly seven feet tall.</p>")
  +SEC("<p>Rolth's workshop. The strapped-down flesh golem is unfinished; the small head stitched to it — short brown hair, a firepelt scar on the left cheek — is <strong>Gaekhen's head</strong> (one of the four body parts; the others lie in "+pg(P["D4"],"D4")+", "+pg(P["D8"],"D8")+", and "+pg(P["D13"],"D13")+"). Removing it without further indignity takes a careful "+chk("type:medicine|dc:15")+" or a steady hand and ten minutes.</p>")
  +B.s_treasure("<p>On the desk: a broken <strong>key-shaped dagger</strong> — Rolth's signature blade, twin to the one in "+pg(P["A14"],"Gaedren's den (A14)")+", confirming the connection. The PCs may not grasp its meaning until they meet Rolth in Chapter 2.</p>"))

area("D12","Rolth's Room", SR("D12","59")
  +box("D12","<p>This chamber holds a large four-poster bed and a simple writing desk, with a full-length mirror propped against an earthen wall.</p>")
  +SEC("<p>Rolth keeps little here. "+chk("type:perception|dc:21")+" (automatic if a PC looks behind the mirror) reveals a hidden niche: masterwork thieves' tools, a pearl-and-silver snuffbox (~25 gp re-scaled) holding a dose of <strong>dust of disappearance</strong>, and a <strong>sustaining spoon</strong>. His spellbooks are not here — he carries them.</p>"))

area("D13","Vreeg's Chamber", SR("D13","59-61")
  +box("D13","<p>A dry, well-kept chamber: a narrow bed, a half-bare shelf of books, bones, and skulls, and a long bench — on which lies a man's tattooed torso, right arm still attached, periodically thrashing and clutching at the air as if alive.</p>")
  +SEC("<p><strong>The torso on the bench is Gaekhen's</strong> — torso and right arm, the last of the four body parts. Vreeg claimed them before Rolth could discard them with the legs ("+pg(P["D4"],"D4")+"), and though the derro can't yet truly animate the dead, he infused the flesh with enough void energy to give it horrible, twitching half-life. <strong>If handled it thrashes and claws:</strong> one unarmed Strike per round, +0 melee for @Damage[1d3[bludgeoning]] (nonlethal), with a 50% miss chance from blindness. The animating spark is fragile — 2 HP, and vitality energy harms it as if it were undead. Putting it to rest is trivial; doing so <em>respectfully</em> matters to Thousand Bones.</p>")
  +"<p>"+act("vreeg","Vreeg")+" the derro necromancer lairs here, living simply — Rolth's lapdog when the master is present; lazy and cruel when he is not, spending 2-3 hours a day tormenting Cabbagehead and the other derros and the rest tinkering with necromancy or reading books borrowed from the library ("+pg(P["D10"],"D10")+"). He is attended by a single "+B.mon("zombie-shambler","human zombie")+" bodyguard left by Rolth. In a fight he flies out of reach, kites with rays and force missiles, hurls skeletons from his robe of bones, and saves Blindness for the front line.</p>"
  +SEC("<p><strong>The gut-punch.</strong> If the PCs left "+act("gaedren","Gaedren Lamm's")+" body in the fishery, this zombie <em>is</em> Gaedren — recovered and animated by his son Rolth. Mindless, it won't know them, but its appearance should unsettle the party and raise the question of <em>who</em> wanted the old man back in undeath.</p>")
  +B.enc("BOSS — Vreeg + zombie",xpb([5,B.mon_lvl("zombie-shambler")],4),
     "<p>"+act("vreeg","Vreeg")+" (the warrens' master) and his "+B.mon("zombie-shambler","zombie")+" guard. Bright light leaves Vreeg dazzled (derro sunlight vulnerability) — a real lever for the PCs.</p>",
     B.aside_token([act("vreeg","Vreeg (5)"), B.mon("zombie-shambler","Human Zombie / undead Gaedren (−1)")], img=TOK("vreeg")))
  +B.s_treasure("<p><strong>Vreeg's spellbook</strong> sits on the shelf: every spell he has prepared, plus a necromancer's cantrips (no conjuration or illusion) and a second tier of utility — animate/command-undead rites, <em>darkness</em>, a fall-arresting charm, a corpse-preserving rite, <em>fear</em>, <em>sleep</em>, and a water-breathing spell. Re-key each to the nearest PF2e common spell when a PC scribes or sells it (worth ~50 gp to an Acadamae buyer — or leverage with the Pharasmins).</p>"
   "<p><strong>His stash</strong>, stripped from the dead he has handled (re-scaled to PF2e): two silver rings (~10 gp each), a gold-and-pearl bracelet (~15 gp), a mithral hip flask etched with a house drake (~40 gp), and a <strong>traveler's any-tool</strong> — an uncommon magic implement that reshapes into any simple hand tool (counts as the relevant basic tool kit). His robe of bones, wand, ring, and dagger are on his sheet.</p>")
  +B.s_conv("<p>With Vreeg down and the four body parts gathered, the warrens are cleared — see "+pg(P["dconc"],"Chapter Conclusion")+" for returning Gaekhen. Rolth returns later to the ruin and becomes a Chapter 2 antagonist (CHG: his vendetta). <em>Faithful note:</em> the torso + right arm are kept here in D13 per the source (an earlier draft had them in "+pg(P["D11"],"D11")+").</p>"))

ev("dconc","Chapter Conclusion",
  SR("Chapter Conclusion","66-67")
  +B.s_milestone("<p><strong>Chapter Conclusion.</strong> With the Dead Warrens cleared and the scapegoat's fate resolved, 'Edge of Anarchy' ends on the attempted execution of an innocent — the PCs' first chance to stand directly against Ileosa's growing power. Run it as an interactive <strong>cut-scene</strong>, not a standard encounter. The PCs should be well into 4th level.</p>")
  +"<p><strong>Returning Gaekhen.</strong> The PCs need only deliver Gaekhen's four body parts to Cressida — she handles the delicate work of seeing the body de-animated, made whole, and returned to "+pg(P["e13"],"Thousand Bones")+" with dignity. She pays the recovery reward (folding in Trinia's deferred coin if applicable), and the Shoanti elder's goodwill becomes important in Chapter 4 (A History of Ashes). She also passes on the news of the sunset execution ("+pg(P["e14"],"Event 14")+") — and asks the PCs to attend.</p>"
  +vbox(["execution it is not an affair to be"],
     "<p>The execution is the social event of the season: Korvosa's gentry attend in garish gowns, fine capes, and blinding jewels. The whole affair feels like a grand ball, not the public death of an assassin.</p>",
     label="The Courtyard at Sunset")
  +"<p><strong>Staging.</strong> Heralds announce <strong>Queen Ileosa</strong> with drums and fanfare; she has fully taken up the mantle of sole monarch — poised, graceful, in a green-and-white silk dress worth thousands — attended by a small army of striking guards. Chief among them, all but unrecognizable in a brand-new suit of full plate with a closed helm and flowing crimson plume, is <strong>Sabina</strong> (the Gray Maidens' look, before the name exists). Ileosa takes a high throne-like chair at one end of the public courtyard; at the other stands a <strong>guillotine</strong>, beside it a towering hooded <strong>executioner</strong> idly holding an immense axe. Gossip ripples through the crowd — the queen's attire, how the traitor will comport herself, the identity of the armored guardian… even the PCs' own exploits, if you like.</p>"
  +"<p><strong>The procession.</strong> An ominous drumbeat silences the gawkers and paces <strong>Trinia's</strong> walk to the block. At the guillotine her shackles and hood are removed — a very frightened young woman bravely holding back tears, arms bound behind her with a leather cord — as the queen rises to address the crowd.</p>"
  +SEC("<p><strong>If the PCs hid Trinia,</strong> the prisoner revealed is a <em>secondary scapegoat</em> — superficially similar, equally innocent. Everything below plays out the same: Blackjack has no intention of letting <em>anyone</em> be falsely executed by the queen.</p>")
  +vbox(["'Fellow Korvosans! You have suffered greatly these",
         "'And so, without further delay, let us usher"],
     "<p>Ileosa tells the crowd their suffering — burned homes, dead kin, lost fortunes — ends today; she shares it, having lost a husband. Before them stands the source of their anguish: no timid girl but a black-hearted assassin, whose death she offers as a salve for all they've endured — and she calls for the new dawn to be ushered in with justice, ending on a shriek: off with her head!</p>",
     label="Queen Ileosa's Address")
  +"<p><strong>The rescue.</strong> Just before the executioner forces Trinia into the guillotine, he howls — a thrown dagger stands in the back of his hand — and a cry goes up: <em>'By the gods! It's Blackjack!'</em> A man in hooded cloak and black mask springs to Trinia's side, cuts her bonds, and hurls the same dagger down through the executioner's boot, pinning his foot to the platform. Then he turns to the stunned crowd:</p>"
  +vbox(["'Yes indeed, my queen! Let us usher"],
     "<p>Blackjack flings the queen's words back at her: justice indeed — justice for Korvosa, not for the shambles she calls a monarchy — and ends with the cry that will echo through the campaign: long live Korvosa; down with the queen!</p>",
     label="Blackjack's Declaration")
  +"<p><strong>Chaos.</strong> The crowd erupts — some scream for the assassin's head, others for the queen's resignation. Ileosa stands frozen a moment, whispers something to Sabina, and flees into Castle Korvosa with Sabina and a dozen guards covering her retreat. The remaining guards push toward Blackjack through blood-thirsty nobles — while the executioner wrenches free and raises his axe over the vigilante, who, delighting in having routed the queen, hasn't noticed.</p>"
  +'<p class="subhead"><strong>Involving the PCs</strong></p>'
  +"<p>Don't run this as a battle — go around the table and ask each player what their character does.</p>"
  +"<ul>"
   "<li><strong>If the PCs stay out of it</strong> (or their actions change little): Blackjack notices the axe in time, ducks away dragging Trinia with him, clambers up a hanging banner to a nearby wall, hauls her up, drinks a <em>potion of feather fall</em>, bows to the crowd backlit by the setting sun — and the two leap from the wall and vanish into the city.</li>"
   "<li><strong>If the PCs help Blackjack:</strong> narrate how their actions save his life (the axe-blow turned, a guard tripped, the crowd parted). When he reaches the wall, his bow is to <em>the PCs</em> in particular, rapier raised in salute, before he and Trinia leap to freedom.</li>"
   "<li><strong>If the PCs hinder him:</strong> let them roll attacks as needed. On low rolls, Blackjack and Trinia escape despite their efforts. <strong>On high rolls, let the dice stand:</strong> Blackjack is captured and unmasked as <strong>Vencarlo Orisini</strong> before being thrown into Castle Korvosa's deepest dungeons, and Trinia is executed after all — this time in a private chamber in the dungeons below. The remaining chapters assume both escaped; if not, things get harder for the PCs in the chapters to come, as you see fit (Chapter 3's Vencarlo thread in particular needs re-rigging).</li>"
   "</ul>"
  +SEC("<p><strong>Aftermath.</strong> Escaping the chaos is easy, and even PCs who visibly helped Blackjack face no Guard retribution — partly the confusion, mostly a shift in the city's heart: Blackjack has always been Korvosa's folk hero, and his open stand against the queen plants the first real doubts among her supporters. Ileosa stays ensconced in Castle Korvosa for several weeks, and the city finally gets room to breathe and rebuild.</p>")
  +vbox(["Yet however safe the city might seem"],
     "<p>But Korvosa sits in the eye of the storm. Greater wheels turn — and not far offshore, a black three-masted ship flying the orange lanterns of a plague vessel drifts ever closer. Death follows it.</p>",
     label="Closing — Read Aloud")
  +SEC("<p><strong>Into Chapter 2 — and the Blood Veil.</strong> That plague ship is the <em>Direption</em>, Chapter 2's opening. This is where the persistent-plague overlay begins: start the <strong>Epidemic Clock</strong> (Conversion Guide journal → <em>Blood Veil &amp; the Epidemic Clock</em>) seeded by how the city fared here. Rolth, returning to his ruined lair, becomes a recurring hunter (Chapter 2).</p>")
  +B.s_conv("<p><strong>Threads carried forward:</strong> Rolth's vendetta · the Arkona/Vimanda watch (from "+pg(P["B8"],"Verik")+") · Trinia &amp; Vencarlo/Blackjack · Grau and the Korvosan Guard · the Shoanti debt · and the queen, who now has the PCs' measure.</p>"))

# =====================================================================
# PREPARED SCENES — Part Three battlemaps (B/C/D areas) on Racooze geometry
# via B.racooze_scene (same firewall as the Old Fishery below: his walls/tiles
# inject from the GM's locally installed module, nothing redistributed). Keyed
# pins + staged tokens come from research/scene_keys.json (keying-fleet output,
# committed). Every id here draws on a SEPARATE deterministic stream so the
# main nid()/sid() pools — and every doc id above and below — stay untouched.
# =====================================================================
import html as _hx
_psg = B._idgen(881001); psid = lambda: next(_psg)
PS_PAGE_ID = psid()        # reserved FIRST so the page id survives keying edits
_PS_MM = "icons/svg/mystery-man.svg"
def _cid(name):
    """Community-copy actor id (the official-monster module copies are community
    docs); None if the community index is absent -> that token is dropped loudly."""
    _m = B._cmeta("npc", name)
    return _m["id"] if _m else None
# actor name -> (pack doc id, token squares). Ids resolve from the pilot registry
# (A) or the community index; squares follow the keying notes (Jigsaw Shark,
# Skeletal Owlbear, Otyugh, and Cabbagehead are Large 2x2 with gx/gy naming the
# top-left square; Small/Tiny creatures stage as 1x1 like Medium).
PS_ACTORS = {
    # Part Three B — All the World's Meat
    "Cow Hammer Boy": (A["cowhammer"], 1), "Verik Vancaskerkin": (A["verik"], 1),
    "Reefclaw": (_cid("Reefclaw"), 1), "Raktavarna Rakshasa": (_cid("Raktavarna Rakshasa"), 1),
    # Part Three C — Eel's End
    "Eel's End Enforcer": (A["enforcer"], 1), "Devargo Barvasi": (A["devargo"], 1),
    "Korvosan Rioter": (A["rioter"], 1), "Chittersnap": (A["chittersnap"], 1),
    "Giant Spider": (_cid("Giant Spider"), 1), "Dream Spider": (_cid("Dream Spider"), 1),
    "Jigsaw Shark": (A["jigsawshark"], 2),
    # Part Three D — The Dead Warrens
    "Human Skeleton": (_cid("Human Skeleton"), 1), "Skeletal Owlbear": (A["skelowlbear"], 2),
    "Derro": (A["derro"], 1), "Otyugh": (_cid("Otyugh"), 2), "Stirge": (A["stirge"], 1),
    "Necrophidius": (_cid("Necrophidius"), 1), "Acid-Spraying Skulls": (A["acidskulls"], 1),
    "Carrion Golem": (_cid("Carrion Golem"), 1), "Cabbagehead": (A["cabbagehead"], 2),
    "Vreeg": (A["vreeg"], 1), "Human Zombie": (_cid("Human Zombie"), 1),
}
_PS_KEYS_PATH = B.ROOT.parent / "research" / "scene_keys.json"
_PS_KEYS = ({e["scene"]: e for e in json.loads(_PS_KEYS_PATH.read_text(encoding="utf-8"))
             if e.get("chapter") == "ch1"} if _PS_KEYS_PATH.exists() else {})
if not _PS_KEYS:
    print("[scene] research/scene_keys.json absent -> Part Three scenes build without pins/tokens")
_PS_PAGE_BY_NAME = {_hx.unescape(p["name"]): p["_id"] for p in pages}
def _ps_pid(page_name, code):
    """Keyed pageName -> page id; falls back to the page whose name leads with
    the area code (e.g. C8 -> 'C8-C12 & C16. Below Decks'); None drops the pin."""
    _pid = _PS_PAGE_BY_NAME.get(_hx.unescape(page_name))
    if _pid: return _pid
    _pid = next((i for n, i in _PS_PAGE_BY_NAME.items()
                 if n.startswith(f"{code}.") or n.startswith(f"{code}-")), None)
    if _pid: print(f"  [scene] keyed page {page_name!r} missing -> matched by area code {code}")
    else:    print(f"  [scene] no page for pin {code} ({page_name!r}) -> pin dropped")
    return _pid

# Visual-QA placement corrections (2026-06-11 overlay re-review): keyed squares
# re-judged against the rendered canvases. Keyed by (racoozeName, token name,
# keyed gx, gy) so an upstream re-key in research/scene_keys.json retires each
# override automatically; values are corrected MAP-LOCAL squares.
_PS_TOKEN_FIX = {
    # Eel's End C7: rows y0-2 are black void above the cabin's north wall —
    # rehome both thugs onto interior floor at the feast tables.
    ("Eel's End", "Hopeful Thug", 4, 1): (6, 4),
    ("Eel's End", "Hopeful Thug", 9, 1): (9, 2),
    # Dead Warrens D9: the 2x2 jailer sat on the dark NW prisoner-pit floor;
    # (37,25) centers him on the rock floor ringed by the three pits.
    ("The Dead Warrens", "Cabbagehead", 36, 23): (37, 25),
}
PS_SCENES = [   # (racoozeName, displayName, pack slug, sort) — after Old Fishery (sort 0);
    # slug prefix = CHAPTER number (matches 01-old-fishery / the other chapters' packs)
    ("All The World's Meat", "All the World's Meat", "01-all-the-worlds-meat", 200000),
    ("Eel's End", "Eel's End", "01-eels-end", 300000),
    ("The Dead Warrens", "The Dead Warrens", "01-the-dead-warrens", 400000),
]
ps_counts = {}
for _rn, _dn, _slug, _sort in PS_SCENES:
    _k = _PS_KEYS.get(_rn, {})
    _ox, _oy = B.scene_origin(_rn)            # map-local squares -> scene px
    _pn, _pt = [], []
    for _n in _k.get("notes", []):
        _pid = _ps_pid(_n["pageName"], _n["code"])
        if _pid:
            _pn.append(B.note(psid(), JID, _pid, _n["label"],
                              _ox + int(round(_n["gx"] * 100)), _oy + int(round(_n["gy"] * 100))))
    for _t in _k.get("tokens", []):
        _aid, _sq = PS_ACTORS[_t["actor"]]    # unknown actor = build error by design
        if not _aid:
            print(f"  [scene] {_dn}: no actor doc for {_t['actor']!r} -> token dropped"); continue
        _gx, _gy = _PS_TOKEN_FIX.get((_rn, _t["name"], _t["gx"], _t["gy"]), (_t["gx"], _t["gy"]))
        _pt.append(B.token(psid(), _aid, _t["name"],
                           _ox + int(_gx) * 100, _oy + int(_gy) * 100,
                           B.token_art(_t["actor"]) or _PS_MM,
                           disposition=_t.get("disp", -1), hidden=True, width=_sq, height=_sq))
    _psc = B.racooze_scene(_rn, _dn, F["s_ch1"], _pn, _pt, sort=_sort)
    B.write("scenes", _slug, copy.deepcopy(_psc))
    ps_counts[_dn] = (len(_pn), len(_pt))
print("[scene] prepared Part Three scenes: "
      + ", ".join(f"{k} ({v[0]} pins/{v[1]} tokens)" for k, v in ps_counts.items()))

# GM staging page at the END of the chapter journal: links each prepared scene
# and digests the keying fleet's design notes (region guides, day/night moves,
# review flags, who is deliberately NOT staged) into compact run-time notes.
_ps_scn = lambda rn, label: scn(B.scene_id(rn), label)
pages.append(B.page(PS_PAGE_ID, "Prepared Scenes",
  "<p>Beyond the "+scn(SCN,"Old Fishery")+" (see "+pg(P["scene"],"Scene Setup")+"), Part Three ships three prepared scenes on <strong>Racooze's battlemap geometry</strong> — his walls, doors, and floor art inject at build time from your locally installed free battlemaps module (nothing of his is redistributed; without it they build as placeholder grids). Map-note pins link every area page; <strong>all staged tokens start hidden</strong> — reveal them as encounters break. Import via the Adventure (not the scene compendium alone) so the token actors exist in your world.</p>"

  +_sub(_ps_scn("All The World's Meat","All the World's Meat")+" — areas B1–B8")
  +"<p><strong>Canvas:</strong> two copies of one building footprint, side by side. The LEFT half is the ground floor (pins "+pg(P["B1"],"B1")+"–"+pg(P["B6"],"B6")+"); the RIGHT half repeats it under the upper-storey overlay tile, so only "+pg(P["B7"],"B7")+"/"+pg(P["B8"],"B8")+" show as rooms (the rest reads as roof). The "+pg(P["B2"],"B2")+" stair descending south is the climb to B7/B8; B4's bloodstained grate sits at its south edge; B8's desk-bed and paper table are east–west flipped versus the text — trust the canvas.</p>"
  +"<p><strong>Staging:</strong> the "+pg(P["B1"],"B1")+" pair (Baldrago, Malder) are neutral — the free-meat storefront; pushed past, they raise longbows and shout for B4. The "+pg(P["B4"],"B4")+" pair (Parns, Karralo) are the 75%-by-day post; on a miss they're tending B5/B6 livestock instead. The three Reefclaws sit on B4's grate squares but are actually BELOW the grate, in the half-flooded sewer tunnel running east to the river (the severed-finger evidence is down there too) — keep them hidden or note the elevation; they attack only if the remains are disturbed. "+act("verik","Verik")+" ("+pg(P["B8"],"B8")+", beside the desk-bed) dithers several rounds before joining any fight below and surrenders readily when shown the evidence — staged hostile, but skippable by design. The 'Silver Dagger' token IS the Raktavarna, disguised as the dagger pinning a paper to the east table (Tiny) — keep it hidden until exposed.</p>"
  +"<p><strong>Not staged:</strong> "+pg(P["B6"],"B6")+"'s livestock (a random handful of cows and pigs arrives each morning, sometimes none) — no actors; skittish, harmless flavor.</p>"

  +_sub(_ps_scn("Eel's End","Eel's End")+" — areas C1–C17")
  +"<p><strong>Canvas (composite, 42×27):</strong> bottom-left is the harbor overview — the "+pg(P["C1"],"C1")+" pier plus all five vessels' weather decks ("+pg(P["C3"],"Goldenhawk")+" = NW tilted barge; "+pg(P["C4"],"Twin Tigers")+" = NE, two shingled huts; "+pg(P["C5"],"House of Clouds")+" = west, one long roof; "+pg(P["C6"],"Dragon's Breath")+" = SE; the big unsigned center-south warship is Eel's End itself, the "+pg(P["C2"],"C2")+" deck). The top-left inset is the warship's stern-cabin interior = "+pg(P["C7"],"C7")+"'s throne room (stairs down at its NW corner). The middle hull is the warship's LOWER DECK, bow north ("+pg(P["Cbelow"],"C8–C12 & C16")+", "+pg(P["C9"],"C9")+", "+pg(P["C13"],"C13")+"–"+pg(P["C15"],"C15")+" — rooms verified by furniture; C13 is the chair-less desk room, its chairs moved up to C7; the unlabeled starboard room with a round table is the crew mess, no area code). The right hull is the BILGE level (C16/"+pg(P["C17"],"C17")+").</p>"
  +"<p><strong>Review flags:</strong> C13's spider-painted door to "+pg(P["C14"],"C14")+" sits in its NORTH wall here where the text says south — treat the map as authoritative. The bilge draws no C16/C17 division: the dry webbed platform at the pointed end is keyed as C17 and the open 2-ft murky water (pier pilings) as C16, but the platform's web wisps also evoke C15's den — swap C17's pin to the far end if you read it the other way.</p>"
  +"<p><strong>Staging:</strong> Devargo's people are <em>neutral</em> — a social encounter by design; only the "+pg(P["C15"],"C15")+" den and the "+pg(P["C17"],"C17")+" shark (Large 2×2) are hostile. By day "+act("devargo","Devargo")+" holds court in C7 (noon until a few hours past dusk) with six hopeful thugs at the feast tables — staged with the "+act("rioter","Korvosan Rioter")+" actor, as the C7 page links them; after midnight he is in C14, so <strong>move his token for night infiltrations</strong>. C7's hidden trap door in front of the throne (not drawn) drops straight to C15; on an alarm, C2 enforcers reinforce C7 one per round. The C4 enforcer counts among the four pier enforcers posted inside — while that token is active, remove one pier token if you want strictly four. C15's 'giant dream spider' is staged with the module Giant Spider actor (the page links the official equivalent).</p>"
  +"<p><strong>Not staged:</strong> Majenko, the caged pseudodragon in C7 (the page links the official house drake instead); the flavor NPCs Tuggins (C3 flophouse keeper, hides under a bunk), Anpugit &amp; Rajeek (C4 gambling-masters), Halvara (C5 madam), and Bezzeraty (C6 smoke-den keeper) — no actors, none fight; likewise the unnamed C2 revelers and C4 gambler crowds.</p>"

  +_sub(_ps_scn("The Dead Warrens","The Dead Warrens")+" — areas D1–D13")
  +"<p><strong>Canvas (single level, 50×33):</strong> the Potter's Ward mausoleum stairs enter "+pg(P["D1"],"D1")+" from the north. Region guide: D1 ossuary NW — the WEST bone pit holds the four skeletons, the EAST pit the owlbear; "+pg(P["D12"],"D12")+" and "+pg(P["D13"],"D13")+" along the north edge; "+pg(P["D11"],"D11")+" stitchery NE (patchwork body on the big table); "+pg(P["D10"],"D10")+" library center (the map draws three book racks where the text says two); "+pg(P["D9"],"D9")+" prisoner pits SE (the rock floor is ringed on three sides by dark 10-ft pits); "+pg(P["D8"],"D8")+" store room (boarded door on its NORTH side); "+pg(P["D7"],"D7")+" alchemy lab beside the skull-studded "+pg(P["D6"],"D6")+" corridor; "+pg(P["D5"],"D5")+" blood tables + black wicker stirge hutch; "+pg(P["D4"],"D4")+" corpse dump south (Gaekhen's legs are in the body-part pile at the mud island's south edge); "+pg(P["D3"],"D3")+" derro cave SW. The "+pg(P["D2"],"D2")+" pin marks the most prominent timber-braced crawl tunnel — more concealed crawl segments riddle the complex as the derros' flank-and-alarm network (each found per the D2 page).</p>"
  +"<p><strong>Staging:</strong> Large 2×2 tokens: Skeletal Owlbear, Otyugh, Cabbagehead. The D1 skeletons pursue intruders anywhere in the warrens but never to the surface; the owlbear never leaves D1 (pillar gaps and stairs are squeeze/difficult terrain for it). In D5 the four 'gorged' stirges on the fresh corpse ignore the PCs — only the two 'hungry' ones by the hutch attack — and the derro's first move is to flee through D2 to warn Vreeg; if the alarm spreads, fold the D5/D3/D7 derros into one Low–Moderate fight (headcount matches the journal: 2 in D3, 1 in D5, 1 in D7). In D6 both necrophidiuses start motionless inside the skull walls at the corridor's far ends; the mid-corridor "+haz("acidskulls","Acid-Spraying Skulls")+" token is the hazard actor — it fires two rounds after entry and rakes the whole hall. The "+pg(P["D8"],"D8")+" carrion golem still clutches Gaekhen's tattooed left arm and triggers the moment the boarded door opens.</p>"
  +"<p><strong>Finale ("+pg(P["D13"],"D13")+"):</strong> "+act("vreeg","Vreeg")+" kites flying with rays — bright light dazzles him (derro sunlight vulnerability). His bodyguard uses the Human Zombie actor: per the journal, if the PCs left Gaedren's body at the fishery, this zombie IS Gaedren, reanimated by Rolth.</p>"
  +"<p><strong>Not staged:</strong> the six malnourished D9 captives (incl. the cutpurse Tiora) — noncombatants in the pits; Gaekhen's twitching torso and right arm on the D13 bench (a 2-HP flavor hazard, described on the page); the unfinished flesh golem on the D11 table (inert — Gaekhen's head is stitched to it); and <em>Rolth himself</em> — his actor exists, but he is absent from the Warrens by design (away securing a scroll; he returns after the PCs leave and hunts them in Chapter 2).</p>",
  level=2))

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
GRID=100
area_codes=["A1","A2","A3","A4","A5","A6","A7","A8","A9","A10","A11","A12","A13","A14"]
# Racooze geometry (walls/doors/tiles), injected at build from the GM's installed
# battlemaps module via extract_racooze.mjs -> scripts/racooze_scenes.json
# (gitignored — his data is never committed, same firewall as AP.md read-aloud).
_RAC_PATH = B.ROOT / "scripts" / "racooze_scenes.json"
_RAC = json.loads(_RAC_PATH.read_text(encoding="utf-8")) if _RAC_PATH.exists() else {}
_FISH = _RAC.get("Old Fishery")
# embedded scene docs use their OWN deterministic id stream so the main nid()
# stream (and every doc id downstream of this section) is unaffected
_sgen = B._idgen(777001); snid = lambda: next(_sgen)
if _FISH:
    # canvas 3600x2200 @0.25 padding: LEFT half = first floor (tile @900,600),
    # RIGHT half = waterline level (tile @2700,600); both floors 18x22 squares
    ffpx = lambda gx, gy: (int(900 + gx * 100), int(600 + gy * 100))
    lfpx = lambda gx, gy: (int(2700 + gx * 100), int(600 + gy * 100))
    # Pin positions verified against the area texts (A10 = the ship's AFT CABIN on
    # the first floor — its stair drops to the hold A11 on the waterline map).
    # Visual-QA overlay pass (2026-06-11): A9/A10 moved off open river water onto
    # the ship (bow deck / webbed aft cabin); A11 into the hold interior; A12 onto
    # the escape-skiff walkway; A14 into the den room proper.
    NOTE_POS = {
        "A1": ffpx(6.5, 19.4), "A2": ffpx(15, 13), "A3": ffpx(2, 14.5), "A4": ffpx(9, 16.5),
        "A5": ffpx(13, 15), "A6": ffpx(11, 12.8), "A7": ffpx(6.5, 5), "A8": ffpx(5.5, 10),
        "A9": ffpx(9.5, 4.5), "A10": ffpx(13.5, 5), "A11": lfpx(12, 5), "A12": lfpx(8, 8),
        "A13": lfpx(8.5, 14), "A14": lfpx(5.5, 15),
    }
    NOTE_NAMES = {  # full page names so the pin TOOLTIP names the location
        "A1": "A1. Front Door", "A2": "A2. Loading Dock", "A3": "A3. Back Alley",
        "A4": "A4. Front Room", "A5": "A5. Barracks", "A6": "A6. Yargin's Office",
        "A7": "A7. Upper Workroom", "A8": "A8. Fishery Floor", "A9": "A9. Kraken's Folly",
        "A10": "A10. Spider Nest", "A11": "A11. Kraken's Hold", "A12": "A12. Underpier",
        "A13": "A13. Gaedren's Playground", "A14": "A14. Gaedren's Den",
    }
    notes=[B.note(snid(),JID,P[c],NOTE_NAMES[c],*NOTE_POS[c]) for c in area_codes]
    MM="icons/svg/mystery-man.svg"
    tok=[]
    def place(actor_id,name,xy,disp=-1,w=1,h=1):
        x,y=(xy[0]//100)*100,(xy[1]//100)*100
        tok.append(B.token(snid(),actor_id,name,x,y,B.token_art(name) or MM,disposition=disp,width=w,height=h))
    # day-shift staging per the area texts (all hidden — GM reveals as the raid
    # unfolds): Yargin in his office (A6), Hookshanks at the loading dock (A2),
    # Giggles overseeing 5 orphans on the fishery floor (A8), 4 orphans at the
    # A7 trough, Bloo asleep under the A4 desk, 1 drain spider in the aft cabin
    # (A10) + 4 in the hold (A11), the shark under the A8 floor-hole.
    place(A["yargin"],"Yargin Balko",ffpx(11,13))
    place(A["hookshanks"],"Hookshanks Gruller",ffpx(14.5,13))
    place(A["giggles"],"Giggles",ffpx(10,10))                # open floor east of the chum vat
    for gx,gy in [(8,4),(6,6),(7,5),(8,6)]:                  # A7 trough crew (on the bow deck)
        place(A["orphan"],"Lamm's Lamb",ffpx(gx,gy),disp=0)
    for gx,gy in [(4,9),(5,11),(4,12),(5,14),(10,11)]:       # A8 floor crew (catwalks/work floor, off the vat)
        place(A["orphan"],"Lamm's Lamb",ffpx(gx,gy),disp=0)
    place(A["drainspider"],"Drain Spider",ffpx(13,4))        # A10 cabin lurker (webbed deck by the stairs down)
    for gx,gy in [(7,5),(8,4),(10,4),(8,6)]:                 # A11 hold infestation (inside the hold)
        place(A["drainspider"],"Drain Spider",lfpx(gx,gy))
    place(A["jigsawshark"],"Jigsaw Shark",lfpx(6,6))
    place(A["gaedren"],"Gaedren Lamm",lfpx(7,16))            # west-side floor by his cluttered tables, across the pool
    _blo=B._cmeta("npc","Bloo"); _gob=B._cmeta("npc","Gobblegut")
    if _blo: place(_blo["id"],"Bloo",ffpx(8.5,16))           # asleep under the A4 desk
    if _gob: place(_gob["id"],"Gobblegut",lfpx(10,15),w=2,h=2)   # centered in the gator pool
    place(A["boardwalk"],"Slippery Boardwalk",ffpx(2,15))
    place(A["rottendeck"],"Rotten Ship Deck",ffpx(8,5))      # the bow deck's rotten planking
    sc = B.scene(SCN,"Old Fishery",_FISH["width"],_FISH["height"],GRID,None,
                 notes,tok,folder=F["s_ch1"],navName="Old Fishery")
    sc["thumb"]=_FISH.get("thumb")     # Racooze's pre-rendered sidebar thumbnail
    for w in _FISH["walls"]:                      # Racooze walls/doors, re-keyed
        w=dict(w); w.pop("levels",None); w["_key"]=f"!scenes.walls!{SCN}.{w['_id']}"
        sc["walls"].append(w)
    for t in _FISH["tiles"]:                      # his composition, untouched art paths
        t=json.loads(json.dumps(t)); t.pop("levels",None)
        t["_key"]=f"!scenes.tiles!{SCN}.{t['_id']}"
        sc["tiles"].append(t)
    # (grading/lighting experiment rolled back 2026-06-11 — scene keeps Racooze's
    # stock look; the active workstream is prepared tokens + per-actor token art)
else:
    print("[scene] racooze_scenes.json absent -> Old Fishery builds as placeholder grid")
    notes=[]
    for i,code in enumerate(area_codes):
        col=i%5; row=i//5
        notes.append(B.note(snid(),JID,P[code],code, 300+col*400, 300+row*400))
    tok=[]
    def place_ph(actor_key,name,code):
        n=next(x for x in notes if x["text"]==code)
        tok.append(B.token(snid(),A[actor_key],name,n["x"],n["y"]+120,TOK(actor_key)))
    place_ph("yargin","Yargin Balko","A6"); place_ph("hookshanks","Hookshanks Gruller","A7")
    place_ph("giggles","Giggles","A8"); place_ph("drainspider","Drain Spider","A10")
    for _ in range(4): place_ph("drainspider","Drain Spider","A11")
    place_ph("jigsawshark","Jigsaw Shark","A12"); place_ph("gaedren","Gaedren Lamm","A13")
    sc = B.scene(SCN,"Old Fishery",2400,1800,GRID,"modules/cotct-pf2e-conversion/assets/maps/01-old-fishery.webp",
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
  +"<p><strong>Blood Veil (disease).</strong> "+chk("type:fortitude|dc:24")+" for ordinary exposure, rising to "+chk("type:fortitude|dc:30")+" for concentrated sources (the cult's brewing vats and raw fluids in Ch.2); on a critical failure the victim <strong>skips the onset</strong> and immediately suffers Stage 1. <strong>Onset</strong> 1 day. <strong>Stage 1</strong> "+B.cond("enfeebled","Enfeebled 1")+" (1 day); <strong>Stage 2</strong> "+B.cond("enfeebled","Enfeebled 2")+" and "+B.cond("drained","Drained 1")+" (1 day); <strong>Stage 3</strong> "+B.cond("enfeebled","Enfeebled 2")+" and "+B.cond("drained","Drained 2")+" (1 day); <strong>Stage 4</strong> "+B.cond("drained","Drained 3")+" and "+B.cond("enfeebled","Enfeebled 3")+". The PF1e Con+Cha damage becomes drained/enfeebled; the suppressant halts progression and steps the stage down rather than curing outright.</p>"
  +"<p><strong>Persistent in-city exposure</strong> (atmosphere, not attrition): while in Plagued-tier Korvosa, a character attempts a flat check each downtime week — "+chk("type:flat|dc:5")+" at a low clock, up to "+chk("type:flat|dc:11")+" at a high clock — on a failure, save against Blood Veil at a reduced DC. Keep it light; make the clock respond to player action.</p>"
  +B.s_conv("<p>Track the clock + city tier on this page across chapters. <strong>Removability hatch:</strong> at any chapter break the GM may rule the suppressant became a true cure (revert to faithful) with zero downstream breakage. Full design: <code>design/persistent_plague.md</code>.</p>"),level=1),
 B.page(nid(),"Source Text, Read-Alouds & Handouts (Policy)",
  B.s_desc("<p>How this conversion handles the adventure's original prose — and why the journals you're reading may differ from another GM's build.</p>")
  +"<p><strong>Injection, not inclusion.</strong> The build scripts never hardcode the adventure's prose (anchors of at most 8 words excepted). At build time, each read-aloud box, NPC speech, briefing, and player handout is pulled <em>verbatim</em> from the GM's own locally supplied AP text (the <code>COTCT_AP_MD</code> file). If that file is absent, every box falls back to an original paraphrase, so the module still works — it just reads in our words instead of Paizo's.</p>"
  +"<p><strong>Player Handouts are explicitly exempt</strong> from the paraphrase rule, exactly like boxed read-aloud text: a handout's entire purpose is to be shown to players as written (Handouts #1-1/#1-2 in Chapter 1, #2-1/#2-2 in Chapter 2, and so on). They are injected from the GM's local source on the same terms as read-aloud boxes and are never shipped beyond the GM's own private build.</p>"
  +B.s_conv("<p><strong>House rules of the build:</strong> every PF1e DC is re-judged to a PF2e @Check (never transliterated); valuables convert at roughly PF1e gp ÷ 10 while named magic items keep their identity as PF2e equivalents; XP story awards become milestone credit (CHG-0007). OCR artifacts in the source (dropped hyphens, two-column interleave) are repaired during injection — report any survivors as bugs.</p>"),level=1)]
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
# community-statblock pets staged on the scene must travel with the adventure
comm_adv=[]
for _cn in ("Bloo","Gobblegut"):
    _cd=B.community_doc("npc",_cn)
    if _cd:
        _cd["folder"]="rBcjiaGq99bkJyYK"; _cd["sort"]=0; _cd["ownership"]={"default":0}
        _cd["_stats"]=dict(B.STATS)
        _sz=((_cd["system"].get("traits",{}).get("size") or {}).get("value")) or "med"
        _cd["prototypeToken"]=B.prototoken(_cd["name"],_sz)
        comm_adv.append(_cd)

adv = B.adventure(ADV,"Curse of the Crimson Throne — Ch.1: Edge of Anarchy (pilot)",
  "modules/cotct-pf2e-conversion/assets/art/cover.webp",
  "<p>Phase-2 pilot: the Old Fishery (the hunt for Gaedren Lamm). Imports the chapter journal, the Old Fishery scene (map-note pins + staged tokens), the converted NPCs/hazards, and the treasure — organized into folders. The Old Fishery scene carries Racooze's walls and our lighting when his free battlemaps module is installed at build time.</p>",
  [strip(f) for f in folders], [strip(intro_journal), strip(cg_journal), strip(journal)], [strip(sc)],
  [strip(a) for a in actors]+[strip(h) for h in hazards]+[strip(x) for x in comm_adv], [strip(i) for i in items]+[strip(b) for b in bgs],
  tables=[strip(harrow_tbl)], macros=[strip(harrow_mac)])
# GUARD: every scene token must reference an actor that the Adventure import
# creates — otherwise Foundry shows "token references an actor which no longer
# exists in this world" when the scene is used.
_adv_actor_ids={a["_id"] for a in adv["actors"]}
_orphan_tokens=[t["name"] for t in sc.get("tokens",[]) if t.get("actorId") not in _adv_actor_ids]
if _orphan_tokens:
    print(f"  [WARN] scene tokens NOT in adventure bundle (will orphan on import): {_orphan_tokens}")
B.write("adventure","cotct-edge-of-anarchy",copy.deepcopy(adv))

print(f"Pilot (Kingmaker-style) built: {len(folders)} folders, {len(actors)} actors, {len(hazards)} hazards, "
      f"{len(items)} items, 1 journal ({len(pages)} pages), 1 scene ({len(notes)} notes / {len(tok)} tokens), 1 adventure.")
