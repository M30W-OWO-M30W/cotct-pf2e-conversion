#!/usr/bin/env python3
"""Chapter 2 — Seven Days to the Grave.

Own fat journal ("2. Seven Days to the Grave"), appended to the shared packs
(actors/journals) alongside Chapter 1. Imports pf2e_build (B) for every doc
helper + the shared verbatim read-aloud. Nests its folders under the same
stable cross-chapter root folders build_pilot.py defines.

This increment builds the chapter front matter (the conspiracy, advancement,
Gray Maidens, the Blood Veil / Epidemic Clock kickoff) + the recurring Gray
Maiden Foot Soldier. The cure missions + the Hospice/Andaisin dungeon follow.
"""
from __future__ import annotations
import copy
import pf2e_build as B
B.SCOPE = (2695, 5514)   # AP.md line range for this chapter (anchor scoping)

# OLLIEBIRD DC ALIGNMENT: applied 75 rulings, added 4 new checks, skipped 5 (reasons below)
# applied = 74 area-keyed DC rulings from research/olliebird/ch2.txt set verbatim (4 already matched:
#   B4 Diplomacy 23, C1 Crafting 22, F1 Diplomacy 25, G8 Fortitude 24; G8 vat adopted at
#   Hardness 18/HP 72/BT 36 per GM instruction) + 1 chapter-wide ruling: every Blood Veil exposure
#   check aligned to the community disease DC band (18 -> 24 in 5 spots: plague-zombie Taint &
#   Death Burst, Brienna exposure, D1 corpse contact, F2 sick ward).
# added = B3 Perception 21 (subsiding-wall alternative), D2 Perception 19 (puncture wounds),
#   Mission 5 iron fence Athletics 20 to Climb, Mission 5 windows Thievery 24.
# skipped = (1) 'Brienna is in Stage 3 of Blood Veil' — state note, no DC; (2) door/fence/window/
#   cabinet Hardness-HP-BT object stats — DCs-only pass (only the G8 vat numbers were mandated);
#   (3) Hospice Warehouse Doors — community line carries no DC at all; (4) 'Unhallow: Consecrate
#   to Urgathoa' — not a DC (page already covers the unhallow effect); (5) creature/hazard
#   stat-block mappings & pf2.tools template URLs — encounter composition, out of scope.

# OLLIEBIRD STATBLOCK RESYNC: community levels into encounter math, bespoke community-only
# docs wired in, duplicate treasure dropped from npc() calls (the write-time swap keeps it).
# levels = Silt Eel -1->1 (A1) · Yvicca 6->3 (A3; 'Severe-leaning' prose dropped, band is
#   computed) · Vendra 5->6 + Lavender Thug 3->2 (C1, C3) · Cultist of Urgathoa 3->2
#   (G5, G7, G8, G13 incl. alert wave) · Ramoska 13->15 (G11 + both 'CR-14-equivalent'
#   text mentions -> level-15) · Andaisin Daughter 11->8 (G14 climax; 'Extreme-tier' prose
#   softened) · Ausio 1->3 (no encounter or text refs to touch).
# rewired = Skinshear: shared jigsaw-shark actor -> B.cmon (A2 prose+enc, A3 aside) ·
#   Juju Zombie: B.mon zombie-brute -> B.cmon (G14 boss) · Shrieker: plain text -> B.cmon
#   hazard (B2) · Ruan Mirukova: plain text -> B.cmon (G11).
# kept-official (community itself maps these to the same official monster) = wererat,
#   giant-rat (dire rat), rat-swarm (their export is L1 base, not the prose's elite),
#   otyugh, vampire-servitor (vampire spawn rogue), skeleton-guard (human skeleton),
#   zombie-shambler (human zombie), leukodaemon, ghoul/ghast (GM-option color).
# gear-dedup (community item covers the same AP parcel) = Gray Maiden full plate +
#   composite longbow (theirs: insignia full plate, shortbow) · Physician 'Healer's Kit'
#   (Healer's Tools) · Girrigz leather armor (+1 chain shirt) · Lavender Thug studded
#   leather · Jolistina studded leather (leather armor) · Davaulus studded leather
#   (+1 chain shirt) + 'Lift Button-Key' (Reiner Devaulus' Button Key) · Cultist
#   breastplate (robe) · Lady Andaisin breastplate (+1 resilient breastplate) · Rolth
#   dagger (+1 key-bladed dagger) + 'Rolth's Blood-Veil Notes' (Rolth Lamm's Notes).
#   Kept-and-flagged: Yvicca + Ramoska armor (stat-support, no community counterpart),
#   thug steel shield/rapier/hand crossbow + Physician club (AP gear community omitted).

# MISSING-CHECK SWEEP: badged gated player actions whose prose showed no check in the
# compiled journal.
# added = G8 catwalk door up to G11: Thievery 29 to pick (prose says key-only, but Ramoska's
#   key is obtainable in play; DC per the community's temple-wide 'Doors ... Thievery 29 to
#   unlock' ruling, already this file's standing temple-door rule) · B3 + B6 squeeze-hole:
#   Acrobatics 20 for a Medium creature to Squeeze (community silent; AP gates the gap to
#   Small creatures — level-based DC at the mission's party level 5).
# judged-no-check = D2 trap door (announced in the read-aloud, unlocked — open access to the
#   crawl space) · G4 display glass / G8 vats / G13 daemon prisons (object Hardness-HP stats
#   inline; smashing resolves as damage, not a check) · G5 bed manacles+straps (unbuckled or
#   cut freely, no time pressure) · B1 rusty grate (it IS B4's west grate — Hardness/HP and
#   lift Athletics 26 live in the B4 entry the sentence points at) · Mission 5 'estate sits
#   locked' (the same page's Getting-in skill block carries every entry DC) · G12 'locked
#   trunk' treasure line (Thievery 29 / Athletics 28 badged one sentence earlier on the page).

MODID = "cotct-pf2e-conversion"
# ---- shared cross-chapter root folder ids (must match build_pilot.py) ----
ACTOR_ROOT, ITEM_ROOT, ADV_FOLDER = "cotctActorRoot01", "cotctItemRoot001", "cotctAdvFolder01"

# ---- stable literal ids (16 chars) ----
JID2 = "ch2SevenDaysJrn1"          # the fat Ch.2 journal
A2 = {"graymaiden": "grayMaidenFoot01", "ishani": "ishaniDhatri0001",
      "physician": "queensPhysician1", "silteel": "siltEel000000001", "yvicca": "yviccaSeaHag0001",
      "girrigz": "girrigzRipper001", "vendra": "vendraLoaggri001", "lavthug": "lavenderThug0001",
      "jolistina": "jolistinaSusp001", "davaulus": "reinerDavaulus01", "cultist": "urgathoaCultist1",
      "ramoska": "ramoskaArkminos1", "andaisin": "andaisinUrgath01", "andaisin_t": "andaisinDaughtr1",
      "rolth": "ch2RolthLamm0001", "pzombie": "ch2PlagueZombie1",
      "bhrunlida": "ch2Bhrunlida0001", "ausio": "ch2AusioCarowyn1"}
H2 = {"breathdoors": "ch2DeathsBreath1"}
# the plaguebringer's mask item doc is OWNED by build_appendix.py (appendix p.435);
# this chapter only links to it (creating it here too collided on the same slug).
I2 = {"mask": "appPlagueMask001"}
F2 = {"a_ch2": "ch2ActorFolder01", "a_creatures": "ch2CreaturesFld1",
      "a_hazards": "ch2HazardsFld001"}

ids = B._idgen(220002)             # Ch.2 folders/pages/notes (distinct seed)
def nid(): return next(ids)
sids = B._idgen(880002)
def sid(): return next(sids)

# ---- link + section helpers ----
def act(_id, label): return f"@UUID[Compendium.{MODID}.cotct-actors.Actor.{_id}]{{{label}}}"
def haz(_id, label): return f"@UUID[Compendium.{MODID}.cotct-hazards.Actor.{_id}]{{{label}}}"
def itm(_id, label): return f"@UUID[Compendium.{MODID}.cotct-items.Item.{_id}]{{{label}}}"
def chk(s): return f"@Check[{s}]"
def SEC(html): return B.s_secret(html, sid())
def box(anchor, fallback_html, cut=None, tail="", patch=None):
    """Verbatim read-aloud box. `cut` truncates the pulled text at the first
    occurrence of that marker (two-column OCR splice repair); `tail` appends an
    original-paraphrase completion; `patch` is a list of (find, replace) fixes."""
    t = B.verbatim(anchor)
    if t and cut and cut in t:
        t = t[:t.index(cut)].rstrip()
    if t and patch:
        for a, b in patch:
            t = t.replace(a, b)
    return B.s_read(B.parafy(t) + tail) if t else B.s_read(fallback_html)
def boxm(*pairs):
    """One read-aloud box assembled from several (anchor, fallback) paragraphs
    (the source splits these boxes across paragraph blocks)."""
    out = ""
    for anchor, fallback in pairs:
        t = B.verbatim(anchor)
        out += B.parafy(t) if t else fallback
    return B.s_read(out)
ROOTC, CHC = "#5a0b0b", "#8a1a1a"

# =====================================================================
# FOLDERS (nest under the shared roots; written into the relevant packs)
# =====================================================================
folders = [
  B.folder(F2["a_ch2"], "2. Seven Days to the Grave", "Actor", ACTOR_ROOT, 200000, CHC),
  B.folder(F2["a_creatures"], "Creatures", "Actor", F2["a_ch2"], 100000, None, "a"),
  B.folder(F2["a_hazards"], "Hazards", "Actor", F2["a_ch2"], 200000, None, "a"),
]
for f in folders:
    pack = {"Actor": "actors", "Item": "items", "JournalEntry": "journals"}[f["type"]]
    B.write(pack, "_folder_ch2-" + f["name"].lower().replace(" ", "-").replace(".", "") + "-" + f["type"][:3].lower(), copy.deepcopy(f))
# mirror the folder chain into the hazards pack (per-pack folder docs)
for hf in [B.folder(F2["a_ch2"], "2. Seven Days to the Grave", "Actor", ACTOR_ROOT, 200000, CHC),
           B.folder(F2["a_hazards"], "Hazards", "Actor", F2["a_ch2"], 200000, None, "a")]:
    B.write("hazards", "_folder_hz2-" + hf["name"].lower().replace(" ", "-").replace(".", ""), copy.deepcopy(hf))

# =====================================================================
# ACTORS — recurring Gray Maiden Foot Soldier (Ileosa's elite enforcers)
# =====================================================================
actors = []
def AW(slug, doc):
    actors.append(copy.deepcopy(doc)); B.write("actors", slug, doc, embed_items=True)

AW("gray-maiden-foot-soldier", B.npc(A2["graymaiden"], "Gray Maiden Foot Soldier", 3, 21, 50, 11, 7, 8, 7,
  {"str": 4, "dex": 1, "con": 3, "int": 0, "wis": -1, "cha": 2}, 20,
  {"athletics": 9, "intimidation": 9}, ["humanoid", "human"], ["common"],
  [B.strike(nid(), "Longsword", 12, "1d8+6", "slashing", ["versatile-p"]),
   B.strike(nid(), "Composite Longbow", 10, "1d8+4", "piercing", ["deadly-d10", "propulsive", "range-increment-100", "volley-30"]),
   B.action(nid(), "Shield Block", "reaction", "<p><strong>Trigger</strong> The Gray Maiden takes damage while her shield is raised.</p><hr /><p><strong>Effect</strong> She reduces the damage by the shield's Hardness (5); she and the shield then split any remaining damage.</p>", None, "defensive"),
   B.gear("steel-shield", nid()), B.gear("longsword", nid())],
  notes="<p><strong>Role:</strong> rank-and-file of the <strong>Gray Maidens</strong>, Queen Ileosa's new all-women elite loyal only to her — the recurring antagonist force from here through Chapter 6. Sword-and-shield in melee, but excellent shots; in numbers a few hang back with longbows.</p>"
        "<p><strong>Presentation:</strong> early in this chapter present them as a welcome restoration of order (the face of martial law), not yet obvious villains — the brutal truth of their conscription and conditioning surfaces over the chapter. <strong>Morale:</strong> Gray Maidens fight to the death.</p>",
  folder=F2["a_creatures"], blurb="Ileosa's elite enforcer", token_src=None, actor_link=False))

AW("ishani-dhatri", B.npc(A2["ishani"], "Ishani Dhatri", 5, 21, 68, 11, 9, 14, 11,
  {"str": 0, "dex": 0, "con": 2, "int": 1, "wis": 4, "cha": 2}, 25,
  {"religion": 13, "medicine": 13, "diplomacy": 11, "society": 11}, ["humanoid", "human"], ["common", "vudrani"],
  [B.strike(nid(), "Crossbow", 9, "1d8", "piercing", ["range-increment-120", "reload-1"]),
   B.strike(nid(), "Dagger", 7, "1d4", "piercing", ["agile", "finesse", "thrown-10", "versatile-s"]),
   B.action(nid(), "Heal", "1", "<p>Divine healing (DC 20). <strong>1 action</strong> (touch): restore @Damage[2d8[healing]]. <strong>2 actions</strong> (30 ft): @Damage[2d8+10[healing]]. <strong>3 actions</strong> (30-ft emanation): @Damage[2d8[healing]] to all living (and damages undead, basic "+chk("type:fortitude|dc:20")+"). Ishani's Healing Font lets him cast this many times a day.</p>", ["concentrate", "manipulate", "healing", "vitality"]),
   B.action(nid(), "Shield of Faith", "1", "<p>Ishani calls a shimmering ward, gaining a +1 status bonus to AC for 1 minute (included while active).</p>", ["concentrate"], "defensive"),
   B.action(nid(), "Sanctuary", "1", "<p>A creature that tries to attack Ishani must succeed at a "+chk("type:will|dc:20")+" or have its action wasted and be unable to target him for 1 round. Ishani's go-to when cornered.</p>", ["concentrate", "manipulate"], "defensive"),
   B.action(nid(), "Remove Disease", "passive", "<p>Once per day (downtime) Ishani can cast <em>remove disease</em> — the in-fiction lever for curing a Blood Veil victim. He can also <em>diagnose disease</em> to identify it.</p>", category="offensive"),
   B.lore(nid(), "Mercantile Lore", 11),
   B.gear("leather-armor", nid()), B.gear("crossbow", nid()), B.gear("dagger", nid()), B.gear("healing-potion-minor", nid(), 2)],
  notes="<p><strong>Role:</strong> a kind, conflicted Abadaran priest (almost 30, still low-ranking) who skirts his church's pay-for-healing rules to help the poor — a key <strong>ally</strong> in the plague chapters and the PCs' best in-fiction source of <em>remove disease</em>. A pacifist: he supports and heals, never starts a fight.</p>"
        "<p><strong>Tactics &amp; morale:</strong> opens with Shield of Faith, falls back on Sanctuary, and heals/supports allies. Alone, he flees; cornered, he fights to the death. Befriended (a "+chk("type:diplomacy|dc:17")+" gets him to heal Brienna free; a PC cleric of a charitable god may even start him converting to Sarenrae), he stops charging the party — they serve Abadar by saving the city.</p>",
  folder=F2["a_creatures"], blurb="Abadaran healer; plague-chapter ally", token_src=None, actor_link=True))

AW("queens-physician", B.npc(A2["physician"], "Queen's Physician", 2, 18, 30, 6, 9, 6, 8,
  {"str": 2, "dex": 4, "con": 1, "int": 1, "wis": 0, "cha": -1}, 25,
  {"stealth": 8, "deception": 6, "medicine": 6, "religion": 6}, ["humanoid", "human"], ["common"],
  [B.strike(nid(), "Club", 9, "1d6+2", "bludgeoning", ["agile"]),
   B.sneak_attack(nid(), 1, "The physician"),
   B.action(nid(), "Beaked Mask", "passive", "<p>The physician's "+itm(I2["mask"], "plaguebringer's mask")+" hides its evil and Urgathoan faith and filters the air — it gains a +1 item bonus to saves vs. diseases and inhaled threats and is <strong>immune to blood veil</strong>. Lifting the mask to 'prove' a human face does not remove it or end its effect.</p>", category="defensive"),
   B.gear("leather-armor", nid()), B.gear("club", nid())],
  notes="<p><strong>Role:</strong> one of Dr. Davaulus's masked 'Queen's Physicians' — secretly Urgathoa cultists who <em>spread</em> blood veil under cover of treating it. Recurring Ch.2 antagonist.</p>"
        "<p><strong>Tactics:</strong> they fight in eerie silence, coordinating by hand-signal to flank for Sneak Attacks. <strong>Morale:</strong> as zealots, they rarely flee.</p>",
  folder=F2["a_creatures"], blurb="Masked Urgathoan plague-spreader", token_src=None, actor_link=False))

AW("silt-eel", B.npc(A2["silteel"], "Silt Eel", -1, 16, 8, 5, 7, 3, 5,
  {"str": -2, "dex": 4, "con": 2, "int": -4, "wis": 1, "cha": -1}, 5,
  {"acrobatics": 7, "stealth": 7}, ["animal", "aquatic"], [],
  [B.strike(nid(), "Jaws", 9, "1d4", "piercing", ["finesse"], [("1d4", "poison", "persistent")]),
   B.action(nid(), "Silt Eel Venom", "passive", "<p>A creature bitten is exposed to silt-eel venom: "+chk("type:fortitude|dc:16")+", inflicting @Damage[1d4[persistent,poison]] and "+B.cond("clumsy", "Clumsy 1")+" for 1 round on a failure (Clumsy 2 on a critical failure).</p>", category="offensive")],
  notes="<p><strong>Role:</strong> a finger-long ambush biter that buries in the river silt and swarms in numbers (six lurk in the Direption's bow). Fragile — one hit usually kills it — but a swarm's venom adds up.</p>",
  folder=F2["a_creatures"], senses=[{"type": "low-light-vision"}, {"acuity": "imprecise", "type": "scent", "range": 30}],
  other_speeds=[{"type": "swim", "value": 30}], size="tiny", blurb="Venomous ambush eel", token_src=None))

AW("yvicca", B.npc(A2["yvicca"], "Yvicca", 6, 23, 105, 14, 12, 14, 14,
  {"str": 3, "dex": 4, "con": 4, "int": 1, "wis": 4, "cha": 2}, 25,
  {"nature": 16, "intimidation": 12, "stealth": 12, "athletics": 14}, ["aberration", "amphibious"], ["common", "aquatic-sign-language", "aklo"],
  [B.strike(nid(), "Claw", 16, "2d6+5", "slashing", ["agile"]),
   B.action(nid(), "Horrific Appearance", "passive", "<p>A creature that first sees Yvicca's true hideousness must attempt a "+chk("type:will|dc:23")+": on a failure it is "+B.cond("sickened", "Sickened 1")+" and "+B.cond("frightened", "Frightened 1")+" (Sickened 2, Frightened 2 on a critical failure). A creature that succeeds is temporarily immune for 1 minute.</p>", category="offensive"),
   B.action(nid(), "Evil Eye", "1", "<p>Yvicca curses a creature within 30 feet (no save to resist the curse's onset): it takes a −2 status penalty to AC, attacks, and saves while it remains within 30 feet and in line of sight. "+chk("type:will|dc:23")+" at the end of each of its turns ends the curse.</p>", ["concentrate", "curse", "occult"]),
   B.action(nid(), "Tanglevine", "2", "<p>Strangling weeds erupt in a 20-foot burst within 60 feet; each creature there attempts a "+chk("type:reflex|dc:23")+" or is "+B.cond("immobilized", "Immobilized")+" (Escape or "+chk("type:athletics|dc:23")+" to break free). Difficult terrain for 1 minute.</p>", ["concentrate", "manipulate", "primal"]),
   B.action(nid(), "Brackish Bolt", "2", "<p>Yvicca hurls a lash of caustic brine, a spell attack (+15) against one creature within 60 feet for @Damage[3d6[acid]] (double on a critical hit).</p>", ["concentrate", "manipulate", "primal", "acid"]),
   B.action(nid(), "Command Skinshear", "1", "<p>Yvicca directs her jigsaw-shark companion Skinshear to Stride and Strike, or to guard a chokepoint.</p>", ["auditory", "concentrate"]),
   B.lore(nid(), "Disease Lore", 14),
   B.gear("leather-armor", nid())],
  notes="<p><strong>Role:</strong> a sea-hag druid, Lady Andaisin's aquatic ally, ensconced in the Direption's stern as the red-herring's lethal surprise. She lairs in the crew quarters (A3) and sets her shark Skinshear to guard the hold (A2), joining the fight once she has buffed.</p>"
        "<p><strong>Tactics:</strong> opens at range with Horrific Appearance + Evil Eye, snares clusters with Tanglevine, and blasts with Brackish Bolt while Skinshear savages the snared. Underwater, the PCs fight at a disadvantage unless they prepared.</p>",
  folder=F2["a_creatures"], senses=[{"type": "darkvision"}], other_speeds=[{"type": "swim", "value": 30}],
  blurb="Sea-hag druid; the Direption's guardian", token_src=None, actor_link=True))

AW("girrigz-ripperclaws", B.npc(A2["girrigz"], "Girrigz Ripperclaws", 6, 23, 105, 12, 16, 14, 13,
  {"str": 2, "dex": 5, "con": 4, "int": 0, "wis": 2, "cha": -2}, 30,
  {"acrobatics": 16, "athletics": 12, "stealth": 14, "intimidation": 12}, ["humanoid", "human", "beast"], ["common"],
  [B.strike(nid(), "+1 Striking Mithral Rapier", 16, "2d6+6", "piercing", ["deadly-d8", "disarm", "finesse", "magical"], slug="girrigz-rapier"),
   B.strike(nid(), "Jaws", 14, "1d8+6", "piercing", []),
   B.action(nid(), "Curse of the Wererat", "passive", "<p>A creature bitten by Girrigz is exposed to wererat lycanthropy (a curse-disease): "+chk("type:fortitude|dc:23")+", and on a failure begins the affliction that ends with the victim becoming a wererat under the next full moon unless cured (<em>remove disease</em> before the third stage).</p>", category="offensive"),
   B.action(nid(), "Change Shape", "1", "<p>Girrigz shifts between human, hybrid (his combat form), and dire-rat shapes. In hybrid or rat form he gains the Jaws Strike and a 20-foot climb Speed.</p>", ["concentrate", "polymorph", "primal"]),
   B.action(nid(), "Vital Strike", "2", "<p>Girrigz makes a Rapier Strike that deals an extra @Damage[2d6[piercing]] on a hit — his signature lunge.</p>", ["flourish"]),
   B.lore(nid(), "Underworld Lore", 12)],
  notes="<p><strong>Role:</strong> the wererat firebrand of Korvosa's sewers, whipping his kin into a doomed war on the plague-panicked city above — the boss of the Plague Rats mission. He <strong>cannot be reasoned with</strong>, hates all non-wererats, and fights to the death.</p>"
        "<p><strong>Tactics:</strong> warned by fighting in B3 or the otyugh's release, he pre-buffs (his potions — bear's endurance, blur, shield of faith) and strikes from stealth with the rapier, Changing Shape to his hybrid form. <strong>Note:</strong> scattering his warband <em>without</em> killing the other (coerced) wererats earns full XP and saves 400 citizens (Survivor Count).</p>",
  folder=F2["a_creatures"], senses=[{"type": "low-light-vision"}, {"acuity": "imprecise", "type": "scent", "range": 30}],
  other_speeds=[{"type": "climb", "value": 20}], blurb="Wererat revolutionary; sewer warlord", token_src=None, actor_link=True))

AW("vendra-loaggri", B.npc(A2["vendra"], "Vendra Loaggri", 5, 21, 60, 8, 13, 11, 13,
  {"str": 0, "dex": 4, "con": -1, "int": 2, "wis": 1, "cha": 4}, 25,
  {"deception": 15, "diplomacy": 15, "society": 11, "stealth": 12, "thievery": 11, "crafting": 9}, ["humanoid", "human"], ["common", "halfling", "shoanti", "varisian", "vudrani"],
  [B.strike(nid(), "Poisoned Dagger", 12, "1d4", "piercing", ["agile", "finesse", "thrown-10", "versatile-s"]),
   B.sneak_attack(nid(), 3, "Vendra"),
   B.action(nid(), "Giant Wasp Poison", "passive", "<p>Vendra keeps her dagger envenomed: a creature she hits with it is exposed to giant wasp poison ("+chk("type:fortitude|dc:22")+"), inflicting @Damage[1d6[poison]] and "+B.cond("enfeebled", "Enfeebled 1")+" (stage 2 on a critical failure).</p>", category="offensive"),
   B.action(nid(), "Wand of Charm Person", "1", "<p>Vendra Activates her wand: one creature within 30 feet must succeed at a "+chk("type:will|dc:18")+" or treat her as a trusted friend for 10 minutes (it won't fight her, though obviously harmful requests get a new save). Her favored escape from a fight.</p>", ["concentrate", "magical"]),
   B.action(nid(), "Deceptive Patter", "1", "<p>A consummate fast-talker, Vendra Creates a Diversion or Feints with a Deception check (vs. Perception/Will DC), sobbing and flailing 'harmlessly' to set up a Sneak Attack.</p>", ["concentrate", "linguistic"]),
   B.lore(nid(), "Perfumery Lore", 11),
   B.gear("leather-armor", nid()), B.gear("dagger", nid())],
  notes="<p><strong>Role:</strong> a Chelish con-artist perfumer hawking 'Lavender's Luxuriant Liniment' — a fake plague cure that is sugar, cheap scent, and <strong>river water</strong> ("+chk("type:crafting|dc:22")+" to analyze). The mission is to <strong>expose her</strong>, not necessarily to fight; bring proof to the Guard.</p>"
        "<p><strong>Tactics:</strong> plays the harmless, shrieking merchant while angling for a poisoned Sneak Attack; charms foes at range; flees to her apartment (C2). <strong>Morale:</strong> surrenders at ≤10-ish HP and will say anything to escape the city alive. She burns her wand of <em>remove disease</em> keeping herself plague-free.</p>",
  folder=F2["a_creatures"], blurb="Snake-oil perfumer; fake-cure grifter", token_src=None, actor_link=True))

AW("lavender-thug", B.npc(A2["lavthug"], "Lavender Thug", 3, 20, 45, 9, 9, 5, 8,
  {"str": 3, "dex": 2, "con": 3, "int": -1, "wis": 1, "cha": 0}, 25,
  {"athletics": 9, "stealth": 8, "intimidation": 7}, ["humanoid", "human"], ["common"],
  [B.strike(nid(), "Rapier", 11, "1d6+3", "piercing", ["deadly-d8", "disarm", "finesse"]),
   B.strike(nid(), "Hand Crossbow", 10, "1d6", "piercing", ["range-increment-60", "reload-1"]),
   B.sneak_attack(nid(), 1, "The thug"),
   B.gear("steel-shield", nid()), B.gear("rapier", nid()), B.gear("hand-crossbow", nid())],
  notes="<p><strong>Role:</strong> Vendra's purple-cravat'd bodyguards (sap-carrying in the shop, lethal in a real fight). They crossbow foes already in melee, then close with the rapier, keeping themselves between the PCs and Vendra. <strong>Morale:</strong> a thug drops his weapon and flees at low HP and does not return.</p>",
  folder=F2["a_creatures"], blurb="Vendra's rapier-armed bodyguard", token_src=None, actor_link=False))

AW("jolistina-susperio", B.npc(A2["jolistina"], "Jolistina Susperio", 8, 26, 130, 14, 18, 14, 16,
  {"str": 2, "dex": 6, "con": 3, "int": 1, "wis": -1, "cha": 2}, 25,
  {"acrobatics": 18, "stealth": 18, "deception": 14, "thievery": 16, "occultism": 14}, ["humanoid", "elf"], ["common", "elven", "necril"],
  [B.strike(nid(), "Hand Crossbow", 18, "1d6", "piercing", ["range-increment-60", "reload-1"]),
   B.strike(nid(), "Dagger", 16, "1d4+2", "piercing", ["agile", "finesse", "thrown-10", "versatile-s"]),
   B.sneak_attack(nid(), 4, "Jolistina"),
   B.action(nid(), "Screaming Bolt", "1", "<p>Jolistina fires a shrieking bolt (a Hand Crossbow Strike); on a hit the target and each creature within 10 feet must succeed at a "+chk("type:will|dc:25")+" or be "+B.cond("frightened", "Frightened 1")+" (Frightened 2 on a critical failure).</p>", ["auditory", "emotion", "fear", "mental"]),
   B.action(nid(), "Ray of Enfeeblement", "2", "<p>A spell attack (+16) against one creature within 30 feet; on a hit it is "+B.cond("enfeebled", "Enfeebled 2")+" for 1 minute ("+chk("type:fortitude|dc:24")+" reduces to Enfeebled 1).</p>", ["concentrate", "manipulate", "occult", "void"]),
   B.action(nid(), "Command Undead", "1", "<p>Jolistina directs her animated nobles (her wand of <em>animate dead</em> made 21 zombies; 7 are uncontrolled) to Stride, Strike, or screen her — she fights from behind them and flanks for Sneak Attacks.</p>", ["auditory", "concentrate"]),
   B.action(nid(), "Vanish", "1", "<p>Jolistina drinks a potion of invisibility and melts into the manor, resetting to ambush from a new room (her signature cat-and-mouse).</p>", ["manipulate"]),
   B.lore(nid(), "Pesh & Poisons Lore", 14),
   B.gear("hand-crossbow", nid()), B.gear("dagger", nid())],
  notes="<p><strong>Role:</strong> a pesh-addicted, self-destructive forsaken elf and the necromancer <strong>Rolth Lamm's</strong> lover (Gaedren's son, from the Ch.1 Dead Warrens). Sent to murder Ileosa's noble hit-list at Carowyn Manor, she slaughtered the whole party and posed 21 zombies into a 'masquerade of the dead,' then disguised every corpse as a blood-veil death with her wand of <em>sculpt corpse</em>.</p>"
        "<p><strong>Tactics:</strong> a stealth-skirmisher who plays cat-and-mouse — sniping from hiding for bleeding Sneak Attacks, screaming-bolting clusters, then Vanishing room to room. She fights melee only from behind her zombies. Cornered alone, she flees to ambush again. <strong>The 'plague deaths' here are fakes</strong> ("+chk("type:medicine|dc:20")+" or "+chk("type:will|dc:11")+" to tell).</p>",
  folder=F2["a_creatures"], senses=[{"type": "low-light-vision"}], blurb="Forsaken elf killer; Rolth's lover", token_src=None, actor_link=True))

# ---- Part 3 finale: the Hospice (Davaulus) & the Temple of Urgathoa ----
AW("reiner-davaulus", B.npc(A2["davaulus"], "Reiner Davaulus", 9, 27, 145, 15, 19, 17, 17,
  {"str": 0, "dex": 4, "con": 1, "int": 4, "wis": 2, "cha": 4}, 25,
  {"deception": 19, "diplomacy": 19, "medicine": 17, "occultism": 15, "stealth": 19, "society": 17}, ["humanoid", "human"], ["common", "infernal", "varisian"],
  [B.strike(nid(), "+1 Human-Bane Rapier", 19, "2d6+6", "piercing", ["deadly-d8", "disarm", "finesse", "magical"], slug="davaulus-rapier"),
   B.sneak_attack(nid(), 3, "Davaulus"),
   B.action(nid(), "Human's Bane", "passive", "<p>Davaulus's rapier is bane to humans: against a human target it gains a +2 status bonus to attack and deals an extra @Damage[2d6[piercing]].</p>", category="offensive"),
   B.action(nid(), "Inspire Courage", "1", "<p>A subtle Red Mantis battle-hymn: allies within 60 feet gain a +1 status bonus to attack rolls, damage, and saves vs. fear for 1 round.</p>", ["concentrate", "auditory", "occult"]),
   B.action(nid(), "Slip Away", "2", "<p>Davaulus turns invisible (as the spell) and Strides; he uses this to flee to the Temple of Urgathoa the instant a fight turns against him (below ~10% HP).</p>", ["concentrate", "manipulate", "occult"]),
   B.lore(nid(), "Red Mantis Lore", 17),
   B.gear("rapier", nid()),
   B.equipment(nid(), "Flask of Curses (labeled 'Elixir of True Healing')", 5, 0,
     "<p>A trap for looters: this elegant flask bears a hand-lettered label promising a miracle cure, but it is a <em>flask of curses</em> — the drinker must succeed at a "+chk("type:will|dc:22")+" or be afflicted (a −2 status penalty to checks and saves until the curse is removed). Davaulus keeps it where a thief would grab it first.</p>",
     traits=["magical", "cursed"], rarity="rare")],
  notes="<p><strong>Role:</strong> a Red Mantis assassin masquerading as the queen's chief physician — the public face of the plague effort and one of its three masterminds (with Andaisin and Ramoska). A poisoner and manipulator, not a front-line fighter; he'd rather misdirect (the fabricated 'Ghlaunder wererat cabal') than brawl.</p>"
        "<p><strong>Tactics:</strong> opens with a bane-rapier Sneak Attack, supports with Inspire, and <strong>flees to the Temple</strong> via Slip Away when threatened — relocating the incriminating blood-veil notes to G14. Loyal to the Red Mantis, he never surrenders; cornered, he fights to the death.</p>",
  folder=F2["a_creatures"], senses=[{"type": "low-light-vision"}], blurb="Red Mantis assassin; the 'queen's physician'", token_src=None, actor_link=True))

AW("cultist-of-urgathoa", B.npc(A2["cultist"], "Cultist of Urgathoa", 3, 20, 50, 11, 6, 10, 9,
  {"str": 2, "dex": 1, "con": 3, "int": 0, "wis": 4, "cha": 1}, 20,
  {"religion": 11, "athletics": 8, "intimidation": 7}, ["humanoid", "human"], ["common"],
  [B.strike(nid(), "+1 Scythe", 10, "2d4+5", "slashing", ["deadly-d10", "magical", "trip"]),
   B.action(nid(), "Harm", "1", "<p>Divine void energy (DC 18). <strong>1 action</strong> (touch): @Damage[2d8[void]] to a living creature (basic "+chk("type:fortitude|dc:18")+"), or heal an undead ally that much. <strong>3 actions</strong>: a 30-ft void burst.</p>", ["concentrate", "manipulate", "void"]),
   B.action(nid(), "Goad Thrall", "1", "<p>The cultist exhorts an undead ally to Stride and Strike — coordinating the temple's animated dead.</p>", ["auditory", "concentrate"]),
   B.lore(nid(), "Urgathoa Lore", 11),
   B.gear("scythe", nid())],
  notes="<p><strong>Role:</strong> rank-and-file zealot of Urgathoa (goddess of disease, gluttony, undeath) staffing the hidden temple. Scythe-and-void; channels to harm the living and mend the undead. <strong>Morale:</strong> fights to the death.</p>",
  folder=F2["a_creatures"], blurb="Scythe-wielding Urgathoan zealot", token_src=None, actor_link=False))

AW("ramoska-arkminos", B.npc(A2["ramoska"], "Ramoska Arkminos", 13, 33, 230, 21, 21, 25, 24,
  {"str": 3, "dex": 4, "con": 5, "int": 7, "wis": 4, "cha": 2}, 25,
  {"arcana": 26, "crafting": 26, "occultism": 24, "medicine": 24, "society": 22, "stealth": 23, "deception": 20}, ["undead", "humanoid"], ["common", "necril", "varisian", "draconic"],
  [B.strike(nid(), "Claw", 25, "3d8+9", "slashing", ["agile", "finesse"]),
   B.action(nid(), "Drain Life", "2", "<p>Ramoska's touch (or a Claw hit) drains vitality for @Damage[4d6[void]] ("+chk("type:fortitude|dc:33|basic:true")+"); he gains temporary Hit Points equal to half the damage and his fast healing redoubles for 1 round.</p>", ["concentrate", "void"]),
   B.action(nid(), "Contagion", "2", "<p>Ramoska inflicts a refined virulence on one creature within 30 feet: "+chk("type:fortitude|dc:33")+" or contract a wasting disease (Fort each day; "+B.cond("enfeebled", "Enfeebled")+" + "+B.cond("drained", "Drained")+" by stage). His specialty.</p>", ["concentrate", "manipulate", "disease", "occult"]),
   B.action(nid(), "Caustic Bomb", "1", "<p>An alchemical splash bomb (a thrown Strike +25, 30 ft): @Damage[3d6[acid]] plus @Damage[3[persistent,acid]], and @Damage[(3[splash])[acid]] splash.</p>", ["manipulate", "acid"]),
   B.action(nid(), "Dimensional Step", "2", "<p>Ramoska teleports up to 120 feet — his preferred exit. He has <strong>no interest in dying on this hill</strong> and flees rather than risk destruction.</p>", ["concentrate", "manipulate", "occult", "teleportation"]),
   B.action(nid(), "Fast Healing 5", "passive", "<p>Ramoska regains 5 Hit Points at the start of each of his turns (unless damaged by his weaknesses that round).</p>", category="defensive"),
   B.action(nid(), "Nosferatu Resilience", "passive", "<p>Undead; immune to disease, paralysis, poison, and mental effects that require a living mind. <strong>Resistance</strong> to physical 5 (except piercing or wood), cold 10, electricity 10. <strong>Weaknesses:</strong> he cannot cross running water unaided, casts no reflection, and recoils from his own forgotten faith's symbols; destroyed only if dealt with at his coffin.</p>", category="defensive"),
   B.lore(nid(), "Disease Lore", 26),
   B.gear("studded-leather", nid())],
  notes="<p><strong>Role:</strong> an ancient <strong>nosferatu</strong> scholar of disease — the deadliest foe in the chapter, and the one the PCs should almost never fight. Lent to the cult by his master Count Tiriac, he loathes his undeath and only wants to find a cure so he can finally die <em>as a man</em>. He has no love for the cult, the queen, or the Red Mantis.</p>"
        "<p><strong>Negotiation, not battle:</strong> he holds the captive Varisian <strong>Ruan Mirukova</strong> (testing Varisian plague-immunity) and will simply <em>sell</em> him and leave — ~200 gp re-scaled, a magic item, a future favor, or the last <em>death's head coffer</em> from Andaisin's sanctum. If attacked he fights ferociously but flees via Dimensional Step rather than be destroyed. <strong>This is a level-15 encounter far above the party — telegraph the danger.</strong></p>",
  folder=F2["a_creatures"], senses=[{"type": "darkvision"}], blurb="Ancient nosferatu disease-scholar (negotiable)", token_src=None, actor_link=True))

AW("andaisin", B.npc(A2["andaisin"], "Lady Andaisin", 9, 28, 150, 19, 13, 19, 17,
  {"str": 1, "dex": -1, "con": 4, "int": 0, "wis": 5, "cha": 2}, 20,
  {"religion": 19, "intimidation": 15, "deception": 15}, ["humanoid", "human"], ["common", "infernal"],
  [B.strike(nid(), "+2 Vicious Scythe", 19, "2d4+9", "slashing", ["deadly-d10", "magical", "trip"], [("1d6", "void")]),
   B.action(nid(), "Divine Spellcasting", "passive", "<p>Andaisin casts as a 10th-level Urgathoan cleric (DC 27, spell attack +19): see her combat actions below. Pre-buffed each morning with <em>status</em> on her lieutenants and, in battle, <em>divine power / air walk / magic vestment / shield of faith</em>.</p>", category="offensive"),
   B.action(nid(), "Slay Living", "2", "<p>A killing curse of void: one creature within 30 feet takes @Damage[7d6+14[void]] ("+chk("type:fortitude|dc:27|basic:true")+"; a critical failure can drop a frail target outright).</p>", ["concentrate", "manipulate", "void"]),
   B.action(nid(), "Greater Command", "2", "<p>One creature within 30 feet must succeed at a "+chk("type:will|dc:27")+" or be compelled to drop "+B.cond("prone", "Prone")+" and grovel (flee, on a critical failure) for 1 round.</p>", ["concentrate", "auditory", "linguistic", "mental", "occult"]),
   B.action(nid(), "Harm (Font)", "3", "<p>A 30-ft void burst: living creatures take @Damage[6d8[void]] ("+chk("type:fortitude|dc:27|basic:true")+") and her undead allies are healed. She channels several times a day.</p>", ["concentrate", "manipulate", "void"]),
   B.action(nid(), "Air Walk & Mist", "1", "<p>Andaisin walks on air 10+ ft up to cast with impunity, dropping <em>obscuring mist</em> below to foil non-flyers when reduced to fewer than ~30 HP, then heals and returns.</p>", ["concentrate", "manipulate", "occult"]),
   B.lore(nid(), "Urgathoa Lore", 19),
   B.gear("scythe", nid())],
  notes="<p><strong>Role:</strong> high priestess of Urgathoa, fled from Nidal — the Temple's master and a co-architect of blood veil. The Inner Sanctum (G14) boss.</p>"
        "<p><strong>Tactics:</strong> buffs (Divine Power), then air-walks aloft and rains Slay Living / Greater Command / Harm before dropping into scythe range; retreats into mist + heals at low HP. <strong>Morale:</strong> she fights to the death — and then <strong>transforms</strong> into a Daughter of Urgathoa (see her second form).</p>",
  folder=F2["a_creatures"], senses=[{"type": "darkvision"}], other_speeds=[{"type": "fly", "value": 20}], blurb="Urgathoan high priestess; plague architect", token_src=None, actor_link=True))

AW("andaisin-transformed", B.npc(A2["andaisin_t"], "Andaisin, Daughter of Urgathoa", 11, 30, 200, 23, 18, 21, 20,
  {"str": 7, "dex": 3, "con": 6, "int": 0, "wis": 4, "cha": 3}, 30,
  {"athletics": 23, "intimidation": 21, "religion": 19}, ["undead"], ["common", "infernal"],
  [B.strike(nid(), "Great Claw", 24, "2d10+11", "slashing", ["deadly-d10", "reach-10"], [("1d6", "void")]),
   B.strike(nid(), "Claw", 24, "2d8+11", "slashing", ["agile"]),
   B.action(nid(), "Daughter's Plague", "passive", "<p>A creature damaged by Andaisin's claws is exposed to a virulent wasting disease ("+chk("type:fortitude|dc:29")+"): @Damage[2d6[void]] and "+B.cond("drained", "Drained 1")+" on a failure, advancing daily — Urgathoa's gift made flesh.</p>", category="offensive"),
   B.action(nid(), "Devouring Maw", "1", "<p>Against a "+B.cond("grabbed", "Grabbed")+" or "+B.cond("prone", "Prone")+" creature, Andaisin bites for @Damage[3d8+11[piercing]] plus @Damage[2d6[void]]; she regains that much vitality.</p>", ["attack"]),
   B.action(nid(), "Pestilent Aura", "passive", "<p>Living creatures that end their turn within 15 feet of Andaisin take @Damage[2d6[void]] (basic "+chk("type:fortitude|dc:29")+") as disease and decay roll off her in waves.</p>", category="offensive"),
   B.action(nid(), "Undead Resilience", "passive", "<p>Undead; immune to disease, death effects, paralysis, poison, and mental effects requiring a living mind; negative healing (harmed by vitality, healed by void).</p>", category="defensive")],
  notes="<p><strong>Role:</strong> the horror Andaisin becomes the instant her mortal body dies — a Large undead <strong>Daughter of Urgathoa</strong>, Urgathoa's blessing on her most fervent. <strong>This is the true climax of Chapter 2.</strong> She fights to destruction, spreading plague with every claw.</p>"
        "<p><strong>Tactics:</strong> wades in with reach claws + the pestilent aura, grabs and devours the wounded, and never relents. The fight begins fresh when she rises — give the party a beat of dread.</p>",
  folder=F2["a_creatures"], senses=[{"type": "darkvision"}], size="lg", blurb="Andaisin's undead death-form", token_src=None, actor_link=True))

AW("rolth-lamm", B.npc(A2["rolth"], "Rolth Lamm", 8, 26, 120, 14, 16, 18, 16,
  {"str": -1, "dex": 2, "con": 3, "int": 5, "wis": 0, "cha": 1}, 25,
  {"arcana": 19, "crafting": 17, "occultism": 17, "stealth": 16, "thievery": 14, "deception": 15}, ["humanoid", "human"], ["common", "elven", "necril", "shoanti", "undercommon", "varisian"],
  [B.strike(nid(), "+1 Dagger", 16, "1d4+2", "piercing", ["agile", "finesse", "magical", "versatile-s"], slug="rolth-dagger"),
   B.sneak_attack(nid(), 1, "Rolth"),
   B.action(nid(), "Arcane Spellcasting", "passive", "<p>Rolth casts as an 8th-level necromancer (DC 26, spell attack +18). He enters a fight pre-buffed (<em>mage armor, shield, false life</em> — ~15 temporary HP, included).</p>", category="offensive"),
   B.action(nid(), "Void Ray", "2", "<p>A ray of entropy (a spell attack +18 against one creature within 60 feet): @Damage[5d6[void]], and the target is "+B.cond("drained", "Drained 1")+" ("+B.cond("drained", "Drained 2")+" on a critical hit). His PF1e <em>enervation</em>.</p>", ["concentrate", "manipulate", "void"]),
   B.action(nid(), "Hold Person", "2", "<p>One humanoid within 30 feet must succeed at a "+chk("type:will|dc:26")+" or be "+B.cond("paralyzed", "Paralyzed")+" for 1 round ("+B.cond("slowed", "Slowed 1")+" on a success). His favorite set-up — a held victim is his to knife at leisure.</p>", ["concentrate", "incapacitation", "mental"]),
   B.action(nid(), "Lightning Bolt", "2", "<p>A 60-foot line of lightning: @Damage[7d6[electricity]] (basic "+chk("type:reflex|dc:26")+").</p>", ["concentrate", "manipulate", "electricity"]),
   B.action(nid(), "Vampiric Touch", "2", "<p>A draining touch (melee spell attack +18): @Damage[5d6[void]]; Rolth gains temporary Hit Points equal to half the damage dealt.</p>", ["concentrate", "manipulate", "void"]),
   B.action(nid(), "Dimension Door", "2", "<p>Rolth teleports up to 120 feet. Reduced to fewer than ~15 HP, he uses this to <strong>escape</strong> — he is meant to survive as a recurring villain who animates the PCs' dead allies against them.</p>", ["concentrate", "manipulate", "teleportation"]),
   B.lore(nid(), "Anatomy Lore", 17),
   B.equipment(nid(), "Mortician's Tools & Black Onyxes", 1, 21, "<p>Fine mortician's tools and six black onyx gems (<em>animate dead</em> components; ~21 gp re-scaled), plus a scroll of <em>teleport</em> and a wand of <em>magic missile</em>.</p>", traits=[])],
  notes="<p><strong>Role:</strong> Gaedren Lamm's son — the necromancer whose Dead Warrens the PCs cleared in Chapter 1, the 'Key Lock Killer' of Korvosan legend, and Jolistina's beloved. Conscripted by the cult, his work drives the <strong>plague-zombie strain</strong> of blood veil, and he holds one of the three note-sets needed for the cure. He is besotted with Lady Andaisin.</p>"
        "<p><strong>Tactics:</strong> a back-line caster — he lets the cultists and zombies fight while he Holds, drains, and bolts from range, shrilly accusing the PCs of <strong>murdering his father</strong> and promising to animate their corpses. <strong>Morale:</strong> Dimension Door out below ~15 HP; if he escapes he is a <strong>recurring campaign villain</strong> (he resurfaces beside other enemies, and animates any ally the PCs lose).</p>",
  folder=F2["a_creatures"], senses=[{"type": "darkvision"}], blurb="Necromancer; the Key Lock Killer; Gaedren's son", token_src=None, actor_link=True))

AW("blood-veil-plague-zombie", B.npc(A2["pzombie"], "Blood Veil Plague Zombie", 1, 14, 40, 7, 1, 4, 1,
  {"str": 4, "dex": -2, "con": 3, "int": -5, "wis": 0, "cha": -2}, 25,
  {"athletics": 7}, ["undead", "zombie", "mindless"], [],
  [B.strike(nid(), "Fist", 9, "1d6+4", "bludgeoning", []),
   B.action(nid(), "Blood Veil Taint", "passive", "<p>A creature damaged by the zombie's Strikes is exposed to <strong>blood veil</strong>: "+chk("type:fortitude|dc:24")+" or contract the disease (the staged affliction in the Conversion Guide). The cult's experimental strain rides in its fluids.</p>", category="offensive"),
   B.action(nid(), "Death Burst", "passive", "<p>When the zombie is destroyed, it ruptures in a spray of contagious fluids: each adjacent creature is exposed to blood veil ("+chk("type:fortitude|dc:24")+").</p>", category="offensive"),
   B.action(nid(), "Always Slowed", "passive", "<p>A zombie is permanently "+B.cond("slowed", "Slowed 1")+" and can't use reactions. Mindless; immune to disease, death effects, mental, paralysis, poison, unconscious.</p>", category="defensive")],
  notes="<p><strong>Role:</strong> the cult's prize — a victim of Rolth's experimental blood-veil strain who rose within two days of death. Three are strapped to the G5 operating beds for observation. The strain <strong>spreads disease on its attacks and in death</strong>, but does not (yet) animate those it kills — the cult is still perfecting that.</p>",
  folder=F2["a_creatures"], senses=[{"type": "darkvision"}], blurb="Blood-veil-strain plague zombie", token_src=None))

AW("bhrunlida-torthus", B.npc(A2["bhrunlida"], "Bhrunlida Torthus", 3, 19, 48, 9, 7, 8, 7,
  {"str": 4, "dex": 1, "con": 2, "int": 0, "wis": 1, "cha": 1}, 25,
  {"athletics": 10, "intimidation": 9, "deception": 8, "medicine": 5}, ["humanoid", "human"], ["common"],
  [B.strike(nid(), "Sap", 11, "1d6+4", "bludgeoning", ["agile", "nonlethal"]),
   B.strike(nid(), "Fist", 11, "1d4+4", "bludgeoning", ["agile", "nonlethal", "unarmed"]),
   B.gear("sap", nid()), B.gear("padded-armor", nid())],
  notes="<p><strong>Role:</strong> the hospice's burly, bull-headed 'nurse' — a hired charlatan gatekeeper, <strong>not</strong> a cultist. She wears three scarves over her face and heavy gloves, touches no one, and knows nothing of the temple below. Her job is the waiting list, and she is adamant about it.</p>"
        "<p><strong>Handling her:</strong> "+chk("type:diplomacy|dc:25")+" or "+chk("type:intimidation|dc:21")+" gets her to fetch an audience with Dr. Davaulus (in F6). Forcing past her instead brings her swinging — impatient and spoiling for an excuse — while her bellows alert F2. <strong>Morale:</strong> under 15 HP she flees or drops to her knees begging; all she can give up is the F2 headcount.</p>",
  folder=F2["a_creatures"], blurb="Hospice gatekeeper; hired charlatan, no cultist", token_src=None))

AW("ausio-carowyn", B.npc(A2["ausio"], "Ausio Carowyn", 1, 13, 18, 5, 3, 7, 4,
  {"str": 1, "dex": -1, "con": 1, "int": 0, "wis": -1, "cha": 2}, 25,
  {"society": 7, "diplomacy": 8, "stealth": 6, "deception": 4}, ["humanoid", "human"], ["common"],
  [B.strike(nid(), "Dull Paint Knife", 5, "1d4+1", "slashing", ["agile"]),
   B.lore(nid(), "Painting Lore", 7), B.lore(nid(), "Nobility Lore", 7)],
  notes="<p><strong>Role:</strong> co-host of the doomed masquerade and the manor's only survivor — a self-described 'realistic' coward who fled at the first crossbow bolt and has hidden for days in his locked wine-cellar studio, living on a water cask and caught rats. He brandishes his paint knife at rescuers, shaking.</p>"
        "<p><strong>Care:</strong> he asks after his wife Olauren; learning she is <em>undead</em> (E2b) breaks his already traumatized mind — be gentle with how the PCs report it. He last saw Ruan in the second-floor gallery. <strong>Morale:</strong> flees any fight; fights only when cornered with no mercy possible.</p>",
  folder=F2["a_creatures"], blurb="Carowyn Manor's surviving host", token_src=None))

# =====================================================================
# HAZARDS — the temple's warded entry
# =====================================================================
hazards = []
def HW(slug, doc):
    hazards.append(copy.deepcopy(doc)); B.write("hazards", slug, doc, embed_items=True)

HW("deaths-breath-doors", B.hazard(H2["breathdoors"], "Death's Breath Doors (G1)", 8, 16,
  "Trained — the painted scythe-skeletons' arms are subtly raised off the plaster.",
  chk("type:thievery|dc:28")+" (expert) to scribe out the wards on a door without touching it, or <em>dispel magic</em> (4th rank, counteract DC 26) against each warded door.",
  "<p>Potent Urgathoan wards seal the north door and the eastern double doors of the temple's entry hall (G1). The skeletons painted around them animate to reap any non-Urgathoan who touches either door, and their painted mouths vent ungol-dust gas into the room.</p>"
  "<p><strong>Linked alarm:</strong> triggering the doors also sets off an <em>alarm</em> in G8, alerting every creature in G8–G13 (see The Temple Under Alert).</p>"
  "<p><strong>Bypass:</strong> if a door is bathed in at least 10 points of vitality/positive energy (a channeled 3-action <em>heal</em>, for example) without anyone touching it, the ward is neutralized for 1 minute before it re-arms.</p>",
  [B.action(nid(), "Reaping Scythes", "reaction",
    "<p><strong>Trigger</strong> A creature that is not a worshiper of Urgathoa touches the north door or the eastern double doors.</p><hr />"
    "<p><strong>Effect</strong> The painted skeletons strike out of the mural: scythe +20 vs. each creature within 5 feet of any of the warded doors, @Damage[2d10+9[slashing]] (deadly — a critical hit also leaves the target "+B.cond("drained", "Drained 1")+"). The skulls then exhale <strong>ungol dust</strong> through the whole of G1: each breathing creature there attempts a "+chk("type:fortitude|dc:26")+", taking @Damage[2d6[poison]] and becoming "+B.cond("drained", "Drained 1")+" and "+B.cond("sickened", "Sickened 1")+" on a failure (Drained 2 on a critical failure). The gas disperses after 1 round.</p>")],
  folder=F2["a_hazards"], ac=27, hardness=14, hp=56, fort=15, ref=12,
  traits=["magical", "trap", "poison"], reset="<p>The wards re-arm automatically after 1 minute.</p>", complex_=False))

# (The Plaguebringer's Mask item itself lives in the appendix pack — every
# Queen's Physician wears one, with two spares in G3; we link via itm().)

# =====================================================================
# JOURNAL — "2. Seven Days to the Grave"
# =====================================================================
SR = lambda area, p: f'<p class="source"><em>Source: CotCT (2016 HC), Ch.2, {area} — p.{p}.</em></p>'
def page(_id, name, html, level=2): return B.page(_id, name, html, level=level)
pages = []
def PG(name, html, level=2): pages.append(B.page(nid(), name, html, level=level))
def area2(code, name, html): PG(f"{code}. {name}", html, level=3)
def encx(levels, pl):
    e = B.encounter(levels, party_level=pl); return f"{e['band']} · {e['xp']} XP @ L{pl}"

pages.append(page(nid(), "Chapter Background", SR("Chapter Background", 70)
  + B.s_milestone("<p><strong>Chapter 2 — Seven Days to the Grave.</strong> Korvosa quiets after the riots — and then Queen Ileosa's true horror begins: a manufactured plague, <strong>Blood Veil</strong>, loosed to cull the citizens she despises. The PCs (now ~L4) race to find a cure as the city dies around them.</p>")
  + SEC("<p><strong>The conspiracy (GM only).</strong> Ileosa always meant her husband's murder to be only the start. Through the Red Mantis assassin <strong>Kayltanya</strong> she obtained <em>Vorel's phage</em>; the Mantis connected her to the 'gentleman's killer' Dr. <strong>Reiner Davaulus</strong>, who with the Urgathoan zealot <strong>Lady Andaisin</strong> and the vampire-scholar <strong>Ramoska Arkminos</strong> weaponized the phage into the fast, dramatic, terror-spreading <strong>blood veil</strong>.</p>")
  + SEC("<p><strong>The delivery.</strong> A fortune in Korvosan silver was tainted with blood veil using a <em>death's head coffer</em> and scattered through the poor quarters and the Bank of Abadar — striking the very priests best placed to fight it. As cover, the conspirators sank the plague-ship <em>Direption</em> in the Jeggare as a <strong>red herring</strong>: investigators who chase the ship waste days while the tainted coin spreads. Letting blood veil run its course cripples the city's will to resist Ileosa's deeper pacts.</p>")
  + B.s_conv("<p>This is the payoff of the <strong>Blood Veil</strong> setup from Chapter 1. Run the persistent-plague overlay from here (Conversion Guide journal → <em>Blood Veil &amp; the Epidemic Clock</em>): start the Epidemic Clock now, seeded by how the city fared in 'Edge of Anarchy.'</p>")))

pages.append(page(nid(), "Advancement & Running the Chapter", SR("Advancement Track / Part 1: Infection", 70)
  + "<p><strong>Advancement.</strong> The PCs begin well into 4th level → <strong>5th</strong> after their first plague mission → <strong>6th</strong> before Carowyn Manor / Racker's Alley → <strong>7th</strong> before the Temple of Urgathoa beneath the hospice → just <strong>8th</strong> by the chapter's end.</p>"
  + "<p><strong>The seven days.</strong> Blood veil takes ~7 days to kill, so the early deaths are isolated among the poor and go unnoticed for days. Keep the PCs busy first (the most time-consuming early task is smuggling Trinia Sabor out of the city), and give them time to resupply and form attachments — the coming tragedies should land personally.</p>"
  + B.s_skill("<p><strong>The Second Harrowing.</strong> Zellara's deck performs its second reading at the chapter's start, generating this chapter's Harrow Points (Conversion Guide → <em>The Harrowing</em>). This chapter is tied to the suit of <strong>shields</strong> and to <strong>Constitution</strong> — read the cards grim: mass graves, ashen-faced women (the Gray Maidens), carrion birds (the Queen's Physicians).</p>")))

pages.append(page(nid(), "NPC Developments", SR("NPC Developments", 71)
  + "<p>Threads from Chapter 1 continue even where the NPCs have no direct role here:</p>"
  + "<ul>"
    "<li><strong>Amin Jalento</strong> barricades himself in his Old Korvosa home, survives the plague, and resurfaces in Chapter 3.</li>"
    "<li><strong>Devargo Barvasi</strong> locks down Eel's End to ride out the quarantine — but unless the PCs intervened, his ettercap "+act("chittersnap00001", "Chittersnap")+", starving, turns on and kills him (his silk-wrapped body found in the hold). If Chittersnap died in Chapter 1, Devargo survives and Eel's End can be a safe haven.</li>"
    "<li><strong>Neolandus Kalepopolis</strong>, the missing seneschal hiding in Old Korvosa, is captured by the Arkonas as this chapter opens — the hook into Chapter 3.</li>"
  "</ul>"))

pages.append(page(nid(), "Cressida's Concern", SR("Cressida's Concern", 72)
  + "<p>Within hours of Trinia's botched execution, Field Marshal <strong>Cressida Kroft</strong> seeks out the PCs, worried. Queen Ileosa is restructuring Korvosa's military; Cressida fears for her own position and warns the PCs that her ability to fund their work — and to shield them — is shrinking.</p>"
  + B.s_conv("<p><strong>Mechanically:</strong> the PCs should no longer consider themselves official Korvosan Guard agents. Cressida still aids them where she can and asks where to reach them — establishing her as their fraying but loyal patron as the city tilts toward martial law.</p>")))

pages.append(page(nid(), "Rise of the Gray Maidens", SR("Rise of the Gray Maidens", 73)
  + "<p>Sabina Merrin first appeared in gleaming red-and-crimson full plate at Trinia's near-execution. She now commands the <strong>Gray Maidens</strong> — an all-women elite loyal only to Ileosa, handed the Longacre Building (arbiter Zenobia Zenderholm welcomes them; the bound efreeti Yzahnum and the bloatmage seneschal Togomor speed their arming) as their headquarters.</p>"
  + SEC("<p><strong>The truth.</strong> Recruits are chosen for beauty and strength; those who fail are disfigured and imprisoned in the dungeons below. Those who pass endure a breaking, scarring initiation. Present them at first as saviors of order — the personification of martial law — and let their brutal nature surface across the chapter. Once they appear, Ileosa retreats into the sealed Castle until Chapter 3.</p>")
  + "<p>Use "+act(A2["graymaiden"], "Gray Maiden Foot Soldier")+" for rank-and-file Gray Maidens in this and later chapters.</p>"))

# --- Part 1: Infection — early events ---
GRAU, TRINIA = "grauSoldado00001", "triniaSabor00001"   # Ch.1 actor ids
PG("A Damsel in Distress", SR("A Damsel in Distress", 76)
  + "<p>Vencarlo Orisini (secretly Blackjack, who rescued Trinia from the gallows) sends the PCs a cryptic note inviting them to his Old Korvosa academy at 16 Hillcrest Street.</p>"
  + box("My friends, I hope this note finds you in good health",
        "<p>My friends, I hope this note finds you in good health in these dangerous times. In light of the recent unrest, I could provide some tips on self-defense, offered gratis, at Orisini Academy, 16 Hillcrest Street. I eagerly await your arrival. — Vencarlo Orisini</p>")
  + "<p>Inside, he reveals "+act(TRINIA, "Trinia Sabor")+" in disguise ('Sorry about the trouble I gave you in the Shingles,' she offers, smiling) and makes his pitch standing:</p>"
  + boxm(("'You were all at the queen's debacle, so I don't doubt you recognize",
          "<p>Vencarlo explains that Blackjack left Trinia in his care the night of the botched execution; he trusts the hero's judgment that she is innocent, and trusts a hero of the city over 'the tantrums of some bloody-minded child playing at queen.'</p>"),
         ("'The matter is simple: Korvosa is no longer safe for Miss Sabor",
          "<p>He has arranged for respected ranchers in Harse to take her in; the problem is the first leg. The bounty has mercenaries, soldiers, and Gray Maidens searching tirelessly — they've knocked at his door three times already — so he turns to the PCs: 'Care to escort a lady home?'</p>"))
  + "<p>He asks the PCs to smuggle her to safety — to a wayside inn called <strong>Trots</strong> (12 miles north), where Jasan Adriel takes her on to a ranch in Harse. He funds the trip (a horse, supplies, 20 gp for the inn) and, if pressed, offers <strong>500 gp</strong>. He won't come himself — too well known, too outspoken against the crown — and plans to vanish into Old Korvosa for a time: <em>don't look for him; he'll call when the time is right</em>.</p>"
  + B.s_skill("<p>A subtle egress is best — a low-key walk out the gates among the afternoon merchants. Crimson-tunic'd guards, Hellknights, mercenaries, and the odd Gray Maiden eye the party, but pass unless the PCs do something suspicious (showy magic, a fight). Optional hinterland encounters en route let Trinia (a bard) fight beside them toward 5th level.</p>")
  + SEC("<p><strong>GM:</strong> Ileosa has set a <strong>5,000 gp bounty</strong> on Trinia. Trinia strongly suspects Vencarlo is Blackjack but keeps it to herself; she warms to the PCs and may become a friend (she returns in Chapter 4).</p>")
  + B.s_treasure("<p><strong>Rewards:</strong> deliver Trinia to Trots → <strong>2,400 XP</strong>. Befriended, she gifts the party her masterwork <strong>mithral dagger</strong> and her <strong>wand of <em>daze monster</em></strong> ('I won't need them in Harse — you might').</p>"))

PG("Yellow Lights", SR("Yellow Lights", 79)
  + "<p>One night early in the chapter (ideally while the PCs are escorting Trinia), the queen's <strong>red herring</strong> sails in: the <em>Direption</em>, a black-sailed Urgathoan ship, slips up the Jeggare just before midnight hung with <strong>yellow lanterns</strong> at the figurehead. The Wall of Eodred's trebuchets fire again and again, waking all of North Point; across the river, Trail's End watches the sleek brig sink into the dark water. Come morning the Crimson Throne says nothing, and ghost-ship gossip drowns the facts.</p>"
  + B.s_skill("<p><strong>Asking around</strong> (Diplomacy to Gather Information) turns up rumors by result:</p>"
    "<table><thead><tr><th>Check</th><th>Rumor</th></tr></thead><tbody>"
    "<tr><td>"+chk("type:diplomacy|dc:10")+"</td><td>The Guard destroyed a ship of Riddleport pirates sneaking in by night. (<em>False.</em>)</td></tr>"
    "<tr><td>"+chk("type:diplomacy|dc:15")+"</td><td>A sinister ship refused inspection and made no answer near North Bridge, so the watch fired on it. (<em>True.</em>)</td></tr>"
    "<tr><td>"+chk("type:diplomacy|dc:20")+"</td><td>No guard who hailed the ship got any response — some say nobody was aboard at all. (<em>Mostly true.</em>)</td></tr>"
    "</tbody></table>"
    "<p>A "+chk("type:society|dc:21")+" (or Sailing Lore) identifies a single yellow bow-light as the Inner Sea signal for a ship <strong>under quarantine</strong>.</p>")
  + SEC("<p><strong>GM:</strong> downplay the wreck for now — it should feel like a handled danger, background flavor. As the plague spreads, rumors that the mystery ship was its source circulate on their own, and the wreck becomes Mission 1. If the PCs insist on diving it immediately, run the wreck <em>without</em> Yvicca (the cult hasn't moved her in yet).</p>"))

PG("The First Symptoms & A Second Favor", SR("The First Symptoms / A Second Favor", 80)
  + "<p>Days before the <em>Direption</em> sank, young <strong>Brienna 'Breeze' Soldado</strong> of Trail's End found a bulging pouch of 50 silver coins in an alley — the biggest fortune of her life — thanked Desna, and spent it all in a day. The coins were tainted by the cult's <em>death's head coffer</em>. By nightfall she was failing; after a sleepless night her mother Tayce sent for an Abadaran cleric and for her late husband's brother, <strong>Grau</strong>.</p>"
  + "<p>"+act(GRAU, "Grau Soldado")+" — shaved, sober, and back with the Guard, but visibly distressed — tracks the PCs down and pulls them somewhere private:</p>"
  + box("'My niece is sick. I don't know what she has",
        "<p>His niece has broken out in red pocks and can't keep food down; her mother can't afford the Bank of Abadar's prices. He saw how the PCs handled the riots — surely they can't sit by while a child suffers?</p>")
  + "<p>He can offer only <strong>100 gp</strong> (50 short of a <em>remove disease</em> casting), and resorts to guilt if refused. At the squat Soldado home the boys play quietly downstairs while ragged coughing fills the loft; the Abadaran acolyte "+act(A2["ishani"], "Ishani Dhatri")+" brews cinnamon-and-anise herbs in the kitchen he can't quite make work — he doesn't recognize Brienna's combination of symptoms, and fears a <strong>new disease</strong>. ("+chk("type:perception|dc:21")+" overhears Grau upstairs scolding Tayce over the healer's bill.)</p>"
  + box("The creaky steps open up into a bedroom loft",
        "<p>Upstairs, a small girl lies dwarfed by quilts and pillows, angry red blotches across her face and arms; a violent fit of coughing wracks her whole frame and leaves her breathing no easier.</p>")
  + B.s_skill("<p><strong>Saving Brienna:</strong> she has <strong>Blood Veil</strong> ("+B.cond("drained", "Drained")+" from Con loss) and dies within days untreated. <em>Remove disease</em> cures it; <em>lesser restoration</em> staves off the drain. "+act(A2["ishani"], "Ishani")+" — out of spells today — suggests buying a <em>remove disease</em> potion from his temple, or for <strong>150 gp</strong> he returns to cast it next morning. "+chk("type:perception|dc:21")+" reads how ashamed he is to ask; "+chk("type:diplomacy|dc:17")+" persuades him to cast it <strong>free</strong> (he spends the rest of the day praying Abadar's forgiveness).</p>")
  + SEC("<p><strong>Exposure.</strong> Treating Brienna exposes the PCs and Ishani to Blood Veil — each attempts "+chk("type:fortitude|dc:24")+" or contracts it (the staged disease in the Conversion Guide). This is the plague's <strong>first on-screen case</strong>: <strong>start the Epidemic Clock now</strong> (Conversion Guide → <em>Blood Veil &amp; the Epidemic Clock</em>).</p>")
  + SEC("<p><strong>The tainted-coins clue.</strong> Cured, Brienna asks if lunch is ready — and goes evasive if pressed about how she got sick. She secretly fears Desna punished her for not sharing the coins; "+chk("type:diplomacy|dc:28")+" (or <em>detect thoughts</em>) coaxes the fear out, and the harder the PCs push, the more protective Tayce gets. The PCs aren't <em>meant</em> to get the coin lead this early — and the taint has already worn off the scattered silver, so scouring the city for coins now is a time-eating goose chase. Don't let it derail them; do let it pay off as foreshadowing when the death's head coffers surface (G14).</p>")
  + B.s_treasure("<p><strong>Story award:</strong> cure Brienna → <strong>1,600 XP</strong>. Tayce cooks the PCs a feast and her door is always open; "+act(A2["ishani"], "Ishani")+" — impressed — asks if he may call on them for charitable work and can be reached at the Grand Vault of Abadar; befriended, he heals them free thereafter.</p>"))

PG("Signs of the Plague", SR("Signs of the Plague (sidebar)", 82)
  + "<p>From here to the chapter's end, Korvosa sinks under the cloak of pestilence. If the PCs need more ways to fight (or witness) the spread, drop in these two sketched events — as color, or expanded into full side-missions:</p>"
  + "<ul><li><strong>Burn Up the Dead.</strong> The city burns its dead in mass graves in the Gray District; plumes of rancid black smoke become a fixture of the southern skyline. Then one mass grave opens into a <strong>ghoul warren</strong>, loosing angry "+B.mon("ghoul", "ghouls")+" and "+B.mon("ghast", "ghasts")+" into the graveyard district — at your option their bites carry <strong>blood veil</strong> instead of ghoul fever.</li>"
  "<li><strong>The Merciless Way Massacre.</strong> "+act(A2["graymaiden"], "Gray Maidens")+" enforcing a block-scale quarantine square off against a terrified mob that won't comply. If nobody talks the crowd down, the standoff becomes a riot and the Maidens cut down nearly <strong>100 citizens</strong>. Diplomacy beats steel here — give the PCs the chance to defuse it (and feed the result into the Survivor Count).</li></ul>"
  + B.s_conv("<p><strong>Part 2: Outbreak.</strong> If the PCs do nothing, roughly <strong>5,000 Korvosans</strong> die before blood veil burns out. From here, most encounters end with a <em>Survivor Count</em> — track lives saved and lost; the running total drives the Epidemic Clock overlay and the chapter-end rewards (→ <em>Final Survivor Count</em>).</p>"))

PG("The Unwashed Masses & the Missing Arbiter", SR("The Unwashed Masses / The Missing Arbiter", 82)
  + "<p>Ishani leads the PCs to the <strong>Grand Vault of Abadar</strong> (North Point), seat of Archbanker Darb Tuttle and the city's most powerful faith — and, by Ileosa's design, the institution best placed to fight the plague and so the one her tainted silver strikes first: several acolytes, guards, and vaultkeepers have already sickened, the clergy's healing magic sold out to a few wealthy worshipers within hours (fewer than two dozen citizens cured in all).</p>"
  + boxm(("Towering over the surrounding buildings, the Grand Vault of Abadar",
          "<p>The Grand Vault's gray-veined white marble towers radiant over its neighbors — unmistakably the house of a god.</p>"),
         ("Yet for a deity of law, the steep stairs and ramps",
          "<p>Dozens of citizens — mostly working class, a few merchants' silks among them — throng the temple's great bronze doors, scarcely held back by gold-armored Abadaran clerics turning nearly all comers away. The reason shows on one desperate believer's face: violent red sores mottling his skin.</p>"))
  + B.s_skill("<p>To reach the doors the PCs must shove through the desperate crowd — "+chk("type:athletics|dc:15")+" each. Any obvious healer is mobbed for aid, and actually healing (or any show of divine power) in the mob's sight nearly sets off a riot; the watching Korvosan Guard forgives thrown punches but <strong>arrests</strong> weapon- or spell-violence, even in defense. Ishani's name (or his company) gets the PCs past the door guards.</p>")
  + B.s_treasure("<p><strong>Story award:</strong> navigate the crowd without harming anyone → <strong>1,600 XP</strong>.</p>")
  + SEC("<p><strong>The Missing Arbiter (GM only — a Chapter 4 hook).</strong> The church frets over its most prominent missing worshiper: senior arbiter <strong>Zenobia Zenderholm</strong>, who handed the Longacre Building to the Gray Maidens and vanished. She soon resurfaces proclaiming allegiance to Queen Ileosa, symbol of Abadar gone, all church contact rebuffed — Archbanker Tuttle writes her off as a 'doubting soul lost to her fears.' <strong>The truth:</strong> Zenobia died of blood veil among its earliest victims; her dying prayers went to Urgathoa, who raised her as a <strong>penanggalen</strong>. She now masquerades as a living turncoat. The PCs learn her true fate in Chapter 4 ('A History of Ashes', Part 3) — plant the wrongness now, resolve nothing.</p>")
  + "<p><strong>The Healer's Hands.</strong> Inside the besieged, fear-silent hall, Ishani draws the PCs into a western meeting room and lays out what he knows:</p>"
  + boxm(("'Thank you for your aid. I assume you already suspect my reasons",
          "<p>He'd hoped the Soldado case was isolated; instead, three brother priests woke with the same symptoms the morning after his first visit — then acolytes, guards, vaultkeepers, and a swelling stream of citizens. They're calling it <strong>blood veil</strong>.</p>"),
         ("'Most of the patients we're treating have come from North Point",
          "<p>The disease runs fastest through the lower classes of North Point and Old Korvosa, and it will soon outpace the temple's resources. The whole city must organize — the faiths of Sarenrae, Pharasma, even Asmodeus; the Guard; the queen's new agents. He asks the PCs to escort him to Citadel Volshyenek for an introduction to Field Marshal Kroft.</p>"))
  + B.s_treasure("<p><strong>Escort pay:</strong> the church has cleared <strong>200 gp per PC</strong> for the errand (Ishani adds 50 gp apiece from his own purse if they hesitate). What he knows beyond the briefing: the first outside cases were a barkeep and his wife from the Three Rings Tavern, cured and sent home — then three more within the hour, and more every hour since.</p>")
  + B.s_conv("<p>From here the chapter opens into <em>First, Do No Harm</em>, then the cure missions (the <em>Direption</em>, the sewers, Lavender, Racker's Alley, Carowyn Manor) and finally the Hospice of the Blessed Maiden / Temple of Urgathoa. Advance the Epidemic Clock as in-city days pass.</p>"))

# --- Part 2: Outbreak — the Queen's Physicians & the cure missions ---
PG("First, Do No Harm & the Queen's Physicians", SR("First, Do No Harm", 85)
  + "<p>Reaching Citadel Volshyenek is easy — the streets conduct business in whispers, as if noise might draw the plague's notice. Hours before the PCs arrive, Kroft received royal orders: the Guard must escort and obey Queen Ileosa's new <strong>Queen's Physicians</strong> and treat any Gray Maiden's command as a superior officer's. The introduction is in full swing as the PCs enter:</p>"
  + box("The echoes of forcefully spoken but unintelligible words",
        "<p>In the citadel's mustering ground, red-and-silver guards stand uneasy as Field Marshal Kroft paces a wooden platform. Behind her loom cowled figures in oily leather, gloves, and wide black hats, each masked with a dark-goggled, beak-like visor — some gripping canes, others dark satchels. Among them: a soft-spoken, white-streaked gentleman clutching a doctor's case.</p>",
        cut="The second figure is an imposing one",
        tail="<p>The second figure is an imposing one: a Gray Maiden, anonymous in her crimson-plumed full plate.</p>")
  + box("The Field Marshal's fierce tone cuts through",
        "<p>Kroft's address is curt: the Guard will escort Doctor Davaulus and his physicians wherever their royal duties take them, and will treat Gray Maiden orders as binding as any superior officer's. These are dire times; the city needs these healers — and needs its Guard. Dismissed.</p>")
  + "<p>The grunts gripe quietly afterward — offended that outsiders now outrank them, and afraid the doctors will bring the sickness with them. The armored woman is <strong>Kordaitra Destaid</strong>, the Gray Maidens' quartermaster and second-in-command; she takes no notice of the PCs now but confronts them later. Kroft (guarded in this company — the doctors unnerve her too) introduces <strong>Dr. Reiner Davaulus</strong>: calm, fatherly, deliberate. He welcomes questions, defers detailed plans until he has conferred with Kroft, and produces the queen's public writ from his bag — one of hundreds soon posted across the city:</p>"
  + boxm(("By Decree of Her Royal Majesty, the Radiant Queen Ileosa",
          "<p><strong>Attention!</strong> By decree of Queen Ileosa, all citizens and the Korvosan Guard are to aid and admit the Queen's Physicians, who will extend healing, organize the defense against 'blood veil,' and may enter any home or building their duties require; all who suffer disease or disorder must submit to them for treatment.</p>"),
         ("To aid in the duties of the Queen's Physicians, know that",
          "<p>The order of the Gray Maidens shall provide military support; the Maidens answer directly to the Crimson Throne and will strengthen the peace wherever city guards do not suffice.</p>"),
         ("Impeding or distracting the Queen's Physicians",
          "<p>Impeding or distracting the Physicians or Maidens: imprisonment. Impersonating either: death. Knowingly harboring or hiding the infected: death. Purposefully spreading blood veil: torture, then death.</p>"),
         ("The Queen's Physicians will be making rounds",
          "<p>The Physicians will make rounds of every district until Her Majesty deems the misfortune abated.</p>"))
  + "<p><em>(Give the players the decree as a handout — it is the chapter's social contract, and its penalty clauses come back to bite anyone who later impersonates a physician or hides a sick friend.)</em> Questioned directly, the masked physicians say little and defer to Davaulus, voices muffled and disembodied; asked to prove themselves human, one <strong>lifts</strong> its mask to show an ordinary face — each claims to be a local healer or a country doctor rushed in from Harse, Palin's Cove, or Veldraine. "+act(A2["ishani"], "Ishani")+" offers to coordinate the Abadaran effort and heads inside, cautiously optimistic; the meeting that follows yields only talk of quarantines and movement limits.</p>"
  + SEC("<p><strong>The truth.</strong> Davaulus is a <strong>Red Mantis</strong> assassin — a poisoner who masterminded blood veil with Andaisin and Ramoska; his masked 'physicians' are "+act(A2["physician"], "Urgathoa cultists")+" who <em>spread</em> the plague while feigning to treat it. Lifting a mask does not remove it — their "+itm(I2["mask"], "plaguebringer's masks")+" keep veiling their auras and faith. His one tell: he praises the queen too warmly, and he never lies when he doesn't have to. He is the Hospice finale boss (Part 3).</p>"))

PG("Combating the Plague (the missions)", SR("Combating the Plague", 88)
  + "<p>Kroft (and Davaulus, for show) sets the PCs to investigate the plague's source and stem it. The chapter offers <strong>five missions</strong>, each opened by its own hook and run in any order over the days the city sickens — every mission completed saves lives (Survivor Count) and adds clues pointing to the Hospice of the Blessed Maiden. Attempting all five isn't required — but <strong>jumping the gun</strong> on the hospice costs the party the gear, levels, and clues the missions provide, and ends the chapter with far more dead.</p>"
  + SEC("<p><strong>The Quarantine of Old Korvosa.</strong> After the PCs complete two or three missions (and before the Hospice in Part 3), Ileosa quarantines all of Old Korvosa: the Gray Maidens burn every wooden bridge and barricade the one stone bridge. This <strong>cannot be prevented</strong> — it sets up Chapter 3. (How to come and go appears in Chapter 3.)</p>"))

PG("Mission 1: The Wreck of the Direption", SR("Mission 1 — the Direption", 89)
  + "<p>Cressida gives the wreck's location. Diving the muddy Jeggare, "+chk("type:perception|dc:19")+" locates the ship ("+chk("type:perception|dc:23")+" without a light source); "+chk("type:athletics|dc:16")+" swims the placid deep. Every 10 minutes searching carries a cumulative chance of drawing the silt eels. "+chk("type:society|dc:21")+" identifies a Nidalese merchantman; "+chk("type:society|dc:28")+" (Guard records) traces it to the long-'lost' <em>Direption</em> of Garagori Whenston — a dead-end that is precisely the point.</p>"
  + SEC("<p><strong>It is a red herring.</strong> The ship carries no plague source — only clues that waste days. Lady Andaisin left a lethal surprise: the sea-hag druid "+act(A2["yvicca"], "Yvicca")+" and her jigsaw-shark companion <strong>Skinshear</strong>, moved into the wreck to kill investigators. The hull lies split in two over a rock; the stern's main hatch ("+chk("type:athletics|dc:24")+") and hold trap door ("+chk("type:athletics|dc:22")+") are swollen shut, but a 10-ft trebuchet hole opens easy access to A2.</p>")
  + B.s_conv("<p>This is an <strong>underwater</strong> dungeon — without water-breathing/freedom of movement the PCs fight at a real disadvantage; flag that to the GM. Re-judge attack/movement penalties per the PF2e aquatic-combat rules.</p>"))

area2("A1", "The Direption's Bow", SR("A1", 90)
  + box("The front portion of the ship broke away and landed awkwardly",
        "<p>The shattered bow lies awkwardly on its side, two splintered decks exposed, the name <em>Direption</em> still legible along the fire-scarred hull.</p>")
  + "<p>The bow emptied its contents into the current as it sank; the forecastle and galley doors swing open in the flow, and "+chk("type:perception|dc:20")+" confirms there were <strong>no supplies and no personal goods</strong> aboard — the first hint the ship sailed empty. Six "+act(A2["silteel"], "silt eels")+" nest in the scattered pots and overturned bunks, lunging at anything that disturbs them.</p>"
  + B.enc("Silt eel nest", encx([1]*6, 4),
     "<p>6 "+act(A2["silteel"], "silt eels")+" swarm — individually weak, but their stacking venom and the underwater footing make them a real nuisance. Wounded eels flee to the bow and there fight to the death.</p>",
     B.aside_token(["6× "+act(A2["silteel"], "Silt Eel (1)")])))

area2("A2", "The Shattered Hold", SR("A2", 90)
  + box("A yawning wound in the ship's charred timbers",
        "<p>Murky water flows through a yawning hole in the charred timbers; loose planks, small fish, and dozens of identical empty boxes float eerily in the dark.</p>")
  + "<p>The hold carried <strong>no plague</strong> — the ship sailed in essentially empty, crewed by cultists who abandoned it at the river mouth, leaving only the zealot Rois Vindmel (A4) to pilot it in. "+act(A2["yvicca"], "Yvicca")+" has set her jigsaw-shark companion "+B.cmon("Skinshear")+" here to guard the way down. It circles, butts the door to A3 to warn its mistress, then attacks.</p>"
  + B.enc("Skinshear (Yvicca's shark)", encx([B.cmon_lvl("Skinshear")], 4),
     "<p>"+B.cmon("Skinshear")+" — Yvicca's unusually large jigsaw shark, statted as his own creature (no Elite adjustment needed). It fights to the death and alerts Yvicca.</p>",
     B.aside_token([B.cmon("Skinshear", "Skinshear (3)")])))

area2("A3", "Crew Quarters", SR("A3", 91)
  + box("Several hammocks drift in the murky waters",
        "<p>Hammocks drift between the beams; the water here swirls with a haze of gore, fish heads, and half-eaten eels — chum, circling.</p>")
  + "<p>As in the hold, <strong>no bodies and no personal effects</strong> — the ship had no crew when it went down. The chum is "+act(A2["yvicca"], "Yvicca's")+" housekeeping: the sea-hag druid lairs here. Warned by Skinshear, she prepares (Evil Eye first, then joins the fight in A2); surprised here, she shrieks for her shark on the first round.</p>"
  + B.enc("BOSS — Yvicca", encx([3], 4),
     "<p>"+act(A2["yvicca"], "Yvicca")+", a sea-hag druid (with Skinshear if it still lives). Underwater, at range, with Horrific Appearance and Tanglevine, she is a genuine threat for a party that came unprepared. She fights to the death.</p>",
     B.aside_token([act(A2["yvicca"], "Yvicca (3)"), B.cmon("Skinshear", "Skinshear (3)")]))
  + B.s_treasure("<p><strong>Yvicca's effects (her actual gear — the source places no hoard here):</strong> her <strong>wand of <em>cure moderate wounds</em></strong> (18 charges; she burns it on herself below 15 HP unless surrounded — as a PF2e <em>wand of heal</em>, 2nd rank) and her <strong>+1 shortspear</strong>. Nothing else: the emptiness <em>is</em> the clue. No plague source is here.</p>")
  + B.s_conv("<p>Clearing the wreck proves the plague's source lies elsewhere — pushing the PCs toward Carowyn Manor / Racker's Alley and, ultimately, the Hospice.</p>"))

area2("A4", "The Captain's Cabin", SR("A4", 91)
  + box("the tattered sheets of a canopied bed twist",
        "<p>The tattered sheets of a canopied bed twist like ghosts above its snapped frame; knotted amid the linens, a drowned man idly floats in the murky water. A closed footlocker lies on its side at the room's far end.</p>")
  + "<p>The swollen door takes "+chk("type:athletics|dc:21")+" to force. The corpse is <strong>Rois Vindmel</strong> — the Urgathoan zealot who steered the ship in, knocked out against his own footlocker as she sank. His face is crab-eaten and his tongue gone: <em>speak with dead</em> yields little ("+chk("type:perception|dc:21")+" to make out his tongueless howl of one word — '<strong>Andaisin</strong>'). His silver unholy symbol of Urgathoa hangs at his neck.</p>"
  + B.s_treasure("<p>"+chk("type:perception|dc:16")+" finds skin and hair on the footlocker's corner (the 'murder weapon'); "+chk("type:perception|dc:21")+" confirms its seal held — <strong>the contents are dry</strong>. Inside: ~90 gp re-scaled in coin, a <strong>cloak of resistance +2</strong> (resilient rune; an embroidered Urgathoan symbol comes off with "+chk("type:crafting|dc:21")+" — a failure leaves the cloak broken, +1 until repaired), and <strong>Serving Your Hunger</strong>, Urgathoa's sacred text — exquisitely bound (~150 gp re-scaled bounty from any non-evil Korvosan church; ruined to a third of that if the footlocker is opened underwater). Rois has scratched out 'Urgathoa' throughout and penned in '<strong>Andaisin</strong>.'</p>")
  + SEC("<p><strong>The name that matters.</strong> "+chk("type:society|dc:21")+" or "+chk("type:diplomacy|dc:23")+" (gather information) — or simply telling Cressida — reveals: years ago the Nidalese village of <strong>Beorandy</strong> died of engineered plague at the hands of an Urgathoan cell led by <strong>Andaisin</strong>, still wanted in Pangolais for mass murder. Cressida grows grim: the 'plague ship' was a decoy, and a plague-cult is loose in Korvosa. <strong>Story awards:</strong> the cult connection (1,600 XP) and Andaisin's significance (1,200 XP).</p>")
  + B.s_conv("<p><strong>Survivor Count:</strong> the wreck is the conspirators' time-sink — every day past the first spent on the Direption costs <strong>10 citizens</strong> from the chapter's saved-lives tally (and feeds the Epidemic Clock).</p>"))

PG("Mission 2: Plague Rats", SR("Mission 2 — Plague Rats", 92)
  + "<p>Plague-panicked mobs have begun lynching Korvosa's reclusive wererats, and the firebrand <strong>Girrigz Ripperclaws</strong> answers with a call to war on the city above. An elder wererat, <strong>Eries Yelloweyes</strong> (50 years hidden as a fishmonger), fears a purge and approaches the PCs in human form: stop Girrigz — ideally <em>without</em> a slaughter of her people — and she'll have her kin fight the plague from the shadows (disposing of infected bodies). She gives directions to his lair beneath Midland.</p>"
  + B.s_skill("<p>The sewers are slick: moving faster than half Speed or attacking in the sewage flow forces "+chk("type:acrobatics|dc:18")+" or fall "+B.cond("prone", "Prone")+". A "+chk("type:nature|dc:19")+" recognizes the alarm-fungus shrieker in B2.</p>")
  + SEC("<p><strong>Survivor Count:</strong> scattering Girrigz's warband without killing the other (coerced) wererats saves <strong>400 citizens</strong> and seeds an ongoing wererat ally network — a major win for the persistent-plague Epidemic Clock.</p>"))

area2("B1", "Sewer Tunnel", SR("B1", 92)
  + box("Through the disgustingly visible haze of noxious sewer reek",
        "<p>Through the visible haze of sewer reek, the flow of slop unexpectedly forks — a thin stream diverting through a man-sized cleft in the moldy masonry, wisps of white smoke drifting out.</p>")
  + "<p>The approach to Girrigz's camp through Korvosa's sewers (pad it with wandering-monster encounters if the party needs XP). The main tunnel bends east another 20 feet to a rusty grate overlooking B4.</p>")

area2("B2", "Guard Den", SR("B2", 92)
  + box("The flow of sewer filth oozes into this rough-hewn stone cave",
        "<p>Sewer filth oozes in from the west and pools to the south; fat black mushrooms crowd the slime, and low alcoves hold moldering hay, filthy furs, and tiny bones.</p>")
  + "<p>A guard post around a sewage pool. A "+B.cmon("Shrieker", "shrieker fungus", kind="hazard")+" by the south wall screeches if any creature enters and doesn't immediately move north past the central pillar — its noise summons the B3 wererats and the B5 swarm, and wakes the B4 "+B.mon("otyugh", "otyugh")+".</p>"
  + B.enc("Wererat guards", encx([2, 2, -1, -1, -1], 5),
     "<p>2 "+B.mon("wererat", "wererats")+" and 3 "+B.mon("giant-rat", "giant rats")+" (the rats avoid crossing the water lest they trip the shrieker; the wererats cross it deliberately to raise the alarm).</p>",
     B.aside_token(["2× "+B.mon("wererat", "Wererat (2)"), "3× "+B.mon("giant-rat", "Giant Rat (−1)"), B.cmon("Shrieker", "Shrieker (Hazard −1)", kind="hazard")])))

area2("B3", "Communal Dens", SR("B3", 93)
  + box("Several pieces of broken furniture, dried hay, and fragments",
        "<p>Broken furniture and lumber burn in a small central fire; alcoves hold oversized rats' nests, black condensation drips, and sewage seeps across the western edge.</p>")
  + "<p>The wererats' fire-lit warren of nests. The floor is slippery in the sewage flow (as B2). "+chk("type:perception|dc:21")+" finds a squeeze-hole to B6 (Small creatures slip through; "+chk("type:acrobatics|dc:20")+" for a Medium creature to Squeeze); "+chk("type:crafting|dc:19")+" or "+chk("type:perception|dc:21")+" notes the subsiding south wall — chipping it (Hardness 8, 40 HP) lets the trapped "+B.mon("otyugh", "otyugh")+" rampage through.</p>"
  + B.enc("Wererat den (Girrigz reinforces)", encx([2, 2, 2, 2], 5),
     "<p>4 "+B.mon("wererat", "wererats")+". If fighting erupts here, "+act(A2["girrigz"], "Girrigz")+" comes through the east wall from B6 in his dire-rat form.</p>",
     B.aside_token(["4× "+B.mon("wererat", "Wererat (2)"), act(A2["girrigz"], "Girrigz (6, reinforces)")]))
  + B.s_treasure("<p>"+chk("type:perception|dc:19")+": 3 smokesticks, a tanglefoot bag, a thunderstone, 20 tindertwigs, a copper coat-of-arms trumpet (~15 gp re-scaled), and masterwork carpenter's tools.</p>"))

area2("B4", "Trapped Otyugh", SR("B4", 93)
  + box("Two thick grates of rusted iron hedge in this section",
        "<p>Two thick, rusted iron grates hedge in this stretch of tunnel; a cart-sized clot of filth and debris part-dams the flow between them.</p>")
  + "<p>The wererats have penned a lone "+B.mon("otyugh", "otyugh")+" between two grates (Hardness 10, 60 HP, lift "+chk("type:athletics|dc:26")+"; the jammed east-grate winch retracts it after a minute's cranking). Starving, it sleeps until noise wakes it.</p>"
  + B.s_skill("<p>The otyugh ('so hungeries!') can be turned against the wererats: "+chk("type:diplomacy|dc:23")+" (+4 if fed) wins an hour's help, or "+chk("type:intimidation|dc:20")+" buys 10 minutes — after which it forgets and tries to eat the PCs.</p>")
  + B.enc("Otyugh (if it attacks)", encx([4], 5),
     "<p>One hungry "+B.mon("otyugh", "otyugh")+" — a potential ally or a third combatant in the wererat fight.</p>",
     B.aside_token([B.mon("otyugh", "Otyugh (4)")])))

area2("B5", "Rat Dens", SR("B5", 93)
  + box("The scrapes and scratches of tiny claws cover the uneven walls",
        "<p>Claw-scratches and dozens of fist-sized holes pock the walls like a rocky beehive; hundreds of bones — rat, horse, fish, human — litter the floor.</p>")
  + "<p>A bone-littered nest cave. The colony attacks anything that doesn't smell of rodent; the swarm investigates if the shrieker sounds, but the dire rats are too lazy to.</p>"
  + B.enc("Rat nest", encx([1, -1, -1, -1, -1, -1, -1], 5),
     "<p>A "+B.mon("rat-swarm", "rat swarm")+" and 6 "+B.mon("giant-rat", "giant rats")+".</p>",
     B.aside_token([B.mon("rat-swarm", "Rat Swarm (1)"), "6× "+B.mon("giant-rat", "Giant Rat (−1)")])))

area2("B6", "Girrigz's Den", SR("B6", 94)
  + box("Several crates, mismatched boxes, and poorly kept weapons",
        "<p>Crates, mismatched boxes, and ill-kept weapons fill the den; a crude sketched map of Korvosa is pinned to one stack, and a moldy-pillowed rat's nest fills a hollow in the south wall.</p>")
  + "<p>The warlord's command den. "+act(A2["girrigz"], "Girrigz")+" plots his war here, dreaming of burning Castle Korvosa — unwarned, he is caught studying his map. He doesn't react to the shrieker, but fighting in B3 or the otyugh's release brings him (pre-buffed, in dire-rat form through the B3 wall-crack).</p>"
  + B.enc("BOSS — Girrigz Ripperclaws", encx([6], 5),
     "<p>"+act(A2["girrigz"], "Girrigz")+" — pre-buffed if warned, striking from stealth with his runed rapier and Vital Strike. He cannot be reasoned with and fights to the death.</p>",
     B.aside_token([act(A2["girrigz"], "Girrigz Ripperclaws (6)")]))
  + B.s_treasure("<p>"+chk("type:perception|dc:19")+": an arms cache (22 daggers, 12 short swords, 3 crossbows, 4 chain shirts, 12 alchemist's fire, a masterwork longsword + chainmail). "+chk("type:perception|dc:21")+" in the nest: 4 potions of healing, a bottle of air, and a <strong>pearl of power</strong> (2nd-rank) — plus the squeeze-crack to B3 ("+chk("type:acrobatics|dc:20")+" for a Medium creature to Squeeze through). Girrigz carries ~23 gp re-scaled besides his runed mithral rapier.</p>"))

PG("Mission 3: The Color of Death", SR("Mission 3 — The Color of Death", 96)
  + "<p>The Lavender perfumery off Summoning Street, owned by the Chelish con-artist "+act(A2["vendra"], "Vendra Loaggri")+", is selling 'Lavender's Luxuriant Liniment' — a 2-gp 'plague cure' that is sugar, cheap scent, and river water. By day a queue stretches four blocks; the mission is to <strong>expose the fraud</strong>, not to fight.</p>"
  + B.s_skill("<p><strong>Cracking the con:</strong> "+chk("type:crafting|dc:22")+" (an hour with an alchemist's lab) reveals the liniment is worthless; "+chk("type:perception|dc:20")+" spots her planted shill Solt Carmino (the only 'customer' browsing perfume), and "+chk("type:diplomacy|dc:24")+" or "+chk("type:intimidation|dc:24")+" makes him confess. The cleanest proof: administer a dose to a real plague victim before a Korvosan Guard (Grau or Kroft will witness), then actually cure them.</p>")
  + SEC("<p>This 'cure' is a <strong>dead end</strong> for the plague (and a moral test) — it heals no one. Watching Vendra's thugs haul river-water barrels from the Jeggare by night (easy to tail) is the fastest evidence. Report to Cressida and the Guard arrests her.</p>")
  + B.s_treasure("<p><strong>Story award:</strong> expose the scam and shut Lavender down → <strong>1,600 XP</strong>, plus full XP for everyone (Vendra included) the PCs <em>didn't</em> have to defeat in combat.</p>")
  + SEC("<p><strong>Survivor Count:</strong> ending the false cure saves <strong>700 citizens</strong> — people who would have contracted and spread blood veil believing the liniment protected them.</p>"))

area2("C1", "The Perfumery (Lavender)", SR("C1", 96)
  + box("Heady scents twist throughout the cramped but stylish perfumery",
        "<p>Heady scents fill the cramped, stylish shop; the long counter is stacked with hundreds of clay phials with magenta stoppers under a violet-flourished sign promising the Luxuriant Liniment.</p>")
  + "<p>"+act(A2["vendra"], "Vendra")+" works the crowd while two shop-girls sell and two "+act(A2["lavthug"], "Lavender thugs")+" watch with saps. Confront her with proof and she screams for the PCs' ejection (offering free doses to win her customers back); cornered, she flees toward C2, knifing a PC on the way out.</p>"
  + B.enc("Vendra + thugs (by day)", encx([6, 2, 2], 6),
     "<p>"+act(A2["vendra"], "Vendra")+" and 2 "+act(A2["lavthug"], "Lavender thugs")+" amid scattering customers (CR7-equivalent by day; fewer guards and no crowd at night make it easier). Vendra fights dirty and runs.</p>",
     B.aside_token([act(A2["vendra"], "Vendra Loaggri (6)"), "2× "+act(A2["lavthug"], "Lavender Thug (2)")]))
  + B.s_treasure("<p>"+chk("type:crafting|dc:20")+" picks out genuine perfumes worth ~80 gp re-scaled; the counter box holds ~42 gp in recent sales, and the safe ("+chk("type:thievery|dc:26")+") ~76 gp in coin + three carved lapis perfume bottles (~5 gp each). Vendra carries a <strong>circlet of persuasion</strong>, a wand of <em>charm person</em>, a wand of <em>remove disease</em> (3 charges — she's saving the last to flee the city), and ~18 gp of silver-and-violet jewelry.</p>"))

area2("C2", "Vendra's Apartment", SR("C2", 99)
  + box("Delicate wall hangings, artistically shaped candles",
        "<p>Delicate hangings, sculpted candles, and cherry-blossom scent dress the apartment; an ivy-carved table bears porcelain tea things and a curved hookah, and the bedroom holds an antique armoire and a purple-silk bed.</p>")
  + "<p>A locked ("+chk("type:thievery|dc:21")+"), prim parody of a Chelish noble's salon — tawdry romances, maudlin poetry, amateur art, and <strong>no alchemy anywhere</strong>. "+chk("type:perception|dc:21")+" finds a corner-hinged <strong>secret door</strong> into the boarded-up lab (C3). By night there's a 50% chance Vendra sleeps here; otherwise she's mixing brew in C3.</p>")

area2("C3", "The Liniment Laboratory", SR("C3", 99)
  + box("Bits of broken crates and barrels cover the floor",
        "<p>Broken crates litter the dilapidated apartment around a four-foot tub of oily liquid with an oar in it, casks of murky water, boxes of magenta-stoppered vials — and, despite the shambles, a delightful smell of spice and flowers.</p>")
  + "<p>The 'condemned' apartment behind the shop, boarded shut inside and out (Hardness 5, 15 HP, "+chk("type:athletics|dc:24")+" to break), reachable by the C2 secret door. Here the fake cure is mixed from river water hauled in nightly — the bottles, perfumes, and water barrels are all the hard evidence the Guard needs. By day one "+act(A2["lavthug"], "thug")+" works; by night Vendra and two thugs brew.</p>"
  + B.enc("Lab guards", encx([2], 6),
     "<p>1 "+act(A2["lavthug"], "Lavender thug")+" by day (more at night with Vendra).</p>",
     B.aside_token([act(A2["lavthug"], "Lavender Thug (2)")]))
  + B.s_treasure("<p>The lab equipment functions as an alchemist's lab; the raw ingredients are ~80 gp re-scaled of potion/alchemy reagents — a useful crafting stock for the party.</p>")
  + B.s_conv("<p>Mission complete: the perfumery con collapses. It cured nothing — the real source is still out there, pointing the PCs onward (Racker's Alley, Carowyn Manor, the Hospice).</p>"))

PG("Mission 4: The Hungry Dead", SR("Mission 4 — The Hungry Dead", 100)
  + "<p>As bodies pile up, lazy plague-carters have been dumping corpses in <strong>Racker's Alley</strong> (western Old Korvosa) instead of the Gray District. Kroft (or the temple, or rumor) sends the PCs to confirm it and clear any scavengers or undead before guards haul the dead away.</p>"
  + SEC("<p><strong>GM:</strong> four "+B.mon("vampire-servitor", "vampire spawn")+" — minions of the Ustalavic vampire-count Tiriac, sent to 'assist' (and watch) the nosferatu <strong>Ramoska Arkminos</strong> — have lairred under Giotorri's Toys and feed on the dumped (and the living). They long ago forgot their charge to watch Ramoska. <em>Ramoska is the Temple-of-Urgathoa villain (Part 3).</em></p>")
  + SEC("<p><strong>Survivor Count:</strong> clearing the spawn and confirming the dumping ground (so the Guard can stop it) saves <strong>200 citizens</strong> — feed it into the Epidemic Clock.</p>"))

area2("D1", "Racker's Alley", SR("D1", 100)
  + box("The high walls of the surrounding buildings throw this awkwardly bent alley",
        "<p>High walls keep the bent alley in constant shadow; heaped against a wooden wall rise three dozen plague dead, faces blistered, eyes staring — and some of the bodies look strangely pale beside the rest.</p>")
  + "<p>A shadowed, sunless dead-end alley with 40+ corpses heaped against the east wall. "+chk("type:perception|dc:20")+" notes that many bodies are blood-drained with neck/wrist punctures — and bear <em>no</em> blood-veil sores. <strong>Contact with the plague-dead exposes a creature to Blood Veil</strong> ("+chk("type:fortitude|dc:24")+"). A 10-ft hole in the east wall opens into the workshop (D2).</p>"
  + B.enc("Vampire spawn sentry", encx([4], 6),
     "<p>By night one "+B.mon("vampire-servitor", "vampire spawn")+" watches from the 20-ft roof (−2 to spot it from the alley floor). Seeing anyone touch the bodies, it shrieks and attacks; its 3 companions arrive from D2 in 1d3 rounds.</p>",
     B.aside_token([B.mon("vampire-servitor", "Vampire Spawn (4)")])))

area2("D2", "The Workshop", SR("D2", 101)
  + box("Dozens of glass eyes-crooked and crazed-glare from the heads",
        "<p>Crooked glass eyes glare from shelves of malformed, half-carved dolls; bins hold rat-gnawed stuffed beasts and unseaworthy toy ships, and in one corner the drying corpse of an old bald man lies amid rusty tools and oily rags.</p>")
  + "<p>Beneath the toy-shop: a 3½-foot dirt crawl space (difficult terrain for Medium creatures) under the trap door, where the four "+B.mon("vampire-servitor", "vampire spawn")+" keep their Ustalavic-soil coffins, watched over by the desiccated corpse of the toymaker Rodolfo Giotorri (eight neck-punctures, "+chk("type:perception|dc:19")+" to notice; "+chk("type:perception|dc:15")+" finds his key ring). By day they sleep here (−10 to their Perception; killing one wakes the rest thrashing and howling). Fight all four here if the alley alarm was raised.</p>"
  + B.enc("BOSS — the four vampire spawn", encx([4, 4, 4, 4], 6),
     "<p>All 4 "+B.mon("vampire-servitor", "vampire spawn")+" — blood drain, dominate gaze, fast healing, and their vampire weaknesses (running water, sunlight). They bicker over prey and split up one-per-PC rather than coordinate. A genuine Severe-leaning fight; bait them toward sunlight or a threshold.</p>",
     B.aside_token(["4× "+B.mon("vampire-servitor", "Vampire Spawn (4)")]))
  + B.s_treasure("<p>"+chk("type:perception|dc:21")+" in the coffin soil: ~45 gp re-scaled of Ustalavic-minted coin, a <strong>ring of jumping</strong> (brass spider-legs), and <strong>pipes of haunting</strong> (bone).</p>"))

area2("D3", "Giotorri's Toys", SR("D3", 101)
  + box("Awkwardly stitched stuffed animals, poorly equipped toy soldiers",
        "<p>Badly stitched animals, shoddy toy soldiers, and accidentally deformed dolls stare from the filth-smeared window; heavy kites trail purple and crimson tails over a dollhouse Castle Korvosa and a counter of dusty candy jars.</p>")
  + "<p>The dusty, locked showroom above ("+chk("type:thievery|dc:28")+", or Giotorri's key from D2). The spawn left the cheap, defective toys alone — which is why nobody ever investigated.</p>"
  + B.s_treasure("<p>"+chk("type:perception|dc:19")+": a jingling lockbox ("+chk("type:thievery|dc:21")+") with a few coins, a silver tooth, and an <strong>Abadaran deposit-box key</strong> (No. 261; "+chk("type:society|dc:20")+" or "+chk("type:religion|dc:20")+" to place it). Redeemed at the Grand Vault, it yields Giotorri's life savings (~7 gp re-scaled), masterwork thieves' tools, <strong>boots of striding and springing</strong>, and a sheaf of terrible toy designs.</p>")
  + B.s_conv("<p>Clearing Racker's Alley removes one of Ramoska's loose ends — and quietly establishes the vampire's presence ahead of the Temple finale.</p>"))

PG("Mission 5: The Case of the Vanishing Virtuoso", SR("Mission 5 — Carowyn Manor", 104)
  + "<p>Deyanira Mirukova begs the PCs (or Kroft refers her) to find her brother <strong>Ruan</strong>, a Varisian ocarina prodigy who went to perform at a masquerade at <strong>Carowyn Manor</strong> and never returned. The estate now sits locked, curtained, and reeking. "+chk("type:society|dc:21")+" recognizes Ruan as a genuine virtuoso. (Her reward is meager — heirlooms under 100 gp and Marbledome passes — but the trail matters.)</p>"
  + SEC("<p><strong>GM:</strong> Ileosa added <em>rich</em> undesirables to the plague's toll; Davaulus farmed the hit-list to the necromancer <strong>Rolth Lamm</strong> (Gaedren's son, the absent master of the Ch.1 Dead Warrens), who — absorbed in studying Varisian plague-immunity — handed it to his lover "+act(A2["jolistina"], "Jolistina Susperio")+". She murdered the entire party, raised 21 of the guests as zombies, and disguised every corpse as a blood-veil death. <strong>The 'plague' here is staged.</strong></p>")
  + B.s_skill("<p><strong>Getting in:</strong> the mahogany front doors are locked ("+chk("type:athletics|dc:26")+" / "+chk("type:thievery|dc:29")+"); the iron fence takes "+chk("type:athletics|dc:20")+" to Climb; the balcony banisters take "+chk("type:athletics|dc:21")+" to climb; the spiked garden hedge "+chk("type:athletics|dc:19")+" (fail by 5+ → @Damage[1d6[piercing]]). Jolistina jammed the side doors and shutters ("+chk("type:athletics|dc:25")+"/"+chk("type:thievery|dc:24")+" doors; windows "+chk("type:thievery|dc:24")+").</p>"))

area2("E1", "Carowyn Manor — First Floor", SR("E1", 106)
  + box("A massacre took place here. Upon the marble floor",
        "<p>A massacre: more than a dozen corpses in garish sequins, silk, and feathers lie heaped on the marble, elaborate masks fallen away from withered, blister-covered faces — and at the room's blood-slick center, three couples sway in a jerking, hellish dance, all obviously dead.</p>")
  + "<p><strong>The whole manor is one complex encounter.</strong> "+act(A2["jolistina"], "Jolistina")+" hides and plays cat-and-mouse, ordering her posed zombies to defend her while she snipes and Vanishes. Of her 21 "+B.mon("zombie-shambler", "zombies")+", <strong>7 are uncontrolled</strong> (they attack anyone — Jolistina included; she avoids those rooms). Every corpse, dead or undead, was disguised with <em>sculpt corpse</em> to look like a blood-veil death: "+chk("type:medicine|dc:20")+" (or "+chk("type:will|dc:11")+") while examining a body reveals the symptoms are <strong>manufactured</strong>, and none are contagious.</p>"
  + B.enc("E1a Great Hall — dancing dead", encx([-1] * 6, 6),
     "<p>6 "+B.mon("zombie-shambler", "human zombies")+" posed as dancing noble couples in the great hall (the read-aloud above); they turn and attack 1 round after the PCs enter.</p>",
     B.aside_token(["6× "+B.mon("zombie-shambler", "Human Zombie (−1)")]))
  + B.enc("E1b Den — uncontrolled trio", encx([-1] * 3, 6),
     "<p>3 <strong>uncontrolled</strong> "+B.mon("zombie-shambler", "zombies")+": a lion- and lioness-masked couple seated before the cold fireplace, attended by a peacock-costumed servant with a silver tray. They attack the moment anyone enters.</p>",
     B.aside_token(["3× "+B.mon("zombie-shambler", "Human Zombie (−1)")]))
  + B.enc("E1c Dining Room — diners", encx([-1] * 4, 6),
     "<p>Eight corpses sit at a finely set table; 4 are "+B.mon("zombie-shambler", "zombies")+" mechanically spooning rotten food into slack jaws. They attack on entry but must each spend an action extricating themselves from their pushed-in chairs.</p>",
     B.aside_token(["4× "+B.mon("zombie-shambler", "Human Zombie (−1)")]))
  + B.enc("E1d Recital Hall — the harpist", encx([-1], 6),
     "<p>1 "+B.mon("zombie-shambler", "zombie")+" dressed as a blue-winged angel strums a standing harp whose every string is broken, before an audience of four costumed corpses (a sea serpent, a castle tower, a swan, a blue skeleton). It attacks on entry.</p>",
     B.aside_token([B.mon("zombie-shambler", "Human Zombie (−1)")]))
  + B.enc("E1e Kitchen — the carvers", encx([-1] * 2, 6),
     "<p>2 <strong>uncontrolled</strong> "+B.mon("zombie-shambler", "zombies")+" — the Carowyns' servants — sit with dull knives, pantomiming the carving of a corpse dressed as a huge pig. They attack on entry.</p>",
     B.aside_token(["2× "+B.mon("zombie-shambler", "Human Zombie (−1)")])))

area2("E2", "Carowyn Manor — Second Floor & Cellar", SR("E2", 108)
  + "<p>Jolistina's remaining 5 posed "+B.mon("zombie-shambler", "zombies")+" haunt the upper floor. Somewhere below, the surviving host <strong>Ausio Carowyn</strong> hides — and the gallery holds the mission's crucial <em>absence</em>.</p>"
  + B.enc("E2a Gallery — the critics", encx([-1] * 3, 6),
     "<p>3 "+B.mon("zombie-shambler", "zombies")+" in flashy metallic costumes wander the picture gallery, pantomiming appreciation and criticism of the Korvosan cityscapes and Carowyn portraits, stumbling over the dozen corpses posed as ghastly statues and contemplative critics. They attack on entry. <strong>The clue:</strong> a search turns up the bodies of three musicians — <strong>Ruan's corpse is not among them.</strong></p>",
     B.aside_token(["3× "+B.mon("zombie-shambler", "Human Zombie (−1)")]))
  + B.enc("E2b Bedroom — the Galtan queen", encx([-1] * 2, 6),
     "<p>2 <strong>uncontrolled</strong> "+B.mon("zombie-shambler", "zombies")+": <strong>Olauren Carowyn</strong> in a pearl-studded gown and ceiling-brushing powdered wig, attended by a 'Qadiran princess.' They attack 1 round after entry. (What the PCs do with Olauren matters to Ausio below — see his entry.)</p>",
     B.aside_token(["2× "+B.mon("zombie-shambler", "Human Zombie (−1)")]))
  + "<p><strong>The wine cellar.</strong></p>"
  + box("A well-stocked wine rack and several large casks line the walls",
        "<p>A well-stocked wine rack and great casks line the stuffy cellar; a small wooden door squats in the southeastern corner.</p>")
  + "<p>Behind the small door is the converted studio of "+act(A2["ausio"], "Ausio Carowyn")+" — <strong>locked from within</strong> ("+chk("type:thievery|dc:29")+" to bypass or "+chk("type:athletics|dc:24")+" to batter down). Inside, among painting supplies: a tawdry divan, a small <strong>shrine to Shelyn</strong>, several scandalous portraits of Olauren — and Ausio himself, shaking, brandishing a dull paint knife. He fled at the first bolt and has lived for days on a water cask and caught rats, listening to shuffling feet and shrill laughter above. Once he believes the PCs mean no harm, he gives what he saw:</p>"
  + box("'We were greeting the Westerkiers when the elven acrobat",
        "<p>They were greeting guests when the hired elven acrobat 'went crazy' — opened fire on a guest with her crossbow, laughing in the most frightful, shrill way. He's been locked in for days; every time he worked up courage, he heard that laughter. Is she dead? Is it safe?</p>")
  + "<p>He asks after his wife: he expected her death, but learning she was made <em>undead</em> — or being shown her body, mangled or worse still walking — breaks his already traumatized mind. Asked about Ruan, he last saw the youth in the second-floor gallery.</p>"
  + B.s_treasure("<p><strong>Story award:</strong> rescue Ausio → XP as if he'd been defeated in combat (he is <em>not</em> Jolistina's plaything — she never found him).</p>")
  + B.enc("BOSS — Jolistina Susperio", encx([8], 6),
     "<p>"+act(A2["jolistina"], "Jolistina")+" makes her stand (or her endless retreat) here, fighting from behind whatever zombies remain. Run her as the manor-spanning skirmish she is, not a stand-up fight. She <strong>surrenders at ≤10 HP</strong>, spilling everything (→ <em>What Jolistina Knows</em>); if she escapes instead, she seeks out Rolth — the PCs may meet her again at his side in the temple.</p>",
     B.aside_token([act(A2["jolistina"], "Jolistina Susperio (8)"), "+ remaining "+B.mon("zombie-shambler", "zombies")]))
  + B.s_treasure("<p>Jolistina carries 2 potions of invisibility, a potion of <em>remove disease</em>, wands of <em>animate dead</em> / <em>sculpt corpse</em> / <em>cat's grace</em>, <strong>+1 glamered studded leather</strong>, a hand crossbow with 3 <strong>screaming bolts</strong>, 4 alchemist's fire, 4 smoke bombs, 4 doses of pesh, and ~23 gp re-scaled in coin and stolen jewelry. The manor itself holds a noble household's worth of re-scaled valuables.</p>")
  + B.s_conv("<p><strong>The reveal:</strong> exposing the staged deaths proves the nobles were murdered, not plagued — and the wand of <em>sculpt corpse</em> + Jolistina's link to <strong>Rolth</strong> ties the killings to the necromancer and the cult of Urgathoa, pointing toward the Hospice. Save Ausio. <strong>Ruan is not dead</strong> — he was carried off alive (see below) and can be rescued from Ramoska's laboratory (G11).</p>"))

PG("What Jolistina Knows & Ruan's Fate", SR("What Jolistina Knows / Ruan's Fate", 109)
  + "<p>Captured alive, "+act(A2["jolistina"], "Jolistina")+" knows much — but she is thoroughly insane. Unless charmed or magically compelled, getting her to talk takes "+chk("type:diplomacy|dc:33")+". Whatever the result she giggles that the speaker's tone reminds her of 'my darling Rolth's silken tongue.'</p>"
  + B.s_skill("<p><strong>Intimidation is a trap with one lever:</strong> the forlorn elf is a fatalistic <strong>masochist</strong> — threats of pain, torture, even infection with blood veil delight her (expect exaggerated scandalous cries). She is immune to all of it <em>except</em> threats of <strong>imprisonment</strong> or of <strong>exposing her failure to Rolth</strong>: with that lever, "+chk("type:intimidation|dc:22")+" gets her talking.</p>")
  + SEC("<p><strong>Her testimony:</strong> Rolth sent her to kill several 'rich bastards' due at the party; everyone else was a bonus. She doesn't know why — she suspects his new employer wanted it, since Rolth knows no such people — nor who the employer is, only that he (or <em>she</em> — an infuriating possibility) keeps Rolth holed up in a hidden laboratory somewhere in the city. The plague disguise? 'Another of my darling Rolth's ideas, but a good one.' <strong>On Ruan:</strong> Rolth asked her to take alive any young, healthy Varisians; Ruan was the only one. She trussed him up, and the morning after the massacre Rolth collected him — with two of those <strong>'bird-masked doctors'</strong> at his side, who carried the youth off to who-knows-where. Released, she finds a pesh den and pines; she asks the PCs to tell Rolth she misses him.</p>")
  + SEC("<p><strong>Redemption (optional):</strong> supportive PCs who take the mad elf in hand — and weather her violent outbursts — can, at your discretion, slowly mend her; redeemed, Jolistina makes a memorable ally or follower.</p>")
  + B.s_treasure("<p><strong>Story award:</strong> learn what Jolistina knows → <strong>2,400 XP</strong> (besides combat XP). <strong>Survivor Count:</strong> destroying the manor's zombies — and stopping Jolistina before boredom sent her creations into the streets, or her on to other manors — saves <strong>500 citizens</strong>.</p>")
  + "<p><strong>Ruan's fate.</strong> Good news and bad for Deyanira: her brother was not among the dead — and a necromancer's masked accomplices carried him off somewhere unknown. The news does little to ease her. She pays what she promised, begs the PCs to chase any rumor of him, and excuses herself, distraught. <strong>Ruan is alive</strong> — strapped to Ramoska Arkminos's operating table in the Temple of Urgathoa (G11), where the PCs can still save him in Part 3.</p>")

# --- Part 3: EPIDEMIC — the Hospice of the Blessed Maiden (F) ---
PG("Part 3 — Epidemic: The Hospice of the Blessed Maiden", SR("Part 3: Epidemic / F. Hospice", 110)
  + B.s_milestone("<p><strong>Part 3 — Epidemic.</strong> The trail converges on the <strong>Hospice of the Blessed Maiden</strong>, the Queen's Physicians' headquarters in a converted warehouse — and on the hidden <strong>Temple of Urgathoa</strong> beneath it. The PCs should be 7th level entering the temple, and just 8th by the chapter's end. This is the plague's heart: "+act(A2["davaulus"], "Davaulus")+", "+act(A2["andaisin"], "Andaisin")+", and the nosferatu "+act(A2["ramoska"], "Ramoska")+".</p>")
  + B.s_skill("<p><strong>Finding the hospice:</strong> Ishani or Cressida simply tell the PCs where it is if asked to investigate the Queen's Physicians (the group makes no secret of its base). Otherwise: "+chk("type:society|dc:21")+" recalls the location, "+chk("type:diplomacy|dc:23")+" gathers it, or the PCs can <strong>tail a group of physicians</strong> for 1d4 hours (a Stealth check against a physician's Perception DC each hour) back to the building.</p>")
  + SEC("<p><strong>The building (GM).</strong> Four months ago the Red Mantis pried this West Dock warehouse — one of the Arkonas' most secret smuggling dens — from the family through bribes and blackmail; when the Arkonas tried to leak its hidden lower level to the Guard, the information <em>and everyone who saw it</em> disappeared. Andaisin's cult rebuilt the smuggler's den into a temple. The 'hospice' above is the perfect cover: nobody wants to enter the city's greatest concentration of sickness — and patients admitted here <strong>do not come back out</strong>; they 'succumb' quickly and the bodies go below. A few days' stake-out makes that arithmetic obvious and damning.</p>")
  + B.s_skill("<p><strong>Getting in:</strong> the front door is unlocked by day, locked after dark ("+chk("type:thievery|dc:29")+"; Hardness 5, HP 15, "+chk("type:athletics|dc:18")+" to break); the boarded-up rear loading doors are sturdier (Hardness 5, HP 30, "+chk("type:athletics|dc:25")+" — and smashing them can be heard from F2). Bluffing or sneaking beats fighting through; pushing too hard gets the PCs an audience with Davaulus (F6), who tries to misdirect them onto a fictional Ghlaunder-worshiping wererat cult. The city can spare <strong>no reinforcements</strong> — this is the PCs' job alone (a token squad of guards or acolytes is your call).</p>"))

area2("F1", "Entry", SR("F1", 112)
  + box("The stinging scent of alcohol and medicine",
        "<p>The stinging smell of alcohol and medicine floods the dingy reception room — the odor of hospices, and of morgues. A stained leather curtain behind the long desk muffles the moans beyond.</p>")
  + "<p>Six poor citizens — all showing blood-veil symptoms, some advanced — huddle here, some having waited hours. At the desk sits the burly 'nurse' "+act(A2["bhrunlida"], "Bhrunlida Torthus")+": a hired charlatan (no cultist; she knows nothing of what's below), triple-scarved and heavy-gloved against infection, with no compassion to spare. She takes names, enforces the queue, and shrilly bars anyone heading for the curtain to F2.</p>"
  + B.s_skill("<p>"+chk("type:diplomacy|dc:25")+" or "+chk("type:intimidation|dc:21")+" convinces her to fetch <strong>Dr. Davaulus</strong>: she steps into F2, and after a few minutes the PCs are led through the sick ward and up to F6, where Davaulus waits with the F6 Gray Maidens and the F7 physicians. Forcing past her instead means her bellows alert F2 while she attacks — impatient and eager for the excuse.</p>")
  + B.enc("The nurse (only if forced)", encx([3], 7),
     "<p>"+act(A2["bhrunlida"], "Bhrunlida Torthus")+" swings to eject intruders while F2 readies a defense; the waiting patients panic and flee. Below 15 HP she runs or begs; all she can betray is the F2 headcount.</p>",
     B.aside_token([act(A2["bhrunlida"], "Bhrunlida Torthus (3)")]))
  + B.s_treasure("<p><strong>Story award:</strong> secure an audience with Davaulus <em>without</em> attacking Bhrunlida → XP as if she'd been defeated in combat.</p>"))

area2("F2", "Sick Ward", SR("F2", 113)
  + box("The warehouse's vast interior has been converted",
        "<p>The vast warehouse interior is one gigantic convalescent ward: the stench of alcohol, sickness, and waste chokes the breath, and tight rows of stained cots — every bed filled, every patient groaning — cram the stone-floored hall.</p>")
  + "<p>More than <strong>60 cots</strong>, each holding a helpless citizen too weak to rise; the cult's masked "+act(A2["physician"], "physicians")+" coo insincerely over the dying. A makeshift kitchen fills the northeast (watery gruel); the ceiling rises ~30 feet, with the F5 catwalks spanning at 20. <strong>Each round a PC spends in this room, 10% chance of blood-veil exposure</strong> — 100% on touching any patient ("+chk("type:fortitude|dc:24")+" as usual).</p>"
  + "<p><strong>Keeping cover:</strong> unescorted PCs are loudly told to wait their turn in F1; demands to see Davaulus get them parked here 1d4+2 minutes, then invited up to F6. The physicians <strong>do not start a fight</strong> — they attack only if attacked, if the PCs name the cult of Urgathoa, or if anyone tries to enter the lift room (F4). The Gray Maidens intercept anyone forcing through and have no such compunctions.</p>"
  + B.enc("Ward watch", encx([3, 3, 2, 2, 2, 2], 7),
     "<p>2 "+act(A2["graymaiden"], "Gray Maidens")+" (door to F4 and the stairs; 2 more on the F5 catwalks above ready bows) and 4 "+act(A2["physician"], "Queen's Physicians")+" among the cots.</p>",
     B.aside_token(["2× "+act(A2["graymaiden"], "Gray Maiden (3)"), "4× "+act(A2["physician"], "Queen's Physician (2)")]))
  + B.s_skill("<p><strong>Fighting among the helpless:</strong> every bed holds an innocent (helpless, 2 HP). The cult doesn't care; the PCs should. Give any <em>missed</em> ranged attack a <strong>25% chance of striking a patient</strong>.</p>")
  + SEC("<p><strong>Development — the evacuation.</strong> Saving 60 bedridden patients is beyond on-the-spot healing: they need somewhere safe. A PC with standing at a city temple can place <strong>30</strong> there; Cressida Kroft can house <strong>30</strong> in unused guard buildings. <strong>If the PCs tip their hand and leave without destroying the cult below</strong>, they return to a shuttered hospice and a cover story about 'thieves and malcontents' forcing a relocation — in truth the patients were murdered and delivered below (bolster the temple with extra zombies). <strong>Story award:</strong> get help for all the patients → <strong>3,200 XP</strong>. <strong>Survivor Count:</strong> every patient who survives the PCs' visit and is cured counts as one life saved.</p>"))

area2("F3", "Loading Dock", SR("F3", 114)
  + boxm(("The scent of exotic wood and sawdust fills this maze of barrels",
          "<p>Exotic wood and sawdust scent this maze of barrels and crates; ropes and pulleys web the ceiling, and a net of barrels hangs twenty feet over the splintered floor.</p>"),
         ("Three great wooden doors stand in the northern wall",
          "<p>Three big wooden doors pierce the north wall; leather flaps lead south and east.</p>"))
  + "<p>The remains of the legitimate Arkona import business — most containers empty, their textiles long since moved. The southwest corner holds <strong>empty animal cages</strong> stenciled with their exotic former occupants ('Three Breaths Viper — Mwangi Expanse,' 'Emperor Cobra (Eggs) — Vudra,' 'Toad Shrew — uncharted island'). Smashing in the alley doors can be heard from F2 (distance-penalized Perception); both F2 Gray Maidens come to investigate anything heard.</p>"
  + B.s_treasure("<p>A thorough half-hour search and "+chk("type:perception|dc:23")+": a crate of elegant Vudrani silks — robes, saris, stoles, turbans — worth ~30 gp re-scaled. One sari is <strong>bloodstained and slashed</strong>: quiet evidence that not everything that happens in this building is medicine.</p>"))

area2("F4", "Warehouse Lift", SR("F4", 114)
  + box("Several cubbies and wooden lockers line the walls",
        "<p>Cubbies and wooden lockers line the small workroom; four rickety chairs ring a water-damaged table, and a well-used but solid cargo lift rises through the ceiling.</p>")
  + "<p>The Red Mantis chose this warehouse <strong>for this room</strong>: the cargo lift is the cleverly concealed — and <strong>only</strong> — access to the hidden level below. Its controls plainly run the lift up to the floors above, but the operating <strong>lever radiates moderate necromancy</strong> (a tell for any caster who looks). "+chk("type:perception|dc:23")+" finds a second control set into the lever's slot: a simple socket <strong>missing its button</strong>. With the button-key seated and pressed, the lift descends to G1 in the Temple of Urgathoa; "+chk("type:thievery|dc:33")+" can force the mechanism to lower without it. <strong>The missing button is carried by Dr. Davaulus</strong> (F8).</p>"
  + B.s_treasure("<p><strong>Story award:</strong> activate the lift and reach the hidden level → <strong>800 XP</strong>.</p>")
  + B.s_conv("<p>The temple guards (G2) listen for the lift: descending it loudly is an announced arrival. Note for mapping: the temple lies <strong>40 feet below</strong> the warehouse floor.</p>"))

area2("F5", "The Catwalks", SR("F5", 114)
  + box("A track of sturdy-looking catwalks soar over the warehouse floor",
        "<p>Sturdy catwalks soar over the warehouse floor, the well-trod platforms hung from iron poles above.</p>")
  + "<p>Relics of the warehouse's shelving days, 20 feet above the F2 floor. Two "+act(A2["graymaiden"], "Gray Maidens")+" patrol here: bows down into the sick ward if a fight breaks out below, intercepting on the stairs (or falling back to guard F6) if intruders head up.</p>"
  + B.enc("Catwalk patrol", encx([3, 3], 7),
     "<p>2 "+act(A2["graymaiden"], "Gray Maidens")+" — sword-and-shield in the choke of the catwalk, longbows if the PCs hang back.</p>",
     B.aside_token(["2× "+act(A2["graymaiden"], "Gray Maiden (3)")])))

area2("F6", "Private Hall", SR("F6", 115)
  + box("The rough functionality of the warehouse below gives way to beige tile",
        "<p>Beige tile and whitewash replace the warehouse's rough function; scored teak double doors engraved with rampant gazelles stand to the south.</p>")
  + "<p>The old clerks' entry, now a guardroom. The doors to F7 are kept <strong>locked</strong> ("+chk("type:thievery|dc:29")+" or "+chk("type:athletics|dc:26")+"; Davaulus holds the key and personally opens them at shift change, dawn and dusk).</p>"
  + B.enc("Hall guards", encx([3, 3], 7),
     "<p>2 "+act(A2["graymaiden"], "Gray Maidens")+" order intruders out — <em>including</em> anyone dressed as staff, since nobody visits outside shift change. Realizing the PCs don't belong, they attack at once, shouting the alarm to F7.</p>",
     B.aside_token(["2× "+act(A2["graymaiden"], "Gray Maiden (3)")]))
  + B.s_skill("<p><strong>Limits of the disguise ruse:</strong> passing as the next shift takes a successful Deception <em>and</em> a disguise (Impersonate) check — and fails <strong>automatically</strong> if more than <strong>2</strong> PCs pose as Gray Maidens or more than <strong>3</strong> as Queen's Physicians (that's the whole shift). Timing it to dawn/dusk is the only window when staff are expected here at all.</p>")
  + SEC("<p><strong>The meeting.</strong> If the PCs arranged an audience (via "+act(A2["bhrunlida"], "Bhrunlida")+" or by being pushy), "+act(A2["davaulus"], "Davaulus")+" receives them <em>here</em>, flanked by the F7 physicians and these guards — see F8 for how he plays it. If combat erupts in this room, the F7 physicians alert the doctor and join within moments.</p>"))

area2("F7", "Experimentation Ward", SR("F7", 115)
  + box("Rows of white-sheeted beds line the walls of this room",
        "<p>White-sheeted beds line the walls, each patient strapped to its metal frame; worktables at the center bear beakers, glass tubing, burners, and other alchemical instruments.</p>")
  + "<p>Here the cult's real work shows: <strong>15 Varisian prisoners</strong>, drugged unconscious and strapped down, each inexplicably <strong>immune to blood veil</strong> — and each being examined, operated on, and mutilated to find out why. All are stable but at death's door; even healed, most are too weak from surgeries to move unaided. None know anything of where they are. The tables hold the cult's research notes.</p>"
  + B.enc("Physicians at work", encx([2, 2, 2], 7),
     "<p>3 "+act(A2["physician"], "Queen's Physicians")+", flanking in silence for Sneak Attacks.</p>",
     B.aside_token(["3× "+act(A2["physician"], "Queen's Physician (2)")]))
  + SEC("<p><strong>The notes — and the alarm.</strong> The research notes spell out <em>why</em> Varisians are being studied, and reference the church of Urgathoa — including several reports '<strong>sent below to A.</strong>' If the PCs attack the hospice openly, the physicians here <strong>burn the notes</strong> (a hasty job — surviving scraps still reveal the cult is active below) and <strong>cut the throats of the 15 Varisians</strong> before joining the defense. Hitting this room fast, or quietly, is the difference between rescue and massacre.</p>")
  + B.s_treasure("<p><strong>Story award:</strong> rescue at least half the prisoners → <strong>1,200 XP</strong>. <strong>Survivor Count:</strong> every Varisian rescued counts as one life saved.</p>"))

area2("F8", "The Doctor's Office", SR("F8", 116)
  + box("Blood, bile, and other humors bubble away",
        "<p>Humors bubble in oddly formed beakers; grisly anatomical parchments — pinned and flagged like a veteran's war maps — paper every gap between cabinets and bookshelves, and a once-beautiful white-ash desk carved with antelope stands disfigured by chemical and gore stains.</p>")
  + "<p>"+act(A2["davaulus"], "Dr. Reiner Davaulus")+"'s laboratory-office. <strong>There is no stair here</strong> — his escape route is the F4 lift, whose button-key he carries. Confronted by appointment (in F6) he plays the gracious, fatherly host with one goal: send the PCs away — ideally to Old Korvosa chasing his <strong>fictional Ghlaunder-worshiping wererat cabal</strong>, even hiring them for the errand. PCs who bite walk into a Red Mantis stalking (Chapter 3) while he relocates every incriminating note to the temple's inner sanctum (G14).</p>"
  + "<p>Caught here unprepared, he turns angry and imperious: they are interrupting <em>royal</em> work on the cure — high treason — and if that fails he lectures, feigning superiority: disease is the world's way of restoring balance; society's dead weight must periodically be pruned; Korvosa will come out of these dark days <em>stronger</em>. The instant he senses an attack coming, he casts <em>invisibility</em> and runs for the lift — possibly tipping off pursuing PCs to the existence of the level below. If he escapes, he is found again in <strong>G5, at Rolth's side</strong>.</p>"
  + B.enc("Reiner Davaulus", encx([9], 7),
     "<p>"+act(A2["davaulus"], "Davaulus")+" (bane-rapier Sneak Attacks, Inspire) — usually backed by the F6/F7 staff if alarmed. He flees to the Temple rather than die in the open; loyal to the Red Mantis, he never surrenders.</p>",
     B.aside_token([act(A2["davaulus"], "Reiner Davaulus (9)")]))
  + B.s_treasure("<p>"+chk("type:perception|dc:21")+" while searching the desk: <strong>Davaulus's scattered notes</strong> on the Varisians' immunity — one of the <strong>three note-sets</strong> behind the cure (→ Chapter Conclusion: Curing Blood Veil); recovering them is worth <strong>2,400 XP</strong>. His gear includes ~58 gp re-scaled, the <strong>lift button-key</strong>, the G3 cabinet and F7 door keys — and a <strong>flask of curses</strong> neatly labeled '<em>elixir of true healing</em>', left where a looter would grab it first ("+chk("type:will|dc:22")+" for the drinker).</p>")
  + B.s_conv("<p>His notes (here, or relocated to G14 if the PCs were fooled) confirm the manufactured plague. The lift down (F4) begins the <strong>Temple of Urgathoa</strong>.</p>"))

# --- Part 3: the Temple of Urgathoa (G) ---
PG("The Temple of Urgathoa", SR("G. Temple of Urgathoa / The Temple Under Alert", 118)
  + B.s_milestone("<p><strong>G. The Temple of Urgathoa</strong> — the cult's hidden warren 40 feet beneath the hospice, reached only by the F4 lift. A former smuggler's den, freshly excavated and re-walled in plaster (already water-stained), its murals celebrate plague-drowned cities. Most areas are lit; <strong>G1 and G9–G12 are dark</strong>. Doors are strong wood (Hardness 5, HP 20, "+chk("type:athletics|dc:25")+" / "+chk("type:thievery|dc:29")+"), locked only where noted.</p>")
  + SEC("<p><strong>The Temple Under Alert.</strong> The areas below assume the cult doesn't know it's under attack. Once the alarm goes up (Davaulus fleeing down, the G1 doors' linked <em>alarm</em>, or any survivor of a first skirmish):</p>"
    "<ul><li><strong>Cultists (14 active):</strong> 6 to hold G8, 8 to defend G13.</li>"
    "<li><strong>Queen's Physicians (5 active):</strong> to the G8 floor.</li>"
    "<li><strong>Davaulus:</strong> warns Andaisin, then joins G8. <strong>Rolth:</strong> to the G8 catwalk.</li>"
    "<li><strong>Gray Maidens</strong> (any who followed Davaulus down): bows trained on G1's doors.</li>"
    "<li><strong>Skeletons (G7) and zombies (G9):</strong> posted to guard G4.</li>"
    "<li><strong>Ramoska:</strong> ignores the alarm entirely and keeps working in G11. <strong>Andaisin:</strong> see G14.</li></ul>"
    "<p><strong>No reinforcements come</strong> — blood veil has mostly run its course and the conspirators above are moving on; the fanatics dig in instead (Andaisin animates the cult's dead as new zombies). The PCs can mount <strong>multiple assaults</strong>: after a week Davaulus and Rolth abandon the cult; 2–3 weeks later Andaisin leads a ritual of self-sacrifice, burns her notes as the last cultist dies, and leaves (perhaps for Deathhead Vault, to face the PCs in Chapter 4).</p>")
  + B.s_skill("<p>Staffed by zealous "+act(A2["cultist"], "cultists of Urgathoa")+" (and the negotiable nosferatu "+act(A2["ramoska"], "Ramoska")+" in his lab). Stealth and speed matter — a roused temple masses at its choke points, and the G13 leukodaemon can be turned into anyone's problem.</p>"))

area2("G1", "Entry Hall", SR("G1", 119)
  + box("The scuffed stone walls of this chamber have been plastered over",
        "<p>Lurid murals coat the plastered walls: skeletons cavorting among the dead of a Korvosa lost to blood veil. Scythe-wielding painted skeletons flank every door — simple wood north, south, and west; to the east, great double doors painted as the opening pyramid of Castle Korvosa.</p>")
  + "<p>The lift from F4 descends into this dark chamber — the temple's threshold. The <strong>north door and the eastern double doors</strong> carry the cult's wards: the "+haz(H2["breathdoors"], "Death's Breath Doors")+" — touched by anyone not of Urgathoa's faith, the painted skeletons strike from the murals and vent <strong>ungol-dust gas</strong> through the room, and a linked <em>alarm</em> rings in G8 (alerting G8–G13). A 3-action channeled <em>heal</em> (10+ vitality damage) bathed over a door neutralizes its ward for 1 minute.</p>"
  + B.enc("The warded doors", "Hazard 8", "<p>"+haz(H2["breathdoors"], "Death's Breath Doors (8)")+" — scythes against everyone within 5 feet of any door, poison gas through all of G1, auto-reset in 1 minute. The G2 physicians step in 1 round after it triggers, once the gas thins.</p>",
     B.aside_token([haz(H2["breathdoors"], "Death's Breath Doors (Hazard 8)")])))

area2("G2", "Guard Post", SR("G2", 120)
  + box("A number of crates fill this room. A particularly large one",
        "<p>Emptied import crates crowd the room; a particularly large one has been dragged to the center as a table, ringed by four mismatched chairs and stools.</p>")
  + "<p>The temple's first watch. The guards ready themselves on a "+chk("type:perception|dc:16")+" to hear the lift descending in G1 — or instantly if the door-wards fire — and step into G1 one round after the gas disperses.</p>"
  + B.enc("Temple watch", encx([2, 2, 2, 2], 7),
     "<p>4 "+act(A2["physician"], "Queen's Physicians")+" (unmasked oddities are still cultists at heart) — they flank in eerie silence and fight to the death under a superior's eye. Trivial XP at this level alone; the danger is the <em>noise</em> they make.</p>",
     B.aside_token(["4× "+act(A2["physician"], "Queen's Physician (2)")])))

area2("G3", "Doctor Indoctrination", SR("G3", 120)
  + box("Cabinets and low benches fill this chamber. From pegs",
        "<p>Cabinets and low benches fill the room; from pegs opposite, the empty black eyes of two beaked plague masks glare, soulless and unblinking.</p>")
  + "<p>Where the cult swears in and outfits each new Queen's Physician: dark leather robes, high boots, wide hats, and solid canes — <strong>enough to outfit 20 doctors</strong> (~0.5 gp re-scaled per set; a ready-made disguise wardrobe, within the F6 ruse's limits). Significant noise here — like breaking the cabinet glass — brings the G7 cultists.</p>"
  + B.s_treasure("<p>The west cabinet's locked glass doors (Hardness 1, HP 1; brass lock "+chk("type:thievery|dc:29")+" — Davaulus has the key) protect delicate doctors' instruments, a medicine jar of <strong>23 black onyx gems</strong> (~5 gp each re-scaled; <em>animate dead</em> components), <strong>4 healer's kits</strong>, and four identical flasks: <strong>3 potions of cure moderate wounds</strong> (2nd-rank healing potions) and one <strong>cursed potion of poison</strong> — no way to tell which without magic. On the pegs: the <strong>two spare "+itm(I2["mask"], "plaguebringer's masks")+"</strong>.</p>"))

area2("G4", "The Princess's Bacchanal", SR("G4", 120)
  + box("Behind thick panes of glass, fragments and even whole bodies",
        "<p>Behind thick glass, fragments and whole bodies of the living dead line the walls and floor — rotting faces sneering, broken fingers clawing — not a mass grave but a stomach-churning attempt at <em>art</em>.</p>")
  + "<p>An Urgathoan memento mori — 'In the end may you be undead' — of dozens of twitching, ruined undead on display until their flesh flakes to dust. The glass is sturdier than it looks (Hardness 4, HP 10 per 5-foot section), <strong>but the PCs shouldn't know that</strong>: let them sweat. If broken open, the fragmentary horrors spill out — hideous, nauseating, and <strong>completely harmless</strong>. Under alert, the G7 skeletons and G9 zombies are posted here as guards.</p>")

area2("G5", "Operating Room", SR("G5", 120)
  + box("Eight unpleasant-looking beds stand here",
        "<p>Eight iron-framed operating beds threaded with manacles and stained straps — several occupied by bound, half-conscious patients — stand among tables of gore-soaked pans and cruel cutting instruments. A brown-crimson stain covers much of the east wall, as if a body's whole blood burst from it at once.</p>")
  + "<p>Here the priests test the diseases brewed in G13 — above all, variants of blood veil meant to break the Varisian immunity — under the direction of <strong>Rolth Lamm</strong>, whose work created the <strong>plague-zombie strain</strong>. Six 'patients' are strapped down: one dead (and highly contagious), two living victims fading in and out, and <strong>three dead men risen as plague zombies</strong>, kept for observation. Sturdy locked iron doors (Hardness 10, HP 60, "+chk("type:athletics|dc:28")+" / "+chk("type:thievery|dc:29")+") lead east to the cells (G6); <strong>every cultist in the complex carries the keys</strong>.</p>"
  + B.enc("Rolth's surgery", encx([8, 2, 2, 2, 2, 1, 1, 1], 7),
     "<p>"+act(A2["rolth"], "Rolth Lamm")+" (+ "+act(A2["davaulus"], "Davaulus")+", if he fled here), 2 "+act(A2["cultist"], "cultists")+", 2 "+act(A2["physician"], "Queen's Physicians")+", and the 3 released "+act(A2["pzombie"], "blood veil plague zombies")+". Rolth hangs back hurling spells, shrilly accusing the PCs of <strong>murdering his father Gaedren</strong> and promising their corpses 'unsettling and unsavory' second careers; below ~15 HP he Dimension Doors away to villain another day.</p>",
     B.aside_token([act(A2["rolth"], "Rolth Lamm (8)"), "2× "+act(A2["cultist"], "Cultist (2)"), "2× "+act(A2["physician"], "Physician (2)"), "3× "+act(A2["pzombie"], "Blood Veil Plague Zombie (1)")]))
  + SEC("<p><strong>The named prisoners.</strong> The two living victims are the cobbler <strong>Olena Hanch</strong> and the Sable Company hostler <strong>Dalvun Krand</strong> (unconscious, 0 HP). Cured, they testify: more prisoners are locked in G6; <strong>the priests of Urgathoa made the plague</strong>, in a laboratory east of here; and the doctors answer to <strong>two</strong> commanders — a beautiful high priestess who speaks of death as a gift, and a disturbing bald, pale, rodent-toothed man who berates them all as amateurs. <strong>Story award:</strong> rescue and heal both → <strong>600 XP</strong>; each counts toward the Survivor Count.</p>")
  + B.s_treasure("<p>Rolth's <strong>extensive blood-veil notes</strong> are here with him — the second of the <strong>three note-sets</strong> behind the cure (→ Chapter Conclusion). His gear: +1 dagger, fine mortician's tools, six black onyxes, a scroll of <em>teleport</em>, and a wand of <em>magic missile</em>.</p>"))

area2("G6", "Patient Cells", SR("G6", 122)
  + box("Iron doors with slotted windows, much like one might find",
        "<p>Slot-windowed iron doors, prison-like, line the chamber; faint bloodstains fleck the straw-strewn flagstones.</p>")
  + "<p>Eight cramped cells behind iron doors (Hardness 10, HP 60, "+chk("type:athletics|dc:28")+" / "+chk("type:thievery|dc:29")+" — or any cultist's keys). <strong>Five hold captive Varisians</strong> of all ages and walks, taken within the last week; many watched earlier prisoners hauled off to the experiments and not return. All are blood-veil immune — the trait that doomed them — and can tell the PCs the same things as Olena and Dalvun (G5).</p>"
  + B.s_treasure("<p><strong>Story award:</strong> free all the prisoners and lead them to safety → <strong>1,200 XP</strong>. <strong>Survivor Count:</strong> every prisoner rescued and healed counts as one life saved.</p>"))

area2("G7", "Cult Quarters", SR("G7", 122)
  + box("Black-sheeted cots fill this room; their satin coverings",
        "<p>Black-sheeted, satin-covered cots more funerary than restful fill the room; candle-lit skulls set into the walls glow like morbid jack-o'-lanterns.</p>")
  + "<p>The cult's barracks. When combat begins, the Urgathoans <strong>order their four skeletal servants into battle first</strong> (one still clutching a platter of goblets and Nidalese midnight wine); two cultists then close, one hangs back casting support, and the fourth <strong>runs to alert G8</strong>. Noise from G3 brings the physicians here to investigate.</p>"
  + B.enc("Off-duty cult", encx([2, 2, 2, 2, 2, 2, 2, -1, -1, -1, -1], 7),
     "<p>4 "+act(A2["cultist"], "cultists of Urgathoa")+", 3 unmasked "+act(A2["physician"], "Queen's Physicians")+", and 4 "+B.mon("skeleton-guard", "skeletal servants")+" who open the fight.</p>",
     B.aside_token(["4× "+act(A2["cultist"], "Cultist (2)"), "3× "+act(A2["physician"], "Physician (2)"), "4× "+B.mon("skeleton-guard", "Skeleton Guard (−1)")]))
  + B.s_treasure("<p>Ten minutes' search and "+chk("type:perception|dc:22")+" through the footlockers' sparse, disturbing effects: <strong>12 bottles of Nidalese midnight wine</strong> (~17 gp re-scaled the lot), a <strong>robe of bones</strong> still bearing a human-skeleton and a wolf-skeleton patch (tear one free to animate a "+B.mon("skeleton-guard", "human skeleton")+" or "+B.mon("wolf-skeleton", "wolf skeleton")+" under the wearer's command), a rune-etched <strong>onyx skull</strong> (~4 gp), and ~16 gp re-scaled in mixed coin.</p>"))

area2("G8", "The Blood Vats", SR("G8", 122)
  + box("The stinging scent of harsh chemicals chokes this high-ceilinged chamber",
        "<p>Three six-foot metal vats bubble under a web of catwalks ten feet up, venting a foul green-brown mist; circling the upper walls, a mosaic of white, black, and green stone shows a giant half-skeletal woman in black veils dancing through fields of the dead, undead, and dying.</p>",
        patch=[("ground 2 stretches", "ground stretches")])
  + "<p><strong>This room is the source of the plague.</strong> The three vats hold ~1,000 gallons each of viscous, concentrated liquid blood veil; <strong>any contact</strong> forces a "+chk("type:fortitude|dc:24")+" against infection. A cultist on the catwalk can dip her scythe as a single action — her next 1d4 hits expose their targets to blood veil. The door up to G11 opens off the catwalk (locked — Ramoska's key, or "+chk("type:thievery|dc:29")+" to pick, as the temple's other doors).</p>"
  + B.enc("Vat-tenders", encx([2, 2, 2, 2, 2, 2], 7),
     "<p>6 "+act(A2["cultist"], "cultists")+" tend the brew — on sighting intruders one hammers on G11's door (Ramoska ignores it), one runs to warn Andaisin (G14), one frees the G9 zombies, and the rest hold to the death. <strong>Under alert</strong> add "+act(A2["davaulus"], "Davaulus")+", "+act(A2["rolth"], "Rolth")+" on the catwalk, and all 5 "+act(A2["physician"], "physicians")+" — a brutal massed defense; thin the temple before it can muster here.</p>",
     B.aside_token(["6× "+act(A2["cultist"], "Cultist of Urgathoa (2)"), "alert: + "+act(A2["davaulus"], "Davaulus (9)"), "+ "+act(A2["rolth"], "Rolth (8)"), "+ 5× "+act(A2["physician"], "Physician (2)")]))
  + B.s_skill("<p><strong>Destroying the vats:</strong> smash one (Hardness 18, HP 72, BT 36) and its contents flood the lower floor — everyone standing there risks exposure, but the batch is ruined (inert after 1 hour). <em>Purify food and drink</em> works but slowly (a vat is ~133 cubic feet — about 2 minutes of repeated castings); a single <em>remove disease</em> cast <strong>on a vat</strong> (a counteract attempt against the brew's infection DC, above) neutralizes it outright. Reward clever alternatives.</p>")
  + B.s_treasure("<p><strong>Story award:</strong> destroy all three vats → <strong>2,400 XP</strong> (the cult would need weeks to rebuild its stock). <strong>Survivor Count: each destroyed vat saves 200 citizens.</strong></p>"))

area2("G9 & G10", "Storage Rooms", SR("G9–G10", 124)
  + box("Little more than barrels of water, kindling, and long stirring poles",
        "<p>Little here but water barrels, kindling, and long stirring poles.</p>")
  + "<p><strong>G9 (Storage):</strong> supplies for the vat-work — and 4 "+B.mon("zombie-shambler", "human zombies")+" standing in the dark, waiting to be needed. They attack any non-Urgathoan who enters; a G8 cultist releases them into a fight there.</p>"
  + B.enc("Stored dead", encx([-1, -1, -1, -1], 7),
     "<p>4 "+B.mon("zombie-shambler", "zombies")+" — negligible alone at this level; they matter as the G8 fight's second wave (or as G4's posted guards under alert).</p>",
     B.aside_token(["4× "+B.mon("zombie-shambler", "Human Zombie (−1)")]))
  + box("The southeastern corner of this otherwise empty room seems to be unfinished",
        "<p>The southeast corner of the otherwise empty room is unfinished, a mound of rubble heaped there.</p>")
  + "<p><strong>G10 (Unfinished Storeroom):</strong> the temple's expansion outpaced its plague — with the operation in full swing, the cultists never finished digging. Empty, dark, and a decent place to catch a breath between assaults.</p>")

area2("G11", "Arkminos's Laboratory", SR("G11", 124)
  + box("An elegant operating table dominates the center of this grim laboratory",
        "<p>An elegant, ogre-sized operating table — iron restraints, cranks and levers, a gore-crusted gutter — dominates the lab; the side tables' alchemical clutter looks centuries old: rusted tools, purpled glass, deep pools of ancient candle wax.</p>")
  + "<p>The nosferatu "+act(A2["ramoska"], "Ramoska Arkminos")+"'s personal laboratory, imported from beneath Castle Corvischoir in Ustalav. Strapped to the table, unconscious at 0 HP, lies "+B.cmon("Ruan Mirukova")+" — Deyanira's brother, <strong>very much alive</strong>. Having failed to infect the youth with strain after strain of blood veil, Ramoska is preparing a regimen of <em>other</em> virulent diseases — and means to try vampirism last. ("+chk("type:perception|dc:29")+" finds the secret door in the western wall, to G12.)</p>"
  + B.s_skill("<p><strong>The table is a torture device:</strong> three levers (each marked in Varisian — 'up' left, 'down' right) move its three crushing crossbeams an inch per slot, currently at the tenth of twenty slots; shifting one lever one slot takes 2 actions. Sliding <strong>left</strong> gradually frees Ruan; each slot <strong>right</strong> crushes him for @Damage[1d6[bludgeoning]] — at 0 HP, do the arithmetic before yanking levers.</p>")
  + SEC("<p><strong>Do not simply fight him.</strong> Ramoska is a level-15 foe far above the party and wants no part of the cult's cause — he says as much before anyone can swing, and leaves the PCs be if they leave him be. What he wants is to cure his own vampirism and finally die <em>as a man</em>. <strong>The bargains:</strong> he opens by offering to sell Ruan and leave for <strong>~200 gp re-scaled</strong>; he entertains counteroffers but accepts <strong>no less than ~100 gp</strong> in coin, magic items, or genuinely useful future favors. Alternatively he proposes a fetch: bring him the last unused <strong><em>death's head coffer</em></strong> from the inner sanctum (G14) — he explains how the coffers seeded the plague, never <em>why</em> he wants one — and Ruan is theirs; Andaisin, of course, will not simply hand it over. He also <strong>accepts surrender</strong> at any point if a fight goes badly for the PCs: the price of their lives is that same coffer (whether he then honors anything is yours to decide). Attacked, he chides, dominates, and disables rather than kills — and below ~40% HP he sighs, says the plague has run its course anyway, lets them have the lad, and Dimension-Steps/teleports out of the adventure.</p>")
  + B.enc("Ramoska Arkminos (only if forced)", encx([15], 7),
     "<p>"+act(A2["ramoska"], "Ramoska")+" — Drain Life, Contagion, caustic bombs, fast healing 5, nosferatu resilience. <strong>An almost-unwinnable straight fight at this level; the intended path is the bargain.</strong></p>",
     B.aside_token([act(A2["ramoska"], "Ramoska Arkminos (15)")]))
  + B.s_treasure("<p><strong>The lab:</strong> 6 "+B.isrd("acid-flask-lesser", "acid flasks")+", sealed tubes of distilled <strong>blood veil, filth fever, and red ache</strong> (handle with extreme care), ~50 gp re-scaled of alchemical and medical equipment — and <strong>Ramoska's notebooks of blood-veil observations</strong>, the third of the <strong>three note-sets</strong> behind the cure (→ Chapter Conclusion). <strong>Story award:</strong> free Ruan and reunite him with Deyanira → <strong>4,800 XP</strong>. Ruan (a gifted bard) is too weakened to help in any further temple fights; he wants only out.</p>"))

area2("G12", "Arkminos's Room", SR("G12", 127)
  + box("Several open trunks spill piles of books across this dusty room",
        "<p>Open trunks spill books across the dusty room; tomes old and older stand in orderly stacks and toppled heaps around an elegant black-canopied bed.</p>")
  + "<p>The sleepless nosferatu's leisure: ancient healing texts, legendary accounts of vampires, religious lore. One trunk is <strong>locked</strong> ("+chk("type:thievery|dc:29")+"; forcing it with "+chk("type:athletics|dc:28")+" destroys the contents). "+chk("type:perception|dc:20")+" reveals the 'bed' is a frame stretched with black satin over one of <strong>Arkminos's traveling coffins</strong> — and it is here he flees if reduced to 0 HP (a fact that matters enormously to anyone intent on truly destroying him).</p>"
  + B.s_treasure("<p>The locked trunk holds padded trays of <strong>150 elegant crystal vials</strong> of blood (32 empty; each full one sates a vampire for a day) — worth ~100 gp re-scaled if emptied — and, at the bottom, a small <strong>gold locket</strong> (~10 gp), its tiny portrait worn to an androgynous outline: the last trace of whoever Ramoska once loved, or was. The <strong>library</strong> is worth ~150 gp re-scaled in all, though many bindings are rotted and crumble unless handled with extreme delicacy.</p>"))

area2("G13", "Hall of Pestilence", SR("G13", 128)
  + box("The reek of burning wax wafts through this morbid chamber",
        "<p>Misshapen candles reek through the chamber; alcoves hold workspaces of foul liquids, insidious diagrams, and cages of whimpering rodents. At the center, four tall glass vats of bubbling emerald fluid tint the light a noxious green — and in each suspension floats a malformed thing of half-formed muscle, part human, part angel, part horse, with a dead equine skull. Three hang motionless; the fourth <em>twitches</em>.</p>")
  + "<p>The cult's disease-forge, and the defiled approach to the Inner Sanctum — the open stone double doors east lead down a 100-foot sloping hall to G14. The four tubes are <strong>magical prisons</strong>, Queen Ileosa's gifts to Andaisin: each held a <strong>leukodaemon</strong>, whose imprisoned infectious aura force-grew the plagues brewed here. Three daemons have already been <em>sacrificed</em> into ever-deadlier strains of blood veil; the fourth waits its turn (it goes into the vat the day the cult cracks the Varisian immunity).</p>"
  + B.s_skill("<p><strong>The prison is fragile:</strong> the inward-focused <em>magic circle</em> holds only while the glass does (Hardness 1, <strong>HP 2</strong>) — one solid blow shatters it, and the enraged daemon bursts free a round later. If one of the two cultists here falls, <strong>the other smashes the vat deliberately</strong>, praying the daemon eats the PCs first. It won't be choosy: the freed leukodaemon treats <em>every</em> humanoid as prey — canny PCs can lure it into the cult's massed defenses, or even into Lady Andaisin's sanctum.</p>")
  + B.enc("Sanctum guards", encx([2, 2], 7),
     "<p>2 "+act(A2["cultist"], "cultists")+" scrub the vats or pray on mats of woven human hair (one bears Andaisin's <em>status</em> — her early warning). <strong>Under alert, 8 cultists</strong> mass here instead — "+encx([2]*8, 7)+".</p>",
     B.aside_token(["2× "+act(A2["cultist"], "Cultist of Urgathoa (2)"), "(alert: 8×)"]))
  + B.enc("The caged leukodaemon (if freed)", encx([9], 7),
     "<p>"+B.mon("leukodaemon", "Leukodaemon")+" (9) — a Severe encounter by itself, hostile to <em>everyone</em>. The best fight is the one where it does the cult's dying for them.</p>",
     B.aside_token([B.mon("leukodaemon", "Leukodaemon (9)")])))

area2("G14", "The Inner Sanctum", SR("G14", 129)
  + boxm(("The long hall opens into a circular chamber rising into a high dome",
          "<p>The hall opens into a domed circular chamber ringed by seven alcoved basins, each brimming with a different liquid — blood, bile, milk, fluids worse — their reeks mingling into a noxious, eye-watering bouquet; small skull-carved metal boxes lie empty around their feet.</p>"),
         ("At the room's center, rising from a wide pool",
          "<p>From a wide pool of crystalline water at the center rises a golden statue both erotic and horrifying: a beautiful nude woman above the waist, bare skeleton below.</p>"))
  + "<p><strong>The seven scourges.</strong> The basins hold the seven fluids said to leak eternally from the Pallid Princess's necrotic body — bile, blood, milk, phlegm, pus, sweat, and tears — spontaneously generated foci of her worship, and here each has been used as a <strong>medium for blood veil</strong>. Touching any of the fluids forces a "+chk("type:fortitude|dc:30")+"; a creature that fails contracts blood veil with <strong>no incubation</strong>, taking the first stage's damage immediately. The empty skull-boxes are <strong>two dozen spent <em>death's head coffers</em></strong> — each once held some contaminant (diseased rats, blood, plague-victim flesh); the one that carried <strong>Vorel's phage</strong> became blood veil itself. <strong>One unused coffer</strong> remains among them — the item Ramoska covets (G11).</p>"
  + "<p><strong>The statue</strong> of Urgathoa is the focus of an <em>unhallow</em> effect (40-foot radius) that grants <strong>worshipers of Urgathoa <em>freedom of movement</em></strong> while within it — Andaisin and her guards cannot be grabbed, restrained, or slowed there; plan accordingly.</p>"
  + "<p>"+act(A2["andaisin"], "Lady Andaisin")+" prays here. Given warning she spends rounds buffing (air walk, magic vestment, barkskin, shield of faith), then returns serenely to her contemplation among her four bodyguards; if no enemy arrives within minutes, she sweeps the temple herself. As the PCs enter she greets them with an icy smile:</p>"
  + box("'And so you have found your way to me, hopeful heroes",
        "<p>She names herself the architect of the city's death — what they call blood veil she calls the Pallid Princess's gentle kiss — and invites them to choose among the seven scourges: drinkers she will merely <em>cripple</em>, to enjoy the goddess quickening in their flesh; abstainers are fools unfit for the divine gift, though prostration will at least buy a swifter end than the one their lovely queen commissioned.</p>")
  + B.enc("BOSS — Lady Andaisin & her guardians", encx([9] + [B.cmon_lvl("Juju Zombie")] * 4, 7),
     "<p>"+act(A2["andaisin"], "Andaisin")+" air-walks aloft and rains Slay Living / Greater Command / Harm before dropping into scythe range (mist-and-heal below ~30 HP), while her 4 "+B.cmon("Juju Zombie", "juju zombies")+" (fast, tough, unslowed) hold the floor. She taunts throughout, promising to cripple one or two PCs to savor her plague later.</p>",
     B.aside_token([act(A2["andaisin"], "Lady Andaisin (9)"), "4× "+B.cmon("Juju Zombie", "Juju Zombie (2)")]))
  + B.enc("CLIMAX — Andaisin, Daughter of Urgathoa", encx([8], 7),
     "<p>Andaisin's arrogance is <strong>not</strong> delusion: Urgathoa has marked her for sainthood. The round after she falls, her corpse crackles aloft, flesh erupting in boils as the goddess's humors congeal a new body — she is reborn as "+act(A2["andaisin_t"], "a Daughter of Urgathoa")+", a Large undead horror (reach claws, devouring maw, pestilent aura, plague-bearing wounds) bent wholly on revenge. Her gear and every spell effect drop with her old body. <strong>The true climax — and end — of Chapter 2.</strong> If the PCs flee mid-transformation, the risen saint may abandon the temple for Deathhead Vault — and Chapter 4.</p>",
     B.aside_token([act(A2["andaisin_t"], "Andaisin, Daughter of Urgathoa (8)")]))
  + B.s_treasure("<p><strong>The statue's secret:</strong> "+chk("type:perception|dc:26")+" while examining the statue finds a concealed compartment at its base — the chapter's richest parcel: a <strong>wand of <em>cure serious wounds</em></strong> (37 charges; as a 3rd-rank <em>heal</em> wand, treat as a limited-charge healing reserve), a <strong>wand of <em>remove disease</em></strong> (8 charges — priceless this month), a <strong>scroll of <em>restoration</em></strong>, a <strong>scroll of <em>raise dead</em></strong>, <strong>3 blocks of incense of meditation</strong>, two silver-encased hand-of-bone <strong>candelabras</strong> (~15 gp each re-scaled), and exotic ritual incense (~45 gp re-scaled). Andaisin's body yields her <strong>+2 vicious scythe</strong>, +2 breastplate, belt of mighty constitution, cloak of resistance, headband of inspired wisdom, an onyx unholy symbol (~20 gp), and the final usable <strong>death's head coffer</strong> (the plague-engine: Ramoska's price, or a thing to destroy).</p>")
  + B.s_conv("<p>With Andaisin destroyed and the vats and coffer ended, the manufactured plague's <strong>source</strong> is broken — but per the persistent-plague overlay (Conversion Guide → Blood Veil), the cure only <em>suppresses</em>, and the Epidemic Clock continues until Ileosa falls in Chapter 6.</p>"))

PG("Chapter Conclusion", SR("Chapter Conclusion", 132)
  + B.s_milestone("<p><strong>Chapter Conclusion.</strong> The Hospice and Temple fall, Davaulus and Andaisin are dead (or fled), and the plague's unnaturally swift, random spread <strong>ends</strong> — though the disease itself remains at large until cured or burned out. The PCs should be 8th level. The victory is bittersweet — the city is scarred, the Gray Maidens entrenched, and Old Korvosa sealed under quarantine.</p>")
  + SEC("<p><strong>A Conspiracy Revealed.</strong> Word that the Queen's Physicians were corrupt spreads fast — dangerous knowledge with no hard evidence behind it. The crown's official line: the charming doctor <strong>duped</strong> Her Majesty; the hospice's Gray Maidens claim ignorance of the chambers below; and if Davaulus survived the PCs, he is <strong>publicly executed</strong> (or branded a traitor in absentia). Lacking proof, most Korvosans can't believe their queen — vain and unpleasant as she is — capable of such evil; they're simply grateful the scourge has passed, and the city is too wounded to contemplate rebellion. <em>But unrest grows:</em> rumors of royal involvement keep spreading — and so do the queen's resources, with Gray Maidens thicker on every street and the laws turning oppressive. The PCs keep their allies (Cressida, Ishani, Grau, Vencarlo, Tayce), yet should feel distinctly less welcome by the week: <strong>Ileosa now knows, beyond doubt, that they are her enemies.</strong></p>")
  + SEC("<p><strong>Into Chapter 3.</strong> The crafted cure <strong>suppresses</strong> rather than eradicates (persistent-plague overlay): set the Epidemic Clock from the Final Survivor Count tally. The quarantine of Old Korvosa and the captured seneschal <strong>Neolandus</strong> (held by the Arkonas) launch 'Escape from Old Korvosa.' If the PCs rode off after Davaulus's fictional wererat cabal, the Red Mantis now hunt them there.</p>")
  + B.s_conv("<p><strong>Threads forward:</strong> the persistent plague + Epidemic Clock · the Gray Maidens (now a standing enemy) · Rolth's vendetta and his immunity research · Ramoska loose with his bargain (or destroyed at his coffin) · Zenobia the penanggalen (Ch.4) · Trinia &amp; Vencarlo · the Arkonas + Neolandus → Chapter 3.</p>"))

PG("Curing Blood Veil", SR("Curing Blood Veil", 133)
  + "<p>The cure lies in the research of three demented minds — <strong>Davaulus (F8)</strong>, <strong>Rolth (G5)</strong>, and <strong>Ramoska (G11)</strong> — each of whom independently found that ~1 in 20 Varisians is immune, none of whom deduced why. With at least one note-set in hand, an alchemist or canny caster can engineer the cure:</p>"
  + B.s_skill("<ul><li><strong>1 note-set:</strong> "+chk("type:crafting|dc:30")+" and <strong>1 week</strong> of work.</li>"
    "<li><strong>2 note-sets:</strong> "+chk("type:crafting|dc:25")+" and <strong>1d4+1 days</strong>.</li>"
    "<li><strong>All 3:</strong> "+chk("type:crafting|dc:20")+" and just <strong>1 day</strong>.</li></ul>"
    "<p><strong>Brewing doses:</strong> with alchemical crafting (or Brew Potion-style magic), ~4 doses per day at ~20 gp re-scaled per day of work, or single doses at "+chk("type:crafting|dc:20")+" for ~10 gp each.</p>")
  + "<p><strong>The mercy in its design:</strong> the disease's supernatural origin is its undoing — for <strong>1 week</strong> after taking the cure, a cured person <em>spreads the cure</em> by contact exactly as blood veil itself spread. Combined with continued <em>lesser restoration</em> and <em>remove disease</em> work, blood veil loses ground daily and is defeated within <strong>1d4+1 weeks</strong>.</p>"
  + SEC("<p><strong>The Kasanda secret (GM only — hold it back).</strong> The original strain, <strong>Vorel's phage</strong>, was infused with spiritual energy: in 4644 <span style='white-space:nowrap'>AR</span>, <strong>Vorel Foxglove</strong> botched his lich apotheosis when his wife <strong>Kasanda</strong> disrupted the final ritual, and a fragment of her spirit suffused the resulting tainted fungus. The immune Varisians are, in effect, being saved <em>by Kasanda herself</em> — her influence is the flaw that makes a cure possible at all. (Had the three researchers ever compared notes, they'd have engineered the flaw out.) Reveal this only to <em>divination / commune / legend lore</em>-grade magic; it is flavor for connoisseurs of Foxglove family horror, not a required clue.</p>")
  + B.s_treasure("<p><strong>Survivor Count — cure timing:</strong> a cure within a <strong>month</strong> saves <strong>100</strong> citizens; within a <strong>week</strong>, <strong>500</strong>; within a <strong>day</strong>, <strong>1,000</strong>.</p>"))

PG("Final Survivor Count", SR("Final Survivor Count", 134)
  + "<p>After Andaisin's defeat the plague slows but doesn't halt: <strong>1d6 citizens die per day</strong> until the cure lands or the disease burns out months later (worst case: <strong>5,000 dead</strong>). When one of those endpoints arrives, total the lives saved minus those killed or allowed to die. The chapter's inputs:</p>"
  + B.s_skill("<table><thead><tr><th>Source</th><th>Lives</th></tr></thead><tbody>"
    "<tr><td>Mission 1 — every extra day spent on the <em>Direption</em></td><td><strong>−10</strong>/day</td></tr>"
    "<tr><td>Mission 2 — stop Girrigz's war (sparing the coerced wererats)</td><td><strong>400</strong></td></tr>"
    "<tr><td>Mission 3 — shut down the false cure</td><td><strong>700</strong></td></tr>"
    "<tr><td>Mission 4 — clear Racker's Alley dumping ground</td><td><strong>200</strong></td></tr>"
    "<tr><td>Mission 5 — destroy the manor zombies / stop Jolistina</td><td><strong>500</strong></td></tr>"
    "<tr><td>F2 sick ward — each patient who survives and is cured</td><td><strong>1</strong> each</td></tr>"
    "<tr><td>F7 / G5 / G6 — each prisoner rescued and healed</td><td><strong>1</strong> each</td></tr>"
    "<tr><td>G8 — each blood-veil vat destroyed</td><td><strong>200</strong> each</td></tr>"
    "<tr><td>Cure within a month / a week / a day</td><td><strong>100 / 500 / 1,000</strong></td></tr>"
    "</tbody></table>")
  + "<p>The rewards below are <strong>cumulative</strong> (save 2,801+, get all four); only the XP awards aren't.</p>"
  + "<ul><li><strong>700 or fewer — Family Friends:</strong> Tayce Soldado organizes the settled Varisians' thanks: a feast at her home and modest gifts — embroidered scarves, jewelry, illustrated harrow decks, fine clothing — totaling ~25 gp re-scaled per PC. <strong>2,400 XP.</strong></li>"
    "<li><strong>701–1,900 — Good Neighbors:</strong> dozens of families recognize the PCs; each PC gains a <strong>favor</strong> from a skilled artisan or artist — a gift worth up to ~100 gp re-scaled, a safe place to lie low for a night, research help (+1 circumstance bonus to the next five relevant Lore/Recall Knowledge checks with the helper's aid), or similar. <strong>3,200 XP.</strong></li>"
    "<li><strong>1,901–2,800 — Local Heroes:</strong> Kroft personally thanks the PCs, finally and officially <strong>deputizes</strong> them into the Korvosan Guard, and opens Citadel Volshyenek's armory: each PC selects gear worth up to ~250 gp re-scaled (magic arms and armor included). <strong>4,800 XP.</strong> At this tier and above the PCs have Queen Ileosa's <em>full attention</em> — chance brushes with Gray Maidens and Red Mantis agents may rise.</li>"
    "<li><strong>2,801 or more — City Saviors:</strong> the whole city knows them: +1 circumstance bonus to Deception, Diplomacy, and Intimidation against Korvosan citizens. Ileosa is <strong>forced to publicly honor them</strong> — a short, grudging speech ("+chk("type:perception|dc:20")+" reads how much it costs her) and a <strong>writ worth ~500 gp re-scaled</strong> per PC, good for any purchase within the walls. (If they've been loud about her involvement, Sabina presents the award instead, the queen pleading exhaustion.) <strong>6,400 XP.</strong></li></ul>"
  + B.s_conv("<p>Feed the final tally into the persistent-plague overlay: the Survivor Count sets the Epidemic Clock's starting state for Chapter 3 (Conversion Guide → <em>Blood Veil &amp; the Epidemic Clock</em>).</p>"))

# =====================================================================
# PREPARED SCENES — Racooze battlemap geometry + keyed pins & staged tokens.
# Coordinates come from the keying pass (research/scene_keys.json; map-local
# grid squares — scene px = origin + g*100, tokens snapped to whole squares).
# Geometry (walls/doors/tiles/lights/thumb) injects from the GM's locally
# installed Racooze module via B.racooze_scene; tokens all ship hidden=True.
# =====================================================================
import html as _html, json as _json, re as _rx

_sg = B._idgen(882001)            # scene-embedded ids: a SEPARATE deterministic
def snid(): return next(_sg)      # stream so nid()/sid() and every doc id downstream stay put

def scn(_id, label): return f"@UUID[Compendium.{MODID}.cotct-scenes.Scene.{_id}]{{{label}}}"

SCENE_FOLDER2 = "ch2SceneFolder01"   # created by build_pilot.py under the shared scene root
MM = "icons/svg/mystery-man.svg"

# keyed actor name -> (actorId, token grid width). Literal ids are the stable
# community-original actors materialized into the packs by build_community.py /
# import_community.py; the rest are this chapter's own A2/H2 docs.
_TOK = {
    "Silt Eel": (A2["silteel"], 1),            "Skinshear": ("RiqACmnzGmuRaDxP", 1),
    "Yvicca": (A2["yvicca"], 1),               "Wererat": ("q2eM3ScJs09UunF7", 1),
    "Dire Rat": ("lFwjg3rcczCkWeMD", 1),       "Shrieker": ("GoOuyKBGBocKnq7D", 1),
    "Otyugh": ("W1srRPmlZZnVFfYH", 2),         "Rat Swarm": ("1VNsOGy3bdFp0YB5", 2),
    "Girrigz Ripperclaws": (A2["girrigz"], 1), "Vampire Spawn": ("peaN29LKkR2MU7JL", 1),
    "Vendra Loaggri": (A2["vendra"], 1),       "Lavender Thug": (A2["lavthug"], 1),
    "Human Zombie": ("SoLzM2IW3fXcISl0", 1),   "Jolistina Susperio": (A2["jolistina"], 1),
    "Ausio Carowyn": (A2["ausio"], 1),         "Bhrunlida Torthus": (A2["bhrunlida"], 1),
    "Gray Maiden Foot Soldier": (A2["graymaiden"], 1),
    "Queen's Physician": (A2["physician"], 1), "Reiner Davaulus": (A2["davaulus"], 1),
    "Death's Breath Doors (G1)": (H2["breathdoors"], 1),
    "Rolth Lamm": (A2["rolth"], 1),            "Cultist of Urgathoa": (A2["cultist"], 1),
    "Blood Veil Plague Zombie": (A2["pzombie"], 1),
    "Human Skeleton": ("4DchLWBlDGaiQe3P", 1), "Ramoska Arkminos": (A2["ramoska"], 1),
    "Ruan Mirukova": ("u0KhFUBJOePZTfIy", 1),  "Leukodaemon": ("gdS28JkSPpkX5gBa", 2),
    "Lady Andaisin": (A2["andaisin"], 1),      "Juju Zombie": ("2rCxh8CXwO9X7co5", 1),
    "Andaisin, Daughter of Urgathoa": (A2["andaisin_t"], 2),  # hidden-finale add (lg 2x2)
}

_NAV = {"The Direption": "Direption", "Wererat Sewer Den": "Sewer Den",
        "Lavender and Vendra's Apartment": "Lavender",
        "Racker's Alley and Giotorri's Toys": "Racker's Alley",
        "Carowyn Manor": "Carowyn Manor",
        "Hospice of the Blessed Maiden": "Hospice",
        "Temple of Urgathoa": "Temple of Urgathoa"}
_SORT = {"The Direption": 100000, "Wererat Sewer Den": 200000,        # mission order
         "Lavender and Vendra's Apartment": 300000,
         "Racker's Alley and Giotorri's Toys": 400000, "Carowyn Manor": 500000,
         "Hospice of the Blessed Maiden": 600000, "Temple of Urgathoa": 700000}

_PAGE_BY_NAME = {_html.unescape(p["name"]): p["_id"] for p in pages}
def _page_for(page_name, code):
    n = _html.unescape(page_name)
    if n in _PAGE_BY_NAME:
        return _PAGE_BY_NAME[n]
    hit = next((pid for nm, pid in _PAGE_BY_NAME.items()
                if nm.startswith(code + ".") or nm.startswith(code + " ")), None)
    print(f"  [scene] pageName {page_name!r} not found -> "
          + (f"area-code fallback used for pin {code}" if hit else f"pin {code} DROPPED"))
    return hit

_SK_PATH = B.ROOT.parent / "research" / "scene_keys.json"
_SCN_KEYS = ([e for e in _json.loads(_SK_PATH.read_text(encoding="utf-8"))
              if e.get("chapter") == "ch2"] if _SK_PATH.exists() else [])
if not _SCN_KEYS:
    print("  [scene] research/scene_keys.json absent -> Ch.2 prepared scenes skipped")

scenes2 = []
for _e in _SCN_KEYS:
    _rn, _dn = _e["scene"], _e["displayName"]
    _ox, _oy = B.scene_origin(_rn)
    _notes = []
    for _n in _e["notes"]:
        _pid = _page_for(_n["pageName"], _n["code"])
        if _pid:
            _notes.append(B.note(snid(), JID2, _pid, _n["label"],
                                 int(_ox + _n["gx"] * 100), int(_oy + _n["gy"] * 100)))
    _toks = []
    def _stage(actor, name, gx, gy, disp):
        _aid, _w = _TOK[actor]
        _toks.append(B.token(snid(), _aid, name, _ox + int(gx) * 100, _oy + int(gy) * 100,
                             B.token_art(actor) or MM, disposition=disp, hidden=True,
                             width=_w, height=_w))
    for _t in _e["tokens"]:
        _stage(_t["actor"], _t["name"], _t["gx"], _t["gy"], _t.get("disp", -1))
    if _rn == "Temple of Urgathoa":
        # hidden finale (keying note's option taken): the risen saint pre-placed
        # at the G14 statue pool, revealed the round after Lady Andaisin falls
        _stage("Andaisin, Daughter of Urgathoa", "Andaisin, Daughter of Urgathoa", 45, 8, -1)
    _sc = B.racooze_scene(_rn, _dn, SCENE_FOLDER2, _notes, _toks,
                          navName=_NAV.get(_rn), sort=_SORT.get(_rn, 0))
    B.write("scenes", "02-" + _rx.sub(r"[^a-z0-9]+", "-", _dn.lower()).strip("-"),
            copy.deepcopy(_sc))
    scenes2.append((_dn, len(_notes), len(_toks)))

# ---- "Prepared Scenes" journal page: links + compact GM staging digests ----
_SID = {k: B.scene_id(k) for k in _NAV}
def _sl(rn, label): return scn(_SID[rn], label)

PG("Prepared Scenes",
  B.s_conv("<p>Seven prepared scenes ship with this chapter, built on <strong>Racooze's CotCT Battlemaps</strong> geometry — his walls, doors, floor art, and lighting inject at build time from your locally installed copy of his free module (without it the scenes build as wall-less placeholder grids; nothing of his is redistributed). Every map pin opens this journal's matching area page, and <strong>every staged token starts hidden</strong> — reveal each group as its area is entered. Dispositions follow the keying pass: hostile by default, neutral/friendly where the text stages a social encounter.</p>")

  + "<p>"+_sl("The Direption", "The Wreck of the Direption")+" <em>(Mission 1)</em></p>"
  + "<ul>"
    "<li><strong>Layout (one 43×18 underwater map):</strong> the bow (A1) lies map-west of the big rock the hull split over; the stern sits east of it — A2 shattered hold, A3 crew quarters, A4 captain's cabin in the far northeast.</li>"
    "<li><strong>Staging:</strong> 6 silt eels nest in A1 (wounded eels flee deeper into the bow and there fight to the death); <strong>Skinshear</strong> circles A2 and butts the A3 door to warn Yvicca before attacking; <strong>Yvicca</strong> lairs in A3 among the chummed hammocks and joins the A2 fight pre-buffed. A4 holds only the Vindmel corpse and the sealed footlocker — props, no tokens; its door is swollen shut.</li>"
    "<li><strong>GM flags:</strong> the whole site is underwater — apply the PF2e aquatic-combat penalties; a party without water breathing / freedom of movement fights at a real disadvantage. Skinshear is staged 1×1 (his actor is Medium despite the 'unusually large shark' flavor).</li>"
    "</ul>"

  + "<p>"+_sl("Wererat Sewer Den", "Wererat Sewer Den")+" <em>(Mission 2)</em></p>"
  + "<ul>"
    "<li><strong>Region guide (20×14):</strong> B5 bone cave across the top · B2 west fungus cave (the <strong>shrieker</strong> hazard token sits at its south mushroom pool) · B3 central bonfire cave · B6 northeast crate den · B1 the channel fork at the southwest · B4 the channel stretch penned between the two rusty grates, where the <strong>otyugh</strong> (2×2) sleeps beside its filth clot.</li>"
    "<li><strong>Alarm web:</strong> the shrieker screeches unless intruders immediately move north past the central pillar — summoning the B3 wererats and the B5 rat swarm (the dire rats are too lazy) and waking the otyugh. Fighting in B3, or the otyugh's release, brings <strong>Girrigz</strong> (staged unwarned in B6 over his map) pre-buffed in dire-rat form through the B3 northeast squeeze-crack.</li>"
    "<li><strong>GM flags:</strong> the otyugh can be bargained into helping — flip its disposition if so. Every wererat but Girrigz is coerced kin: scattering the band without killing them saves 400 citizens. Sewage-flow squares are slick (B2/B3 west edges and all channel floors). Not staged: Eries Yelloweyes (mission-giver, met in the city).</li>"
    "</ul>"

  + "<p>"+_sl("Lavender and Vendra's Apartment", "Lavender &amp; Vendra's Apartment")+" <em>(Mission 3)</em></p>"
  + "<ul>"
    "<li><strong>Layout (17×20):</strong> top building = the C1 shop; bottom = two mirrored apartments — C2 (west, Vendra's) and C3 (east, the boarded-up liniment lab with the oar-in-tub mixer); the corner-hinged secret door sits in their shared wall.</li>"
    "<li><strong>Day staging (default):</strong> Vendra works the crowd mid-shop with two sap-armed thugs by the window and the counter; one more thug works the C3 tub. C2 is locked and empty by day.</li>"
    "<li><strong>Night variant (not staged):</strong> no crowd and fewer guards in C1; Vendra and two thugs brew in C3 (50% she is instead asleep in C2); the thugs haul river-water barrels in by night — the easiest evidence to tail.</li>"
    "<li><strong>GM flags:</strong> the mission resolves by exposure, not combat (full XP for foes not fought) — treat the tokens as neutral until Vendra is cornered; she knifes a PC and bolts toward C2. Not staged (props/social): the two shop-girls, the planted shill Solt Carmino, the customer queue.</li>"
    "</ul>"

  + "<p>"+_sl("Racker's Alley and Giotorri's Toys", "Racker's Alley &amp; Giotorri's Toys")+" <em>(Mission 4)</em></p>"
  + "<ul>"
    "<li><strong>Layout (17×20):</strong> D3 = the toy showroom (north room); D2 = the workshop (south room — the toymaker's punctured corpse at the workbench is a prop; the trap door hugs the <strong>east</strong> wall); D1 = the bent, shadowed alley along the west side, its corpse pile heaped against D2's wooden wall around the 10-ft hole.</li>"
    "<li><strong>Day staging (default):</strong> all four vampire spawn cluster beside the D2 trap door — stand-ins for their soil coffins in the undrawn crawl space below. Keep them hidden until the trap door opens or noise wakes them (asleep: −10 Perception; killing one wakes the rest; the crawl space is difficult terrain for Medium creatures).</li>"
    "<li><strong>Night variant:</strong> move one spawn to the D1 rooftop (20 ft up, −2 to spot from the alley floor); it shrieks when anyone touches the bodies and its three companions arrive from D2 in 1d3 rounds.</li>"
    "<li><strong>GM flags:</strong> contact with the plague-dead exposes to Blood Veil. The tile shows alley mouths both north and south, but play D1 as the journal's shadowed dead-end — constant shadow keeps the spawns' sunlight weakness a tactical prize, not a default.</li>"
    "</ul>"

  + "<p>"+_sl("Carowyn Manor", "Carowyn Manor")+" <em>(Mission 5)</em></p>"
  + "<ul>"
    "<li><strong>Canvas regions:</strong> LEFT copy = ground floor (E1a–E1e) · RIGHT copy (map-local x &gt; 24) = second floor (E2a/E2b and the gallery stairs) · the small bottom-left tile (y &gt; 26) = the wine cellar ('E2c' is a coined code — the AP gives the cellar no sub-letter, so its pin opens the E2 page).</li>"
    "<li><strong>Zombie math is exact (21 staged):</strong> 6 dancers (E1a) + 3 den (E1b) + 4 diners (E1c — deliberately ON the chair squares; each spends an action extricating) + 1 harpist (E1d) + 2 carvers (E1e) + 3 critics (E2a) + 2 bedroom (E2b). The <strong>7 uncontrolled</strong> (attack everyone; Jolistina avoids their rooms) are the E1b trio, E1e pair, and E2b pair — same actor, a GM-side distinction.</li>"
    "<li><strong>Staging:</strong> Jolistina starts at her gallery / stair-head final-stand spot but fights a manor-spanning cat-and-mouse — move her freely between ambushes. Ausio (friendly) sits at the cellar's southeast corner, standing in for his undrawn locked studio. The 'E' getting-in pin marks the west approach — the book never says which door is the mahogany front door.</li>"
    "<li><strong>Not staged:</strong> Ruan Mirukova (<em>deliberately</em> — his absence from the gallery dead is the clue; he is staged at Temple G11), the dozens of posed masquerade corpses (props), and Deyanira (quest-giver, off-site).</li>"
    "</ul>"

  + "<p>"+_sl("Hospice of the Blessed Maiden", "Hospice of the Blessed Maiden")+" <em>(Part 3)</em></p>"
  + "<ul>"
    "<li><strong>Canvas regions:</strong> LEFT copy = ground floor (F1–F4) · MIDDLE copy = the same floor under the F5 <strong>catwalk overlay</strong> (the black rectangle is open air over the loading dock) · RIGHT strip = the second-floor offices (F6–F8; playable rooms ≈ x 50–59). Ground occupants stage on the left copy, the catwalk pair on the middle, the F6–F8 staff on the right.</li>"
    "<li><strong>Staging:</strong> Bhrunlida is NEUTRAL behind the F1 desk (a hired charlatan — story award for not attacking her). Six Gray Maidens in all: 2 in the ward (F4 door + stairs), 2 on the catwalks, 2 at the F6 hall — matching the disguise-ruse shift limits. Davaulus stands by his F8 desk; <strong>on alarm he turns invisible and runs for the F4 lift</strong>.</li>"
    "<li><strong>Honest calls:</strong> F4's rope-winch capstan = the concealed cargo lift (moderate confidence — no other candidate room exists). The F7/F8 dividing wall reads faint on the tile; trust the pins.</li>"
    "<li><strong>GM flags:</strong> the default posture is non-hostile cover — physicians fight only if attacked, if the cult is named, or if anyone enters F4; dispositions are hostile for staging convenience, so run the social layer first. Not staged: the 60+ cot patients, F1's six waiting sick, and the 15 strapped Varisians (the drawn cots and beds are them).</li>"
    "</ul>"

  + "<p>"+_sl("Temple of Urgathoa", "Temple of Urgathoa")+" <em>(Part 3 finale)</em></p>"
  + "<ul>"
    "<li><strong>Layout (one 54×23 map):</strong> the F4 lift arrives in G1's west alcove; G13's stone doors open onto the 100-ft sloping hall east to the G14 rotunda. <strong>G1 and G9–G12 are dark</strong>; the rest is lit.</li>"
    "<li><strong>Honest caveat:</strong> the fan map flips some of the book's directions — the G5/G7 assignment here (G5 = south strap-cot hall, G7 = north satin-cot room) is a judgment call, and G3 was identified by elimination. If you prefer the book's literal reading, swap the G5/G7 pins and their token groups wholesale.</li>"
    "<li><strong>Staging:</strong> ONE Death's Breath Doors hazard actor wards TWO doors — a token on G1's north door and one on its east double doors. Headcounts match the alert text: 14 cultists (4 G7 + 2 G5 + 6 G8 vat-tenders + 2 G13) and 9 physicians staged per room text (4 G2 + 2 G5 + 3 G7; the alert page's '5 active' is a redeployment count, not a contradiction). Ramoska is NEUTRAL (a level-15 foe; the intended path is the bargain for Ruan) and Ruan FRIENDLY — unconscious at 0 HP <em>on</em> the operating table, crushing levers at slot 10 of 20. A few G5/G7 tokens sit on cot edges by necessity — nudge freely.</li>"
    "<li><strong>Hidden finales:</strong> the caged <strong>leukodaemon</strong> (2×2) sits on the northwest glass tube — hostile to <em>everyone</em> once the tube (Hardness 1, HP 2) breaks; which of the four tubes holds the live daemon is your choice. <strong>Andaisin, Daughter of Urgathoa</strong> is pre-placed hidden at the G14 statue pool: reveal her the round after Lady Andaisin falls.</li>"
    "<li><strong>Not staged:</strong> alert-posture redeployments (cultists massing at G8/G13, the G7 skeletons + G9 zombies posting to G4, Gray Maidens covering G1) — move the standing tokens instead; Davaulus (his default station is hospice F8 — not duplicated here); the wolf skeleton (item-summoned from the G7 robe); G5's named prisoners and G6's five Varisian captives (innocents — the drawn beds and cells are them).</li>"
    "</ul>", level=2)

journal = B.journal_entry(JID2, "2. Seven Days to the Grave", pages, folder=ADV_FOLDER)
B.write("journals", "02-seven-days-to-the-grave", copy.deepcopy(journal), embed_pages=True)

print(f"Chapter 2 built: {len(folders)} folders, {len(actors)} actors, {len(hazards)} hazards, "
      f"1 journal ({len(pages)} pages), {len(scenes2)} scenes "
      f"({sum(n for _, n, _ in scenes2)} pins / {sum(t for _, _, t in scenes2)} tokens).")
for _dn, _np, _nt in scenes2:
    print(f"  [scene] {_dn}: {_np} pins, {_nt} tokens")
