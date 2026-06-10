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
      "physician": "queensPhysician1", "silteel": "siltEel000000001", "yvicca": "yviccaSeaHag0001"}
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
    return B.s_read("<p>" + t + "</p>") if t else B.s_read(fallback_html)
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

journal = B.journal_entry(JID2, "2. Seven Days to the Grave", pages, folder=ADV_FOLDER)
B.write("journals", "02-seven-days-to-the-grave", copy.deepcopy(journal), embed_pages=True)

print(f"Chapter 2 (front matter) built: {len(folders)} folders, {len(actors)} actors, 1 journal ({len(pages)} pages).")
