#!/usr/bin/env python3
"""Chapter 6 — Crown of Fangs. Party L15 -> 17. The finale:
the rebellion, the assault on Castle Korvosa (A1-A95), and the Sunken Queen
(B1-B20) — Ileosa at the Everdawn Pool, and the Rise of the Dragon."""
from __future__ import annotations
import copy
import pf2e_build as B

MODID = "cotct-pf2e-conversion"
ACTOR_ROOT, ADV_FOLDER = "cotctActorRoot01", "cotctAdvFolder01"

JID6 = "ch6CrownOfFangs1"
A6 = {"yzahnum": "yzahnumEfreeti01", "sabina": "sabinaMerrin0001", "palaceguard": "gmPalaceGuard001",
      "yallop": "yallopSister0001", "togomor": "togomorBloatmg01", "sermignatto": "sermignattoDvl01",
      "venster": "vensterArabast01", "mavrokeras": "mavrokerasDrak01", "kayltanya": "kayltanyaRedM001",
      "boggardchamp": "boggardChamp0001", "ithier": "ithierGylou00001", "fury": "ileosasFury00001",
      "falseileosa": "falseIleosa00001", "ichor": "immortalIchor001", "taniniver": "taniniverKaz0001",
      "ileosa": "queenIleosa00001", "soulgem": "soultrapGem00001"}
F6 = {"a_ch6": "ch6ActorFolder01", "a_creatures": "ch6CreaturesFld1", "a_hazards": "ch6HazardsFld001"}

ids = B._idgen(660006)
def nid(): return next(ids)
sids = B._idgen(886006)
def sid(): return next(sids)

def act(_id, label): return f"@UUID[Compendium.{MODID}.cotct-actors.Actor.{_id}]{{{label}}}"
def haz(_id, label): return f"@UUID[Compendium.{MODID}.cotct-hazards.Actor.{_id}]{{{label}}}"
def chk(s): return f"@Check[{s}]"
def SEC(html): return B.s_secret(html, sid())
def box(anchor, fb):
    t = B.verbatim(anchor)
    return B.s_read(B.parafy(t)) if t else B.s_read(fb)
CHC = "#8a1a1a"

for f in [B.folder(F6["a_ch6"], "6. Crown of Fangs", "Actor", ACTOR_ROOT, 600000, CHC),
          B.folder(F6["a_creatures"], "Creatures", "Actor", F6["a_ch6"], 100000, None, "a"),
          B.folder(F6["a_hazards"], "Hazards", "Actor", F6["a_ch6"], 200000, None, "a")]:
    B.write("actors", "_folder_ch6-" + f["name"].lower().replace(" ", "-").replace(".", "") + "-act", copy.deepcopy(f))

# mirror the folder chain into the hazards pack (per-pack folder docs)
for hf in [B.folder(F6["a_ch6"], "6. Crown of Fangs", "Actor", ACTOR_ROOT, 600000, CHC),
           B.folder(F6["a_hazards"], "Hazards", "Actor", F6["a_ch6"], 200000, None, "a")]:
    B.write("hazards", "_folder_hz6-" + hf["name"].lower().replace(" ", "-").replace(".", ""), copy.deepcopy(hf))

actors = []
def AW(slug, doc):
    actors.append(copy.deepcopy(doc)); B.write("actors", slug, doc, embed_items=True)

AW("yzahnum-trifaccia", B.npc(A6["yzahnum"], "Yzahnum ('Trifaccia')", 15, 37, 300, 27, 25, 24, 26,
  {"str": 7, "dex": 5, "con": 5, "int": 2, "wis": 2, "cha": 6}, 30,
  {"deception": 29, "performance": 27, "acrobatics": 27, "intimidation": 27}, ["fiend", "genie", "fire"], ["common", "ignan", "infernal"],
  [B.strike(nid(), "Golden Flaming Scimitar", 30, "3d6+13", "slashing", ["forceful", "magical", "sweep"], [("2d6", "fire")]),
   B.action(nid(), "Hostile Wish", "2", "<p><strong>Frequency</strong> 3 per scene, only while hidden (a thug 'wishes' aloud; the magic has no visible source). Pick one: <em>'Go to Hell'</em> — "+chk("type:will|dc:32")+" or banished to Hell (incapacitation; returns in 1 day); <em>'Be a pig'</em> — "+chk("type:fortitude|dc:32")+" or baleful polymorph 1 hour; <em>'Drop dead'</em> — "+chk("type:fortitude|dc:32")+" or @Damage[100[void]] (death).</p>", ["concentrate", "divine", "incapacitation"]),
   B.action(nid(), "Scorching Wall", "2", "<p>True form: <em>scorching ray</em> (spell attack +29, @Damage[8d6[fire]]) or a 60-ft <em>wall of fire</em> (@Damage[6d6[fire]]).</p>", ["fire", "divine"]),
   B.action(nid(), "Shrink the Mighty", "2", "<p>"+chk("type:fortitude|dc:35")+" or one foe shrinks a size ("+B.cond("clumsy", "Clumsy 1")+", weapon dice down a step) for 1 minute.</p>", ["divine", "polymorph"]),
   B.action(nid(), "Genie's Resilience", "passive", "<p>Fire immunity; fly 50; <em>invisibility</em> at will (his exit at ~50 HP — his bargain with Ileosa forbids plane shift).</p>", category="defensive")],
  notes="<p><strong>Role (EVENT 1):</strong> the efreeti who forged the Gray Maidens' arms, restaged as <strong>'Trifaccia,'</strong> a brass-masked 'hero' whose paid 'rebels' (a dozen L3 charlatans) rob citizens for him to save — propaganda against the real rebellion. He corners the PCs publicly, grants three hostile 'wishes' from hiding, then duels for the city's eyes. <strong>Exposing his true nature destroys the persona</strong> (+1 Rebellion Point); at ~half HP he reverts (flight, fire, shrinking); at ~50 HP he flees invisible to the castle (re-encounter him there).</p>",
  folder=F6["a_creatures"], senses=[{"type": "darkvision"}], size="lg",
  other_speeds=[{"type": "fly", "value": 50}], blurb="Efreeti propagandist 'Trifaccia' (Event 1)", token_src=None, actor_link=True))

AW("sabina-merrin", B.npc(A6["sabina"], "Sabina Merrin", 14, 35, 270, 25, 22, 21, 23,
  {"str": 6, "dex": 4, "con": 4, "int": 1, "wis": 2, "cha": 4}, 25,
  {"athletics": 27, "intimidation": 25, "nature": 22, "diplomacy": 22, "acrobatics": 24}, ["humanoid", "human"], ["common"],
  [B.strike(nid(), "+2 Greater Striking Longsword", 29, "3d8+12", "slashing", ["magical", "versatile-p"]),
   B.action(nid(), "Perfect Riposte", "reaction", "<p><strong>Trigger</strong> A foe in reach critically fails a Strike.</p><hr /><p><strong>Effect</strong> A Longsword Strike — Vencarlo's best student but one.</p>"),
   B.action(nid(), "Sabotage the Saddle", "1", "<p>Mounted: "+chk("type:nature|dc:25")+" to 'mis-ride' Zarmangarof — the dragon is "+B.cond("off-guard", "Off-Guard")+" and takes −2 to attacks for 1 round (the dragon's Perception vs. her check notices the treachery).</p>", ["concentrate"]),
   B.action(nid(), "Gray General's Word", "1", "<p>City Gray Maidens within 60 feet who hear her: "+chk("type:will|dc:34")+" at −2 or stand down 1 round — they were hers before they were Ileosa's.</p>", ["auditory", "emotion", "linguistic", "mental"]),
   B.gear("full-plate", nid()), B.gear("longsword", nid())],
  notes="<p><strong>Role (EVENT 2):</strong> the queen's general and lover — long disillusioned (Trinia, the conditioning, the plague, the devils), secretly softening the Maidens' cruelty. Her gambit: fly <strong>Zarmangarof</strong> (the charmed black dragon — link "+B.mon("black-dragon-ancient", "Black Dragon (Ancient)")+", run at CR-15 weight) over the city to bait the PCs, sabotage the beast from the saddle, and <strong>fight it beside them when it turns on her</strong>. After: she casts down her sword, bares her face, confesses everything, and asks for redemption — castle intelligence, and the city Maidens rallied to the rebellion. <strong>She never attacks the PCs.</strong> (+2 RP for the dragon, +3 for sparing and recruiting her.)</p>",
  folder=F6["a_creatures"], blurb="The Gray Mistress; the queen's regretful general", token_src=None, actor_link=True))

AW("gray-maiden-palace-guard", B.npc(A6["palaceguard"], "Gray Maiden Palace Guard", 8, 27, 135, 17, 13, 14, 15,
  {"str": 5, "dex": 2, "con": 4, "int": 0, "wis": 0, "cha": 2}, 20,
  {"athletics": 18, "intimidation": 16}, ["humanoid", "human"], ["common"],
  [B.strike(nid(), "+1 Longsword", 20, "2d8+9", "slashing", ["magical", "versatile-p"]),
   B.strike(nid(), "Longbow", 17, "2d8+4", "piercing", ["deadly-d10", "volley-30"]),
   B.action(nid(), "Phalanx Discipline", "passive", "<p>+1 status AC while adjacent to another Maiden; Shield Block; they fight to the death — the castle garrison is the conditioning's finest.</p>", category="defensive"),
   B.gear("full-plate", nid()), B.gear("steel-shield", nid())],
  notes="<p><strong>Role:</strong> the castle's elite garrison — patrols of 4 (8 at the gates), barracks at A37/A38 (with the three <strong>Yallop sisters</strong>, L11 conditioning-matrons — run as Elite "+act(A6["palaceguard"], "guards")+" with Demoralize auras), reinforcing in 1d4 rounds castle-wide. Sabina's Word can still some; the rest die for the Crown.</p>",
  folder=F6["a_creatures"], blurb="Castle-garrison Gray Maiden", token_src=None))

AW("togomor", B.npc(A6["togomor"], "Togomor", 15, 36, 290, 24, 22, 28, 26,
  {"str": 2, "dex": 1, "con": 5, "int": 7, "wis": 3, "cha": 2}, 20,
  {"arcana": 31, "occultism": 29, "society": 27, "intimidation": 25}, ["humanoid", "human"], ["common", "infernal", "thassilonian"],
  [B.strike(nid(), "Bloated Slam", 27, "3d8+8", "bludgeoning", []),
   B.action(nid(), "Blood Magic", "passive", "<p>A bloatmage: his blood is his power. Each spell he casts above 5th rank deals him @Damage[1d6[bleed]] (already in his HP); when he bleeds, his next spell gains +1 to its DC.</p>", category="offensive"),
   B.action(nid(), "Hemorrhage Wave", "3", "<p>A 30-ft cone of pressurized blood-magic: @Damage[14d6[force]] ("+chk("type:reflex|dc:36|basic:true")+"); failures take @Damage[2d6[bleed]].</p>", ["arcane", "force"]),
   B.action(nid(), "Wizard's Arsenal", "2", "<p>CL-15 wizardry (DC 36): <em>quickened magic missile</em> volleys (5 darts), <em>black tentacles</em> ("+chk("type:reflex|dc:36")+" or "+B.cond("grabbed", "Grabbed")+", Escape DC 36), <em>cone of cold</em> @Damage[13d6[cold]], <em>dimension door</em>, <em>fly</em>, layered <em>mirror image</em> + <em>stoneskin</em> (pre-cast).</p>", ["arcane"]),
   B.action(nid(), "Pudgyknuckles", "1", "<p>His toad familiar croaks a stored spell (one 3rd-rank effect per scene) from a pocket dimension.</p>", ["concentrate"]),
   B.lore(nid(), "Thassilon Lore", 29)],
  notes="<p><strong>Role:</strong> the bloatmage <strong>seneschal</strong> — Ileosa's vault-keeper and the castle's arcane warden (A44), grotesquely swollen with leeched blood. He knows the Hidden Way Below (A5) and warded it; his notes name the <strong>Sunken Queen</strong>. <strong>Morale:</strong> dimension-doors to the throne floor at ~60 HP; fights to the death only beside the queen's interests.</p>",
  folder=F6["a_creatures"], blurb="Bloatmage seneschal of Castle Korvosa (A44)", token_src=None, actor_link=True))

AW("sermignatto", B.npc(A6["sermignatto"], "Sermignatto", 15, 37, 280, 25, 24, 28, 27,
  {"str": 5, "dex": 4, "con": 4, "int": 6, "wis": 4, "cha": 7}, 30,
  {"deception": 31, "diplomacy": 29, "society": 29, "occultism": 27, "intimidation": 27}, ["fiend", "devil"], ["common", "infernal", "celestial"],
  [B.strike(nid(), "Binding Quill", 28, "3d8+11", "piercing", ["agile", "magical", "unholy"], [("2d6", "mental")]),
   B.action(nid(), "Read the Fine Print", "1", "<p>He knows the soul-terms of everyone present: <em>detect thoughts</em> at will ("+chk("type:will|dc:35")+"), and +2 circumstance on all checks against anyone who has ever sworn him anything.</p>", ["concentrate", "mental"]),
   B.action(nid(), "Clause of Agony", "2", "<p>One creature within 60 feet: "+chk("type:will|dc:35")+" or contract-script burns across its skin — @Damage[10d6[mental]] and "+B.cond("stupefied", "Stupefied 2")+" 1 round.</p>", ["divine", "mental"]),
   B.action(nid(), "Infernal Court", "2", "<p>Summons 1d4 lesser devils (use "+act(A6["fury"], "Fury")+" stats at Weak) for 1 minute, once per day.</p>", ["conjuration", "divine"]),
   B.action(nid(), "Devil's Resilience", "passive", "<p>Fire immunity; resistance physical 10 (except silver); teleport at will (castle-bound by his own contract).</p>", category="defensive")],
  notes="<p><strong>Role:</strong> the contract devil behind the throne (A52) — broker of Ileosa's erinyes-binding (and secretly the agent of his hidden master, the infernal Duke <strong>Lorthact</strong>). He holds 'court' among the throne room's sycophants, <strong>far preferring negotiation</strong>: the PCs' souls have prices, and he knows them. If Ileosa dies un-raiseable, her contract reverts to him — to Lorthact. A devil worth out-lawyering rather than out-fighting.</p>",
  folder=F6["a_creatures"], senses=[{"type": "darkvision"}, {"type": "true-seeing"}], blurb="Contract devil of the throne room (A52)", token_src=None, actor_link=True))

AW("venster-arabasti", B.npc(A6["venster"], "Venster Arabasti", 6, 22, 80, 11, 13, 16, 14,
  {"str": 0, "dex": 3, "con": 0, "int": 2, "wis": 3, "cha": 4}, 0,
  {"society": 15, "diplomacy": 14, "occultism": 12}, ["undead", "ghost", "incorporeal"], ["common", "infernal"],
  [B.strike(nid(), "Chilling Touch", 15, "2d6+4", "void", ["agile", "magical"]),
   B.action(nid(), "Walled-Up Witness", "passive", "<p>Incorporeal; resistance all 8 (except force/vitality). He cannot leave his boxroom (A89) until avenged — or until the truth he holds is <em>used</em>.</p>", category="defensive")],
  notes="<p><strong>Role (A88–A89):</strong> the king's tiefling stepbrother — Ileosa's poison-tool and first murder, walled up behind his own card-table. <strong>The castle's kindest ghost and best informant:</strong> treated gently ("+chk("type:diplomacy|dc:20")+", or simply <em>listening</em>), he tells everything — the fool's-leprosy cards, the Crown, the Hidden Way Below (A5), and where the queen has gone: <strong>the Sunken Queen, in the Mushfens</strong>. Avenging him (Ileosa's defeat) lets him rest; his remains deserve the royal crypt (A3).</p>",
  folder=F6["a_creatures"], blurb="Ghost of the murdered stepbrother (A89)", token_src=None, actor_link=True))

AW("mavrokeras", B.npc(A6["mavrokeras"], "Mavrokeras", 16, 38, 320, 28, 25, 26, 28,
  {"str": 8, "dex": 4, "con": 6, "int": 1, "wis": 3, "cha": 4}, 40,
  {"athletics": 32, "stealth": 26, "intimidation": 28}, ["dragon", "amphibious"], ["common", "draconic"],
  [B.strike(nid(), "Jaws", 32, "3d12+14", "piercing", ["reach-15"], [("3d6", "acid")]),
   B.strike(nid(), "Claw", 32, "3d10+14", "slashing", ["agile", "reach-10"]),
   B.action(nid(), "Caustic Breath", "2", "<p><strong>Frequency</strong> once per 1d4 rounds. A 60-ft line of black acid: @Damage[16d6[acid]] ("+chk("type:reflex|dc:38|basic:true")+").</p>", ["acid", "arcane"]),
   B.action(nid(), "Frightful Presence", "passive", "<p>90 ft, "+chk("type:will|dc:34")+".</p>", category="offensive"),
   B.action(nid(), "Sea-Tower Ambush", "passive", "<p>He laired in Seawatch Tower (A94) as Ileosa's door-ward: +4 initiative when attacking from the tower's dark, and the first Strike against a surprised creature deals +2d6 precision.</p>", category="offensive")],
  notes="<p><strong>Role (A94):</strong> the second black dragon — Zarmangarof's broodmate, bought with the castle's emptied treasury to ward the Seawatch approach. Less charmed than <em>paid</em>: "+chk("type:diplomacy|dc:38")+" with a better offer (or proof the treasury is spent) can simply make him leave.</p>",
  folder=F6["a_creatures"], senses=[{"type": "darkvision"}], size="grg",
  other_speeds=[{"type": "fly", "value": 120}, {"type": "swim", "value": 60}], blurb="Bought black dragon of Seawatch (A94)", token_src=None, actor_link=True))

AW("kayltanya", B.npc(A6["kayltanya"], "Mistress Kayltanya", 15, 37, 290, 24, 27, 22, 26,
  {"str": 5, "dex": 7, "con": 4, "int": 2, "wis": 1, "cha": 4}, 35,
  {"acrobatics": 29, "stealth": 29, "deception": 27, "intimidation": 27, "religion": 25}, ["humanoid", "human"], ["common", "infernal"],
  [B.strike(nid(), "+2 Greater Striking Sawtooth Saber", 31, "3d8+11", "slashing", ["agile", "finesse", "magical", "twin"], slug="kayltanya-saber"),
   B.sneak_attack(nid(), 5, "Kayltanya"),
   B.action(nid(), "Twin Sabers", "2", "<p>Two Saber Strikes, one target, combined damage.</p>", ["flourish"]),
   B.action(nid(), "Prayer Attack", "1", "<p>The guild-mistress's perfected version: "+chk("type:will|dc:36")+" or "+B.cond("fascinated", "Fascinated")+"; after 2 sustained rounds (not 3), her next Strike on the victim is an automatic critical.</p>", ["concentrate", "incapacitation", "mental", "visual"]),
   B.action(nid(), "Mantis Form", "2", "<p>Once per day: a blood-red Huge mantis; her sabers' magic rides her claws.</p>", ["polymorph", "divine"]),
   B.action(nid(), "Red Shroud", "1", "<p>5/day; +1 AC and fast healing 5 for 7 rounds; may dissolve on death.</p>", ["concentrate"], "defensive")],
  notes="<p><strong>Role:</strong> the Red Mantis <strong>mistress</strong> who collected Vorel's phage and brokered the plague — returned with a hand-picked cell after the Deathhead rout to ward the castle's halls (and judge Cinnabar, if she lives). The Crown's last professional. <strong>If Cinnabar was redeemed, Kayltanya hunts her first</strong> — a loud, well-timed distraction.</p>",
  folder=F6["a_creatures"], senses=[{"type": "darkvision"}], blurb="Red Mantis guild-mistress (castle halls)", token_src=None, actor_link=True))

AW("boggard-champion", B.npc(A6["boggardchamp"], "Boggard Champion", 10, 29, 175, 21, 16, 16, 18,
  {"str": 6, "dex": 2, "con": 5, "int": -1, "wis": 1, "cha": 0}, 20,
  {"athletics": 22, "stealth": 18}, ["humanoid", "boggard"], ["boggard"],
  [B.strike(nid(), "Spiked Club", 23, "2d10+10", "bludgeoning", ["shove"]),
   B.strike(nid(), "Tongue", 21, "", "bludgeoning", ["reach-15"]),
   B.action(nid(), "Tongue Drag", "1", "<p>Tongue hit: the target is "+B.cond("grabbed", "Grabbed")+" (Escape DC 29) and pulled 10 feet toward the champion.</p>", ["attack"]),
   B.action(nid(), "Terrifying Croak", "1", "<p>30-ft burst: "+chk("type:will|dc:27")+" or "+B.cond("frightened", "Frightened 1")+" (non-boggards only).</p>", ["auditory", "fear", "mental"]),
   B.action(nid(), "Swamp King's Own", "passive", "<p>Swim 30; hold breath an hour; +2 status to saves vs. fear while within sight of the Sunken Queen (their god-queen pays in dragon-meat).</p>", category="defensive")],
  notes="<p><strong>Role:</strong> Ileosa's hired swamp-guard — six champions of the Mushfen tribes (1 at the surface entrance B7, 5 in the quarters B8), paid in coin and Beirawash's leavings.</p>",
  folder=F6["a_creatures"], size="lg", other_speeds=[{"type": "swim", "value": 30}],
  blurb="Mushfen boggard elite (B7-B8)", token_src=None))

AW("ithier", B.npc(A6["ithier"], "Ithier", 17, 40, 340, 28, 28, 30, 30,
  {"str": 7, "dex": 6, "con": 5, "int": 4, "wis": 5, "cha": 7}, 35,
  {"deception": 33, "religion": 31, "intimidation": 31, "stealth": 29}, ["fiend", "devil"], ["common", "infernal", "celestial"],
  [B.strike(nid(), "Caress of Chains", 33, "3d10+13", "slashing", ["agile", "magical", "reach-10", "unholy"], [("2d6", "void")]),
   B.action(nid(), "Nursemaid's Embrace", "2", "<p>One adjacent creature: "+chk("type:reflex|dc:38")+" or swept beneath her skirts — "+B.cond("grabbed", "Grabbed")+" (Escape DC 38), "+B.cond("blinded", "Blinded")+", and @Damage[4d6[void]] per round held.</p>", ["attack", "incapacitation"]),
   B.action(nid(), "Handmaiden's Litany", "2", "<p>30-ft burst within 120 feet: @Damage[10d6[mental]] ("+chk("type:will|dc:38|basic:true")+"; failures "+B.cond("stupefied", "Stupefied 1")+").</p>", ["auditory", "divine", "mental"]),
   B.action(nid(), "Devil's Resilience", "passive", "<p>Fire immunity; resistance physical 15 (except holy silver); teleport at will (bound to the Sunken Queen's halls by contract); regeneration 10 (suppressed by holy).</p>", category="defensive")],
  notes="<p><strong>Role (B15):</strong> the gylou 'handmaiden devil' who serves as Ileosa's seneschal-below — mistress of the Great Hall, keeper of the false Ileosas' wardrobe, and the contract's chaperone. She joins the Everdawn fight from below if she still lives. <strong>Negotiation interests her</strong> exactly as long as it amuses.</p>",
  folder=F6["a_creatures"], senses=[{"type": "darkvision"}, {"type": "true-seeing"}], size="lg",
  blurb="Gylou seneschal of the Sunken Queen (B15)", token_src=None, actor_link=True))

AW("ileosas-fury", B.npc(A6["fury"], "Ileosa's Fury", 12, 33, 215, 22, 24, 21, 23,
  {"str": 5, "dex": 6, "con": 3, "int": 2, "wis": 2, "cha": 4}, 30,
  {"acrobatics": 26, "intimidation": 24, "religion": 20}, ["fiend", "devil"], ["common", "infernal"],
  [B.strike(nid(), "+1 Striking Longbow of Flame", 27, "2d8+8", "piercing", ["deadly-d10", "magical", "volley-30"], [("2d6", "fire")]),
   B.strike(nid(), "+1 Striking Longsword", 26, "2d8+10", "slashing", ["magical", "versatile-p"]),
   B.action(nid(), "Rope of Binding", "2", "<p>A 30-ft living rope: "+chk("type:reflex|dc:32")+" or "+B.cond("grabbed", "Grabbed")+" and "+B.cond("immobilized", "Immobilized")+" (Escape DC 32) as it winches the victim to her.</p>", ["attack", "divine"]),
   B.action(nid(), "Fury's Resilience", "passive", "<p>Fire immunity; resistance physical 10 (except holy); fly 60; <em>true seeing</em>; teleport once per hour. <strong>Decabbara, Eveanie, Suishani, Verasia</strong> — they teleport to their queen when the Everdawn battle begins.</p>", category="defensive")],
  notes="<p><strong>Role:</strong> the four erinyes bound into Ileosa's contract — her bodyguard-furies, encountered across the Sunken Queen (B16) and at the Pool. They fight in shrieking pairs, ropes first.</p>",
  folder=F6["a_creatures"], senses=[{"type": "darkvision"}, {"type": "true-seeing"}],
  other_speeds=[{"type": "fly", "value": 60}], blurb="Erinyes bodyguard-fury (B16)", token_src=None))

AW("false-ileosa", B.npc(A6["falseileosa"], "False Ileosa", 9, 27, 130, 17, 19, 16, 18,
  {"str": 2, "dex": 5, "con": 1, "int": 2, "wis": 1, "cha": 5}, 25,
  {"deception": 22, "performance": 20, "acrobatics": 19}, ["humanoid", "human"], ["common", "infernal"],
  [B.strike(nid(), "Glamered Rapier", 21, "2d6+5", "piercing", ["deadly-d8", "finesse", "magical"]),
   B.action(nid(), "Queen's Mockery", "2", "<p>The simulacrum performs its template's scorn: one creature within 30 feet, "+chk("type:will|dc:27")+" or "+B.cond("frightened", "Frightened 1")+" and −1 to attacks against any Ileosa (true or false) for 1 round.</p>", ["auditory", "emotion", "mental"]),
   B.action(nid(), "Snow and Spite", "passive", "<p>A simulacrum: half the queen's memories, none of her power; melts to slush at 0 HP. Telling true from false: "+chk("type:perception|dc:34")+", or any damage (the queen bleeds; these <em>seep</em>).</p>", category="defensive")],
  notes="<p><strong>Role:</strong> six snow-and-blood simulacrums — decoys seeded through the castle and the Sunken Queen, and released as a screaming chorus at the Everdawn Pool. Six queens, one truth.</p>",
  folder=F6["a_creatures"], blurb="Simulacrum decoy of the queen", token_src=None))

AW("immortal-ichor", B.npc(A6["ichor"], "Immortal Ichor", 17, 40, 380, 30, 20, 26, 28,
  {"str": 9, "dex": 0, "con": 8, "int": -3, "wis": 2, "cha": 4}, 20,
  {"athletics": 33}, ["ooze"], [],
  [B.strike(nid(), "Blood Pseudopod", 33, "4d10+15", "bludgeoning", ["reach-15"]),
   B.action(nid(), "Engulf in Blood", "2", "<p>10-ft burst within reach: "+chk("type:reflex|dc:39")+" or engulfed — "+B.cond("grabbed", "Grabbed")+" (Escape DC 39), @Damage[4d6[acid]] per round, and the ichor <strong>heals</strong> that much.</p>", ["attack"]),
   B.action(nid(), "Ooze Resilience", "passive", "<p>Mindless; immune to critical hits, precision, mental; resistance physical 15 (except force). It IS the repository: destroy it and the pool loses 5 charges.</p>", category="defensive")],
  notes="<p><strong>Role (B19):</strong> the Blood Repository — the harvested blood of Korvosa's dead, alive and jealous, guarding the "+haz(A6["soulgem"], "Soultrapping Gem")+". Every gallon the PCs burn here is youth Ileosa never gets.</p>",
  folder=F6["a_creatures"], size="grg", blurb="The living blood-repository (B19)", token_src=None))

AW("taniniver", B.npc(A6["taniniver"], "Taniniver (Kazavon's Shade)", 17, 40, 330, 29, 26, 27, 29,
  {"str": 8, "dex": 4, "con": 6, "int": 1, "wis": 3, "cha": 5}, 40,
  {"athletics": 33, "intimidation": 31}, ["dragon", "disease"], ["draconic"],
  [B.strike(nid(), "Diseased Jaws", 33, "3d12+14", "piercing", ["reach-15"], [("3d6", "void")]),
   B.strike(nid(), "Claw", 33, "3d10+14", "slashing", ["agile", "reach-10"]),
   B.action(nid(), "Blood Veil Incarnate", "passive", "<p>Every natural attack exposes the target to <strong>blood veil</strong> at its apex: "+chk("type:fortitude|dc:37")+" or contract it (the Conversion Guide disease at +5 DC). The plague has teeth now.</p>", category="offensive"),
   B.action(nid(), "Pestilent Breath", "2", "<p><strong>Frequency</strong> once per 1d4 rounds. 60-ft cone: @Damage[16d6[void]] ("+chk("type:fortitude|dc:39|basic:true")+"); failures are exposed to blood veil.</p>", ["divine", "void", "disease"]),
   B.action(nid(), "Manifestation of the Pool", "passive", "<p>Spun from <strong>5 pool charges</strong>; if charges remain, a replacement coalesces the round after this one dies (one at a time). It obeys Ileosa absolutely and cannot pursue past a mile from the Pool. <strong>Every taniniver the PCs destroy burns five days of the ritual.</strong></p>", category="defensive")],
  notes="<p><strong>Role (B20):</strong> the Everdawn Pool's dream of <strong>Kazavon</strong> — a rotting, plague-wrapped serpent-dragon conjured from stolen blood. Not the true dragon (that horror is the fail-state); a promise of him.</p>",
  folder=F6["a_creatures"], senses=[{"type": "darkvision"}], size="grg",
  other_speeds=[{"type": "fly", "value": 80}], blurb="Plague-dragon manifestation of the Pool (B20)", token_src=None))

AW("queen-ileosa", B.npc(A6["ileosa"], "Queen Ileosa Arabasti", 21, 47, 420, 32, 35, 33, 35,
  {"str": 4, "dex": 9, "con": 6, "int": 3, "wis": 2, "cha": 10}, 30,
  {"performance": 40, "deception": 40, "diplomacy": 40, "acrobatics": 38, "arcana": 36, "intimidation": 38}, ["humanoid", "human"], ["common", "infernal", "thassilonian", "varisian", "shadowtongue"],
  [B.strike(nid(), "+3 Major-Striking Speed Rapier", 40, "4d6+15", "piercing", ["deadly-d8", "finesse", "magical"], [("1d6", "cold")], slug="ileosa-rapier"),
   B.action(nid(), "Quickened Grace", "free", "<p>Once per round: an extra Rapier Strike or Stride (her blade's speed rune).</p>"),
   B.action(nid(), "Crown of Fangs", "passive", "<p><strong>The artifact.</strong> Regeneration 20 (suppressed only by <em>Serithtial</em>); <em>mirror image</em> at will; <em>dominate</em> 3/day ("+chk("type:will|dc:42")+"); true seeing; her death is impossible while she wears it — <strong>sundering the Crown with Serithtial</strong> (Hardness 20, HP 80 vs. that blade alone) ends the regeneration and the second soul. <em>Susceptible to Serithtial:</em> each hit from it, "+chk("type:fortitude|dc:35")+" or "+B.cond("drained", "Drained 1")+" (cumulative).</p>", category="defensive"),
   B.action(nid(), "Songs of the Two-Souled", "1", "<p>Bardic war-art (DC 42): <em>inspire courage</em> for her court; <strong>Frightening Tune</strong> ("+chk("type:will|dc:42")+" or "+B.cond("frightened", "Frightened 2")+" and "+B.cond("fleeing", "Fleeing")+" 1 round); or <em>mass suggestion</em> — 'kneel before your queen' ("+chk("type:will|dc:42")+").</p>", ["auditory", "concentrate", "mental"]),
   B.action(nid(), "Irresistible Dance", "2", "<p>Her projected image delivers it: one creature, "+chk("type:will|dc:42")+" or dance ("+B.cond("slowed", "Slowed 2")+", −2 AC) for 1d4 rounds (incapacitation).</p>", ["occult", "incapacitation", "mental"]),
   B.action(nid(), "Court of Devils", "2", "<p>Once per day: summon an ice-devil-grade fiend (run as "+act(A6["ithier"], "Ithier")+" at Weak) for 1 minute; her four "+act(A6["fury"], "Furies")+" answer without being called.</p>", ["conjuration", "divine"]),
   B.action(nid(), "Getaway", "2", "<p><strong>At ~60 HP:</strong> she and every fury and false Ileosa within 30 feet teleport to the Blood Repository (B19); she heals (ring of spell storing: <em>heal</em>; contingency: <em>heal</em> at 30 HP) and returns. <strong>After that, she fights to the death.</strong></p>", ["concentrate", "teleportation"]),
   B.lore(nid(), "Kazavon Lore", 36)],
  notes="<p><strong>THE FINAL BOSS (B20, the Everdawn Pool).</strong> Two souls wear one crown: the spoiled queen, and the seed of <strong>Kazavon</strong> ripening inside her. She floats in trance at the Pool's heart — <strong>10 days remain</strong> on the ritual (give the party two attempts; driven off twice, she finishes it — see What If Ileosa Wins). Noticing intruders, she releases the six "+act(A6["falseileosa"], "false Ileosas")+", her "+act(A6["fury"], "Furies")+" teleport in, "+act(A6["ithier"], "Ithier")+" climbs from below — and the Pool spins up a "+act(A6["taniniver"], "taniniver")+" (5 charges each, replaceable). <strong>Only Serithtial ends her</strong>: suppress the regeneration, sunder the Crown, and the dragon-soul dies screaming. Her contract: un-raiseable without "+act(A6["sermignatto"], "Sermignatto's")+" leave; his master Lorthact inherits if he's dead.</p>",
  folder=F6["a_creatures"], senses=[{"type": "darkvision"}, {"type": "true-seeing"}],
  other_speeds=[{"type": "fly", "value": 60}], blurb="THE QUEEN — two souls, one crown (B20)", token_src=None, actor_link=True))

# ---- hazard ----
hazards = []
def HW(slug, doc):
    hazards.append(copy.deepcopy(doc)); B.write("hazards", slug, doc, embed_items=True)

HW("soultrapping-gem", B.hazard(A6["soulgem"], "Soultrapping Gem (B19)", 9, 28,
  "<p>"+chk("type:perception|dc:28")+" (trained) to feel the hunger in the fist-sized ruby on its pedestal.</p>",
  "<p>"+chk("type:thievery|dc:30")+" to ground the matrix, or shatter it (Hardness 10, HP 40 — releasing its prisoners).</p>",
  "<p>The repository's collector — the 'largest gem below,' which dominated intruders are sent to fetch.</p>",
  [B.action(nid(), "Drink the Soul", "reaction", "<p><strong>Trigger</strong> A living creature touches the gem.</p><hr /><p><strong>Effect</strong> "+chk("type:will|dc:28")+" or the toucher's soul is drawn in (the body drops, "+B.cond("dying", "Dying 1")+", soulless); shattering the gem frees every soul inside.</p>")],
  folder=F6["a_hazards"], traits=["magical", "trap", "incapacitation"], reset="<p>Automatic.</p>", complex_=False))

# =====================================================================
# JOURNAL — "6. Crown of Fangs"
# =====================================================================
SR = lambda area, p: f'<p class="source"><em>Source: CotCT (2016 HC), Ch.6, {area} — p.{p}.</em></p>'
pages = []
def PG(name, html, level=2): pages.append(B.page(nid(), name, html, level=level))
def area6(code, name, html): PG(f"{code}. {name}", html, level=3)
def encx(levels, pl):
    e = B.encounter(levels, party_level=pl); return f"{e['band']} · {e['xp']} XP @ L{pl}"

PG("Chapter Background & the Rebellion",
  B.s_milestone("<p><strong>Chapter 6 — Crown of Fangs.</strong> Serithtial in hand, the PCs return to a city under the queen's heel — and end it. Begin <strong>well into L15</strong>; the Sunken Queen expects L16+; the campaign closes at <strong>L17</strong>. The <strong>Final Harrowing</strong> (suit of crowns) opens the chapter.</p>")
  + SEC("<p><strong>The Korvosan Rebellion</strong> (Victory Points, mirroring Ch.4's Respect): the rebels (Cressida, Vencarlo, the Pharasmins, surviving allies — Amin, Grau, Ishani, Trinia, freed Maidens…) need <strong>Rebellion Points</strong> to hold the city while the PCs strike: expose Trifaccia +1 · kill Zarmangarof +2 · recruit Sabina +3 · each castle commander removed +1 · the castle taken +5. At 10+ RP the rebellion holds Korvosa through the endgame; under 5, the streets burn behind the party (feed the Epidemic Clock its catastrophe tier).</p>")
  + "<p><strong>Threads resolving:</strong> every promise made since Chapter 1 comes home — Sabina's regret, Vencarlo's blade and mantle, Cinnabar's redemption (Kayltanya hunts her), Laori's long walk, Zellara's rest, the Arkonas' papers, the Epidemic Clock's final reading.</p>")

PG("Events 1-2: The Hero & the Mistress",
  box("Greetings, heroes of yesterday! My name is Trifaccia. Have you",
      "<p>'Greetings, heroes of yesterday! My name is Trifaccia. Have you come to surrender?' The brass mask catches the sun; the crowd, primed, roars.</p>")
  + B.enc("EVENT 1 — Korvosa's New Hero", encx([15], 15),
     "<p>"+act(A6["yzahnum"], "Yzahnum")+" as 'Trifaccia' + 12 staged 'rebels' (L3 chaff): three hostile wishes from hiding, then the duel. Unmask the efreeti before the crowd and the persona — and the propaganda — dies (+1 RP).</p>",
     B.aside_token([act(A6["yzahnum"], "Yzahnum / Trifaccia (15)")]))
  + B.enc("EVENT 2 — The Gray Mistress", encx([16, 14], 15),
     "<p>"+act(A6["sabina"], "Sabina Merrin")+" on <strong>Zarmangarof</strong> ("+B.mon("black-dragon-ancient", "Black Dragon, Ancient")+" — run at CR-15 weight). <strong>She is sabotaging her own mount</strong>; when the geas-maddened dragon turns on her, she dismounts and fights it beside the PCs — then surrenders, confesses, and offers everything. The campaign's great redemption: take it.</p>",
     B.aside_token([act(A6["sabina"], "Sabina Merrin (14)"), B.mon("black-dragon-ancient", "Zarmangarof (16)")])))

PG("Part 2: The Assault on Castle Korvosa",
  B.s_milestone("<p><strong>Castle Korvosa</strong> — the pyramid-borne palace, ~95 keyed areas (A1–A95) over five levels. <strong>Getting inside:</strong> Sabina's intelligence (post-Event 2), Venster's ghost, the Epochal Tower clockworks, the Seawatch approach (past "+act(A6["mavrokeras"], "Mavrokeras")+"), or the front door. <strong>Patrols:</strong> 4 "+act(A6["palaceguard"], "Palace Guards")+" per ("+encx([8]*4, 15)+" — chaff; 8 at gates), reinforcing in 1d4 rounds. Alarm escalates to commanders.</p>")
  + SEC("<p><strong>The truth the castle hides:</strong> Ileosa is <em>gone</em> — decamped to the <strong>Sunken Queen</strong> in the Mushfens with the Crown and the harvest, leaving simulacra, devils, and the garrison to bleed the rebellion. The castle assault's prize is the <em>path</em>: Togomor's notes, Venster's testimony, and the Hidden Way Below (A5).</p>"))

area6("A1-A25", "The Dungeon & First Floor", SR("A1-A25", 348)
  + "<ul>"
    "<li><strong>The dungeon:</strong> the emptied Vault of Fangs (A1 — where the Crown was born) and the royal crypts (A3 — Eodred's dust).</li>"
    "<li><strong>A5 — The Hidden Way Below:</strong> "+chk("type:perception|dc:36")+", or Venster/Togomor's notes — the Thassilonian shaft beneath the pyramid.</li>"
    "<li><strong>A8:</strong> two "+B.mon("shining-child", "shining children")+" (Elite — "+encx([13, 13], 15)+") ward the old stair.</li>"
    "<li><strong>A11 — Venster's End:</strong> the walled-up card room — first whisper of the ghost upstairs.</li>"
    "<li><strong>First floor:</strong> gate-stairs, desecrated chapel, the prisons (A19–A22 — the rebellion's missing, freeable: +1 RP), guardrooms ("+encx([8]*4, 15)+" each).</li>"
   "</ul>")

area6("A26-A44", "Second Floor — the Seneschal's Wing", SR("A26-A44", 356)
  + "<p>Offices, archives, the scriptorium — and the garrison heart: <strong>A37/A38</strong> mess and barracks ("+encx([8]*6 + [11]*3, 15)+" with the three Yallop matron-sisters). <strong>A43:</strong> the scriptorium's records (the castle's ledgers = the rebellion's evidence, +1 RP).</p>"
  + B.enc("A44 — Togomor", encx([15], 15),
     "<p>The bloatmage "+act(A6["togomor"], "seneschal")+" among his instruments — tentacles, cold, quickened missiles, and a familiar with one spell too many. His notes name the <strong>Sunken Queen</strong>.</p>",
     B.aside_token([act(A6["togomor"], "Togomor (15)")])))

area6("A45-A66", "Third Floor — Throne & Court", SR("A45-A66", 362)
  + "<ul>"
    "<li><strong>A45 — Main Entrance Landing:</strong> the castle's hardest set-piece if forced ("+encx([15, 8, 8, 8, 8, 8, 8], 15)+" — "+act(A6["kayltanya"], "Kayltanya")+" + the gate-garrison; CR-18-equivalent — <em>do not knock</em>).</li>"
    "<li><strong>A52 — The Throne Room:</strong> "+act(A6["sermignatto"], "Sermignatto")+" holds false court ("+encx([15], 15)+" — or a contract negotiation worth more than the fight).</li>"
    "<li><strong>A54/A65:</strong> gatehouse galleries. <strong>A56:</strong> the arbiters' last honest chambers.</li>"
    "<li><strong>A59 — The Royal Bedroom:</strong> a "+act(A6["falseileosa"], "False Ileosa")+" 'discovered' among traps ("+encx([9, 9], 16)+" with her twin — the queen's first decoy lesson).</li>"
    "<li><strong>A60 — Sabina's room:</strong> spartan; her letters humanize her surrender.</li>"
   "</ul>")

area6("A67-A95", "Fourth Floor, Attics & Towers", SR("A67-A95", 370)
  + box("This huge, lofty chamber is illuminated by braziers",
        "<p>The grand salon's mirrors are draped in mourning-cloth, and behind a walled-up door in the old apartments, something knocks politely.</p>")
  + "<ul>"
    "<li><strong>A72 — The Grand Salon:</strong> a "+act(A6["falseileosa"], "False-Ileosa")+" stage ("+encx([9]*3, 16)+" — three at once, performing grief).</li>"
    "<li><strong>A88–A89 — VENSTER'S GHOST:</strong> "+act(A6["venster"], "the kindest reveal")+" — listen, learn everything, promise him rest.</li>"
    "<li><strong>A90 — Domina's study:</strong> the castle's oldest secrets. <strong>A91–A92:</strong> the Epochal Tower clockworks (a climbing route in).</li>"
    "<li><strong>A94 — Seawatch:</strong> "+act(A6["mavrokeras"], "Mavrokeras")+" ("+encx([16], 15)+" — or "+chk("type:diplomacy|dc:38")+" and an empty-treasury ledger sends him home).</li>"
    "<li><strong>AFTERSHOCKS:</strong> the castle taken (+5 RP), the rebellion surfaces — and Venster's truth points south, to the swamp.</li>"
   "</ul>")

PG("Part 3: Legacy of Blood — the Sunken Queen",
  B.s_milestone("<p><strong>The Sunken Queen</strong> — a drowned Thassilonian pyramid in the Mushfens, Sorshen's face carved a hundred feet tall in its flank. Inside: the harvest of Korvosa's blood, the <strong>Everdawn Pool</strong>, and the queen at her ablutions. <strong>The timer: ~10 days of ritual remain</strong> (each day below burns a charge toward her permanent apotheosis — give the party two attempts at her).</p>")
  + "<p><strong>The approach (B1–B14):</strong> the flooded entrance hall (B1 — "+encx([15], 16)+", the matriarch <strong>Beirawash</strong>: "+B.mon("black-dragon-ancient", "Black Dragon, Ancient")+" at Weak — Zarmangarof's dam, owed a grudge for her stolen son); the surface door ("+act(A6["boggardchamp"], "boggard champion")+", B7) and quarters (5 more, B8 — "+encx([10]*5, 16)+"); the crystal tubes (B12) siphoning blood up the pyramid's veins.</p>"
  + B.enc("B15-B16 — the Great Hall & the Furies", encx([17, 12, 12, 12, 12], 16),
     "<p>"+act(A6["ithier"], "Ithier")+" holding court over the wardrobe of queens, with the four "+act(A6["fury"], "Furies")+" (Decabbara, Eveanie, Suishani, Verasia) mustering — thin them here or meet them all at the Pool.</p>",
     B.aside_token([act(A6["ithier"], "Ithier (17)"), "4× "+act(A6["fury"], "Fury (12)")]))
  + B.enc("B19 — the Blood Repository", encx([17], 16),
     "<p>The "+act(A6["ichor"], "Immortal Ichor")+" over the "+haz(A6["soulgem"], "Soultrapping Gem")+" — <strong>Ileosa's getaway destination</strong> and her reserve of youth. Destroy it before the throne fight and she has nowhere to run and five fewer charges to spend.</p>",
     B.aside_token([act(A6["ichor"], "Immortal Ichor (17)"), haz(A6["soulgem"], "Soultrapping Gem (9)")])))

PG("B20: THE EVERDAWN POOL — the Finale",
  box("This huge, lofty chamber is illuminated by braziers",
      "<p>This huge, lofty chamber is lit by braziers and by the Pool itself — thirty feet of living blood, floating, rippling with faces. At its heart, eyes closed, the queen of Korvosa bathes in her city.</p>")
  + B.enc("THE LAST BATTLE", encx([21, 17, 9, 9, 9, 9, 9, 9], 16),
     "<p><strong>"+act(A6["ileosa"], "QUEEN ILEOSA")+"</strong> (L21) + six "+act(A6["falseileosa"], "false Ileosas")+" + the "+act(A6["taniniver"], "taniniver")+" (replaceable at 5 charges each) + surviving "+act(A6["fury"], "Furies")+" and "+act(A6["ithier"], "Ithier")+". An Extreme-plus battle <em>by design</em>: <strong>Serithtial</strong> suppresses her regeneration, drains her with every cut, and alone can <strong>sunder the Crown</strong>. Stealth to the Pool's heart buys a surprise round. She <em>getaways</em> to B19 at ~60 HP, heals, returns — then fights to the death. Killing her destabilizes the Pool: run <strong>the Rise of the Dragon</strong> immediately.</p>",
     B.aside_token([act(A6["ileosa"], "ILEOSA (21)"), act(A6["taniniver"], "Taniniver (17)"), "6× "+act(A6["falseileosa"], "False Ileosa (9)")]))
  + SEC("<p><strong>THE RISE OF THE DRAGON:</strong> the Pool's stored blood erupts — <strong>Kazavon tries to be born</strong> (a CR-25 cataclysm, not a fight): the pyramid shakes apart as a half-formed dragon of blood claws free. The PCs' job is to <strong>break the birth</strong> — sunder the Crown if they haven't ("+chk("type:athletics|dc:40")+" to hold position in the blood-storm; Serithtial's bearer strikes the Crown), collapse the crystal tubes, and run. Succeed: Kazavon's seed dies forever. Fail to act: see What If Ileosa Wins.</p>")
  + SEC("<p><strong>WHAT IF ILEOSA WINS</strong> (driven off twice, or the ritual completes): the queen ascends — eternal, beautiful, mad — and Korvosa becomes the seat of a dragon-souled god-queen. The campaign continues as resistance: Kazavon manifests fully within the year; the epilogue arc (Continuing the Campaign) inherits a darker world. <em>The Epidemic Clock reads 10 forever.</em></p>"))

PG("Chapter Conclusion — Long Live the Queen",
  B.s_milestone("<p><strong>Immediate repercussions:</strong> with Ileosa dead and the Crown sundered, the contract hunts a new holder ("+act(A6["sermignatto"], "Sermignatto")+" — or his master Lorthact — collects unless out-lawyered); the Pool drains; the trapped souls fly home; <strong>Korvosa wakes.</strong></p>")
  + SEC("<p><strong>The accounting:</strong> the rebellion's RP decides the city's dawn (Cressida as Field Marshal-Regent; the seneschal question — Neolandus restored; the succession council). <strong>Epidemic Clock:</strong> with the harvest dead, Blood Veil's re-seeding ends — the clock empties over the denouement (the CHG-0011b payoff). Sabina's trial and pardon; Trinia's homecoming; Vencarlo passes the Blackjack mantle; Zellara's deck falls finally, gratefully silent. The Shoanti send riders — not for war.</p>")
  + B.s_conv("<p><strong>Campaign complete.</strong> Epilogue and the optional post-finale arc: see the <strong>Appendices &amp; Beyond</strong> journal (Continuing the Campaign — Kazavon Rises · Sorshen's Legacy · Rulers of Korvosa).</p>"))

journal = B.journal_entry(JID6, "6. Crown of Fangs", pages, folder=ADV_FOLDER)
B.write("journals", "06-crown-of-fangs", copy.deepcopy(journal), embed_pages=True)
print(f"Chapter 6 built: {len(actors)} actors, {len(hazards)} hazards, 1 journal ({len(pages)} pages).")
