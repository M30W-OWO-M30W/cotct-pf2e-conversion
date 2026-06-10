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

MODID = "cotct-pf2e-conversion"
ACTOR_ROOT, ITEM_ROOT, ADV_FOLDER = "cotctActorRoot01", "cotctItemRoot001", "cotctAdvFolder01"

# ---- stable literal ids (16 chars) ----
JID3 = "ch3EscapeOldKor1"
A3 = {"empthug": "emperorsThug0001", "redmantis": "redMantisAssn001", "housefire": "spreadingFire001",
      "laori": "laoriVaus0000001", "pilts": "piltsSwastel0001", "jabbyr": "jabbyrGnome00001",
      "chokerbrute": "chokerBrute00001", "salvator": "salvatorScream01", "tallknife": "tallKnifeGuillo1"}
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
    return B.s_read("<p>" + t + "</p>") if t else B.s_read(fallback_html)
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
   B.gear("studded-leather", nid()), B.gear("steel-shield", nid())],
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
   B.lore(nid(), "Assassin Lore", 17),
   B.gear("leather-armor", nid()), B.gear("sawtooth-saber", nid(), 2), B.gear("dagger", nid(), 4),
   B.equipment(nid(), "Alchemist's Fire (x2) & Fire-Ward Potions", 5, 10, "<p>2 vials of alchemist's fire (her ambush-arson tools) and pre-quaffed potions of fire resistance (resistance 10 for the ambush) — see her tactics.</p>", traits=["alchemical", "consumable"])],
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
   B.lore(nid(), "Zon-Kuthon Lore", 21),
   B.gear("chain-mail", nid())],
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
   B.lore(nid(), "Theater Lore", 18),
   B.gear("leather-armor", nid())],
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
        "<p><strong>What he knows</strong> (price: the Emperor's death + escort to the mainland; "+chk("type:diplomacy|dc:10")+" with a rescue promise, or Intimidation/magic): Vencarlo questioned him about <strong>Neolandus</strong>; the seneschal arrived at his door bloodied and poisoned the morning the king died, revealed that <strong>Ileosa murdered Eodred II</strong> in league with the Red Mantis, said the queen had 'changed — grown worse'… and that Salvator gave Neolandus to the <strong>Arkonas</strong> for safekeeping. He says <em>nothing</em> while Pilts lives.</p>",
  folder=F3["a_creatures"], blurb="Kazavon-touched painter; the key witness", token_src=None, actor_link=True))

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

# =====================================================================
# JOURNAL — "3. Escape from Old Korvosa"
# =====================================================================
SR = lambda area, p: f'<p class="source"><em>Source: CotCT (2016 HC), Ch.3, {area} — p.{p}.</em></p>'
pages = []
def PG(name, html, level=2): pages.append(B.page(nid(), name, html, level=level))
def area3(code, name, html): PG(f"{code}. {name}", html, level=3)
def encx(levels, pl):
    e = B.encounter(levels, party_level=pl); return f"{e['band']} · {e['xp']} XP @ L{pl}"

PG("Chapter Background",
  B.s_milestone("<p><strong>Chapter 3 — Escape from Old Korvosa.</strong> The queen's madness blossoms as Kazavon's fragment quickens within her. Quarantined Old Korvosa rots under mob rule — and somewhere in it hides the city's salvation: the missing seneschal, <strong>Neolandus Kalepopolis</strong>, the one man who can legally depose a corrupt monarch. PCs begin at <strong>8th level</strong> → 9th after the Emperor of Old Korvosa → 10th before the Vivified Labyrinth → nearly 11th by chapter's end.</p>")
  + SEC("<p><strong>Kazavon's whispers (GM only).</strong> For centuries the fangs whispered to sensitive souls, breeding madmen instead of servants. When Ileosa freed the dragon's spirit-fragment, its seven current 'projects' lost their muse — six killed themselves; the seventh is the painter <strong>Salvator Scream</strong>, Pilts Swastel's gore-artist at Exemplary Execrables.</p>")
  + SEC("<p><strong>The Neolandus chain (the chapter's spine):</strong> the wounded seneschal fled the Red Mantis to his secret friend Salvator → Salvator hid him with the Arkonas (patron 'Glorio Arkona' — actually the rakshasa <strong>Bahor</strong>) → the Arkonas now cage Neolandus as an insurance policy against the queen. <strong>Vencarlo</strong>, investigating, was ambushed by the Red Mantis (they suspect he is Blackjack), survived, tried to infiltrate Arkona Palace — and is now a prisoner alongside the man he sought. The trail the PCs must follow: Vencarlo's home → Salvator → Pilts → the Arkonas.</p>"))

PG("The Crown Revealed",
  "<p>As the plague breaks, Queen Ileosa — wearing a new crown set with curved fangs — calls a surprise public address. Flanked by Sabina Merrin, the bloatmage seneschal <strong>Togomor</strong>, Cressida Kroft, and Sable Company commandant <strong>Marcus Endrin</strong>, she declares victory over blood veil (deftly spinning Davaulus's fate), names the <strong>Gray Maidens</strong> Korvosa's official protectors with Sabina as general — and <strong>disbands the Sable Company</strong>, seizing its holdings and demanding Endrin surrender his badge.</p>"
  + SEC("<p><strong>The assassination attempt.</strong> Endrin instead puts an arrow into the queen — a perfect, fatal shot. <strong>Ileosa does not die.</strong> The Crown of Fangs knits the wound before the crowd's eyes; she laughs, and the Gray Maidens drag Endrin away (he lives, imprisoned in the Longacre Building — rescuable in Chapter 4). The city reels: their queen cannot be killed. <strong>Time this</strong> just after Davaulus falls, while the PCs are mopping up the temple — they should hear of it secondhand.</p>")
  + B.s_conv("<p>This is the campaign's mid-point reveal: Ileosa is now visibly superhuman, the Gray Maidens are the law, and open opposition is suicide. The <em>Crown of Fangs</em> artifact debuts here; the queen retreats from public view until Chapter 6's endgame begins to turn.</p>"))

PG("Whispers from Old Korvosa (Cressida's Mission)",
  "<p>Soon after, a haggard Cressida summons the PCs to a nearly deserted Citadel Volshyenek and, behind a <em>mage's private sanctum</em>, lays it out: Korvosa is being murdered by its queen, and only the PCs can act.</p>"
  + box("Korvosa is dying. No, strike that.",
        "<p>'Korvosa is dying. No — Korvosa is being <em>murdered</em>. Killed by our queen… Vencarlo wrote of discovering something of vital importance regarding the queen — dark magic, a pact with a devil — and he hinted he'd found a lead on Seneschal Kalepopolis. Then his messages stopped. Find Vencarlo in Old Korvosa. Learn what he knows. And if the seneschal lives — bring him home.'</p>")
  + B.s_skill("<p><strong>The mission:</strong> infiltrate quarantined Old Korvosa, find Vencarlo (start at his home by the Orisini Academy), and trace Neolandus. Cressida warns of the new 'Emperor of Old Korvosa' holding the streets. Ironically the island is the <em>safest</em> place for queen-hunted PCs — if they keep a low profile and avoid Gray Maidens.</p>")
  + B.s_treasure("<p><strong>Cressida's cache</strong> (the citadel's last reserves): 4 potions of <em>cure serious wounds</em> (moderate healing potions), 3 potions of <em>lesser restoration</em>, a <strong>wand of invisibility</strong> (10 charges), and a <strong>wand of cure moderate wounds</strong> (30 charges).</p>"))

PG("Old Korvosa Today",
  "<p>Endrin Isle is sealed: the Gray Maidens burned every wooden bridge, walled the stone Jeggare Bridge with a 15-ft <em>wall of stone</em> barricade, and patrol the Narrows in swift barges. <strong>Anyone may enter; no one may leave</strong> — escapees are warned once, then fired upon.</p>"
  + "<p><strong>The four wards:</strong> <em>Fort Korvosa</em> (highest, most orderly — the Arkonas' redoubt) · <em>Garrison Hill</em> (burned, scavenger-haunted) · <em>Bridgefront</em> (worst-off, morale shattered) · <em>Old Dock</em> (the most dangerous — the Emperor's domain).</p>"
  + B.s_skill("<p><strong>Getting in/out:</strong> flight or teleportation trivializes it; otherwise a night swim or skiff across the northern Jeggare ("+chk("type:athletics|dc:15")+" to swim quietly; "+chk("type:stealth|dc:18")+" to evade the barge patrols), returning via the dark, half-burned far side of the Narrows. Don't over-police it — any half-decent plan works.</p>")
  + SEC("<p><strong>The mob.</strong> Unless the PCs stay unobtrusive, each hour carries a 10% chance (50% per 10 minutes in Old Dock) that mob soldiers notice them — four "+act(A3["empthug"], "Emperor's Thugs")+" demand to know their business in 'the emperor's domain.' Color encounters: Tesh Zobberdin (a doomed avenger marching on Old Dock), Olmere Bliversin (a giggling balcony ranter).</p>")
  + B.enc("Pilts's Mob (recurring)", encx([5, 5, 5, 5], 8),
     "<p>4 "+act(A3["empthug"], "Emperor's Thugs")+" — the standard mob shakedown. They scatter once half fall. Repeatable; escalate to 8 thugs ("+encx([5]*8, 8)+") if the PCs make a spectacle.</p>",
     B.aside_token(["4× "+act(A3["empthug"], "Emperor's Thug (5)")])))

area3("A", "Vencarlo's Home", SR("A — Vencarlo's Home", 141)
  + "<p>A humble house in southern Fort Korvosa, beside the charred ruin of the <strong>Orisini Academy</strong> (burned by the Red Mantis after Vencarlo escaped their ambush). The door is unlocked; the rooms are warm, quiet, unlit — and both fireplaces are burning in an 'empty' house.</p>"
  + B.s_skill("<p><strong>Reading the scene:</strong> "+chk("type:perception|dc:20")+" (in A7/A8; +10 with scent) catches a strange-tanged smoke; "+chk("type:crafting|dc:15")+" identifies <strong>residual alchemist's fire</strong>, and "+chk("type:perception|dc:25")+" finds it faintly staining walls, floor, and furniture. "+chk("type:survival|dc:20")+": no real traffic since Vencarlo's last letter; "+chk("type:survival|dc:30")+": faint marks of a <em>very</em> stealthy recent visitor.</p>")
  + "<p><strong>The rooms (A1–A8):</strong> a Vudrani-rug entry · a blade-repair workshop · bath · a study of fencing and philosophy texts (the academy's books show business dying after the king's death) · pantry · the living room (lit hearth, hiding-nook under the stairs) · the double-height training room (lit hearth, open rafters) · Vencarlo's unslept-in bedroom.</p>"
  + SEC("<p><strong>The ambush.</strong> Two "+act(A3["redmantis"], "Red Mantis assassins")+" squat here in 8-hour shifts (relieved from the guild's hideout below the Longacre Building — a Chapter 4 thread), waiting for Vencarlo. One hides under the A6 stairs, one in the A7 rafters. They pre-buff the moment anyone enters and spring when a PC climbs to A7 — opening by igniting <strong>both fireplaces</strong> into the "+haz(A3["housefire"], "Spreading House Fire")+".</p>")
  + B.enc("Red Mantis ambush", encx([9, 9], 8),
     "<p>2 "+act(A3["redmantis"], "Red Mantis assassins")+" + the "+haz(A3["housefire"], "fire")+" they are warded against. A telegraphed Severe: the fire punishes slow play, and the assassins use it as terrain.</p>",
     B.aside_token(["2× "+act(A3["redmantis"], "Red Mantis Assassin (9)"), haz(A3["housefire"], "Spreading House Fire (8)")]))
  + B.s_treasure("<p><strong>The Blackjack cache.</strong> "+chk("type:perception|dc:30")+" in the A8 closet reveals a hidden panel; the iron lockbox within ("+chk("type:thievery|dc:40")+", or Hardness 10 / 40 HP — the key is with Vencarlo's confiscated gear in the Arkona vaults, D16) holds a <strong>bag of holding (type I)</strong> containing Blackjack's full regalia: a black hooded <strong>cloak of elvenkind</strong>, several masks, 12 masterwork 'B'-pommeled daggers, <strong>+1 resilient slick leather armor</strong>, <strong>boots of elvenkind</strong>, an <strong>amulet of proof against detection</strong>, black <strong>gloves of climbing and swimming</strong> (two fingers of the right glove false and adjustable — concealing Vencarlo's old dueling wound), and a <strong>+2 striking keen rapier</strong>. "+chk("type:society|dc:15")+" (automatic for anyone who saw the execution rescue) recognizes <strong>Blackjack's</strong> signature gear.</p>")
  + B.s_conv("<p><strong>The Blackjack legacy.</strong> The mantle has passed hero-to-hero for generations; Vencarlo is merely its latest bearer. With this cache, <em>a PC could become the next Blackjack</em> — encourage it; the regalia is sized to fit its wearer. If the PCs don't fight the fire, the house burns (citizens + Arkona brigades contain the blaze but can't save it; the lockbox survives, "+chk("type:perception|dc:25")+" in the rubble).</p>"))

area3("A½", "The Concerned Student", SR("The Concerned Student", 145)
  + "<p>Drawn by the flames or the fight, a familiar face approaches: <strong>Amin Jalento</strong> (the noble the PCs may have saved from the Chapter 1 mob — or his cousin Gerran, if Amin died), trapped on the island by the quarantine and squatting in a collapsed building across from the academy.</p>"
  + "<p>His story: he was Vencarlo's houseguest when <strong>Red Mantis assassins stormed the academy</strong> — Vencarlo cut one down and fled; the assassins burned the school. Before that, Vencarlo kept strange hours, came home bloodied, and met three times behind closed doors with a wild-haired, paint-stained visitor Amin recognized: the notorious artist <strong>Salvator Scream</strong>. Their last meeting ended in shouting. Salvator lives at <strong>140 Wave Street, Old Dock</strong> — the Emperor's territory.</p>"
  + B.s_treasure("<p><strong>Story awards:</strong> learning of Salvator Scream → <strong>2,400 XP</strong>; escorting Amin safely off the island → a further <strong>4,800 XP</strong>.</p>"))

PG("B. The Artist's Lair",
  B.s_milestone("<p><strong>B. The Artist's Lair</strong> — Salvator Scream's leaning, decrepit house at <strong>140 Wave Street</strong>, Old Dock, near a ruined Narrows bridge. "+chk("type:diplomacy|dc:15")+" (gather information) confirms the address and the artist's grisly reputation (Exemplary Execrables' backdrop painter). A <em>locate creature</em> would reveal Salvator is no longer here — the Emperor's thugs took him days ago.</p>")
  + SEC("<p><strong>Who's actually home:</strong> "+act(A3["laori"], "Laori Vaus")+", squatting amid her investigation. She is <em>friendly</em> unless attacked — let her be the PCs' strangest handshake of the campaign.</p>"))

area3("B1-B2", "Front Room & Bedroom", SR("B1-B2", 146)
  + box("The smell in this entryway is of must and",
        "<p>The entry smells of must and old paint; muddy boot prints track across the floor past a single emptied shelf. In the bedroom beyond, blankets lie thrown back from a single bed — a dark stain dried on the pillow.</p>")
  + B.s_skill("<p>"+chk("type:survival|dc:20")+" (front room): a half-dozen people tromped through — and a seventh was <strong>dragged out</strong>, toes scuffing. "+chk("type:survival|dc:20")+" (bedroom): the prints converge on the bed — Salvator was clubbed in his sleep (the blood) and carried off. The trail is days old and leads toward central Old Dock: <strong>Pilts's Palace</strong>.</p>"))

area3("B3", "Salvator's Studio", SR("B3", 146)
  + box("Both of this room's windows are tightly shuttered, yet",
        "<p>Both windows are tightly shuttered, yet candlelight flickers within: six polished human skulls arranged in an arc across a paint-spattered desk, a lit taper atop each. Gruesome unsold canvases lean ten deep against the walls.</p>")
  + "<p>"+act(A3["laori"], "Laori Vaus")+" works here among the skulls of Kazavon's six suicides (costumer, toymaker, writer, sculptor, tattooist, poet — she names them fondly), questioning the dead with mostly-garbled results.</p>"
  + SEC("<p><strong>Her bargain:</strong> an alliance to reach Salvator, sealed by her evidence — a bloodstained sleeve-scrap bearing the city's coat of arms, found wedged behind the bed ("+chk("type:society|dc:15")+": it is from the uniform of the <strong>seneschal of Castle Korvosa</strong> — torn when Salvator splinted Neolandus's broken arm). She reveals the Emperor of Old Korvosa holds Salvator. <strong>Story award</strong> for a peaceful alliance. If rebuffed, she cheerfully shadows the party for a dramatic save later.</p>"))

area3("B4", "Fungal Incursion", SR("B4", 147)
  + box("This room appears to have once been a combination",
        "<p>A onetime kitchen and storeroom, now riotous with fungal growth — Salvator's pigment-cultivation gone feral in his absence.</p>")
  + "<p>A patch of "+YELLOW_MOLD+" (the official L8 hazard) chokes the sunless northeast corner — Salvator handled his samples only in sunlight; his abductors didn't know to.</p>"
  + B.s_treasure("<p>Beneath the growth, among the painting supplies: a full jar of <strong>marvelous pigments</strong> — the chapter's signature wondrous treasure.</p>"))

area3("B5", "The Sinkhole", SR("B5", 147)
  + box("What once might have been a small house has",
        "<p>What once might have been a small house has collapsed into a twenty-foot sinkhole of mud and standing water; the adjacent boardwalk sags into the pit.</p>")
  + "<p>The quarantine ended the city's otyugh-control; several burst up a drainage tunnel here. The mud bottom is difficult terrain; the slick slope takes "+chk("type:athletics|dc:12")+" to scale under pressure.</p>"
  + B.enc("Sewer otyughs", encx([B.mon_lvl("otyugh")] * 3, 8),
     "<p>3 "+B.mon("otyugh", "otyughs")+" wallow and lurch out at passersby (apply the Elite adjustment for a meaner fight). If the PCs haven't met "+act(A3["laori"], "Laori")+" yet, she bursts from B3 a round in, shrieking with delight, and joins the fight to earn goodwill.</p>",
     B.aside_token(["3× "+B.mon("otyugh", "Otyugh (4)"), act(A3["laori"], "Laori Vaus (10, ally)")])))

PG("Part 2 — The Emperor of Old Korvosa",
  B.s_milestone("<p><strong>Part 2.</strong> Pilts Swastel — failed impresario of the gore-playhouse <strong>Exemplary Execrables</strong> — has crowned himself Emperor of Old Korvosa. He rules Old Dock by spectacle: real-death 'plays,' the mob game <strong>blood pig</strong>, and an ornately carved guillotine (the 'tall knife') with a standing appetite. When volunteers run short, he invents traitors.</p>")
  + B.s_skill("<p><strong>Researching the emperor:</strong> each attempt takes 1d4 hours and a "+chk("type:diplomacy|dc:20")+" (gather information; substantially harder off-island). Better results name Pilts, his guillotine, his salvaged playhouse hoard, and his newest 'acquisition' — a captive painter.</p>")
  + B.s_conv("<p>His 'palace' is a block of converted tenements in central Old Dock. Salvator is there. So is the audience the PCs will need to play to — or fight through.</p>"))

# --- C. Pilts's Palace ---
PG("C. Pilts's Palace",
  B.s_milestone("<p><strong>C. Pilts's Palace</strong> — a block of gutted tenements in central Old Dock, linked by rope bridges and rooftop fields, where the Emperor holds court from an hour past sunrise to dusk. The intended path is <strong>showmanship, not siege</strong>: petition the Emperor, accept the blood pig wager, win an audience with Salvator. Fighting the whole court at once is an Extreme-tier mistake — "+encx([10, 8, 5, 5, 5, 5], 8)+".</p>"))

area3("C1-C2", "Entrance & Guardroom", SR("C1-C2", 152)
  + box("The interior of this home has been gutted",
        "<p>The first home stands gutted around a mound of rubble; rickety stairs wind up to a splintered hole near the roofline, where a rope bridge sways 15 feet up.</p>")
  + "<p>The attic guardroom beyond holds 4 "+act(A3["empthug"], "Emperor's Thugs")+" (−2 to their Perception — they're arguing about whether chokers have skeletons). Rope bridges exit level (NE) and climbing 10 ft (SW, to the throne balcony); the ground-floor stairs are rubble-choked.</p>"
  + B.enc("Guardroom", encx([5, 5, 5, 5], 8),
     "<p>4 "+act(A3["empthug"], "Emperor's Thugs")+" — posted only while the alarm is down.</p>",
     B.aside_token(["4× "+act(A3["empthug"], "Emperor's Thug (5)")])))

area3("C3", "The Emperor's Throne", SR("C3", 153)
  + box("This open-air balcony is shielded from rain",
        "<p>A canvas-roofed balcony overlooks the rooftop field 25 feet below. Upon it squats a throne of gilt scrap — a cheap mockery of the Crimson Throne — and, to its west, an ornately carved guillotine, its blade gleaming with use it has not yet been given today.</p>")
  + "<p>"+act(A3["pilts"], "Pilts Swastel")+" holds court here daily with "+act(A3["jabbyr"], "Jabbyr")+" (in executioner's costume at the "+haz(A3["tallknife"], "Tall Knife")+") and 4 "+act(A3["empthug"], "thugs")+", hearing mob reports, citizen pleas, and execution dockets.</p>"
  + SEC("<p><strong>Negotiating:</strong> Pilts happily confirms Salvator is his 'houseguest' but refuses every plea and threat — until boredom suggests <strong>the wager</strong> (see A Rousing Game). An <em>unnoticed</em> <em>suggestion</em>-style spell can move him; a noticed one means the Tall Knife. </p>")
  + B.enc("The full court (DON'T)", encx([10, 8, 5, 5, 5, 5], 8),
     "<p>"+act(A3["pilts"], "Pilts (10)")+" + "+act(A3["jabbyr"], "Jabbyr (8)")+" + 4 "+act(A3["empthug"], "thugs")+" + a mob of spectators — an Extreme bloodbath best avoided until the blood pig audience isolates Pilts (see the Development under Blood Pig).</p>",
     B.aside_token([act(A3["pilts"], "Pilts Swastel (10)"), act(A3["jabbyr"], "Jabbyr (8)"), "4× "+act(A3["empthug"], "Thug (5)"), haz(A3["tallknife"], "The Tall Knife (10)")])))

area3("C4-C5", "The Emperor's Stage & Rooftops", SR("C4-C5", 154)
  + box("The large, flat roof of this long building",
        "<p>The long building's flat roof has been made a game-field: two blood-outlined squares mid-field, pig-cages over roof-holes at either end, and gently sloped rooftops to the south fitted with scavenged arena seating.</p>")
  + "<p>The <strong>blood pig field</strong>: cages (C4a/C4e) over trapdoors; wolverine pits (C4b/C4f — one starving "+B.mon("wolverine", "wolverine")+" each); team squares (C4c/C4d). The southern spectator rooftops (C5) hold 4 patrolling "+act(A3["empthug"], "thugs")+" off-game, and dozens of lowlifes during one.</p>")

area3("C6", "Storeroom", SR("C6", 155)
  + box("Crates, boxes, and barrels fill this long storeroom",
        "<p>Crates, boxes, and barrels fill this long storeroom — fire-scarred props, tools, and salvage from Exemplary Execrables.</p>")
  + B.s_treasure("<p>"+chk("type:perception|dc:25")+" turns up a small jewelry box of worthless costume glass — and a real <strong>ring of chameleon power</strong> (quirk: activating or removing it turns all the wearer's hair a random unnatural colour; Pilts refused to wear it).</p>"))

area3("C7", "Choker Nest", SR("C7", 155)
  + box("This large room might once have been an attic",
        "<p>This large attic opens to the sky where its northwest corner has collapsed; the shadows between the rafters seem to shift and reach.</p>")
  + "<p>Six "+act(A3["chokerbrute"], "choker brutes")+" — Pilts's corpse-disposal partners since the theater days — nest here. The collapsed gap can be a stealth entry ("+chk("type:athletics|dc:20")+" to climb the 25-ft exterior), but within 5 feet of the broken floor a square crumbles: "+chk("type:reflex|dc:15")+" to lurch back or fall for @Damage[2d6[bludgeoning]] (and the noise).</p>"
  + B.enc("The nest", encx([5] * 6, 8),
     "<p>6 "+act(A3["chokerbrute"], "choker brutes")+" strike from the rafters — at the door from outside, or 3 rounds after southern intruders start moving. They fight to the death.</p>",
     B.aside_token(["6× "+act(A3["chokerbrute"], "Choker Brute (5)")]))
  + B.s_treasure("<p>"+chk("type:perception|dc:15")+" finds their bag wedged in the SE rafters: ~75 gp re-scaled in coin, a pearl-inset silk glove, a masterwork hand crossbow, and a <strong>wand of slow</strong> (13 charges).</p>"))

area3("C8-C10", "Stairway, Art Supplies & Trophy Hall", SR("C8-C10", 156)
  + "<p><strong>C8</strong>, a collapsed stairway, and <strong>C9</strong>, where Salvator's confiscated paints and his finished commissions are stored. <strong>C10</strong> is the trophy hall:</p>"
  + box("The air in this room smells sickly sweet",
        "<p>The air smells sickly sweet: fourteen brine-and-perfume-preserved heads — mostly human, two elven, one dwarven — gaze down from the walls. A child-sized bed sits in one corner; a fine-set dining table fills the middle.</p>")
  + SEC("<p>Pilts talks to the heads on sleepless nights; the small bed is Jabbyr's. The C11 door carries an <em>alarm</em> spell keyed to Pilts.</p>")
  + B.s_treasure("<p>The table is set with a full silverware service (~50 gp re-scaled) and a platinum-and-crystal brandy decanter (~75 gp).</p>"))

area3("C11", "The Emperor's Chambers", SR("C11", 157)
  + box("This extravagantly decorated bedroom would seem to belong",
        "<p>An extravagantly royal bedroom — until a second look picks out the worn theatrical props, gilt paint, and patched curtains of a stage-set monarchy.</p>")
  + "<p>Pilts sleeps and reads here after dark, and for an hour each night unbolts the C12 door to feed Salvator and collect finished paintings.</p>"
  + B.s_treasure("<p><strong>The three Scream originals</strong> (painted before his muse fell silent — and full of buried truth): a shadow-clad figure at a dolmen ("+chk("type:religion|dc:25")+": Zon-Kuthon entering ancient Nidal; ~45 gp); desert riders over skull-dunes ("+chk("type:religion|dc:30")+": a scene from the <em>Umbral Leaves</em>; ~110 gp); a man peeling away his own flesh to reveal <strong>blue scales</strong> ("+chk("type:society|dc:30")+" places the horizon-castle as <strong>Scarwall</strong> in Belkzen; "+chk("type:arcana|dc:30")+" matches the scales to a blue dragon; ~200 gp). If "+act(A3["laori"], "Laori")+" is along she wants all three, settles for a split — and keeps offering to buy the PCs' share.</p>"))

area3("C12", "Salvator's Cell", SR("C12", 158)
  + box("The air in this room is an unpleasant mix",
        "<p>The air is an unpleasant mix of paint, sweat, and despair: a barred room of easels and half-finished horrors, its single occupant flinching at the sound of the bolt.</p>")
  + "<p>"+act(A3["salvator"], "Salvator Scream")+" paints here under lock, bar, and beating. He begs rescue of any visitor who isn't the Emperor — but says <em>nothing</em> of Neolandus while Pilts lives. His price: <strong>the Emperor's death, and escort to the mainland</strong> ("+chk("type:diplomacy|dc:10")+" with a credible rescue promise; Intimidation or magic also work — "+act(A3["laori"], "Laori")+" cheerfully recommends both).</p>"
  + B.s_conv("<p>His testimony is the chapter's hinge: <strong>Ileosa murdered the king; Neolandus knows; the Arkonas have him.</strong> On to Part 3 — and the rescue earns the trail to Arkona Palace.</p>"))

PG("A Rousing Game: BLOOD PIG!",
  B.s_milestone("<p><strong>The wager.</strong> Pilts offers it when pleading stalls: beat his champion team — the eight-thug <strong>Shinglesnipes</strong> — at <strong>blood pig</strong>, and the PCs get five supervised minutes with Salvator (plus, if they surrendered their gear at the door, its return and safe escort from Old Dock). The rules were invented by a madman, are never written down, and change weekly — narrate Pilts declaiming them; confusion is part of the show.</p>")
  + "<p><strong>The rules (as declaimed this week):</strong> first team to <strong>5 points</strong>; a point = your team's pig into your team's pit. No weapons, no spellcasting (each violation = a point to the other team); unarmed Strikes are legal. Up to 8 a side, starting in the marked squares; a fresh pig is craned into the cage opposite the scoring team's pit; a coin flip starts play.</p>"
  + "<ul>"
    "<li><strong>Picking up</strong> a pig (cage or loose): an Interact action that provokes reactions; a loose pig also needs a successful unarmed Strike vs AC 15 to corner.</li>"
    "<li><strong>Carrying</strong> a live pig: each round roll d6 on the <em>Squirming Pig</em> table — 1 slump (lose 1 action) · 2 squirm ("+chk("type:athletics|dc:18")+" or drop) · 3 squeal (the crowd roars) · 4 bite (pig attacks +6, 1 damage; if damaged, check to drop) · 5 kick ("+chk("type:reflex|dc:18")+" or drop) · 6 panic (all four at once). Taking damage while carrying: "+chk("type:fortitude|dc:18")+" or drop. Thugs knock their pigs out first.</li>"
    "<li><strong>Loose pigs</strong> bolt 30 ft from the nearest creature each round (never off the roof or into a pit). <strong>Pass</strong> = Interact to an adjacent ally; <strong>throw</strong> = improvised −2 Strike, 10-ft increments; <strong>catch</strong> "+chk("type:athletics|dc:18")+"; <strong>intercept</strong> (reaction) "+chk("type:athletics|dc:22")+"; <strong>steal</strong> = a Disarm attempt, then the table.</li>"
    "<li><strong>Scoring:</strong> drop into an adjacent pit free, or throw at the 1-ft mouth (a Strike vs AC 10). The pits are 10 ft deep with a starving "+B.mon("wolverine", "wolverine")+" in each — <strong>killing a wolverine forfeits</strong> for the killer's team; it spends 1d3 rounds devouring each scored piglet, otherwise claws at anything within 5 ft of the mouth.</li>"
    "<li><strong>Betting:</strong> the thugs give 2-to-1 against the PCs, up to 100 gp per PC.</li>"
   "</ul>"
  + B.enc("BLOOD PIG — the Shinglesnipes", encx([5] * 8, 8),
     "<p>8 "+act(A3["empthug"], "Emperor's Thugs")+" (the Shinglesnipes) — but it's a <em>game</em>, not a battle: unarmed, pig-fixated, crowd-roared. Run it fast and absurd.</p>",
     B.aside_token(["8× "+act(A3["empthug"], "Shinglesnipe (5)"), "2× "+B.mon("wolverine", "Wolverine (2)") + " (in the pits)"]))
  + SEC("<p><strong>Development — the sore loser.</strong> On a PC win Pilts demands two-of-three and adds "+act(A3["jabbyr"], "Jabbyr")+" to the Shinglesnipes; after a second loss he calls for three-of-five — and is told they're out of pigs. He nearly guillotines the messenger, then laughs, congratulates the PCs, and brings them up the balcony <em>with only Jabbyr and two thugs</em>. The supervised meeting (Salvator silent while Pilts lives) is the PCs' <strong>best shot at Pilts away from his mob</strong>: "+encx([10, 8, 5, 5], 9)+".</p>"))

PG("Part 3 — Wrath of the Arkonas",
  B.s_milestone("<p><strong>Part 3.</strong> Salvator's testimony points across Old Korvosa to <strong>Arkona Palace</strong>, where both Neolandus <em>and</em> Vencarlo sit in the dungeons below — insurance policies in a rakshasa's game.</p>")
  + SEC("<p><strong>The Arkona secret:</strong> generations ago, on a Vudra trade voyage, the human Arkonas were slaughtered and replaced by <strong>rakshasas</strong>. 'Glorio' is the rakshasa <strong>Bahor</strong>; his 'sister Meliya' is <strong>Vimanda</strong> (Verik's 'lover' from Chapter 1) — rivals locked in covert sibling war beneath a flawless family front. The palace crawls with lesser rakshasas and magically-thralled human 'relatives' who believe the family merely criminal.</p>"))

journal = B.journal_entry(JID3, "3. Escape from Old Korvosa", pages, folder=ADV_FOLDER)
B.write("journals", "03-escape-from-old-korvosa", copy.deepcopy(journal), embed_pages=True)

print(f"Chapter 3 built: {len(folders)} folders, {len(actors)} actors, 1 journal ({len(pages)} pages).")
