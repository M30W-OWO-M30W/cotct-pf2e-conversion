#!/usr/bin/env python3
"""Chapter 3 — Escape from Old Korvosa.

Own fat journal ("3. Escape from Old Korvosa"), appended to the shared packs
alongside Chapters 1-2. Party L8 -> L11. The quarantined island: Vencarlo's
trail, the Emperor of Old Korvosa (Pilts Swastel), the Arkona rakshasas, the
Vivified Labyrinth, and the rescue of Neolandus Kalepopolis.
"""
from __future__ import annotations
import copy
import pf2e_build as B
B.SCOPE = (5514, 8160)   # AP.md line range for this chapter (anchor scoping)

# OLLIEBIRD DC ALIGNMENT (community doc = DC authority): applied 45 rulings, added 3 new checks, skipped 11
# Skipped: already-aligned (Chamidu Religion 30 x2, D11 grounds good-lock 30, lever-override Thievery 30,
#          E14 secret-door Perception 30, E20 manacles Thievery 30 x2, Grab Pig DC 15);
#          out-of-scope, not DCs (pig bite attack/damage stats, A8 search durations, E5 heal rank);
#          no DC stated in doc (Catch Pig / symbols / pools / Tall Knife are template links only).
# Note: Devargo/Eel's End rungs are Ch.1 material; here the 19/22/24/29 rungs map to the
#       Researching-the-Emperor table (Society, per community) and the audience socials use the
#       community's area-keyed DC 26 Diplomacy / DC 22 Intimidation ruling.

# MISSING-CHECK SWEEP (gated actions with no badge): added 3 —
#   C12 cell-door pick Thievery 20 (AP p.158: simple wooden door, lock + heavy bar, key with Pilts;
#       community silent -> simple-lock convention 15/20 judged at party L8-9);
#   E16 sphere-oubliette + E21 southern cells: cell locks Thievery 30 (community silent -> good-lock
#       convention 30; matches the Labyrinth's lever-override/manacle DC 30s at L10).
#   Judged no-check: D4 'secret trap door' (Perception 28 badge already on the same page, per
#       community [D4]); D11 'feed in true form behind locked doors' (NPC dining custom — the area's
#       grounds doors carry the Thievery 30 badge in the same paragraph); E23 'gears unlock'
#       (machine narration, no player action gated); D20 Cat's Cradle rope bridges ('sturdy...easy
#       access' per AP); B3 shuttered windows / C4 pig-cage trapdoors / Jeggare barricade (narrative
#       or already governed by game-rule text).

# OLLIEBIRD STATBLOCK RESYNC (community statblock = stat authority; npc()/hazard() literals are
# swapped in place by B.write, so only encounter() args + "(L)" text labels are re-synced here):
#   Levels: Emperor's Thug 5->6 (mob/guardroom/court/blood-pig encs), Red Mantis Assassin 9->8,
#           Choker Brute 5->2, Marai 9->8, Bahor 13->14 (Severe-solo prose -> Extreme-solo),
#           Sivit 11->10, Enormous Reefclaw 12->11, Senshiir 10->9 (E21 band prose softened),
#           Belker 7->8. Symbols E6/E18 6->7 + Stinging Wasps 8->10 have no enc/text level refs.
#   Rewired to community-only docs: D4 marble elephant mon(giant-animated-statue)->cmon(Marble
#           Elephant); D24 Avidexu mon(raja-rakshasa)->cmon(Avidexu); E7 blood cobra
#           mon(giant-viper)->cmon(Blood Cobra); E4 pool now links cmon(Corrupted Pool) hazard;
#           Blood Pig now links cmon(Piglet).
#   Kept official: otyugh, wolverine, living-waterfall (community Large Water Elemental = same
#           re-export), emperor-cobra (community doc = base L5 re-export; their prose says Elite
#           but exported base), pf2e Yellow Mold (community hazard = same doc). Elite Red Mantis
#           Assassin + Pudgyknuckles: no matching ch3 encounter in our build — not linked.
#   Gear dedup vs community inventories: dropped thug Studded Leather (their Leather Armor covers
#           the armor parcel), Pilts Leather Armor (their +1 Glamered Chain Shirt), RMA leather/
#           sabers/daggers/alch-fire+potions pack (all on their statblock), Laori Chain Mail,
#           Vencarlo Rapier (same-name), Bahor keystone equipment (their Rakshasan Third Eye is
#           the parcel; network notes live in D1-D3/D17-D18 treasure text). Kept: thug Steel
#           Shield (PF1 parcel they omit), marai Scimitar, Vimanda Gold Armbands, Neolandus
#           Crossbow (his PF1 tactics weapon; no community dup).

MODID = "cotct-pf2e-conversion"
ACTOR_ROOT, ITEM_ROOT, ADV_FOLDER = "cotctActorRoot01", "cotctItemRoot001", "cotctAdvFolder01"

# ---- stable literal ids (16 chars) ----
JID3 = "ch3EscapeOldKor1"
A3 = {"empthug": "emperorsThug0001", "redmantis": "redMantisAssn001", "housefire": "spreadingFire001",
      "laori": "laoriVaus0000001", "pilts": "piltsSwastel0001", "jabbyr": "jabbyrGnome00001",
      "chokerbrute": "chokerBrute00001", "salvator": "salvatorScream01", "tallknife": "tallKnifeGuillo1",
      # Part 3 — Arkona Palace + Vivified Labyrinth
      "marai": "maraiRakshasa001", "bahor": "bahorArkona00001", "vimanda": "vimandaArkona001",
      "sivit": "sivitDarksphinx1", "gardenguard": "gardenGuardian01", "enormreef": "enormousReefclaw",
      "senshiir": "senshiirAsura001", "rajambari": "rajambariSkel001", "neolandus": "neolandusKalep01",
      "vencarlo": "vencarloOrisini1", "belker": "belkerSmoke00001",
      "hungrysmoke": "hungrySmokeTrap1", "symfear": "symbolFear000001", "sympain": "symbolPain000001",
      "symsleep": "symbolSleep00001", "symstun": "symbolStunning01", "insanitychest": "insanityChest001",
      "terinavchest": "terinavChest0001", "bitingtigers": "bitingTigers0001", "fangsdiom": "fangsDiomazul001",
      "wailingmaidens": "wailingMaidens01", "stingingwasps": "stingingWasps001"}
YELLOW_MOLD = "@UUID[Compendium.pf2e.hazards.Actor.A93flWUsot3FmC7t]{Yellow Mold}"
F3 = {"a_ch3": "ch3ActorFolder01", "a_creatures": "ch3CreaturesFld1", "a_hazards": "ch3HazardsFld001"}

ids = B._idgen(330003)
def nid(): return next(ids)
sids = B._idgen(883003)
def sid(): return next(sids)

def act(_id, label): return f"@UUID[Compendium.{MODID}.cotct-actors.Actor.{_id}]{{{label}}}"
def haz(_id, label): return f"@UUID[Compendium.{MODID}.cotct-hazards.Actor.{_id}]{{{label}}}"
def chk(s): return f"@Check[{s}]"
def SEC(html): return B.s_secret(html, sid())
def box(anchor, fallback_html):
    t = B.verbatim(anchor)
    return B.s_read(B.parafy(t)) if t else B.s_read(fallback_html)
def box_stitch(a1, cut, a2, fallback_html):
    """Read-aloud split by a two-column OCR interleave: keep a1's paragraph up
    through `cut`, drop the interleaved wrong-column merge, then append a2's
    paragraph (the true continuation, which OCR placed earlier in the file)."""
    t1, t2 = B.verbatim(a1), B.verbatim(a2)
    if t1 and t2 and cut in t1:
        return B.s_read(B.parafy(t1.split(cut)[0] + cut + " " + t2))
    return B.s_read(fallback_html)
CHC = "#8a1a1a"

# =====================================================================
# FOLDERS
# =====================================================================
folders = [
  B.folder(F3["a_ch3"], "3. Escape from Old Korvosa", "Actor", ACTOR_ROOT, 300000, CHC),
  B.folder(F3["a_creatures"], "Creatures", "Actor", F3["a_ch3"], 100000, None, "a"),
  B.folder(F3["a_hazards"], "Hazards", "Actor", F3["a_ch3"], 200000, None, "a"),
]
for f in folders:
    pack = {"Actor": "actors", "Item": "items", "JournalEntry": "journals"}[f["type"]]
    B.write(pack, "_folder_ch3-" + f["name"].lower().replace(" ", "-").replace(".", "") + "-" + f["type"][:3].lower(), copy.deepcopy(f))

# =====================================================================
# ACTORS
# =====================================================================
# mirror the folder chain into the hazards pack (per-pack folder docs)
for hf in [B.folder(F3["a_ch3"], "3. Escape from Old Korvosa", "Actor", ACTOR_ROOT, 300000, CHC),
           B.folder(F3["a_hazards"], "Hazards", "Actor", F3["a_ch3"], 200000, None, "a")]:
    B.write("hazards", "_folder_hz3-" + hf["name"].lower().replace(" ", "-").replace(".", ""), copy.deepcopy(hf))

actors = []
def AW(slug, doc):
    actors.append(copy.deepcopy(doc)); B.write("actors", slug, doc, embed_items=True)

AW("emperors-thug", B.npc(A3["empthug"], "Emperor's Thug", 5, 22, 75, 12, 11, 9, 11,
  {"str": 4, "dex": 3, "con": 3, "int": -1, "wis": 1, "cha": 0}, 25,
  {"athletics": 13, "intimidation": 11, "stealth": 11}, ["humanoid", "human"], ["common"],
  [B.strike(nid(), "Battleaxe", 14, "1d8+7", "slashing", ["sweep"]),
   B.strike(nid(), "Throwing Axe", 12, "1d6+7", "slashing", ["agile", "thrown-10"]),
   B.sneak_attack(nid(), 2, "The thug"),
   B.action(nid(), "Mob Tactics", "passive", "<p>Emperor's thugs swarm and flank: a thug's Strikes gain a +1 circumstance bonus against a creature adjacent to another thug.</p>", category="offensive"),
   B.gear("steel-shield", nid())],
  notes="<p><strong>Role:</strong> the muscle of Pilts Swastel's mob — soldiers of the 'Emperor of Old Korvosa,' commanding the petty thugs of Old Dock through fear. Reused throughout the island: street mobs (4), the palace guardroom, the Blood Pig arena (up to 8).</p>"
        "<p><strong>Tactics:</strong> swarm with battleaxes for flanked Sneak Attacks, hurling throwing axes at runners. <strong>Morale:</strong> bullies at heart — once half their number falls, the rest scatter into the alleys.</p>",
  folder=F3["a_creatures"], blurb="Mob soldier of the Emperor of Old Korvosa", token_src=None, actor_link=False))

AW("red-mantis-assassin", B.npc(A3["redmantis"], "Red Mantis Assassin", 9, 28, 135, 17, 20, 16, 18,
  {"str": 4, "dex": 5, "con": 2, "int": -1, "wis": 0, "cha": 1}, 25,
  {"acrobatics": 20, "athletics": 17, "stealth": 20, "intimidation": 15, "deception": 15}, ["humanoid", "human"], ["common"],
  [B.strike(nid(), "+1 Striking Sawtooth Saber", 20, "2d8+7", "slashing", ["agile", "finesse", "magical", "twin"], slug="rma-saber"),
   B.strike(nid(), "Dagger", 19, "1d4+7", "piercing", ["agile", "finesse", "thrown-10", "versatile-s"]),
   B.sneak_attack(nid(), 3, "The assassin"),
   B.action(nid(), "Twin Sabers", "2", "<p>The assassin makes two Sawtooth Saber Strikes against the same target (the twin trait adds +2 circumstance damage to the second). If both hit, combine the damage for resistances.</p>", ["flourish"]),
   B.action(nid(), "Prayer Attack", "1", "<p>The assassin weaves her blades point-down before a creature within 30 feet that can see her: "+chk("type:will|dc:28")+" or the target is "+B.cond("fascinated", "Fascinated")+" (it may re-save whenever a new threat appears). The assassin Sustains this hypnosis; after sustaining 3 full rounds, her next Saber Strike against the still-fascinated target is an <strong>automatic critical hit</strong> on a success — the Red Mantis's signature execution.</p>", ["concentrate", "incapacitation", "mental", "visual"]),
   B.action(nid(), "Red Shroud", "1", "<p><strong>Frequency</strong> twice per day. A veil of red mist (unaffected by wind) wreathes the assassin for 3 rounds: +1 circumstance bonus to AC and fast healing 2. If she dies while shrouded, she may disintegrate into red mist, leaving only her gear — denying enemies her remains.</p>", ["concentrate"], "defensive"),
   B.action(nid(), "Vanish", "1", "<p>The assassin becomes "+B.cond("invisible", "Invisible")+" until the end of her next turn or until she Strikes — her favored repositioning trick (she can also cast <em>feather fall</em> and <em>expeditious retreat</em>).</p>", ["concentrate", "occult"]),
   B.action(nid(), "Mask of the Mantis", "passive", "<p>Her insectile mask grants darkvision, and by spending charges: <em>see invisibility</em>, <em>deathwatch</em>, and a +2 item bonus to Perception (active when prepared for an ambush).</p>", category="defensive"),
   B.lore(nid(), "Assassin Lore", 17)],
  notes="<p><strong>Role:</strong> the Red Mantis — the assassin guild Ileosa hired for the king's murder, now hunting <strong>Neolandus</strong> (and anyone shielding him). The campaign's recurring elite killers: paired ambushes here, more beneath the Longacre Building in Chapter 4.</p>"
        "<p><strong>Ambush doctrine (Vencarlo's home):</strong> pre-buffed (fire resistance 10, mask charges burning, blades enchanted), hidden under the stairs (A6) and in the A7 rafters. Round 1 each hurls alchemist's fire into her level's fireplace, igniting the "+act(A3["housefire"], "Spreading House Fire")+" they are warded against. They Red Shroud, pair up to flank, and Prayer-Attack a lone PC; the Spreading House Fire hazard is their battlefield. <strong>Morale:</strong> they fight to the death (and may dissolve to red mist).</p>",
  folder=F3["a_creatures"], senses=[{"type": "darkvision"}], blurb="Elite Red Mantis killer (recurring)", token_src=None, actor_link=False))

AW("laori-vaus", B.npc(A3["laori"], "Laori Vaus", 10, 29, 165, 19, 17, 21, 20,
  {"str": 3, "dex": 4, "con": 3, "int": 1, "wis": 5, "cha": 4}, 25,
  {"religion": 21, "intimidation": 19, "occultism": 17, "diplomacy": 17, "stealth": 17}, ["humanoid", "elf"], ["common", "elven", "infernal", "shadowtongue"],
  [B.strike(nid(), "+1 Striking Spiked Chain", 21, "2d8+8", "slashing", ["disarm", "finesse", "magical", "trip"], slug="laori-chain"),
   B.action(nid(), "Harm", "1", "<p>Void energy (DC 29). <strong>1 action</strong> (touch): @Damage[5d8[void]] to the living (basic "+chk("type:fortitude|dc:29")+") or that much healing to undead. <strong>2 actions</strong> (30 ft) adds +10. She channels several times a day — and can invert it to <em>mend her allies</em> through stimulating pain (treat as equivalent healing) when she has taken the PCs as friends.</p>", ["concentrate", "manipulate", "void"]),
   B.action(nid(), "Savor the Sting", "2", "<p>One creature within 30 feet relives exquisite agony: @Damage[4d6[mental]] and "+chk("type:will|dc:29")+" or "+B.cond("sickened", "Sickened 1")+" with pain (Sickened 2 and "+B.cond("slowed", "Slowed 1")+" for 1 round on a critical failure). Laori giggles.</p>", ["concentrate", "manipulate", "mental", "nonlethal", "occult"]),
   B.action(nid(), "Shadow Step", "1", "<p>Laori steps from one shadow to another she can see within 60 feet — Zon-Kuthon's roads are dark and quick.</p>", ["concentrate", "shadow", "teleportation"]),
   B.action(nid(), "Umbral Chains", "2", "<p>Shadowy chains lash a 15-ft burst within 60 feet: @Damage[6d6[negative]] void damage and "+chk("type:reflex|dc:29|basic:true")+"; a creature critically failing is "+B.cond("grabbed", "Grabbed")+" by the chains (Escape DC 29) for 1 round.</p>", ["concentrate", "manipulate", "shadow", "occult"]),
   B.lore(nid(), "Zon-Kuthon Lore", 21)],
  notes="<p><strong>Role:</strong> a chipper, utterly sincere elf priestess of <strong>Zon-Kuthon</strong> — a cheerful sadist and one of the campaign's strangest, most useful <strong>allies</strong>. She belongs to the <strong>Brotherhood of Bones</strong>, Kuthite fanatics hunting Kazavon's relics to prevent his resurrection; she tracked Andaisin to Korvosa, then stayed to find the dragon's seven whisper-touched artists. Six are suicides (their candle-lit skulls decorate Salvator's desk — she <em>speaks with dead</em> to them); Salvator, the strongest-touched, was taken before she arrived.</p>"
        "<p><strong>Playing her:</strong> bubbly, friendly, casually horrifying. She offers an alliance to reach Salvator and trades her evidence — a bloodstained scrap of the <strong>seneschal's uniform</strong> — for it. She admits her faith freely but conceals the Brotherhood, her queen-suspicions, and Kazavon (except under magical compulsion — or when the story needs the crown reveal early). Rebuffed, she shadows the party and 'reappears' at a dramatic moment, ideally saving their lives. She returns as a major ally in Chapter 5 (Scarwall).</p>",
  folder=F3["a_creatures"], senses=[{"type": "low-light-vision"}], blurb="Cheerful Kuthite priestess; Brotherhood of Bones", token_src=None, actor_link=True))

AW("pilts-swastel", B.npc(A3["pilts"], "Pilts Swastel", 10, 29, 175, 17, 21, 19, 19,
  {"str": 0, "dex": 5, "con": 2, "int": 1, "wis": -1, "cha": 5}, 20,
  {"performance": 22, "diplomacy": 20, "intimidation": 20, "deception": 20, "society": 18, "thievery": 17, "stealth": 17}, ["humanoid", "human"], ["common", "gnomish", "varisian"],
  [B.strike(nid(), "War Razor", 19, "2d4+4", "slashing", ["agile", "backstabber", "deadly-d8", "finesse"]),
   B.strike(nid(), "Crossbow", 19, "2d8+2", "piercing", ["range-increment-120", "reload-1"]),
   B.action(nid(), "Dirge of Doom", "1", "<p>A grinding, theatrical death-hymn: enemies within 30 feet are "+B.cond("frightened", "Frightened 1")+" (no save, but a creature that ends its turn out of earshot recovers). His showman's counterpart, <em>Inspire Courage</em>, grants his mob +1 status to attacks, damage, and saves vs. fear.</p>", ["auditory", "composition", "emotion", "fear", "mental"]),
   B.action(nid(), "Confounding Performance", "2", "<p>Pilts targets one creature within 60 feet with a maddening harangue: "+chk("type:will|dc:29")+" or the creature is "+B.cond("confused", "Confused")+" for 1 round (3 rounds on a critical failure; he favors <em>charm</em> and <em>hold person</em> variants — Will save, "+B.cond("paralyzed", "Paralyzed")+" 1 round — as the mood takes him).</p>", ["auditory", "concentrate", "emotion", "incapacitation", "mental", "occult"]),
   B.action(nid(), "Rod of Wonder", "1", "<p>Pilts Activates his beloved <strong>rod of wonder</strong> at a foe and gleefully narrates whatever chaos results (use the PF2e wand-of-wonder table). He does this even when losing — <em>especially</em> when losing.</p>", ["manipulate", "magical"]),
   B.action(nid(), "Displacement", "2", "<p>When personally threatened: attacks against Pilts suffer a 50% miss chance (as <em>blur</em>-displacement) for 1 minute, and he finally draws his razor.</p>", ["concentrate", "illusion", "occult"], "defensive"),
   B.action(nid(), "Dimension Door", "2", "<p>Pilts teleports up to 120 feet — his exit, twice. Below ~20 HP he doors to his chambers (C11), spends rounds snatching favourite prizes, then doors again to vanish into Old Dock and plot revenge. Out of doors and below ~10 HP, he drops to his knees and begs, offering anything.</p>", ["concentrate", "occult", "teleportation"]),
   B.lore(nid(), "Theater Lore", 18)],
  notes="<p><strong>Role:</strong> the <strong>Emperor of Old Korvosa</strong> — a failed gore-theater impresario turned mob-tyrant, ruling Old Dock from a salvage-prop throne beside his guillotine. A showman-bard: glibness, charm, mirror-tricks, and a rod of wonder; his power is the <em>audience</em>, not his blade.</p>"
        "<p><strong>Court:</strong> held daily, breakfast to dusk, with "+act(A3["jabbyr"], "Jabbyr")+" at the Tall Knife and four thugs at hand. He freely admits Salvator is his 'houseguest' but no Diplomacy or Intimidation wins an audience — only the <strong>blood pig wager</strong> (or violence). A <em>noticed</em> enchantment attempt = execution order. <strong>Morale:</strong> flees by dimension door at ~20 HP; his death or public surrender disbands the mob in 2d6 rounds.</p>",
  folder=F3["a_creatures"], blurb="The Emperor of Old Korvosa; mad impresario", token_src=None, actor_link=True))

AW("jabbyr", B.npc(A3["jabbyr"], "Jabbyr", 8, 26, 160, 17, 14, 13, 15,
  {"str": 6, "dex": 2, "con": 5, "int": -3, "wis": 1, "cha": -3}, 30,
  {"athletics": 19, "acrobatics": 14}, ["humanoid", "gnome"], ["gnomish"],
  [B.strike(nid(), "+1 Striking Greataxe", 20, "2d12+9", "slashing", ["magical", "sweep"], slug="jabbyr-axe"),
   B.action(nid(), "Rage", "1", "<p>Jabbyr rages the instant combat begins: +4 damage (included), 16 temporary HP, −1 AC (included). While raging he cannot use concentrate actions.</p>", ["concentrate", "emotion", "mental"], "defensive"),
   B.action(nid(), "No Escape", "reaction", "<p><strong>Trigger</strong> A foe within reach moves away.</p><hr /><p><strong>Effect</strong> Jabbyr Strides up to his Speed, following the foe; if he ends adjacent, he makes a Greataxe Strike against it.</p>"),
   B.action(nid(), "Operate the Tall Knife", "1", "<p>Jabbyr releases the guillotine's blade (see the Tall Knife hazard) — his sacred office, performed in full executioner's costume.</p>", ["manipulate"])],
  notes="<p><strong>Role:</strong> Pilts's executioner — a tongueless, one-eyed gnome berserker who calls the Emperor 'Unca Pit' and loves the guillotine like a pet. <strong>He never attacks gnomes</strong> unless struck first (Pilts knows never to order it). Understanding his babbling takes "+chk("type:society|dc:20")+" (or Sense Motive at the GM's whim).</p>"
        "<p><strong>Morale:</strong> fights to the death. If Pilts dies he freezes a round in shock, then resumes. If Pilts <strong>surrenders</strong> in his presence, Jabbyr snaps and attacks the ex-emperor for treason — and may demand the PCs help him strap 'Unca Pit' into the Tall Knife.</p>",
  folder=F3["a_creatures"], senses=[{"type": "low-light-vision"}], size="sml", blurb="Tongueless gnome executioner", token_src=None, actor_link=True))

AW("choker-brute", B.npc(A3["chokerbrute"], "Choker Brute", 5, 22, 78, 11, 11, 12, 13,
  {"str": 5, "dex": 2, "con": 4, "int": -2, "wis": 3, "cha": -3}, 20,
  {"athletics": 14, "stealth": 13, "acrobatics": 9}, ["aberration"], ["undercommon"],
  [B.strike(nid(), "Tentacle", 15, "1d8+7", "bludgeoning", ["agile", "reach-10"]),
   B.sneak_attack(nid(), 1, "The choker"),
   B.action(nid(), "Choke", "1", "<p><strong>Requirement</strong> The choker's last action was a successful Tentacle Strike.</p><hr /><p><strong>Effect</strong> It Grabs the target ("+B.cond("grabbed", "Grabbed")+", Escape DC 21) and begins to strangle: the victim takes @Damage[1d8+7[bludgeoning]] at the start of each of the choker's turns and cannot speak or cast verbal spells while held.</p>", ["attack"]),
   B.action(nid(), "Quickness", "passive", "<p>The choker is preternaturally quick: it gains an extra action each turn that it can use only to Stride or Climb (climb Speed 20 ft).</p>", category="defensive")],
  notes="<p><strong>Role:</strong> Pilts's rooftop allies from the playhouse days — they dispose of his corpses (eating the choice bits, stashing the rest across the Shingles; the headless state of recent deliveries doesn't bother them). Six nest in the palace attic (C7).</p>"
        "<p><strong>Tactics:</strong> lurk in rafter-shadow; strike the moment someone opens the door from outside, or 3 rounds after intruders start moving within. Fight to the death.</p>",
  folder=F3["a_creatures"], senses=[{"type": "darkvision"}], size="sml", blurb="Strangling rafter-lurker", token_src=None))

AW("salvator-scream", B.npc(A3["salvator"], "Salvator Scream", 4, 16, 55, 9, 7, 11, 10,
  {"str": 0, "dex": 1, "con": 1, "int": 4, "wis": -1, "cha": -1}, 25,
  {"crafting": 14, "society": 12, "religion": 12, "occultism": 12, "deception": 8}, ["humanoid", "human"], ["common", "aklo", "draconic"],
  [B.strike(nid(), "Fist", 8, "1d4", "bludgeoning", ["agile", "nonlethal"]),
   B.lore(nid(), "Art Lore", 14)],
  notes="<p><strong>Role:</strong> the last of Kazavon's whisper-touched artists — the campaign's key witness. A noncombatant: he cowers, flees below half HP, and (if he escapes alone) wanders home to his death unless the otyughs were cleared.</p>"
        "<p><strong>What he knows</strong> (price: the Emperor's death + escort to the mainland; "+chk("type:diplomacy|dc:19")+" with a rescue promise, or Intimidation/magic): Vencarlo questioned him about <strong>Neolandus</strong>; the seneschal arrived at his door bloodied and poisoned the morning the king died, revealed that <strong>Ileosa murdered Eodred II</strong> in league with the Red Mantis, said the queen had 'changed — grown worse'… and that Salvator gave Neolandus to the <strong>Arkonas</strong> for safekeeping. He says <em>nothing</em> while Pilts lives.</p>",
  folder=F3["a_creatures"], blurb="Kazavon-touched painter; the key witness", token_src=None, actor_link=True))

# ---- Part 3: Arkona Palace + Vivified Labyrinth actors ----
AW("marai-rakshasa", B.npc(A3["marai"], "Marai Rakshasa", 9, 28, 155, 16, 18, 19, 18,
  {"str": 5, "dex": 4, "con": 3, "int": 2, "wis": 2, "cha": 4}, 30,
  {"deception": 21, "diplomacy": 17, "stealth": 17, "society": 15, "acrobatics": 17}, ["fiend", "rakshasa"], ["common", "vudrani", "infernal"],
  [B.strike(nid(), "Claw", 20, "2d8+8", "slashing", ["agile", "magical", "unholy"]),
   B.strike(nid(), "Scimitar", 20, "2d6+8", "slashing", ["forceful", "sweep"]),
   B.action(nid(), "Scorching Ray", "2", "<p>A spell attack (+19) against one creature within 60 feet for @Damage[6d6[fire]] (double on a critical hit) — their favored opener while still wearing a human face.</p>", ["concentrate", "fire", "manipulate", "occult"]),
   B.action(nid(), "Energy Bolt", "2", "<p>Once exposed in true form, the marai hurls raw fiendish power: a 30-ft line of @Damage[5d12[electricity]] ("+chk("type:reflex|dc:28|basic:true")+").</p>", ["concentrate", "electricity", "manipulate", "occult"]),
   B.action(nid(), "Change Shape", "1", "<p>The marai assumes or abandons any humanoid form (its disguise is nearly perfect: +4 circumstance to Deception to impersonate). Its corpse reverts to true tiger-headed form when slain.</p>", ["concentrate", "polymorph", "occult"]),
   B.action(nid(), "Read Minds", "1", "<p>The marai reads the surface thoughts of one creature within 30 feet ("+chk("type:will|dc:28")+" negates and the target feels the probing) — how the family always seems one step ahead.</p>", ["concentrate", "mental", "occult"]),
   B.action(nid(), "Fiendish Resilience", "passive", "<p><strong>Resistance</strong> physical 10 (except piercing weapons that are holy); immune to disease. The marai's wounds knit unnaturally before witnesses' eyes.</p>", category="defensive"),
   B.lore(nid(), "Vudra Lore", 17),
   B.gear("scimitar", nid()) if "scimitar" in B._GEAR else B.equipment(nid(), "Scimitar", 0, 2, "<p>A curved Vudrani blade.</p>", traits=["weapon"])],
  notes="<p><strong>Role:</strong> the four 'Arkona cousins' — <strong>Avishandu</strong> (gardener-artist), <strong>Carnochan</strong> (one-eyed majordomo, telepathically bonded to Bahor), <strong>Nudhaali</strong> (kitchen-mistress; much of the meat is humanoid), and <strong>Vennashti</strong> (security chief; the others defer to her in a fight). Tiger-headed fiends in flawless human masks.</p>"
        "<p><strong>Alert doctrine:</strong> servants flee; Avishandu + Nudhaali take the garden (D4, invisible in the howdah); Carnochan + Vennashti sweep the rooms in order. They fight in human form with spells until one dies (the corpse reverts) — then all revert and fight to the death to keep the secret. Off-duty (D14) they bicker in true form at −2 Perception to the house alarms.</p>",
  folder=F3["a_creatures"], senses=[{"type": "darkvision"}], blurb="Tiger-headed 'Arkona cousin'", token_src=None))

AW("bahor-glorio-arkona", B.npc(A3["bahor"], "Bahor (Glorio Arkona)", 13, 34, 270, 22, 24, 25, 25,
  {"str": 6, "dex": 5, "con": 4, "int": 5, "wis": 3, "cha": 7}, 30,
  {"deception": 28, "diplomacy": 26, "society": 24, "intimidation": 24, "occultism": 22, "stealth": 22}, ["fiend", "rakshasa"], ["common", "vudrani", "infernal", "undercommon"],
  [B.strike(nid(), "Claw", 26, "3d8+12", "slashing", ["agile", "magical", "unholy"]),
   B.strike(nid(), "+2 Striking Kukri", 26, "2d6+12", "slashing", ["agile", "deadly-d8", "finesse", "magical", "trip"]),
   B.action(nid(), "Dominate", "2", "<p>One creature within 30 feet must succeed at a "+chk("type:will|dc:33")+" or be "+B.cond("controlled", "Controlled")+" by Bahor (a critical success makes the target immune for a day; the victim re-saves each day). His favourite tool — why fight pawns when you can own them?</p>", ["concentrate", "incapacitation", "mental", "occult"]),
   B.action(nid(), "Read Minds", "1", "<p>Bahor reads the surface thoughts of any creature within 60 feet ("+chk("type:will|dc:33")+" to resist, and he knows who resisted). In conversation, assume he already knows what the PCs want.</p>", ["concentrate", "mental", "occult"]),
   B.action(nid(), "Rakshasa's Mockery", "2", "<p>Bahor turns a victim's own faith against it: one creature within 30 feet takes @Damage[8d6[mental]] ("+chk("type:will|dc:33|basic:true")+"); a divine caster who critically fails is also "+B.cond("stupefied", "Stupefied 2")+" for 1 minute.</p>", ["concentrate", "emotion", "mental", "occult"]),
   B.action(nid(), "Change Shape", "1", "<p>Any humanoid form. 'Glorio Arkona' is merely his favourite mask.</p>", ["concentrate", "polymorph", "occult"]),
   B.action(nid(), "Lord's Resilience", "passive", "<p><strong>Resistance</strong> physical 15 (except piercing holy); immune to disease and to <em>detect</em>-style divinations weaker than his own art. The most dangerous foe of this chapter — the PCs are not expected to beat him at L10.</p>", category="defensive"),
   B.lore(nid(), "Korvosa Lore", 24)],
  notes="<p><strong>Role:</strong> patriarch of the Arkonas — the rakshasa behind 'Glorio.' He wants Ileosa <em>removed</em> (Neolandus is his legal lever, to be played months from now) but cannot hand over the prisoners without looking weak before <strong>Vimanda</strong>. So he deals: <strong>kill Pilts</strong>, and he'll 'help'; afterwards he gifts the <strong>ring of evasion</strong> (its bloodstone is his spy-eye), reveals the elephant-statue passage ('Chamidu is blind'), and sends the PCs into the Labyrinth — secretly dispatching Vimanda to die at their hands, clearing his rival.</p>"
        "<p><strong>If infiltrated instead:</strong> he lets his defenses test the PCs and intervenes only at his chambers (D18) or the treasury — then pitches the same offer. <strong>Story award (negotiation):</strong> learning the prisoners' location from Bahor without violence is worth a full encounter's XP. <strong>If attacked:</strong> he fights in earnest — Extreme-solo at L10, beyond it with marai support — but prefers not to waste good pawns; per the Conclusion he likely survives the chapter in damage-control or vendetta mode.</p>",
  folder=F3["a_creatures"], senses=[{"type": "darkvision"}, {"type": "see-invisibility"}], blurb="Rakshasa patriarch of House Arkona", token_src=None, actor_link=True))

AW("vimanda-arkona", B.npc(A3["vimanda"], "Vimanda (Meliya Arkona)", 12, 33, 230, 21, 24, 22, 22,
  {"str": 6, "dex": 5, "con": 4, "int": 0, "wis": 2, "cha": 5}, 50,
  {"acrobatics": 25, "deception": 26, "stealth": 22, "performance": 20, "diplomacy": 20}, ["fiend", "rakshasa"], ["common", "vudrani"],
  [B.strike(nid(), "+1 Striking Shock Kukri", 25, "2d6+9", "slashing", ["agile", "deadly-d8", "finesse", "magical", "trip"], [("1d6", "electricity")], slug="vimanda-kukri"),
   B.strike(nid(), "Tiger Fist", 25, "2d8+9", "bludgeoning", ["agile", "magical", "unarmed"]),
   B.action(nid(), "Flurry of Blows", "1", "<p>Vimanda makes two Tiger Fist Strikes against one target (combine damage for resistances) — monk-trained, tiger-fast.</p>", ["flourish"]),
   B.action(nid(), "Stunning Fist", "passive", "<p>When both Flurry Strikes hit one creature, it must succeed at a "+chk("type:fortitude|dc:31")+" or be "+B.cond("stunned", "Stunned 1")+" (Stunned 3 on a critical failure).</p>", category="offensive"),
   B.action(nid(), "Javelin of Lightning", "1", "<p>She hurls a crackling javelin: a 60-ft line of @Damage[4d6[electricity]] ("+chk("type:reflex|dc:31|basic:true")+"). She carries two.</p>", ["electricity", "manipulate", "magical"]),
   B.action(nid(), "Suggestion", "2", "<p>One creature within 30 feet: "+chk("type:will|dc:31")+" or follow a reasonable-sounding course (her favourite: 'drink from that pool' beside the E4 poison). She can also cast <em>fly</em>, <em>invisibility</em>, <em>scorching ray</em>, and <em>locate object</em> (tracking Bahor's gifted ring).</p>", ["auditory", "concentrate", "linguistic", "mental", "occult", "incapacitation"]),
   B.action(nid(), "Change Shape", "1", "<p>Any humanoid form — currently a <strong>bedraggled, starved Vencarlo Orisini</strong> (+4 circumstance to the imposture; Deception +30 in this role).</p>", ["concentrate", "polymorph", "occult"]),
   B.action(nid(), "Wand of Dimension Door", "2", "<p>3 charges — her insertion (E21→E13) and her escape. Below half HP she offers alliance against Bahor ('your true enemy'); refused, she doors away to Old Korvosa to plot revenge.</p>", ["concentrate", "magical", "teleportation"]),
   B.action(nid(), "Fiendish Resilience", "passive", "<p><strong>Resistance</strong> physical 10 (except piercing holy); immune to disease; the Labyrinth's symbol traps (keyed to the family) ignore her.</p>", category="defensive"),
   B.lore(nid(), "Underworld Lore", 20),
   B.equipment(nid(), "Gold Armbands", 9, 140, "<p>Vudrani gold armbands (~140 gp re-scaled).</p>", traits=["art-object"])],
  notes="<p><strong>Role:</strong> Bahor's sister-rival — 'Meliya,' the rakshasa who duped Verik Vancaskerkin in Chapter 1. Sent into the Labyrinth by Bahor (framed as an honour; meant as her death), she instead plays her own game: <strong>disguised as a rescued Vencarlo</strong>, she begs the PCs to abandon the dungeon and storm Bahor's chambers. Her tells: her 'scavenged' javelins, her unfamiliarity under <em>detect thoughts</em>-grade scrutiny, and — if the PCs still carry the Chapter 1 <strong>raktavarna</strong> 'silver dagger' — her command that it revert and rejoin her (biting its owner first).</p>"
        "<p><strong>Tactics:</strong> she avoids Sivit absolutely (the sphinx's binding compels attack on traitors). In battle she flies, hurls javelins and rays, then closes with kukri + Stunning Fist flurries — never assuming true form. <strong>Morale:</strong> below half HP she offers a genuine alliance against Bahor; the PCs may end the chapter with a rakshasa 'sibling' as an extremely double-edged ally.</p>",
  folder=F3["a_creatures"], senses=[{"type": "darkvision"}], blurb="Rakshasa rival-sister; the false Vencarlo", token_src=None, actor_link=True))

AW("sivit-darksphinx", B.npc(A3["sivit"], "Sivit, Lady of the Labyrinth", 11, 31, 200, 21, 19, 21, 22,
  {"str": 6, "dex": 3, "con": 5, "int": 6, "wis": 4, "cha": 5}, 40,
  {"deception": 22, "diplomacy": 22, "occultism": 23, "religion": 21, "crafting": 21, "stealth": 18}, ["fiend", "beast"], ["common", "draconic", "infernal", "sphinx", "vudrani", "celestial"],
  [B.strike(nid(), "+1 Striking Kukri", 24, "2d6+9", "slashing", ["agile", "deadly-d8", "finesse", "magical", "trip"]),
   B.strike(nid(), "Claw", 24, "2d10+9", "slashing", ["agile"]),
   B.action(nid(), "Pounce", "2", "<p>Sivit Strides (or Flies) and makes a Claw Strike; if she started the turn hidden or her target was unaware, she follows with a second Claw against the same target.</p>", ["attack"]),
   B.action(nid(), "Twin Kukri Dance", "2", "<p>Two Kukri Strikes against one target (combine damage); on a critical hit her blades also leave the target "+B.cond("off-guard", "Off-Guard")+" until the start of her next turn.</p>", ["flourish"]),
   B.action(nid(), "Unholy Blight", "2", "<p>A 10-ft burst of profane rot within 60 feet: @Damage[7d6[void]] ("+chk("type:fortitude|dc:30|basic:true")+"); on a failure the creature is also "+B.cond("sickened", "Sickened 1")+".</p>", ["concentrate", "manipulate", "occult", "void"]),
   B.action(nid(), "Mistress of Symbols", "passive", "<p>Sivit placed the Labyrinth's four <em>symbol</em> traps (E5/E6/E18/E19 — fear, pain, sleep, stunning; refreshed weekly) and times her ambushes to herd prey across them. Constant: <em>see invisibility</em>, <em>comprehend languages</em>. She scries the lever-rooms (<em>clairvoyance</em>) and tracks odd PC gear (<em>locate object</em>); her <strong>wand of dimension door</strong> (19 charges) returns her to her throne (E20).</p>", category="offensive"),
   B.action(nid(), "Bound to the Labyrinth", "passive", "<p>An old <em>binding</em> (cast by Bahor's slain predecessor, with no release clause) chains her to the dungeon — she cannot pass E2. The same geas compels her to <strong>attack any betrayer of Bahor</strong> she discovers… including Vimanda.</p>", category="defensive"),
   B.lore(nid(), "Labyrinth Lore", 23)],
  notes="<p><strong>Role:</strong> the darksphinx warden of the Vivified Labyrinth — brilliant, bitter, and bound. She knows all four rotations, pulls levers to split parties, and lairs at her throne (E20) with her surviving plaything: <strong>Vencarlo Orisini</strong>, chained at 0 HP.</p>"
        "<p><strong>Tactics:</strong> scry, rotate, herd onto symbols, then pounce from darkness; she retreats by wand when bloodied and <strong>fights to the death</strong> within her prison. <strong>The lever she cannot pull:</strong> reveal Vimanda's treachery to her and the binding does the PCs' work.</p>",
  folder=F3["a_creatures"], senses=[{"type": "darkvision"}, {"type": "see-invisibility"}], size="lg",
  other_speeds=[{"type": "fly", "value": 60}], blurb="Darksphinx warden of the Labyrinth", token_src=None, actor_link=True))

AW("garden-guardian", B.npc(A3["gardenguard"], "Garden Guardian", 8, 27, 130, 17, 14, 14, 16,
  {"str": 5, "dex": 1, "con": 3, "int": 2, "wis": 2, "cha": 1}, 20,
  {"athletics": 18, "stealth": 14, "crafting": 14}, ["plant", "genie"], ["common", "sylvan", "vudrani"],
  [B.strike(nid(), "+1 Scimitar", 20, "2d6+8", "slashing", ["forceful", "magical", "sweep"]),
   B.action(nid(), "Poison Spore Cloud", "2", "<p>A 15-ft burst of choking spores within 30 feet: "+chk("type:fortitude|dc:26")+" or @Damage[4d6[poison]] and "+B.cond("sickened", "Sickened 1")+" (half damage and no sickness on a success).</p>", ["manipulate", "poison"]),
   B.action(nid(), "Fade from Sight", "2", "<p>The guardian turns "+B.cond("invisible", "Invisible")+" (until it Strikes) — their standing order on hearing intruders.</p>", ["concentrate", "occult"]),
   B.action(nid(), "Shrink the Mighty", "2", "<p>One creature within 30 feet: "+chk("type:fortitude|dc:26")+" or shrink one size (weapon damage dice shrink a step; "+B.cond("clumsy", "Clumsy 1")+") for 1 minute. They never enlarge themselves — the ledge is narrow.</p>", ["concentrate", "polymorph", "occult"]),
   B.action(nid(), "Fungal Body", "passive", "<p>A plant-thing wearing a dead janni's memories: immune to disease, paralysis, poison, polymorph, sleep, and mental effects; resistance fire 10. Bound to Arkona will; it attacks anyone not recognized as family.</p>", category="defensive")],
  notes="<p><strong>Role:</strong> four janni slaves murdered into fungal puppetry by the wizard Innachi Naven (who learned the Arkonas' nature and was fed to Senshiir for it). They tend the hidden grotto-garden (D19) and kill all non-Arkonas on sight.</p>"
        "<p><strong>Tactics:</strong> invisible on approach; open with overlapping spore clouds, then scimitars; they shrink the party's biggest threat. They pursue through the cavern but never into D24/D25 or the palace above. They fight to the death — there is nothing left in them to fear with.</p>",
  folder=F3["a_creatures"], senses=[{"type": "darkvision"}, {"type": "low-light-vision"}], blurb="Fungal janni slave-guardian", token_src=None))

AW("enormous-reefclaw", B.npc(A3["enormreef"], "Enormous Reefclaw", 12, 32, 240, 24, 18, 21, 22,
  {"str": 8, "dex": 2, "con": 7, "int": -1, "wis": 3, "cha": 3}, 5,
  {"athletics": 26, "stealth": 19}, ["aberration", "aquatic"], ["common"],
  [B.strike(nid(), "Claw", 26, "3d8+12", "slashing", ["agile", "reach-10"]),
   B.action(nid(), "Crushing Grab", "1", "<p><strong>Requirement</strong> Its last action was a successful Claw Strike.</p><hr /><p><strong>Effect</strong> It Grabs the target (any size; Escape DC 32) and constricts: @Damage[3d8+12[bludgeoning]] ("+chk("type:fortitude|dc:32|basic:true")+") — and the victim is exposed to its numbing venom ("+chk("type:fortitude|dc:32")+" or "+B.cond("enfeebled", "Enfeebled 2")+" for 1 round).</p>", ["attack"]),
   B.action(nid(), "Death Frenzy", "reaction", "<p><strong>Trigger</strong> The reefclaw is reduced to 0 HP.</p><hr /><p><strong>Effect</strong> It thrashes in dying fury — one final Claw Strike against each adjacent creature before it dies or flees.</p>"),
   B.action(nid(), "Territorial", "passive", "<p>It scrupulously avoids damaging the Arkona barge and pier (its feeders' property) but savages all intruders. <strong>Morale:</strong> below ~20 HP it flees to the open sea and never returns.</p>", category="defensive")],
  notes="<p><strong>Role:</strong> a unique, dog-trained horror — charmed long ago by Avidexu, kept fed until the sea-cave became its territory. It guards the Arkona pier (D23) of its own volition: <strong>50% absent (hunting) on the PCs' first visit, always present when they return</strong> — i.e., during the escape with Vencarlo and Neolandus aboard the barge.</p>",
  folder=F3["a_creatures"], senses=[{"type": "darkvision"}, {"type": "low-light-vision"}], size="lg",
  other_speeds=[{"type": "swim", "value": 40}], blurb="Unique pier-guardian reefclaw", token_src=None))

AW("senshiir", B.npc(A3["senshiir"], "Senshiir", 10, 30, 175, 19, 21, 17, 19,
  {"str": 5, "dex": 6, "con": 3, "int": 2, "wis": 3, "cha": 4}, 30,
  {"acrobatics": 22, "medicine": 18, "intimidation": 20, "occultism": 16}, ["fiend", "asura"], ["common", "infernal", "vudrani"],
  [B.strike(nid(), "Blade Dance (4 arms)", 23, "2d8+8", "slashing", ["agile", "magical", "unholy"]),
   B.action(nid(), "Whirling Blades", "2", "<p>Four arms, four blades: Senshiir makes a Blade Dance Strike against each creature within reach (each at the same multiple-attack penalty).</p>", ["flourish"]),
   B.action(nid(), "Anatomist's Eye", "passive", "<p>Centuries of vivisection: her Strikes against "+B.cond("grabbed", "Grabbed")+", "+B.cond("prone", "Prone")+", or restrained creatures deal an extra @Damage[2d6[precision]] and she knows every creature's pain-points ("+chk("type:medicine|dc:10")+" to Recall a victim's weakness as a free action).</p>", category="offensive"),
   B.action(nid(), "Wave of Agony", "2", "<p>A 30-ft cone of remembered pain: @Damage[5d6[mental]] ("+chk("type:will|dc:29|basic:true")+"); creatures that fail are "+B.cond("sickened", "Sickened 1")+".</p>", ["concentrate", "emotion", "mental", "occult"]),
   B.action(nid(), "Asura Resilience", "passive", "<p>Immune to curses and disease; resistance physical 10 (except holy). Born of a god's mistake, she does not fear death — only boredom.</p>", category="defensive"),
   B.lore(nid(), "Torture Lore", 20)],
  notes="<p><strong>Role:</strong> an upasunda asura — the Labyrinth's contract torturer, paid in 'a steady supply of fresh victims.' The quarantine has starved her docket and Bahor forbade marking the 'guest'; she has just strapped a sobbing <strong>Neolandus</strong> to the rack (E21), studying him with detached, infernal curiosity, when the PCs arrive.</p>"
        "<p><strong>Tactics:</strong> a four-armed blade-dancer; she whirls into the thick, carves the restrained, and projects waves of remembered agony. If "+act(A3["vimanda"], "Vimanda")+" is present (un-alerted infiltration), the sisters-in-cruelty fight together: a Moderate-to-Severe room.</p>",
  folder=F3["a_creatures"], senses=[{"type": "darkvision"}], blurb="Four-armed asura torturer", token_src=None))

AW("rajambari", B.npc(A3["rajambari"], "Rajambari", 8, 26, 120, 17, 12, 14, 12,
  {"str": 7, "dex": 1, "con": 0, "int": -5, "wis": 0, "cha": 0}, 40,
  {"athletics": 19}, ["undead", "skeleton", "mindless"], [],
  [B.strike(nid(), "Gore", 20, "2d10+9", "piercing", ["reach-15"]),
   B.strike(nid(), "Slam", 20, "2d8+9", "bludgeoning", ["reach-15"]),
   B.action(nid(), "War Stomp", "2", "<p><strong>Frequency</strong> once per minute. The rajambari slams its forefeet down: every creature on the ground within 20 feet must succeed at a "+chk("type:reflex|dc:26")+" or be knocked "+B.cond("prone", "Prone")+" (it uses this at the first opportunity, mindlessly — even atop other rajambari).</p>", ["attack"]),
   B.action(nid(), "Turn the Wheel", "passive", "<p>Chained to its pillar-axle, each rajambari walks a quarter-circle when the bells ring, rotating the Labyrinth 90°. <strong>Servile:</strong> any command-undead effect lasts double against it; it understands any commander's tongue. If two or more are destroyed, the Labyrinth's configuration <strong>locks permanently</strong>.</p>", category="defensive"),
   B.action(nid(), "Skeletal Bulk", "passive", "<p>Mindless undead; immune to death effects, disease, mental, paralysis, poison, unconscious; resistance cold 10, piercing 10, slashing 10. Huge; it can move at most 15 feet from its pillar.</p>", category="defensive")],
  notes="<p><strong>Role:</strong> four undead mastodons — antique Vudrani necromancy — chained in the Gizzard (E23) as the Labyrinth's engine. Passive unless they or the works are harmed; then all four defend the machine until destroyed, shaking the rooms above (the rooms themselves cannot shift while the gears are locked).</p>",
  folder=F3["a_creatures"], senses=[{"type": "darkvision"}], size="grg", blurb="Skeletal mastodon labyrinth-engine", token_src=None))

AW("vencarlo-orisini", B.npc(A3["vencarlo"], "Vencarlo Orisini", 8, 27, 125, 14, 19, 16, 18,
  {"str": 2, "dex": 6, "con": 1, "int": 2, "wis": 3, "cha": 4}, 25,
  {"acrobatics": 19, "athletics": 14, "deception": 16, "diplomacy": 18, "society": 16, "stealth": 16}, ["humanoid", "human"], ["common", "varisian"],
  [B.strike(nid(), "+1 Rapier", 19, "2d6+5", "piercing", ["deadly-d8", "disarm", "finesse", "magical"]),
   B.action(nid(), "Master's Riposte", "reaction", "<p><strong>Trigger</strong> A creature within his reach critically fails a Strike against him.</p><hr /><p><strong>Effect</strong> Vencarlo makes a Rapier Strike against it — forty years of the academy in one motion.</p>"),
   B.action(nid(), "Disarming Flourish", "1", "<p>Vencarlo attempts to Disarm with a +2 circumstance bonus; on a success he flicks the weapon to any square within 10 feet (he famously took two of Sabina's fingers — and lost two of his own — in such an exchange).</p>", ["attack", "flourish"]),
   B.lore(nid(), "Dueling Lore", 16)],
  notes="<p><strong>Role:</strong> swordmaster, mentor, conscience — and secretly <strong>Blackjack</strong>. Found chained to the western statue of Sivit's throne room (E20) at 0 HP, starved and beaten; the manacle key hides under the throne cushion ("+chk("type:perception|dc:26")+"; "+chk("type:thievery|dc:30")+" without it). Healed and re-armed (his gear sits in the D16 treasury), he insists on helping — <strong>Neolandus first</strong> — and knows the illusory walls of the lower level.</p>"
        "<p><strong>The mask:</strong> confronted about Blackjack he laughs it off; with proof he admits it — after the rescue, after the escape. The mantle, he'll say, has passed before; perhaps it's time it passed again.</p>",
  folder=F3["a_creatures"], blurb="Swordmaster; secretly Blackjack", token_src=None, actor_link=True))

AW("neolandus-kalepopolis", B.npc(A3["neolandus"], "Neolandus Kalepopolis", 5, 18, 60, 9, 11, 12, 12,
  {"str": -1, "dex": 3, "con": 0, "int": 1, "wis": 2, "cha": 2}, 25,
  {"diplomacy": 16, "society": 13, "survival": 11, "deception": 11, "nature": 9}, ["humanoid", "human"], ["common", "varisian"],
  [B.strike(nid(), "Crossbow", 12, "1d8", "piercing", ["range-increment-120", "reload-1"]),
   B.strike(nid(), "Fist", 8, "1d4-1", "bludgeoning", ["agile", "nonlethal"]),
   B.lore(nid(), "Korvosa Politics Lore", 13),
   B.gear("crossbow", nid())],
  notes="<p><strong>Role:</strong> the missing <strong>seneschal of Castle Korvosa</strong> — the one man who can lawfully depose a monarch, and the campaign's living MacGuffin. Found strapped to Senshiir's rack (E21); "+chk("type:society|dc:15")+" recognizes him through the rags (he otherwise claims to be 'Velak,' a caught thief, and begs the PCs to also rescue 'a friend' — Vencarlo). A diplomat, not a fighter: he flees below quarter HP but never abandons an ally.</p>"
        "<p><strong>What he knows</strong> (once sure the PCs aren't the queen's): everything — Ileosa's murder of the king, the Red Mantis, and his terrible conclusion: the queen is host to <strong>the spirit-fragment of Kazavon</strong>, kept deathless by the Crown of Fangs; the lore to defeat it sleeps with the <strong>Shoanti of the Cinderlands</strong> (Chapter 4's hook).</p>",
  folder=F3["a_creatures"], blurb="The missing seneschal; living MacGuffin", token_src=None, actor_link=True))

AW("belker", B.npc(A3["belker"], "Belker", 7, 25, 110, 13, 17, 13, 16,
  {"str": 4, "dex": 5, "con": 2, "int": -2, "wis": 2, "cha": -1}, 0,
  {"acrobatics": 17, "stealth": 17}, ["elemental", "air", "fiend"], ["sussuran"],
  [B.strike(nid(), "Smoke Claw", 18, "2d8+6", "slashing", ["agile", "magical"]),
   B.action(nid(), "Smoke Form", "1", "<p>The belker becomes coiling smoke: it can Fly through gaps, gains resistance physical 5, and may occupy other creatures' squares.</p>", ["concentrate", "polymorph"]),
   B.action(nid(), "Choking Infiltration", "2", "<p><strong>Requirement</strong> Smoke form, sharing a square with a breathing creature.</p><hr /><p><strong>Effect</strong> It pours into the victim's lungs: @Damage[3d6[bludgeoning]] internal damage per round ("+chk("type:fortitude|dc:25|basic:true")+"), and the victim is "+B.cond("sickened", "Sickened 1")+" while it remains. Coughing it out: the victim (or allies dealing it damage) forces it back to claw-form.</p>", None)],
  notes="<p><strong>Role:</strong> smoke-fiends conjured by the Hungry Smoke trap (D8). They materialize at the 20-ft ceiling — their reach raking the floor while most foes can't reach back — and dissipate when slain or when the summons lapses (~1 minute).</p>",
  folder=F3["a_creatures"], senses=[{"type": "darkvision"}], size="lg",
  other_speeds=[{"type": "fly", "value": 50}], blurb="Smoke-fiend of the Hungry Smoke trap", token_src=None))

# ---- hazards ----
hazards = []
def HW(slug, doc):
    hazards.append(copy.deepcopy(doc)); B.write("hazards", slug, doc, embed_items=True)

HW("spreading-house-fire", B.hazard(A3["housefire"], "Spreading House Fire", 8, 0,
  "<p>Obvious once ignited — no check needed.</p>",
  "<p>Douse a burning square with water or smothering ("+chk("type:athletics|dc:26")+" or an appropriate improvisation per square); cold/water magic clears bursts. Left alone, the house is lost.</p>",
  "<p>Distilled alchemist's fire painted invisibly over walls, floors, and furniture — the Red Mantis's prepared ambush-arson. One vial in a fireplace ignites it; each round the blaze spreads to 1d4 adjacent squares.</p>",
  [B.action(nid(), "Burn", "reaction", "<p><strong>Trigger</strong> A creature enters or ends its turn in a burning square.</p><hr /><p><strong>Effect</strong> @Damage[2d6[fire]] ("+chk("type:reflex|dc:26|basic:true")+"); on a critical failure the creature also takes @Damage[1d6[persistent,fire]].</p>"),
   B.action(nid(), "Spread", "free", "<p>At the start of each round, the fire spreads to 1d4 squares adjacent to burning squares. After ~10 minutes unchecked, the structure collapses.</p>")],
  folder=F3["a_hazards"], traits=["environmental", "fire"], reset="<p>Burns until extinguished or the fuel is spent.</p>", complex_=True))

HW("the-tall-knife", B.hazard(A3["tallknife"], "The Tall Knife (Guillotine)", 10, 0,
  "<p>Entirely obvious — that is the point.</p>",
  "<p>"+chk("type:thievery|dc:30")+" to jam the release; Hardness 12, HP 50 to wreck the frame. A strapped victim Escapes with "+chk("type:athletics|dc:30")+" (or 3 rounds of being unstrapped by allies).</p>",
  "<p>Pilts's ornately carved guillotine — 'the Tall Knife,' 'Jabbyr's Tongue,' 'the Demon's Maw' — stands beside the throne (C3). Strapping a willing or helpless victim in takes 3 rounds; Jabbyr triggers it with a single Interact action. No one has survived it yet.</p>",
  [B.action(nid(), "Falling Blade", "reaction", "<p><strong>Trigger</strong> The release is pulled with a victim strapped in.</p><hr /><p><strong>Effect</strong> The blade falls: @Damage[6d12+20[slashing]] to the strapped victim, who must then succeed at a "+chk("type:fortitude|dc:30")+" or <strong>die</strong> (decapitated). A merely held (not strapped) victim takes the damage but not the death save.</p>")],
  folder=F3["a_hazards"], traits=["mechanical", "trap", "death"], reset="<p>Rewinding the blade takes 1 minute.</p>", complex_=False))

HW("hungry-smoke", B.hazard(A3["hungrysmoke"], "Hungry Smoke", 8, 30,
  "<p>"+chk("type:perception|dc:30")+" (trained) to sense the conjuration woven into the display case.</p>",
  "<p>"+chk("type:thievery|dc:30")+" to unweave the ward, or <em>dispel magic</em> (4th rank). Bahor carries the case's only key (an average lock — "+chk("type:thievery|dc:25")+" to pick).</p>",
  "<p>The locked glass case beneath the smoking-den stairs (D8). Any attempt to damage the case or pick its lock tears the seal on a bound summoning.</p>",
  [B.action(nid(), "Disgorge Belkers", "reaction", "<p><strong>Trigger</strong> The case is damaged or its lock tampered with.</p><hr /><p><strong>Effect</strong> Two "+act(A3["belker"], "belkers")+" boil out of the hookah-smoke at the 20-ft ceiling and attack for 1 minute before dissipating.</p>")],
  folder=F3["a_hazards"], traits=["magical", "trap"], reset="<p>None — the binding must be re-laid.</p>", complex_=False))

HW("symbol-of-fear", B.hazard(A3["symfear"], "Symbol of Fear (E5)", 7, 29,
  "<p>"+chk("type:perception|dc:29")+" (trained) to spot the glyph on the wall opposite the entrance before sight falls on it.</p>",
  "<p>"+chk("type:thievery|dc:29")+" to scour it, or <em>dispel magic</em> (4th rank).</p>",
  "<p>One of Sivit's weekly-renewed <em>symbol</em> glyphs, keyed to spare the Arkona household; it guards the refreshing pool.</p>",
  [B.action(nid(), "Glyph of Terror", "reaction", "<p><strong>Trigger</strong> A non-keyed creature sees the symbol.</p><hr /><p><strong>Effect</strong> Every such viewer within 60 feet: "+chk("type:will|dc:27")+" or "+B.cond("frightened", "Frightened 2")+" and "+B.cond("fleeing", "Fleeing")+" for 1 round (Frightened 3 on a critical failure).</p>")],
  folder=F3["a_hazards"], traits=["magical", "trap", "fear", "mental"], reset="<p>None (Sivit re-inscribes weekly).</p>", complex_=False))

HW("symbol-of-pain", B.hazard(A3["sympain"], "Symbol of Pain (E6)", 6, 28,
  "<p>"+chk("type:perception|dc:28")+" (trained) to spot the floor-glyph.</p>",
  "<p>"+chk("type:thievery|dc:28")+" to scour it, or <em>dispel magic</em> (4th rank).</p>",
  "<p>Sivit's pain-glyph on the floor of the bare room E6 — a pure trap room.</p>",
  [B.action(nid(), "Glyph of Agony", "reaction", "<p><strong>Trigger</strong> Sight (non-keyed).</p><hr /><p><strong>Effect</strong> Viewers within 60 feet: "+chk("type:fortitude|dc:26")+" or wracked with pain — "+B.cond("enfeebled", "Enfeebled 2")+" and "+B.cond("clumsy", "Clumsy 2")+" for 10 minutes (1 hour on a critical failure).</p>")],
  folder=F3["a_hazards"], traits=["magical", "trap", "mental"], reset="<p>None (re-inscribed weekly).</p>", complex_=False))

HW("symbol-of-sleep", B.hazard(A3["symsleep"], "Symbol of Sleep (E18)", 6, 28,
  "<p>"+chk("type:perception|dc:28")+" (trained) to spot the floor-glyph.</p>",
  "<p>"+chk("type:thievery|dc:28")+" to scour it, or <em>dispel magic</em> (4th rank).</p>",
  "<p>Sivit's sleep-glyph in the Hall of Slumber — one of the two rooms that rotates open onto her throne.</p>",
  [B.action(nid(), "Glyph of Slumber", "reaction", "<p><strong>Trigger</strong> Sight (non-keyed).</p><hr /><p><strong>Effect</strong> Viewers within 60 feet: "+chk("type:will|dc:26")+" or fall "+B.cond("unconscious", "Unconscious")+" for 1 minute (10 minutes on a critical failure). Sivit times her pounce for the snoring.</p>")],
  folder=F3["a_hazards"], traits=["magical", "trap", "sleep", "mental"], reset="<p>None (re-inscribed weekly).</p>", complex_=False))

HW("symbol-of-stunning", B.hazard(A3["symstun"], "Symbol of Stunning (E19)", 8, 30,
  "<p>"+chk("type:perception|dc:30")+" (trained) to spot the floor-glyph in the crooked hall.</p>",
  "<p>"+chk("type:thievery|dc:30")+" to scour it, or <em>dispel magic</em> (5th rank).</p>",
  "<p>Sivit's strongest glyph, in the other throne-adjacent hall (E19).</p>",
  [B.action(nid(), "Glyph of Stunning", "reaction", "<p><strong>Trigger</strong> Sight (non-keyed).</p><hr /><p><strong>Effect</strong> Viewers within 60 feet: "+chk("type:fortitude|dc:28")+" or "+B.cond("stunned", "Stunned 2")+" (stunned a full round on a critical failure).</p>")],
  folder=F3["a_hazards"], traits=["magical", "trap", "incapacitation", "mental"], reset="<p>None (re-inscribed weekly).</p>", complex_=False))

HW("insanity-mist-chest", B.hazard(A3["insanitychest"], "Insanity Mist Chest (E7, right)", 7, 25,
  "<p>"+chk("type:perception|dc:25")+" to spot the bellows-seam in the lid ('Breathe deep your salvation').</p>",
  "<p>"+chk("type:thievery|dc:25")+" to disable the bellows before opening.</p>",
  "<p>The right-hand chest of the Three Flavors of Venom: opening it floods the room with insanity mist (it disperses after 1 round).</p>",
  [B.action(nid(), "Mist Burst", "reaction", "<p><strong>Trigger</strong> The chest is opened.</p><hr /><p><strong>Effect</strong> Every breathing creature in the room: "+chk("type:fortitude|dc:25")+" or "+B.cond("confused", "Confused")+" for 1 round and "+B.cond("stupefied", "Stupefied 2")+" for 10 minutes (Confused for 1 minute on a critical failure).</p>")],
  folder=F3["a_hazards"], traits=["mechanical", "trap", "poison", "inhaled"], reset="<p>None (single charge).</p>", complex_=False))

HW("terinav-chest", B.hazard(A3["terinavchest"], "Terinav-Treated Chest (E7, left)", 7, 25,
  "<p>"+chk("type:perception|dc:25")+" to notice the oily sheen on the wood ('By gentle caress shall truth be known').</p>",
  "<p>"+chk("type:thievery|dc:25")+" (gloved, with tools) to neutralize the contact venom.</p>",
  "<p>The left-hand chest — empty, its entire surface painted with terinav-root contact poison.</p>",
  [B.action(nid(), "Contact Venom", "reaction", "<p><strong>Trigger</strong> Bare flesh touches the chest.</p><hr /><p><strong>Effect</strong> "+chk("type:fortitude|dc:25")+" or @Damage[3d6[poison]] and "+B.cond("clumsy", "Clumsy 2")+" for 1 hour (plus "+B.cond("slowed", "Slowed 1")+" for 1 minute on a critical failure).</p>")],
  folder=F3["a_hazards"], traits=["mechanical", "trap", "poison", "contact"], reset="<p>None until repainted.</p>", complex_=False))

HW("biting-tigers", B.hazard(A3["bitingtigers"], "The Biting Tigers (E9)", 10, 28,
  "<p>"+chk("type:perception|dc:28")+" to read the malice in the mounted tiger-heads; "+chk("type:perception|dc:30")+" finds the bypass switch beside each entrance (suppresses the room 3 rounds, re-pressable) — and a second "+chk("type:perception|dc:30")+" the secret door to E10.</p>",
  "<p>The bypass switch, or destroy heads: each AC 28, Hardness 5, HP 40.</p>",
  "<p>First of Mapras's obstacle rooms (Bahor killed his father but kept his toys): preserved tiger heads on serpentine necks line the corridor, animating one round after a creature enters, watched by an invisible arcane eye.</p>",
  [B.action(nid(), "Snapping Heads", "free", "<p><strong>Routine</strong> (each round): four heads lash at four random creatures in the corridor — Strike +24, @Damage[2d10+8[piercing]] each.</p>")],
  folder=F3["a_hazards"], traits=["magical", "mechanical", "trap"], reset="<p>Automatic.</p>", complex_=True))

HW("fangs-of-diomazul", B.hazard(A3["fangsdiom"], "The Fangs of Diomazul (E10)", 10, 25,
  "<p>"+chk("type:perception|dc:25")+" to glimpse the blade-track beneath the well's four inches of dark water. "+chk("type:religion|dc:30")+": the statue is <strong>Diomazul</strong>, the Serpent of Eighty Blades, an obscure Vudrani god of battle-fury.</p>",
  "<p>"+chk("type:thievery|dc:25")+" at the mechanism, or the hidden bypass switch.</p>",
  "<p>A serpent-fountain ringed by a hidden blade carousel: two rounds after entry the blades spring out and spin for 5 rounds (difficult terrain near the well), then retract and re-arm.</p>",
  [B.action(nid(), "Whirling Blades", "free", "<p><strong>Routine</strong> (5 rounds): every creature on the ground within 5 feet of the well takes @Damage[6d6[slashing]] ("+chk("type:reflex|dc:29")+" negates that round).</p>")],
  folder=F3["a_hazards"], traits=["mechanical", "trap"], reset="<p>Automatic; re-triggers 2 rounds after re-entry.</p>", complex_=True))

HW("wailing-maidens", B.hazard(A3["wailingmaidens"], "The Wailing Maidens (E11)", 10, 28,
  "<p>"+chk("type:perception|dc:28")+" to note the tilt-seams between the eight iron-maiden alcoves (bypass switch "+chk("type:perception|dc:30")+" as in the other obstacle rooms).</p>",
  "<p>The bypass switch, or "+chk("type:thievery|dc:28")+" on the floor mechanism; resetting takes 5 audible, grinding rounds.</p>",
  "<p>A two-stage horror, springing 3 rounds after a creature crosses the lane: the floor tilts 45° ("+chk("type:reflex|dc:12")+" or slide into the kill-lane and fall "+B.cond("prone", "Prone")+"), the western maidens wail, the eastern fire spikes.</p>",
  [B.action(nid(), "Stunning Wail", "free", "<p><strong>Stage 1:</strong> every creature in the lane: "+chk("type:fortitude|dc:29")+" or "+B.cond("stunned", "Stunned 1")+" and "+B.cond("deafened", "Deafened")+" for 1d4 rounds.</p>"),
   B.action(nid(), "Spike Barrage", "free", "<p><strong>Stage 2 (routine, 4 rounds):</strong> long-shaft spikes lance across the lane — Strike +21, @Damage[2d10+8[piercing]] against each creature between the alcoves, once per round.</p>")],
  folder=F3["a_hazards"], traits=["magical", "mechanical", "trap", "auditory"], reset="<p>Automatic after 5 rounds (audibly).</p>", complex_=True))

HW("stinging-wasps", B.hazard(A3["stingingwasps"], "The Stinging Wasps (E12)", 8, 25,
  "<p>"+chk("type:perception|dc:25")+" to notice the thousands of needle-holes in the wasp-swarm mosaic (bypass switch "+chk("type:perception|dc:30")+").</p>",
  "<p>The bypass switch, or "+chk("type:thievery|dc:25")+" on a wall panel.</p>",
  "<p>Walls, floor, and ceiling stab in rippling waves of six-inch numbing needles a round after entry; the room is difficult terrain while active.</p>",
  [B.action(nid(), "Needle Wave", "free", "<p><strong>Routine</strong> (while any creature remains): Strike +23 against every creature touching a surface — @Damage[1d6+4[piercing]], and "+chk("type:fortitude|dc:26")+" or "+B.cond("clumsy", "Clumsy 1")+" from the numbing toxin (cumulative, to Clumsy 4).</p>")],
  folder=F3["a_hazards"], traits=["magical", "mechanical", "trap", "poison"], reset="<p>Automatic.</p>", complex_=True))

# =====================================================================
# JOURNAL — "3. Escape from Old Korvosa"
# =====================================================================
SR = lambda area, p: f'<p class="source"><em>Source: CotCT (2016 HC), Ch.3, {area} — p.{p}.</em></p>'
pages = []
def PG(name, html, level=2): pages.append(B.page(nid(), name, html, level=level))
def area3(code, name, html): PG(f"{code}. {name}", html, level=3)
def encx(levels, pl):
    e = B.encounter(levels, party_level=pl); return f"{e['band']} · {e['xp']} XP @ L{pl}"

PG("Chapter Background", SR("Chapter Background", 134)
  + B.s_milestone("<p><strong>Chapter 3 — Escape from Old Korvosa.</strong> The queen's madness blossoms as Kazavon's fragment quickens within her. Quarantined Old Korvosa rots under mob rule — and somewhere in it hides the city's salvation: the missing seneschal, <strong>Neolandus Kalepopolis</strong>, the one man who can legally depose a corrupt monarch. PCs begin at <strong>8th level</strong> → 9th after the Emperor of Old Korvosa → 10th before the Vivified Labyrinth → nearly 11th by chapter's end.</p>")
  + SEC("<p><strong>Kazavon's whispers (GM only).</strong> For centuries the fangs whispered to sensitive souls, breeding madmen instead of servants. When Ileosa freed the dragon's spirit-fragment, its seven current 'projects' lost their muse — six killed themselves; the seventh is the painter <strong>Salvator Scream</strong>, Pilts Swastel's gore-artist at Exemplary Execrables.</p>")
  + SEC("<p><strong>The Neolandus chain (the chapter's spine):</strong> the wounded seneschal fled the Red Mantis to his secret friend Salvator → Salvator hid him with the Arkonas (patron 'Glorio Arkona' — actually the rakshasa <strong>Bahor</strong>) → the Arkonas now cage Neolandus as an insurance policy against the queen. <strong>Vencarlo</strong>, investigating, was ambushed by the Red Mantis (they suspect he is Blackjack), survived, tried to infiltrate Arkona Palace — and is now a prisoner alongside the man he sought. The trail the PCs must follow: Vencarlo's home → Salvator → Pilts → the Arkonas.</p>"))

PG("The Crown Revealed", SR("The Crown Revealed", 136)
  + "<p>As the plague breaks, Queen Ileosa — wearing a new crown set with curved fangs — calls a surprise public address. Flanked by Sabina Merrin, the bloatmage seneschal <strong>Togomor</strong>, Cressida Kroft, and Sable Company commandant <strong>Marcus Endrin</strong>, she declares victory over blood veil (deftly spinning Davaulus's fate), names the <strong>Gray Maidens</strong> Korvosa's official protectors with Sabina as general — and <strong>disbands the Sable Company</strong>, seizing its holdings and demanding Endrin surrender his badge.</p>"
  + SEC("<p><strong>The assassination attempt.</strong> Endrin steps forward, trembling — then hurls his badge into the queen's face, bellows that her shameful reign ends today, and puts an arrow into her right temple before anyone can move. A perfect, fatal shot, sunk deep. <strong>Ileosa does not fall.</strong> Relay what the stunned witnesses saw (the PCs should hear all of this secondhand — <strong>time it</strong> just after Davaulus dies, while they are still mopping up the temple below the hospice):</p>")
  + box("With incredible speed, she regains her composure",
        "<p>The queen recovers in a heartbeat. She wrenches the arrow out of her own skull, and before the blood can run as far as her jaw she is standing in front of Endrin. One hand snaps shut around his throat and hoists the commandant into the air for the whole plaza to see — then she rams his own arrow up beneath his jaw and out through the side of his face.</p>")
  + box("As Endrin's body crumples to the ground",
        "<p>As Endrin crumples, the queen shakes his blood from her fingers and cries out, in a strong clear voice, that this is the fate awaiting every enemy of Korvosa — that his punishment is only the first. Then Togomor takes her hand and teleports her back to the castle, and the Gray Maidens drown the erupting riot in steel. Cressida Kroft flees to Citadel Volshyenek, horrified by what she has witnessed. (Endrin survives — he can be rescued from the Longacre Building in Chapter 4.)</p>")
  + B.s_conv("<p>This is the campaign's mid-point reveal: Ileosa is now visibly superhuman, the Gray Maidens are the law, and open opposition is suicide. The city reels — their queen cannot be killed. The <em>Crown of Fangs</em> artifact debuts here; the queen retreats from public view until Chapter 6's endgame begins to turn.</p>"))

PG("The Third Harrowing", SR("The Third Harrowing", 136)
  + "<p>Best timed soon after the Urgathoan cult's defeat. Zellara senses Ileosa's gathering strength — though not yet what it signifies — and uses her empathic link to plant an itch in the deck-bearer's mind: <em>deal the cards</em>. If the PC doesn't oblige within a day or two, she takes matters into her own hands the next time the PCs are alone, manifesting via <em>major image</em> and performing the reading herself.</p>"
  + B.s_skill("<p><strong>The Third Harrowing.</strong> This reading generates the chapter's <strong>Harrow Points</strong> (Conversion Guide → <em>The Harrowing</em>). This chapter is tied to the suit of <strong>books</strong> and to <strong>Intelligence</strong> — a chapter of masks, lies, and puzzles rewarded for thinking.</p>")
  + "<p><strong>Interpreting the spread:</strong></p><ul>"
    "<li><strong>Past:</strong> dwell on despots — cruel overlords and dictators, drawn from the campaign so far or from each PC's own history.</li>"
    "<li><strong>Present:</strong> Korvosa's wounds — oppression, martial law, and the dawning certainty that the queen herself may want the PCs dead.</li>"
    "<li><strong>Future:</strong> be grim — ghosts; demonic beasts (<em>tigers</em> and <em>mantises</em> especially); life as a cruel, vindictive play or other work of art; and the recurring image of beautiful women with ashen skin and blank faces (the Gray Maidens).</li>"
   "</ul>"
  + SEC("<p><strong>The Rakshasa card.</strong> If it appears anywhere in the spread, give it special weight: depending on its position, play up its meanings of <em>dominance</em> or of <em>freedom from enslavement</em>. The players won't understand until Arkona Palace — then they'll remember.</p>"))

PG("Whispers from Old Korvosa (Cressida's Mission)", SR("Whispers from Old Korvosa", 138)
  + "<p>Soon after, a haggard Cressida summons the PCs to a nearly deserted Citadel Volshyenek and, behind a <em>mage's private sanctum</em>, lays it out: Korvosa is being murdered by its queen, and only the PCs can act.</p>"
  + box("Korvosa is dying. No, strike that.",
        "<p>'Korvosa is dying. No — Korvosa is being <em>murdered</em>. Killed by our queen. The evidence tying her to the plague was damning enough; now she has disbanded the Sable Company and handed our own funding to her Gray Maidens. If I move against her, my guards are dead by sundown. But she must be stopped — and I know no one else who can do this.'</p>")
  + box("You see, just this morning, new information",
        "<p>'New word reached me only this morning. Vencarlo has been my truest ear among the people, and even under the quarantine he found ways to smuggle a report out to me <em>every single day</em>. His latest claimed he'd discovered something vital about the queen — something about dark magic, a pact with a devil — and, more astounding still, that he had a lead suggesting Seneschal Kalepopolis may yet be hiding in Old Korvosa. Then the messages stopped. That was several days ago, and I fear for him.'</p>")
  + B.s_skill("<p><strong>The mission:</strong> infiltrate quarantined Old Korvosa, find Vencarlo (start at his home by the Orisini Academy), and trace Neolandus — whose return would give the queen's opponents a <em>legal</em> lever against her. Cressida warns of the new 'Emperor of Old Korvosa' holding the streets. Ironically the island is the <em>safest</em> place for queen-hunted PCs — if they keep a low profile and avoid Gray Maidens. <strong>Timeline note:</strong> Vencarlo's daily smuggled messages ran unbroken from the quarantine's start until several days ago — dating his disappearance precisely.</p>")
  + B.s_treasure("<p><strong>Cressida's cache</strong> (the citadel's last reserves): 4 potions of <em>cure serious wounds</em> (moderate healing potions), 3 potions of <em>lesser restoration</em>, a <strong>wand of invisibility</strong> (10 charges), and a <strong>wand of cure moderate wounds</strong> (30 charges).</p>"))

PG("Old Korvosa Today", SR("Old Korvosa Today", 139)
  + "<p>Endrin Isle is sealed: the Gray Maidens burned every wooden bridge, walled the stone Jeggare Bridge with a 15-ft <em>wall of stone</em> barricade, and patrol the Narrows in swift barges. <strong>Anyone may enter; no one may leave</strong> — escapees are warned once, then fired upon.</p>"
  + "<p><strong>The four wards:</strong> <em>Fort Korvosa</em> (highest, most orderly — the Arkonas' redoubt) · <em>Garrison Hill</em> (burned, scavenger-haunted) · <em>Bridgefront</em> (worst-off, morale shattered) · <em>Old Dock</em> (the most dangerous — the Emperor's domain).</p>"
  + B.s_skill("<p><strong>Getting in/out:</strong> flight or teleportation trivializes it; otherwise a night swim or skiff across the northern Jeggare ("+chk("type:athletics|dc:15")+" to swim quietly; "+chk("type:stealth|dc:18")+" to evade the barge patrols), returning via the dark, half-burned far side of the Narrows. Don't over-police it — any half-decent plan works.</p>")
  + "<p><strong>Strange times in Old Korvosa</strong> — color the streets with the desperate and the broken whenever the PCs travel:</p>"
  + box("A flock of incongruously happy children sing",
        "<p>A knot of strangely cheerful children ring a toy guillotine built from sticks and pegs, feeding it a procession of dolls while they sing a skipping rhyme — 'Headless, headless, that's what you'll be…' — about brand-new dolls for the Emperor's cemetery, and the chop-chop of the tall knife waiting for the day Korvosa falls. Pressed, they boast (falsely) that they've been to see the Emperor's real 'tall knife' at his palace.</p>")
  + "<ul>"
    "<li><strong>Rook, the mad plague doctor</strong> ("+act("queensPhysician1", "Queen's Physician (2)")+"): the highest Perception roll in the party hears a chirping, cooing voice — more human than bird — from a nearby alley. Within crouches a man in a filthy beaked mask. The plague broke his mind: he remembers nothing of his old life and believes himself a birdlike psychopomp called <em>Rook</em>. He offers to 'breathe in the sick' from the PCs so they never fall ill again; the 'cure' does nothing, and at the GM's discretion close contact may expose them to something worse.</li>"
    "<li><strong>Old Mother Mifeg</strong> (a sad old fungus-seller): shuffles the street edges hawking dully colored pigment-fungi, sobbing that she may not earn enough coppers to feed her six children. The truth is crueler — she is her family's only blood veil survivor, and the rotting bodies she tends so lovingly at home are, to her, merely 'sleeping off the sick.'</li>"
    "<li><strong>Tesh Zobberdin</strong> (a doomed avenger): wild-eyed in ill-fitting leather, marching on Old Dock with sword drawn — last of a family the Emperor executed. He is hopelessly outmatched, but could serve the PCs as a guide.</li>"
    "<li><strong>Olmere Bliversin</strong> (the ranting baker): harangues the empty street from his balcony — what will the queen do about the mob? the bridges? the quarantine? — in his nightclothes, every demand punctuated by a high-pitched giggle.</li>"
   "</ul>"
  + SEC("<p><strong>The mob.</strong> Unless the PCs stay unobtrusive, each hour carries a 10% chance (50% per 10 minutes in Old Dock) that mob soldiers notice them — four "+act(A3["empthug"], "Emperor's Thugs")+", arrogant and jeering, demand to know their business in 'the emperor's domain.' Any answer except 'We're here to join you' draws scorn and an order to hand over weapons. <strong>PCs who comply are escorted to the throne balcony (C3)</strong> to be judged by the Emperor, their gear stacked beside his throne as an offering. The mob should be the PCs' <em>first</em> encounter; afterwards roll on the Korvosa Street Encounter table (Appendices).</p>")
  + B.enc("Pilts's Mob (recurring, in waves)", encx([6, 6, 6, 6], 8),
     "<p>4 "+act(A3["empthug"], "Emperor's Thugs")+" — the standard shakedown. They open with nonlethal fists (live captives amuse the Emperor) and draw axes only if the PCs fight lethally; each flees at ~10 HP. <strong>Escalation:</strong> if the PCs cut down the first group, <strong>two more groups of four</strong> converge 3d6 minutes later ("+encx([6]*8, 8)+"); if those fall too, a <strong>fourth group of four</strong> arrives in another 3d6 minutes — this one extending a wary <em>invitation</em> to meet the Emperor. PCs who accept keep their gear, but are shadowed by thugs all the way to the palace.</p>",
     B.aside_token(["4× "+act(A3["empthug"], "Emperor's Thug (6)")])))

area3("A", "Vencarlo's Home", SR("A — Vencarlo's Home", 141)
  + "<p>A humble house in southern Fort Korvosa, beside the charred ruin of the <strong>Orisini Academy</strong> (burned by the Red Mantis after Vencarlo escaped their ambush). The door is unlocked; the rooms are warm, quiet, unlit — and both fireplaces are burning in an 'empty' house.</p>"
  + B.s_skill("<p><strong>Reading the scene:</strong> "+chk("type:perception|dc:24")+" (in A7/A8; +10 with scent) catches a strange-tanged smoke; "+chk("type:crafting|dc:20")+" identifies <strong>residual alchemist's fire</strong>, and "+chk("type:perception|dc:26")+" finds it faintly staining walls, floor, and furniture. "+chk("type:survival|dc:24")+": no real traffic since Vencarlo's last letter; "+chk("type:survival|dc:29")+": faint marks of a <em>very</em> stealthy recent visitor.</p>")
  + "<p><strong>The rooms (A1–A8):</strong> a Vudrani-rug entry · a blade-repair workshop · bath · a study of fencing and philosophy texts (the academy's books show business dying after the king's death) · pantry · the living room (lit hearth, hiding-nook under the stairs) · the double-height training room (lit hearth, open rafters) · Vencarlo's unslept-in bedroom.</p>"
  + SEC("<p><strong>The ambush.</strong> Two "+act(A3["redmantis"], "Red Mantis assassins")+" squat here in 8-hour shifts (relieved from the guild's hideout below the Longacre Building — a Chapter 4 thread), waiting for Vencarlo. One hides under the A6 stairs, one in the A7 rafters. They pre-buff the moment anyone enters and spring when a PC climbs to A7 — opening by igniting <strong>both fireplaces</strong> into the "+haz(A3["housefire"], "Spreading House Fire")+".</p>")
  + B.enc("Red Mantis ambush", encx([8, 8], 8),
     "<p>2 "+act(A3["redmantis"], "Red Mantis assassins")+" + the "+haz(A3["housefire"], "fire")+" they are warded against. A telegraphed set-piece: the fire punishes slow play, and the assassins use it as terrain.</p>",
     B.aside_token(["2× "+act(A3["redmantis"], "Red Mantis Assassin (8)"), haz(A3["housefire"], "Spreading House Fire (8)")]))
  + B.s_treasure("<p><strong>The Blackjack cache.</strong> "+chk("type:perception|dc:29")+" in the A8 closet reveals a hidden panel; the iron lockbox within ("+chk("type:thievery|dc:40")+", or Hardness 10 / 40 HP — the key is with Vencarlo's confiscated gear in the Arkona vaults, D16) holds a <strong>bag of holding (type I)</strong> containing Blackjack's full regalia: a black hooded <strong>cloak of elvenkind</strong>, several masks, 12 masterwork 'B'-pommeled daggers, <strong>+1 resilient slick leather armor</strong>, <strong>boots of elvenkind</strong>, an <strong>amulet of proof against detection</strong>, black <strong>gloves of climbing and swimming</strong> (two fingers of the right glove false and adjustable — concealing Vencarlo's old dueling wound), and a <strong>+2 striking keen rapier</strong>. "+chk("type:society|dc:15")+" (automatic for anyone who saw the execution rescue) recognizes <strong>Blackjack's</strong> signature gear.</p>")
  + B.s_conv("<p><strong>The Blackjack legacy.</strong> The mantle has passed hero-to-hero for generations; Vencarlo is merely its latest bearer. With this cache, <em>a PC could become the next Blackjack</em> — encourage it; the regalia is sized to fit its wearer. If the PCs don't fight the fire, the house burns (citizens + Arkona brigades contain the blaze but can't save it; the lockbox survives, "+chk("type:perception|dc:26")+" in the rubble).</p>"))

area3("A½", "The Concerned Student", SR("The Concerned Student", 145)
  + "<p>Drawn by the flames or the fight, a familiar face approaches: <strong>Amin Jalento</strong> (the noble the PCs may have saved from the Chapter 1 mob — or his cousin Gerran, if Amin died), trapped on the island by the quarantine and squatting in a collapsed building across from the academy.</p>"
  + "<p>His story: he was Vencarlo's houseguest when <strong>Red Mantis assassins stormed the academy</strong> — Vencarlo cut one down and fled; the assassins burned the school. Before that, Vencarlo kept strange hours, came home bloodied, and met three times behind closed doors with a wild-haired, paint-stained visitor Amin recognized: the notorious artist <strong>Salvator Scream</strong>. Their last meeting ended in shouting. Salvator lives at <strong>140 Wave Street, Old Dock</strong> — the Emperor's territory.</p>"
  + B.s_treasure("<p><strong>Story awards:</strong> learning of Salvator Scream → <strong>2,400 XP</strong>; escorting Amin safely off the island → a further <strong>4,800 XP</strong>.</p>"))

PG("B. The Artist's Lair", SR("B — The Artist's Lair", 145)
  + B.s_milestone("<p><strong>B. The Artist's Lair</strong> — Salvator Scream's leaning, decrepit house at <strong>140 Wave Street</strong>, Old Dock, near a ruined Narrows bridge. "+chk("type:diplomacy|dc:15")+" (gather information) confirms the address and the artist's grisly reputation (Exemplary Execrables' backdrop painter); "+chk("type:society|dc:22")+" knows who Salvator Scream is outright. A <em>locate creature</em> would reveal Salvator is no longer here — the Emperor's thugs took him days ago.</p>")
  + SEC("<p><strong>Who's actually home:</strong> "+act(A3["laori"], "Laori Vaus")+", squatting amid her investigation. She is <em>friendly</em> unless attacked — let her be the PCs' strangest handshake of the campaign.</p>")
  + SEC("<p><strong>Laori's hidden layer (GM only).</strong> The chipper elf is a priestess of <strong>Zon-Kuthon</strong> and an agent of the <strong>Brotherhood of Bones</strong> — Kuthite fanatics sworn to secure the relics of <strong>Kazavon</strong> so no one can ever resurrect the warlord. Her 'hunt for the criminal Andaisin' was cover for a relic-search; she instead found Kazavon's influence saturating seven local artists — and, most potent of all, the city's new <em>queen</em>. When Ileosa appeared publicly wearing fangs on her crown, Laori was stunned; she now watches and waits while her superiors deliberate.</p>")
  + B.s_conv("<p><strong>Sanctioned early reveal.</strong> The intended endgame revelation — that the fangs on Ileosa's crown are <strong>Kazavon's teeth</strong>, and that is why she cannot be killed — is normally learned from Neolandus at the chapter's end. The AP explicitly blesses letting the PCs learn it <em>early</em> from Laori instead (under magical compulsion, or if she comes to trust them). Nothing breaks: the PCs still need the seneschal to learn how such power can be fought.</p>"))

area3("B1-B2", "Front Room & Bedroom", SR("B1-B2", 146)
  + box("The smell in this entryway is of must and",
        "<p>The entry smells of must and old paint; muddy boot prints track across the floor past a single emptied shelf.</p>")
  + box("A single bed, the blankets and pillows",
        "<p>In the bedroom, a single bed stands to the south, its blankets and pillows flung into disarray. More muddy boot prints scar the floorboards — and a splash of dried blood darkens one pillow.</p>")
  + B.s_skill("<p>"+chk("type:survival|dc:24")+" (front room): a half-dozen people tromped through — and a seventh was <strong>dragged out</strong>, toes scuffing. "+chk("type:survival|dc:24")+" (bedroom): the prints converge on the bed — Salvator was clubbed in his sleep (the blood) and carried off. The trail is days old and leads toward central Old Dock: <strong>Pilts's Palace</strong>.</p>"))

area3("B3", "Salvator's Studio", SR("B3", 146)
  + box("Both of this room's windows are tightly shuttered, yet",
        "<p>Both windows are tightly shuttered, yet candlelight flickers within: six polished human skulls arranged in an arc across a paint-spattered desk, a lit taper atop each. Gruesome unsold canvases lean ten deep against the walls.</p>")
  + "<p>"+act(A3["laori"], "Laori Vaus")+" works here among the skulls of Kazavon's six suicides — left to right: <strong>Jeonia Chirco</strong> the costumer, <strong>Boathar Kaay</strong> the toymaker, <strong>Velaka Hoon</strong> the writer, <strong>Maxtel Erns</strong> the sculptor, <strong>Yvos Tanguany</strong> the tattooist, and <strong>Imon Vernell</strong> the poet (she names them fondly) — questioning the dead with mostly-garbled results. She saved Salvator for last, judging Kazavon's whispers strongest in his work, and arrived to find him already taken.</p>"
  + SEC("<p><strong>Her bargain:</strong> an alliance to reach Salvator, sealed by her evidence — a bloodstained sleeve-scrap bearing the city's coat of arms, found wedged behind the bed ("+chk("type:society|dc:22")+": it is from the uniform of the <strong>seneschal of Castle Korvosa</strong> — torn when Salvator splinted Neolandus's broken arm). She reveals the Emperor of Old Korvosa holds Salvator. Asked if she means the artist harm, she laughs the idea off, truthfully: she only wants to ask where his inspiration comes from.</p>")
  + SEC("<p><strong>What she admits vs. conceals:</strong> she owns her Zon-Kuthon faith freely if asked (his art shares her god's themes, she says) — but volunteers nothing of the <strong>Brotherhood of Bones</strong>, her suspicions of the queen, or <strong>Kazavon</strong>. Only magical compulsion pries those loose — unless you opt for the sanctioned early crown reveal (see the Artist's Lair overview). She is wariest of paladins and priests of Shelyn.</p>")
  + B.s_treasure("<p><strong>Story award:</strong> dealing with Laori peacefully and forming the alliance is worth XP as if the party had defeated her in combat — a full Severe encounter's award (PF1e 9,600 XP).</p>")
  + B.s_conv("<p><strong>If rebuffed:</strong> she looks briefly hurt, bounces back, predicts they'll meet again, and leaves — then shadows the party, waiting to 'reappear' once they find Salvator, ideally by saving their lives in a fight gone bad to prove her good intentions.</p>"))

area3("B4", "Fungal Incursion", SR("B4", 147)
  + box("This room appears to have once been a combination",
        "<p>A onetime kitchen and storeroom, now riotous with fungal growth — Salvator's pigment-cultivation gone feral in his absence.</p>")
  + "<p>A patch of "+YELLOW_MOLD+" (the official L8 hazard) chokes the sunless northeast corner — Salvator handled his samples only in sunlight; his abductors didn't know to.</p>"
  + B.s_treasure("<p>Beneath the growth, among the painting supplies: a full jar of <strong>marvelous pigments</strong> — the chapter's signature wondrous treasure.</p>"))

area3("B5", "The Sinkhole", SR("B5", 147)
  + box("What once might have been a small house has",
        "<p>What once might have been a small house has collapsed into a twenty-foot sinkhole of mud and standing water; the adjacent boardwalk sags into the pit.</p>")
  + "<p>The quarantine ended the city's otyugh-control; several burst up a drainage tunnel here. The mud bottom is difficult terrain; the slick slope takes "+chk("type:athletics|dc:14")+" to scale under pressure.</p>"
  + B.enc("Sewer otyughs", encx([B.mon_lvl("otyugh")] * 3, 8),
     "<p>3 "+B.mon("otyugh", "otyughs")+" wallow and lurch out at passersby (apply the Elite adjustment for a meaner fight). If the PCs haven't met "+act(A3["laori"], "Laori")+" yet, she bursts from B3 a round in, shrieking with delight, and joins the fight to earn goodwill.</p>",
     B.aside_token(["3× "+B.mon("otyugh", "Otyugh (4)"), act(A3["laori"], "Laori Vaus (10, ally)")])))

PG("Part 2 — The Emperor of Old Korvosa", SR("Part 2 — Emperor of Old Korvosa", 150)
  + B.s_milestone("<p><strong>Part 2.</strong> Pilts Swastel — failed impresario of the gore-playhouse <strong>Exemplary Execrables</strong> — has crowned himself Emperor of Old Korvosa. He rules Old Dock by spectacle: real-death 'plays,' the mob game <strong>blood pig</strong>, and an ornately carved guillotine (the 'tall knife') with a standing appetite. When volunteers run short, he invents traitors.</p>")
  + B.s_skill("<p><strong>Researching the Emperor:</strong> each attempt takes 1d4 hours and a Society check to gather and sift the island's strangled gossip (treat it as nearly impossible from off the island). Results are cumulative:</p>"
    "<ul>"
    "<li>"+chk("type:society|dc:19")+" — the Emperor rules Old Dock from a seized tenement 'palace' on <strong>Silk Street</strong> and rarely leaves it. His fanatics sweep Old Dock for conscripts; those who refuse are taken anyway — for other purposes.</li>"
    "<li>"+chk("type:society|dc:22")+" — Old Korvosa is his stage: prisoners are forced into deadly games and gruesome performances against his pets and followers, and the rest are beheaded by his favourite toy, an extravagant guillotine he calls the <strong>'Tall Knife.'</strong></li>"
    "<li>"+chk("type:society|dc:24")+" — an audience must be <em>earned</em> with entertainment. His current obsession is a brutal game of his own invention, <strong>blood pig</strong>, played on a converted rooftop field in the palace every evening; the howling of players and crowd carries across Old Dock.</li>"
    "<li>"+chk("type:society|dc:29")+" — the Emperor's real name: <strong>Pilts Swastel</strong>, pre-quarantine owner of the notorious Old Korvosa theater <em>Exemplary Execrables</em>.</li>"
    "</ul>")
  + B.s_conv("<p>His 'palace' is a block of converted tenements in central Old Dock. Salvator is there. So is the audience the PCs will need to play to — or fight through.</p>"))

# --- C. Pilts's Palace ---
PG("C. Pilts's Palace", SR("C — Pilts's Palace", 151)
  + B.s_milestone("<p><strong>C. Pilts's Palace</strong> — a block of six gutted tenements at <strong>11 Silk Street</strong>, central Old Dock, linked by rope bridges and rooftop fields, where the Emperor holds court from an hour past sunrise to dusk. The intended path is <strong>showmanship, not siege</strong>: petition the Emperor, accept the blood pig wager, win an audience with Salvator. Fighting the whole court at once is an Extreme-tier mistake — "+encx([10, 8, 6, 6, 6, 6], 8)+".</p>")
  + B.s_skill("<p><strong>Getting in:</strong> guards who spot unescorted PCs raise the alarm and demand their purpose. "+chk("type:diplomacy|dc:26")+" or "+chk("type:intimidation|dc:22")+" talks the thugs into escorting the party to the Emperor (a critical success and they don't insist on confiscating weapons first). Mob-escorted PCs enter at C1 and are marched up to the game-field (C4) before the throne, every thug alert. If it comes to blades: a guard battle can spread palace-wide with Pilts barking orders from his throne — but <strong>defeating the Emperor cows the entire mob</strong>; nobody needs to kill every thug, and Pilts can summon hundreds of replacements from Old Dock besides.</p>"))

area3("C1-C2", "Entrance & Guardroom", SR("C1-C2", 152)
  + box("The interior of this home has been gutted",
        "<p>The first home stands gutted around a mound of rubble; rickety stairs wind up to a splintered hole near the roofline, where a rope bridge sways 15 feet up.</p>")
  + box("What was once an attic has been",
        "<p>The attic beyond has been swept bare to the rafters — a wide open space under the roof. Rope bridges run out to the northeast and southwest, and a wooden stair drops away to the northwest.</p>")
  + "<p>The guardroom holds 4 "+act(A3["empthug"], "Emperor's Thugs")+" (−2 to their Perception — they're arguing about whether chokers have skeletons). The NE bridge runs level; the SW one climbs an extra 10 ft to the throne balcony as an unsettling 'rope stairway'; the NW stairs descend into rubble that blocks all entry from below.</p>"
  + B.enc("Guardroom", encx([6, 6, 6, 6], 8),
     "<p>4 "+act(A3["empthug"], "Emperor's Thugs")+" — posted only while the alarm is down.</p>",
     B.aside_token(["4× "+act(A3["empthug"], "Emperor's Thug (6)")])))

area3("C3", "The Emperor's Throne", SR("C3", 153)
  + box("This open-air balcony is shielded from rain",
        "<p>A canvas-roofed balcony overlooks the rooftop field 25 feet below. Upon it squats a throne of gilt scrap — a cheap mockery of the Crimson Throne — and, to its west, an ornately carved guillotine, its blade gleaming with use it has not yet been given today.</p>")
  + "<p>"+act(A3["pilts"], "Pilts Swastel")+" holds court here daily with "+act(A3["jabbyr"], "Jabbyr")+" (in executioner's costume at the "+haz(A3["tallknife"], "Tall Knife")+") and 4 "+act(A3["empthug"], "thugs")+", hearing mob reports, citizen pleas, and execution dockets.</p>"
  + SEC("<p><strong>Negotiating:</strong> Pilts happily confirms Salvator is his 'houseguest' but refuses every plea and threat — until boredom suggests <strong>the wager</strong> (see A Rousing Game). An <em>unnoticed</em> <em>suggestion</em>-style spell can move him; a noticed one means the Tall Knife. </p>")
  + B.enc("The full court (DON'T)", encx([10, 8, 6, 6, 6, 6], 8),
     "<p>"+act(A3["pilts"], "Pilts (10)")+" + "+act(A3["jabbyr"], "Jabbyr (8)")+" + 4 "+act(A3["empthug"], "thugs")+" + a mob of spectators — an Extreme bloodbath best avoided until the blood pig audience isolates Pilts (see the Development under Blood Pig).</p>",
     B.aside_token([act(A3["pilts"], "Pilts Swastel (10)"), act(A3["jabbyr"], "Jabbyr (8)"), "4× "+act(A3["empthug"], "Thug (6)"), haz(A3["tallknife"], "The Tall Knife (10)")])))

area3("C4-C5", "The Emperor's Stage & Rooftops", SR("C4-C5", 154)
  + box("The large, flat roof of this long building",
        "<p>The long building's flat roof has been made a game-field: two blood-outlined squares mid-field, pig-cages over roof-holes at either end, and gently sloped rooftops to the south fitted with scavenged arena seating.</p>")
  + "<p>The <strong>blood pig field</strong>: cages (C4a/C4e) over trapdoors; wolverine pits (C4b/C4f — one starving "+B.mon("wolverine", "wolverine")+" each); team squares (C4c — Shinglesnipes, C4d — visitors). The game's name rotates with its animal (blood dog, blood cat, and blood rat all had their runs); pig squeals please the Emperor most.</p>"
  + box("Two gently sloped rooftops overlook a flat",
        "<p>South of the field, two gently pitched rooftops have been turned into arena seating — boards, shingle-stacks, and improvised benches crowd the north-facing slopes, all of it visibly cannibalized from the decaying southern slopes behind.</p>")
  + "<p><strong>C5, the spectator rooftops</strong>, hold 4 patrolling "+act(A3["empthug"], "thugs")+" (a pair per roof) when no game runs — and dozens of howling lowlifes during one.</p>")

area3("C6", "Storeroom", SR("C6", 155)
  + box("Crates, boxes, and barrels fill this long storeroom",
        "<p>Crates, boxes, and barrels fill this long storeroom — fire-scarred props, tools, and salvage from Exemplary Execrables.</p>")
  + B.s_treasure("<p>"+chk("type:perception|dc:26")+" turns up a small jewelry box of worthless costume glass — and a real <strong>ring of chameleon power</strong> (quirk: activating or removing it turns all the wearer's hair a random unnatural colour; Pilts refused to wear it).</p>"))

area3("C7", "Choker Nest", SR("C7", 155)
  + box("This large room might once have been an attic",
        "<p>This large attic opens to the sky where its northwest corner has collapsed; the shadows between the rafters seem to shift and reach.</p>")
  + "<p>Six "+act(A3["chokerbrute"], "choker brutes")+" — Pilts's corpse-disposal partners since the theater days — nest here. The collapsed gap can be a stealth entry ("+chk("type:athletics|dc:24")+" to climb the 25-ft exterior), but within 5 feet of the broken floor a square crumbles: "+chk("type:reflex|dc:20")+" to lurch back or fall for @Damage[2d6[bludgeoning]] (and the noise).</p>"
  + B.enc("The nest", encx([2] * 6, 8),
     "<p>6 "+act(A3["chokerbrute"], "choker brutes")+" strike from the rafters — at the door from outside, or 3 rounds after southern intruders start moving. They fight to the death.</p>",
     B.aside_token(["6× "+act(A3["chokerbrute"], "Choker Brute (2)")]))
  + B.s_treasure("<p>"+chk("type:perception|dc:22")+" finds their bag wedged in the SE rafters: ~75 gp re-scaled in coin, a pearl-inset silk glove, a masterwork hand crossbow, and a <strong>wand of slow</strong> (13 charges).</p>"))

area3("C8-C10", "Stairway, Art Supplies & Trophy Hall", SR("C8-C10", 156)
  + "<p><strong>C8</strong> is a rubble-choked stairway — the only obstacle is the 1d4 hours it takes to clear a path to the abandoned floor below.</p>"
  + box("Several barrels and crates sit against the",
        "<p><strong>C9:</strong> barrels and crates line the walls, stacked with blank canvases and ceramic pigment-pots; against the eastern wall leans a sheet-draped stack of framed paintings.</p>")
  + B.s_skill("<p><strong>The new Screams:</strong> "+chk("type:society|dc:24")+" (or Art Lore) identifies the stacked paintings as brand-new work by Salvator Scream; <strong>beating the DC by 10</strong> reveals something more — they're muddled and pedestrian beside his pre-quarantine brilliance, the trademark <strong>blue pigment</strong> applied sloppy and thin.</p>")
  + SEC("<p><strong>Why (GM only):</strong> when Kazavon's spirit-fragment bonded with Queen Ileosa, it abandoned the artists it had been cultivating. <em>Salvator's muse is gone</em> — the same clue written across his cell's failures. If "+act(A3["laori"], "Laori")+" is along she gleefully riffles the whole stack, is crestfallen at how <em>ordinary</em> they are, and wants nothing more to do with them.</p>")
  + B.s_treasure("<p><strong>C9 treasure:</strong> 11 new Scream paintings — same beloved themes (shadowy dragons, torture, vivid despair), little of the old power — worth ~2 gp each re-scaled.</p>")
  + "<p><strong>C10</strong> is the trophy hall:</p>"
  + box("The air in this room smells sickly sweet",
        "<p>The air smells sickly sweet: fourteen brine-and-perfume-preserved heads — mostly human, two elven, one dwarven — gaze down from the walls. A child-sized bed sits in one corner; a fine-set dining table fills the middle.</p>")
  + SEC("<p>Pilts talks to the heads on sleepless nights; the small bed is Jabbyr's. The C11 door carries an <em>alarm</em> spell keyed to Pilts.</p>")
  + B.s_treasure("<p>The table is set with a full silverware service (~50 gp re-scaled) and a platinum-and-crystal brandy decanter (~75 gp).</p>"))

area3("C11", "The Emperor's Chambers", SR("C11", 157)
  + box("This extravagantly decorated bedroom would seem to belong",
        "<p>An extravagantly royal bedroom — until a second look picks out the worn theatrical props, gilt paint, and patched curtains of a stage-set monarchy.</p>")
  + "<p>Pilts sleeps and reads here after dark, and for an hour each night unbolts the C12 door to feed Salvator and collect finished paintings.</p>"
  + B.s_treasure("<p><strong>The three Scream originals</strong> (painted before his muse fell silent — and full of buried truth): a shadow-clad figure at a dolmen ("+chk("type:religion|dc:26")+": Zon-Kuthon entering ancient Nidal; ~45 gp); desert riders over skull-dunes ("+chk("type:religion|dc:29")+": a scene from the <em>Umbral Leaves</em>; ~110 gp); a man peeling away his own flesh to reveal <strong>blue scales</strong> ("+chk("type:survival|dc:29")+" places the horizon-castle as <strong>Scarwall</strong> in Belkzen; "+chk("type:arcana|dc:29")+" matches the scales to a blue dragon; ~200 gp). If "+act(A3["laori"], "Laori")+" is along she wants all three, settles for a split — and keeps offering to buy the PCs' share.</p>"))

area3("C12", "Salvator's Cell", SR("C12", 158)
  + box("The air in this room is an unpleasant mix",
        "<p>The air is an unpleasant mix of paint, sweat, and despair: a barred room of easels and half-finished horrors, its single occupant flinching at the sound of the bolt.</p>")
  + "<p>"+act(A3["salvator"], "Salvator Scream")+" paints here under lock, bar, and beating (the heavy bar lifts from the C11 side; "+chk("type:thievery|dc:20")+" picks the lock without Pilts's key). He begs rescue of any visitor who isn't the Emperor — but says <em>nothing</em> of Neolandus while Pilts lives. His price: <strong>the Emperor's death, and escort to the mainland</strong> ("+chk("type:diplomacy|dc:19")+" with a credible rescue promise; Intimidation or magic also work — "+act(A3["laori"], "Laori")+" cheerfully recommends both). Even then he won't finish the story until he's somewhere he <em>can't be overheard</em>.</p>"
  + SEC("<p><strong>Wards &amp; what becomes of him:</strong> every morning Pilts re-casts an <em>alarm</em> on this cell's door — a mental ping warns the Emperor the instant anyone but him opens it (on top of the warded C10 door). And mind the artist's nerve: below half HP he bolts for any small dark hole, and if he slips away on his own he eventually creeps home to 140 Wave Street — <strong>where the sinkhole otyughs (B5) eat him</strong>, unless the PCs already cleared them.</p>")
  + SEC("<p><strong>Laori's payoff.</strong> She has questions she'd rather ask Salvator privately: <em>where do the ideas come from?</em> Learning that his muse spoke in vivid dreams — and that the dreams have stopped — excites, then deflates her. She means him no harm (a living artist's muse might someday return), and she <strong>volunteers to escort Salvator to the mainland</strong> — a promise this priestess of the god of pain genuinely keeps. Errand done, she takes her leave to report to her superiors, enigmatically predicting the PCs haven't seen the last of her (true — Chapter 5), and slips into the lengthening shadows.</p>")
  + B.s_treasure("<p><strong>Story award:</strong> learning what Salvator knows — the Neolandus/Arkona revelation below — is worth a Moderate encounter's XP (PF1e 4,800).</p>")
  + B.s_conv("<p>His testimony is the chapter's hinge: <strong>Ileosa murdered the king; Neolandus knows; the Arkonas have him.</strong> On to Part 3 — and the rescue earns the trail to Arkona Palace.</p>"))

PG("A Rousing Game: BLOOD PIG!", SR("A Rousing Game / Blood Pig!", 158)
  + B.s_milestone("<p><strong>The wager.</strong> Pilts offers it when pleading stalls: beat his champion team — the eight-thug <strong>Shinglesnipes</strong> — at <strong>blood pig</strong>, and the PCs get five supervised minutes with Salvator (plus, if they surrendered their gear at the door, its return and safe escort from Old Dock). The rules were invented by a madman, are never written down, and change weekly — narrate Pilts declaiming them; confusion is part of the show.</p>")
  + "<p><strong>The rules (as declaimed this week):</strong> first team to <strong>5 points</strong>; a point = your team's pig into your team's pit. No weapons, no spellcasting (each violation = a point to the other team); unarmed Strikes are legal. Up to 8 a side, starting in the marked squares; a fresh "+B.cmon("Piglet", "pig")+" is craned into the cage opposite the scoring team's pit; a coin flip starts play.</p>"
  + "<ul>"
    "<li><strong>Picking up</strong> a pig (cage or loose): an Interact action that provokes reactions; a loose pig also needs a successful unarmed Strike vs AC 15 to corner.</li>"
    "<li><strong>Carrying</strong> a live pig: each round roll d6 on the <em>Squirming Pig</em> table — 1 slump (lose 1 action) · 2 squirm ("+chk("type:athletics|dc:20")+" or drop) · 3 squeal (the crowd roars) · 4 bite (pig attacks +6, 1 damage; if damaged, check to drop) · 5 kick ("+chk("type:acrobatics|dc:20")+" or drop) · 6 panic (all four at once). Taking damage while carrying: "+chk("type:athletics|dc:15")+" (+1 to the DC per point of damage taken) or drop. Thugs knock their pigs out first.</li>"
    "<li><strong>Loose pigs</strong> bolt 30 ft from the nearest creature each round (never off the roof or into a pit). <strong>Pass</strong> = Interact to an adjacent ally; <strong>throw</strong> = improvised −2 Strike, 10-ft increments; <strong>catch</strong> "+chk("type:athletics|dc:18")+"; <strong>intercept</strong> (reaction) "+chk("type:athletics|dc:24")+"; <strong>steal</strong> = a Disarm attempt, then the table.</li>"
    "<li><strong>Scoring:</strong> drop into an adjacent pit free, or throw at the 1-ft mouth (a Strike vs AC 15). The pits are 10 ft deep with a starving "+B.mon("wolverine", "wolverine")+" in each — <strong>killing a wolverine forfeits</strong> for the killer's team; it spends 1d3 rounds devouring each scored piglet, otherwise claws at anything within 5 ft of the mouth.</li>"
    "<li><strong>Betting:</strong> the thugs give 2-to-1 against the PCs, up to 100 gp per PC.</li>"
   "</ul>"
  + B.enc("BLOOD PIG — the Shinglesnipes", encx([6] * 8, 8),
     "<p>8 "+act(A3["empthug"], "Emperor's Thugs")+" (the Shinglesnipes) — but it's a <em>game</em>, not a battle: unarmed, pig-fixated, crowd-roared. Run it fast and absurd.</p>",
     B.aside_token(["8× "+act(A3["empthug"], "Shinglesnipe (6)"), "2× "+B.mon("wolverine", "Wolverine (2)") + " (in the pits)", B.cmon("Piglet", "Piglet (-1)") + " (the living ball)"]))
  + SEC("<p><strong>Development — the sore loser.</strong> On a PC win Pilts demands two-of-three and adds "+act(A3["jabbyr"], "Jabbyr")+" to the Shinglesnipes (player cap be damned); after a second loss he calls for three-of-five — and is told they're out of pigs. He nearly guillotines the messenger, then laughs, congratulates the PCs, and brings them up the balcony <em>with only Jabbyr and two thugs</em>. The supervised meeting (Salvator silent while Pilts lives) is the PCs' <strong>best shot at Pilts away from his mob</strong>: "+encx([10, 8, 6, 6], 9)+".</p>")
  + B.s_treasure("<p><strong>Payouts &amp; awards:</strong> the thugs honor their 2-to-1 bets — up to 200 gp profit per wagering PC per game. Winning two games and the audience with Salvator is itself worth a Severe encounter's XP (PF1e 9,600) <em>on top of</em> XP for any thugs bested during play.</p>"))

PG("Part 3 — Wrath of the Arkonas", SR("Part 3 — Wrath of the Arkonas", 162)
  + B.s_milestone("<p><strong>Part 3.</strong> Salvator's testimony points across Old Korvosa to <strong>Arkona Palace</strong>, where both Neolandus <em>and</em> Vencarlo sit in the dungeons below — insurance policies in a rakshasa's game.</p>")
  + SEC("<p><strong>The Arkona secret:</strong> generations ago, on a Vudra trade voyage, the human Arkonas were slaughtered and replaced by <strong>rakshasas</strong>. 'Glorio' is the rakshasa <strong>Bahor</strong>; his 'sister Meliya' is <strong>Vimanda</strong> (Verik's 'lover' from Chapter 1) — rivals locked in covert sibling war beneath a flawless family front. The palace crawls with lesser rakshasas and magically-thralled human 'relatives' who believe the family merely criminal.</p>"))

# --- D. Arkona Palace ---
PG("D. Arkona Palace", SR("D — Arkona Palace", 162)
  + B.s_milestone("<p><strong>D. Arkona Palace</strong> — the Vudrani-styled seat atop Endrin Isle, all topiary tigers, sandalwood censers, everburning torches, and 20-ft ceilings. Only 'family' lives inside. "+chk("type:religion|dc:30")+" identifies the door-carvings as <strong>Chamidu</strong>, Vudrani goddess of wild beasts.</p>")
  + SEC("<p><strong>Securing an audience:</strong> a believable request gets a six-guard escort to the entry, where the one-eyed majordomo <strong>Carnochan</strong> (a "+act(A3["marai"], "marai")+", telepathically bonded to Bahor) receives visitors; the PCs wait in the lounge (D2) under Bahor's scrying. Five minutes later 'Glorio' appears — concerned, charming, mind-reading. <strong>His deal:</strong> he wants Ileosa gone (Neolandus is his legal lever, for later) but can't look weak before Vimanda — so: <em>kill the Emperor of Old Korvosa</em>, and he'll help the PCs find their friends.</p>")
  + SEC("<p><strong>Bahor's Offer (after Pilts dies):</strong> a congratulation in the baths (D15), the gift of a <strong>ring of evasion</strong> (its deep-green bloodstone is his spy-eye), and the truth: both 'guests' are in the <strong>Vivified Labyrinth</strong> ("+chk("type:society|dc:25")+" recalls its rumors). He reveals the D4 elephant-passage, the passphrase <strong>'Chamidu is blind,'</strong> and the rotation levers — and secretly sends "+act(A3["vimanda"], "Vimanda")+" down to die at the PCs' hands (a <em>sending</em> scroll burned as they leave, the trap framed to her as an honour). <strong>Story award:</strong> learning the prisoners' location by negotiation, without violence, is worth a full Severe encounter's XP (PF1e 19,200).</p>")
  + SEC("<p><strong>Where are the prisoners?</strong> Vencarlo in E20, Neolandus in E21 — under a permanent <em>mage's private sanctum</em> (no scrying), kept unconscious (<em>sending</em> fails; <em>dream</em> reports only 'alive, sleeping').</p>")
  + B.s_conv("<p><strong>Infiltration logic:</strong> Bahor lets his house test intruders, intervening only at his chambers or treasury (then pitching the deal). On alarm: humans flee; Avishandu + Nudhaali hold the garden invisible; Carnochan + Vennashti sweep rooms in order; the marai fight human-shaped until one dies — then all revert and fight to the death. <strong>If the PCs retreat,</strong> nothing pursues: the rakshasas resume their human masks, give their dead to Avidexu in D24 — and a day later a scroll-borne <em>sending</em> reaches a PC:</p>")
  + box("Greetings. This is Glorio Arkona. I apologize",
        "<p>'Greetings — Glorio Arkona. Do forgive the misunderstanding with my rather unusual servants. I would speak with you privately, at the palace.'</p>")
  + SEC("<p><strong>The cover story:</strong> PCs who accept are received graciously; 'Glorio' explains away what they saw as <em>bound rakshasas</em> kept as bodyguards — a noble family's regrettable but necessary precaution — asks for their discretion, and tries to recruit them with the same kill-Pilts bargain. PCs who refuse the invitation leave him to his defenses: he withdraws to D18 and lets the palace repel intruders, attacking personally only if they grind through it room by room. (More rakshasas <em>could</em> be summoned from Vudra — but not within this chapter.)</p>"))

area3("D1-D3", "Entrance, Lounge & Chamidu", SR("D1-D3", 162)
  + box("A black marble arch depicting dozens of elephants",
        "<p>A black marble arch of marching elephants frames mahogany doors; above them, a bull-elephant's head watches with a single gleaming green eye.</p>")
  + "<p>A permanent <em>magic mouth</em> trumpets (and the elephant-head animates) for any visitor not wearing the Arkona crest. At night the front doors are secured with a good lock ("+chk("type:thievery|dc:30")+"). The fireplace-warmed lounge (D2) is the waiting room — and the watching room.</p>"
  + box("A fourteen-foot-tall marble statue of a six-armed",
        "<p><strong>D3:</strong> a fourteen-foot marble figure — a six-armed woman whose head bears four faces, one gazing down each compass point, weapons filling every hand — rises beneath a dome of coloured glass. A small kneeler waits at her feet, and each of her eight eyes is a bright green sparkling orb.</p>")
  + "<p>"+chk("type:religion|dc:30")+" names the exotic statue: <strong>Chamidu</strong>, Vudrani goddess of wild beasts.</p>"
  + B.s_treasure("<p><strong>The third-eye network:</strong> nine <em>third eye bloodstones</em> stud the palace (the elephant's eye ~100 gp; the statue's west-face eye, a fountain cobra, a hookah, the wax-corpse 'heart,' a javelin head, the treasury watch-stone, Bahor's paperweight, and the gifted ring) — every one a lens for "+act(A3["bahor"], "Bahor")+"; their faint divination auras are masked (<em>magic aura</em>).</p>"))

area3("D4", "The Garden", SR("D4", 163)
  + box("This chamber hardly seems to be part of",
        "<p>This chamber hardly seems part of a building at all: a living Vudrani jungle under a glass dome, loud with birds, threaded with fountains — and watched from a balcony twenty-five feet up.</p>")
  + "<p>Illusion-dressed windows keep the jungle seamless; "+chk("type:perception|dc:23")+" picks the real balcony from the painted walls. The door to the palace grounds is kept secured with a good lock ("+chk("type:thievery|dc:30")+"). The cobra-fountain holds two bloodstone 'eyes' (one a spy-stone); its plume is an officially-statted "+B.mon("living-waterfall", "living waterfall")+" that ignores intruders — unless they open the <strong>secret trap door</strong>.</p>"
  + SEC("<p><strong>The way down:</strong> "+chk("type:perception|dc:28")+" finds the circular platform under the elephant statue; a hidden pressure-plate rotates it open onto spiral stairs (10 minutes, then auto-close; a second switch 20 steps down reopens it). Without the passphrase <strong>'Chamidu is blind,'</strong> the statue — a "+B.cmon("Marble Elephant", "marble elephant guardian")+" (a 26,000-gp variant <em>figurine of wondrous power</em> that can also hold a <em>statue</em>-spell form indefinitely) — animates and attacks.</p>")
  + B.enc("Garden on alert", encx([B.cmon_lvl("Marble Elephant"), 5, 8, 8], 10),
     "<p>The "+B.cmon("Marble Elephant", "marble elephant")+" + the "+B.mon("living-waterfall", "living waterfall")+" + Avishandu and Nudhaali (2 "+act(A3["marai"], "marai")+", invisible in the howdah, re-casting every 5 minutes before abandoning post). Avishandu directs the elephant; Nudhaali rains <em>scorching rays</em>.</p>",
     B.aside_token([B.cmon("Marble Elephant", "Marble Elephant (7)"), B.mon("living-waterfall", "Living Waterfall (5)"), "2× "+act(A3["marai"], "Marai Rakshasa (8)")])))

area3("D5-D8", "Stores, Library & Smoking Den", SR("D5-D8", 165)
  + "<p><strong>D5</strong> holds garden tools, five huge water casks, and buckets by the dozen; the <strong>D6 storerooms</strong> (three of them) stack tools, firewood, and food among barrels and crates — fine hiding spots for sneaking PCs.</p>"
  + box("Two floor-to-ceiling bookshelves decorate the south and",
        "<p><strong>D7:</strong> two floor-to-ceiling bookshelves face a curved wall hung with half a dozen grotesque paintings — torture, murder, worse — while twin chandeliers light a floor strewn with reading cushions.</p>")
  + "<p>The library shelves poetry beside conjuration treatises in no order at all; many volumes are in <strong>Vudrani</strong>. The six wall paintings are <strong>Salvator Scream originals</strong> — among his most stomach-turning, the trademark blue everywhere — worth ~80 gp each re-scaled.</p>"
  + box("A long couch and two stuffed chairs sit",
        "<p><strong>D8:</strong> a long couch and stuffed chairs ring an elegant rug below walls carved with cloud-dancing air spirits. Exotic smoke perfumes the air around four jewelled hookahs, and beneath the stairs a glass case displays cigars, pottery jars, and bundles of dried leaves in a dozen colours.</p>")
  + B.s_treasure("<p><strong>D8 treasure:</strong> the four bejeweled hookahs run ~35 gp each (the one by the southwestern chair hides a 100-gp-grade <em>third eye</em> spy-stone in its pipe); the case holds <strong>10 pounds of exotic cigars, smoking-weed, and minor narcotics worth ~140 gp re-scaled</strong> — and is warded by the "+haz(A3["hungrysmoke"], "Hungry Smoke")+" trap (Bahor keeps the only key).</p>")
  + B.enc("Hungry Smoke springs", encx([8, 8], 10),
     "<p>2 "+act(A3["belker"], "belkers")+" from the 20-ft ceiling — reach down, can't easily be reached back.</p>",
     B.aside_token([haz(A3["hungrysmoke"], "Hungry Smoke (8)"), "2× "+act(A3["belker"], "Belker (8)")])))

area3("D9-D10", "Trophy Hall & Statuary", SR("D9-D10", 166)
  + box("Glass cases line this hallway's north and",
        "<p><strong>D9:</strong> glass cases run the hallway's north and south walls. The northern case hangs exotic blades around a suit of brilliant blue leather-and-ivory armor; the southern stages a gruesome tableau — a stuffed tiger feeding on an unsettlingly lifelike sculpture of a dead Vudrani man.</p>")
  + B.s_treasure("<p><strong>D9 treasure</strong> (cases locked, untrapped — "+chk("type:thievery|dc:26")+", expert): the wax corpse's exposed 'heart' ("+chk("type:society|dc:20")+" to appraise from afar) is a carved <em>third eye</em> bloodstone, ~50 gp re-scaled. North case: a <strong>+1 ghost touch kama</strong>, 12 masterwork daggers, a masterwork falchion, six punching daggers, two sais, two sianghams, two spears — and the armor, <strong>+1 resilient studded leather</strong> in blue leather and ivory.</p>")
  + box("A gracefully curving wall lined with tall",
        "<p><strong>D10:</strong> a graceful window-lined curve of wall commands the western grounds. The room stands empty but for three statues of Vudrani warriors, each brandishing a glittering blue-green javelin tipped with a carved bloodstone head.</p>")
  + SEC("<p><strong>The house alarm:</strong> each statue bears a <em>magic mouth</em> that erupts in insulting Vudrani oaths the moment any creature carries a drawn weapon into the room — instantly alerting the household (especially any marai resting in D14). Prying a javelin loose is easy, but triggers that statue's mouth all the same.</p>")
  + B.s_treasure("<p><strong>D10 treasure:</strong> the three bloodstone javelin heads are worth ~15 gp each re-scaled — and <strong>the central statue's is a <em>third eye</em> spy-stone</strong>, another lens for "+act(A3["bahor"], "Bahor")+".</p>"))

area3("D11-D13", "Banquet Hall, Balcony & Washroom", SR("D11-D13", 166)
  + box("A magnificent mahogany table dominates this room,",
        "<p><strong>D11:</strong> a magnificent mahogany table fills the hall, spread with an immense cover stitched from the bright skins of great snakes.</p>")
  + "<p>No servant ever enters during dinner ('a restrictive Vudrani custom' — and convenient, since now and then the family prefers to feed in true form behind locked doors, tidying up with <em>prestidigitation</em>). The grounds doors are locked ("+chk("type:thievery|dc:30")+") and <em>magic mouth</em>-alarmed like D1, though without bloodstones.</p>"
  + "<p><strong>D12</strong>, the upper balcony, overlooks the garden 25 feet below — warm air, birdsong, and fountain-babble drift up (and the D4 ambushers can target creatures here).</p>"
  + box("A large, ornate mirror hangs on the",
        "<p><strong>D13:</strong> an ornate mirror dominates the western wall of this washroom; the air is impossibly fresh, and the water-filled porcelain commode looks more comfortable than any commode has a right to.</p>")
  + B.s_treasure("<p><strong>D13 comedy treasure:</strong> the magical toilet — minor magics freshen the air and transmute waste to clean water piped down to the garden — is technically worth ~15 gp re-scaled… and weighs some 300 pounds. Hauling it out of a rakshasa palace is left as an exercise for the party.</p>"))

area3("D14", "Guard Quarters", SR("D14", 166)
  + box("The floor of this room is thickly carpeted",
        "<p>Thick carpets, low couches, the musk of great cats — and four figures who are no longer wearing their faces.</p>")
  + "<p>Off-duty, the four 'Arkona cousins' lounge in true form (often with abducted 'entertainment'; the quarantine has made them short-tempered). Bickering, they take −2 Perception to hear the house alarms. On alert they defer to <strong>Vennashti's</strong> tactics.</p>"
  + B.enc("The four marai", encx([8, 8, 8, 8], 10),
     "<p>Avishandu, Carnochan, Nudhaali, Vennashti — 4 "+act(A3["marai"], "marai rakshasas")+". A bruising brawl; worse if the alarm has scattered them into ambush pairs.</p>",
     B.aside_token(["4× "+act(A3["marai"], "Marai Rakshasa (8)")])))

area3("D16", "Leaves of Gold and Glitter (the Treasury)", SR("D16", 167)
  + box("The plain ebony walls of this chamber seem",
        "<p>Plain ebony walls frame a single luminous illusion: a vast golden tree in eternal dawn, leaves drifting like sparks.</p>")
  + SEC("<p><strong>The vault:</strong> an iron door dressed as ebony (Hardness 10, HP 60; "+chk("type:thievery|dc:40")+", master — a heightened <em>arcane-locked</em> lock; a silent mental <em>alarm</em> to Bahor; the walls, floor, and ceiling are sheathed in <em>walls of force</em>; a <em>forbiddance</em> bars planar tricks). "+chk("type:religion|dc:30")+" names the illusion the <strong>Tree of Eternal Dawn</strong>, whose leaves grant eternal life at a terrible cost. A persistent <em>screen</em> hides the room's real contents ("+chk("type:will|dc:23")+" on interaction): one iron chest ("+chk("type:thievery|dc:40")+"), a bloodstone watch-eye atop it.</p>")
  + B.s_treasure("<p><strong>The chest:</strong> the Arkonas' true wealth is <em>paper</em> — oaths of loyalty, debt, and servitude, including the entire <strong>Cerulean Society</strong> roster in Arkona pockets and Glorio's letter ordering Guildmaster Boule to lie low so the desperate city ripens ('…and Old Korvosa shall be the Society's'). Enough to politically destroy the family — after Ileosa. Plus: ~650 gp re-scaled in coin and gems, a <strong>+1 holy light crossbow</strong> (cherrywood and ivory — kept, beautifully, by the creature it could kill), the <strong>ring of evasion</strong> (if never gifted) — and <strong>Vencarlo's confiscated gear</strong>: his clothes, purse, <strong>+1 rapier</strong>, signet ring, and the brass key to the Blackjack lockbox (area A8).</p>"))

area3("D17-D18", "The Siblings' Rooms", SR("D17-D18", 169)
  + box("This austere chamber is apparently the sleeping",
        "<p><strong>D17:</strong> an austere sleeping chamber kept with unnerving precision — sheets drawn drum-tight, pillows squared, the dressing table and chair dust-free and polished to a gleam.</p>")
  + "<p><strong>Vimanda's room</strong> — austere to the point of insult. The 'loving' siblings privately despise each other; she has built her own underworld network to seize the family, plans curdled since the king's death, and lately lives in the dungeons venting on prisoners ("+act(A3["vimanda"], "see her entry")+").</p>"
  + box("The crowning glory of this dazzling chamber is,",
        "<p>The crowning glory of this dazzling chamber is its trophy wall: six mounted animal heads of species no naturalist could place, gazing down with disquieting attention.</p>")
  + SEC("<p><strong>D18, Bahor's room:</strong> the six 'Vudrani animal' heads ("+chk("type:nature|dc:28")+": <em>not</em> real animals; "+chk("type:arcana|dc:30")+": preserved <strong>rakshasa heads</strong> — his predecessors and disappointing children). During an infiltration "+act(A3["bahor"], "Bahor")+" waits here in human form, offering his deal one last time before the claws come out.</p>")
  + B.enc("BAHOR (if it comes to it)", encx([14], 10),
     "<p>"+act(A3["bahor"], "Bahor")+" alone is Extreme at L10 — with marai support, beyond it. The chapter neither expects nor requires his death; per the conclusion, he likely survives in damage-control (secret safe) or vendetta (secret out) mode.</p>",
     B.aside_token([act(A3["bahor"], "Bahor (14)")]))
  + B.s_treasure("<p>Exquisite furniture (~300 gp re-scaled, unwieldy), a 500-gp bloodstone paperweight (spy-stone), and a gold-filigreed Jawassan sitar (~35 gp).</p>"))

area3("D19-D25", "The Sea Caves", SR("D19-D25", 170)
  + box("The air in this vast grotto is cool.",
        "<p>The air in this vast grotto is cool, loud with unseen surf; a fungal garden glows along the ledge, and rope bridges sag away into the dark.</p>")
  + "<p>The natural sea-cave beneath the palace — the reason the Arkonas built here. The ledge spirals from the D4 stairs (100 ft above the water) down rope bridges (D20, the 'Cat's Cradle') past <strong>Avidexu's room</strong> (D21 — his animal carvings: a blue-coral gecko, a redwood cougar, a pearl-eyed gold flame drake, ~170 gp the set) to the pier.</p>"
  + SEC("<p><strong>The Innachi Naven hook:</strong> the four guardians below were once living janni slaves, murdered into fungal puppetry by the wizard <strong>Innachi Naven</strong> — a hireling who learned what the Arkonas really are and was handed to <strong>Senshiir</strong> (E21) as 'entertainment' for his trouble. Bahor tried and failed to craft more guardians himself; PCs who piece this together hold one more thread of the family's buried bodies.</p>")
  + B.enc("D19 — the Garden Guardians", encx([8, 8, 8, 8], 10),
     "<p>4 "+act(A3["gardenguard"], "Garden Guardians")+" — invisible, opening with overlapping spore-clouds on the narrow ledge. They never pursue into D24/D25 or the palace.</p>",
     B.aside_token(["4× "+act(A3["gardenguard"], "Garden Guardian (8)")]))
  + box("At the bottom of the vast cavern,",
        "<p><strong>D23:</strong> at the cavern's floor a wooden pier juts into a sloshing pool of blue seawater, a shallow-draft barge tied alongside with an unlit lantern at its bow. Timber-and-brick shoring to west and south betrays where the sea cave was artificially widened; from a twenty-five-foot waterway to the north drift the distant, muffled sounds of surf.</p>")
  + B.enc("D23 — the Arkona Pier (the escape scene)", encx([11], 10),
     "<p>The 15-ft-deep pool is home to the "+act(A3["enormreef"], "Enormous Reefclaw")+" (50% out hunting on the first visit; <strong>always home for the escape</strong> — run this as the chapter's last battle, Vencarlo and Neolandus huddled aboard the barge). The waterway winds ~120 ft northwest to a 'stone wall' that is an illusion ("+chk("type:will|dc:16")+" on interaction) masking the exit onto the Jeggare; the Arkonas use the cave to move sensitive cargo — most often unconscious abductees bound for the family table.</p>",
     B.aside_token([act(A3["enormreef"], "Enormous Reefclaw (11)")]))
  + box("Four lit braziers illuminate this vast chamber,",
        "<p><strong>D24:</strong> four burning braziers light a cathedral of polished tan marble, its dome arching sixty feet overhead, empty of bench or pew. Six alcove statues of a tiger-headed man line the walls; on a raised pulpit stand three more — the central figure twice life-size, holding out two lances flying the flag of Korvosa and the Arkona arms.</p>")
  + B.enc("D24 — the Arkona 'Temple'", encx([B.cmon_lvl("Avidexu"), 5, 5], 10),
     "<p>No god is worshiped here — every statue is <strong>Bahor as god-king of Korvosa</strong>, a monument to rakshasa ego. "+B.cmon("Avidexu", "Avidexu")+" (a true rakshasa, indifferent to politics, devoted to his pets) shares a fresh-shed snakeskin meal with two 18-ft "+B.mon("emperor-cobra", "emperor cobras")+", which he feeds on animals and vagrants. D22 hides the dungeon door ("+chk("type:perception|dc:25")+"; a tunnel winds 100 ft southeast to E1); D25 is the second tunnel to E1.</p>",
     B.aside_token([B.cmon("Avidexu", "Avidexu (10)"), "2× "+B.mon("emperor-cobra", "Emperor Cobra (5)")])))

# --- E. The Vivified Labyrinth ---
PG("E. The Vivified Labyrinth", SR("E — The Vivified Labyrinth", 176)
  + B.s_milestone("<p><strong>E. The Vivified Labyrinth</strong> — the Arkonas' rotating dungeon-engine, built for their own entertainment: testing recruits, punishing prisoners. (Bahor's favourite game: a prisoner, a knife, a loincloth, a slow venom — and the promise of a curing pool somewhere deep inside. No one has ever won.) Four great central sections <strong>turn 90°</strong> when any rotation lever is pulled (E3, E8, E14, E16, E17 — the E14 lever is hidden), reshuffling every route. Below, in the Gizzard (E23), four chained skeletal mastodons walk the gears. Rooms are unlit, ceilings 10 ft unless noted. The party should be <strong>L10</strong> entering.</p>")
  + B.s_skill("<p><strong>The rotation has teeth.</strong> A pulled lever <strong>locks for 1 minute</strong> ("+chk("type:thievery|dc:30")+", taking a full round at the mechanism, overrides the lockout for one extra pull). All four sections turn together over 1 round per 90°, bells ringing in the Gizzard and the grinding plainly audible through E1-E20 — and the openings between sections slam shut <em>fast</em>:</p>"
    "<ul>"
    "<li><strong>Caught astride a seam</strong> (a transitional square): "+chk("type:reflex|dc:23")+" — on a success the creature flings itself 5 ft to either side, clear of the seam; on a failure the closing walls <strong>scissor it for @Damage[6d10[bludgeoning]]</strong> and shunt it into a random adjacent non-transitional square.</li>"
    "<li><strong>Riding a turning section:</strong> "+chk("type:acrobatics|dc:20")+" to keep footing or fall "+B.cond("prone", "Prone")+".</li>"
    "<li>"+chk("type:perception|dc:23")+" at any seam reveals the tell-tale floor-and-ceiling gaps before the first pull.</li>"
    "</ul>"
    "<p>The dungeon has <strong>four orientations</strong>; only the mapped first allows entry from E2 without teleportation. Sivit knows all four layouts and pulls levers to split parties.</p>")
  + B.s_conv("<p><strong>Running the revolving dungeon:</strong> roll initiative when the PCs trigger the first rotation at E3 — and roll for "+act(A3["sivit"], "Sivit")+" and "+act(A3["vimanda"], "Vimanda")+" too, tracking their movements secretly on their turns. Sketch the four mobile sections on four separate paper circles so each can physically rotate 90° at the table. If the PCs strand themselves away from every lever, have an NPC elsewhere pull one to keep the game afoot. <strong>Sanctioned static fallback:</strong> if rotation would only frustrate your group, throw it out entirely — connect <strong>E3-E4</strong>, <strong>E14-E15</strong>, and <strong>E17-E18</strong> with tunnels and run the place as a fixed dungeon.</p>")
  + SEC("<p><strong>The two roamers:</strong> "+act(A3["vimanda"], "Vimanda")+" — disguised as a starved, grateful <strong>Vencarlo</strong> ('Bahor sent you to die; come, we must face him!') — patrols clockwise from E13, tracking Bahor's gifted ring by <em>locate object</em>, immune to the symbol glyphs, terrified of Sivit. "+act(A3["sivit"], "Sivit")+" scries the lever rooms, herds prey across her glyphs, and cannot leave. <strong>Tell Sivit of Vimanda's treachery and the binding does the rest.</strong> If the PCs still carry the Chapter-1 raktavarna 'silver dagger,' it has been Vimanda's informant all along — and bites its owner when she calls it home.</p>"))

area3("E1-E4", "Entrance, Statues, First Lever & the Poisoned Pool", SR("E1-E4", 176)
  + "<p><strong>E1:</strong> silent bronze tiger-doors; an illusory wall ("+chk("type:will|dc:25")+" on interaction) hides the eastern passage. <strong>E2:</strong> two statues of a tiger-headed man — Bahor again ("+chk("type:perception|dc:23")+" spots the rotation seam beyond). <strong>E3:</strong> the first ebony rotation lever. <strong>E4:</strong> a crystal pool — the "+B.cmon("Corrupted Pool", "Corrupted Pool", kind="hazard")+" — whose water is a <em>poison</em> effect ("+chk("type:fortitude|dc:25")+"; @Damage[6d6[poison]]; the magic is aura-masked, and water removed from it turns ordinary — Vimanda loves a well-timed <em>suggestion</em> here).</p>")

area3("E5-E8", "Pools, Pain & the Second Lever", SR("E5-E8", 177)
  + "<p><strong>E5:</strong> a <em>murky</em> pool that is actually a once-per-day <em>heal</em> (both roamers retreat here when hurt; liquid carried off reverts to foul water) — guarded by the "+haz(A3["symfear"], "Symbol of Fear")+". <strong>E6:</strong> a bare room whose floor bears the "+haz(A3["sympain"], "Symbol of Pain")+".</p>"
  + box("Three large wooden chests, their lids decorated",
        "<p><strong>E7:</strong> three big wooden chests, lids carved with cavorting tigers, stand against one wall — a short phrase incised on each. The facing wall's fresco marches hundreds of tigers in widening rings around a fist-sized green gem, set into the stone and cut as a tiger's head.</p>")
  + B.s_skill("<p><strong>The language gate:</strong> the lid inscriptions are carved <strong>in Vudrani</strong> — only readers of that tongue (or <em>comprehend languages</em> etc.) get Bahor's 'hints,' and since the hints mislead, speaking his native language is more curse than gift here. Left: <em>'By gentle caress shall truth be known.'</em> Right: <em>'Breathe deep your salvation.'</em> Middle: <em>'Life within but Death without.'</em></p>")
  + "<p>Left is the "+haz(A3["terinavchest"], "terinav-painted decoy")+" (empty); right is the "+haz(A3["insanitychest"], "insanity-mist bellows")+"; the middle holds 3 healing potions + 3 lesser restoration potions <em>and</em> an underfed, furious "+B.cmon("Blood Cobra", "blood cobra")+" that strikes the first face it sees. The fresco's gem is a 75-gp-grade <em>third eye</em> bloodstone (re-scaled). <strong>E8:</strong> the second lever (Sivit scries this room after the first rotation).</p>")

area3("E9-E12", "Mapras's Obstacle Course", SR("E9-E12", 178)
  + "<p>Four rooms built by Bahor's father (Bahor killed him; the rooms were too ingeniously cruel to demolish). Each has a hidden bypass switch ("+chk("type:perception|dc:30")+"; suppresses 3 rounds, re-pressable):</p>"
  + "<p>"+haz(A3["bitingtigers"], "The Biting Tigers (E9)")+" — snapping mounted heads on serpentine necks, four Strikes a round, watched by an invisible <em>arcane eye</em>; a secret door ("+chk("type:perception|dc:30")+") hides E10.</p>"
  + box("A ten-foot-wide, two-foot-tall well rises from the",
        "<p><strong>E10:</strong> a squat, ten-foot-wide well of inky water fills the round room's center, and from it rears a stone serpent — dozens of carved arms crossed over its belly, each fist gripping a long curved blade — its head rising ten feet to regard the door with amethyst eyes.</p>")
  + "<p>"+haz(A3["fangsdiom"], "The Fangs of Diomazul (E10)")+" — the 'well' is four inches of dark water over a blade-carousel; "+chk("type:religion|dc:30")+" names the statue <strong>Diomazul</strong>, Serpent of Eighty Blades, an obscure Vudrani god of battle-fury and cruelty. The amethyst eyes pry out at ~50 gp each (a full round apiece).</p>"
  + box("Eight alcoves line this long, narrow hallway.",
        "<p><strong>E11:</strong> eight alcoves flank the long narrow hall, an upright iron casket in each — a sobbing woman worked into every lid — above a floor of tiny red stones that gleams like a corridor awash in blood.</p>")
  + "<p>"+haz(A3["wailingmaidens"], "The Wailing Maidens (E11)")+" — tilting floors dump victims into the kill-lane, the western maidens wail, the eastern fire spikes. "+haz(A3["stingingwasps"], "The Stinging Wasps (E12)")+" — the wasp-swarm mosaic room, where thousands of six-inch needles stab in rippling waves.</p>")

area3("E13-E17", "The Maze's Heart", SR("E13-E17", 180)
  + "<p><strong>E13, Meditation Chamber:</strong> a humming black-marble <strong>sonorous stone</strong> ("+chk("type:occultism|dc:28")+" while reading auras): a minute within 5 feet grants <em>calm emotions</em>; touching it casts <em>restoration</em> AND restores up to 3 expended spell slots — four uses a month (it dies if removed). Vimanda's patrol starts here. <strong>E14:</strong> a bone-strewn room hiding a lever behind a secret door ("+chk("type:perception|dc:30")+"). <strong>E15:</strong> murals that paint the viewer among the prey — pure dread. <strong>E17:</strong> Sivit's body-dump (the Arkonas carry the remains to table).</p>"
  + box("Four alcoves in the walls of this",
        "<p><strong>E16:</strong> four wall alcoves each hold a sphere of mist hovering three feet off the floor — a foot across, one each of black, white, green, and gold. Just north of the spheres, two levers jut from opposite walls.</p>")
  + SEC("<p><strong>E16, Transport Room:</strong> the mist-spheres teleport a toucher (thrown objects too) — white→E2, black→E13, green→E20, gold→E5 — <em>if</em> the western lever is up. It starts <strong>down</strong>: every sphere instead dumps the toucher into a random unoccupied locked cell in E21 (a good lock — "+chk("type:thievery|dc:30")+" to pick from within; no cells free → the spheres simply go dead). Superb mobility for those who know the pattern; a one-way oubliette for those who don't. The eastern lever is another rotation pull.</p>"))

area3("E18-E19", "The Throne Approaches", SR("E18-E19", 181)
  + "<p>The two rooms that rotate open onto Sivit's chamber: the Hall of Slumber with its "+haz(A3["symsleep"], "Symbol of Sleep")+", and the crooked Hall of Stunning with the "+haz(A3["symstun"], "Symbol of Stunning")+". She times her entrances for the glyphs' harvest.</p>")

area3("E20", "Sivit's Throne — the Vencarlo Rescue", SR("E20", 182)
  + box("A great green throne sits atop a dais in the",
        "<p>A great green throne rises on a dais between two chained statues of the tiger-headed man; the marble around them is dark with old blood.</p>")
  + "<p>"+act(A3["sivit"], "Sivit")+" keeps her playthings shackled to the statues (the dead go to E17). <strong>"+act(A3["vencarlo"], "Vencarlo Orisini")+" hangs from the western one — at 0 HP</strong>, starved, in rags, waking the moment anyone heals him. Battered as he is, his face lights up: <em>'It's quite the delight to see you.'</em> He points out the manacle key under the throne cushion ("+chk("type:perception|dc:26")+"; "+chk("type:thievery|dc:30")+" without it). Healed, he insists on helping — <em>Neolandus first</em> — and, having spent time in the torture chamber, can show the PCs the illusory walls hiding the lower level.</p>"
  + SEC("<p><strong>The Blackjack confrontation:</strong> challenged about his other identity, Vencarlo laughs it off as a fine joke. Presented with proof (he <em>was</em> caught dressed as Blackjack), he goes quiet, then concedes — <em>'Looks like you caught me. Well done.'</em> — and immediately defers the whole conversation: no time now; rescue Neolandus, get out of Korvosa, and there will be plenty of time to talk it over later. He keeps that promise.</p>")
  + B.s_treasure("<p><strong>Story award:</strong> rescuing Vencarlo is worth a Severe encounter's XP (PF1e 9,600).</p>")
  + B.enc("BOSS — Sivit, Lady of the Labyrinth", encx([10], 10),
     "<p>"+act(A3["sivit"], "Sivit")+" — scry, rotate, herd, pounce. She wand-doors back here when bloodied and fights to the death inside her prison. <strong>Story award</strong> for Vencarlo's rescue.</p>",
     B.aside_token([act(A3["sivit"], "Sivit (10)"), act(A3["vencarlo"], "Vencarlo (0 HP)")])))

area3("E21-E22", "The Torture Chamber — the Neolandus Rescue", SR("E21", 184)
  + box_stitch("This large room is lit by a heartily", "hooks in the", "ceiling, while racks, strappados, gibbets",
        "<p>A firepit burns merrily at the room's center; caged silhouettes sway on chains hooked to the ceiling, and racks, strappados, gibbets, and subtler instruments crowd the floor between them. Immense wooden doors fill the north wall; along the south waits a row of narrow, very clean cells.</p>")
  + "<p>"+act(A3["senshiir"], "Senshiir")+", the four-armed asura who tortures for the Arkonas by contract, has just strapped a sobbing man to the rack — <strong>"+act(A3["neolandus"], "Neolandus Kalepopolis")+"</strong> ("+chk("type:society|dc:15")+" to recognize him; he claims to be 'Velak' otherwise, and begs the PCs to rescue 'a friend' before they leave). The E16 teleporters dump victims into the southern cells (good locks — "+chk("type:thievery|dc:30")+"). E22 is the dead torturer's old room, where Senshiir sometimes meditates.</p>"
  + B.enc("Senshiir (+ Vimanda, if unalerted)", encx([9, 12], 10),
     "<p>"+act(A3["senshiir"], "Senshiir")+" alone is a light fight — but if the PCs reached here without alarms or Bahor's deal, "+act(A3["vimanda"], "Vimanda")+" is here trading torture-craft with her, and the room is <strong>Moderate-to-Severe</strong>.</p>",
     B.aside_token([act(A3["senshiir"], "Senshiir (9)"), act(A3["vimanda"], "Vimanda (12, perhaps)")]))
  + B.s_treasure("<p><strong>Story award:</strong> rescuing Neolandus from the rack is worth a Moderate-to-Severe encounter's XP (PF1e 6,400).</p>")
  + B.s_conv("<p>Once Neolandus is sure the PCs aren't the queen's agents, he grows excited — these are exactly the heroes he's been hoping for — and shares everything; see the Conclusion.</p>"))

area3("E23", "The Gizzard", SR("E23", 186)
  + box("This vast cavern stretches into the shadows, the true",
        "<p>This vast cavern stretches into shadow: four stone pillars rise as axles into forty-foot wooden gear-disks overhead, and about each pillar stands a chained colossus of yellowed bone.</p>")
  + "<p>The Labyrinth's engine. Bells ring, gears unlock, and the four "+act(A3["rajambari"], "rajambari")+" walk their quarter-circles. The timber tangle above 10 feet takes "+chk("type:acrobatics|dc:10")+" or "+chk("type:athletics|dc:10")+" to thread.</p>"
  + B.enc("The rajambari (if provoked)", encx([8, 8, 8, 8], 10),
     "<p>Passive unless they or the works are damaged — then all four defend the machine to destruction. <strong>Destroying two or more locks the Labyrinth's configuration permanently</strong> (which may be exactly what the PCs want).</p>",
     B.aside_token(["4× "+act(A3["rajambari"], "Rajambari (8)")])))

PG("Chapter Conclusion", SR("Chapter Conclusion", 188)
  + B.s_milestone("<p><strong>Chapter Conclusion.</strong> With Vencarlo and Neolandus free, the campaign pivots: politics can no longer stop Ileosa, and both men must flee Korvosa. <strong>The escape:</strong> the barge at the Arkona pier (D23 — past the "+act(A3["enormreef"], "Enormous Reefclaw")+", home this time), out the illusory wall, up the coast by darkness, then inland to <strong>Harse</strong> — where Vencarlo's friends already shelter Trinia. The PCs should be on the cusp of <strong>L11</strong>.</p>")
  + SEC("<p><strong>Neolandus's revelation:</strong> Ileosa is host to the spirit-fragment of <strong>Kazavon</strong>, a long-dead draconic warlord — and while she wears the <strong>Crown of Fangs</strong> she cannot be killed (Endrin's failed shot proved it to the whole city). The lore to defeat the evil beneath Castle Korvosa — and perhaps save the queen — survives only among the <strong>Shoanti of the Cinderlands</strong>, who do not love Korvosans. Winning them is Chapter 4.</p>")
  + SEC("<p><strong>Ileosa's escalation</strong> (while the PCs are away): crushing taxes, slavery, martial law, ever-stranger edicts; the Gray Maidens grow openly brutal; Cressida walks the rebel/loyalist knife-edge and quietly protects the PCs' people. Opposing the queen head-on now means a deathless bard backed by devils, blades — and soon a dragon.</p>")
  + B.s_conv("<p><strong>Arkona ramifications:</strong> the AP assumes the family exits play, but <strong>Bahor likely survives</strong>. Secret safe → damage control: he abandons the prisoners and offers non-interference. Secret exposed → assassins follow the PCs, and Bahor weighs fleeing to Vudra for reinforcements. <strong>Vimanda</strong>, if allied, is a gloriously untrustworthy asset. The D16 papers can destroy the family politically — after the queen falls. Epidemic Clock: the city sickens unattended while the PCs ride north (+1 per away-stretch, per the Blood Veil overlay).</p>"))

journal = B.journal_entry(JID3, "3. Escape from Old Korvosa", pages, folder=ADV_FOLDER)
B.write("journals", "03-escape-from-old-korvosa", copy.deepcopy(journal), embed_pages=True)

print(f"Chapter 3 built: {len(folders)} folders, {len(actors)} actors, 1 journal ({len(pages)} pages).")
