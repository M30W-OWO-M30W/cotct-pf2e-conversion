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

MODID = "cotct-pf2e-conversion"
# ---- shared cross-chapter root folder ids (must match build_pilot.py) ----
ACTOR_ROOT, ITEM_ROOT, ADV_FOLDER = "cotctActorRoot01", "cotctItemRoot001", "cotctAdvFolder01"

# ---- stable literal ids (16 chars) ----
JID2 = "ch2SevenDaysJrn1"          # the fat Ch.2 journal
A2 = {"graymaiden": "grayMaidenFoot01", "ishani": "ishaniDhatri0001",
      "physician": "queensPhysician1", "silteel": "siltEel000000001", "yvicca": "yviccaSeaHag0001",
      "girrigz": "girrigzRipper001", "vendra": "vendraLoaggri001", "lavthug": "lavenderThug0001",
      "jolistina": "jolistinaSusp001", "davaulus": "reinerDavaulus01", "cultist": "urgathoaCultist1",
      "ramoska": "ramoskaArkminos1", "andaisin": "andaisinUrgath01", "andaisin_t": "andaisinDaughtr1"}
F2 = {"a_ch2": "ch2ActorFolder01", "a_creatures": "ch2CreaturesFld1"}

ids = B._idgen(220002)             # Ch.2 folders/pages/notes (distinct seed)
def nid(): return next(ids)
sids = B._idgen(880002)
def sid(): return next(sids)

# ---- link + section helpers ----
def act(_id, label): return f"@UUID[Compendium.{MODID}.cotct-actors.Actor.{_id}]{{{label}}}"
def chk(s): return f"@Check[{s}]"
def SEC(html): return B.s_secret(html, sid())
def box(anchor, fallback_html):
    t = B.verbatim(anchor)
    return B.s_read(B.parafy(t)) if t else B.s_read(fallback_html)
ROOTC, CHC = "#5a0b0b", "#8a1a1a"

# =====================================================================
# FOLDERS (nest under the shared roots; written into the relevant packs)
# =====================================================================
folders = [
  B.folder(F2["a_ch2"], "2. Seven Days to the Grave", "Actor", ACTOR_ROOT, 200000, CHC),
  B.folder(F2["a_creatures"], "Creatures", "Actor", F2["a_ch2"], 100000, None, "a"),
]
for f in folders:
    pack = {"Actor": "actors", "Item": "items", "JournalEntry": "journals"}[f["type"]]
    B.write(pack, "_folder_ch2-" + f["name"].lower().replace(" ", "-").replace(".", "") + "-" + f["type"][:3].lower(), copy.deepcopy(f))

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
   B.gear("full-plate", nid()), B.gear("steel-shield", nid()), B.gear("longsword", nid()), B.gear("composite-longbow", nid())],
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
        "<p><strong>Tactics &amp; morale:</strong> opens with Shield of Faith, falls back on Sanctuary, and heals/supports allies. Alone, he flees; cornered, he fights to the death. Befriended (a "+chk("type:diplomacy|dc:12")+" gets him to heal Brienna free; a PC cleric of a charitable god may even start him converting to Sarenrae), he stops charging the party — they serve Abadar by saving the city.</p>",
  folder=F2["a_creatures"], blurb="Abadaran healer; plague-chapter ally", token_src=None, actor_link=True))

AW("queens-physician", B.npc(A2["physician"], "Queen's Physician", 2, 18, 30, 6, 9, 6, 8,
  {"str": 2, "dex": 4, "con": 1, "int": 1, "wis": 0, "cha": -1}, 25,
  {"stealth": 8, "deception": 6, "medicine": 6, "religion": 6}, ["humanoid", "human"], ["common"],
  [B.strike(nid(), "Club", 9, "1d6+2", "bludgeoning", ["agile"]),
   B.sneak_attack(nid(), 1, "The physician"),
   B.action(nid(), "Beaked Mask", "passive", "<p>The physician's magic plague-mask hides its evil and Urgathoan faith and filters the air — it gains a +2 status bonus to saves vs. disease and inhaled threats. Lifting the mask to 'prove' a human face does not remove it or end its effect.</p>", category="defensive"),
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
   B.lore(nid(), "Underworld Lore", 12),
   B.gear("leather-armor", nid())],
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
   B.gear("studded-leather", nid()), B.gear("steel-shield", nid()), B.gear("rapier", nid()), B.gear("hand-crossbow", nid())],
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
   B.gear("studded-leather", nid()), B.gear("hand-crossbow", nid()), B.gear("dagger", nid())],
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
   B.gear("studded-leather", nid()), B.gear("rapier", nid())],
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
   B.gear("breastplate", nid()), B.gear("scythe", nid())],
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
        "<p><strong>Negotiation, not battle:</strong> he holds the captive Varisian <strong>Ruan Mirukova</strong> (testing Varisian plague-immunity) and will simply <em>sell</em> him and leave — ~200 gp re-scaled, a magic item, a future favor, or the last <em>death's head coffer</em> from Andaisin's sanctum. If attacked he fights ferociously but flees via Dimensional Step rather than be destroyed. <strong>This is a CR-14-equivalent encounter far above the party — telegraph the danger.</strong></p>",
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
   B.gear("breastplate", nid()), B.gear("scythe", nid())],
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

pages.append(page(nid(), "Chapter Background",
  B.s_milestone("<p><strong>Chapter 2 — Seven Days to the Grave.</strong> Korvosa quiets after the riots — and then Queen Ileosa's true horror begins: a manufactured plague, <strong>Blood Veil</strong>, loosed to cull the citizens she despises. The PCs (now ~L4) race to find a cure as the city dies around them.</p>")
  + SEC("<p><strong>The conspiracy (GM only).</strong> Ileosa always meant her husband's murder to be only the start. Through the Red Mantis assassin <strong>Kayltanya</strong> she obtained <em>Vorel's phage</em>; the Mantis connected her to the 'gentleman's killer' Dr. <strong>Reiner Davaulus</strong>, who with the Urgathoan zealot <strong>Lady Andaisin</strong> and the vampire-scholar <strong>Ramoska Arkminos</strong> weaponized the phage into the fast, dramatic, terror-spreading <strong>blood veil</strong>.</p>")
  + SEC("<p><strong>The delivery.</strong> A fortune in Korvosan silver was tainted with blood veil using a <em>death's head coffer</em> and scattered through the poor quarters and the Bank of Abadar — striking the very priests best placed to fight it. As cover, the conspirators sank the plague-ship <em>Direption</em> in the Jeggare as a <strong>red herring</strong>: investigators who chase the ship waste days while the tainted coin spreads. Letting blood veil run its course cripples the city's will to resist Ileosa's deeper pacts.</p>")
  + B.s_conv("<p>This is the payoff of the <strong>Blood Veil</strong> setup from Chapter 1. Run the persistent-plague overlay from here (Conversion Guide journal → <em>Blood Veil &amp; the Epidemic Clock</em>): start the Epidemic Clock now, seeded by how the city fared in 'Edge of Anarchy.'</p>")))

pages.append(page(nid(), "Advancement & Running the Chapter",
  "<p><strong>Advancement.</strong> The PCs begin well into 4th level → <strong>5th</strong> after their first plague mission → <strong>6th</strong> before Carowyn Manor / Racker's Alley → <strong>7th</strong> before the Temple of Urgathoa beneath the hospice → just <strong>8th</strong> by the chapter's end.</p>"
  + "<p><strong>The seven days.</strong> Blood veil takes ~7 days to kill, so the early deaths are isolated among the poor and go unnoticed for days. Keep the PCs busy first (the most time-consuming early task is smuggling Trinia Sabor out of the city), and give them time to resupply and form attachments — the coming tragedies should land personally.</p>"
  + B.s_skill("<p><strong>The Second Harrowing.</strong> Zellara's deck performs its second reading at the chapter's start, generating this chapter's Harrow Points (Conversion Guide → <em>The Harrowing</em>). This chapter is tied to the suit of <strong>shields</strong> and to <strong>Constitution</strong> — read the cards grim: mass graves, ashen-faced women (the Gray Maidens), carrion birds (the Queen's Physicians).</p>")))

pages.append(page(nid(), "NPC Developments",
  "<p>Threads from Chapter 1 continue even where the NPCs have no direct role here:</p>"
  + "<ul>"
    "<li><strong>Amin Jalento</strong> barricades himself in his Old Korvosa home, survives the plague, and resurfaces in Chapter 3.</li>"
    "<li><strong>Devargo Barvasi</strong> locks down Eel's End to ride out the quarantine — but unless the PCs intervened, his ettercap "+act("chittersnap00001", "Chittersnap")+", starving, turns on and kills him (his silk-wrapped body found in the hold). If Chittersnap died in Chapter 1, Devargo survives and Eel's End can be a safe haven.</li>"
    "<li><strong>Neolandus Kalepopolis</strong>, the missing seneschal hiding in Old Korvosa, is captured by the Arkonas as this chapter opens — the hook into Chapter 3.</li>"
  "</ul>"))

pages.append(page(nid(), "Cressida's Concern",
  "<p>Within hours of Trinia's botched execution, Field Marshal <strong>Cressida Kroft</strong> seeks out the PCs, worried. Queen Ileosa is restructuring Korvosa's military; Cressida fears for her own position and warns the PCs that her ability to fund their work — and to shield them — is shrinking.</p>"
  + B.s_conv("<p><strong>Mechanically:</strong> the PCs should no longer consider themselves official Korvosan Guard agents. Cressida still aids them where she can and asks where to reach them — establishing her as their fraying but loyal patron as the city tilts toward martial law.</p>")))

pages.append(page(nid(), "Rise of the Gray Maidens",
  "<p>Sabina Merrin first appeared in gleaming red-and-crimson full plate at Trinia's near-execution. She now commands the <strong>Gray Maidens</strong> — an all-women elite loyal only to Ileosa, handed the Longacre Building (arbiter Zenobia Zenderholm welcomes them; the bound efreeti Yzahnum and the bloatmage seneschal Togomor speed their arming) as their headquarters.</p>"
  + SEC("<p><strong>The truth.</strong> Recruits are chosen for beauty and strength; those who fail are disfigured and imprisoned in the dungeons below. Those who pass endure a breaking, scarring initiation. Present them at first as saviors of order — the personification of martial law — and let their brutal nature surface across the chapter. Once they appear, Ileosa retreats into the sealed Castle until Chapter 3.</p>")
  + "<p>Use "+act(A2["graymaiden"], "Gray Maiden Foot Soldier")+" for rank-and-file Gray Maidens in this and later chapters.</p>"))

# --- Part 1: Infection — early events ---
GRAU, TRINIA = "grauSoldado00001", "triniaSabor00001"   # Ch.1 actor ids
PG("A Damsel in Distress", SR("A Damsel in Distress", 76)
  + "<p>Vencarlo Orisini (secretly Blackjack, who rescued Trinia from the gallows) sends the PCs a cryptic note inviting them to his Old Korvosa academy at 16 Hillcrest Street.</p>"
  + box("My friends, I hope this note finds you in good health",
        "<p>My friends, I hope this note finds you in good health in these dangerous times. In light of the recent unrest, I could provide some tips on self-defense, offered gratis, at Orisini Academy, 16 Hillcrest Street. I eagerly await your arrival. — Vencarlo Orisini</p>")
  + "<p>Inside, he reveals "+act(TRINIA, "Trinia Sabor")+" in disguise and asks the PCs to smuggle her to safety — to a wayside inn called <strong>Trots</strong> (12 miles north), where Jasan Adriel takes her on to a ranch in Harse. He funds the trip (a horse, supplies, 20 gp for the inn) and, if pressed, offers <strong>500 gp</strong>.</p>"
  + B.s_skill("<p>A subtle egress is best — a low-key walk out the gates among the afternoon merchants. Crimson-tunic'd guards, Hellknights, mercenaries, and the odd Gray Maiden eye the party, but pass unless the PCs do something suspicious (showy magic, a fight). Optional hinterland encounters en route let Trinia (a bard) fight beside them toward 5th level.</p>")
  + SEC("<p><strong>GM:</strong> Ileosa has set a <strong>5,000 gp bounty</strong> on Trinia. Trinia strongly suspects Vencarlo is Blackjack but keeps it to herself; she warms to the PCs and may become a friend (she returns in Chapter 4).</p>")
  + B.s_treasure("<p><strong>Rewards:</strong> deliver Trinia to Trots → <strong>2,400 XP</strong>. Befriended, she gifts the party her masterwork <strong>mithral dagger</strong> and her <strong>wand of <em>daze monster</em></strong> ('I won't need them in Harse — you might').</p>"))

PG("Yellow Lights & the First Symptoms", SR("Yellow Lights / First Symptoms", 80)
  + "<p>One night early in the chapter (ideally while the PCs are escorting Trinia), the queen's <strong>red herring</strong> sails in: the <em>Direption</em>, a black-sailed Urgathoan ship hung with <strong>yellow quarantine lanterns</strong>, before it sinks in the Jeggare. Anyone hunting the plague's source is meant to waste days on the wreck — and meet the deadly thing the cult left in it (the Direption wreck, built in the next increment).</p>"
  + "<p><strong>A second favor.</strong> "+act(GRAU, "Grau Soldado")+" — sober and back with the Guard — begs the PCs' help: his niece <strong>Brienna</strong> (in Trail's End) has broken out in red pocks, can't keep food down, and is failing. At the Soldado home the PCs meet the Abadaran healer "+act(A2["ishani"], "Ishani Dhatri")+", brewing herbs he can't quite make work — he doesn't recognize Brienna's symptoms, and fears a new disease.</p>"
  + B.s_skill("<p><strong>Saving Brienna:</strong> she has <strong>Blood Veil</strong> ("+B.cond("drained", "Drained")+" from Con loss). <em>Remove disease</em> cures it; <em>lesser restoration</em> staves off the drain. "+act(A2["ishani"], "Ishani")+" will sell a <em>remove disease</em> potion or return to cast it for <strong>150 gp</strong> — or, with "+chk("type:diplomacy|dc:12")+" (he's ashamed to charge; "+chk("type:perception|dc:20")+" reads it), cast it <strong>free</strong> the next day.</p>")
  + SEC("<p><strong>Exposure.</strong> Treating Brienna exposes the PCs and Ishani to Blood Veil — each attempts "+chk("type:fortitude|dc:18")+" or contracts it (the staged disease in the Conversion Guide). This is the plague's <strong>first on-screen case</strong>: <strong>start the Epidemic Clock now</strong> (Conversion Guide → <em>Blood Veil &amp; the Epidemic Clock</em>).</p>")
  + B.s_treasure("<p><strong>Story award:</strong> cure Brienna → <strong>1,600 XP</strong>. "+act(A2["ishani"], "Ishani")+" — impressed — offers to aid the PCs' charitable work and can be reached at the Grand Vault of Abadar; befriended, he heals them free thereafter.</p>"))

PG("The Unwashed Masses & the Missing Arbiter", SR("Outbreak / Grand Vault", 82)
  + "<p>Ishani leads the PCs to the <strong>Grand Vault of Abadar</strong> (North Point), seat of Archbanker Darb Tuttle and the city's most powerful faith — and, by Ileosa's design, the institution best placed to fight the plague and so the one her tainted silver strikes first.</p>"
  + box("Yet for a deity of law, the steep stairs and ramps",
        "<p>Dozens of citizens — mostly working class, a few merchants' silks among them — throng the temple's great bronze doors, scarcely held back by gold-armored Abadaran clerics turning nearly all comers away. The reason shows on one desperate believer's face: violent red sores mottling his skin.</p>")
  + B.s_skill("<p>To reach the doors the PCs must shove through the desperate crowd — "+chk("type:athletics|dc:18")+" each. Any obvious healer is mobbed for aid. Ishani's name (or his company) gets them past the door guards.</p>")
  + "<p><strong>The Missing Arbiter.</strong> Inside, the plague's spread is undeniable and the trail of the missing investigating arbiter opens the cure-hunt. Field Marshal Kroft soon calls the PCs to a meeting (<em>First, Do No Harm</em>) to formally task them with finding the source.</p>"
  + B.s_treasure("<p><strong>Story award:</strong> navigate the crowd without harming anyone → <strong>1,600 XP</strong>.</p>")
  + B.s_conv("<p>From here the chapter opens into the cure missions (the <em>Direption</em> wreck, Carowyn Manor, Racker's Alley) and finally the Hospice of the Blessed Maiden / Temple of Urgathoa — built in the next increments. Advance the Epidemic Clock as in-city days pass.</p>"))

# --- Part 2: Outbreak — the Queen's Physicians & the cure missions ---
PG("First, Do No Harm & the Queen's Physicians", SR("First, Do No Harm", 85)
  + "<p>Field Marshal Kroft summons the PCs to Citadel Volshyenek. Royal orders have just arrived: the Guard must escort and obey Queen Ileosa's new <strong>Queen's Physicians</strong> and treat any Gray Maiden's command as a superior officer's.</p>"
  + box("The echoes of forcefully spoken but unintelligible words",
        "<p>In the citadel's mustering ground, red-and-silver guards stand uneasy as Field Marshal Kroft paces a wooden platform. Behind her loom cowled figures in oily leather, gloves, and wide black hats, each masked with a dark-goggled, beak-like visor — some gripping canes, others dark satchels. Among them: a soft-spoken, white-streaked gentleman clutching a doctor's case, and an imposing Gray Maiden in crimson-plumed plate.</p>")
  + "<p>Kroft introduces <strong>Dr. Reiner Davaulus</strong>, leader of the Queen's Physicians — calm, fatherly, analytical — and hands out the royal decree (Handout #2-2). The Gray Maiden is Kordaitra Destaid, the Maidens' quartermaster, who will confront the PCs later. "+act(A2["ishani"], "Ishani")+" cautiously offers to coordinate the Abadaran effort.</p>"
  + box("By Decree of Her Royal Majesty, the Radiant Queen Ileosa",
        "<p><strong>Attention!</strong> By decree of Queen Ileosa, all citizens and the Korvosan Guard must aid and admit the Queen's Physicians, who may enter any home or building in their duties; the sick must submit to treatment. The Gray Maidens will provide military support and answer only to the Crimson Throne. Impeding the Physicians or Maidens means imprisonment; impersonating one, death; harboring the infected, death; spreading blood veil, torture then death.</p>")
  + SEC("<p><strong>The truth.</strong> Davaulus is a <strong>Red Mantis</strong> assassin — a poisoner who masterminded blood veil with Andaisin and Ramoska; his masked 'physicians' are "+act(A2["physician"], "Urgathoa cultists")+" who <em>spread</em> the plague while feigning to treat it. His one tell: he praises the queen too warmly. He is the Hospice finale boss (Part 3).</p>"))

PG("Combating the Plague (the missions)", SR("Combating the Plague", 88)
  + "<p>Kroft (and Davaulus, for show) sets the PCs to investigate the plague's source and stem it. The chapter offers several missions, run in any order over the days the city sickens — each advances the Epidemic Clock as time passes. The headline lead is the <strong>plague-ship</strong> sunk in the Jeggare (Mission 1), with Carowyn Manor and Racker's Alley to follow.</p>"
  + SEC("<p><strong>The Quarantine of Old Korvosa.</strong> After the PCs complete two or three missions (and before the Hospice in Part 3), Ileosa quarantines all of Old Korvosa: the Gray Maidens burn every wooden bridge and barricade the one stone bridge. This <strong>cannot be prevented</strong> — it sets up Chapter 3. (How to come and go appears in Chapter 3.)</p>"))

PG("Mission 1: The Wreck of the Direption", SR("Mission 1 — the Direption", 89)
  + "<p>Cressida gives the wreck's location. Diving the muddy Jeggare, "+chk("type:perception|dc:15")+" locates the ship ("+chk("type:perception|dc:25")+" without a light source); "+chk("type:athletics|dc:10")+" swims the placid deep. Every 10 minutes searching carries a cumulative chance of drawing the silt eels. "+chk("type:society|dc:20")+" identifies a Nidalese merchantman; "+chk("type:society|dc:30")+" (Guard records) traces it to the long-'lost' <em>Direption</em> of Garagori Whenston — a dead-end that is precisely the point.</p>"
  + SEC("<p><strong>It is a red herring.</strong> The ship carries no plague source — only clues that waste days. Lady Andaisin left a lethal surprise: the sea-hag druid "+act(A2["yvicca"], "Yvicca")+" and her jigsaw-shark companion <strong>Skinshear</strong>, moved into the wreck to kill investigators. The hull lies split in two over a rock; the stern's main hatch ("+chk("type:athletics|dc:26")+") and hold trap door ("+chk("type:athletics|dc:23")+") are swollen shut, but a 10-ft trebuchet hole opens easy access to A2.</p>")
  + B.s_conv("<p>This is an <strong>underwater</strong> dungeon — without water-breathing/freedom of movement the PCs fight at a real disadvantage; flag that to the GM. Re-judge attack/movement penalties per the PF2e aquatic-combat rules.</p>"))

area2("A1", "The Direption's Bow", SR("A1", 90)
  + "<p>The shattered bow lies open to the river. Six "+act(A2["silteel"], "silt eels")+" nest in the silt among the splinters, lunging at anything that disturbs them.</p>"
  + B.enc("Silt eel nest", encx([-1]*6, 4),
     "<p>6 "+act(A2["silteel"], "silt eels")+" swarm — individually trivial, but their stacking venom and the underwater footing make them a real nuisance.</p>",
     B.aside_token(["6× "+act(A2["silteel"], "Silt Eel (−1)")])))

area2("A2", "The Shattered Hold", SR("A2", 90)
  + "<p>The trebuchet hole opens into the flooded hold. "+act(A2["yvicca"], "Yvicca")+" has set her jigsaw-shark companion <strong>Skinshear</strong> here to guard the way down. It circles, butts the door to A3 to warn its mistress, then attacks.</p>"
  + B.enc("Skinshear (Yvicca's shark)", encx([1], 4),
     "<p><strong>Skinshear</strong> — an unusually large "+act("lsdWSvGJ81hDy4it", "jigsaw shark")+" (the GM may apply the Elite adjustment for the named companion). It fights to the death and alerts Yvicca.</p>",
     B.aside_token([act("lsdWSvGJ81hDy4it", "Skinshear — Jigsaw Shark (1, elite)")])))

area2("A3", "Crew Quarters", SR("A3", 91)
  + "<p>The cleaved stern holds the captain's cabin — "+act(A2["yvicca"], "Yvicca's")+" lair. She prepares (Evil Eye, then joins from A2 once Skinshear raises the alarm) and fights as the wreck's boss.</p>"
  + B.enc("BOSS — Yvicca", encx([6], 4),
     "<p>"+act(A2["yvicca"], "Yvicca")+", a sea-hag druid (with Skinshear if it still lives). Underwater, at range, with Horrific Appearance and Tanglevine, she is a genuine Severe-leaning threat for a party that came unprepared.</p>",
     B.aside_token([act(A2["yvicca"], "Yvicca (6)"), act("lsdWSvGJ81hDy4it", "Skinshear (1)")]))
  + B.s_treasure("<p>Yvicca's hoard (re-scaled to PF2e ~L5–6): a few hundred gp in coin and pearls, a minor druidic trinket, and the cult's planted <em>clues</em> (forged manifests pointing nowhere) that confirm the wreck was bait. No plague source is here.</p>")
  + B.s_conv("<p>Clearing the wreck proves the plague's source lies elsewhere — pushing the PCs toward Carowyn Manor / Racker's Alley and, ultimately, the Hospice.</p>"))

area2("A4", "The Captain's Cabin", SR("A4", 91)
  + box("the tattered sheets of a canopied bed twist",
        "<p>The tattered sheets of a canopied bed twist like ghosts above its snapped frame; knotted amid the linens, a drowned man idly floats in the murky water. A closed footlocker lies on its side at the room's far end.</p>")
  + "<p>The swollen door takes "+chk("type:athletics|dc:20")+" to force. The corpse is <strong>Rois Vindmel</strong> — the Urgathoan zealot who steered the ship in, knocked out against his own footlocker as she sank. His face is crab-eaten and his tongue gone: <em>speak with dead</em> yields little ("+chk("type:perception|dc:20")+" to make out his tongueless howl of one word — '<strong>Andaisin</strong>'). His silver unholy symbol of Urgathoa hangs at his neck.</p>"
  + B.s_treasure("<p>"+chk("type:perception|dc:10")+" finds skin and hair on the footlocker's corner (the 'murder weapon'); "+chk("type:perception|dc:20")+" confirms its seal held — <strong>the contents are dry</strong>. Inside: ~90 gp re-scaled in coin, a <strong>cloak of resistance +2</strong> (resilient rune; an embroidered Urgathoan symbol comes off with "+chk("type:crafting|dc:20")+" — a failure leaves the cloak broken, +1 until repaired), and <strong>Serving Your Hunger</strong>, Urgathoa's sacred text — exquisitely bound (~150 gp re-scaled bounty from any non-evil Korvosan church; ruined to a third of that if the footlocker is opened underwater). Rois has scratched out 'Urgathoa' throughout and penned in '<strong>Andaisin</strong>.'</p>")
  + SEC("<p><strong>The name that matters.</strong> "+chk("type:society|dc:20")+" or "+chk("type:diplomacy|dc:25")+" (gather information) — or simply telling Cressida — reveals: years ago the Nidalese village of <strong>Beorandy</strong> died of engineered plague at the hands of an Urgathoan cell led by <strong>Andaisin</strong>, still wanted in Pangolais for mass murder. Cressida grows grim: the 'plague ship' was a decoy, and a plague-cult is loose in Korvosa. <strong>Story awards:</strong> the cult connection (1,600 XP) and Andaisin's significance (1,200 XP).</p>")
  + B.s_conv("<p><strong>Survivor Count:</strong> the wreck is the conspirators' time-sink — every day past the first spent on the Direption costs <strong>10 citizens</strong> from the chapter's saved-lives tally (and feeds the Epidemic Clock).</p>"))

PG("Mission 2: Plague Rats", SR("Mission 2 — Plague Rats", 92)
  + "<p>Plague-panicked mobs have begun lynching Korvosa's reclusive wererats, and the firebrand <strong>Girrigz Ripperclaws</strong> answers with a call to war on the city above. An elder wererat, <strong>Eries Yelloweyes</strong> (50 years hidden as a fishmonger), fears a purge and approaches the PCs in human form: stop Girrigz — ideally <em>without</em> a slaughter of her people — and she'll have her kin fight the plague from the shadows (disposing of infected bodies). She gives directions to his lair beneath Midland.</p>"
  + B.s_skill("<p>The sewers are slick: moving faster than half Speed or attacking in the sewage flow forces "+chk("type:acrobatics|dc:12")+" or fall "+B.cond("prone", "Prone")+". A "+chk("type:nature|dc:15")+" recognizes the alarm-fungus shrieker in B2.</p>")
  + SEC("<p><strong>Survivor Count:</strong> scattering Girrigz's warband without killing the other (coerced) wererats saves <strong>400 citizens</strong> and seeds an ongoing wererat ally network — a major win for the persistent-plague Epidemic Clock.</p>"))

area2("B1", "Sewer Tunnel", SR("B1", 92)
  + "<p>The approach to Girrigz's camp through Korvosa's sewers (pad it with wandering-monster encounters if the party needs XP). The main tunnel bends east to a rusty grate overlooking B4.</p>")

area2("B2", "Guard Den", SR("B2", 92)
  + "<p>A guard post around a sewage pool. A <strong>shrieker fungus</strong> by the south wall screeches if any creature enters and doesn't immediately move north past the central pillar — its noise summons the B3 wererats and the B5 swarm, and wakes the B4 "+B.mon("otyugh", "otyugh")+".</p>"
  + B.enc("Wererat guards", encx([2, 2, -1, -1, -1], 5),
     "<p>2 "+B.mon("wererat", "wererats")+" and 3 "+B.mon("giant-rat", "giant rats")+" (the rats avoid crossing the water lest they trip the shrieker; the wererats cross it deliberately to raise the alarm).</p>",
     B.aside_token(["2× "+B.mon("wererat", "Wererat (2)"), "3× "+B.mon("giant-rat", "Giant Rat (−1)")])))

area2("B3", "Communal Dens", SR("B3", 93)
  + "<p>The wererats' fire-lit warren of nests. The floor is slippery in the sewage flow (as B2). "+chk("type:perception|dc:20")+" finds a squeeze-hole to B6; "+chk("type:crafting|dc:14")+" notes the subsiding south wall — chipping it (Hardness 8, 40 HP) lets the trapped "+B.mon("otyugh", "otyugh")+" rampage through.</p>"
  + B.enc("Wererat den (Girrigz reinforces)", encx([2, 2, 2, 2], 5),
     "<p>4 "+B.mon("wererat", "wererats")+". If fighting erupts here, "+act(A2["girrigz"], "Girrigz")+" comes through the east wall from B6 in his dire-rat form.</p>",
     B.aside_token(["4× "+B.mon("wererat", "Wererat (2)"), act(A2["girrigz"], "Girrigz (6, reinforces)")]))
  + B.s_treasure("<p>"+chk("type:perception|dc:18")+": 3 smokesticks, a tanglefoot bag, a thunderstone, 20 tindertwigs, a copper coat-of-arms trumpet (~15 gp re-scaled), and masterwork carpenter's tools.</p>"))

area2("B4", "Trapped Otyugh", SR("B4", 93)
  + "<p>The wererats have penned a lone "+B.mon("otyugh", "otyugh")+" between two grates (Hardness 10, 60 HP, lift "+chk("type:athletics|dc:26")+"; the jammed east-grate winch retracts it after a minute's cranking). Starving, it sleeps until noise wakes it.</p>"
  + B.s_skill("<p>The otyugh ('so hungeries!') can be turned against the wererats: "+chk("type:diplomacy|dc:23")+" (+4 if fed) wins an hour's help, or "+chk("type:intimidation|dc:17")+" buys 10 minutes — after which it forgets and tries to eat the PCs.</p>")
  + B.enc("Otyugh (if it attacks)", encx([4], 5),
     "<p>One hungry "+B.mon("otyugh", "otyugh")+" — a potential ally or a third combatant in the wererat fight.</p>",
     B.aside_token([B.mon("otyugh", "Otyugh (4)")])))

area2("B5", "Rat Dens", SR("B5", 93)
  + "<p>A bone-littered nest cave. It attacks anything that doesn't smell of rodent; the swarm investigates if the shrieker sounds, but the rats are too lazy to.</p>"
  + B.enc("Rat nest", encx([1, -1, -1, -1, -1, -1, -1], 5),
     "<p>A "+B.mon("rat-swarm", "rat swarm")+" and 6 "+B.mon("giant-rat", "giant rats")+".</p>",
     B.aside_token([B.mon("rat-swarm", "Rat Swarm (1)"), "6× "+B.mon("giant-rat", "Giant Rat (−1)")])))

area2("B6", "Girrigz's Den", SR("B6", 94)
  + "<p>The warlord's command den — a crude map of Korvosa pinned to a crate, crates of scavenged arms and alchemist's fire. "+act(A2["girrigz"], "Girrigz")+" plots his war here, dreaming of burning Castle Korvosa.</p>"
  + B.enc("BOSS — Girrigz Ripperclaws", encx([6], 5),
     "<p>"+act(A2["girrigz"], "Girrigz")+" — pre-buffed if warned, striking from stealth with his runed rapier and Vital Strike. He fights to the death.</p>",
     B.aside_token([act(A2["girrigz"], "Girrigz Ripperclaws (6)")]))
  + B.s_treasure("<p>"+chk("type:perception|dc:15")+": an arms cache (22 daggers, 12 short swords, 3 crossbows, 4 chain shirts, 12 alchemist's fire, a masterwork longsword + chainmail). "+chk("type:perception|dc:20")+" in the nest: 4 potions of healing, a bottle of air, and a <strong>pearl of power</strong> (1st-rank) — plus the squeeze-crack to B3.</p>"))

PG("Mission 3: The Color of Death", SR("Mission 3 — The Color of Death", 96)
  + "<p>The Lavender perfumery off Summoning Street, owned by the Chelish con-artist "+act(A2["vendra"], "Vendra Loaggri")+", is selling 'Lavender's Luxuriant Liniment' — a 2-gp 'plague cure' that is sugar, cheap scent, and river water. By day a queue stretches four blocks; the mission is to <strong>expose the fraud</strong>, not to fight.</p>"
  + B.s_skill("<p><strong>Cracking the con:</strong> "+chk("type:crafting|dc:22")+" (an hour with an alchemist's lab) reveals the liniment is worthless; "+chk("type:perception|dc:18")+" spots her planted shill Solt Carmino (the only 'customer' browsing perfume), and "+chk("type:diplomacy|dc:25")+" or "+chk("type:intimidation|dc:25")+" makes him confess. The cleanest proof: administer a dose to a real plague victim before a Korvosan Guard (Grau or Kroft will witness), then actually cure them.</p>")
  + SEC("<p>This 'cure' is a <strong>dead end</strong> for the plague (and a moral test) — it heals no one. Watching Vendra's thugs haul river-water barrels from the Jeggare by night (easy to tail) is the fastest evidence. Report to Cressida and the Guard arrests her.</p>")
  + B.s_treasure("<p><strong>Story award:</strong> expose the scam and shut Lavender down → <strong>1,600 XP</strong>, plus full XP for everyone (Vendra included) the PCs <em>didn't</em> have to kill.</p>"))

area2("C1", "The Perfumery (Lavender)", SR("C1", 96)
  + "<p>A cramped, stylish shop of amethyst glass, its counter stacked with magenta-stoppered phials of the fake liniment. "+act(A2["vendra"], "Vendra")+" works the crowd while two shop-girls sell and two "+act(A2["lavthug"], "Lavender thugs")+" watch with saps. Confront her with proof and she screams for the PCs' ejection; cornered, she flees toward C2, knifing a PC on the way out.</p>"
  + B.enc("Vendra + thugs (by day)", encx([5, 3, 3], 6),
     "<p>"+act(A2["vendra"], "Vendra")+" and 2 "+act(A2["lavthug"], "Lavender thugs")+" amid scattering customers (CR7-equivalent by day; fewer guards and no crowd at night make it easier). Vendra fights dirty and runs.</p>",
     B.aside_token([act(A2["vendra"], "Vendra Loaggri (5)"), "2× "+act(A2["lavthug"], "Lavender Thug (3)")]))
  + B.s_treasure("<p>"+chk("type:society|dc:18")+" picks out genuine perfumes worth ~80 gp re-scaled; the counter box holds ~40 gp in recent sales, and the safe ("+chk("type:thievery|dc:28")+") a few hundred gp in coin + three lapis perfume bottles. Vendra carries a <strong>circlet of persuasion</strong>, a wand of <em>charm person</em>, and a wand of <em>remove disease</em>.</p>"))

area2("C2", "Vendra's Apartment", SR("C2", 99)
  + "<p>A locked ("+chk("type:thievery|dc:20")+"), prim parody of a Chelish noble's salon — no alchemy here. "+chk("type:perception|dc:20")+" finds a corner-hinged <strong>secret door</strong> into the boarded-up lab (C3). By night there's a 50% chance Vendra sleeps here; otherwise she's mixing brew in C3.</p>")

area2("C3", "The Liniment Laboratory", SR("C3", 99)
  + "<p>The 'condemned' apartment behind the shop, boarded shut inside and out (Hardness 5, 15 HP, "+chk("type:athletics|dc:24")+" to break), reachable by the C2 secret door. Here the fake cure is mixed from river water hauled in nightly. By day one "+act(A2["lavthug"], "thug")+" works; by night Vendra and two thugs brew.</p>"
  + B.enc("Lab guards", encx([3], 6),
     "<p>1 "+act(A2["lavthug"], "Lavender thug")+" by day (more at night with Vendra).</p>",
     B.aside_token([act(A2["lavthug"], "Lavender Thug (3)")]))
  + B.s_treasure("<p>The lab equipment functions as an alchemist's lab; the raw ingredients are ~800 gp (PF1e) of potion/alchemy reagents — re-scale to a useful crafting stock for the party.</p>")
  + B.s_conv("<p>Mission complete: the perfumery con collapses. It cured nothing — the real source is still out there, pointing the PCs onward (Racker's Alley, Carowyn Manor, the Hospice).</p>"))

PG("Mission 4: The Hungry Dead", SR("Mission 4 — The Hungry Dead", 100)
  + "<p>As bodies pile up, lazy plague-carters have been dumping corpses in <strong>Racker's Alley</strong> (western Old Korvosa) instead of the Gray District. Kroft (or the temple, or rumor) sends the PCs to confirm it and clear any scavengers or undead before guards haul the dead away.</p>"
  + SEC("<p><strong>GM:</strong> four "+B.mon("vampire-servitor", "vampire spawn")+" — minions of the Ustalavic vampire-count Tiriac, sent to 'assist' (and watch) the nosferatu <strong>Ramoska Arkminos</strong> — have lairred under Giotorri's Toys and feed on the dumped (and the living). They long ago forgot their charge to watch Ramoska. <em>Ramoska is the Temple-of-Urgathoa villain (Part 3).</em></p>")
  + SEC("<p><strong>Survivor Count:</strong> clearing the spawn and confirming the dumping ground (so the Guard can stop it) saves <strong>200 citizens</strong> — feed it into the Epidemic Clock.</p>"))

area2("D1", "Racker's Alley", SR("D1", 100)
  + "<p>A shadowed, sunless dead-end alley with 40+ corpses heaped against the east wall. "+chk("type:perception|dc:16")+" notes that many bodies are blood-drained with neck/wrist punctures — and bear <em>no</em> blood-veil sores. <strong>Contact with the plague-dead exposes a creature to Blood Veil</strong> ("+chk("type:fortitude|dc:18")+"). A 10-ft hole in the east wall opens into the workshop (D2).</p>"
  + B.enc("Vampire spawn sentry", encx([4], 6),
     "<p>By night one "+B.mon("vampire-servitor", "vampire spawn")+" watches from the 20-ft roof (−2 to spot it from the alley floor). Seeing anyone touch the bodies, it shrieks and attacks; its 3 companions arrive from D2 in 1d3 rounds.</p>",
     B.aside_token([B.mon("vampire-servitor", "Vampire Spawn (4)")])))

area2("D2", "The Workshop", SR("D2", 101)
  + "<p>Beneath the toy-shop: the lair where the four "+B.mon("vampire-servitor", "vampire spawn")+" keep their coffins, watched over by the desiccated corpse of the toymaker Rodolfo Giotorri (eight neck-punctures; "+chk("type:perception|dc:15")+" finds his key ring). Fight all four here if the alley alarm was raised.</p>"
  + B.enc("BOSS — the four vampire spawn", encx([4, 4, 4, 4], 6),
     "<p>All 4 "+B.mon("vampire-servitor", "vampire spawn")+" — blood drain, dominate gaze, drain, fast healing, and their vampire weaknesses (running water, sunlight). A genuine Severe-leaning fight; bait them toward sunlight or a threshold.</p>",
     B.aside_token(["4× "+B.mon("vampire-servitor", "Vampire Spawn (4)")]))
  + B.s_treasure("<p>"+chk("type:perception|dc:20")+" in the coffin soil: ~15 pp + 300 gp of Ustalavic coin (re-scale to ~90 gp), a <strong>ring of jumping</strong> (brass spider-legs), and <strong>pipes of haunting</strong> (bone).</p>"))

area2("D3", "Giotorri's Toys", SR("D3", 101)
  + "<p>The dusty, locked showroom above ("+chk("type:thievery|dc:30")+", or Giotorri's key from D2). The spawn left the cheap, defective toys alone.</p>"
  + B.s_treasure("<p>"+chk("type:perception|dc:14")+": a jingling lockbox ("+chk("type:thievery|dc:20")+") with a few coins and an <strong>Abadaran deposit-box key</strong> (No. 261; "+chk("type:society|dc:16")+" or "+chk("type:religion|dc:16")+" to place it). Redeemed at the Grand Vault, it yields Giotorri's savings (~68 gp), masterwork thieves' tools, and <strong>boots of striding and springing</strong>.</p>")
  + B.s_conv("<p>Clearing Racker's Alley removes one of Ramoska's loose ends — and quietly establishes the vampire's presence ahead of the Temple finale.</p>"))

PG("Mission 5: The Case of the Vanishing Virtuoso", SR("Mission 5 — Carowyn Manor", 104)
  + "<p>Deyanira Mirukova begs the PCs (or Kroft refers her) to find her brother <strong>Ruan</strong>, a Varisian ocarina prodigy who went to perform at a masquerade at <strong>Carowyn Manor</strong> and never returned. The estate now sits locked, curtained, and reeking. "+chk("type:society|dc:16")+" recognizes Ruan as a genuine virtuoso. (Her reward is meager — heirlooms under 100 gp and Marbledome passes — but the trail matters.)</p>"
  + SEC("<p><strong>GM:</strong> Ileosa added <em>rich</em> undesirables to the plague's toll; Davaulus farmed the hit-list to the necromancer <strong>Rolth Lamm</strong> (Gaedren's son, the absent master of the Ch.1 Dead Warrens), who — absorbed in studying Varisian plague-immunity — handed it to his lover "+act(A2["jolistina"], "Jolistina Susperio")+". She murdered the entire party, raised 21 of the guests as zombies, and disguised every corpse as a blood-veil death. <strong>The 'plague' here is staged.</strong></p>")
  + B.s_skill("<p><strong>Getting in:</strong> the mahogany front doors are locked ("+chk("type:athletics|dc:26")+" / "+chk("type:thievery|dc:30")+"); the balcony banisters take "+chk("type:athletics|dc:15")+" to climb; the spiked garden hedge "+chk("type:athletics|dc:12")+" (fail by 5+ → @Damage[1d6[piercing]]). Jolistina jammed the side doors and shutters ("+chk("type:athletics|dc:25")+"/"+chk("type:thievery|dc:22")+" doors; shutters easier).</p>"))

area2("E1", "Carowyn Manor — First Floor", SR("E1", 108)
  + box("every papier-mache mask and sequined gown hides a blister-covered corpse",
        "<p>The masquerade is long over: every papier-mâché mask and sequined gown hides a blister-covered corpse. Save for one murderess and one captive host, everyone in Carowyn Manor is dead — and many of them are still dancing.</p>")
  + "<p><strong>The whole manor is one complex encounter.</strong> "+act(A2["jolistina"], "Jolistina")+" hides and plays cat-and-mouse, ordering her posed zombies to defend her while she snipes and Vanishes. Of her 21 "+B.mon("zombie-shambler", "zombies")+", 7 are uncontrolled (they attack anyone).</p>"
  + B.enc("E1a Great Hall — dancing dead", encx([-1] * 6, 6),
     "<p>6 "+B.mon("zombie-shambler", "human zombies")+" posed as dancing noble couples; they turn and attack 1 round after the PCs enter.</p>",
     B.aside_token(["6× "+B.mon("zombie-shambler", "Human Zombie (−1)")]))
  + B.enc("E1b Den — uncontrolled trio", encx([-1] * 3, 6),
     "<p>3 uncontrolled "+B.mon("zombie-shambler", "zombies")+" (lion/lioness/peacock masks); Jolistina avoids this room.</p>",
     B.aside_token(["3× "+B.mon("zombie-shambler", "Human Zombie (−1)")]))
  + B.enc("E1c Dining Room — diners", encx([-1] * 4, 6),
     "<p>4 "+B.mon("zombie-shambler", "zombies")+" mechanically 'dining' among real corpses.</p>",
     B.aside_token(["4× "+B.mon("zombie-shambler", "Human Zombie (−1)")])))

area2("E2", "Carowyn Manor — Second Floor", SR("E2", 110)
  + "<p>More posed "+B.mon("zombie-shambler", "zombies")+" (the remaining ~8) drift through the bedrooms and salon. Here too is the surviving host, <strong>Ausio Carowyn</strong> — broken and captive, kept alive as Jolistina's plaything — and, among the masquerade dead, Deyanira's brother <strong>Ruan</strong>.</p>"
  + B.enc("BOSS — Jolistina Susperio", encx([8], 6),
     "<p>"+act(A2["jolistina"], "Jolistina")+" makes her stand (or her endless retreat) here, fighting from behind whatever zombies remain. Run her as the manor-spanning skirmish she is, not a stand-up fight.</p>",
     B.aside_token([act(A2["jolistina"], "Jolistina Susperio (8)"), "+ remaining "+B.mon("zombie-shambler", "zombies")]))
  + B.s_treasure("<p>Jolistina carries 2 potions of invisibility, a potion of <em>remove disease</em>, wands of <em>animate dead</em> / <em>sculpt corpse</em> / <em>cat's grace</em>, <strong>+1 glamered studded leather</strong>, a hand crossbow with 3 <strong>screaming bolts</strong>, and ~150 gp + stolen jewelry. The manor itself holds a noble household's worth of re-scaled valuables.</p>")
  + B.s_conv("<p><strong>The reveal:</strong> exposing the staged deaths proves the nobles were murdered, not plagued — and the wand of <em>sculpt corpse</em> + Jolistina's link to <strong>Rolth</strong> ties the plague to the necromancer and the cult of Urgathoa, pointing toward the Hospice. Save Ausio; recover Ruan's body for Deyanira.</p>"))

# --- Part 3: EPIDEMIC — the Hospice of the Blessed Maiden (F) ---
PG("Part 3 — Epidemic: The Hospice of the Blessed Maiden", SR("Hospice", 112)
  + B.s_milestone("<p><strong>Part 3 — Epidemic.</strong> The trail converges on the <strong>Hospice of the Blessed Maiden</strong>, the Queen's Physicians' headquarters in a converted warehouse — and on the hidden <strong>Temple of Urgathoa</strong> beneath it. The PCs should be 7th level entering the temple, and just 8th by the chapter's end. This is the plague's heart: "+act(A2["davaulus"], "Davaulus")+", "+act(A2["andaisin"], "Andaisin")+", and the nosferatu "+act(A2["ramoska"], "Ramoska")+".</p>")
  + B.s_skill("<p>The hospice masquerades as a legitimate plague-treatment center, patrolled by "+act(A2["graymaiden"], "Gray Maidens")+" and the masked "+act(A2["physician"], "Queen's Physicians")+". Bluffing or sneaking in beats fighting through; pushing too hard gets the PCs an audience with Davaulus, who tries to misdirect them onto a fictional wererat cult.</p>"))

area2("F1", "Hospice Entry", SR("F1", 112)
  + "<p>The warehouse front: a façade of cots, suffering patients, and brisk masked physicians. "+act(A2["graymaiden"], "Gray Maidens")+" control access; a "+chk("type:deception|dc:24")+" or genuine business gets the PCs past the entry without a fight.</p>"
  + B.enc("Entry watch", encx([3, 2], 7),
     "<p>A "+act(A2["graymaiden"], "Gray Maiden")+" and a "+act(A2["physician"], "Queen's Physician")+" on the door (more respond to an alarm).</p>",
     B.aside_token([act(A2["graymaiden"], "Gray Maiden (3)"), act(A2["physician"], "Queen's Physician (2)")])))

area2("F5", "The Catwalks", SR("F5", 113)
  + "<p>Catwalks ring the warehouse's upper level over the treatment floor — the physicians' route between wards. Gray Maidens patrol here.</p>"
  + B.enc("Catwalk patrol", encx([3, 3], 7),
     "<p>2 "+act(A2["graymaiden"], "Gray Maidens")+" — sword-and-shield in the choke of the catwalk, longbows if the PCs hang back.</p>",
     B.aside_token(["2× "+act(A2["graymaiden"], "Gray Maiden (3)")])))

area2("F7", "Experimentation Ward", SR("F7", 114)
  + "<p>Behind the public wards, the physicians 'treat' captured plague victims — in truth refining and spreading blood veil. The horror here is hard proof of the conspiracy.</p>"
  + B.enc("Physicians at work", encx([2, 2, 2], 7),
     "<p>3 "+act(A2["physician"], "Queen's Physicians")+", flanking in silence for Sneak Attacks.</p>",
     B.aside_token(["3× "+act(A2["physician"], "Queen's Physician (2)")])))

area2("F8", "The Doctor's Office", SR("F8", 116)
  + "<p>"+act(A2["davaulus"], "Dr. Reiner Davaulus")+"'s office, and the concealed stair down to the Temple of Urgathoa. Confronted, he plays the gracious host and tries to talk the PCs away; the moment he senses an attack he turns invisible and flees below.</p>"
  + B.enc("Reiner Davaulus", encx([9], 7),
     "<p>"+act(A2["davaulus"], "Davaulus")+" (bane-rapier Sneak Attacks, Inspire) — usually backed by the F5/F7 staff if alarmed. He flees to the Temple rather than die in the open.</p>",
     B.aside_token([act(A2["davaulus"], "Reiner Davaulus (9)")]))
  + B.s_conv("<p>His notes (here, or relocated to G14 if the PCs were fooled) confirm the manufactured plague. The stair down begins the <strong>Temple of Urgathoa</strong>.</p>"))

# --- Part 3: the Temple of Urgathoa (G) ---
PG("The Temple of Urgathoa", SR("Temple of Urgathoa", 118)
  + B.s_milestone("<p><strong>G. The Temple of Urgathoa</strong> — the cult's hidden warren beneath the hospice, where blood veil is brewed and the dying are 'harvested.' Andaisin pre-buffs her lieutenants (<em>status</em>) each morning and rallies the temple the moment the alarm sounds.</p>")
  + B.s_skill("<p>Staffed by zealous "+act(A2["cultist"], "cultists of Urgathoa")+" (and the negotiable nosferatu "+act(A2["ramoska"], "Ramoska")+" in his lab). Stealth and speed matter — a roused temple converges on the Inner Sanctum.</p>"))

area2("G2", "Guard Post", SR("G2", 118)
  + "<p>The temple's first defended threshold. "+act(A2["cultist"], "Cultists")+" (and any Gray Maidens who followed Davaulus down) hold the entry and raise the alarm.</p>"
  + B.enc("Temple guards", encx([3, 3, 3], 7),
     "<p>3 "+act(A2["cultist"], "cultists of Urgathoa")+" — scythes and void-channeling; they fight to the death.</p>",
     B.aside_token(["3× "+act(A2["cultist"], "Cultist of Urgathoa (3)")])))

area2("G5", "Operating Room", SR("G5", 120)
  + "<p>A blood-slick surgery where the cult vivisects victims to study the disease.</p>"
  + B.enc("Cult surgeons", encx([3, 3], 7),
     "<p>2 "+act(A2["cultist"], "cultists")+" mid-operation.</p>",
     B.aside_token(["2× "+act(A2["cultist"], "Cultist of Urgathoa (3)")])))

area2("G7", "Cult Quarters", SR("G7", 122)
  + "<p>The cultists' barracks. If the alarm is up, expect the off-duty zealots here to reinforce elsewhere.</p>"
  + B.enc("Off-duty cult", encx([3, 3, 3, 3], 7),
     "<p>4 "+act(A2["cultist"], "cultists of Urgathoa")+".</p>",
     B.aside_token(["4× "+act(A2["cultist"], "Cultist of Urgathoa (3)")])))

area2("G8", "The Blood Vats", SR("G8", 122)
  + "<p>Great vats where tainted blood is rendered into blood veil — the production heart of the plague. Destroying the vats (and the death's-head coffers' work) is a major blow.</p>"
  + B.enc("Vat-tenders", encx([3, 3, 3, 3, 3, 3], 7),
     "<p>6 "+act(A2["cultist"], "cultists")+" tending the vats — a <strong>Severe</strong> swarm if met all at once; thin them in the approach.</p>",
     B.aside_token(["6× "+act(A2["cultist"], "Cultist of Urgathoa (3)")])))

area2("G11", "Arkminos's Laboratory", SR("G11", 124)
  + "<p>The nosferatu "+act(A2["ramoska"], "Ramoska Arkminos")+"'s imported laboratory, where he tests Varisian plague-immunity on the captive "+"<strong>Ruan Mirukova</strong> (Deyanira's brother, very much alive).</p>"
  + SEC("<p><strong>Do not simply fight him.</strong> Ramoska is a CR-14-equivalent foe far above the party and wants no part of the cult's cause. He will <strong>sell Ruan and leave</strong> — for coin (~200 gp re-scaled), a magic item, a future favor, or the last <em>death's head coffer</em> from G14. Attacked, he fights savagely but Dimensional-Steps away rather than be destroyed.</p>")
  + B.enc("Ramoska Arkminos (only if forced)", encx([13], 7),
     "<p>"+act(A2["ramoska"], "Ramoska")+" — Drain Life, Contagion, caustic bombs, fast healing 5, nosferatu resilience. <strong>An almost-unwinnable straight fight at this level; the intended path is the bargain.</strong></p>",
     B.aside_token([act(A2["ramoska"], "Ramoska Arkminos (13)")]))
  + B.s_treasure("<p>Free Ruan (bargain or battle) to complete the Carowyn thread and earn the Mirukovas' lasting gratitude. Ramoska's lab is a trove of alchemical and disease lore (GM-scaled).</p>"))

area2("G13", "Hall of Pestilence", SR("G13", 132)
  + "<p>The defiled approach to the Inner Sanctum, lined with Urgathoan iconography of feast and rot. Andaisin's last guards make their stand.</p>"
  + B.enc("Sanctum guards", encx([3, 3], 7),
     "<p>2 "+act(A2["cultist"], "cultists")+" (one bearing Andaisin's <em>status</em> — her early warning).</p>",
     B.aside_token(["2× "+act(A2["cultist"], "Cultist of Urgathoa (3)")])))

area2("G14", "The Inner Sanctum", SR("G14", 132)
  + box("Inner Sanctum of Urgathoa",
        "<p>The Inner Sanctum reeks of incense and corruption — an altar to the Pallid Princess slick with old blood, the last death's-head coffer upon it. Here Lady Andaisin awaits, scythe in hand, serene with terrible faith.</p>")
  + "<p>"+act(A2["andaisin"], "Lady Andaisin")+", high priestess of Urgathoa, is the chapter's villain made flesh — and she does not die easily.</p>"
  + B.enc("BOSS — Lady Andaisin", encx([9], 7),
     "<p>"+act(A2["andaisin"], "Andaisin")+" buffs, air-walks aloft, and rains Slay Living / Greater Command / Harm before dropping into scythe range; she mists-and-heals when low.</p>",
     B.aside_token([act(A2["andaisin"], "Lady Andaisin (9)")]))
  + B.enc("CLIMAX — Andaisin, Daughter of Urgathoa", encx([11], 7),
     "<p>The instant Andaisin dies, Urgathoa's blessing erupts: she rises as "+act(A2["andaisin_t"], "a Daughter of Urgathoa")+" — a Large undead horror with reach claws, a devouring maw, a pestilent aura, and plague-bearing wounds. <strong>An Extreme-tier climax; the true end of Chapter 2.</strong></p>",
     B.aside_token([act(A2["andaisin_t"], "Andaisin, Daughter of Urgathoa (11)")]))
  + B.s_treasure("<p>On the altar: the final <strong>death's-head coffer</strong> (the plague-engine — Ramoska covets it; destroying it ends the seeding), Andaisin's +2 vicious scythe and +2 breastplate, a belt of mighty constitution, a cloak of resistance, a headband of wisdom, and the cult's hoard (re-scaled).</p>")
  + B.s_conv("<p>With Andaisin destroyed and the vats and coffer ended, the manufactured plague's <strong>source</strong> is broken — but per the persistent-plague overlay (Conversion Guide → Blood Veil), the cult's re-seeding only <em>suppresses</em>, and the Epidemic Clock continues until Ileosa falls in Chapter 6.</p>"))

PG("Chapter Conclusion", SR("Chapter Conclusion", 132)
  + B.s_milestone("<p><strong>Chapter Conclusion.</strong> The Hospice and Temple fall, Davaulus and Andaisin are dead (or fled), and Korvosa's acute outbreak breaks. The PCs should be 8th level. But the victory is bittersweet — the city is scarred, the Gray Maidens entrenched, and Old Korvosa now sealed under quarantine.</p>")
  + SEC("<p><strong>Into Chapter 3.</strong> The crafted cure <strong>suppresses</strong> rather than eradicates (persistent-plague overlay): set the Epidemic Clock from the Survivor Count tally across the missions. The quarantine of Old Korvosa and the captured seneschal <strong>Neolandus</strong> (held by the Arkonas) launch 'Escape from Old Korvosa.' If Davaulus was duped-and-fled, the Red Mantis now hunt the PCs there.</p>")
  + B.s_conv("<p><strong>Threads forward:</strong> the persistent plague + Epidemic Clock · the Gray Maidens (now a standing enemy) · Rolth's vendetta and his immunity research · Ramoska loose with his bargain (or destroyed) · Trinia & Vencarlo · the Arkonas + Neolandus → Chapter 3.</p>"))

journal = B.journal_entry(JID2, "2. Seven Days to the Grave", pages, folder=ADV_FOLDER)
B.write("journals", "02-seven-days-to-the-grave", copy.deepcopy(journal), embed_pages=True)

print(f"Chapter 2 (front matter) built: {len(folders)} folders, {len(actors)} actors, 1 journal ({len(pages)} pages).")
