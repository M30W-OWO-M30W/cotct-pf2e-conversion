#!/usr/bin/env python3
"""Chapter 4 — A History of Ashes.

Own fat journal, appended to the shared packs alongside Ch.1-3. Party L10/11 -> 13.
The Cinderlands: the Respect Points subsystem, the Shoanti trials (Acropolis /
House of the Moon / Cindermaw / Flameford), the Flameford assault, and Part 3's
Deathhead Vault (Red Mantis HQ + Gray Maiden dungeons) back in Korvosa.
"""
from __future__ import annotations
import copy
import pf2e_build as B

MODID = "cotct-pf2e-conversion"
ACTOR_ROOT, ITEM_ROOT, ADV_FOLDER = "cotctActorRoot01", "cotctItemRoot001", "cotctAdvFolder01"

JID4 = "ch4HistoryAshes1"
A4 = {"ashwing": "ashwingGargoyl01", "cinderlander": "cinderlander0001", "krojun": "krojunEatsWhat01",
      "boneslayer": "skoanBoneslayer1", "thundercaller": "sklarThundercal1", "havtentacle": "haveroTentacle01",
      "moonmaiden": "moonMaiden000001", "akram": "akramTruthspeak1", "redreaver": "redReaver0000001",
      "cindermaw": "cindermawWorm001", "cinnabar": "cinnabarRedMant1", "koriantu": "koriantuPriest01",
      "manananggal": "manananggal00001", "cytillipede": "cytillipede00001", "endrin": "marcusEndrin0001",
      "gmguard": "grayMaidenGuard1", "tisharue": "tisharueWarden01", "zenobia": "zenobiaZenderh01",
      "motherthorns": "motherOfThorns01", "vyloth": "vylothMeladaem01", "kordaitra": "kordaitraDesta01",
      "eternalglyphs": "eternalGlyphs001", "dispellingmist": "dispellingMist01"}
F4 = {"a_ch4": "ch4ActorFolder01", "a_creatures": "ch4CreaturesFld1", "a_hazards": "ch4HazardsFld001"}
RMA = "redMantisAssn001"   # Ch.3 Red Mantis Assassin (reused throughout)

ids = B._idgen(440004)
def nid(): return next(ids)
sids = B._idgen(884004)
def sid(): return next(sids)

def act(_id, label): return f"@UUID[Compendium.{MODID}.cotct-actors.Actor.{_id}]{{{label}}}"
def haz(_id, label): return f"@UUID[Compendium.{MODID}.cotct-hazards.Actor.{_id}]{{{label}}}"
def chk(s): return f"@Check[{s}]"
def SEC(html): return B.s_secret(html, sid())
def box(anchor, fallback_html):
    t = B.verbatim(anchor)
    return B.s_read("<p>" + t + "</p>") if t else B.s_read(fallback_html)
CHC = "#8a1a1a"

folders = [
  B.folder(F4["a_ch4"], "4. A History of Ashes", "Actor", ACTOR_ROOT, 400000, CHC),
  B.folder(F4["a_creatures"], "Creatures", "Actor", F4["a_ch4"], 100000, None, "a"),
  B.folder(F4["a_hazards"], "Hazards", "Actor", F4["a_ch4"], 200000, None, "a"),
]
for f in folders:
    B.write("actors", "_folder_ch4-" + f["name"].lower().replace(" ", "-").replace(".", "") + "-act", copy.deepcopy(f))

actors = []
def AW(slug, doc):
    actors.append(copy.deepcopy(doc)); B.write("actors", slug, doc, embed_items=True)

# ---- Cinderlands actors ----
AW("ashwing-gargoyle", B.npc(A4["ashwing"], "Ashwing Gargoyle", 6, 24, 95, 14, 14, 12, 13,
  {"str": 4, "dex": 4, "con": 4, "int": 0, "wis": 2, "cha": 0}, 40,
  {"stealth": 16, "acrobatics": 14, "survival": 12}, ["earth", "gargoyle"], ["common", "petran"],
  [B.strike(nid(), "Claw", 17, "2d8+7", "slashing", ["agile"]),
   B.strike(nid(), "Jaws", 17, "2d10+7", "piercing", []),
   B.action(nid(), "Flyby Strike", "2", "<p>The gargoyle Flies up to its Speed and makes one Strike at any point along the way — denying grounded foes their full answer.</p>", ["attack"]),
   B.action(nid(), "Freeze", "1", "<p>It holds statue-still: until it moves, it is indistinguishable from eroded rock ("+chk("type:perception|dc:26")+" against its Stealth to pick it from the cindercone scree). +4 circumstance to Stealth in stony terrain.</p>", ["concentrate"], "defensive"),
   B.action(nid(), "Stone Hide", "passive", "<p>Resistance physical 5 (except adamantine).</p>", category="defensive")],
  notes="<p><strong>Role:</strong> the Ashwings — advanced gargoyles at generations-long war with all three quahs, bought for this chapter with Red Mantis gold from Mediogalti. They hate humans (Shoanti most of all), ferry the assassins over the spike-stone fields at Flameford, and look exactly like wind-carved rocks until they don't.</p>"
        "<p><strong>Tactics:</strong> Flyby Strikes and altitude; they never brawl grounded. <strong>Morale:</strong> a gargoyle flees below ~10 HP; when the last assassin dies, all survivors quit the field.</p>",
  folder=F4["a_creatures"], senses=[{"type": "darkvision"}], other_speeds=[{"type": "fly", "value": 60}],
  blurb="Mercenary gargoyle of the Cinderlands", token_src=None))

AW("the-cinderlander", B.npc(A4["cinderlander"], "The Cinderlander", 12, 33, 230, 23, 24, 19, 25,
  {"str": 2, "dex": 6, "con": 5, "int": 0, "wis": 3, "cha": -1}, 25,
  {"stealth": 26, "survival": 24, "intimidation": 20, "nature": 20, "medicine": 22}, ["humanoid", "human"], ["common", "jotun", "shoanti"],
  [B.strike(nid(), "Vindicator (+2 Striking Human-Bane Repeating Crossbow)", 27, "3d10+8", "piercing", ["magical", "range-increment-120", "reload-0"], slug="vindicator"),
   B.strike(nid(), "Handaxe", 22, "2d6+4", "slashing", ["agile", "sweep", "thrown-10"]),
   B.action(nid(), "Human's Bane", "passive", "<p><em>Vindicator</em> is bane to humans: +2 status to hit them and an extra @Damage[2d6[piercing]]; against <strong>Shoanti</strong> the Cinderlander also adds his hunted-prey bonus (+2 circumstance to hit, included against them). He loads <strong>screaming bolts</strong> (on a hit, foes within 20 ft: "+chk("type:will|dc:30")+" or "+B.cond("frightened", "Frightened 1")+").</p>", category="offensive"),
   B.action(nid(), "Hunter's Volley", "2", "<p>Two Vindicator Strikes against the same target; if both hit, the target also takes @Damage[1d8[bleed]] (his signature crippling shot).</p>", ["flourish"]),
   B.action(nid(), "Shot on the Run", "2", "<p>He Strides twice (or Strides and Takes Cover) and makes one Vindicator Strike at any point — fighting like the desert: never where the answer lands.</p>", ["attack", "move"]),
   B.action(nid(), "Desert Master", "passive", "<p>Immune to fatigue and exhaustion; fire resistance 10; <em>pass without trace</em> at will in the Cinderlands (+4 circumstance vs. tracking).</p>", category="defensive"),
   B.lore(nid(), "Cinderlands Lore", 24),
   B.gear("chain-mail", nid())],
  notes="<p><strong>Role:</strong> the 'devil tshamek' — sole survivor of a thorp the Shoanti burned, turned genocidal hunter. His calling card: a Shoanti head on a pole, red crossbow bolts through both eyes ("+chk("type:society|dc:30")+" to place it; automatic with a Shoanti companion). Skoan-Quah legend says he is a dead general's unquiet ghost killing until his losses are equalled. Now <strong>Cinnabar's paid guide</strong> — he leads the Red Mantis to the Acropolis and Flameford. His firepelt cougar <strong>Neverfar</strong> (treat as an official leopard with +10 HP) guards his sleep and dies before abandoning his body.</p>"
        "<p><strong>Tactics:</strong> never within reach — <em>Vindicator</em> at range, Shoanti to the exclusion of all else. <strong>Morale &amp; the lever:</strong> he despises the Red Mantis; a bribe of <strong>~50 gp or better</strong> (re-scaled) turns him mid-fight. He flees below ~20 HP. At Flameford his price is <strong>Krojun's life</strong> (see Saving Krojun). His head is a valid CR-9+ respect trophy.</p>",
  folder=F4["a_creatures"], blurb="The devil tshamek; Shoanti-hunter for hire", token_src=None, actor_link=True))

AW("krojun-eats-what-he-kills", B.npc(A4["krojun"], "Krojun Eats-What-He-Kills", 12, 33, 250, 25, 20, 21, 20,
  {"str": 7, "dex": 2, "con": 6, "int": -1, "wis": 0, "cha": 1}, 45,
  {"athletics": 26, "intimidation": 23, "survival": 20, "acrobatics": 20}, ["humanoid", "human"], ["common", "shoanti"],
  [B.strike(nid(), "+1 Striking Thundering Earth Breaker", 26, "2d12+13", "bludgeoning", ["backswing", "magical", "shove"], [("1d6", "sonic")], slug="krojun-breaker"),
   B.strike(nid(), "+1 Klar", 25, "2d6+11", "slashing", ["magical"]),
   B.strike(nid(), "Bite", 24, "2d8+9", "piercing", ["agile"]),
   B.action(nid(), "Thunder and Fang", "2", "<p>Krojun Strikes with the earth breaker and the klar against one target (combine damage); the klar's shield keeps a +1 circumstance bonus to his AC all round. On a critical hit he <strong>screams his own name</strong>.</p>", ["flourish"]),
   B.action(nid(), "Rage", "1", "<p>+6 damage (included), 24 temporary HP, −1 AC (included). He rages if a sredna match passes six rounds, and always in real battle.</p>", ["concentrate", "emotion", "mental"], "defensive"),
   B.action(nid(), "Unstoppable", "passive", "<p>Resistance physical 4; he cannot be flanked by creatures of his level or lower; scent (imprecise) 30 ft.</p>", category="defensive"),
   B.lore(nid(), "Shoanti Lore", 20),
   B.equipment(nid(), "Shoanti War Paint (orange, x3)", 8, 15, "<p>Ritual paint; a dose grants +1 status to saves vs. fear for 10 minutes.</p>", traits=["consumable", "talisman"])],
  notes="<p><strong>Role:</strong> Sklar-Quah champion — trained in Thunder and Fang by a sorcerer's trials, single-handedly freed his enslaved kin from the orc champion Kyrust Chiefkiller. He despises tshamek on principle but is <em>secretly testing</em> whether these ones deserve respect: he wants to stop a suicidal Shoanti march on Korvosa. The chapter's rival-then-ally: the sredna challenge, the shadowing war party ("+chk("type:perception|dc:40")+" to be sure it's him), the Acropolis 'observation,' the Flameford protest — and, if the PCs save him from the Cinderlander, <strong>nalharest</strong>: honorary siblinghood and lifelong alliance.</p>"
        "<p><strong>Morale:</strong> withdraws if hopelessly overmatched or at ~20 HP — but <strong>fights to the death while raging</strong>. At the Flameford duel he stands at 30 HP against the Cinderlander's 100.</p>",
  folder=F4["a_creatures"], senses=[{"acuity": "imprecise", "type": "scent", "range": 30}],
  blurb="Sklar-Quah champion; rival, then nalharest", token_src=None, actor_link=True))

AW("skoan-quah-boneslayer", B.npc(A4["boneslayer"], "Skoan-Quah Boneslayer", 5, 21, 70, 11, 11, 12, 11,
  {"str": 3, "dex": 2, "con": 2, "int": -1, "wis": 2, "cha": 3}, 20,
  {"medicine": 13, "religion": 11, "survival": 11, "stealth": 11}, ["humanoid", "human"], ["common", "shoanti"],
  [B.strike(nid(), "Earth Breaker", 14, "2d6+6", "bludgeoning", ["backswing", "shove"]),
   B.strike(nid(), "Composite Longbow", 13, "1d8+4", "piercing", ["deadly-d10", "propulsive", "range-increment-100", "volley-30"]),
   B.action(nid(), "Bone Ward", "1", "<p>The boneslayer calls on the ancestors: one ally within 30 feet gains +1 status to AC and saves vs. undead and fear for 1 round; or the boneslayer casts a minor heal (@Damage[1d8+4[healing]], touch).</p>", ["concentrate", "divine"]),
   B.action(nid(), "Undead Hunter", "passive", "<p>+2 circumstance damage against undead; +2 status to saves vs. disease, mental, and poison (the haunted oracle-blood of the Skull Clan).</p>", category="offensive"),
   B.gear("composite-longbow", nid()), B.gear("healing-potion-minor", nid(), 2)],
  notes="<p><strong>Role:</strong> the four Skoan-Quah escorts Thousand Bones lends the party — <strong>Ahalak, Hargev, Nalmid, Shadfrar</strong> — guides, witnesses, and walking proof the PCs can protect Shoanti. <strong>At least one alive</strong> when meeting a Sun Shaman eases everything.</p>"
        "<p><strong>Tactics:</strong> bows from cover; they mob whatever engages one of them; at 10+ Respect Points they follow the PCs' plans. They fight to the death. <strong>Stakes:</strong> each one slain and unraised costs 1d4 Respect Points; all four dead freezes RP gains until one is raised or replaced (Thousand Bones can resupply four more, three times). <strong>Story award</strong> per original survivor at chapter's end.</p>",
  folder=F4["a_creatures"], blurb="Skull-clan escort & witness (Ahalak/Hargev/Nalmid/Shadfrar)", token_src=None))

AW("sklar-quah-thundercaller", B.npc(A4["thundercaller"], "Sklar-Quah Thundercaller", 7, 25, 110, 15, 12, 15, 13,
  {"str": 4, "dex": 3, "con": 5, "int": 0, "wis": -1, "cha": 3}, 25,
  {"performance": 16, "intimidation": 14, "survival": 12, "athletics": 15}, ["humanoid", "human"], ["common", "shoanti"],
  [B.strike(nid(), "+1 Totem Spear", 17, "2d10+7", "piercing", ["magical", "versatile-s"], slug="totem-spear"),
   B.strike(nid(), "Thrown Totem Spear", 15, "1d10+7", "piercing", ["thrown-20"]),
   B.action(nid(), "Inspired Rage", "1", "<p>The thundercaller's raging song: allies within 60 feet gain +2 status to melee damage and saves vs. fear, and may rage along (the skald-magic of the Burn Riders).</p>", ["auditory", "composition", "emotion", "mental"]),
   B.action(nid(), "Sound Burst", "2", "<p>A crash of thunder in a 10-ft burst within 60 feet: @Damage[4d10[sonic]] ("+chk("type:fortitude|dc:25|basic:true")+"; "+B.cond("deafened", "Deafened")+" 1 round on a failure).</p>", ["concentrate", "manipulate", "sonic", "occult"]),
   B.action(nid(), "Whistling Spear", "passive", "<p>The holed shovel-head of the totem spear plays eerie music in motion — the thundercaller may Demoralize with Performance, and his healing songs (cure spells) work at 30 ft.</p>", category="offensive"),
   B.lore(nid(), "Sklar-Quah Lore", 13)],
  notes="<p><strong>Role:</strong> Sklar-Quah war-skalds (Krojun's honor guard at the Acropolis travels three strong). One sings Inspired Rage while the others fight; the singer heals from range; any melee skald at ~30 HP falls back and swaps roles.</p>"
        "<p><strong>Morale:</strong> they fight to the death <em>while Krojun lives</em>; if he falls, they quit the field and speak ill of the PCs (−1d6 Respect Points). <strong>Story award:</strong> if the PCs never attack the hot-heads, each thundercaller surviving the Acropolis pays XP as if defeated.</p>",
  folder=F4["a_creatures"], blurb="Sklar-Quah war-skald", token_src=None))

AW("havero-tentacle", B.npc(A4["havtentacle"], "Havero Tentacle", 9, 28, 110, 20, 14, 14, 16,
  {"str": 7, "dex": 3, "con": 5, "int": -5, "wis": 0, "cha": 0}, 0,
  {"athletics": 22}, ["aberration", "mindless"], [],
  [B.strike(nid(), "Tentacle Lash", 22, "2d12+9", "bludgeoning", ["reach-60"]),
   B.action(nid(), "Serpentine Reach", "1", "<p>The tentacle's tip relocates anywhere within 50 feet of its base (its base cannot move), then Strikes any creature adjacent to <em>any point along its length</em> — track its coils on the map.</p>", ["attack", "move"]),
   B.action(nid(), "Sever & Recoil", "passive", "<p>At 0 HP the tentacle whips back beneath the pool (reduce the Noise total by 1d20). It can be attacked anywhere along its length. <strong>At most four tentacles are active at once</strong>; killing 20+ in one battle quells the havero for an hour.</p>", category="defensive")],
  notes="<p><strong>Role:</strong> the reaching limbs of the <strong>havero</strong> — an Outer-Rifts horror the Thrallkeepers part-summoned millennia ago, hibernating beneath the A2 pool, its bulk dimensionally adjacent to a dead star. <em>The havero itself (CR 24) cannot wake or come through.</em> Its tentacles answer <strong>Noise Points</strong> (see the A2 page): Twitch at 10, Investigate (1 tentacle) at 20, Seek (~30), Assault (2) at 40, Wrath (4) at 50.</p>",
  folder=F4["a_creatures"], size="grg", blurb="Reaching limb of the sleeping havero", token_src=None))

AW("lyrune-quah-moon-maiden", B.npc(A4["moonmaiden"], "Lyrune-Quah Moon Maiden", 6, 23, 95, 14, 11, 11, 13,
  {"str": 4, "dex": 1, "con": 5, "int": -1, "wis": 1, "cha": 0}, 40,
  {"survival": 13, "stealth": 12, "athletics": 14, "acrobatics": 11}, ["humanoid", "human"], ["common", "shoanti"],
  [B.strike(nid(), "+1 Starknife", 16, "2d4+7", "piercing", ["agile", "deadly-d6", "finesse", "magical", "thrown-20", "versatile-s"]),
   B.strike(nid(), "Thrown Starknife", 15, "1d4+7", "piercing", ["agile", "thrown-20"]),
   B.action(nid(), "Twin Stars", "2", "<p>Two Starknife Strikes against one target (combine damage); on a critical hit the target also takes @Damage[1d6[bleed]].</p>", ["flourish"]),
   B.action(nid(), "Moon Rage", "1", "<p>+4 damage (included while raging), 12 temporary HP, −1 AC. <strong>A raging maiden never flees.</strong></p>", ["concentrate", "emotion", "mental"], "defensive")],
  notes="<p><strong>Role:</strong> warrior-sisters of the Moon Clan — <strong>Tekrakai</strong> (leader), Eaklai, Maeva, Yandree — guarding the desecrated House of the Moon; a dozen of their sisters already died on the red reaver's claws. Potential <strong>allies</strong>, not foes: Tekrakai asks (or gratefully accepts) help killing it.</p>"
        "<p><strong>Tactics:</strong> open thrown, close raging with paired starknives. <strong>Morale:</strong> flee below ~10 HP unless raging. <strong>Story award</strong> per maiden surviving the reaver fight; arguing them out of it costs 2d4 Respect Points.</p>",
  folder=F4["a_creatures"], blurb="Moon-clan starknife warrior (Tekrakai's band)", token_src=None))

AW("akram", B.npc(A4["akram"], "Truthspeaker Akram", 7, 22, 85, 11, 9, 17, 13,
  {"str": -2, "dex": -1, "con": 0, "int": 1, "wis": 5, "cha": 3}, 40,
  {"religion": 17, "diplomacy": 15, "nature": 13, "society": 11}, ["humanoid", "human"], ["common", "shoanti"],
  [B.strike(nid(), "+1 Returning Starknife", 12, "2d4-1", "piercing", ["agile", "magical", "thrown-20"]),
   B.action(nid(), "Discern Lies", "passive", "<p>Akram always knows when he hears a deliberate lie — the gift that makes him the Cinderlands' only living <strong>truthspeaker</strong>. He is immune to charms and compulsions.</p>", category="defensive"),
   B.action(nid(), "Desna's Grace", "1", "<p>Heal (@Damage[4d8[healing]], touch or 30 ft), <em>calm emotions</em> ("+chk("type:will|dc:25")+"), or a luck-twist: one ally rerolls a failed save (once each per day per ally).</p>", ["concentrate", "divine", "healing"]),
   B.action(nid(), "Dimensional Hop", "1", "<p>Akram steps through space up to 80 feet total per day — his exit when alone and bloodied (then <em>fly</em> to safety).</p>", ["concentrate", "divine", "teleportation"]),
   B.lore(nid(), "Shoanti Tradition Lore", 17)],
  notes="<p><strong>Role:</strong> the Lyrune-Quah's 68-year-old cleric of Desna — spry-minded, frail-bodied, and the party's <strong>living endorsement</strong> (+3 Respect Points for his support; +10 circumstance on the Flameford Diplomacy). He insists on travelling along to <em>witness</em> their deeds, fixates charmingly on the most wilderness-awkward PC, and may not be given a Lyrune-Quah escort (honor forbids). Keeping him alive is the party's unspoken burden — a second story award if he survives to the Sun Shaman's lore.</p>",
  folder=F4["a_creatures"], blurb="The last truthspeaker; fragile, priceless ally", token_src=None, actor_link=True))

AW("red-reaver", B.npc(A4["redreaver"], "Red Reaver", 13, 34, 260, 26, 22, 21, 24,
  {"str": 8, "dex": 3, "con": 6, "int": -3, "wis": 2, "cha": 0}, 35,
  {"athletics": 27, "stealth": 21}, ["beast"], [],
  [B.strike(nid(), "Rending Claw", 27, "3d10+12", "slashing", ["agile"]),
   B.strike(nid(), "Jaws", 27, "3d8+12", "piercing", []),
   B.action(nid(), "Rend", "1", "<p><strong>Requirement</strong> Its last two actions were both successful Claw Strikes against one creature.</p><hr /><p><strong>Effect</strong> It tears: @Damage[3d10+12[slashing]] and @Damage[2d6[bleed]].</p>", ["attack"]),
   B.action(nid(), "Discordant Roar", "2", "<p>A 30-ft cone of skull-rattling sound: @Damage[6d6[sonic]] ("+chk("type:fortitude|dc:31|basic:true")+"), and creatures that fail are "+B.cond("frightened", "Frightened 2")+".</p>", ["auditory", "fear", "sonic"]),
   B.action(nid(), "Enraptured by Art", "passive", "<p>Its one flaw: a genuine artistic performance ("+chk("type:performance|dc:31")+") leaves it "+B.cond("fascinated", "Fascinated")+" — calm for 1 round per point of success, until threatened. It <strong>never sleeps</strong>.</p>", category="defensive")],
  notes="<p><strong>Role:</strong> the crimson horror squatting in the House of the Moon — it lost its mountain observatory to a landslide and adopted this one, eating the previous moon-maiden commander. Tekrakai's briefing is accurate: rending claws, the discord-roar, the art-trance, the sleeplessness, the territorial focus.</p>"
        "<p><strong>Tactics:</strong> roars first, then focuses its wrath on the <em>most heavily armored</em> targets. Fights to the death; pursues fleeing prey up to half a mile from the shrine.</p>",
  folder=F4["a_creatures"], senses=[{"type": "darkvision"}], size="lg", blurb="Art-loving territorial horror", token_src=None))

AW("cindermaw", B.npc(A4["cindermaw"], "Cindermaw, the Clan-Eater", 14, 36, 310, 28, 20, 23, 25,
  {"str": 9, "dex": 1, "con": 7, "int": -3, "wis": 2, "cha": 2}, 40,
  {"athletics": 30}, ["beast", "fire"], ["ignan"],
  [B.strike(nid(), "Jaws", 29, "3d12+13", "piercing", ["reach-15"], [("2d6", "fire")]),
   B.strike(nid(), "Body Slam", 29, "3d10+13", "bludgeoning", ["reach-15"]),
   B.action(nid(), "Swallow Whole", "1", "<p><strong>Requirement</strong> A Large or smaller creature is "+B.cond("grabbed", "Grabbed")+" in its jaws.</p><hr /><p><strong>Effect</strong> Gulp: the victim is swallowed — @Damage[3d6+13[bludgeoning]] plus @Damage[3d6[fire]] per round inside (Rupture 30: dealing 30 slashing/piercing damage to the gullet from within cuts an exit — <em>the entire point of the quest</em>).</p>", ["attack"]),
   B.action(nid(), "Volcanic Burrow", "passive", "<p>Burrow 40 ft through rock and cinder, surfacing in gouts of sparks; fire immunity; tremorsense (imprecise) 120 ft. <strong>Paralysis-resistant</strong> (+4 status vs. paralysis and slow — would-be Skuraks beware).</p>", category="defensive")],
  notes="<p><strong>Role:</strong> a quasi-divine fire-infused purple worm — an awakened, <em>vain</em> ancient that once devoured a Plane-of-Fire portal. The quest (Skurak's Tale, Handout #4-1): <strong>be swallowed and emerge, witnessed by Shoanti</strong>. How you get out is irrelevant; killing it is gauche (−1 Respect Point — a slain god 'wasn't that tough'). Tempting it to swallow you: a Deception against its Sense Motive at −2 (it suspects everything is food anyway). Illusions must beat the witnesses' saves <em>and radiate heat</em>.</p>"
        "<p><strong>Respect:</strong> +2 for a swallowed-and-escaped PC; <strong>+4 if Cindermaw also lives</strong>. Fire resistance strongly advised; <em>teleport</em>-from-the-belly is legal (concentration check inside).</p>",
  folder=F4["a_creatures"], senses=[{"acuity": "imprecise", "type": "tremorsense", "range": 120}], size="grg",
  other_speeds=[{"type": "burrow", "value": 40}], blurb="Quasi-divine clan-eating fire worm", token_src=None, actor_link=True))

# ---- The Cinderlander's rival + vault actors ----
AW("cinnabar", B.npc(A4["cinnabar"], "Cinnabar", 13, 34, 245, 21, 25, 18, 23,
  {"str": 4, "dex": 6, "con": 4, "int": 0, "wis": -1, "cha": 2}, 30,
  {"acrobatics": 25, "stealth": 25, "deception": 23, "intimidation": 23, "survival": 21}, ["humanoid", "human"], ["common"],
  [B.strike(nid(), "+1 Striking Sawtooth Saber", 27, "2d8+10", "slashing", ["agile", "finesse", "magical", "twin"], slug="cinnabar-saber"),
   B.sneak_attack(nid(), 5, "Cinnabar"),
   B.action(nid(), "Twin Sabers", "2", "<p>Two Saber Strikes against one target (the twin trait adds +3 circumstance damage to the second; combine for resistances).</p>", ["flourish"]),
   B.action(nid(), "Prayer Attack", "1", "<p>The blades weave, point-down: one creature within 30 feet, "+chk("type:will|dc:30")+" or "+B.cond("fascinated", "Fascinated")+"; sustained 3 full rounds, her next Saber Strike against the still-fascinated victim critically hits on a success.</p>", ["concentrate", "incapacitation", "mental", "visual"]),
   B.action(nid(), "Mantis Form", "2", "<p><strong>Frequency</strong> once per day. Cinnabar becomes a blood-red giant praying mantis (Large; her sabers' magic flows into her two claws; gains Grab and a lunging 10-ft reach). Her favorite opener with witnesses to terrify.</p>", ["concentrate", "polymorph", "occult"]),
   B.action(nid(), "Summon Mantis", "2", "<p><strong>Frequency</strong> once per day. She calls 1d3 fiendish "+B.mon("giant-mantis", "giant mantises")+" (blood-red) for 1 minute — round one of any planned fight, with <em>haste</em> on herself round two.</p>", ["concentrate", "conjuration", "occult"]),
   B.action(nid(), "Red Shroud", "1", "<p><strong>Frequency</strong> 4/day. Red mist: +1 circumstance AC and fast healing 2 for 7 rounds; on death she may dissolve into mist, leaving only gear.</p>", ["concentrate"], "defensive"),
   B.action(nid(), "Resurrection Sense", "passive", "<p>She knows, instantly and at any distance on the same plane, if a creature she slew within the past year returns to life.</p>", category="defensive"),
   B.lore(nid(), "Red Mantis Lore", 21),
   B.gear("chain-mail", nid()), B.gear("sawtooth-saber", nid(), 2)],
  notes="<p><strong>Role:</strong> commander of the Red Mantis in Korvosa — retasked by Ileosa from Neolandus to <em>the PCs</em>. Daughter of a Red Mantis cultist who laid a kill-weekly geas on her at eight; the geas died with her mother, but her underlings still believe in it, and their terror passes for loyalty. She directs the chapter's ambushes from afar (her cleric Koriantu's <em>sending</em>), pays the Cinderlander, and buys the Ashwings.</p>"
        "<p><strong>Morale — the broken thing in her:</strong> at ~10 HP she drops her sabers, kneels, and <strong>begs for a quick death</strong>. Killed: that's that. Left unharmed one round: she snatches up her blades and fights to the death at +4 attack and damage for 10 rounds. <strong>Offered surrender:</strong> speechless 1d6 rounds — and if unattacked through them, the kind child under the assassin may begin to surface. A redeemed Cinnabar shares the Kayltanya letter, warns of her Mistress, details the vault's defenders — and may stand with the PCs at the AP's climax. The Red Mantis will mark her for death.</p>",
  folder=F4["a_creatures"], blurb="Red Mantis commander; breakable blade", token_src=None, actor_link=True))

AW("koriantu", B.npc(A4["koriantu"], "Koriantu", 13, 33, 250, 23, 19, 25, 23,
  {"str": 4, "dex": 2, "con": 3, "int": 1, "wis": 6, "cha": 4}, 25,
  {"religion": 25, "deception": 21, "intimidation": 21, "medicine": 23}, ["humanoid", "aasimar"], ["common", "celestial", "infernal"],
  [B.strike(nid(), "+1 Striking Sawtooth Saber", 24, "2d8+7", "slashing", ["agile", "finesse", "magical", "twin"]),
   B.action(nid(), "Achaekek's Harm", "2", "<p>Void font (DC 31): touch for @Damage[7d8[void]] (basic "+chk("type:fortitude|dc:31")+"), 30-ft for @Damage[7d8+14[void]], or a 30-ft burst harming the living and mending undead.</p>", ["concentrate", "manipulate", "void", "divine"]),
   B.action(nid(), "Blade Barrier", "3", "<p>A wall of whirling sawtooth blades (60 ft long): @Damage[7d8[force]] to creatures passing through ("+chk("type:reflex|dc:31|basic:true")+") — her battlefield-splitter.</p>", ["concentrate", "force", "manipulate", "divine"]),
   B.action(nid(), "Divine Wrath", "2", "<p>A 20-ft burst within 120 feet: @Damage[6d10[spirit]] ("+chk("type:fortitude|dc:31|basic:true")+"; "+B.cond("sickened", "Sickened 1")+" on a failure).</p>", ["concentrate", "manipulate", "divine"]),
   B.action(nid(), "Scry the Hunt", "passive", "<p>From her sanctum's water-bowl she watches through her assassins (the Acropolis ambush exists so she can <em>study the PCs fight</em>); she relays Cinnabar's orders across the Cinderlands by <em>sending</em>.</p>", category="offensive"),
   B.lore(nid(), "Achaekek Lore", 25),
   B.gear("chain-mail", nid()), B.gear("sawtooth-saber", nid())],
  notes="<p><strong>Role:</strong> aasimar high priestess of Achaekek — an ex-Iomedaean crusader twelve years fallen, now the Red Mantis's <em>internal affairs</em>: she volunteered for Korvosa to document Cinnabar's failure and execute her as a weak link. She thinks the Ileosa contract cheapens the Mantis brand and has no personal interest in the PCs at all.</p>"
        "<p><strong>Her sanctum (E6)</strong> hides behind a <em>screen</em> illusion — animated slaughter-murals and a towering four-armed mantis statue ("+chk("type:will|dc:32")+" on interaction to doubt; only the six pillars are real). The 'statue' hides her cot, altar, and scrying bowl.</p>",
  folder=F4["a_creatures"], senses=[{"type": "darkvision"}], blurb="Achaekek's internal-affairs priestess", token_src=None, actor_link=True))

AW("manananggal", B.npc(A4["manananggal"], "Manananggal", 9, 27, 130, 17, 18, 18, 18,
  {"str": 5, "dex": 5, "con": 0, "int": 0, "wis": 2, "cha": 4}, 20,
  {"deception": 19, "stealth": 17, "acrobatics": 17}, ["undead"], ["common"],
  [B.strike(nid(), "Claw", 21, "2d10+8", "slashing", ["agile"]),
   B.strike(nid(), "Bite", 21, "2d8+8", "piercing", []),
   B.action(nid(), "Deep Slumber", "2", "<p>Up to three creatures in a 10-ft burst within 60 feet: "+chk("type:will|dc:27")+" or fall "+B.cond("unconscious", "Unconscious")+" (1 minute; slapping/damage wakes).</p>", ["concentrate", "incapacitation", "mental", "occult", "sleep"]),
   B.action(nid(), "Sever Torso", "1", "<p>By night the manananggal detaches: a legless, bat-winged upper body (fly 40 ft) — its abandoned lower torso (Hardness 0, HP 30) hides elsewhere; <strong>destroying the torso destroys the creature at dawn</strong>. By day it must rejoin or perish. In human guise it keeps its bite and claws.</p>", ["concentrate"], "defensive"),
   B.action(nid(), "Undead Resilience", "passive", "<p>Immune to death effects, disease, paralysis, poison, sleep (its own excepted), unconsciousness; void healing.</p>", category="defensive")],
  notes="<p><strong>Role:</strong> the two horrors of the Chokepoint (E3) were <strong>Sable Company officers</strong> — Avanah Banzul (second-in-command) and Ulweth Wevenner (hippogriff-master) — handed to Zenobia as prisoners and transformed ("+chk("type:society|dc:20")+" to recognize them). They remember their lives; the corruption is total. Their stored lower torsos lie in the E8 crypt.</p>"
        "<p><strong>Tactics:</strong> by night, slumber-bombs from the ledges, then swooping claws; by day they wear human shapes and pose as escaped prisoners to split parties. Loyal to Zenobia.</p>",
  folder=F4["a_creatures"], senses=[{"type": "darkvision"}], other_speeds=[{"type": "fly", "value": 40}],
  blurb="Severed-torso undead; ex-Sable officers", token_src=None))

AW("cytillipede", B.npc(A4["cytillipede"], "Cytillipede", 8, 26, 120, 17, 15, 13, 15,
  {"str": 5, "dex": 4, "con": 4, "int": -3, "wis": 1, "cha": -2}, 40,
  {"athletics": 18, "stealth": 16}, ["aberration"], ["undercommon"],
  [B.strike(nid(), "Mandibles", 20, "2d10+7", "piercing", [], [("1d6", "poison")]),
   B.action(nid(), "Cytillesh Flash", "2", "<p>Its segments strobe with brain-mold light in a 20-ft burst: "+chk("type:will|dc:26")+" or "+B.cond("stunned", "Stunned 1")+" and "+B.cond("dazzled", "Dazzled")+" 1 round (Stunned 2 on a critical failure). It times the flash for maximum coverage — the assassins sneak-attack the stunned.</p>", ["concentrate", "light", "visual", "incapacitation"]),
   B.action(nid(), "Numbing Venom", "passive", "<p>Mandible poison: "+chk("type:fortitude|dc:26")+" or @Damage[1d6[poison]] and "+B.cond("slowed", "Slowed 1")+" for 1 round.</p>", category="offensive")],
  notes="<p><strong>Role:</strong> a horse-sized, intelligent centipede-thing that begged for its life during the Gray Maidens' derro purge — and got it, in exchange for service. It lairs amid the E4 cytillesh patches (the brain-mold: 24 hours within 20 ft of a patch, "+chk("type:will|dc:25")+" or "+B.cond("stupefied", "Stupefied 1")+", cumulative).</p>",
  folder=F4["a_creatures"], senses=[{"type": "darkvision"}], size="lg", blurb="Mercy-bought brain-mold centipede", token_src=None))

AW("gray-maiden-guard", B.npc(A4["gmguard"], "Gray Maiden Guard", 6, 24, 100, 14, 10, 11, 12,
  {"str": 5, "dex": 1, "con": 4, "int": 0, "wis": -1, "cha": 2}, 20,
  {"athletics": 14, "intimidation": 14}, ["humanoid", "human"], ["common"],
  [B.strike(nid(), "Longsword", 17, "1d8+9", "slashing", ["versatile-p"]),
   B.strike(nid(), "Longbow", 14, "1d8+4", "piercing", ["deadly-d10", "propulsive", "range-increment-100", "volley-30"]),
   B.action(nid(), "Shield Wall", "reaction", "<p><strong>Trigger</strong> An adjacent Gray Maiden is hit.</p><hr /><p><strong>Effect</strong> The guard interposes her shield: the ally gains +2 circumstance AC against the triggering Strike.</p>"),
   B.action(nid(), "Shield Block", "reaction", "<p>Standard shield block (Hardness 5).</p>"),
   B.gear("full-plate", nid()), B.gear("steel-shield", nid()), B.gear("longsword", nid())],
  notes="<p><strong>Role:</strong> the Deathhead Vault's veteran garrison (a step above the Ch.2 foot soldier). Posts: the E15 cage (two firing through bars with cover, one shouting the alarm), E16 quarters (four resting — ~5 minutes to armor up after an alarm), the E18 watch-post (five). Conditioned: they fight to the death.</p>",
  folder=F4["a_creatures"], blurb="Veteran vault Gray Maiden", token_src=None))

AW("marcus-endrin", B.npc(A4["endrin"], "Marcus Endrin", 12, 32, 220, 22, 22, 19, 23,
  {"str": 4, "dex": 5, "con": 3, "int": 1, "wis": 3, "cha": 2}, 25,
  {"acrobatics": 23, "athletics": 21, "nature": 19, "society": 17, "survival": 19}, ["humanoid", "human"], ["common"],
  [B.strike(nid(), "Composite Longbow", 25, "2d8+7", "piercing", ["deadly-d10", "propulsive", "range-increment-100", "volley-30"]),
   B.strike(nid(), "Longsword", 22, "2d8+7", "slashing", ["versatile-p"]),
   B.action(nid(), "Commandant's Shot", "2", "<p>Two Longbow Strikes against one target; if both hit, the target is "+B.cond("off-guard", "Off-Guard")+" against the next attack before his next turn — thirty years of Sable Company marksmanship.</p>", ["flourish"]),
   B.lore(nid(), "Sable Company Lore", 19),
   B.gear("composite-longbow", nid()), B.gear("longsword", nid())],
  notes="<p><strong>Role:</strong> the last commandant of the Sable Company — the man who put an arrow in the queen's eye before all Korvosa and watched her smile. Found in the secret cell E14 ("+chk("type:perception|dc:40")+" for the door, +20 with the E20 records; Kordaitra's key or "+chk("type:thievery|dc:40")+"): unconscious, kept at death's edge by Kordaitra's visits, and <strong>feebleminded</strong>. Healed, he cringes like a beaten animal until the curse is lifted; cured and re-armed, "+chk("type:diplomacy|dc:24")+" enlists him ("+chk("type:intimidation|dc:25")+" works, but he bolts at first chance). <strong>Rescue = a full encounter's XP</strong>; his survival galvanizes the rebellion.</p>",
  folder=F4["a_creatures"], blurb="Feebleminded Sable commandant; great rescue", token_src=None, actor_link=True))

AW("tisharue", B.npc(A4["tisharue"], "Tisharue", 11, 31, 210, 21, 18, 17, 19,
  {"str": 5, "dex": 4, "con": 3, "int": 1, "wis": 1, "cha": 2}, 25,
  {"athletics": 22, "intimidation": 20, "society": 17, "deception": 17}, ["humanoid", "elf"], ["common", "elven"],
  [B.strike(nid(), "+1 Striking Longsword", 24, "2d8+11", "slashing", ["magical", "versatile-p"]),
   B.strike(nid(), "Composite Longbow", 22, "2d8+5", "piercing", ["deadly-d10", "propulsive", "volley-30"]),
   B.action(nid(), "Warden's Onslaught", "2", "<p>Three Longsword Strikes against one target (multiple-attack penalty applies; combine the first two for resistances) — fighter-perfect bladework.</p>", ["flourish"]),
   B.action(nid(), "Disciplinarian", "passive", "<p>Allied Gray Maidens within 30 feet gain +1 status to attacks and saves vs. fear — and would rather die than retreat before her.</p>", category="offensive"),
   B.lore(nid(), "Gray Maiden Lore", 19)],
  notes="<p><strong>Role:</strong> the elf warden of Deathhead — an early, fervent Maiden hunting 'relapse' in her own ranks. Her quarters (E17) display her mother's <strong>+2 invulnerability elven chain</strong> (a Tanglebriar heirloom; convert: +2 resilient mithral chain) and her files: margin-notes in Elven concluding that <strong>Sabina Merrin received far less conditioning than any other Maiden</strong> — leverage she hoards, hoping to take Sabina's place (and cultivate Kordaitra's favor).</p>",
  folder=F4["a_creatures"], senses=[{"type": "low-light-vision"}], blurb="Elf warden of Deathhead Vault", token_src=None, actor_link=True))

AW("zenobia-zenderholm", B.npc(A4["zenobia"], "Zenobia Zenderholm", 11, 30, 195, 17, 18, 21, 21,
  {"str": 4, "dex": 4, "con": 0, "int": 3, "wis": 4, "cha": 5}, 20,
  {"society": 22, "deception": 22, "intimidation": 20, "religion": 18, "occultism": 18}, ["undead"], ["common", "infernal", "necril"],
  [B.strike(nid(), "Entrail Caress", 23, "2d8+7", "bludgeoning", ["agile", "reach-10"], [("2d6", "void")]),
   B.strike(nid(), "Diseased Bite", 23, "2d10+7", "piercing", []),
   B.action(nid(), "Blood Drain", "1", "<p><strong>Requirement</strong> Her last action was a successful Bite.</p><hr /><p><strong>Effect</strong> She drains: @Damage[2d8[bleed]] and she gains that many temporary HP; the victim is exposed to <strong>filth fever</strong> ("+chk("type:fortitude|dc:30")+").</p>", ["attack"]),
   B.action(nid(), "Judge's Sentence", "2", "<p>Her old courtroom voice, weaponized: one creature within 30 feet, "+chk("type:will|dc:30")+" or "+B.cond("paralyzed", "Paralyzed")+" 1 round (incapacitation) as guilt and dread crush it.</p>", ["auditory", "emotion", "incapacitation", "mental", "occult"]),
   B.action(nid(), "Detach", "1", "<p>By night the penanggalen's head and entrails pull free of her body (fly 40 ft); the abandoned body (in the E8 sarcophagus) is helpless — destroying it doesn't destroy <em>her</em>, but ends her masquerade as a living woman. She must soak her entrails in vinegar to rejoin it.</p>", ["concentrate"], "defensive"),
   B.action(nid(), "Undead Resilience", "passive", "<p>Immune to death effects, disease, paralysis, poison, sleep; void healing; resistance physical 5 (except magical slashing).</p>", category="defensive"),
   B.lore(nid(), "Korvosan Law Lore", 22)],
  notes="<p><strong>Role:</strong> the senior arbiter who welcomed the Gray Maidens into the Longacre Building — because she was already theirs. Blood veil took her; Abadar's <em>remove disease</em> kept failing; <strong>Urgathoa answered</strong>. Now a penanggalen, she is the Pallid Princess's greatest Korvosan agent since Andaisin — and the vault's indoctrinator, torturing recruits by day and feeding by night (E18). Her guardian Vyloth resents the duty.</p>"
        "<p><strong>The mission question answered:</strong> 'why did Zenobia side with the queen?' — she didn't; she sided with her goddess. There is no one to rescue.</p>",
  folder=F4["a_creatures"], senses=[{"type": "darkvision"}], other_speeds=[{"type": "fly", "value": 40}],
  blurb="Penanggalen arbiter; the vault's indoctrinator", token_src=None, actor_link=True))

AW("mother-of-thorns", B.npc(A4["motherthorns"], "Mother of Thorns", 13, 33, 255, 21, 24, 22, 25,
  {"str": 5, "dex": 7, "con": 3, "int": 2, "wis": 4, "cha": 6}, 30,
  {"stealth": 26, "deception": 25, "intimidation": 25, "medicine": 21, "acrobatics": 25}, ["fiend", "sahkil"], ["common", "infernal", "necril"],
  [B.strike(nid(), "Razor Vine", 26, "3d8+9", "slashing", ["agile", "reach-15", "trip"], [("1d6", "poison")]),
   B.sneak_attack(nid(), 3, "The Mother"),
   B.action(nid(), "Look of Fear", "1", "<p>Her gaze: one creature within 30 feet, "+chk("type:will|dc:33")+" or "+B.cond("frightened", "Frightened 2")+" and "+B.cond("fleeing", "Fleeing")+" 1 round (Frightened 3 on a critical failure).</p>", ["concentrate", "emotion", "fear", "mental", "visual"]),
   B.action(nid(), "Dominate", "2", "<p>One humanoid within 30 feet: "+chk("type:will|dc:31")+" or "+B.cond("controlled", "Controlled")+" (re-save daily) — how the obstinate recruits are 'finished.'</p>", ["concentrate", "incapacitation", "mental", "occult"]),
   B.action(nid(), "Mind-Numbing Venom", "passive", "<p>Vine poison: "+chk("type:fortitude|dc:33")+" or @Damage[2d6[poison]] and "+B.cond("stupefied", "Stupefied 1")+" (stage 2: Stupefied 2 and "+B.cond("slowed", "Slowed 1")+").</p>", category="offensive"),
   B.action(nid(), "Spirit Walk", "2", "<p>She becomes briefly ethereal, stepping through walls — fear given form does not respect doors.</p>", ["concentrate", "occult"], "defensive")],
  notes="<p><strong>Role:</strong> a pakalchi sahkil — a fear-spirit called by <em>greater planar ally</em> to serve as the Gray Maidens' <strong>scar-carver</strong>: every recruit's ritual facial scars are her vinework (E11, the old execution chamber). She breaks the obstinate with venom and domination, and chats with Kordaitra telepathically mid-fight.</p>"
        "<p><strong>Tactics:</strong> vines from reach, fear to scatter, domination to turn the strongest. She attacks intruders on sight and may fall back to E18 when bloodied.</p>",
  folder=F4["a_creatures"], senses=[{"type": "darkvision"}], size="lg", blurb="Sahkil scar-carver of the Maidens", token_src=None))

AW("vyloth", B.npc(A4["vyloth"], "Vyloth", 13, 34, 260, 24, 21, 23, 24,
  {"str": 7, "dex": 4, "con": 5, "int": 3, "wis": 3, "cha": 4}, 35,
  {"deception": 25, "religion": 23, "intimidation": 25, "occultism": 23}, ["fiend", "daemon"], ["common", "daemonic", "infernal"],
  [B.strike(nid(), "Claw", 27, "3d8+11", "slashing", ["agile", "magical", "unholy"], [("2d6", "void")]),
   B.strike(nid(), "Jaws", 27, "3d10+11", "piercing", ["magical"], [("1d6", "bleed")]),
   B.action(nid(), "Consumptive Aura", "passive", "<p>15-ft emanation of gnawing famine: living creatures ending their turn inside take @Damage[2d6[void]] (basic "+chk("type:fortitude|dc:33")+") and on a critical failure are "+B.cond("fatigued", "Fatigued")+".</p>", category="offensive"),
   B.action(nid(), "Horrid Wilting", "3", "<p>Moisture rips from up to five creatures within 120 feet: @Damage[10d8[void]] ("+chk("type:fortitude|dc:33|basic:true")+") — his opener.</p>", ["concentrate", "manipulate", "void", "divine"]),
   B.action(nid(), "Quickened Missiles", "1", "<p>Five unerring force darts (@Damage[1d4+1[force]] each) at the most wounded foe — every round, after the wilting.</p>", ["concentrate", "force", "divine"]),
   B.action(nid(), "Daemonic Resilience", "passive", "<p>Immune to death effects and disease; resistance physical 10 (except holy); teleports to Zenobia's side if her body is destroyed (re-encounter him in E18).</p>", category="defensive"),
   B.lore(nid(), "Lies Lore", 23)],
  notes="<p><strong>Role:</strong> an advanced meladaemon — famine made flesh — granted by Urgathoa to guard Zenobia's helpless daytime body (E8). He finds bodyguarding <em>beneath him</em>, and his boredom is the party's opening: he proposes a question-game first — news of chaos, disease, and famine in the city for answers about the vault. <strong>Every answer he gives is a calculated lie</strong> built to misdirect or despair.</p>"
        "<p><strong>Tactics:</strong> steps into aura range, opens with Horrid Wilting, then quickened missiles at the bloodiest PC; focuses anyone touching Zenobia's body. Fights to the death — unless the body is destroyed, when he relocates to her.</p>",
  folder=F4["a_creatures"], senses=[{"type": "darkvision"}, {"type": "true-seeing"}], size="lg", blurb="Bored famine-daemon bodyguard", token_src=None))

AW("kordaitra-destaid", B.npc(A4["kordaitra"], "Kordaitra Destaid", 10, 30, 190, 21, 16, 16, 17,
  {"str": 5, "dex": 2, "con": 4, "int": 2, "wis": 1, "cha": 3}, 20,
  {"athletics": 21, "intimidation": 19, "society": 18, "deception": 16, "occultism": 14}, ["humanoid", "human"], ["common", "infernal"],
  [B.strike(nid(), "+1 Striking Longsword", 23, "2d8+10", "slashing", ["magical", "versatile-p"]),
   B.strike(nid(), "Steel Gauntlet", 21, "1d6+8", "bludgeoning", ["agile", "free-hand"]),
   B.action(nid(), "Constable's Challenge", "1", "<p>She marks one foe: +2 circumstance damage against it, and it takes −1 to attacks against anyone but her — the Asmodean enforcer's discipline.</p>", ["concentrate"]),
   B.action(nid(), "Break the Will", "2", "<p>A gauntleted Strike followed by an Intimidation Demoralize against the same target at +2 circumstance (her conditioning craft, miniaturized).</p>", ["flourish"]),
   B.action(nid(), "Shield Block", "reaction", "<p>Standard (tower-trained; Hardness 5).</p>"),
   B.lore(nid(), "Asmodean Doctrine Lore", 18),
   B.gear("full-plate", nid()), B.gear("steel-shield", nid()), B.gear("longsword", nid())],
  notes="<p><strong>Role:</strong> the Gray Maidens' de facto second — quartermaster at the Ch.2 muster, ex-knight-enforcer of Asmodeus, author of the Maidens' loyalty-conditioning. She resents Sabina's credit and means to replace her. <strong>Boule's bait:</strong> fake 'Korvosan Revolution' ciphers keep the would-be codebreaker ensconced in her quarters (E21) for at least a week — if she cracks them first, she decamps to Castle Korvosa with the emergency cache.</p>"
        "<p><strong>On the alarm</strong> she relocates to the Nursery (E18) and commands the defense beside Zenobia. Her keys open the vault's cells — including Endrin's.</p>",
  folder=F4["a_creatures"], blurb="Gray Maiden second; Asmodean conditioner", token_src=None, actor_link=True))

# ---- hazards ----
hazards = []
def HW(slug, doc):
    hazards.append(copy.deepcopy(doc)); B.write("hazards", slug, doc, embed_items=True)

HW("eternal-glyphs", B.hazard(A4["eternalglyphs"], "The Eternal Glyphs (A7)", 9, 33,
  "<p>"+chk("type:perception|dc:33")+" (trained) to sense the compulsion woven through the wall-text before reading.</p>",
  "<p>"+chk("type:thievery|dc:33")+" to deface a keystone glyph, or <em>dispel magic</em> (5th rank). Only readers who comprehend <strong>Thassilonian</strong> can be affected at all.</p>",
  "<p>Coded Thassilonian wall-text ("+chk("type:society|dc:30")+" + the language to decipher) that claims to warn of perils — and self-alters so it can never be finished. Ancient Shoanti skeletons (their gear: <strong>+1 hide armor, a +1 striking frost earth breaker, a +1 striking returning totem spear</strong>) died of thirst mid-sentence here.</p>",
  [B.action(nid(), "Compulsion to Read", "reaction", "<p><strong>Trigger</strong> A creature that understands Thassilonian reads the text.</p><hr /><p><strong>Effect</strong> "+chk("type:will|dc:28")+" or the reader is "+B.cond("fascinated", "Fascinated")+" and <strong>cannot stop reading</strong> — a new save each day at a cumulative −2. An unaffected ally can drag a victim free (the victim resists: a successful Athletics check against their Fortitude DC), which ends it instantly. String the player along ('five more minutes… maybe seven hours') before calling for the save.</p>")],
  folder=F4["a_hazards"], traits=["magical", "trap", "mental", "incapacitation"], reset="<p>Automatic — the text rewrites itself.</p>", complex_=False))

HW("dispelling-mist", B.hazard(A4["dispellingmist"], "Dispelling Mist (E3)", 8, 20,
  "<p>"+chk("type:perception|dc:20")+" — the 5-ft wall of glowing pale-yellow fog across the NW tunnel is obvious; its function is not.</p>",
  "<p>"+chk("type:thievery|dc:30")+" to ground the matrix, or <em>dispel magic</em> (4th rank).</p>",
  "<p>A standing fog-ward at the Chokepoint's entrance — the Red Mantis's insurance against buffed intruders.</p>",
  [B.action(nid(), "Strip Magic", "reaction", "<p><strong>Trigger</strong> A creature passes through the fog.</p><hr /><p><strong>Effect</strong> A targeted <em>dispel magic</em> (counteract +17, 4th rank) strikes one active spell effect on the creature — fly, invisibility, and false life are favorite casualties, 60 feet above a spike-floored pit room.</p>")],
  folder=F4["a_hazards"], traits=["magical", "trap"], reset="<p>Automatic.</p>", complex_=False))

# =====================================================================
# JOURNAL — "4. A History of Ashes"
# =====================================================================
SR = lambda area, p: f'<p class="source"><em>Source: CotCT (2016 HC), Ch.4, {area} — p.{p}.</em></p>'
pages = []
def PG(name, html, level=2): pages.append(B.page(nid(), name, html, level=level))
def area4(code, name, html): PG(f"{code}. {name}", html, level=3)
def encx(levels, pl):
    e = B.encounter(levels, party_level=pl); return f"{e['band']} · {e['xp']} XP @ L{pl}"

PG("Chapter Background",
  B.s_milestone("<p><strong>Chapter 4 — A History of Ashes.</strong> The PCs ride into the Cinderlands to win the Shoanti's trust — and the lore of Kazavon. Begin at <strong>L10/11</strong>; reach <strong>12th before the Deathhead Vault</strong>; 13th by chapter's end.</p>")
  + SEC("<p><strong>The history (GM):</strong> centuries ago the blue dragon <strong>Kazavon</strong>, champion of Zon-Kuthon, conquered Belkzen from Castle <strong>Scarwall</strong> — until <strong>Mandraivus</strong> of the Order of the Palatine Eye slew him with the bastard sword <strong><em>Serithtial</em></strong>. The dragon's remains would not be destroyed; seven survivors each carried one relic away in secret. The Shoanti shaman <strong>Amarund</strong> took the fangs — 'Midnight's Teeth' — to the Thassilonian pyramid on Conqueror's Bay… where Korvosa now stands. Her line guarded them for three hundred years. Ileosa found them anyway. And the Shoanti, watching their queen-enemy rise, now sharpen blades for a war that would only feed her.</p>")
  + "<p><strong>NPC developments:</strong> Amin (if escorted out) runs with Cressida's rebels in the Gray District; Pilts (if alive) executes Cerulean Society envoys for sport — Boule may want him dead; Salvator (if rescued) leaves for Nidal with Laori's Brotherhood; if left behind, he dies trying to escape.</p>")

PG("The Road North",
  "<p>The PCs escort Vencarlo and Neolandus out of Korvosa to <strong>Harse</strong>. Cressida's parting kit: a <strong>wand of <em>sending</em></strong> (10 charges), 2 scrolls of <em>dream</em>, and 4 scrolls of <em>teleport</em> for emergency returns (Bishop Keppira d'Bear of Pharasma relays <em>sendings</em> if no PC can).</p>"
  + "<p><strong>Blackbird Ranch:</strong> five minutes north of Harse — Jasan Adriel's spread (ex-adventurer, 'the Blackbirds,' Vencarlo's old comrade). <strong>Trinia Sabor</strong> is here, leveled-up and delighted. After dinner, in the basement, Neolandus gives the full <strong>Kazavon Situation</strong> briefing (the Background above, as he knows it) and Vencarlo asks for the <em>amulet of proof against detection</em> from the Blackjack cache, if found, to hide Neolandus. Jasan outfits the party: trail rations, light warhorses, pack animals — free.</p>"
  + B.s_skill("<p><strong>The Fourth Harrowing</strong> en route: past = Korvosa's founding on stolen ground; present = the PCs as fugitives mirroring the Shoanti exile; future = a city dangerous but topple-able. Foreshadow Cindermaw, the Moon temple, Bolt Rock, and the vault.</p>")
  + SEC("<p><strong>Factions in play all chapter:</strong> the <strong>Brotherhood of Bones</strong> (Shadowcount Sial + a chained kyton join "+act("laoriVaus0000001", "Laori")+" in Kaer Maga; they scry the PCs and won't approach until Scarwall); the <strong>Red Mantis</strong> — "+act(A4["cinnabar"], "Cinnabar")+" runs the hunt from Korvosa via "+act(A4["koriantu"], "Koriantu's")+" <em>sendings</em>, hiring "+act(A4["cinderlander"], "the Cinderlander")+" as guide and buying the "+act(A4["ashwing"], "Ashwing gargoyles")+" with Mediogalti gold. Two scripted ambushes in Part 2; the reckoning in Part 3.</p>"))

PG("The Respect Points Subsystem",
  B.s_milestone("<p><strong>Respect Points (RP)</strong> — the chapter's spine, run as PF2e Victory Points. <strong>20 RP</strong> → Thousand Bones declares the PCs worthy and the Sun Shaman speaks. <strong>−10 RP</strong> → branded enemies of the people; only battle remains. Show the running total; never reveal the target.</p>")
  + "<ul>"
    "<li><strong>Shoanti PCs:</strong> +1 each (once); an exposed impostor (e.g. <em>illusory disguise</em>): −3.</li>"
    "<li><strong>Trophies:</strong> the severed head of a CR-9+ enemy of the Shoanti (great orcs, giants, dragons, the Cinderlander…), presented publicly to an elder within a week: +1 each, <strong>max 10 from trophies</strong> ("+chk("type:society|dc:15")+" or any Shoanti to learn the custom).</li>"
    "<li><strong>Quests:</strong> per their entries (sredna +1–3; Akram +3; Cindermaw +2/+4; the Mark +3; the Trial +1/+1 per totem; Flameford +4; saving Krojun +3; Diplomacy at the Fire +2).</li>"
    "<li><strong>Losses:</strong> dead boneslayers −1d4 each; thundercallers routed and bad-mouthing −1d6; talking the moon maidens out of their fight −2d4; Krojun-rescues-the-party −1d6; refusing sredna −1; killing Cindermaw −1; public disrespect at GM discretion. The total can go negative.</li>"
   "</ul>")

PG("The Kallow Mounds & Krojun",
  "<p>Hundreds of skull-topped cairns ("+chk("type:society|dc:15")+": Skoan-Quah markers) — the three quahs' burial ground for 300 years. ~75 Skull Clan camp here under <strong>Chief One-Life</strong>, the shaman <strong>Ash Dancer</strong>, the wingless dragonne <strong>Wicked-Claws</strong> — and <strong>Thousand Bones</strong>, who remembers Gaekhen. A boneslayer patrol intercepts at half a mile; his name (or Gaekhen's) opens the camp: a guest yurt, water, and a visit to Gaekhen's cairn (he approves if told Rolth was punished).</p>"
  + box("Krojun asks Chief One-Life, 'Why do the",
        "<p>'Why do the dead keep such company?' rumbles the newcomer — a mountain of a man with an earth breaker across his back, eyeing the tshamek guests with open contempt.</p>")
  + SEC("<p><strong>"+act(A4["krojun"], "Krojun Eats-What-He-Kills")+"</strong> arrives bearing the hero Berak's body and bristles at outsiders; Thousand Bones defuses with the funeral. Then the challenge: <strong>sredna</strong> ("+chk("type:society|dc:20")+" recognizes the leather loop; "+chk("type:society|dc:30")+" or ask, for his story). Refusing costs −1 RP. He is secretly <em>testing</em> them: he wants a reason not to march his people into Ileosa's jaws.</p>")
  + B.s_skill("<p><strong>SREDNA</strong> (converted): two contestants on hands and knees, bound head-to-head by a loop. <strong>Rounds 1–3:</strong> opposed Intimidation — winner +2 points, tie +1 each (pulling early disqualifies). <strong>Round 4+:</strong> initiative; each turn <em>Tug</em> (opposed Athletics; the defender who Dug In last round gets +4 circumstance; win +2 points, lose/tie +2 to the foe) or <em>Dig In</em> (+4 vs. the next tug). After each round past the 4th: each contestant attempts a Fortitude save, <strong>DC = the opponent's current points</strong> — fail and collapse (both fail = draw; Endurance-style abilities grant +4). Krojun <strong>rages</strong> if it passes six rounds.</p>")
  + B.s_treasure("<p><strong>RP:</strong> force his rage +1 · lose gamely +1 · draw +2 · win +3. <strong>Story award</strong> for earning 2+ RP from the game, even in defeat.</p>"))

PG("The Bone Council Fire & Skoan-Quah Support",
  box("'You have already done my people a great",
      "<p>'You have already done my people a great kindness,' says Thousand Bones over the council flames. 'But what you ask is not mine to give.'</p>")
  + "<p>Thousand Bones knows 'Kazavon' only as a name of fear: <strong>the lore lives with the Sklar-Quah Sun Shamans</strong>, and the Sun Clan kills tshamek on sight. The council names <strong>five paths to respect</strong>: become "+act(A4["krojun"], "Krojun's")+" <em>nalharest</em> · re-create Skurak's deed in "+act(A4["cindermaw"], "Cindermaw's")+" belly (Handout #4-1) · win Truthspeaker "+act(A4["akram"], "Akram's")+" endorsement · earn the <strong>Thrallkeeper's Mark</strong> at the Acropolis · survive the Sklar-Quah <strong>Trial of the Totem</strong>. ("+chk("type:arcana|dc:30")+" or "+chk("type:society|dc:30")+": the 'Thrallkeeper's Mark' is the <strong>Sihedron rune</strong> of old Thassilon.)</p>"
  + B.s_treasure("<p><strong>Thousand Bones's gifts:</strong> 5 healing potions (moderate), a <strong>wand of create water</strong> (44 charges), a <strong>wand of endure elements</strong> (23), 5 pots of Shoanti war paint — and four "+act(A4["boneslayer"], "boneslayer")+" escorts: <strong>Ahalak, Hargev, Nalmid, Shadfrar</strong> (guides, witnesses, and the party's most fragile asset — see their entry for the RP stakes). In the wastes, "+chk("type:perception|dc:40")+" confirms the distant riders shadowing the party are Krojun's — he evades all confrontation until the Acropolis.</p>"))

# --- Quest A: the Acropolis ---
PG("Quest A: The Acropolis of the Thrallkeepers",
  B.s_milestone("<p><strong>The Acropolis</strong> — a Thassilonian conjuration complex whose masters died summoning the <strong>havero</strong>, 'Arms and Eyes of Forever,' from the Dark Tapestry; the part-summoned horror still hibernates below. Black granite flecked with blood-red crystal; every stone door bears a Sihedron bas-relief (press → it grinds up; descends after a minute; "+chk("type:thievery|dc:15")+" jams one for a month; the closing crush deals @Damage[3d6[bludgeoning]] and pins — "+chk("type:athletics|dc:25")+" to wrench free).</p>")
  + SEC("<p><strong>A crowded dungeon:</strong> 4 "+act(RMA, "Red Mantis assassins")+" enter ~10 minutes behind the PCs ("+act(A4["cinderlander"], "the Cinderlander")+" guided them but waits outside) — their real mission is to let "+act(A4["koriantu"], "Koriantu")+" <em>watch the PCs fight</em> through a scried assassin. And "+act(A4["krojun"], "Krojun")+" + 3 "+act(A4["thundercaller"], "thundercallers")+" arrived an hour <em>before</em>, hiding at the observation gallery (A3) to take the party's measure (he mocks the Mark-quest as 'stargazing' — his laugh adds 2 Noise Points). "+chk("type:diplomacy|dc:31")+" or "+chk("type:intimidation|dc:23")+" brings the Shoanti in against the Mantis early (intimidated, they leave after and bad-mouth). The Shoanti <em>automatically</em> aid against the havero. Save them from certain death and Krojun may declare <strong>nalharest</strong> on the spot.</p>")
  + B.enc("The Mantis tail", encx([9, 9, 9, 9], 11),
     "<p>4 "+act(RMA, "Red Mantis assassins")+" — they strike once discovered (or as the PCs leave, if never engaged). Koriantu is watching; let the players feel it.</p>",
     B.aside_token(["4× "+act(RMA, "Red Mantis Assassin (9)")])))

area4("A1-A3", "Thrallkeeper's Walk, the Pool & the Gallery", SR("A1-A3", 209)
  + box("The air in this massive, cathedral-like space",
        "<p>The air in this cathedral-space lies cold and still over a black pool. Something vast beneath the water looks, at first, like stone — until an eye the size of a shield rolls beneath its lid.</p>")
  + "<p>A1's dust shows tracks ("+chk("type:survival|dc:19")+" follows them to the A2/A3 door). <strong>A2, Pool of the Havero:</strong> a 60-ft vault over a 15-ft pool floored with the sleeping horror's rubbery flank — the bottom is dimensionally adjacent to a thing orbiting a dead star.</p>"
  + B.s_skill("<p><strong>NOISE POINTS</strong> (track openly): verbal spell +1 · running +1/runner · yell +1 · <strong>combat +5/round</strong> · sonic effect +10 · damaging the flank +1/point. Noise <em>in A2</em> doubles. The total <strong>decays 1d10/minute</strong>. Thresholds (trigger the round after): <strong>10</strong> Twitch · <strong>20</strong> Investigate (1 "+act(A4["havtentacle"], "tentacle")+") · <strong>~30</strong> Seek · <strong>40</strong> Assault (2) · <strong>50</strong> Wrath (4, the max). Each slain tentacle −1d20 noise; below 10, all retract (quelled 1 hour). 20+ tentacles slain in one fight also quells it. <strong>Story award</strong> for crossing without waking it — or for quelling it once woken.</p>")
  + B.enc("Tentacle Wrath (worst case)", encx([9, 9, 9, 9], 11),
     "<p>4 "+act(A4["havtentacle"], "havero tentacles")+" at 60-ft reach, attackable anywhere along their lengths. The Mantis <em>watch</em>; the Shoanti help.</p>",
     B.aside_token(["≤4× "+act(A4["havtentacle"], "Havero Tentacle (9)")])))

area4("A4-A7", "Shrines, the Illumacore & the Eternal Glyphs", SR("A4-A7", 211)
  + "<p><strong>A4:</strong> a six-winged serpent-woman shrine ("+chk("type:religion|dc:25")+": <strong>Kurshu the Undying</strong>, Lissala's herald) — sapphire and emerald slivers in the tail, ~320 gp re-scaled (the thundercallers hoot at it: +2 Noise). <strong>A5, the Illumacore:</strong> a rune-ringed shaft of emerald light ("+chk("type:arcana|dc:26")+" to deduce): step in → <em>feather fall</em> 70 ft down to A9; cross the lower ring → <em>levitate</em> back up. Krojun goes first, to show off. <strong>A6:</strong> a bronze Lissala statue — her jade whip is a <strong>+2 axiomatic whip</strong>, cursed (1 Wisdom drain/day of visions; −6 Will saves while Thassilonian writing is visible; lifts only re-handed to the statue or <em>remove curse</em> vs. 18th). The base-drawer frame ("+chk("type:thievery|dc:20")+") projects the original acropolis map on the ceiling via the illumacore.</p>"
  + "<p><strong>A7:</strong> the "+haz(A4["eternalglyphs"], "Eternal Glyphs")+" — and the gear of the Shoanti dead who starved reading (+1 hide, a <strong>+1 striking frost earth breaker</strong>, a <strong>+1 striking returning totem spear</strong>). If Krojun must drag the party out: <strong>−1d6 RP</strong>.</p>")

area4("A8-A11", "The Lower Level & the Golarion Globe", SR("A8-A11", 213)
  + box("A jumble of five crushed humanoid skeletons lie",
        "<p>Five crushed skeletons lie in a sealed vault, their finery intact — the Thrallkeepers' panic room, which saved them from nothing at all.</p>")
  + "<p><strong>A9:</strong> beyond the havero's reach (the Mantis love an ambush at the illumacore landing). A 120-ton stone plug ("+chk("type:perception|dc:22")+") hides <strong>A10, the Fallback Vault</strong> (gaseous-form gap): the five dead Thrallkeepers' gear — a <strong>bottle of air</strong>, <strong>decanter of endless water</strong>, <strong>sustaining spoon</strong>, scrolls (2× <em>clairvoyance</em>, 2× <em>sending</em>, 2× <em>dimension door</em>), a <strong>+1 striking magical-beast-bane dagger</strong>, a bright-orange <strong>cloak of resistance +3</strong> (greater resilient rune), a <strong>scabbard of keen edges</strong>, and ~700 gp re-scaled in jewelry and a Lissalan holy symbol.</p>"
  + SEC("<p><strong>A11, the Golarion Globe:</strong> a hollow 10-ft stone globe of the pre-Earthfall world ("+chk("type:society|dc:20")+") floating on <strong>three immovable rods</strong>. Touch it and contemplate the <em>stars</em> → drawn inside into suspended animation and space-visions ("+chk("type:will|dc:15")+" per minute or 1d4 Intelligence drain; concentrate on Golarion to exit; auto-ejected at Int 0). Exit grants the <strong>THRALLKEEPER'S MARK</strong> (one palm, one week, once per year): right palm = <em>banishment</em> 1/day; left = <em>summon</em> (5th rank) 1/day; either grants +4 status vs. mental. Pulling a rod drops the globe (+10 Noise; it cracks — 1d4 more weeks of function). <strong>+3 RP</strong> for gaining the Mark before Shoanti eyes; <strong>story award</strong> if any PC gains it.</p>"))

# --- Quest B / C ---
PG("Quest B: The House of the Moon",
  box("A silvery stone shrine stands atop a low",
      "<p>A silvery shrine stands atop a low rise, its walls faintly luminous even by day — and its threshold dark with old blood.</p>")
  + "<p>Thousand Bones's pointer: Truthspeaker <strong>Akram</strong> arrives with the Lyrune-Quah in days — but a <strong>red reaver</strong> has taken the shrine, eating a dozen moon maidens and their commander. <strong>Tekrakai's</strong> surviving band of four ("+chk("type:diplomacy|dc:30")+" or "+chk("type:intimidation|dc:23")+" to bench them — but doing so costs <strong>−2d4 RP</strong>) wants it dead; her briefing is exact: rending claws, a discord-roar, <strong>distracted by artistic beauty</strong>, never sleeps.</p>"
  + B.enc("The Red Reaver", encx([13], 11),
     "<p>"+act(A4["redreaver"], "the Red Reaver")+" (at ~85% HP from old wounds) in the moonlit hall — walls of self-repairing blessed masonry (Hardness 16; SR vs. manipulation). It targets the heaviest armor, pursues half a mile, fights to the death. A performance ("+chk("type:performance|dc:31")+") buys calm rounds. <strong>Story award</strong> per surviving maiden.</p>",
     B.aside_token([act(A4["redreaver"], "Red Reaver (13)"), "4× "+act(A4["moonmaiden"], "Moon Maiden (6, allies)")]))
  + B.s_treasure("<p>Among the seven dead maidens: 3× +1 hide armor and 5× <strong>+1 starknives</strong> (the Lyrune-Quah gift them to helpers). The shrine itself: Desnan sleepers receive a yearly dream-<em>commune</em> from the avoral <strong>Nightspear</strong>; the sky-well projects the true night sky at all hours.</p>")
  + SEC("<p><strong>After:</strong> the tribe arrives; <strong>"+act(A4["akram"], "Akram")+"</strong> agrees to travel as witness (<strong>+3 RP</strong>, story award; second award if he lives to the Sun Shaman's tale). He is 68 and frail; honor forbids him an escort. Keep. Him. Alive.</p>"))

PG("Quest C: The Belly of the Beast (Cindermaw)",
  box("Skurak was a great warrior and greater traitor",
      "<p><strong>Skurak's Tale (Handout #4-1):</strong> Skurak, great warrior and greater traitor, dove into the Clan-Eater's gullet armed with a single knife — and cut his way back into the world, reborn.</p>")
  + "<p>The deed: <strong>one PC swallowed by "+act(A4["cindermaw"], "Cindermaw")+" and out again, before Shoanti witnesses.</strong> The method is irrelevant — cut free (Rupture 30; fire resistance advised), <em>teleport</em> from the belly (concentration inside), even <em>charm</em>. Tempting a swallow: Deception at −2 vs. its Sense Motive. An illusion of the deed must beat the witnesses' saves <em>and radiate heat</em>. Hunt it near the western cindercones; it finds loiterers — stage its spark-gout surfacings first.</p>"
  + B.enc("Cindermaw (do not slay)", encx([14], 11),
     "<p>"+act(A4["cindermaw"], "Cindermaw")+" — Severe+ if fought honestly, which is the wrong lesson: <strong>killing it costs RP</strong> (a dead god 'wasn't that tough'). +2 RP for the deed; <strong>+4 if the worm lives</strong>.</p>",
     B.aside_token([act(A4["cindermaw"], "Cindermaw (14)")])))


# --- Quest D: Flameford ---
PG("Quest D: Flameford & the Trial of the Totem",
  B.s_milestone("<p><strong>Flameford</strong> — 52 Sklar-Quah on a cliff-edge behind permanent <em>spike stones</em> fields ("+chk("type:perception|dc:29")+" per square; hidden zigzag paths), under <strong>Chief Ready-Klar</strong> (Krojun's uncle) and the nameless <strong>Sun Shaman</strong>. A six-rider burn-rider patrol laughs at the PCs' goal but escorts them in, armed.</p>")
  + "<p><strong>At the Foot of the Fire:</strong> the whole camp gathers; "+chk("type:diplomacy|dc:29")+" mollifies the chieftain (+10 circumstance with "+act(A4["akram"], "Akram")+"; "+chk("type:intimidation|dc:24")+" works instead) — <strong>+2 RP</strong>. At 20 RP, skip to the Assault; under it, the Sun Shaman grants the <strong>Trial of the Totem</strong> (Krojun storms off on a long ride). Mentioning Kazavon makes the old man <em>pale</em> and refuse. Akram departs before the Sklar-Quah dawn, advising: <em>win Krojun</em>.</p>"
  + B.s_skill("<p><strong>THE TRIAL:</strong> haul fired-clay sun totems (10 ft, 500 lbs; Hardness 6, HP 40) up <strong>Bolt Rock</strong> — to the 30-ft tier by day one, the 40-ft mesa by day two, each kept <em>standing</em> through its day; the third dawn crowns success. Teamwork legal; no food or water provided (bring your own; <em>endure elements</em> and <em>create food</em> are fair); <strong>altering totem or rock is cheating</strong> — the Sun Shaman inspects ("+chk("type:survival|dc:20")+" per alteration to hide; 3+ immovable rods leave no trace). Steadying: "+chk("type:athletics|dc:12")+" every 6 hours; a failure leans the totem ("+chk("type:athletics|dc:16")+" to catch); a second topples it (@Damage[3d6[bludgeoning]] to the totem — shattered = that PC is out). Day two without sleep: "+B.cond("fatigued", "Fatigued")+"; run heat and thirst by the environment rules.</p>")
  + SEC("<p><strong>The Sun Vision:</strong> each hour fatigued, 10% cumulative chance (+30%/hour exhausted) of the aurochs-vision — two easy Wisdom-flavored insights: <em>she is the aurochs… and she is not prey</em>. A PC who completes it gains <strong>+1 insight to attack and damage vs. the Red Mantis and their minions</strong> for the chapter. The message: stop waiting. Turn and face them.</p>")
  + B.enc("Hungry Visitors (day 2, exhausted)", encx([8] * 6, 11),
     "<p>6 "+B.mon("bulette", "bulettes")+" leap the lower tier (2d4 rounds of burrowing warning). Fighting one-handed on a totem: -2 to attacks; a bulette passing a totem forces "+chk("type:athletics|dc:15")+" or it topples; misses by 3 or less against a holder strike the totem half the time. <strong>Dropping a totem on a bulette:</strong> @Damage[3d6[bludgeoning]] ("+chk("type:reflex|dc:15")+" avoids) — and the totem takes the same.</p>",
     B.aside_token(["6× "+B.mon("bulette", "Bulette (8)")]))
  + B.s_treasure("<p><strong>The Third Dawn:</strong> the tribe ascends pre-dawn; one standing totem makes the whole party Sklar-Quah-accepted (its keeper a citizen; the rest honored nalharests). The Sun Shaman casts <em>lesser restoration</em> on each PC. <strong>+1 RP</strong> for the attempt, <strong>+1 per totem</strong> that never toppled; <strong>story award</strong> if at least one stood. Krojun, returned and calmed, watches day two from the rocks and grudgingly calls the PCs lucky in their nalharests.</p>"))

PG("The Flameford Assault & Saving Krojun",
  B.s_milestone("<p><strong>The Assault</strong> triggers at 20 RP: the Sun Shaman must first commune at the Kallow Mounds (<em>wind walk</em>, back in a day; Krojun commands). At dusk the "+act(A4["ashwing"], "Ashwings")+" lift the Red Mantis over the spike-fields and drop them among the yurts.</p>")
  + B.enc("The Assault", encx([9, 9, 9, 6, 6, 6], 11),
     "<p><strong>If the vault still stands / PCs L11:</strong> 3 "+act(RMA, "Red Mantis assassins")+" + 3 "+act(A4["ashwing"], "Ashwing gargoyles")+". <strong>If the hideout fell first / PCs L12:</strong> double it (6+6 — "+encx([9]*6+[6]*6, 12)+"), adding "+act(A4["cinnabar"], "Cinnabar")+" if she escaped with a grudge. The lead assassin names the PCs and offers the Shoanti peace for their heads: <strong>with 5+ RP the Shoanti refuse</strong>; with 4 or fewer they stand aside and the PCs face the <em>full</em> force (6 assassins, the Cinderlander, two dozen gargoyles). The tribal battle runs offstage: if the PCs win their fight, most Shoanti live. <strong>+4 RP</strong> for breaking the assault.</p>",
     B.aside_token(["3-6× "+act(RMA, "Red Mantis Assassin (9)"), "3-6× "+act(A4["ashwing"], "Ashwing Gargoyle (6)")]))
  + SEC("<p><strong>Saving Krojun:</strong> the "+act(A4["cinderlander"], "Cinderlander's")+" price for guiding the Mantis was <em>Krojun</em>. As the PCs finish their fight, the duel still rages — "+act(A4["krojun"], "Krojun")+" at ~30 HP against the hunter's ~100 ("+encx([12], 11)+"). Unaided, Krojun dies and the killer walks. Intervene: the Cinderlander flees below ~20 HP; Krojun, saved, declares the PCs <strong>nalharest</strong> — <strong>+3 RP</strong> and a story award equal to his own defeat. The aftermath is a victory feast: sredna rematches, Sklar-Quah tattoos, a marriage offer contingent on shaving a PC's head.</p>")
  + B.s_conv("<p>If the PCs fall, the Shoanti are wiped out — the merciful out: survivors wake stripped and imprisoned in the Deathhead Vault, which conveniently is where Part 3 goes anyway.</p>"))

# --- Part 3: Mantis and Maiden ---
PG("Part 3: Mantis and Maiden",
  B.s_milestone("<p><strong>Part 3</strong> — Korvosa, meanwhile: the Sable Company disbanded, the Hellknights withdrawn, the Guard gutted; Abadar's archbanker and the Asmodeans back the queen (seeding schism among young clergy); only Pharasma's church quietly resists; the Red Mantis kill notables in daylight; Ileosa's endgame — <em>thousands sacrificed for eternal youth</em> — gathers. <strong>Do not start before L12.</strong> Keppira d'Bear's <em>sending</em> recalls the PCs: <em>'Return to Korvosa! An opportunity to strike at the heart of the queen's power…'</em></p>")
  + SEC("<p><strong>An Unexpected Opportunity:</strong> the rebel HQ is the old Dead Warrens ossuary (Ch.1!), warded and password-keyed ('<strong>Blackjack</strong>'). Guildmaster <strong>Boule</strong> of the Cerulean Society ("+chk("type:society|dc:20")+") wants the D16 Arkona papers — offering <strong>600 pp per PC</strong> ("+chk("type:diplomacy|dc:25")+" raises it to 900; <strong>story award</strong> for brokering <em>favors</em> instead of coin, Kroft's preference). His intel: the Society's old derro-tunnel back door into the <strong>Deathhead Vault</strong> beneath the Longacre Building — now Red Mantis + Gray Maiden territory. His extras: a <strong>partial key</strong>, directions (+20 circumstance to the E1/E2, E6, and E9 secret doors) — and fake 'Revolution ciphers' leaked to "+act(A4["kordaitra"], "Kordaitra")+", nailing the would-be codebreaker to her quarters for a week.</p>")
  + "<p><strong>Objectives</strong> (Kroft): rescue <strong>Marcus Endrin</strong> · recover the records · learn why Arbiter <strong>Zenobia</strong> sided with the queen · break the Red Mantis and Gray Maiden leadership. Doors: stone in the west (E1-E9: Hardness 8, HP 60), locked reinforced wood in the Vault proper (E10-E21: "+chk("type:thievery|dc:40")+" or carried keys).</p>")

area4("E1-E4", "The Red Mantis Caverns", SR("E1-E4", 237)
  + box("A ten-foot-wide trough of murky water fills",
        "<p>A ten-foot-wide trough of murky water fills the sewer's heart; the 'rust' on the great gate is paint, and something vast and pale stirs in the dark beyond.</p>")
  + B.enc("E1 — Snagglebreath", encx([12], 12),
     "<p>An albino "+B.mon("catoblepas", "catoblepas")+" — Cinnabar's imported pet ("+chk("type:perception|dc:15")+" spots the painted rust; its mithral-spiked collar, engraved 'Snagglebreath,' ~100 gp re-scaled). It loves Red Mantis colors and savages everyone else. The secret door beyond: "+chk("type:perception|dc:40")+" (+20 with Boule's directions).</p>",
     B.aside_token([B.mon("catoblepas", "Catoblepas (12)")]))
  + B.enc("E2 — the 'Sewer Brewer'", encx([7], 12),
     "<p>"+B.mon("greater-barghest", "Mogmora")+" (an Elite greater barghest in goblin form), planar-bound bartender of a dressed-up tavern, offering free ale <strong>poisoned with lich dust</strong> (party-size + 4 doses behind the bar). He stalls 1d4 rounds cataloguing the party, then feigns terror and <em>dimension doors</em> to E6 to report.</p>",
     B.aside_token([B.mon("greater-barghest", "Mogmora (7, Elite)")]))
  + B.enc("E3 — the Chokepoint", encx([9, 9, 9], 12),
     "<p>The "+haz(A4["dispellingmist"], "Dispelling Mist")+" at the entry; a 60-ft pit bridged by a <em>permanent-image</em> plank ("+chk("type:will|dc:17")+" on interaction); cytillesh patches ("+B.cond("stupefied", "Stupefied")+" creep within 20 ft per day); and 2 "+act(A4["manananggal"], "manananggals")+" — the late Sable officers Banzul and Wevenner — plus a hidden "+act(RMA, "Red Mantis assassin")+" who watches two rounds, then slips to E4 to report. Their torsos lie in E8: destroy those to end them at dawn.</p>",
     B.aside_token([haz(A4["dispellingmist"], "Dispelling Mist (8)"), "2× "+act(A4["manananggal"], "Manananggal (9)"), act(RMA, "Red Mantis Assassin (9)")]))
  + B.enc("E4 — the Temple of Achaekek", encx([9, 9, 8], 12),
     "<p>A crescent cathedral-cavern (the mantis façade is fresh <em>stone shape</em>, "+chk("type:arcana|dc:28")+"; "+chk("type:religion|dc:15")+" names <strong>Achaekek</strong>). 2 resting "+act(RMA, "assassins")+" + the mercy-bought "+act(A4["cytillipede"], "cytillipede")+", whose flash is timed for maximum coverage. If the alarm is up, everything that fled converges here, with "+act(A4["cinnabar"], "Cinnabar")+" and "+act(A4["koriantu"], "Koriantu")+" behind ("+encx([13, 13, 9, 9, 9, 8], 12)+" — the vault's worst case).</p>",
     B.aside_token(["2× "+act(RMA, "Red Mantis Assassin (9)"), act(A4["cytillipede"], "Cytillipede (8)")])))

area4("E5-E6", "Cinnabar & Koriantu", SR("E5-E6", 242)
  + box("Three large stone vats sit in alcoves",
        "<p>Three great stone vats sit in alcoves, blue-crusted and empty; beside a soldier's cot, a writing desk holds prayers, anatomies — and something hidden.</p>")
  + B.enc("E5 — Cinnabar", encx([13], 12),
     "<p>"+act(A4["cinnabar"], "Cinnabar")+" in her spartan chambers — masked, mantis-formed, summoning. <strong>Read her morale before running this:</strong> the kneeling surrender at ~10 HP is a genuine fork in the campaign. "+chk("type:perception|dc:25")+" at the desk finds a crimson parchment under <em>secret page</em> — speak '<strong>Kayltanya</strong>' to reveal <strong>Handout #4-2</strong>, the Mistress's letter binding the Mantis contract to the Crown.</p>",
     B.aside_token([act(A4["cinnabar"], "Cinnabar (13)")]))
  + B.enc("E6 — the Inner Sanctum", encx([13], 12),
     "<p>"+act(A4["koriantu"], "Koriantu")+" behind her <em>screen</em>-illusion of slaughter-murals and a towering mantis idol ("+chk("type:will|dc:32")+" on interaction; only the pillars are real). Blade barrier, void, and zero personal stake in the PCs — she came to document Cinnabar's failure. South secret door: "+chk("type:perception|dc:40")+" (+20 from Boule).</p>",
     B.aside_token([act(A4["koriantu"], "Koriantu (13)")])))

area4("E7-E11", "Crypts, the Daemon & the Mother of Thorns", SR("E7-E11", 245)
  + box("The walls of this large room bear",
        "<p>The walls bear carved Cinderlands vistas meant to soothe the honored dead — and the room now smells of rank vinegar and old blood.</p>")
  + "<p><strong>E7:</strong> looted Shoanti sarcophagi ("+chk("type:society|dc:25")+"), once derro cages. <strong>E8, Zenobia's Crypt:</strong> by night her headless body lies in the west sarcophagus and the manananggals' torsos in the others ("+chk("type:religion|dc:27")+": destroying torsos destroys their owners; destroying <em>Zenobia's</em> body only ends her living masquerade).</p>"
  + B.enc("E8 — Vyloth", encx([13], 12),
     "<p>"+act(A4["vyloth"], "Vyloth")+", the bored famine-daemon, opens with his lying question-game — then Horrid Wilting. If the body is destroyed he teleports to Zenobia (E18) and is fought there instead.</p>",
     B.aside_token([act(A4["vyloth"], "Vyloth (13)")]))
  + "<p><strong>E9:</strong> the Society's secret stair ("+chk("type:perception|dc:40")+", +20 from Boule). <strong>E10:</strong> the Final Walk — the condemned's glowing ivory corridor, its woven <em>calm emotions</em> long disarmed.</p>"
  + B.enc("E11 — the Mother of Thorns", encx([13], 12),
     "<p>The old execution chamber, now the scar-carving room: "+act(A4["motherthorns"], "the Mother of Thorns")+" attacks on sight — vines at 15 feet, fear to scatter, domination for the strongest — narrating to Kordaitra telepathically all the while.</p>",
     B.aside_token([act(A4["motherthorns"], "Mother of Thorns (13)")])))

area4("E12-E21", "The Gray Maiden Dungeons", SR("E12-E21", 248)
  + box("This grim chamber is outfitted with",
        "<p>This grim chamber is outfitted with rack, cage, stockade, and screw — and, on the table, a young woman mid-'lesson,' her tutor's head floating free of its body on a fan of glistening entrails.</p>")
  + "<p><strong>E12</strong> observation office (secret doors "+chk("type:perception|dc:30")+"). <strong>E13:</strong> 12 imprisoned <strong>recruits</strong> who refused the Maidens (cells: Boule's or Kordaitra's keys, or "+chk("type:thievery|dc:40")+") — <strong>story award per woman freed</strong> (15 total with E18's three). <strong>E14, the secret cell:</strong> "+act(A4["endrin"], "Marcus Endrin")+" — see his entry; the E20 records reveal the door. <strong>E15/E16:</strong> the "+act(A4["gmguard"], "guard")+" posts (4 + 4 resting — ~5 minutes to armor up). <strong>E17:</strong> "+act(A4["tisharue"], "Tisharue")+", her heirloom <strong>+2 resilient mithral chain</strong>, and her dossier concluding <strong>Sabina Merrin was barely conditioned</strong>. <strong>E19:</strong> Vavana Dhatri's empty room (reassigned to the castle — a Ch.6 thread). <strong>E20:</strong> the <strong>records</strong> — every woman taken, every 'traitor' executed, and Endrin's cell — <strong>story award</strong>. <strong>E21:</strong> "+act(A4["kordaitra"], "Kordaitra")+" at her ciphers, the 'Sinister Sister' painting (~450 gp), and the emergency cache: a <strong>bag of holding IV</strong> of potions, <em>dust of disappearance</em>, a <strong>wand of cure critical wounds</strong>, and scrolls of <em>break enchantment, heal, limited wish,</em> and <em>resurrection</em>.</p>"
  + B.enc("E18 — the Maiden's Nursery (climax)", encx([11, 6, 6, 6, 6, 6], 12),
     "<p>"+act(A4["zenobia"], "Zenobia")+" mid-indoctrination behind a 5-"+act(A4["gmguard"], "guard")+" watch post; <strong>on the alarm "+act(A4["kordaitra"], "Kordaitra")+" relocates here</strong> ("+encx([11, 10, 6, 6, 6, 6, 6], 12)+"), and the Mother of Thorns or Vyloth may fall back per their morale. The vault's true boss-pile — thin it before it stacks.</p>",
     B.aside_token([act(A4["zenobia"], "Zenobia (11)"), act(A4["kordaitra"], "Kordaitra (10)"), "5× "+act(A4["gmguard"], "Gray Maiden Guard (6)")])))

PG("Chapter Conclusion",
  B.s_milestone("<p><strong>Bolstering the Rebellion:</strong> the vault broken, the Red Mantis quit Korvosa (returning only with Mistress <strong>Kayltanya</strong> in Ch.6), the Maidens fall back to the castle, <strong>martial law ends</strong> — run Korvosa as <em>Unrest</em> hereafter, and let the Epidemic Clock ease accordingly.</p>")
  + box("Many hundreds of years ago, a",
        "<p>'Many hundreds of years ago,' the Sun Shaman begins, firelight in the seams of his face, 'a wound was cut into the world at Scarwall — and my foremother carried a piece of it here, that it might sleep forever…'</p>")
  + SEC("<p><strong>The Sun Shaman's Tale</strong> (at 20 RP): Mandraivus's seven survivors; Amarund's fangs in the pyramid beneath what is now Korvosa; the <em>seeds</em> of Kazavon's soul — Ileosa carries <strong>two souls</strong>, and while the second ripens she commands her own mortality (he nods grimly at news of the failed assassination). The counterstroke sleeps at <strong>Scarwall</strong> in Belkzen, where <em>Serithtial</em> waits among the chained dead. Chapter 5's road.</p>")
  + SEC("<p><strong>The Blessing of the Ancestors</strong> (Bolt Rock, two hours before dawn; the conduit is <strong>Zellara</strong> — her deck-bearer feels the empathic wave): the spirit greets the PCs by name, offers the <strong>fifth Harrowing</strong>, and sings the Spirit's Song (Handout #4-3). <strong>Boons:</strong> each PC infuses one owned weapon (<em>undead-bane</em>) or armor/shield (<em>ghost touch</em>) — <strong>functioning only within Castle Scarwall</strong> — and gains <strong>Infused Soul</strong>: the next failed save vs. a death effect is negated instead ("+B.cond("stunned", "Stunned 1")+" for a round; once, works anywhere). Ready-Klar proclaims the PCs Friends of the Sun.</p>"))

journal = B.journal_entry(JID4, "4. A History of Ashes", pages, folder=ADV_FOLDER)
B.write("journals", "04-a-history-of-ashes", copy.deepcopy(journal), embed_pages=True)
print(f"Chapter 4 built: {len(folders)} folders, {len(actors)} actors, {len(hazards)} hazards, 1 journal ({len(pages)} pages).")
