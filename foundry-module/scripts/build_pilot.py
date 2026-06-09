#!/usr/bin/env python3
"""Build the Phase-2 pilot (Old Fishery) in Kingmaker-style Foundry structure.

Produces: per-type folders, actors (with prototype tokens), hazards, items, ONE
fat chapter journal ("1. Edge of Anarchy") with section-block pages + @Check/@UUID
enrichers, a scene placeholder with map-note pins -> pages and staged tokens, and
an Adventure bundle that imports the whole tree in one click.

Run: python3 scripts/build_pilot.py   (deterministic; safe to re-run)
"""
from __future__ import annotations
import copy, json
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

# UUID link helpers (bare world-UUIDs intra-adventure; Compendium for SRD)
def act(k,label): return f"@UUID[Actor.{A[k]}]{{{label}}}"
def haz(k,label): return f"@UUID[Actor.{A[k]}]{{{label}}}"
def itm(k,label): return f"@UUID[Item.{A[k]}]{{{label}}}"
def mc(k,label): return f"@UUID[Compendium.pf2e.pathfinder-monster-core.Actor.{MC[k]}]{{{label}}}"
def pg(pid,label): return f"@UUID[.{pid}]{{{label}}}"          # same-entry page jump
def chk(s): return f"@Check[{s}]"

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
  ["humanoid","human"],["Common","Varisian"],
  [B.strike(nid(),"Fine Dagger",9,"1d4+1","piercing",["agile","finesse","versatile-s"],[("1d6","precision")]),
   B.strike(nid(),"Hand Crossbow",9,"1d6","piercing",["range-increment-60","reload-1"],[("1d6","precision")]),
   B.action(nid(),"Sneak Attack","passive","<p>+1d6 precision damage vs off-guard creatures (already in his Strikes when applicable).</p>",["rogue"]),
   B.action(nid(),"Limping Gait","passive","<p>An old leg wound caps his Speed at 15 ft; he snipes from across the gator pool rather than kiting.</p>"),
   B.action(nid(),"Nimble Dodge","reaction","<p><strong>Trigger</strong> A creature he can see attacks him.</p><hr /><p><strong>Effect</strong> +2 circumstance bonus to AC vs that attack.</p>",["mental"],"defensive"),
   B.action(nid(),"Spur the Beast","1","<p>Gaedren makes a Hand Crossbow Strike against Gobblegut; on a hit the enraged crocodile gains a +2 status bonus to attack/damage and must Strike the nearest creature other than Gaedren next turn. His signature: turn his pet into a weapon, then snipe from cover.</p>",["concentrate"]),
   B.lore(nid(),"Underworld Lore",8)],
  notes="<p><strong>Role:</strong> the AP's first villain and every PC's revenge payoff — but a frail catalyst, not a tank. The threat is the crocodile; Gaedren weaponizes it. <strong>Tactics:</strong> R1 Spur the Beast, then snipe across the pool; Nimble Dodge when focus-fired; flees to the A12 skiffs at &le;8 HP. <strong>If killed and left in A14,</strong> his son Rolth animates the body in the Dead Warrens (D13) — track it.</p>",
  folder=F["a_creatures"], blurb="Decrepit crime lord; first villain of the AP", token_src=TOK("gaedren-lamm"), actor_link=True))

AW("yargin-balko", B.npc(A["yargin"],"Yargin Balko",1,16,20,5,5,7,6,
  {"str":1,"dex":2,"con":1,"int":3,"wis":2,"cha":1},25,
  {"crafting":7,"society":6,"deception":5,"thievery":5,"intimidation":6,"arcana":6},
  ["humanoid","human"],["Common","Gnomish","Varisian"],
  [B.strike(nid(),"Acid Flask",7,"1d6","acid",["range-increment-20","splash","alchemical","bomb"],[("1","persistent-acid")]),
   B.strike(nid(),"Light Crossbow",5,"1d8","piercing",["range-increment-60","reload-1"]),
   B.strike(nid(),"Dagger",5,"1d4+1","piercing",["agile","finesse","versatile-s"]),
   B.action(nid(),"Quick Acid","1","<p>Draw and throw an Acid Flask in one action (carries 3).</p>",["alchemical"]),
   B.lore(nid(),"Alchemy Lore",7)],
  notes="<p><strong>Role:</strong> Gaedren's fence; answers the front door, fights from A6. Opens with thrown Acid Flasks, falls back to crossbow. <strong>Flees down the hidden trapdoor to warn Gaedren if losing.</strong> Carries the brass key (all fishery doors).</p>",
  folder=F["a_creatures"], blurb="Bitter alchemist-fence; Gaedren's right hand", token_src=TOK("yargin-balko")))

AW("hookshanks-gruller", B.npc(A["hookshanks"],"Hookshanks Gruller",1,16,18,4,7,5,5,
  {"str":0,"dex":4,"con":1,"int":1,"wis":1,"cha":2},25,
  {"stealth":9,"deception":8,"thievery":7,"acrobatics":7,"society":4,"intimidation":5},
  ["humanoid","gnome"],["Common","Gnomish"],
  [B.strike(nid(),"Kukri",7,"1d6+1","slashing",["agile","finesse","trip"],[("1d6","precision")]),
   B.strike(nid(),"Dagger",7,"1d4+1","piercing",["agile","finesse","thrown-10","versatile-s"],[("1d6","precision")]),
   B.action(nid(),"Sneak Attack","passive","<p>+1d6 precision vs off-guard.</p>",["rogue"]),
   B.action(nid(),"Disguised as an Orphan","passive","<p>Passes as one of Lamm's Lambs; "+chk("type:perception|dc:17")+" vs his Deception to spot him before he Sneak Attacks.</p>"),
   B.action(nid(),"Surrender & Inform","free","<p>At &lt;half HP he talks; knows the fishery and Gaedren's routine except the den (A14).</p>"),
   B.lore(nid(),"Streetwise Lore",6)],
  notes="<p><strong>Role:</strong> taskmaster over the orphans in A7; hides among them; can surrender and inform.</p>",
  folder=F["a_creatures"], size="sml", blurb="Gnome taskmaster who hides among the orphans", token_src=TOK("hookshanks-gruller")))

AW("giggles", B.npc(A["giggles"],"Giggles",1,16,24,7,5,3,5,
  {"str":3,"dex":1,"con":3,"int":0,"wis":1,"cha":0},25,
  {"athletics":7,"intimidation":5},["humanoid","orc","human"],["Common","Orcish"],
  [B.strike(nid(),"Flail",7,"1d6+3","bludgeoning",["sweep","trip"]),
   B.strike(nid(),"Fist",7,"1d4+3","bludgeoning",["agile","nonlethal","unarmed"]),
   B.strike(nid(),"Composite Longbow",5,"1d6+3","piercing",["range-increment-100","deadly-d10","propulsive"]),
   B.action(nid(),"Bludgeoner","passive","<p>Deals nonlethal with his Flail at no penalty; +1 circumstance to attack on nonlethal Strikes vs foes above half HP.</p>"),
   B.action(nid(),"Orc Ferocity","reaction","<p><strong>Trigger</strong> reduced to 0 HP.</p><hr /><p>Stays at 1 HP, wounded 1. Once per day.</p>"),
   B.lore(nid(),"Brawling Lore",5)],
  notes="<p><strong>Role:</strong> muscle on the main floor (A8); tries to <strong>capture</strong> PCs nonlethally for Gaedren, then fights to the death. Carries 3 minor healing potions.</p>",
  folder=F["a_creatures"], blurb="Half-orc brute; the fishery's muscle", token_src=TOK("giggles")))

AW("drain-spider", B.npc(A["drainspider"],"Drain Spider",-1,15,8,3,6,2,5,
  {"str":-2,"dex":4,"con":1,"int":-5,"wis":1,"cha":-4},25,
  {"stealth":6,"athletics":3},["animal"],[],
  [B.strike(nid(),"Fangs",7,"1d4","piercing",["finesse"],[("1d4","poison")]),
   B.action(nid(),"Drain Spider Venom","passive","<p><strong>Saving Throw</strong> "+chk("type:fortitude|dc:15")+"; <strong>Stage 1</strong> 1d4 poison + enfeebled 1 (1 round). A spider that smells Gaedren's vermin repellent (looted in A13) is sickened and won't approach a coated creature.</p>",["poison"]),
   B.action(nid(),"Lunge","passive","<p>Attacks the first creature to enter its lair, off-guard to the surprised target.</p>")],
  notes="<p>Cat-sized vermin nesting in the wreck (A10 = 1; A11 = 4). Trivially repelled by vermin repellent.</p>",
  folder=F["a_creatures"], senses=[{"type":"darkvision"},{"acuity":"imprecise","type":"tremorsense","range":30}],
  other_speeds=[{"type":"climb","value":25}], size="tiny", blurb="Aggressive venomous spider", token_src=TOK("drain-spider")))

AW("jigsaw-shark", B.npc(A["jigsawshark"],"Jigsaw Shark",1,16,20,7,6,3,7,
  {"str":3,"dex":2,"con":2,"int":-4,"wis":2,"cha":-2},5,
  {"athletics":8},["animal","aquatic"],[],
  [B.strike(nid(),"Jaws",8,"1d8+3","piercing",["deadly-d8"]),
   B.action(nid(),"Aquatic Ambush","1","<p>While hidden in water, Swim up to Speed and Strike; target off-guard.</p>"),
   B.action(nid(),"Reluctant Leaper","passive","<p>Attacks anything that falls in the water, but only leaps onto the underpier (A12) if attacked and damaged first.</p>")],
  notes="<p>Scavenger under the fishery. Avoidable if the PCs stay dry; the hazards feed creatures to it.</p>",
  folder=F["a_creatures"], senses=[{"acuity":"imprecise","type":"scent","range":30}],
  other_speeds=[{"type":"swim","value":35}], blurb="River shark beneath the fishery", token_src=TOK("jigsaw-shark")))

AW("lamms-lamb", B.npc(A["orphan"],"Lamm's Lamb (Orphan)",-1,15,6,2,6,3,5,
  {"str":-2,"dex":3,"con":0,"int":0,"wis":-1,"cha":0},25,
  {"acrobatics":7,"thievery":7,"stealth":6},["humanoid","human"],["Common"],
  [B.strike(nid(),"Pitchfork (improvised)",5,"1d6-1","piercing",["reach","improvised"]),
   B.action(nid(),"Cower","passive","<p>An orphan that takes damage flees to A8, or out of the fishery if the thugs are down. Orphans invaded at night are too frightened to fight.</p>"),
   B.action(nid(),"Rally to the Heroes","passive","<p>A PC can rally an orphan ("+chk("type:diplomacy|dc:15")+"; Intimidation fails) to Aid or reveal info. <strong>Non-combatants — not an XP source for killing.</strong> Rescuing them is the dungeon's heart (a 'Missing Child' background payoff).</p>")],
  notes="<p>Enslaved child pickpockets: 9 by day across A7/A8, 26 asleep in A8 at night. The moral core of the dungeon.</p>",
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
  [B.action(nid(),"Slip","reaction","<p><strong>Trigger</strong> A creature Strides &gt;5 ft or fights on it.</p><hr /><p><strong>Effect</strong> "+chk("type:reflex|dc:15|basic:true")+" or fall prone; on a critical failure, slide off and fall 13 ft into the river (@Damage[1[bludgeoning]]) and the Jigsaw Shark's water (A12).</p>")],
  folder=F["a_hazards"], traits=["environmental"], reset="<p>Persistent terrain.</p>"))

HW("rotten-ship-deck", B.hazard(A["rottendeck"],"Rotten Ship Deck",1,16,
  "<p>"+chk("type:perception|dc:16")+" to spot the unsafe foredeck first.</p>",
  "<p>"+chk("type:crafting|dc:16")+" to shore up a path, or keep to the sound stern.</p>",
  "<p>The derelict Kraken's Folly (A9) has a rotten foredeck; only the stern holds weight.</p>",
  [B.action(nid(),"Collapse","reaction","<p><strong>Trigger</strong> A Medium+ creature moves onto the foredeck toward the bow.</p><hr /><p><strong>Effect</strong> "+chk("type:reflex|dc:16|basic:true")+" or crash to the hold (A11) for @Damage[1d6[bludgeoning]] and land prone among the drain spiders.</p>")],
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
PAGE_KEYS=["overview","scene","features","A1","A2","A3","A4","A5","A6","A7","A8","A9","A10",
           "A11","A12","A13","A14","npcs","treasure","conv"]
P={k:nid() for k in PAGE_KEYS}   # pre-assign so forward relative links resolve
def newpage(key,name,html,level=3):
    return B.page(P[key],name,html,level=level)

pages=[]
# 1. Overview & Run Sheet
pages.append(newpage("overview","Overview & Run Sheet",
  B.s_desc("<p>The ghost-spirit Zellara draws the PCs together with a harrow reading and sends them to kill crime-lord <strong>Gaedren Lamm</strong>, who hides in the <strong>Old Fishery</strong> with his thugs, his pet crocodile <strong>Gobblegut</strong>, and his enslaved orphans. The PCs recover Queen Ileosa's stolen brooch, Gaedren's ledger, and Zellara's haunted harrow deck — and as they leave, the king dies and Korvosa erupts.</p>")
  +B.s_gm("<p><strong>Party:</strong> 4 PCs, level 1 → 2 (milestone on clearing the fishery). <strong>System:</strong> PF2e Remaster (Foundry v14 / pf2e 8.2.0).</p>"
   "<p><strong>Run it like Gotham.</strong> Tell players up front that Gaedren is a <em>connector</em>, not a final boss — this avoids the classic 'Lamm is a Lamb' let-down. Day: 9 orphans toil, thugs patrol, A7 open. Night: doors lock, 26 orphans sleep in A8, "+mc("guarddog","Bloo")+" roams (alarm). The orphans are non-combatants; rescuing them is the point.</p>"
   "<p><strong>First Harrowing (CHG-0010):</strong> run Zellara's reading as foreshadowing (coming unrest; the PCs are fated heroes), then grant each PC a small pool of hero-point-style suit boons via "+itm("harrowdeck","her harrow deck")+".</p>"),level=1))
# 2. Scene Setup
pages.append(newpage("scene","Scene Setup (maps & VTT)",
  B.s_gm("<p><strong>No maps shipped</strong> (copyright). Open the "+f"@UUID[Scene.{SCN}]{{Old Fishery scene}}"+" — its map-note pins already link to each area page below and its tokens reference the converted actors. Drop in a map (Racooze's free CotCT battlemaps, or your own at <code>assets/maps/01-old-fishery.webp</code>), then confirm pin/token positions (currently staged — <strong>NEEDS GM REVIEW</strong>). Drag "+mc("crocodile","Crocodile")+" (rename 'Gobblegut') into A13 and "+mc("guarddog","Guard Dog")+" ('Bloo') into A4/A8 from the pf2e compendium.</p>"),level=2))
# 3. Fishery Features
pages.append(newpage("features","Fishery Features & Layout",
  SR("A. Old Fishery","17")
  +B.s_gm("<p>A two-floor fishery on pilings over the Jeggare River, on a 13-ft embankment ("+chk("type:athletics|dc:15")+" to climb the slick bank). Doors: "+chk("type:thievery|dc:15")+" to pick; the brass key bypasses all. Standing hazards: "+haz("boardwalk","Slippery Boardwalk")+" (A3) and "+haz("rottendeck","Rotten Ship Deck")+" (A9) — both can dump a PC into "+act("jigsawshark","the shark's")+" water (A12).</p>"),level=2))

# Area pages A1-A14
def area(code,name,page_html): pages.append(newpage(code,f"{code}. {name}",page_html))
area("A1","Front Door", SR("A1","18")+B.s_gm("<p>Locked double doors ("+chk("type:thievery|dc:15")+"); a loud pick or a knock brings "+act("yargin","Yargin")+" from A6.</p>"))
area("A2","Loading Dock", SR("A2","18")+B.s_gm("<p>A 15-ft dock with slurry barrels; riverside stairs. A7 doors open by day; the A8 door is always locked ("+chk("type:thievery|dc:15")+").</p>"))
area("A3","Back Alley", SR("A3","18-20")+B.s_gm("<p>The "+haz("boardwalk","Slippery Boardwalk")+" hugs the south wall 13 ft above the river. A Step is safe; moving fast or fighting risks a fall into the shark water. The A6 door is locked.</p>"))
area("A4","Front Room — Bloo (E1)", SR("A4","19")
  +B.s_gm("<p>Under the desk sleeps "+mc("guarddog","Bloo")+", Yargin's cur (use <strong>Guard Dog</strong>; rename the token). He attacks strangers on sight and his barks rouse the fishery.</p>")
  +B.s_encounter('<header class="split"><h3>E1 · Bloo</h3><p>Trivial · 20 XP</p></header>'+f'<aside class="right token"><ul><li>@UUID[Compendium.pf2e.pathfinder-monster-core.Actor.{MC["guarddog"]}]{{Bloo (Guard Dog −1)}}</li></ul></aside>'+"<p>Silence him fast (Stealth/Diplomacy to avoid, or a quick kill) before the barks alert the others.</p>"))
area("A5","Barracks", SR("A5","20")+B.s_gm("<p>The thugs' bunkroom; they distrust each other and keep no valuables here.</p>"))
area("A6","Yargin's Office (E2)", SR("A6","19-21")
  +B.s_gm("<p>"+act("yargin","Yargin Balko")+" works here. A <strong>hidden trapdoor</strong> ("+chk("type:perception|dc:18")+" to spot; barred — "+chk("type:athletics|dc:17")+" to force) drops to A13, a flanking route onto the boss. Yargin holds the brass key.</p>")
  +B.s_encounter('<header class="split"><h3>E2 · Yargin</h3><p>Low · 40 XP</p></header><aside class="right token"><ul><li>'+act("yargin","Yargin Balko (1)")+"</li></ul></aside><p>Opens with thrown Acid Flasks, then light crossbow. <strong>Flees down the trapdoor to warn Gaedren</strong> if losing.</p>"))
area("A7","Upper Workroom — Hookshanks (E3)", SR("A7","20-22")
  +B.s_gm("<p>4 orphans toil under "+act("hookshanks","Hookshanks")+", who hides among them ("+chk("type:perception|dc:17")+" to pick out). Slippery floor ("+chk("type:acrobatics|dc:15")+" if moving fast). Locked cash cabinet ("+chk("type:thievery|dc:15")+").</p>")
  +B.s_encounter('<header class="split"><h3>E3 · Hookshanks + orphans</h3><p>Low · 40 XP</p></header><aside class="right token"><ul><li>'+act("hookshanks","Hookshanks Gruller (1)")+"</li><li>4× "+act("orphan","Lamm's Lamb")+" (non-combatant)</li></ul></aside><p>Rally the orphans ("+chk("type:diplomacy|dc:15")+"); Hookshanks can surrender and inform.</p>"))
area("A8","Fishery Floor — Giggles (E4)", SR("A8","21-22")
  +B.s_gm("<p>Main slurry floor (8-ft vat, catwalks, a hole to the river). "+act("giggles","Giggles")+" oversees 5 orphans by day (26 sleep here at night). Beware feeding PCs through the hole to "+act("jigsawshark","the shark")+".</p>")
  +B.s_encounter('<header class="split"><h3>E4 · Giggles [+Bloo at night]</h3><p>Low · 40–60 XP</p></header><aside class="right token"><ul><li>'+act("giggles","Giggles (1)")+"</li><li>5× "+act("orphan","orphans")+" (non-combatant)</li></ul></aside><p>Giggles tries to <strong>capture</strong> PCs nonlethally, then fights to the death (Orc Ferocity).</p>"))
area("A9","Kraken's Folly", SR("A9","23-24")+B.s_gm("<p>A derelict ship; the "+haz("rottendeck","Rotten Ship Deck")+" foredeck collapses under Medium+ weight (drop to A11). Stairs to the spider nest.</p>"))
area("A10","Spider Nest (E5)", SR("A10","24")
  +B.s_gm("<p>Aft cabin lair of a single "+act("drainspider","drain spider")+" that lunges at the first to enter.</p>")
  +B.s_encounter('<header class="split"><h3>E5 · Drain Spider</h3><p>Trivial · 20 XP</p></header><aside class="right token"><ul><li>'+act("drainspider","Drain Spider (−1)")+"</li></ul></aside><p>Repelled by the vermin repellent looted in A13.</p>"))
area("A11","Kraken's Hold (E6)", SR("A11","24")
  +B.s_gm("<p>Four more "+act("drainspider","drain spiders")+" infest the hold. Hull secret door ("+chk("type:perception|dc:17")+"; +2 if "+chk("type:survival|dc:15")+" tracked Gaedren) leads to A12 and the boss.</p>")
  +B.s_encounter('<header class="split"><h3>E6 · Drain Spider nest</h3><p>Moderate · 80 XP (trivialized by vermin repellent)</p></header><aside class="right token"><ul><li>4× '+act("drainspider","Drain Spider (−1)")+"</li></ul></aside><p>Combine with the Rotten Deck hazard above (A9).</p>"))
area("A12","Underpier (E7)", SR("A12","24-25")
  +B.s_gm("<p>A floating walkway under the fishery; Gaedren's escape skiffs are tied here. The small (2½-ft) door ("+chk("type:thievery|dc:17")+") leads to A13.</p>")
  +B.s_encounter('<header class="split"><h3>E7 · Jigsaw Shark</h3><p>Low · 40 XP · avoidable</p></header><aside class="right token"><ul><li>'+act("jigsawshark","Jigsaw Shark (1)")+"</li></ul></aside><p>Attacks anyone in the water; only leaps onto the walkway if attacked first.</p>"))
area("A13","Gaedren's Playground — BOSS (E8)", SR("A13","24-26")
  +B.s_desc("<p>A chilly chamber over a water pit; two 5-ft walkways cross it. Loot tables line the far side. Something large stirs in the dark water below.</p>")
  +B.s_gm("<p>"+mc("crocodile","Gobblegut")+" (use <strong>Crocodile</strong>) lurks in the pit; "+act("gaedren","Gaedren Lamm")+" sorts loot across it. <strong>Reaching him means crossing the gator's water.</strong> He opens with <em>Spur the Beast</em> (enrage Gobblegut), snipes, Nimble Dodges, and flees to the A12 skiffs at &le;8 HP.</p>")
  +B.s_encounter('<header class="split"><h3>E8 · BOSS — Gaedren + Gobblegut</h3><p>SEVERE · 120 XP @ level 1 (Moderate @ level 2)</p></header><aside class="right token"><ul><li>'+act("gaedren","Gaedren Lamm (2)")+"</li><li>"+mc("crocodile","Gobblegut (Crocodile 2)")+"</li></ul></aside><p><strong>Scaling:</strong> 3 PCs → Weak Crocodile; 5–6 PCs → Elite Crocodile and/or add a Drain Spider from the pool. If Yargin reached Gaedren, start with Gobblegut pre-enraged.</p>")
  +B.s_treasure("<p>On the tables: "+itm("coffer","darkwood coffer + 20 shiver + 7 vermin repellent")+".</p>")
  +B.s_conv("<p><strong>⚠ Track:</strong> leaving Gaedren's body here → Rolth animates it in the Dead Warrens (D13). See "+pg(P["conv"],"Conversion Notes")+".</p>"))
area("A14","Gaedren's Den (treasure & the reveal)", SR("A14","26-28")
  +B.s_gm("<p>Gaedren's filthy quarters. Strongbox (rusty iron key, or "+chk("type:thievery|dc:15")+") holds "+itm("brooch","Queen Ileosa's Brooch")+". A hatbox holds Zellara's severed head ("+chk("type:medicine|dc:14")+": dead for weeks — the reveal) and "+itm("harrowdeck","her harrow deck")+". Atop the strongbox: "+itm("ledger","Gaedren's coded ledger")+".</p>")
  +B.s_treasure("<p>Full parcel on the "+pg(P["treasure"],"Treasure")+" page.</p>"))
# NPCs index
pages.append(newpage("npcs","NPCs & Creatures",
  B.s_gm("<ul><li>"+act("gaedren","Gaedren Lamm")+" (L2) — A13 boss · "+act("yargin","Yargin Balko")+" (L1) — A6 · "+act("hookshanks","Hookshanks Gruller")+" (L1) — A7 · "+act("giggles","Giggles")+" (L1) — A8</li>"
   "<li>"+mc("crocodile","Gobblegut")+" = Crocodile (L2) · "+mc("guarddog","Bloo")+" = Guard Dog (L−1) · "+act("drainspider","Drain Spider")+" (L−1) · "+act("jigsawshark","Jigsaw Shark")+" (L1) · "+act("orphan","Lamm's Lambs")+" (non-combatant)</li>"
   "<li><strong>Zellara</strong> — the harrow-spirit guide, bound to "+itm("harrowdeck","her deck")+" (story NPC, no stat block).</li></ul>"
   "<p>Build rationale: <code>reports/npc_monster_conversion_report.md</code>.</p>"),level=2))
# Treasure
pages.append(newpage("treasure","Treasure",
  B.s_treasure("<p>Rebuilt to PF2e level 1→2 (PF1e gp discarded; CHG-0008). Full table: <code>reports/treasure_report.md</code>.</p>"
   "<ul><li>"+itm("dagger","+1 Dagger (Gaedren's)")+" — boss loot · +1 armor potency (Gaedren's padded) · A14 hoard → 1st-rank scroll + ~50 gp gems.</li>"
   "<li>"+itm("garnet","Garnet")+" (~8 gp) · "+itm("coffer","Coffer + vermin repellent")+" (~12 gp) · 2× Acid Flask + Thunderstone (Yargin) · 3× minor Healing Potion (Giggles) · ~30 gp coin.</li>"
   "<li>"+itm("ledger","Coded ledger")+" → Guard bounty 15 gp (30 w/ cipher key).</li></ul>")
  +B.s_gm("<p><strong>Story items:</strong> "+itm("brooch","Queen's Brooch")+" (launches the queen's audience + reward), "+itm("harrowdeck","Zellara's Harrow Deck")+" (the Harrow subsystem). Don't restore PF1e gp.</p>"),level=2))
# Conversion Notes
pages.append(newpage("conv","Conversion Notes (Changes from Original)",
  B.s_conv("<p>Mirrors <code>conversion_change_log.md</code> (CHG-0101..0108). Story preserved; no approval-gated changes here.</p>"
   "<ul><li><strong>Gaedren rebuilt as a credible Severe</strong> (with Gobblegut as the real threat) — fixes the 'Lamm is a Lamb' anticlimax + PF2e solo math. Added Spur the Beast / Nimble Dodge; kept Limping Gait. ⚠ Confirm Severe @L1 vs run @L2.</li>"
   "<li><strong>Gobblegut/Bloo referenced</strong> as official Crocodile/Guard Dog.</li>"
   "<li><strong>DCs re-derived</strong> to PF2e level-based/simple (locked-door spam collapsed).</li>"
   "<li><strong>Treasure rebuilt</strong> to PF2e level 1→2 (CHG-0008).</li>"
   "<li><strong>Drain Spider Venom</strong>: PF1e Con-drain → PF2e 1-stage poison + enfeebled.</li>"
   "<li><strong>Harrowing</strong> → hero-point-style suit pool (CHG-0010).</li>"
   "<li><strong>Orphans</strong> = explicit non-combatants (Rally/Cower); never an XP-for-kill source.</li>"
   "<li><strong>Forward hooks:</strong> leave Gaedren's body → Rolth zombie (D13); Brooch → queen's audience; deck → recurring Harrowings.</li></ul>"),level=2))

journal = B.journal_entry(JID,"1. Edge of Anarchy",pages,folder=F["j_adventure"])
B.write("journals","01-edge-of-anarchy",copy.deepcopy(journal),embed_pages=True)

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
  [strip(f) for f in folders], [strip(journal)], [strip(sc)],
  [strip(a) for a in actors]+[strip(h) for h in hazards], [strip(i) for i in items])
B.write("adventure","cotct-edge-of-anarchy",copy.deepcopy(adv))

print(f"Pilot (Kingmaker-style) built: {len(folders)} folders, {len(actors)} actors, {len(hazards)} hazards, "
      f"{len(items)} items, 1 journal ({len(pages)} pages), 1 scene ({len(notes)} notes / {len(tok)} tokens), 1 adventure.")
