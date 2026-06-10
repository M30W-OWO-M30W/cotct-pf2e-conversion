#!/usr/bin/env python3
"""Chapter 5 — Skeletons of Scarwall. Party L13 -> 15+.

The cursed castle in Belkzen: the Scarwall Curse + Spiritual Doom systems, the
Lords of Scarwall, the four spirit anchors + Mithrodar the chained spirit, and
Serithtial beneath the Sacred Lake. ~137 keyed areas, clustered by wing.
"""
from __future__ import annotations
import copy
import pf2e_build as B

MODID = "cotct-pf2e-conversion"
ACTOR_ROOT, ADV_FOLDER = "cotctActorRoot01", "cotctAdvFolder01"

JID5 = "ch5SkelScarwall1"
A5 = {"deadwatcher": "deadwatcherOrc01", "ury": "urySevenskulls01", "gargbrute": "gargoyleBrute001",
      "scarguard": "scarwallGuard001", "lashton": "lashtonDreadSk01", "skelnightmare": "skelNightmare001",
      "corpseorgy": "corpseOrgy000001", "mandraivus": "mandraivusLost01", "cinderghoul": "cinderGhoul00001",
      "belshallam": "belshallamUmbr01", "ukwar": "ukwarFext0000001", "castothrane": "castothraneSk001",
      "nihil": "nihilDevil000001", "aerilaya": "aerilayaBanshe01", "gorstav": "gorstavJuju00001",
      "mingorc": "mingorcDonjon001", "aruth": "prelateAruth0001", "zev": "zevRavenkaDemi01",
      "ildervok": "ildervokNight001", "kleestad": "kleestadPharma01", "mithrodar": "mithrodarChain01",
      "sial": "shadowcountSial1",
      "vortexmadness": "vortexMadness001", "crematoryblast": "crematoryBlast01", "obsessionhaunt": "obsessionHaunt01",
      "curseworm": "curseOfTheWorm01", "dansemacabre": "danseMacabre0001", "polongbottles": "polongBottles001"}
F5 = {"a_ch5": "ch5ActorFolder01", "a_creatures": "ch5CreaturesFld1", "a_hazards": "ch5HazardsFld001"}

ids = B._idgen(550005)
def nid(): return next(ids)
sids = B._idgen(885005)
def sid(): return next(sids)

def act(_id, label): return f"@UUID[Compendium.{MODID}.cotct-actors.Actor.{_id}]{{{label}}}"
def haz(_id, label): return f"@UUID[Compendium.{MODID}.cotct-hazards.Actor.{_id}]{{{label}}}"
def chk(s): return f"@Check[{s}]"
def SEC(html): return B.s_secret(html, sid())
def box(anchor, fb):
    t = B.verbatim(anchor)
    return B.s_read("<p>" + t + "</p>") if t else B.s_read(fb)
CHC = "#8a1a1a"

for f in [B.folder(F5["a_ch5"], "5. Skeletons of Scarwall", "Actor", ACTOR_ROOT, 500000, CHC),
          B.folder(F5["a_creatures"], "Creatures", "Actor", F5["a_ch5"], 100000, None, "a"),
          B.folder(F5["a_hazards"], "Hazards", "Actor", F5["a_ch5"], 200000, None, "a")]:
    B.write("actors", "_folder_ch5-" + f["name"].lower().replace(" ", "-").replace(".", "") + "-act", copy.deepcopy(f))

# mirror the folder chain into the hazards pack (per-pack folder docs)
for hf in [B.folder(F5["a_ch5"], "5. Skeletons of Scarwall", "Actor", ACTOR_ROOT, 500000, CHC),
           B.folder(F5["a_hazards"], "Hazards", "Actor", F5["a_ch5"], 200000, None, "a")]:
    B.write("hazards", "_folder_hz5-" + hf["name"].lower().replace(" ", "-").replace(".", ""), copy.deepcopy(hf))

actors = []
def AW(slug, doc):
    actors.append(copy.deepcopy(doc)); B.write("actors", slug, doc, embed_items=True)

AW("deadwatcher-orc", B.npc(A5["deadwatcher"], "Deadwatcher Orc", 7, 25, 110, 16, 13, 11, 14,
  {"str": 5, "dex": 2, "con": 4, "int": -1, "wis": 1, "cha": 0}, 25,
  {"athletics": 17, "intimidation": 13, "survival": 13}, ["humanoid", "orc"], ["orcish"],
  [B.strike(nid(), "Greataxe", 18, "2d12+8", "slashing", ["sweep"]),
   B.strike(nid(), "Javelin", 15, "1d6+8", "piercing", ["thrown-30"]),
   B.action(nid(), "Death-Inured", "passive", "<p>Generations beside the cursed causeway: +2 status to saves vs. fear and death effects; they do not flinch at undead.</p>", category="defensive"),
   B.action(nid(), "Ferocity", "reaction", "<p><strong>Trigger</strong> Reduced to 0 HP.</p><hr /><p><strong>Effect</strong> Stays at 1 HP and "+B.cond("wounded", "Wounded 1")+".</p>")],
  notes="<p><strong>Role:</strong> the Deadwatchers — the orc tribe squatting in Scarwall's barbican, the only Belkzen clan hard enough to live beside the curse. They hold the gate under "+act(A5["ury"], "Ury Sevenskulls")+" and want no part of the castle proper.</p>",
  folder=F5["a_creatures"], senses=[{"type": "darkvision"}], blurb="Barbican orc of the Deadwatchers", token_src=None))

AW("ury-sevenskulls", B.npc(A5["ury"], "Ury Sevenskulls", 10, 30, 190, 21, 16, 16, 18,
  {"str": 6, "dex": 2, "con": 5, "int": 0, "wis": 1, "cha": 2}, 25,
  {"athletics": 22, "intimidation": 20, "survival": 16}, ["humanoid", "orc"], ["orcish", "common"],
  [B.strike(nid(), "+1 Striking Greataxe", 23, "2d12+12", "slashing", ["magical", "sweep"]),
   B.action(nid(), "Skull-Taker's Sweep", "2", "<p>A Greataxe Strike against each of two adjacent foes; a critical hit also knocks the target "+B.cond("prone", "Prone")+".</p>", ["flourish"]),
   B.action(nid(), "Seven Skulls Roar", "1", "<p>Demoralize all foes within 30 feet with one Intimidation check (his necklace of seven champion-skulls rattling).</p>", ["auditory", "emotion", "fear", "mental"]),
   B.action(nid(), "Ferocity", "reaction", "<p>As his warriors' — he dies standing or not at all.</p>")],
  notes="<p><strong>Role:</strong> Deadwatcher chieftain (A10). Pragmatic for an orc: the PCs can <strong>fight through the barbican or talk past it</strong> — "+chk("type:intimidation|dc:28")+" or "+chk("type:diplomacy|dc:32")+" (or a worthy gift/duel) buys passage; the Deadwatchers will not follow anyone inside. His seven-skull necklace is a Belkzen legend.</p>",
  folder=F5["a_creatures"], senses=[{"type": "darkvision"}], blurb="Deadwatcher chieftain of the barbican", token_src=None, actor_link=True))

AW("gargoyle-brute", B.npc(A5["gargbrute"], "Gargoyle Brute", 9, 28, 155, 19, 15, 15, 17,
  {"str": 6, "dex": 3, "con": 5, "int": -2, "wis": 2, "cha": -1}, 30,
  {"athletics": 20, "stealth": 19}, ["earth", "gargoyle"], ["petran"],
  [B.strike(nid(), "Claw", 21, "2d10+9", "slashing", ["agile"]),
   B.strike(nid(), "Horns", 21, "2d12+9", "piercing", []),
   B.action(nid(), "Freeze", "1", "<p>Statue-still: indistinguishable from Scarwall's grotesques ("+chk("type:perception|dc:29")+" vs. its Stealth).</p>", ["concentrate"], "defensive"),
   B.action(nid(), "Stone Hide", "passive", "<p>Resistance physical 8 (except adamantine).</p>", category="defensive")],
  notes="<p><strong>Role:</strong> the castle's living grotesques — gargoyle packs roosting on the minarets (D8) and parapets, swooping on anything that crosses the open courts. Encounters scale by roost: 2 (a patrol) to 8 (the full minaret flock).</p>",
  folder=F5["a_creatures"], senses=[{"type": "darkvision"}], blurb="Scarwall grotesque-pack gargoyle", token_src=None))

AW("scarwall-guard", B.npc(A5["scarguard"], "Scarwall Guard", 7, 25, 100, 15, 11, 13, 14,
  {"str": 5, "dex": 1, "con": 0, "int": -3, "wis": 1, "cha": 0}, 25,
  {"athletics": 16}, ["undead", "skeleton"], [],
  [B.strike(nid(), "Bastard Sword", 18, "2d8+8", "slashing", ["two-hand-d12"]),
   B.strike(nid(), "Longbow", 16, "2d8+4", "piercing", ["deadly-d10", "range-increment-100", "volley-30"]),
   B.action(nid(), "Eternal Post", "passive", "<p>Mithrodar's eyes: when a guard 'falls,' its spirit reports — rooms know the PCs are coming. Skeleton: immune to death effects, disease, mental, paralysis, poison, unconscious; resistance cold 10, piercing 10, slashing 10.</p>", category="defensive")],
  notes="<p><strong>Role:</strong> the garrison that never went off duty — armored skeletal soldiers at every watchpost (B3, B17, C2, C13, D9, E3…), still walking their patrol routes after five centuries. Numbers per area card; they raise alarms by dying.</p>",
  folder=F5["a_creatures"], senses=[{"type": "darkvision"}], blurb="Skeletal garrison soldier", token_src=None))

AW("lashton", B.npc(A5["lashton"], "Lashton", 10, 30, 175, 19, 17, 18, 19,
  {"str": 6, "dex": 4, "con": 0, "int": 1, "wis": 2, "cha": 3}, 30,
  {"athletics": 21, "intimidation": 19}, ["undead", "skeleton"], ["common"],
  [B.strike(nid(), "+1 Striking Lance", 23, "2d8+11", "piercing", ["deadly-d8", "jousting-d6", "magical", "reach-10"]),
   B.action(nid(), "Watch Commander's Charge", "2", "<p>Mounted on his "+act(A5["skelnightmare"], "skeletal nightmare")+", Lashton Strides (the mount moves) and Strikes with the lance: +4 circumstance damage if he moved 20+ feet.</p>", ["attack"]),
   B.action(nid(), "Dread Rebuke", "1", "<p>One creature within 30 feet: "+chk("type:will|dc:29")+" or "+B.cond("frightened", "Frightened 2")+" — five hundred years of garrison discipline in a dead voice.</p>", ["auditory", "emotion", "fear", "mental"]),
   B.action(nid(), "Dread Skeleton", "passive", "<p>Skeleton immunities; resistance cold/piercing/slashing 10; his fall alerts the keep.</p>", category="defensive")],
  notes="<p><strong>Role:</strong> Scarwall's eternal watch commander — Lord of the causeway gate (B1), patrolling with his "+act(A5["skelnightmare"], "skeletal nightmare")+" mount and a dozen skeletal champions. The PCs' formal welcome to the castle.</p>",
  folder=F5["a_creatures"], senses=[{"type": "darkvision"}], blurb="Dread-skeleton watch commander (B1)", token_src=None, actor_link=True))

AW("skeletal-nightmare", B.npc(A5["skelnightmare"], "Skeletal Nightmare", 7, 25, 105, 17, 14, 12, 13,
  {"str": 5, "dex": 3, "con": 0, "int": -4, "wis": 1, "cha": 0}, 40,
  {"athletics": 17}, ["undead", "skeleton", "beast"], [],
  [B.strike(nid(), "Hooves", 18, "2d8+7", "bludgeoning", ["agile"], [("1d6", "fire")]),
   B.strike(nid(), "Bite", 18, "2d10+7", "piercing", []),
   B.action(nid(), "Smoldering Gallop", "2", "<p>It Strides twice through the air (fly 60), leaving a 5-ft trail of choking smoke (concealment) for 1 round.</p>", ["move"]),
   B.action(nid(), "Skeletal Mount", "passive", "<p>Skeleton immunities; fire immunity; resistance cold/piercing/slashing 10.</p>", category="defensive")],
  notes="<p><strong>Role:</strong> the burned bones of Kazavon's hell-steeds — Lashton's mount and the stable-dead of the courtyard. Flaming hooves, smoke-trailing flight.</p>",
  folder=F5["a_creatures"], senses=[{"type": "darkvision"}], size="lg", other_speeds=[{"type": "fly", "value": 60}],
  blurb="Burned hell-steed skeleton", token_src=None))

AW("cinder-ghoul", B.npc(A5["cinderghoul"], "Cinder Ghoul", 9, 27, 135, 17, 18, 15, 17,
  {"str": 4, "dex": 5, "con": 0, "int": -1, "wis": 2, "cha": 1}, 30,
  {"acrobatics": 19, "stealth": 19}, ["undead", "ghoul", "fire"], ["necril"],
  [B.strike(nid(), "Charred Claw", 21, "2d8+7", "slashing", ["agile"], [("1d6", "fire")]),
   B.strike(nid(), "Jaws", 21, "2d10+7", "piercing", [], [("1d6", "fire")]),
   B.action(nid(), "Smoke Inhalation", "1", "<p><strong>Requirement</strong> Adjacent to a creature.</p><hr /><p><strong>Effect</strong> It exhales its body-smoke: "+chk("type:fortitude|dc:27")+" or "+B.cond("sickened", "Sickened 1")+" and "+B.cond("dazzled", "Dazzled")+" 1 round.</p>", ["incapacitation"]),
   B.action(nid(), "Ghoul Paralysis", "passive", "<p>A creature damaged by its claws: "+chk("type:fortitude|dc:27")+" or "+B.cond("paralyzed", "Paralyzed")+" 1 round (incapacitation; elves immune).</p>", category="offensive")],
  notes="<p><strong>Role:</strong> the kitchen dead (B15) — servants who burned in the great ovens when Mandraivus's invasion torched the kitchens, risen hungry and still smoldering. They hunt with the "+haz(A5["crematoryblast"], "Crematory Blast")+" haunt.</p>",
  folder=F5["a_creatures"], senses=[{"type": "darkvision"}], blurb="Smoldering kitchen ghoul (B15)", token_src=None))

AW("corpse-orgy", B.npc(A5["corpseorgy"], "Corpse Orgy", 13, 33, 270, 24, 18, 21, 23,
  {"str": 7, "dex": 3, "con": 0, "int": -2, "wis": 2, "cha": 4}, 20,
  {"athletics": 27, "stealth": 21}, ["undead"], ["necril"],
  [B.strike(nid(), "Grasping Limbs", 27, "3d10+11", "bludgeoning", ["agile", "reach-15"]),
   B.action(nid(), "Engulf the Living", "2", "<p>It rolls over every creature in a 10-ft burst within reach: "+chk("type:reflex|dc:33")+" or be pulled into the writhing mass — "+B.cond("grabbed", "Grabbed")+" (Escape DC 33) and @Damage[3d10+11[bludgeoning]] per round inside.</p>", ["attack"]),
   B.action(nid(), "Moan of the Mass", "1", "<p>A hundred mouths at once: creatures within 30 feet, "+chk("type:will|dc:31")+" or "+B.cond("frightened", "Frightened 1")+" and "+B.cond("sickened", "Sickened 1")+".</p>", ["auditory", "emotion", "fear", "mental"]),
   B.action(nid(), "Amalgam Resilience", "passive", "<p>Undead immunities; resistance physical 10 (it is everyone it has absorbed). Destroying it releases a sigh from a hundred throats.</p>", category="defensive")],
  notes="<p><strong>Role:</strong> the Death Chamber's horror (B4) — the castle's massacred court, fused by the curse into one rolling mass of the dead. One of the first true horrors of the keep.</p>",
  folder=F5["a_creatures"], senses=[{"type": "darkvision"}], size="grg", blurb="Fused mass of the massacred court (B4)", token_src=None))

AW("mandraivus-the-lost", B.npc(A5["mandraivus"], "Mandraivus the Lost", 13, 33, 250, 21, 22, 24, 24,
  {"str": 0, "dex": 6, "con": 0, "int": 2, "wis": 4, "cha": 6}, 0,
  {"athletics": 22, "intimidation": 24, "religion": 22}, ["undead", "ghost", "incorporeal"], ["common", "shoanti"],
  [B.strike(nid(), "Ghostly Bastard Sword", 27, "3d8+9", "force", ["agile", "magical"]),
   B.action(nid(), "Hero's Lament", "2", "<p>A 30-ft cone of remembered failure: @Damage[8d6[mental]] ("+chk("type:will|dc:33|basic:true")+"); failures are "+B.cond("frightened", "Frightened 2")+".</p>", ["concentrate", "emotion", "mental"]),
   B.action(nid(), "Frightful Presence", "passive", "<p>60-ft aura: "+chk("type:will|dc:31")+" or "+B.cond("frightened", "Frightened 1")+" on first sight.</p>", category="offensive"),
   B.action(nid(), "Ghost Resilience", "passive", "<p>Incorporeal; resistance all 15 (except force, ghost touch, vitality); rejuvenates in the Vortex of Madness until his anguish is answered.</p>", category="defensive")],
  notes="<p><strong>Role:</strong> the hero who slew Kazavon — murdered here (B5) by the traitor Kleestad minutes after his victory, and bound by the curse beside the "+haz(A5["vortexmadness"], "Vortex of Madness")+". He attacks all who approach… unless calmed: speaking his name, Serithtial's, or showing Shoanti regalia earns "+chk("type:diplomacy|dc:34")+" to reach the hero inside ("+chk("type:religion|dc:30")+" reveals his rejuvenation). Laid to rest — or told Serithtial will be carried against Kazavon's seed — he yields his blessing instead of his blade: <strong>+1 status to saves vs. the castle's fear effects</strong> for the party, and the truth of Kleestad's treason.</p>",
  folder=F5["a_creatures"], senses=[{"type": "darkvision"}], blurb="Ghost of Kazavon's slayer (B5)", token_src=None, actor_link=True))

# ---- The Lords, the anchors, the deep ----
AW("belshallam", B.npc(A5["belshallam"], "Belshallam", 15, 37, 320, 28, 24, 26, 28,
  {"str": 8, "dex": 3, "con": 6, "int": 2, "wis": 3, "cha": 5}, 40,
  {"athletics": 31, "intimidation": 29, "stealth": 25, "arcana": 25}, ["dragon", "shadow"], ["common", "draconic", "shadowtongue"],
  [B.strike(nid(), "Jaws", 31, "3d12+14", "piercing", ["reach-15"], [("3d6", "void")]),
   B.strike(nid(), "Claw", 31, "3d10+14", "slashing", ["agile", "reach-10"]),
   B.strike(nid(), "Tail", 29, "3d8+14", "bludgeoning", ["reach-20"]),
   B.action(nid(), "Umbral Breath", "2", "<p><strong>Frequency</strong> once per 1d4 rounds. A 60-ft cone of devouring shadow: @Damage[15d6[void]] ("+chk("type:reflex|dc:37|basic:true")+"); living creatures that critically fail are "+B.cond("drained", "Drained 2")+".</p>", ["arcane", "void"]),
   B.action(nid(), "Draconic Frenzy", "2", "<p>Two Claw Strikes and one Tail Strike.</p>", ["flourish"]),
   B.action(nid(), "Frightful Presence", "passive", "<p>90-ft aura, "+chk("type:will|dc:33")+" — the dark below the War Tower has teeth.</p>", category="offensive"),
   B.action(nid(), "SPIRIT ANCHOR", "passive", "<p><strong>One of Mithrodar's four anchors.</strong> While Belshallam exists, the chained spirit cannot be destroyed. Slaying him (or severing the anchor with <em>dispel evil</em>-grade magic) advances the curse-breaking by one stage.</p>", category="defensive")],
  notes="<p><strong>Role:</strong> umbral dragon Lord of the lower halls (B23) — Kazavon's last living lieutenant in the castle, anchor-bound and resentful. He cares for nothing beyond his lair, his tenebrous-worm 'pets' (B22 — four shadow-worms he is fattening into gloomwings), and his hoard (B24). <strong>Negotiable in bad faith:</strong> he'll trade castle-lore for treasure, then betray.</p>",
  folder=F5["a_creatures"], senses=[{"type": "darkvision"}], size="grg",
  other_speeds=[{"type": "fly", "value": 120}], blurb="Umbral dragon; SPIRIT ANCHOR (B23)", token_src=None, actor_link=True))

AW("ukwar", B.npc(A5["ukwar"], "Ukwar", 12, 32, 230, 22, 18, 19, 21,
  {"str": 6, "dex": 3, "con": 0, "int": 0, "wis": 2, "cha": 3}, 25,
  {"athletics": 24, "intimidation": 22}, ["undead", "fext"], ["orcish", "necril"],
  [B.strike(nid(), "+1 Striking Falchion", 25, "2d10+12", "slashing", ["forceful", "magical", "sweep"]),
   B.action(nid(), "Nearly Indestructible", "passive", "<p>A fext's pact-flesh: resistance <strong>all damage 10</strong> (bypassed only by <em>cold iron</em>); immune to death effects, disease, paralysis, poison.</p>", category="defensive"),
   B.action(nid(), "Court of Dead Orcs", "1", "<p>Ukwar commands his orc-spirit retainers: one wraith-servant Strides and Strikes.</p>", ["auditory"]),
   B.action(nid(), "Host's Wrath", "2", "<p>Two Falchion Strikes; if both hit, the target is "+B.cond("grabbed", "Grabbed")+" by spectral orc hands (Escape DC 32).</p>", ["flourish"])],
  notes="<p><strong>Role:</strong> the only Deadwatcher chieftain who answered the castle's call — now an undead <strong>fext</strong> holding mock court in the guest wing (B29), served by orc spirits. The wing's master; Pegg and Loute (B26 — two L6 ettin-spawn 'entertainers,' run as Elite official ogres with juggled cleavers) perform for him.</p>",
  folder=F5["a_creatures"], senses=[{"type": "darkvision"}], blurb="Fext lord of the guest wing (B29)", token_src=None, actor_link=True))

AW("castothrane", B.npc(A5["castothrane"], "Castothrane", 12, 33, 220, 23, 17, 19, 20,
  {"str": 6, "dex": 2, "con": 0, "int": 1, "wis": 2, "cha": 2}, 25,
  {"athletics": 24, "intimidation": 22, "society": 18}, ["undead", "skeleton"], ["common", "infernal"],
  [B.strike(nid(), "+1 Striking Bastard Sword", 26, "2d8+12", "slashing", ["magical", "two-hand-d12"]),
   B.action(nid(), "Captain's Phalanx", "1", "<p>All skeletal undead within 60 feet gain +1 status to AC and attacks for 1 round — the gatehouse fights as one body.</p>", ["auditory"]),
   B.action(nid(), "Five Centuries' Parry", "reaction", "<p><strong>Trigger</strong> Hit by a Strike.</p><hr /><p><strong>Effect</strong> +2 circumstance AC against it.</p>"),
   B.action(nid(), "SPIRIT ANCHOR", "passive", "<p><strong>One of Mithrodar's four anchors.</strong> Skeleton immunities; resistance cold/piercing/slashing 12. His fall rings the curse one stage looser.</p>", category="defensive")],
  notes="<p><strong>Role:</strong> Kazavon's captain of the guard, a skeletal champion lord commanding the gatehouse dead (D1, with the loft's garrison). Anchor the party likely breaks first — and the castle <em>screams</em> when any anchor falls (all Scarwall undead gain +4 to resist vitality until the curse breaks).</p>",
  folder=F5["a_creatures"], senses=[{"type": "darkvision"}], blurb="Skeletal captain; SPIRIT ANCHOR (D1)", token_src=None, actor_link=True))

AW("nihil", B.npc(A5["nihil"], "Nihil", 14, 35, 280, 24, 23, 24, 25,
  {"str": 7, "dex": 5, "con": 4, "int": 3, "wis": 3, "cha": 5}, 35,
  {"acrobatics": 27, "stealth": 27, "deception": 25, "religion": 23}, ["fiend", "devil"], ["common", "infernal", "shadowtongue"],
  [B.strike(nid(), "Shadow-Barbed Chain", 29, "3d8+13", "slashing", ["magical", "reach-15", "trip", "unholy"], [("2d6", "void")]),
   B.action(nid(), "Assassin's Gift", "2", "<p>Against an "+B.cond("off-guard", "Off-Guard")+" creature: a Chain Strike that deals +3d6 precision and forces "+chk("type:fortitude|dc:34")+" or "+B.cond("enfeebled", "Enfeebled 2")+" (Zon-Kuthon's gift was a killer, not a soldier).</p>", ["attack"]),
   B.action(nid(), "Chains of Night", "2", "<p>Shadow-chains erupt in a 15-ft burst within 60 feet: "+chk("type:reflex|dc:34")+" or "+B.cond("grabbed", "Grabbed")+" (Escape DC 34) and @Damage[4d6[void]].</p>", ["concentrate", "divine", "shadow"]),
   B.action(nid(), "SPIRIT ANCHOR", "passive", "<p><strong>One of Mithrodar's four anchors</strong> — bound by the chains, not loyalty. Devil immunities (fire; bleed; resistance physical 10 except silver). <em>He wants to be free:</em> clever PCs may bargain his cooperation against the others — though severing his anchor is the only freedom the chains allow.</p>", category="defensive")],
  notes="<p><strong>Role:</strong> Zon-Kuthon's gift-assassin to Kazavon, imprisoned by Mithrodar's network in the Tower of Kazavon (D14). The anchor with an agenda — and the best conversation in the Heights.</p>",
  folder=F5["a_creatures"], senses=[{"type": "darkvision"}], blurb="Chained devil-assassin; SPIRIT ANCHOR (D14)", token_src=None, actor_link=True))

AW("aerilaya", B.npc(A5["aerilaya"], "Aerilaya", 13, 33, 240, 20, 22, 25, 24,
  {"str": 0, "dex": 6, "con": 0, "int": 3, "wis": 4, "cha": 7}, 0,
  {"stealth": 25, "arcana": 23, "intimidation": 25}, ["undead", "incorporeal", "spirit"], ["common", "elven", "necril"],
  [B.strike(nid(), "Spectral Touch", 27, "3d10+8", "void", ["agile", "magical"]),
   B.action(nid(), "Wail", "2", "<p><strong>Frequency</strong> once per day (her opener from the cupola, D16). All living creatures within 40 feet: "+chk("type:fortitude|dc:33")+"; critical failure = dropped to 0 HP and "+B.cond("dying", "Dying 1")+"; failure = @Damage[8d10[void]]; success = half.</p>", ["auditory", "death", "incapacitation"]),
   B.action(nid(), "Spellstrike Memory", "2", "<p>In life a magus: a ray of frost-and-shadow, spell attack +25, @Damage[6d8[cold]] plus "+B.cond("slowed", "Slowed 1")+" on a critical hit.</p>", ["arcane", "cold"]),
   B.action(nid(), "Banshee Resilience", "passive", "<p>Incorporeal; resistance all 15 (except force/ghost touch/vitality); sunlight powerlessness (she keeps to the tower's shadow).</p>", category="defensive")],
  notes="<p><strong>Role:</strong> Kazavon's elf-assassin and rare arcanist, now the banshee watching Scarwall's skies from the cupola (D16) with two bone devils (run as Elite "+B.mon("war-wraith", "war-wraiths")+" if no devil stats are at hand). <strong>Any aerial approach</strong> (the Air Approach hazard) answers to her first.</p>",
  folder=F5["a_creatures"], senses=[{"type": "darkvision"}], blurb="Banshee sky-warden (D16)", token_src=None, actor_link=True))

AW("gorstav", B.npc(A5["gorstav"], "Gorstav", 13, 33, 260, 24, 19, 21, 22,
  {"str": 7, "dex": 3, "con": 0, "int": 1, "wis": 2, "cha": 2}, 25,
  {"athletics": 27, "intimidation": 23, "society": 19}, ["undead", "zombie"], ["common", "infernal"],
  [B.strike(nid(), "+2 Striking Greatsword", 28, "2d12+13", "slashing", ["magical", "versatile-p"]),
   B.action(nid(), "General's Order", "1", "<p>Every undead soldier within 60 feet Strides or Strikes — the War Tower obeys its general still.</p>", ["auditory"]),
   B.action(nid(), "Executioner's Memory", "passive", "<p>Kazavon beheaded him for failing to stop Mandraivus; the juju zombie remembers. Against anyone carrying <em>Serithtial</em> (or naming Mandraivus): +2 status to attack and damage, and he fights past destruction for 1 round.</p>", category="offensive"),
   B.action(nid(), "Juju Resilience", "passive", "<p>Zombie immunities; resistance physical 10 (except slashing), cold 10, electricity 10; not slowed (juju).</p>", category="defensive")],
  notes="<p><strong>Role:</strong> general of Kazavon's armies, executed minutes before the Star Tower fell — risen as a juju zombie in the War Room (E11) beside the "+haz(A5["curseworm"], "Curse of the Worm")+" haunt. The sayona <strong>Risibeth</strong> (E7 — his old war-commander, run as an Elite "+act(A5["aerilaya"], "Aerilaya")+"-style spirit) trades castle-intelligence for a disturbing taste of living blood: she names three anchors and points to the chapel for the fourth.</p>",
  folder=F5["a_creatures"], senses=[{"type": "darkvision"}], blurb="Juju-zombie general (E11)", token_src=None, actor_link=True))

AW("mingorc", B.npc(A5["mingorc"], "Mingorc", 13, 34, 255, 25, 18, 22, 22,
  {"str": 7, "dex": 2, "con": 5, "int": 0, "wis": 3, "cha": 2}, 25,
  {"athletics": 27, "intimidation": 23, "religion": 21}, ["undead", "giant"], ["jotun", "necril"],
  [B.strike(nid(), "Gravewrought Maul", 28, "3d12+13", "bludgeoning", ["magical", "reach-10", "shove"]),
   B.action(nid(), "Porter's Toll", "reaction", "<p><strong>Trigger</strong> A creature tries to pass his station (F8).</p><hr /><p><strong>Effect</strong> A Maul Strike; on a hit the creature is shoved 10 feet back.</p>"),
   B.action(nid(), "Crushing Sweep", "2", "<p>A Maul Strike against each creature in a 10-ft arc.</p>", ["flourish"]),
   B.action(nid(), "Grave Resilience", "passive", "<p>Undead immunities; resistance physical 10.</p>", category="defensive")],
  notes="<p><strong>Role:</strong> the donjon's undead giant porter (F8) — Zon-Kuthon's chapel suffers no uninvited guests. The toll is blood.</p>",
  folder=F5["a_creatures"], senses=[{"type": "darkvision"}], size="lg", blurb="Undead giant porter of the donjon (F8)", token_src=None))

AW("prelate-aruth", B.npc(A5["aruth"], "Prelate Aruth", 13, 33, 250, 23, 18, 24, 23,
  {"str": 5, "dex": 1, "con": 0, "int": 2, "wis": 6, "cha": 4}, 20,
  {"religion": 25, "intimidation": 23, "occultism": 21}, ["undead", "mummy"], ["common", "infernal", "necril", "shadowtongue"],
  [B.strike(nid(), "Rotting Fist", 26, "3d8+10", "bludgeoning", [], [("2d6", "void")]),
   B.action(nid(), "Mummy Rot", "passive", "<p>A creature damaged by his fist: "+chk("type:fortitude|dc:33")+" or contract mummy rot ("+B.cond("drained", "Drained")+" by stage; cured only by disease-removing magic of 6th rank+).</p>", category="offensive"),
   B.action(nid(), "Midnight Litany", "2", "<p>Zon-Kuthon's pain-prayer, 30-ft burst within 120 feet: @Damage[8d6[mental]] ("+chk("type:will|dc:33|basic:true")+"); failures are "+B.cond("sickened", "Sickened 1")+" with razor-ecstasy.</p>", ["auditory", "divine", "mental"]),
   B.action(nid(), "Despair", "passive", "<p>First sight: "+chk("type:will|dc:31")+" or "+B.cond("paralyzed", "Paralyzed")+" 1 round (incapacitation).</p>", category="offensive")],
  notes="<p><strong>Role:</strong> mummy-lord Prelate of the Dark Shrine — Zev Ravenka's second, holding the private chapel (F10) with his cinder-eyed congregation. Still kneels to the demilich next door.</p>",
  folder=F5["a_creatures"], senses=[{"type": "darkvision"}], blurb="Mummy-lord prelate (F10)", token_src=None, actor_link=True))

AW("zev-ravenka", B.npc(A5["zev"], "Zev Ravenka", 15, 37, 240, 24, 26, 28, 28,
  {"str": 0, "dex": 7, "con": 0, "int": 6, "wis": 5, "cha": 7}, 0,
  {"religion": 29, "arcana": 29, "occultism": 29, "intimidation": 27}, ["undead"], ["common", "infernal", "necril", "shadowtongue"],
  [B.strike(nid(), "Soul-Raking Gaze", 29, "4d8+10", "void", ["magical", "range-increment-30"]),
   B.action(nid(), "Trap Soul", "2", "<p>His signature: one creature within 30 feet, "+chk("type:will|dc:37")+" or its soul is torn into one of his ruby teeth (the body drops, "+B.cond("dying", "Dying 1")+", soulless — death-warded characters resist with the Blessing's <em>Infused Soul</em>). Crushing the gem (Hardness 5) frees the soul. He repeats this every round until bloodied.</p>", ["concentrate", "death", "incapacitation", "necromancy"]),
   B.action(nid(), "Wail of the Banshee", "3", "<p><strong>Below ~20% HP:</strong> all living creatures within 40 feet: "+chk("type:fortitude|dc:37")+"; critical failure = death; failure = @Damage[10d10[void]].</p>", ["auditory", "death", "divine"]),
   B.action(nid(), "SPIRIT ANCHOR / Demilich", "passive", "<p><strong>The fourth anchor.</strong> A skull and dust — he takes 1 round to fully wake when his remains are disturbed. Immune to all but his weaknesses; resistance all 15. <em>Dispel evil</em>-grade magic can sever the anchor without battle — but the attempt itself disturbs his remains.</p>", category="defensive")],
  notes="<p><strong>Role:</strong> Kazavon's religious adviser — a lich who transcended into a <strong>demilich</strong>, drifting as a jeweled skull above the Dark Shrine of Midnight (F11). The hardest anchor. <strong>Treasure is his body:</strong> two ruby eyes (~250 gp each re-scaled) and ten ruby teeth (~100 gp each) — some holding screaming souls.</p>",
  folder=F5["a_creatures"], senses=[{"type": "darkvision"}, {"type": "true-seeing"}], size="tiny",
  other_speeds=[{"type": "fly", "value": 30}], blurb="Demilich; SPIRIT ANCHOR (F11)", token_src=None, actor_link=True))

AW("ildervok", B.npc(A5["ildervok"], "Ildervok", 14, 36, 295, 26, 22, 24, 26,
  {"str": 8, "dex": 4, "con": 5, "int": 2, "wis": 4, "cha": 5}, 30,
  {"stealth": 26, "religion": 24, "intimidation": 26}, ["undead", "nightshade"], ["common", "necril", "shadowtongue"],
  [B.strike(nid(), "Shadow Bite", 30, "3d12+14", "piercing", ["magical", "reach-10"], [("2d6", "void")]),
   B.action(nid(), "Drain Magic", "1", "<p><strong>Requirement</strong> Bite hit a creature bearing magic items.</p><hr /><p><strong>Effect</strong> One of the target's magic items: "+chk("type:fortitude|dc:34")+" (item's owner) or the item is suppressed 1 round (drained of light and power).</p>", ["necromancy"]),
   B.action(nid(), "Umbral Dive", "2", "<p>He folds through shadow up to 120 feet and Strikes from "+B.cond("hidden", "Hidden")+".</p>", ["attack", "shadow", "teleportation"]),
   B.action(nid(), "Nightshade Resilience", "passive", "<p>Undead immunities; resistance all 12 (except vitality and silver); <em>light aversion</em>: "+B.cond("sickened", "Sickened 1")+" in bright light.</p>", category="defensive")],
  notes="<p><strong>Role:</strong> the nightwing of the Star Tower (G7) — sent by <strong>Zon-Kuthon himself</strong> to ward the Chamber of the Well until a new curate takes the post; bound by the god's will, <em>not</em> the curse (he cannot become an anchor). He greets visitors telepathically, invisible above the well: his bargain is simple — <strong>give him a curate, and the way below opens.</strong> Shadowcount Sial wants the job; so, terribly, might Laori.</p>",
  folder=F5["a_creatures"], senses=[{"type": "darkvision"}, {"type": "true-seeing"}], size="grg",
  other_speeds=[{"type": "fly", "value": 60}], blurb="Nightwing warden of the Star Tower (G7)", token_src=None, actor_link=True))

AW("kleestad", B.npc(A5["kleestad"], "Kleestad", 15, 36, 330, 28, 22, 25, 26,
  {"str": 9, "dex": 2, "con": 7, "int": 0, "wis": 3, "cha": 4}, 30,
  {"athletics": 31, "intimidation": 27}, ["undead", "aberration"], ["common", "necril"],
  [B.strike(nid(), "Worm Maw", 31, "3d12+15", "piercing", ["reach-15"], [("2d6", "acid")]),
   B.strike(nid(), "Grasping Hands", 31, "3d8+15", "bludgeoning", ["agile", "reach-10"]),
   B.action(nid(), "Caustic Breath", "2", "<p><strong>Frequency</strong> once per 1d4 rounds. A 60-ft cone of grave-acid: @Damage[14d6[acid]] ("+chk("type:reflex|dc:37|basic:true")+") — opened on the largest knot of PCs.</p>", ["acid"]),
   B.action(nid(), "Traitor's Hunger", "passive", "<p>Against any creature carrying <em>Serithtial</em>: +2 status to attack and damage, and he <strong>pursues to the world's end</strong> if they flee with it.</p>", category="offensive"),
   B.action(nid(), "Pharmakos Bulk", "passive", "<p>Undead immunities; resistance physical 12; <em>air walk</em> at will (he fights striding the lake's surface).</p>", category="defensive")],
  notes="<p><strong>Role:</strong> the chamberlain whose treason opened Scarwall to Mandraivus — and who, denied his promised reward, drowned the hero's sword in the Sacred Lake (H3–H4) and fed. Five centuries of guilt and hunger made him a <strong>pharmakos</strong>: an 80-foot worm of scapegoated sin coiled around <strong>Serithtial</strong> itself. The campaign's last gate before the sword.</p>",
  folder=F5["a_creatures"], senses=[{"type": "darkvision"}], size="grg",
  other_speeds=[{"type": "swim", "value": 40}], blurb="Pharmakos traitor; keeper of Serithtial (H4)", token_src=None, actor_link=True))

AW("mithrodar", B.npc(A5["mithrodar"], "Mithrodar", 16, 38, 320, 26, 27, 29, 30,
  {"str": 0, "dex": 7, "con": 0, "int": 3, "wis": 5, "cha": 8}, 0,
  {"intimidation": 30, "occultism": 28, "religion": 28}, ["undead", "incorporeal", "spirit"], ["common", "infernal", "necril", "shadowtongue"],
  [B.strike(nid(), "Spectral Chains", 31, "4d8+12", "void", ["agile", "magical", "reach-20"]),
   B.action(nid(), "Chain the Living", "2", "<p>Ghost-chains lash a 20-ft burst within 60 feet: "+chk("type:reflex|dc:38")+" or "+B.cond("grabbed", "Grabbed")+" (Escape DC 38) and @Damage[4d8[void]] per round held.</p>", ["concentrate", "divine"]),
   B.action(nid(), "Castle's Voice", "1", "<p>Mithrodar speaks through every wall: all foes in the castle who can hear, "+chk("type:will|dc:36")+" or "+B.cond("frightened", "Frightened 1")+"; his undead gain +1 status to attacks for 1 round.</p>", ["auditory", "fear", "mental"]),
   B.action(nid(), "Spirit Anchors", "passive", "<p><strong>While any of his four anchors exists</strong> (Belshallam B23, Castothrane D1, Nihil D14, Zev Ravenka F11), Mithrodar re-forms 1d4 days after 'destruction' — he <strong>cannot be permanently defeated</strong>. He can chain a new non-mindless evil creature as a replacement anchor (constructs never; Ildervok never — Zon-Kuthon's writ outranks his; <em>Sial or Laori would serve nicely</em>). Per anchor destroyed, the curse sheds a layer: 1 — safe sleep (and the castle screams: all Scarwall undead +4 vs. vitality); 2 — the Aura of Menace ends; 3 — wall-spirits stop roaming; 4 — the <em>unhallow</em> and dimensional lock fall, and he can finally die.</p>", category="defensive"),
   B.action(nid(), "Chained Spirit", "passive", "<p>Incorporeal; resistance all 15 (except force/ghost touch/vitality); the curse's soultrap (see the Curse page) is <em>his</em> reach — he assaults any spirit entering the castle, Zellara above all.</p>", category="defensive")],
  notes="<p><strong>Role:</strong> Scarwall's castellan, hanged in his own chains when Kazavon fell — now the <strong>chained spirit</strong> at the heart of the curse, enthroned in the Great Hall (C14). Every bound soul in the walls is his to spend. <strong>Destroying him (after the four anchors) frees every trapped soul, lifts the curse — and wakes <em>Serithtial</em>.</strong></p>",
  folder=F5["a_creatures"], senses=[{"type": "darkvision"}, {"type": "true-seeing"}], size="lg",
  blurb="The chained spirit; heart of the curse (C14)", token_src=None, actor_link=True))

AW("shadowcount-sial", B.npc(A5["sial"], "Shadowcount Sial", 12, 31, 200, 18, 19, 24, 22,
  {"str": 1, "dex": 4, "con": 2, "int": 4, "wis": 5, "cha": 4}, 25,
  {"religion": 24, "occultism": 22, "deception": 20, "diplomacy": 20, "society": 20}, ["humanoid", "human"], ["common", "infernal", "shadowtongue"],
  [B.strike(nid(), "+1 Striking Spiked Chain", 22, "2d8+7", "slashing", ["disarm", "finesse", "magical", "trip"]),
   B.action(nid(), "Midnight Touch", "2", "<p>Zon-Kuthon's chill: touch, @Damage[6d8[void]] ("+chk("type:fortitude|dc:31|basic:true")+"; "+B.cond("enfeebled", "Enfeebled 1")+" on a failure).</p>", ["divine", "void"]),
   B.action(nid(), "Shadow Body", "2", "<p>Sial becomes living shadow for 1 minute: resistance all 10, Speed 50, may move through gaps.</p>", ["divine", "polymorph", "shadow"], "defensive"),
   B.action(nid(), "Summon Asyra", "2", "<p>He unhooks his iron casket: the bound kyton-eidolon <strong>Asyra</strong> (run as an Elite "+act(A5["nihil"], "chain-devil pattern")+" at L11) unfolds in chains and obeys for 10 minutes.</p>", ["conjuration", "divine"]),
   B.lore(nid(), "Zon-Kuthon Lore", 24)],
  notes="<p><strong>Role:</strong> Brotherhood of Bones shadowcount — Laori's superior, polished where she is chipper, patient where she is gleeful. He and his casket-bound eidolon <strong>Asyra</strong> joined the PCs' orbit at Kaer Maga and have scryed them since Chapter 4 ('The Devil You Know'). The Brotherhood's goal is real: <em>prevent Kazavon's resurrection</em> — and for that, the PCs make excellent chain-breakers. <strong>His endgame:</strong> the Star Tower curacy (G7). Offering Ildervok a willing curate is the 'clean' path below — and the Brotherhood considers it an honor. Whether Sial volunteers, or maneuvers <em>Laori</em> into it, is the chapter's quietest knife-fight.</p>",
  folder=F5["a_creatures"], blurb="Brotherhood shadowcount; would-be curate", token_src=None, actor_link=True))

# ---- hazards ----
hazards = []
def HW(slug, doc):
    hazards.append(copy.deepcopy(doc)); B.write("hazards", slug, doc, embed_items=True)

HW("vortex-of-madness", B.hazard(A5["vortexmadness"], "Vortex of Madness (B5)", 10, 30,
  "<p>"+chk("type:perception|dc:30")+" (trained) to feel the psychic undertow before entering.</p>",
  "<p>Lay "+act(A5["mandraivus"], "Mandraivus")+" to rest, or <em>dispel magic</em> (5th rank) for 1 hour's calm.</p>",
  "<p>The spiritual maelstrom where Mandraivus died — anguish given rotation.</p>",
  [B.action(nid(), "Drowning Despair", "free", "<p><strong>Routine:</strong> creatures in the chamber each round: "+chk("type:will|dc:29")+" or @Damage[4d6[mental]] and "+B.cond("stupefied", "Stupefied 1")+" (cumulative to 3).</p>")],
  folder=F5["a_hazards"], traits=["haunt", "mental"], reset="<p>Permanent until Mandraivus rests.</p>", complex_=True))

HW("crematory-blast", B.hazard(A5["crematoryblast"], "Crematory Blast (B15)", 10, 28,
  "<p>"+chk("type:perception|dc:28")+" to feel the ovens' heat rising before they roar.</p>",
  "<p>"+chk("type:religion|dc:28")+" (cast vitality into the ovens) or douse all four fireboxes.</p>",
  "<p>The kitchen ovens remember the night they were fed people.</p>",
  [B.action(nid(), "Roaring Ovens", "reaction", "<p><strong>Trigger</strong> A living creature crosses the kitchens' midline.</p><hr /><p><strong>Effect</strong> Fire floods the room: @Damage[10d6[fire]] ("+chk("type:reflex|dc:29|basic:true")+") — and the "+act(A5["cinderghoul"], "cinder ghouls")+" attack out of the smoke.</p>")],
  folder=F5["a_hazards"], traits=["haunt", "fire"], reset="<p>1 hour.</p>", complex_=False))

HW("obsession-haunts", B.hazard(A5["obsessionhaunt"], "Obsession Haunts (C6/C7)", 12, 32,
  "<p>"+chk("type:perception|dc:32")+" (trained) to notice the compulsion gathering.</p>",
  "<p>"+chk("type:religion|dc:32")+" to exorcise (vitality), or indulge the obsession to exhaustion.</p>",
  "<p>Twin haunts of the servants' floor: <strong>Servitude</strong> (C6) and <strong>Battle</strong> (C7).</p>",
  [B.action(nid(), "Obsession of Servitude", "reaction", "<p><strong>Trigger</strong> Entering the lounge (C6).</p><hr /><p><strong>Effect</strong> "+chk("type:will|dc:32")+" or compelled to clean, mend, and serve for 1 hour ("+B.cond("fascinated", "Fascinated")+"; an ally may slap them free — Athletics vs. Fort DC).</p>"),
   B.action(nid(), "Obsession of Battle", "reaction", "<p><strong>Trigger</strong> Entering the sparring room (C7).</p><hr /><p><strong>Effect</strong> "+chk("type:will|dc:32")+" or compelled to spar — the victim attacks the nearest creature with nonlethal Strikes for 1 minute ("+B.cond("confused", "Confused")+" in effect; damage ends it).</p>")],
  folder=F5["a_hazards"], traits=["haunt", "mental", "incapacitation"], reset="<p>1 day.</p>", complex_=False))

HW("curse-of-the-worm", B.hazard(A5["curseworm"], "Curse of the Worm (E10)", 13, 34,
  "<p>"+chk("type:perception|dc:34")+" (trained) to hear the chewing beneath the records.</p>",
  "<p>"+chk("type:religion|dc:34")+" or burn the gnawed ledgers (losing their intelligence).</p>",
  "<p>The records room's haunt — the army's roll of the dead, hungry to add names.</p>",
  [B.action(nid(), "Gnawing Names", "reaction", "<p><strong>Trigger</strong> Reading the rolls.</p><hr /><p><strong>Effect</strong> Spectral worms burrow at the reader: @Damage[12d6[void]] ("+chk("type:fortitude|dc:33|basic:true")+"); on a critical failure also "+B.cond("drained", "Drained 2")+". The surviving rolls name every officer — and both anchors quartered in the towers.</p>")],
  folder=F5["a_hazards"], traits=["haunt", "void"], reset="<p>1 day.</p>", complex_=False))

HW("danse-macabre", B.hazard(A5["dansemacabre"], "The Danse Macabre (B36)", 14, 35,
  "<p>"+chk("type:perception|dc:35")+" (trained) to hear the music before the rosette door opens.</p>",
  "<p>It cannot be disabled — only escaped (leave the observatory) or destroyed (HP 250; harmed only by vitality and force).</p>",
  "<p>A whirling procession of the dead in the Rosette Observatory — <strong>no part of Mithrodar's network</strong>; even Scarwall's Lords fear the far end of the guest wing.</p>",
  [B.action(nid(), "Join the Dance", "free", "<p><strong>Routine:</strong> every living creature in the observatory: "+chk("type:will|dc:37")+" or be swept into the dance — "+B.cond("controlled", "Controlled")+" (dance toward the windows and the 100-ft fall) until it succeeds; each round dancing deals @Damage[6d6[void]].</p>")],
  folder=F5["a_hazards"], traits=["haunt", "incapacitation", "mental"], reset="<p>Always dancing.</p>", complex_=True))

HW("polong-bottles", B.hazard(A5["polongbottles"], "The Polong Bottles (B18)", 12, 32,
  "<p>"+chk("type:perception|dc:32")+" to notice the three corked bottles trembling on the workbench.</p>",
  "<p>Leave them corked; "+chk("type:thievery|dc:32")+" to wax-seal them permanently.</p>",
  "<p>Three blood-spirits imprisoned in glass by the castle's old caretaker-alchemist.</p>",
  [B.action(nid(), "Uncorked", "reaction", "<p><strong>Trigger</strong> A bottle is opened or broken.</p><hr /><p><strong>Effect</strong> A polong (run as an invisible "+B.mon("wraith", "wraith")+" with +2 status to attacks) erupts and possesses or pummels; all three loose at once is a Severe surprise.</p>")],
  folder=F5["a_hazards"], traits=["magical", "trap", "possession"], reset="<p>None.</p>", complex_=False))

# =====================================================================
# JOURNAL — "5. Skeletons of Scarwall"
# =====================================================================
SR = lambda area, p: f'<p class="source"><em>Source: CotCT (2016 HC), Ch.5, {area} — p.{p}.</em></p>'
pages = []
def PG(name, html, level=2): pages.append(B.page(nid(), name, html, level=level))
def area5(code, name, html): PG(f"{code}. {name}", html, level=3)
def encx(levels, pl):
    e = B.encounter(levels, party_level=pl); return f"{e['band']} · {e['xp']} XP @ L{pl}"

PG("Chapter Background",
  B.s_milestone("<p><strong>Chapter 5 — Skeletons of Scarwall.</strong> Across Belkzen to the drowned castle where Kazavon died, for the one blade that can unmake the Crown: <strong><em>Serithtial</em></strong>. PCs begin at <strong>L13</strong>; retrieve the sword and stand <em>at least</em> well into L15 before Chapter 6.</p>")
  + SEC("<p><strong>The Fifth Harrowing</strong> opens the chapter (suit of keys — dexterity, locks, escapes). <strong>The Devil You Know:</strong> "+act(A5["sial"], "Shadowcount Sial")+" and his casket-eidolon Asyra formally join (with "+act("laoriVaus0000001", "Laori")+"): the Brotherhood knows the castle's history and wants Kazavon never to rise — an alliance of genuine use and genuinely awful long-term implications (see the Star Tower). The PCs travel via the Shoanti and the World's Edge passes; the castle stands in a crater lake (the <strong>Tarnworm</strong>, a L13 lake-serpent, takes boats; the <strong>Air Approach</strong> answers to "+act(A5["aerilaya"], "Aerilaya")+").</p>"))

PG("The Scarwall Curse & Spiritual Doom",
  B.s_milestone("<p><strong>The Curse</strong> (castle-wide, CL 20th — read this page before running anything):</p>")
  + "<ul>"
    "<li><strong>Aura of Menace:</strong> <em>detect</em>-style divinations of evil/undead fail: "+chk("type:will|dc:25")+" or "+B.cond("stunned", "Stunned 1")+". The whole castle reads as one necromantic aura.</li>"
    "<li><strong>Dread:</strong> sleeping inside: "+chk("type:will|dc:20")+" on waking or the rest grants nothing — "+B.cond("fatigued", "Fatigued")+", no spell recovery (mental, fear).</li>"
    "<li><strong>Soultrapping:</strong> a living creature dying inside: "+chk("type:will|dc:23")+" or its soul binds into the walls (resurrection requires <em>dispelling</em> that bind and beginning the raise within 1 round). Any undead created inside is bound instantly; a week's residence forces "+chk("type:will|dc:22")+" weekly.</li>"
    "<li><strong>Unhallow + dimensional lock:</strong> non-inhabitants cannot teleport within or out; vitality channels at −4, void at +4.</li>"
    "<li><strong>Phantasms:</strong> one-shot terrors per location — flavor, no effect. <strong>Self-repair:</strong> the castle heals over a year.</li>"
   "</ul>"
  + SEC("<p><strong>SPIRITUAL DOOM — Zellara:</strong> if her deck crosses the causeway, <strong>Mithrodar attacks her spirit within 2 rounds</strong> — "+chk("type:will|dc:25")+" each round (the bearer may substitute their own save); failure = absorbed, the deck dies, and only lifting the curse frees her. <strong>Leave the deck off the island.</strong> Possession-style magic: "+chk("type:will|dc:15")+" on casting or soul-bound ("+chk("type:arcana|dc:25")+" while casting notices in time to abort). <em>Speak with dead</em> auto-fails ("+chk("type:fortitude|dc:20")+" or permanently "+B.cond("deafened", "Deafened")+").</p>")
  + SEC("<p><strong>BREAKING IT</strong> ("+chk("type:arcana|dc:25")+" to learn <em>remove curse</em> won't): destroy the four <strong>spirit anchors</strong> — "+act(A5["belshallam"], "Belshallam")+" (B23), "+act(A5["castothrane"], "Castothrane")+" (D1), "+act(A5["nihil"], "Nihil")+" (D14), "+act(A5["zev"], "Zev Ravenka")+" (F11) — then "+act(A5["mithrodar"], "Mithrodar")+" (C14). Each anchor down peels a layer (his sheet has the ladder) — and the castle <em>screams</em>. He can chain replacements (never constructs, never Ildervok; <em>Sial and Laori qualify</em>). All four down: the locks fall, and he can die. His death frees every soul — and wakes <em>Serithtial</em>.</p>"))

PG("The Lords of Scarwall",
  "<p>The castle's society of horrors — play them against each other:</p>"
  + "<ul>"
    "<li><strong>Anchors:</strong> "+act(A5["belshallam"], "Belshallam")+" (umbral dragon, B23) · "+act(A5["castothrane"], "Castothrane")+" (gatehouse captain, D1) · "+act(A5["nihil"], "Nihil")+" (chained devil-assassin, D14 — <em>wants out</em>) · "+act(A5["zev"], "Zev Ravenka")+" (demilich, F11).</li>"
    "<li><strong>The keep:</strong> "+act(A5["mithrodar"], "Mithrodar")+" (C14) · "+act(A5["lashton"], "Lashton")+" (causeway) · "+act(A5["mandraivus"], "Mandraivus the Lost")+" (B5) · the "+haz(A5["dansemacabre"], "Danse Macabre")+" (B36 — feared by <em>everyone</em>).</li>"
    "<li><strong>The wings:</strong> "+act(A5["ukwar"], "Ukwar")+" (fext, guest wing) · Anizora (debilitated "+B.mon("dybbuk", "dybbuk")+", the smithy floor) · "+act(A5["aerilaya"], "Aerilaya")+" (banshee, the cupola) · Glimkarus (a bogeyman tourist who thinks staying is his idea).</li>"
    "<li><strong>The towers:</strong> "+act(A5["gorstav"], "Gorstav")+" (War Tower) · Risibeth (sayona — <em>blood for secrets</em>: names three anchors, points at the chapel) · "+act(A5["aruth"], "Prelate Aruth")+" + "+act(A5["zev"], "Zev")+" (donjon) · "+act(A5["ildervok"], "Ildervok")+" (Star Tower, Zon-Kuthon's writ) · "+act(A5["kleestad"], "Kleestad")+" (the lake below).</li>"
   "</ul>"
  + B.s_conv("<p><strong>Random encounters</strong> (1 in 6 per hour moving, flavored per wing): "+act(A5["scarguard"], "Scarwall guards")+", "+B.mon("wraith", "wraiths")+", "+B.mon("greater-shadow", "greater shadows")+", "+act(A5["gargbrute"], "gargoyle packs")+", wall-spirits — the spirits stop roaming at 3 anchors down.</p>"))

area5("A", "The Barbican (A1-A12)", SR("A — Barbican", 262)
  + box("The tunnel curves sharply to the north here, ending", "<p>The causeway runs to a squat barbican whose arrow-slits glow with orc-fire — the only living things for forty miles, and proud of it.</p>")
  + "<p>The <strong>Deadwatchers</strong> hold the gate: "+act(A5["deadwatcher"], "orc warriors")+" at the entry (A2, 4×) and barracks (A6, 8×), watch-posts (A11), and "+act(A5["ury"], "Ury Sevenskulls")+" in his chamber (A10). <strong>Fight or talk</strong> — "+chk("type:intimidation|dc:28")+" / "+chk("type:diplomacy|dc:32")+" / a duel or worthy gift buys passage (they will not enter the castle).</p>"
  + B.enc("Barbican in arms", encx([7]*8 + [10], 13),
     "<p>The full garrison if roused: 8 "+act(A5["deadwatcher"], "Deadwatchers")+" + "+act(A5["ury"], "Ury")+". The lake routes instead: the <strong>Tarnworm</strong> ("+encx([13], 13)+", a Huge lake-serpent — use "+act(A5["kleestad"], "Kleestad's")+" Strikes at −2) under the boats, or "+act(A5["aerilaya"], "Aerilaya")+" + gargoyles aloft.</p>",
     B.aside_token(["8× "+act(A5["deadwatcher"], "Deadwatcher (7)"), act(A5["ury"], "Ury Sevenskulls (10)")])))

area5("B1-B6", "First Floor — the Gate & the Hero", SR("B1-B6", 270)
  + "<p><strong>B1, the Causeway:</strong> "+act(A5["lashton"], "Lashton")+" on his "+act(A5["skelnightmare"], "skeletal nightmare")+" with 12 skeletal champions ("+encx([10, 7] + [2]*12, 13)+" — the champions are chaff; the welcome is the point). <strong>B3:</strong> "+act(A5["scarguard"], "guard")+" posts (2/room). <strong>B4, the Death Chamber:</strong> the "+act(A5["corpseorgy"], "Corpse Orgy")+" ("+encx([13], 13)+"). <strong>B6:</strong> trench-mist corridors (concealment) prowled by 6 juju zombies (Elite "+B.mon("zombie-brute", "zombie brutes")+").</p>"
  + B.enc("B5 — Mandraivus's Fall", encx([13], 13),
     "<p>"+act(A5["mandraivus"], "Mandraivus the Lost")+" beside the "+haz(A5["vortexmadness"], "Vortex of Madness")+" — fight a hero, or <em>free</em> one (his entry). The room of the chapter's soul.</p>",
     B.aside_token([act(A5["mandraivus"], "Mandraivus (13)"), haz(A5["vortexmadness"], "Vortex of Madness (10)")])))

area5("B7-B24", "First Floor — Barracks, Kitchens & the Dragon", SR("B7-B24", 276)
  + "<p><strong>B7–B14:</strong> the garrison wing — quarters, offices, the magus's and captain's rooms; <strong>B10</strong> holds the graveknight <strong>Knurlott</strong> (link "+B.mon("graveknight-warmaster", "Graveknight Warmaster")+", renamed — "+encx([14], 13)+"). <strong>B15, the Kitchens:</strong> the "+haz(A5["crematoryblast"], "Crematory Blast")+" + 4 "+act(A5["cinderghoul"], "cinder ghouls")+" ("+encx([9]*4, 13)+"). <strong>B17:</strong> 5 "+act(A5["scarguard"], "guards")+". <strong>B18:</strong> the "+haz(A5["polongbottles"], "Polong Bottles")+". <strong>B19:</strong> Malatrothe, a hollow caretaker-wight (run as an Elite "+B.mon("war-wraith", "war-wraith")+"). <strong>B20–B21:</strong> wine cellar and courtyard — a <strong>corpse lotus</strong> ("+encx([13], 13)+"; a Huge carrion-plant: grasping vines reach 20 ft, "+chk("type:reflex|dc:33")+" or "+B.cond("grabbed", "Grabbed")+" and fed toward the maw, @Damage[3d10+11[bludgeoning]] per round).</p>"
  + B.enc("B23 — Belshallam's Lair", encx([15], 13),
     "<p>The "+act(A5["belshallam"], "umbral dragon")+" — <strong>SPIRIT ANCHOR</strong> — among his worm-pets (B22: 4 tenebrous worms, L9 shadow-larvae: bristles "+chk("type:fortitude|dc:28")+" or "+B.cond("paralyzed", "Paralyzed")+" 1 round). His hoard (B24): the wing's treasury, re-scaled L13–14 parcel + a <em>shadow</em> rune and the castle's best mundane plunder.</p>",
     B.aside_token([act(A5["belshallam"], "Belshallam (15) — ANCHOR")])))

area5("B25-B37", "The Guest Wing & the Observatory", SR("B25-B37", 284)
  + "<p><strong>B26:</strong> Pegg & Loute, two L6 'entertainers' juggling cleavers for a dead audience. <strong>B29:</strong> "+act(A5["ukwar"], "Ukwar")+" holds court ("+encx([12], 13)+"). <strong>B30/B32:</strong> haunted baths (festering spirits — 6× "+B.mon("greater-shadow", "greater shadows")+", "+encx([7]*6, 13)+"). <strong>B33:</strong> wraith-guests (10× "+B.mon("wraith", "wraiths")+" across the rooms). <strong>B34, Malice Aforethought:</strong> a murder-haunt (as the "+haz(A5["obsessionhaunt"], "Obsession")+" pattern, lethal Strikes). <strong>B35:</strong> the Prison of Woe. <strong>B37:</strong> the hidden mooring — the Tarnworm's other hunting ground.</p>"
  + B.enc("B36 — the Rosette Observatory", encx([14], 13),
     "<p>The "+haz(A5["dansemacabre"], "DANSE MACABRE")+" — the one horror even the Lords avoid. Nothing here is worth the dance. (The players will go anyway.)</p>",
     B.aside_token([haz(A5["dansemacabre"], "Danse Macabre (14)")])))

area5("C", "Second Floor & the Great Hall (C1-C20)", SR("C", 292)
  + "<p><strong>C1:</strong> the gate-winch (10 "+act(A5["scarguard"], "guards")+"). <strong>C4, the Armory:</strong> an "+B.mon("iron-golem", "iron golem")+" ("+encx([13], 13)+") before racks of five-century steel (the castle's best mundane arms + a <em>+2 striking</em> cache). <strong>C6/C7:</strong> the "+haz(A5["obsessionhaunt"], "Obsession Haunts")+". <strong>C8:</strong> 4 geists (Elite "+B.mon("wraith", "wraiths")+"). <strong>C9:</strong> a riderless "+B.mon("nightmare", "nightmare")+" stabled in shadow. <strong>C10:</strong> the torture room and its penitent dead. <strong>C19/C20:</strong> the hunt-commander Anizora, a debilitated "+B.mon("dybbuk", "dybbuk")+" (Weak adjustment; she possesses a PC and <em>walks them</em> toward the smithy's forge).</p>"
  + B.enc("C14 — THE GREAT HALL: Mithrodar", encx([16], 14),
     "<p>"+act(A5["mithrodar"], "MITHRODAR")+" enthroned in chains. Before all four anchors fall he re-forms in 1d4 days — fighting him early is how the castle <em>teaches</em>. After the fourth: the true battle, every freed soul straining at his chains. (Coordinate the curse-ladder on his sheet.)</p>",
     B.aside_token([act(A5["mithrodar"], "Mithrodar (16) — the Chained Spirit")])))

area5("D", "Scarwall Heights (D1-D18)", SR("D", 300)
  + "<p><strong>D1, the Gatehouse Loft:</strong> "+act(A5["castothrane"], "CASTOTHRANE")+" — <strong>ANCHOR</strong> — and his skeletal garrison ("+encx([12] + [7]*4, 13)+"). <strong>D8, the Minarets:</strong> the "+act(A5["gargbrute"], "gargoyle")+" roosts (2–8 by provocation). <strong>D12:</strong> a guard-captain post. <strong>D14, the Tower of Kazavon:</strong> "+act(A5["nihil"], "NIHIL")+" — <strong>ANCHOR</strong> — in his chains ("+encx([14], 13)+"; talk first — he <em>wants</em> this). <strong>D15/D16, Belfry & Cupola:</strong> "+act(A5["aerilaya"], "Aerilaya")+" and her court ("+encx([13, 9, 9], 13)+" with two bone-devil 'wraiths'). <strong>D18:</strong> the Lord's Overlook — the castle's one honest view.</p>")

area5("E", "The War Tower (E1-E14)", SR("E", 308)
  + "<p><strong>E3:</strong> 3 elite "+act(A5["scarguard"], "guards")+". <strong>E5:</strong> 2 Nessian hell hounds ("+B.mon("greater-hell-hound", "greater hell hounds")+", Elite). <strong>E7:</strong> Risibeth the sayona — <em>blood for secrets</em> (her price: a pint, willingly; her goods: three anchors named, the chapel fingered, the castle's history). <strong>E10:</strong> the "+haz(A5["curseworm"], "Curse of the Worm")+" over the army's records. <strong>E13:</strong> 4 spectres ("+B.mon("war-wraith", "war-wraiths")+").</p>"
  + B.enc("E11 — the War Room: Gorstav", encx([13], 13),
     "<p>"+act(A5["gorstav"], "Gorstav")+" at his eternal sand-table, refighting the day he lost. Carriers of <em>Serithtial's</em> name beware.</p>",
     B.aside_token([act(A5["gorstav"], "Gorstav (13)")])))

area5("F", "The Donjon (F1-F14)", SR("F", 314)
  + "<p><strong>F2:</strong> a fiendish elder water elemental in the font ("+encx([12], 14)+"; run as Elite "+B.mon("elemental-tsunami", "elemental tsunami")+", Weak). <strong>F3:</strong> 5 advanced spectres ("+B.mon("war-wraith", "war-wraiths")+"). <strong>F8:</strong> "+act(A5["mingorc"], "Mingorc")+" at the porter's station ("+encx([13], 14)+"). <strong>F10:</strong> "+act(A5["aruth"], "Prelate Aruth")+" and his congregation ("+encx([13, 7, 7], 14)+").</p>"
  + B.enc("F11 — the Dark Shrine of Midnight", encx([15], 14),
     "<p>"+act(A5["zev"], "ZEV RAVENKA")+" — the fourth <strong>ANCHOR</strong> — a jeweled skull over Zon-Kuthon's altar. One round to wake; then Trap Soul every round. His rubies are the donjon's treasury — and some of them scream.</p>",
     B.aside_token([act(A5["zev"], "Zev Ravenka (15) — ANCHOR")])))

area5("G-H", "The Star Tower & the Sacred Lake", SR("G-H", 320)
  + box("Many hundreds of years ago, a", "<p>The Star Tower descends, not rises — a well of dark at the castle's root, and below it, water that remembers a sword.</p>")
  + "<p><strong>G7, the Chamber of the Well:</strong> "+act(A5["ildervok"], "ILDERVOK")+", invisible and courteous ("+encx([14], 14)+" if it comes to blades). <strong>His toll: a curate for Zon-Kuthon's post.</strong> "+act(A5["sial"], "Sial")+" wants it; Sial would prefer <em>Laori</em> got it; Laori refuses, hurt — the Brotherhood's quiet knife-fight, decided by the PCs' word. A banishment-grade effect also clears the post (and angers a god). <strong>H1–H2:</strong> the caverns (a sealed gate to Sekamina). <strong>H3:</strong> the Sacred Lake — 4 "+B.mon("gug", "gugs")+" haunt its shore ("+encx([10]*4, 14)+").</p>"
  + B.enc("H4 — KLEESTAD & SERITHTIAL", encx([15], 14),
     "<p>"+act(A5["kleestad"], "Kleestad")+", the traitor-worm, coiled on the lakebed around the sword he can never wield. <strong><em>Serithtial</em></strong> sleeps suppressed (a masterwork blade until the curse lifts): a <strong>+3 major-striking holy bastard sword</strong>, Kazavon's bane, that <em>chooses</em> a good-hearted bearer — the only edge that can sunder the Crown of Fangs.</p>",
     B.aside_token([act(A5["kleestad"], "Kleestad (15)")])))

PG("Chapter Conclusion",
  B.s_milestone("<p><strong>Conclusion.</strong> Serithtial recovered (and ideally the curse broken — every soul in the walls released, <em>including any the castle took from the party</em>), the PCs return across Belkzen. They must be <strong>well into L15</strong>, sword in hand, before Castle Korvosa.</p>")
  + SEC("<p><strong>A Swifter Scarwall (optional, recommended):</strong> the full castle is a long crawl — the AP's own advice: run B1→B5 (Mandraivus), one wing of choice, the four anchors, C14, and the Star Tower descent; compress the rest to random encounters and dread. <strong>Interleave Korvosa beats</strong> (the Epidemic Clock has been climbing unattended — the persistent-plague overlay's away-penalty) so the city's decay pulls the party home.</p>")
  + SEC("<p><strong>Redemption threads:</strong> "+act(A5["sial"], "Sial")+" likely takes the curacy (gone to the Plane of Shadow) or dies; <strong>Laori</strong> refuses it, survives, and — befriended — may begin the long walk away from Zon-Kuthon. <strong>Mithrodar's fall frees Zellara</strong> if the castle took her. Kleestad, if he somehow lived, pursues the sword to the world's end. Next: <strong>Chapter 6 — Crown of Fangs.</strong></p>"))

journal = B.journal_entry(JID5, "5. Skeletons of Scarwall", pages, folder=ADV_FOLDER)
B.write("journals", "05-skeletons-of-scarwall", copy.deepcopy(journal), embed_pages=True)
print(f"Chapter 5 built: {len(actors)} actors, {len(hazards)} hazards, 1 journal ({len(pages)} pages).")
