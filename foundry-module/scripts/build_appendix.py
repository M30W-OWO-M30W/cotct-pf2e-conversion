#!/usr/bin/env python3
"""Appendices & Beyond — post-finale arc (CHG-0003), campaign artifacts, the
Appendix 5 item conversions, the Appendix 6 campaign-wide NPCs (Cressida, Rolth,
Thousand Bones, Asyra, the returned Trinia, Akaruzug, Kazavon), the Appendix 7
random-encounter rolltables + Harrow Deck of Many Things, the Cinderlands travel
hazards, the rebuilt (original-prose) Introduction journal, and idempotent
cross-journal patches (Blackjack, Guard ranks, chapter→suit table, item links).

RUN ORDER: build_pilot.py → build_ch2..ch6.py → build_appendix.py (LAST — this
script overwrites 00-introduction.json and patches other chapters' built JSON)."""
from __future__ import annotations
import copy, json
import pf2e_build as B
B.SCOPE = (17221, 23239)   # AP.md line range for the appendices (anchor scoping)

MODID = "cotct-pf2e-conversion"
ACTOR_ROOT, ITEM_ROOT, ADV_FOLDER = "cotctActorRoot01", "cotctItemRoot001", "cotctAdvFolder01"

JIDA = "appendicesBeyond"
INTRO_JID = "cotctIntro000001"           # same id build_pilot uses — we own the final content
ARTIFACT_FOLDER = "campaignArtifct1"
APP_ITEM_FOLDER = "appItemFolder001"
SERITHTIAL_ID, CROWN_ID = "serithtialSword1", "crownOfFangs0001"
ZELLARA_DECK_ID = "DPDen8gco6rznX9Y"     # ch1 items pack

FA = {"a_app": "appActorFolder01", "a_creatures": "appCreaturesFld1", "a_hazards": "appHazardsFld001"}

# new appendix document ids (16 chars, app-prefixed)
AKT = {"cressida": "appCressidaKrft1", "rolth": "appRolthLamm0001", "bones": "appThousandBone1",
       "asyra": "appAsyraKyton001", "trinia2": "appTriniaSabor01", "akaruzug": "appAkaruzug00001",
       "kazavon": "appKazavon000001"}
HZ = {"emberstorm": "appEmberstorm001", "cindercone": "appCinderCone001", "heat": "appCinderHeat001"}
IT = {"ringsplendid": "appRingSplendid1", "warpaint": "appWarpaint00001", "mantismask": "appMantisMask001",
      "plaguemask": "appPlagueMask001",   # may be overridden below to match ch2's links
      "coffer": "appDeathCoffer01", "souljar": "appSoulJar000001",
      "ringimmolate": "appRingImmolate1", "smokebomb": "appSmokeBomb0001", "ukwaraxe": "appUkwarAxe00001",
      "foolslep": "appFoolsLeprosy1"}
TBL = {"harrowdeck": "appHarrowDeck001", "shingles": "appTblShingles01", "streets": "appTblStreets001",
       "sewers": "appTblSewers0001", "jeggare": "appTblJeggare001", "cinder": "appTblCinder0001",
       "hinter": "appTblHinter0001", "belkzen": "appTblBelkzen001", "mushfens": "appTblMushfen001",
       "rumors": "appTblRumors0001"}
# embedded inventory copies (injected into other chapters' actors)
EMB = {"ring": "appEmbRingSplnd1", "mask": "appEmbMantisMsk1", "smoke": "appEmbSmokeBomb1"}

ids = B._idgen(770007)
def nid(): return next(ids)
sids = B._idgen(887007)
def sid(): return next(sids)

def act(_id, label): return f"@UUID[Compendium.{MODID}.cotct-actors.Actor.{_id}]{{{label}}}"
def haz(_id, label): return f"@UUID[Compendium.{MODID}.cotct-hazards.Actor.{_id}]{{{label}}}"
def itm(_id, label): return f"@UUID[Compendium.{MODID}.cotct-items.Item.{_id}]{{{label}}}"
def tbl(_id, label): return f"@UUID[Compendium.{MODID}.cotct-rolltables.RollTable.{_id}]{{{label}}}"
def chk(s): return f"@Check[{s}]"
def SEC(html): return B.s_secret(html, sid())
def pg(pid, label): return f"@UUID[.{pid}]{{{label}}}"

# module actors referenced by the encounter tables (ids verified against packs)
MA = {"stirge": "stirgeFeeder0001", "drainspider": "1M94tm3wnSRGcTG5", "jigsaw": "lsdWSvGJ81hDy4it",
      "silteel": "siltEel000000001", "derro": "derroMinion00001", "cytillipede": "cytillipede00001",
      "gmfoot": "grayMaidenFoot01", "gmguard": "grayMaidenGuard1", "physician": "queensPhysician1",
      "redmantis": "redMantisAssn001", "rioter": "korvosanRioter01", "lavthug": "lavenderThug0001",
      "empthug": "emperorsThug0001", "boggard": "boggardChamp0001", "thunder": "sklarThundercal1",
      "ashwing": "ashwingGargoyl01", "mithrodar": "mithrodarChain01", "redreaver": "redReaver0000001",
      "havtentacle": "haveroTentacle01", "ukwarfext": "ukwarFext0000001", "sial": "shadowcountSial1"}

# OLLIEBIRD STATBLOCK RESYNC (community swap made these levels/links authoritative):
# levels: Kazavon 25->23 (Arc III finale enc + L-mentions ×3; band recomputes Extreme->Severe,
#   prose follows) · Asyra unchanged (L11 both sides) · swapped items carry no level text here
# rewires: Appendix 7 bestiary page Danse Macabre -> B.cmon (ch5 deletes our danseMacabre0001
#   hazard; community creature L15, MA entry dropped) · items5/artifacts pages now link the
#   community-only Rakshasan Third Eye + Everdawn Pool item docs (build_community files them
#   into OUR appendix/artifact folders; CIT below resolves their original ids) · Mushfens
#   96-100 flavor un-names Beirawash (ch6's actor is the B1 devilfish, not a black dragon)
# gear dedup vs community inventory: injection (9) drops our embedded Mask of the Mantis copy
#   (community Red Mantis Assassin already carries one) and our Smoke Bombs ×3 (community
#   Jolistina carries ×4) — stale embedded copies are stripped idempotently · KEPT: Ring of
#   Splendid Security -> Queen Ileosa (community Ileosa omits this AP treasure), injected as
#   the community item text so it matches the swapped items-pack doc
# skipped: rolltable rows keep official B.mon for wolverine / dream spider / house drake / imp /
#   otyugh / rat swarm / reefclaw / wererat / bulette / erinys / specter / barbed+bone devils /
#   wyvern — the community exports are the same plain creatures (bespoke ones already link
#   module ids) · Kazavon npc() fallback statline left at 25 (swapped at write either way)
# MISSING-CHECK SWEEP (gated-interaction audit): ADDED gazetteer Vaults strata — the barred
#   walls joining brick sewers to older works now badge Athletics DC 30 to Force Open
#   (community ch6 convention: Iron Portcullis A26 / Brick Wall A11 both Force DC 30; = GMC
#   master simple DC for an iron barrier). Judged narrative, no badge: the Acadamae's barred
#   gates (deliberate campaign-long design boundary, gazetteer + rumor row) · Harrow draws
#   (Locksmith/Avalanche are card effects, not obstacles) · V5 Avenue of Arms dig (automatic
#   consequence) · Posh and Turtle glass floor (decor). Already badged nearby: Death's Head
#   Coffer pick DC 30 (same sentence) · Akaruzug Soul Engine wrench-free Athletics DC 36 ·
#   Soul Jar shows Hardness 1/HP 10 · Blackjack kit discovery lives on ch3's A8 page
#   (Perception DC 29 panel + Thievery DC 40 lockbox) — our subsystem page only points there.

# community-only item docs build_community ships into our folders (original 16-char ids)
CIT = {"thirdeye": B.community_doc("item", "Rakshasan Third Eye")["_id"],
       "everdawn": B.community_doc("item", "Everdawn Pool")["_id"]}

# ---------- pack-file IO for idempotent cross-chapter patches ----------
def _load(p): return json.loads(p.read_text(encoding="utf-8"))
def _save(p, doc): p.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
JSRC = B.PACKS / "journals" / "_source"
ASRC = B.PACKS / "actors" / "_source"

# Self-healing shared id: the plaguebringer's mask doc is ours to ship, but ch2's
# journal/actors link it — adopt whatever id ch2 currently references.
_ch2j = JSRC / "02-seven-days-to-the-grave.json"
if _ch2j.exists():
    import re as _re
    _m = _re.search(r"cotct-items\.Item\.(\w*[Pp]lagueMask\w*)", _ch2j.read_text(encoding="utf-8"))
    if _m and _m.group(1) != IT["plaguemask"]:
        print(f"  [shared] plaguebringer's mask id adopted from ch2 links: {_m.group(1)}")
        IT["plaguemask"] = _m.group(1)

def shared_actor(slug, my_id):
    """Defensive shared-actor check: if another chapter already shipped this slug
    (e.g. ch2's Rolth), link to that id instead of double-building."""
    p = ASRC / f"{slug}.json"
    if p.exists():
        ex = _load(p)["_id"]
        if ex != my_id:
            print(f"  [shared] {slug} exists as {ex} — linking, not rebuilding")
            return ex, False
    return my_id, True

def shared_item_free(slug, my_id):
    """True if no OTHER items-pack file already ships this _id (shared-id safety)."""
    for f in (B.PACKS / "items" / "_source").glob("*.json"):
        if f.name.startswith("_folder") or f.stem == slug:
            continue
        try:
            if _load(f).get("_id") == my_id:
                print(f"  [shared] item id {my_id} already shipped by {f.name} — linking only")
                return False
        except Exception:
            continue
    return True

def patch_page(jslug, name_part, marker, html_append):
    p = JSRC / f"{jslug}.json"
    if not p.exists():
        print(f"  [patch] SKIP {jslug} (not built yet — re-run appendix after it)"); return
    d = _load(p)
    for page in d["pages"]:
        if name_part.lower() in page["name"].lower():
            if marker in page["text"]["content"]:
                return
            page["text"]["content"] += html_append
            _save(p, d); print(f"  [patch] {jslug} :: {page['name']}"); return
    print(f"  [patch] page '{name_part}' NOT FOUND in {jslug}")

def patch_replace(jslug, old, new, marker):
    p = JSRC / f"{jslug}.json"
    if not p.exists():
        print(f"  [patch] SKIP {jslug} (not built yet)"); return
    d = _load(p)
    if any(marker in page["text"]["content"] for page in d["pages"]):
        return
    for page in d["pages"]:
        c = page["text"]["content"]
        if old in c:
            page["text"]["content"] = c.replace(old, new, 1)
            _save(p, d); print(f"  [patch] {jslug} :: replaced in {page['name']}"); return
    print(f"  [patch] text NOT FOUND in {jslug}: {old[:50]!r}")

def add_page(jslug, page_id, name, html, level=1):
    """Append (or refresh) a page in another chapter's built journal."""
    p = JSRC / f"{jslug}.json"
    if not p.exists():
        print(f"  [patch] SKIP {jslug} (not built yet)"); return
    d = _load(p)
    for page in d["pages"]:
        if page["_id"] == page_id or page["name"] == name:
            page["name"], page["text"]["content"] = name, html
            _save(p, d); print(f"  [patch] {jslug} :: refreshed page {name}"); return
    pgdoc = B.page(page_id, name, html, level=level)
    pgdoc["sort"] = max((x["sort"] for x in d["pages"]), default=0) + 100000
    pgdoc["_key"] = f"!journal.pages!{d['_id']}.{page_id}"
    d["pages"].append(pgdoc)
    _save(p, d); print(f"  [patch] {jslug} :: added page {name}")

def inject_item(actor_slug, item):
    """Embed a copy of an item doc into another chapter's actor inventory."""
    p = ASRC / f"{actor_slug}.json"
    if not p.exists():
        print(f"  [inject] SKIP {actor_slug} (not built yet)"); return
    d = _load(p)
    it = copy.deepcopy(item); it["folder"] = None
    it["_key"] = f"!actors.items!{d['_id']}.{it['_id']}"
    d["items"] = [x for x in d["items"] if x["_id"] != it["_id"]] + [it]
    _save(p, d); print(f"  [inject] {item['name']} -> {actor_slug}")

# =====================================================================
# FOLDERS
# =====================================================================
B.write("items", "_folder_campaign-artifacts-ite",
        copy.deepcopy(B.folder(ARTIFACT_FOLDER, "Campaign Artifacts", "Item", ITEM_ROOT, 300000, "#b3541e", "a")))
B.write("items", "_folder_appendix-equipment-ite",
        copy.deepcopy(B.folder(APP_ITEM_FOLDER, "Appendix: Equipment & Magic", "Item", ITEM_ROOT, 400000, "#b3541e", "a")))
CHC = "#8a1a1a"
for f in [B.folder(FA["a_app"], "7. Appendices", "Actor", ACTOR_ROOT, 700000, CHC),
          B.folder(FA["a_creatures"], "Creatures", "Actor", FA["a_app"], 100000, None, "a"),
          B.folder(FA["a_hazards"], "Hazards", "Actor", FA["a_app"], 200000, None, "a")]:
    B.write("actors", "_folder_app-" + f["name"].lower().replace(" ", "-").replace(".", "") + "-act", copy.deepcopy(f))
for hf in [B.folder(FA["a_app"], "7. Appendices", "Actor", ACTOR_ROOT, 700000, CHC),
           B.folder(FA["a_hazards"], "Hazards", "Actor", FA["a_app"], 200000, None, "a")]:
    B.write("hazards", "_folder_hz7-" + hf["name"].lower().replace(" ", "-").replace(".", ""), copy.deepcopy(hf))

# =====================================================================
# ITEMS — the two great artifacts + the Appendix 5 conversions
# =====================================================================
B.write("items", "serithtial", B.equipment(SERITHTIAL_ID, "Serithtial", 20, 0,
  "<p><strong>Artifact — the bane of Kazavon.</strong> The bastard sword of Mandraivus, forged by the Esoteric Order of the Palatine Eye and quenched in the dragon's own defeat. Recovered from the Sacred Lake beneath Scarwall (Ch.5, H4), <strong>suppressed</strong> (a masterwork blade) until the Scarwall curse breaks — then fully woken.</p>"
  + "<p><strong>Awakened:</strong> a <em>+3 major striking keen holy bastard sword</em> (treat as a d12 two-hand sword with deadly d10). Against creatures bearing any fragment of Kazavon's essence (the Crown's wearer, the taniniver, Kazavon himself): +4 status damage per die. <strong>Suppresses Queen Ileosa's regeneration</strong> while it has damaged her this round; each hit forces her "+chk("type:fortitude|dc:35")+" or "+B.cond("drained", "Drained 1")+" (cumulative). <strong>Only Serithtial can sunder the Crown of Fangs</strong> (Hardness 20, HP 80 against this blade alone).</p>"
  + "<p><strong>Intelligent &amp; choosy:</strong> Serithtial favors a good-hearted bearer (she <em>chooses</em>; an unworthy hand finds her merely sharp). She speaks rarely, remembers Mandraivus, and wants one thing: the seed of Kazavon dead forever. She shifts in hand to whatever sword-form her bearer favors, counts as cold iron and silver, sheds light at will, and mends her bearer (2-action <em>heal</em>, 3/day, usually held until the bearer is bloodied). Near-indestructible (artifact).</p>",
  traits=["artifact", "magical", "holy", "unique"], rarity="unique", folder=ARTIFACT_FOLDER))

B.write("items", "crown-of-fangs", B.equipment(CROWN_ID, "The Crown of Fangs", 22, 0,
  "<p><strong>Artifact — Midnight's Teeth.</strong> Queen Ileosa's crown, self-forged around the fangs of Kazavon; the vessel of the dragon's soul-seed. While worn: <strong>regeneration 20</strong> (suppressed only by <em>Serithtial</em>), <em>mirror image</em> at will, <em>dominate</em> 3/day ("+chk("type:will|dc:42")+"), continuous true seeing — and the wearer cannot truly die. The second soul grows with every day worn and every death defied; a non-Ileosa wearer begins the campaign's horror over again ("+chk("type:will|dc:40")+" per week or the whispers take root).</p>"
  + "<p><strong>Destruction:</strong> only <em>Serithtial</em> can sunder it (Hardness 20, HP 80 vs. that blade; effectively indestructible otherwise). Its destruction kills the soul-seed — screaming — and ends the regeneration instantly. The six other relics of Kazavon (Armor of Skulls, Bound Blade, Howling Horn, Shredskin, Staff of the Slain, Throne of Nalt) remain scattered across Avistan — <strong>deliberately unplaced</strong>: they are the post-finale arc's hooks (see Continuing the Campaign).</p>",
  traits=["artifact", "magical", "unholy", "unique"], rarity="unique", folder=ARTIFACT_FOLDER))

items_built = []
def IW(slug, doc):
    items_built.append(slug); B.write("items", slug, copy.deepcopy(doc))

ring_splendid = B.equipment(IT["ringsplendid"], "Ring of Splendid Security", 18, 18000,
  "<p><strong>Queen Ileosa's ring</strong> (Appendix 5; PF1e 180,000 gp → 18,000 gp). Invested ring of warded vanity.</p>"
  + "<ul><li><strong>Glamour at will</strong> (1 action, illusion): restyle the apparent fashion of your worn armor, clothing, and weapons — no mechanical change, no drastic size change.</li>"
  + "<li><strong>Worn wards:</strong> +1 item bonus to AC and to all saving throws (already included in Queen Ileosa's stat block).</li>"
  + "<li><strong>Splendid Security</strong> (reaction, 1/hour): when targeted by an attack, spell, or effect, gain a +2 circumstance bonus to your AC or save against it.</li></ul>",
  traits=["invested", "magical"], rarity="rare", folder=APP_ITEM_FOLDER)
IW("ring-of-splendid-security", ring_splendid)

IW("shoanti-warpaint", B.equipment(IT["warpaint"], "Shoanti Warpaint", 8, 90,
  "<p><strong>Appendix 5 (PF1e prices ÷10): 90 gp per pot; black and white 180 gp.</strong> One pot = one application: 1 minute to paint (it provokes nothing but attention); only one color can be active at a time (a new color replaces the old); the magic lasts 24 hours.</p>"
  + "<ul>"
  "<li><strong>Black</strong> (180 gp) — your outline smears: you are concealed against attacks from farther than 5 feet (as <em>blur</em>).</li>"
  "<li><strong>Blue</strong> (90 gp) — +10-foot status bonus to your Speeds.</li>"
  "<li><strong>Green</strong> (90 gp) — the war-chant rides you: +1 status bonus to attack rolls and to saves vs. fear.</li>"
  "<li><strong>Orange</strong> (90 gp) — resistance 2 to physical damage (stacks with rage-granted resistance).</li>"
  "<li><strong>Red</strong> (90 gp) — fire resistance 10 (the burn riders' paint).</li>"
  "<li><strong>Silver</strong> (90 gp) — +1 status bonus to AC.</li>"
  "<li><strong>White</strong> (180 gp) — Skoan-Quah grave-paint: +2 status to saves vs. death and void effects; the first time you would become "+B.cond("drained", "Drained")+", reduce the value by 1 and the paint flakes away spent.</li>"
  "<li><strong>Yellow</strong> (90 gp) — +2 item bonus to Perception.</li>"
  "</ul><p><strong>Ch.4:</strong> Flameford's gratitude includes 5 pots (GM's pick of colors) — this doc supplies the mechanics the chapter grant references.</p>",
  traits=["consumable", "magical"], rarity="uncommon", folder=APP_ITEM_FOLDER))

mantis_mask = B.equipment(IT["mantismask"], "Mask of the Mantis", 10, 600,
  "<p><strong>Red Mantis insignia-helm</strong> (Appendix 5; 6,000 gp → 600 gp). Invested. 3 charges per day, restored at dawn. Spend 1 charge (1 action, concentrate) for one of the following, lasting 30 minutes (effects can run simultaneously):</p>"
  + "<ul><li><strong>Hunter's eyes:</strong> darkvision.</li>"
  "<li><strong>See the unseen:</strong> as <em>see the unseen</em> — invisible creatures appear as shimmering outlines.</li>"
  "<li><strong>Deathwatch:</strong> you sense whether creatures you see are alive, "+B.cond("dying", "Dying")+", undead, or neither.</li>"
  "<li><strong>Vigil:</strong> +2 item bonus to Perception.</li></ul>"
  + "<p>Standard issue for Red Mantis assassins (a copy rides in their inventory); Mistress Kayltanya's is rubied.</p>",
  traits=["invested", "magical"], rarity="uncommon", folder=APP_ITEM_FOLDER)
IW("mask-of-the-mantis", mantis_mask)

if shared_item_free("plaguebringers-mask", IT["plaguemask"]):
    IW("plaguebringers-mask", B.equipment(IT["plaguemask"], "Plaguebringer's Mask", 6, 200,
  "<p><strong>The Queen's Physicians' beaked masks</strong> (Ch.2; Appendix 5: 2,000 gp → 200 gp). Invested.</p>"
  + "<ul><li>+1 item bonus to saves vs. inhaled threats and olfactory effects.</li>"
  "<li><strong>Immunity to one disease</strong>, chosen at creation — every mask in this campaign is keyed to <strong>blood veil</strong> (which is why the doctors never sicken).</li>"
  "<li><strong>Veiled aura:</strong> divination reads the wearer as an ordinary, unremarkable citizen ("+chk("type:perception|dc:24")+" for a detecting caster to notice the veil itself).</li></ul>"
  + "<p>A recovered mask is hard evidence the 'physicians' expected the plague.</p>",
  traits=["invested", "magical"], rarity="uncommon", folder=APP_ITEM_FOLDER))

IW("deaths-head-coffer", B.equipment(IT["coffer"], "Death's Head Coffer", 4, 100,
  "<p><strong>Ch.2's infection vector</strong> (Appendix 5; 1,000 gp → 100 gp). A skull-chased metal coffer about the size of two fists. <strong>Single use:</strong> while the lid is closed, the contents (up to Tiny) hang in stasis — no aging, no decay, no damage — and any infectious matter stays viable.</p>"
  + "<ul><li><strong>Plague box:</strong> seal items in with a disease source and every item inside becomes a carrier; for 1 week after removal, touching a carried item forces a save against that disease (blood veil, for the cult's coin-shipments).</li>"
  "<li>Opening the coffer ends the magic forever (it becomes a mundane box). Some are locked: "+chk("type:thievery|dc:30")+" to pick.</li></ul>",
  traits=["magical", "consumable"], rarity="rare", folder=APP_ITEM_FOLDER))

IW("soul-jar", B.equipment(IT["souljar"], "Soul Jar", 9, 500,
  "<p><strong>Urgathoan reliquary</strong> (Appendix 5; 5,000 gp → 500 gp). A squat ceramic jar warm to the touch.</p>"
  + "<ul><li><strong>Decant a soul:</strong> hold a soul-bound gem (e.g. a <em>bind soul</em> black sapphire) to the lid for 1 round to pour the soul (a creature of level 20 or lower) into the jar; the gem has a 50% chance of shattering. Creatures that can bind souls without a focus can deposit one directly.</li>"
  "<li>A jarred soul cannot pass to judgment — but <strong>can</strong> still be returned to life by <em>resurrection</em>-grade magic.</li>"
  "<li>One soul at a time. Fragile: Hardness 1, HP 10 — breaking the jar frees the soul to the Boneyard.</li></ul>",
  traits=["magical", "unholy"], rarity="rare", folder=APP_ITEM_FOLDER))

IW("ring-of-immolation", B.equipment(IT["ringimmolate"], "Ring of Immolation", 11, 1200,
  "<p><strong>Cinderlands relic</strong> (Appendix 5; the OCR ate its price line — costed from construction at 12,000 gp → 1,200 gp). A band of pumice and hardened ash, strong as steel. Invested.</p>"
  + "<ul><li><strong>Wreath of flame</strong> (free action): up to 10 rounds per day (nonconsecutive). While burning: any creature that hits you with a melee Strike from within your reach takes @Damage[2d6[fire]].</li>"
  "<li><strong>Cold-bane reflex:</strong> if you would take cold damage while rounds remain, the wreath auto-ignites (1 round) and grants resistance 10 to that cold.</li></ul>",
  traits=["invested", "magical", "fire"], rarity="uncommon", folder=APP_ITEM_FOLDER))

smoke_bomb = B.equipment(IT["smokebomb"], "Smoke Bomb", 3, 10,
  "<p><strong>Jolistina's signature toy</strong> (Appendix 5; 100 gp → 10 gp). Martial thrown bomb, range 20 feet.</p>"
  + "<ul><li>On impact, the square fills with roiling gray fog for 1 round (creatures inside are concealed).</li>"
  "<li>The struck creature and every creature in or passing through the cloud: "+chk("type:fortitude|dc:19")+" or "+B.cond("sickened", "Sickened 1")+" (on a critical failure, also "+B.cond("slowed", "Slowed 1")+" for 1 round, retching). Poison effect.</li>"
  "<li><strong>Craft:</strong> "+chk("type:crafting|dc:22")+" (alchemy; trained), 10 gp of reagents — these <em>are</em> purchasable, unlike fool's leprosy.</li></ul>",
  traits=["alchemical", "bomb", "consumable", "poison"], rarity="uncommon", folder=APP_ITEM_FOLDER)
IW("smoke-bomb", smoke_bomb)

IW("ukwar-battleaxe", B.equipment(IT["ukwaraxe"], "Ukwar (Intelligent Battleaxe)", 12, 2000,
  "<p><strong>The fext-axe</strong> (Appendix 5; 23,335 gp → ~2,000 gp): when the Deadwatcher leader "+act(MA["ukwarfext"], "Ukwar")+" is permanently destroyed (Ch.5), her spirit sinks into her <em>+1 striking battleaxe</em> — this item. CE; speaks Common and Orc; darkvision 30 feet; a voice like rocks chewing.</p>"
  + "<ul><li><strong>Axe-sense:</strong> the wielder counts as trained with it; an already-proficient wielder instead gains +1 circumstance to damage with it (her spite guiding the edge).</li>"
  "<li><strong>Rage</strong> (1/day): Ukwar bellows — the wielder gains <em>animal rage</em>-style fury (temp HP = level, +2 status melee damage, −1 AC, 1 minute). It triggers automatically the first time each day the wielder Strikes a spirit anchor or the chained spirit; otherwise "+chk("type:diplomacy|dc:28")+" or "+chk("type:intimidation|dc:28")+" to talk her into it.</li>"
  "<li><strong>Special purpose — lift Scarwall's curse:</strong> while the wielder pursues it inside Scarwall, the axe gains <em>ghost touch</em> and deals an extra @Damage[1d6[spirit]] against the spirit anchors and the chained spirit.</li>"
  "<li><strong>The leash:</strong> a wielder who spends more than a day outside Scarwall while the castle stays cursed faces her nightly: "+chk("type:will|dc:28")+" or be compelled back. Non-chaotic-evil wielders outside Scarwall are "+B.cond("drained", "Drained 1")+" while wielding her. <strong>If the curse breaks, the spirit departs</strong> — leaving an ordinary <em>+1 striking battleaxe</em>.</li></ul>",
  traits=["magical", "unique"], rarity="unique", folder=APP_ITEM_FOLDER))

IW("fools-leprosy", B.equipment(IT["foolslep"], "Fool's Leprosy", 13, 1000,
  "<p><strong>The Red Mantis poison that murdered a king</strong> (Appendix 5; 10,000 gp → 1,000 gp; not for sale anywhere). Ingested poison engineered to wear a disease's face — King Eodred's 'wasting sickness,' delivered via Venster's marked harrow cards.</p>"
  + "<ul><li><strong>Saving throw</strong> "+chk("type:fortitude|dc:33")+"; <strong>Onset</strong> 1 day; <strong>Maximum duration</strong> 6 days; <strong>Virulent</strong> (stages step down only on 2 successive successful saves).</li>"
  "<li><strong>Stage 1</strong> "+B.cond("drained", "Drained 1")+" and "+B.cond("enfeebled", "Enfeebled 1")+", skin lesions (1 day); <strong>Stage 2</strong> Drained 2, Enfeebled 2, flesh visibly sloughing (1 day); <strong>Stage 3</strong> Drained 3, Enfeebled 2, "+B.cond("sickened", "Sickened 1")+" that can't be removed (1 day). The drained value from this poison heals only via <em>restoration</em>-grade magic.</li>"
  "<li><strong>The lie:</strong> to every sense, spell, and symptom it IS fast leprosy. Detecting the poison or diagnosing the truth: "+chk("type:medicine|dc:35")+" (or a counteract-style check at the same DC for detection magic). Disease-curing magic does nothing; <em>neutralize poison</em>-grade effects work normally.</li></ul>",
  traits=["alchemical", "poison", "ingested", "consumable"], rarity="rare", folder=APP_ITEM_FOLDER))

print(f"Appendix items: {len(items_built)+2} written.")

# =====================================================================
# ACTORS — the Appendix 6 campaign-wide NPCs
# =====================================================================
actors = []
def AW(slug, doc):
    actors.append(slug); B.write("actors", slug, doc, embed_items=True)

# Cressida Kroft — the campaign patron (referenced in every chapter; never had an actor)
AW("cressida-kroft", B.npc(AKT["cressida"], "Field Marshal Cressida Kroft", 10, 30, 190, 21, 16, 20, 20,
  {"str": 4, "dex": 0, "con": 3, "int": 1, "wis": 2, "cha": 4}, 20,
  {"diplomacy": 22, "intimidation": 22, "society": 19, "athletics": 20}, ["humanoid", "human"], ["common"],
  [B.strike(nid(), "+1 Striking Longsword", 24, "2d8+10", "slashing", ["magical", "versatile-p"]),
   B.strike(nid(), "Composite Longbow", 18, "2d8+5", "piercing", ["deadly-d10", "volley-30"]),
   B.action(nid(), "Field Marshal's Orders", "1", "<p>One ally within 60 feet that can hear her gains +1 status to attack rolls until the start of her next turn — a career of command in two words.</p>", ["auditory", "linguistic", "mental"]),
   B.action(nid(), "Power Attack", "2", "<p>A Longsword Strike with an extra weapon damage die.</p>", ["flourish"]),
   B.action(nid(), "Cover the Retreat", "reaction", "<p><strong>Trigger</strong> An ally within 30 feet is reduced to 0 HP or starts to flee.</p><hr /><p><strong>Effect</strong> She Strides to put herself between that ally and the nearest enemy and Raises her Shield. She never abandons her people — she dies buying their escape first.</p>", category="defensive"),
   B.action(nid(), "Steadfast", "passive", "<p>+2 status to saves vs. fear; allies within 30 feet who can see her gain +1.</p>", category="defensive"),
   B.lore(nid(), "Korvosa Lore", 19), B.lore(nid(), "Warfare Lore", 19),
   B.gear("full-plate", nid()), B.gear("steel-shield", nid()), B.gear("longsword", nid()),
   B.gear("composite-longbow", nid()), B.gear("healing-potion-minor", nid())],
  notes="<p><strong>THE PATRON.</strong> Ex-adventurer; foiled a Norgorber-cult mass poisoning at the city's third centennial; King Eodred made her Field Marshal for it. From Ch.1 Event 9 she hires the PCs for the Guard's off-book problems — and by Ch.6 she leads the rebellion from the Dead Warrens with a skeleton crew of loyalists.</p>"
  + "<p><strong>Tactics:</strong> melee first, bow for skirmishers; Power Attack until it misses twice, then fights clean. Saves her potion for subordinates. <strong>Morale:</strong> fights to the death covering any retreat that isn't hers.</p>"
  + "<p><strong>Korvosan Guard ranks:</strong> her patronage is the party's ladder — see the Conversion Guide's Reputation page for the rank gates (R2 Trinia's escape · R3 ending blood veil · R4 rescuing Neolandus) and the borrow/recovery benefits.</p>",
  folder=FA["a_creatures"], blurb="Field Marshal of the Korvosan Guard — the campaign's patron", token_src=None, actor_link=True))

# Rolth Lamm — defensive shared build (ch2 fix #4 may own him)
ROLTH_ID, build_rolth = shared_actor("rolth-lamm", AKT["rolth"])
if build_rolth:
    AW("rolth-lamm", B.npc(AKT["rolth"], "Rolth Lamm", 8, 26, 115, 16, 16, 19, 16,
      {"str": -1, "dex": 2, "con": 3, "int": 5, "wis": 0, "cha": 1}, 25,
      {"arcana": 19, "crafting": 17, "thievery": 16, "stealth": 16, "society": 14, "medicine": 14}, ["humanoid", "human"], ["common", "necril", "shoanti", "undercommon", "varisian"],
      [B.strike(nid(), "+1 Key-Blade Dagger", 18, "2d4+2", "piercing", ["agile", "finesse", "magical", "versatile-s"]),
       B.sneak_attack(nid(), 1, "Rolth"),
       B.action(nid(), "Necromancer's Repertoire", "2", "<p>Arcane DC 26, spell attack +18: <em>paralyzing hold</em> (one creature, "+chk("type:will|dc:26")+" or "+B.cond("paralyzed", "Paralyzed")+" 1 round; incapacitation) · <em>lightning bolt</em> @Damage[5d12[electricity]] ("+chk("type:reflex|dc:26|basic:true")+") · <em>enervation ray</em> (spell attack; "+B.cond("drained", "Drained 1")+", 2 on a crit) · <em>vampiric touch</em> @Damage[5d6[void]] and he gains half as temporary HP. Pre-cast when warned: <em>mage armor</em>, <em>shield</em>, <em>false life</em> (in his stats).</p>", ["arcane", "concentrate"]),
       B.action(nid(), "Unlock Flesh", "1", "<p><strong>His own spell.</strong> Touch with a bladed tool: a living creature saves "+chk("type:fortitude|dc:26")+" or is "+B.cond("slowed", "Slowed 1")+" for 1 minute as its flesh hangs open bloodlessly (a new save at the end of each of its turns ends it); a corporeal undead instead takes @Damage[8d6[slashing]] ("+chk("type:fortitude|dc:26|basic:true")+"). Fleshless and incorporeal creatures are immune. He used it to terrorize his father Gaedren.</p>", ["arcane", "necromancy"]),
       B.action(nid(), "Infuse Decay", "passive", "<p><strong>His other spell</strong> (10-minute ritual, fine mortician's tools worth 10 gp): he loads one of his touch effects (Unlock Flesh, a paralyzing or enfeebling touch) into a corporeal undead he controls; it discharges on that undead's next successful Strike (one infusion per undead, one discharge per round). His favorite art: a murdered ally of the PCs, returned as a zombie that paralyzes with a caress.</p>", ["arcane", "necromancy"], "offensive"),
       B.action(nid(), "Grave Touch", "1", "<p>Touch: "+chk("type:fortitude|dc:26")+" or "+B.cond("enfeebled", "Enfeebled 1")+" for 1 minute.</p>", ["arcane", "necromancy"]),
       B.action(nid(), "Key-Lock Killer", "passive", "<p>+2 circumstance to Thievery against locks; his key-shaped blades are his signature — nine locked-room murders the Guard never solved.</p>", category="offensive"),
       B.lore(nid(), "Underworld Lore", 16),
       B.gear("dagger", nid())],
      notes="<p><strong>Gaedren's son</strong> — necromancer, flesh-artist, and Korvosa's uncaught <strong>Key-Lock Killer</strong>. Allied with the Urgathoan cult for resources (his blood-veil notes are Ch.2 evidence: he was studying Varisian immunity). <strong>Tactics:</strong> hangs back behind undead, paralyzes a victim, then takes his time with the knife. <strong>Morale:</strong> flees at ~25 HP via <em>translocate</em> — and if he escapes Ch.2, run him as a recurring hunter (Red Mantis or Arkona patronage; the PCs' slain allies returning as his infused zombies).</p>"
      + "<p><strong>Treasure:</strong> key-blade dagger, mortician's tools (10 gp), 6 black onyxes (15 gp each), his spellbook, and the blood-veil notes (plot).</p>",
      folder=FA["a_creatures"], blurb="The Key-Lock Killer — Gaedren's necromancer son", token_src=None, actor_link=True))

AW("thousand-bones", B.npc(AKT["bones"], "Thousand Bones", 7, 23, 90, 13, 11, 19, 17,
  {"str": -2, "dex": -1, "con": 0, "int": 3, "wis": 5, "cha": 2}, 20,
  {"religion": 18, "nature": 17, "survival": 17, "diplomacy": 16, "medicine": 16}, ["humanoid", "human"], ["common", "dwarven", "giant", "shoanti", "varisian"],
  [B.strike(nid(), "+1 Quarterstaff", 13, "2d4-1", "bludgeoning", ["magical", "two-hand-d8"]),
   B.action(nid(), "Ancestral Spirits", "2", "<p>Divine DC 25: <em>heal</em> (restore @Damage[4d8+10[healing]] HP to a touched ally, or a 30-ft burst at half) · <em>spectral klar</em> (spiritual-weapon spirit shield-blade: +15, @Damage[2d8+3[force]], sustain) · <em>paralyzing hold</em> ("+chk("type:will|dc:25")+"; incapacitation).</p>", ["divine", "concentrate"]),
   B.action(nid(), "Bone Ward", "1", "<p>Hex: one ally within 30 feet gains +1 status AC against undead and can't be "+B.cond("frightened", "Frightened")+" by them, for 1 minute. His crow, <strong>Eats-Eyes</strong>, delivers it.</p>", ["divine", "concentrate"]),
   B.action(nid(), "Speaker for the Dead", "passive", "<p>He understands and is understood in any spoken language (spirit-tongues); senses undead within 60 feet; a day of his instruction gives the party +1 circumstance to checks navigating Shoanti custom (Ch.4).</p>", category="defensive"),
   B.lore(nid(), "Shoanti Lore", 18), B.lore(nid(), "Korvosa Lore", 14)],
  notes="<p><strong>The Skoan-Quah ambassador</strong> — aged Skull Clan shaman who spent years in Korvosa keeping the peace and watching the old tombs in the city's bedrock. His grandson Gaekhen's murder (Ch.1) and Ileosa's coronation send him home to the Kallow Mounds — where, if the PCs honored Gaekhen, he becomes the door to everything in Ch.4.</p>"
  + "<p><strong>Tactics:</strong> heals and wards from the rear; prefers words to war. <strong>Morale:</strong> never leaves while one ally still fights; alone, he surrenders to honorable foes and trusts the spirit world with the rest.</p>",
  folder=FA["a_creatures"], blurb="Skoan-Quah shaman — the Shoanti door (Ch.1, 4)", token_src=None, actor_link=True))

AW("asyra", B.npc(AKT["asyra"], "Asyra", 11, 31, 200, 22, 20, 19, 20,
  {"str": 6, "dex": 5, "con": 4, "int": -2, "wis": 0, "cha": 0}, 30,
  {"acrobatics": 22, "intimidation": 19, "medicine": 17}, ["fiend", "kyton", "eidolon"], ["common"],
  [B.strike(nid(), "+2 Spiked Chain", 25, "2d8+12", "slashing", ["disarm", "magical", "reach-10", "trip"]),
   B.strike(nid(), "Animated Chain", 23, "2d6+9", "bludgeoning", ["agile", "reach-10"]),
   B.strike(nid(), "Claw", 23, "2d6+9", "slashing", ["agile"]),
   B.action(nid(), "Chain Dance", "2", "<p>One Spiked Chain Strike and one Animated Chain Strike (different targets allowed) — her body-chains fight beside her hands.</p>", ["flourish"]),
   B.action(nid(), "Unnerving Gaze", "1", "<p>One creature within 30 feet: "+chk("type:will|dc:29")+" or "+B.cond("sickened", "Sickened 1")+" ("+B.cond("frightened", "Frightened 1")+" as well on a critical failure). Sial is immune; so are other kytons.</p>", ["emotion", "fear", "mental", "visual"]),
   B.action(nid(), "Eidolon Bond", "passive", "<p>Bound to "+act(MA["sial"], "Shadowcount Sial")+" (his casket is her door): when Sial would take damage, she can absorb it instead (his life link). At 0 HP she is <strong>banished to the Plane of Shadow, not slain</strong> — Sial cannot call her back for a day. Resistance 10 cold; resistance 5 physical (except holy).</p>", category="defensive")],
  notes="<p><strong>Sial's kyton eidolon</strong> (Appendix 4's kyton subtype, made flesh): a woman-shaped lattice of pale skin and living chains. She manifests from the bone-house casket Sial carries, speaks rarely, and regards Laori with something like professional disappointment.</p>"
  + "<p><strong>Morale: she fights to the death defending Sial — every time, without hesitation.</strong> Her 'death' is a banishment; her loyalty is structural.</p>",
  folder=FA["a_creatures"], senses=[{"type": "darkvision"}], blurb="Sial's chain-eidolon — fights to the death for him", token_src=None, actor_link=True))

AW("trinia-sabor-returned", B.npc(AKT["trinia2"], "Trinia Sabor (Returned)", 8, 26, 110, 14, 18, 17, 16,
  {"str": 0, "dex": 4, "con": 2, "int": 1, "wis": 0, "cha": 5}, 25,
  {"acrobatics": 19, "performance": 19, "deception": 18, "stealth": 16, "thievery": 16, "society": 15, "athletics": 14}, ["humanoid", "human"], ["common", "varisian"],
  [B.strike(nid(), "+1 Mithral Dagger", 19, "2d4+4", "piercing", ["agile", "finesse", "magical", "thrown-10", "versatile-s"]),
   B.strike(nid(), "Shortbow", 18, "2d6+1", "piercing", ["deadly-d10"]),
   B.action(nid(), "Inspire Courage", "1", "<p>Allies within 60 feet gain +1 status to attacks, damage, and saves vs. fear for 1 round (her comedy is a weapon now).</p>", ["auditory", "concentrate", "emotion", "mental"]),
   B.action(nid(), "Saving Finale", "reaction", "<p><strong>Trigger</strong> An ally within 60 feet fails a save while she's performing.</p><hr /><p><strong>Effect</strong> The ally rerolls the save and keeps the better result. Once per minute.</p>", ["auditory", "concentrate"], "defensive"),
   B.action(nid(), "Painter's Misdirection", "2", "<p>Occult DC 26: <em>mirror image</em> on herself, or <em>glitterdust</em> ("+chk("type:reflex|dc:26")+" or "+B.cond("dazzled", "Dazzled")+" and outlined, 1 minute), or <em>laughing fit</em> ("+chk("type:will|dc:26")+" or "+B.cond("slowed", "Slowed 1")+" 1 round, helpless giggling; incapacitation).</p>", ["occult", "concentrate"]),
   B.action(nid(), "Shingle Runner", "passive", "<p>+2 circumstance to Acrobatics, and to Athletics to Climb; she treats falls as 10 feet shorter and rooftops as roads.</p>", category="defensive"),
   B.lore(nid(), "Painting Lore", 15)],
  notes="<p><strong>The framed painter, leveled up</strong> (replaces the L3 Ch.1 actor for Ch.4+). <strong>Her off-screen arc (Ch.2–4, GM truth):</strong> hiding near Harse, she harried the Craghawk bandits until their leader baited her into a forgotten Shoanti tomb — where she <em>volunteered</em> to host an ancient sorcerer's ghost. The ghost broke the Craghawks, released her, and left a parting gift (her charisma-wreathed headband). She told no one — Jasan at Blackbird Ranch thinks she was off painting — and now she wants <em>in</em>.</p>"
  + "<p><strong>Training with Trinia (retrain):</strong> after 5 days of her coaching (can overlap travel), a PC may retrain one general or skill feat into <strong>Cat Fall, Quick Climb, or Steady Balance</strong> — her Shingle Runner curriculum.</p>"
  + "<p><strong>Morale:</strong> with allies she performs, heals, and saves; below ~25 HP she flees — then spends everything she has rescuing whoever was left behind.</p>",
  folder=FA["a_creatures"], blurb="The painter returned — L8 bard companion (Ch.4+)", token_src=None, actor_link=True))

# Akaruzug — shared with ch6 fix #2
AKARUZUG_ID, build_aka = shared_actor("akaruzug", AKT["akaruzug"])
if build_aka:
    AW("akaruzug", B.npc(AKT["akaruzug"], "Akaruzug", 15, 36, 290, 26, 24, 25, 26,
      {"str": 8, "dex": 3, "con": 0, "int": 2, "wis": 4, "cha": 4}, 0,
      {"religion": 25, "intimidation": 27}, ["construct", "unholy"], ["infernal"],
      [B.strike(nid(), "Claw", 30, "3d10+13", "slashing", ["agile", "magical"]),
       B.strike(nid(), "Gore", 30, "3d12+13", "piercing", ["magical"]),
       B.strike(nid(), "Wing", 28, "2d8+11", "bludgeoning", ["agile", "magical"]),
       B.action(nid(), "Soul Steal", "2", "<p><strong>Frequency</strong> once per 1d4 rounds. 20-foot emanation: living creatures "+chk("type:fortitude|dc:36")+" or "+B.cond("drained", "Drained 1")+" ("+B.cond("drained", "Drained 2")+" on a critical failure); the akaruzug regains 10 HP per creature drained.</p>", ["divine", "void"]),
       B.action(nid(), "Soul Slave", "1", "<p>Once per day: the crucified victim's ghost manifests wielding its favored weapon — a spiritual ally (+28, @Damage[3d10+6[force]], sustain 1 action).</p>", ["concentrate", "divine"]),
       B.action(nid(), "Unhallow Aura", "passive", "<p>A 40-foot unholy aura (chosen rider effect set at creation — commonly darkness, sense-the-righteous, or an invisibility purge); the construct benefits from the rider.</p>", category="offensive"),
       B.action(nid(), "Soul Engine", "passive", "<p><strong>It runs on a person.</strong> A creature crucified to its frame powers it: while active it has +4 status AC and +60 HP (both included), and any attack or effect aimed at the victim strikes the akaruzug instead. The bound soul can't be returned to life. <strong>Shutting it down:</strong> restrain or pin the statue, then 2 actions and "+chk("type:athletics|dc:36")+" to wrench the body free — it deactivates in 1d4 rounds (loses the bonus AC/HP, then all actions), and the soul flies free; destroying it frees the soul too. Re-arming it takes a fresh willing or helpless victim and 1 minute.</p>", category="defensive")],
      notes="<p><strong>The crucifixion engine</strong> (Appendix 7; fielded in the Deathhead Vault arc and at Scarwall). A 15-foot winged statue of stone and iron, a body nailed to its chest, animated by the slow drinking of that soul. Immunities (construct): bleed, death effects, disease, doomed, drained for itself, fatigued, healing, void healing, paralyzed, poison, sickened, unconscious. <strong>The moral lever is the engine:</strong> parties that free the victim mid-fight turn a Severe encounter into a salvage operation.</p>",
      folder=FA["a_creatures"], senses=[{"type": "darkvision"}], size="lg",
      other_speeds=[{"type": "fly", "value": 40}], blurb="Soul-powered crucifixion construct (Appendix 7)", token_src=None))

# Kazavon — CR 25 contingency (shared with ch6 fix #8)
KAZAVON_ID, build_kaz = shared_actor("kazavon", AKT["kazavon"])
if build_kaz:
    AW("kazavon", B.npc(AKT["kazavon"], "Kazavon", 25, 50, 600, 40, 35, 38, 38,
      {"str": 10, "dex": 3, "con": 8, "int": 7, "wis": 6, "cha": 8}, 40,
      {"deception": 44, "diplomacy": 44, "intimidation": 46, "arcana": 42, "religion": 42, "society": 40}, ["dragon", "earth", "unholy"], ["common", "draconic", "infernal", "necril", "orcish", "shoanti"],
      [B.strike(nid(), "Fang of Midnight (Jaws)", 42, "4d12+20", "piercing", ["magical", "reach-30"], [("2d6", "electricity")]),
       B.strike(nid(), "Claw", 42, "4d8+20", "slashing", ["agile", "magical", "reach-20"]),
       B.strike(nid(), "Tail", 40, "4d8+20", "bludgeoning", ["magical", "reach-25"]),
       B.action(nid(), "Breath Weapon", "2", "<p><strong>Frequency</strong> once per 1d4 rounds. A 140-foot line of lightning: @Damage[24d6[electricity]] ("+chk("type:reflex|dc:47|basic:true")+").</p>", ["arcane", "electricity"]),
       B.action(nid(), "Frightful Presence", "passive", "<p>360 feet, "+chk("type:will|dc:45")+". Storm-aura: creatures adjacent at the start of his turn take @Damage[2d6[electricity]].</p>", category="offensive"),
       B.action(nid(), "Warlord's Sorcery", "2", "<p>Arcane DC 47: <em>freeze time</em> (1/day, the classic opener) · <em>maze</em> · <em>wall of force</em> (his battlefield architecture) · <em>chain lightning</em> @Damage[8d12[electricity]] · <em>invisibility (4th)</em> · <em>teleport</em>/<em>gate</em> (his exits). He spends his first stolen round walling the battlefield into a killing floor.</p>", ["arcane", "concentrate"]),
       B.action(nid(), "Human Form", "1", "<p>Zon-Kuthon's gift: a fixed human shape — the pale warlord (AC 47; <em>+3 greater striking unholy spiked chain</em> +44, @Damage[3d8+22[slashing]] plus @Damage[1d6[bleed]]). <strong>Death Transformation:</strong> at 0 HP in human form he erupts back into the dragon at full HP, "+B.cond("slowed", "Slowed 1")+" for 2d4 rounds, his armor destroyed. In human form he fights to the death — because death is a costume change.</p>", ["arcane", "polymorph"]),
       B.action(nid(), "Rejuvenation", "passive", "<p><strong>While any of his seven relics exist, he can always manifest again</strong> (GM's timetable — months or years). Defeated or driven off, he takes <strong>2d6 weeks</strong> to secure his human-form gear before acting openly. <strong>If he was restored via the Everdawn Pool</strong> (Ch.6's fail-state), destroying him leaves <em>only his fangs</em> in the dust — the Crown's seeds, again.</p>", category="defensive"),
       B.lore(nid(), "Scarwall Lore", 44)],
      notes="<p><strong>THE CONTINGENCY (CR 25 → L23).</strong> Kazavon — blue great wyrm, champion of Zon-Kuthon, the warlord whose fangs crown a queen — only walks if the campaign fails: the Crown unsundered, the ritual finished, or the seven relics allowed to converge (Continuing the Campaign, Arc III). First contact is always the dragon; the human warlord comes later, with armies.</p>"
      + "<p><strong>Tactics (dragon):</strong> opens with <em>freeze time</em>, walls the field, goes invisible on the stolen round's end, then fights mobile and airborne — breath and sorcery, never landing. <strong>Morale (dragon):</strong> below ~100 HP he teleports out or gates to the Shadow Plane, returns in days. <strong>Morale (human):</strong> to the death — see Death Transformation.</p>"
      + "<p><strong>His goal on returning:</strong> reclaim Scarwall, rebuild the warlord state that once broke Belkzen — a years-long shadow over any post-campaign play.</p>",
      folder=FA["a_creatures"], senses=[{"type": "darkvision"}, {"type": "scent"}], size="grg",
      other_speeds=[{"type": "fly", "value": 100}, {"type": "burrow", "value": 20}],
      blurb="THE DRAGON — CR 25 contingency (Arc III / fail-state)", token_src=None, actor_link=True))

print(f"Appendix actors: {len(actors)} built (rolth={'new' if build_rolth else 'linked'}, akaruzug={'new' if build_aka else 'linked'}, kazavon={'new' if build_kaz else 'linked'}).")

# =====================================================================
# HAZARDS — the Cinderlands travel hazards the gazetteer cites (used in Ch.4)
# =====================================================================
hazards = []
def HW(slug, doc):
    hazards.append(slug); B.write("hazards", slug, doc, embed_items=True)

HW("cinder-cone-bombardment", B.hazard(HZ["cindercone"], "Cinder Cone Bombardment", 9, 28,
  "<p>"+chk("type:perception|dc:28")+" to hear the tear-drop whistle of an incoming volcanic bomb in time to act.</p>",
  "<p>"+chk("type:survival|dc:28")+" (expert) to read the active cone's rhythm and route the group through a quiet window (avoids the hazard for that leg of travel).</p>",
  "<p>The Cinderlands' active cinder cones lob tear-shaped volcanic bombs up to a mile. They detonate on impact.</p>",
  [B.action(nid(), "Volcanic Bomb", "reaction", "<p><strong>Trigger</strong> The party crosses a bombardment zone (or the GM's d20 travel die comes up a 1 near an active cone).</p><hr /><p><strong>Effect</strong> A bomb shatters in a 15-foot burst: @Damage[6d6[piercing]] and @Damage[6d6[fire]] ("+chk("type:reflex|dc:28|basic:true")+"); on a critical failure, @Damage[2d6[fire]] persistent fire as clinging cinders.</p>")],
  folder=FA["a_hazards"], traits=["environmental", "fire"], reset="<p>The cone keeps coughing — a new bomb every 1d4 hours in an active stretch.</p>", complex_=False))

HW("emberstorm", B.hazard(HZ["emberstorm"], "Emberstorm", 11, 20,
  "<p>It announces itself: a wall of black ash on the horizon. "+chk("type:survival|dc:30")+" (expert) to predict its path an hour ahead.</p>",
  "<p>"+chk("type:survival|dc:30")+" (expert) to lead the group out of the heart to the storm's edge (one check per 10 minutes); reaching real shelter — a gorge, a lotra grove, a tent buried in ash — ends exposure.</p>",
  "<p>The Cinderlands' burning dust storms. The <strong>edge</strong> (outermost 100 feet) is a severe windstorm: difficult terrain, everything is concealed beyond 30 feet, ranged attacks take −4. The <strong>heart</strong> is on fire.</p>",
  [B.action(nid(), "The Burning Heart", "passive", "<p><strong>Routine (heart only)</strong> Each round, every creature in the storm's heart takes @Damage[2d6[fire]] and @Damage[2d6[bludgeoning]] ("+chk("type:fortitude|dc:30|basic:true")+"); a creature that fails also breathes ash and is "+B.cond("sickened", "Sickened 1")+". Eyes and lungs: while in the heart, creatures without sealed protection are "+B.cond("dazzled", "Dazzled")+".</p>")],
  folder=FA["a_hazards"], traits=["environmental", "fire", "complex"], reset="<p>A storm runs 1d4 hours, then collapses into drifting ash.</p>",
  routine="<p>(1 action) The storm advances 60 feet in a direction of the wind's choosing; everything in the heart takes the Burning Heart damage.</p>", complex_=True))

HW("cinderlands-heat", B.hazard(HZ["heat"], "Cinderlands Heat & Thirst", 7, 24,
  "<p>No surprise — the land itself. "+chk("type:survival|dc:24")+" to recognize the day's heat will turn lethal by noon.</p>",
  "<p>"+chk("type:survival|dc:24")+" to find a flask tree, a shaded gorge, or a Shoanti cache (negates the day's exposure for the group). Carrying <strong>double water rations</strong> negates it outright.</p>",
  "<p>The region-wide pressure Ch.4 travels under: water is ash-fouled and scarce — <strong>Subsist checks in the Cinderlands take a −2 circumstance penalty</strong>, and each travel day costs double water.</p>",
  [B.action(nid(), "Scorching Day", "passive", "<p><strong>Each day</strong> traveled without shade and double water: "+chk("type:fortitude|dc:25")+" or take @Damage[4d6[fire]] (heat exhaustion; this damage can't be healed until the creature drinks and rests in shade) and become "+B.cond("fatigued", "Fatigued")+"; critical failure also "+B.cond("drained", "Drained 1")+".</p>")],
  folder=FA["a_hazards"], traits=["environmental"], reset="<p>Daily, until the party leaves the badlands.</p>", complex_=False))

print(f"Appendix hazards: {len(hazards)} built.")

# =====================================================================
# ROLLTABLES
# =====================================================================
tables_built = []
def rows(entries):
    return [{"_id": nid(), "range": [lo, hi], "text": t} for lo, hi, t in entries]
def TW(slug, doc):
    tables_built.append(slug); B.write("rolltables", slug, copy.deepcopy(doc))

def M(slug, label=None): return B.mon(slug, label)
def L(key, label): return act(MA[key], label)

# ---- Harrow Deck of Many Things — all 54 draws, PF2e-converted (OGL mechanics) ----
HDOMT = [
 "<strong>The Avalanche</strong> — Imprisoned: sealed away by a 9th-rank binding (a rescue arc for the others).",
 "<strong>The Bear</strong> — Cursed with lycanthropy (GM picks the beast; a werecreature affliction with no first save).",
 "<strong>The Beating</strong> — In every combat, you are treated as flanked (off-guard) whenever an enemy attacks you.",
 "<strong>The Betrayal</strong> — Your animal companion, familiar, or closest allied NPC turns on you forever — and stands at Ileosa's side at the climax.",
 "<strong>The Big Sky</strong> — 1/day, +10 status to one Athletics check for an attack maneuver (or to your DC against one); each use shatters a nearby metal object.",
 "<strong>The Brass Dwarf</strong> — Immunity to one energy type (your choice); weakness 15 to another (GM's choice).",
 "<strong>The Carnival</strong> — Set aside: the GM reveals 9 fresh cards, flips and shuffles them face down; you pick one and take its effect (sharp eyes can track a card).",
 "<strong>The Courtesan</strong> — Your favorite weapon awakens as an intelligent item. If you bear <em>Serithtial</em>: instead draw 3 cards and keep one.",
 "<strong>The Cricket</strong> — You may draw up to 3 additional cards; permanent +10-foot status to Speed per extra card drawn (plus those cards' effects).",
 "<strong>The Crows</strong> — The GM names your most valuable item and a major ally: choose one to keep; the other is destroyed or slain beyond mortal recall.",
 "<strong>The Cyclone</strong> — Whisked to a ghost-ringed arena: solo duel vs. an elder air elemental (Elite living whirlwind); fail to win in 1d6+1 rounds and you're stranded on the Plane of Air.",
 "<strong>The Dance</strong> — Permanently roll initiative twice and keep either.",
 "<strong>The Demon's Lantern</strong> — Your body disintegrates; your gear remains beside a glowing soul gem (your level × 250 gp). Only resurrection-grade magic restores you (consuming the gem).",
 "<strong>The Desert</strong> — One-time free action: transport yourself, up to 10 allies, and your gear to any known place on this plane — through every ward (including the Sunken Queen's).",
 "<strong>The Eclipse</strong> — From dusk to dawn, every night, you are Drained 1 (irreducible while the sun is down).",
 "<strong>The Empty Throne</strong> — An urge (not a compulsion) to sit the Crimson Throne. If you do: all Korvosa remembers you as old aristocracy — manor, servants, and a 1,500 gp inheritance (player-spent, GM approval).",
 "<strong>The Fiend</strong> — The exiled Infernal Duke Lorthact marks you for destruction; an immolation devil joins Ileosa at the Sunken Queen to deliver the message personally.",
 "<strong>The Foreign Trader</strong> — Trade years for treasure: advance any number of age categories (penalties only) for 2,000 gp of non-unique magic items per category; only a deity returns the years.",
 "<strong>The Forge</strong> — You must reforge one weapon or armor you own into another of equal or lesser value; the difference is lost.",
 "<strong>The Hidden Truth</strong> — One-time free action: an omniscient spirit truthfully answers one question or solves one puzzle.",
 "<strong>The Idiot</strong> — Permanently Stupefied 1; only wish-grade magic lifts it (greed made flesh).",
 "<strong>The Inquisitor</strong> — One-time: force any one creature to answer a single question truthfully (wasted on the genuinely ignorant).",
 "<strong>The Joke</strong> — Choose another PC; the GM reveals 3 fresh cards; they keep one effect, you take one of the remaining two; the last is discarded.",
 "<strong>The Juggler</strong> — Raise two attributes of your choice by +1 apiece — then swap those two attributes with one another.",
 "<strong>The Keep</strong> — A permanent personal demiplane, keyed to you.",
 "<strong>The Liar</strong> — Your favorite magic item gains a curse (GM picks a classic item curse).",
 "<strong>The Locksmith</strong> — One-time: open any one door, lock, binding, or barrier — including conditional magic portals. You know it can suppress the Sunken Queen's teleport ward for 24 hours.",
 "<strong>The Lost</strong> — You cannot gain another level until you die and return — and your next return to life works as <em>reincarnate</em>, whatever spell was cast.",
 "<strong>The Marriage</strong> — A comely genie proposes: a lavish wedding within the week and a lifelong vow — or its elemental court takes mortal offense (GM adjudicates the feud).",
 "<strong>The Midwife</strong> — You gain exactly enough XP to reach your next level.",
 "<strong>The Mountain Man</strong> — You grow one size category. Your equipment does not.",
 "<strong>The Mute Hag</strong> — Permanently blinded, deafened, or mute (your choice); only wish-grade magic cures it.",
 "<strong>The Owl</strong> — One-time: scry any target for 1 minute; the target instantly knows it is watched, and by whom. Scrying 'Ileosa' finds the real queen, never a simulacrum.",
 "<strong>The Paladin</strong> — Granted a <em>holy avenger</em>. If you bear <em>Serithtial</em>: a permanent +1 to one attribute instead.",
 "<strong>The Peacock</strong> — Your skin jewels over: +1 status to AC, permanently Clumsy 1.",
 "<strong>The Publican</strong> — One enemy of yours (not Ileosa; GM picks — restored to life if needed) has a change of heart, seeks you out, and serves as an ally.",
 "<strong>The Queen Mother</strong> — A formian myrmarch (an L10+ hive-knight ally) arrives, devoted to you; its hive-song aids the whole party.",
 "<strong>The Rabbit Prince</strong> — Every Strike you make — and every Strike made against you — gains a doubled critical threat range (19-20).",
 "<strong>The Rakshasa</strong> — Bahor's 'gift': on good terms, 1/week summon a rakshasa servitor; on bad, a "+B.mon("raja-rakshasa", "raja rakshasa")+" hunts you within 24 hours; if Bahor is dead, your hands twist backward — resistance 5 to physical (except piercing) and no other benefit.",
 "<strong>The Sickness</strong> — Incurable blood veil: it progresses to its last stage and stays; only wish-grade magic lifts it.",
 "<strong>The Snakebite</strong> — Your skin weeps venom: any creature that touches you (aid, healing, grapples) saves vs. your class DC or is poisoned (greenblood-oil-style: enfeebled track). It cannot be weaponized deliberately.",
 "<strong>The Survivor</strong> — The next time you would die or fall unconscious from damage, you are instantly restored to full HP instead; no-damage death effects simply fail.",
 "<strong>The Tangled Briar</strong> — 1/day, ask one question of a plant — and each use calls 1d4+2 fiendish "+B.mon("shambler", "shamblers")+" that attack you, regardless of terrain.",
 "<strong>The Teamster</strong> — A beautiful ghost ("+chk("type:arcana|dc:40")+" or "+chk("type:society|dc:40")+" to know her: Sorshen) commands Ileosa's defeat within 7 days. Each week late: an irremovable Drained 1 (die of it and rise a wraith). Succeed: all of it lifts, and +1 Charisma forever.",
 "<strong>The Theater</strong> — The next creature you defeat grants +1 to the attribute matching its own highest.",
 "<strong>The Trumpet</strong> — 1/day, summon a like-hearted celestial/fiend/monitor (level ≤ yours − 2) for 1 minute.",
 "<strong>The Twin</strong> — An exact duplicate of you (mirror-made; copied gear, no artifacts; knowing only what Ileosa knows) manifests at the queen's side as her perfectly loyal bodyguard. You feel it happen.",
 "<strong>The Tyrant</strong> — Your soul attunes to Kazavon: you always sense the nearest relic (the Crown), and you are immune to the relics' offensive effects and to mind-control from anyone wearing one.",
 "<strong>The Unicorn</strong> — One-time: undo one past choice or action — reality respun around it (the dead may live; history bends). The player picks the moment; the GM adjudicates the ripples.",
 "<strong>The Uprising</strong> — 3d6 unruly, accident-prone commoners adopt you as their hero-leader; their deaths and your mistreatment both make the news.",
 "<strong>The Vision</strong> — Two visions — past, present, or future. Exactly one is true. You will never know which.",
 "<strong>The Wanderer</strong> — One mundane possession (GM's choice) quietly becomes a magic item worth 2,000 gp or less (GM's choice).",
 "<strong>The Waxworks</strong> — 1d6 exact duplicates of you, opposite in heart, appear within 20 miles working against everything you want; at least one reaches Ileosa before you do.",
 "<strong>The Winged Serpent</strong> — A single <em>wish</em>.",
]
hd_rows = rows([(i + 1, i + 1, t) for i, t in enumerate(HDOMT)])
harrow_deck_tbl = B.rolltable(TBL["harrowdeck"], "Harrow Deck of Many Things", "1d54", hd_rows,
  desc="<p><strong>Endgame artifact (CHG-0010).</strong> Zellara's deck transcended: each PC declares up to 4 draws before drawing; 1 Harrow Point discards a drawn card for a redraw (doesn't count against the declared total); reshuffle everything between PCs; after every PC finishes, the deck goes forever quiet. Effects bind only the drawer.</p>", sort=100000)
TW("harrow-deck-of-many-things", harrow_deck_tbl)

# ---- the 8 Appendix 7 random-encounter tables ----
DANGER_NOTE = ("<p><strong>City tables:</strong> add Korvosa's current Danger modifier to the d% roll "
  "(+10 Unrest/Plagued · +20 Martial Law · +30 Anarchy — see the Conversion Guide's Reputation page); "
  "halve the roll to skew safer. Base rate everywhere: 20% per travel day or night of rest.</p>")

TW("enc-korvosa-shingles", B.rolltable(TBL["shingles"], "Encounters: The Shingles", "1d100", rows([
 (1, 8, "1 "+M("spider-swarm")), (9, 13, "1d4 "+M("dream-spider", "dream spiders")),
 (14, 23, "2d4 shingle spiders — "+L("drainspider", "drain spider")+" variant (chimney-dwellers; same stats)"),
 (24, 31, "1 "+M("vampire-bat-swarm", "bat swarm")), (32, 36, "1 "+M("hippogriff")),
 (37, 46, "1 "+M("rat-swarm")),
 (47, 58, "1d8 cutpurses — reuse "+L("rioter", "Korvosan Rioter")+" with Thievery +7"),
 (59, 63, "1d8 "+L("stirge", "stirges")), (64, 68, "2d6 "+M("giant-rat", "giant rats")),
 (69, 73, "1d4 "+M("choker", "chokers")), (74, 78, "1d4 "+M("house-drake", "house drakes")+" (CG — talk first)"),
 (79, 83, "1d4 "+M("imp", "imps")), (84, 86, "1d4 ratlings — use "+M("giant-rat", "Giant Rat")+" (Elite) with speech"),
 (87, 94, "1d4 charlatans — reuse "+L("lavthug", "Lavender Thug")+" with Deception +12"),
 (95, 99, "1d4 "+M("dandasuka", "dandasukas")+" (Arkona eyes)"),
 (100, 109, "1d4 veteran burglars — "+L("empthug", "Emperor's Thug")+" (Elite)"),
 (110, 112, "1 "+M("erinys")), (113, 115, "1 "+M("osyluth", "bone devil")),
 (116, 127, "1d4 "+L("redmantis", "Red Mantis assassins")), (128, 130, "1 "+M("hamatula", "barbed devil")),
]), desc="<p>Rooftop-ward table (Appendix 7)."+DANGER_NOTE[3:], sort=200000))

TW("enc-korvosa-streets", B.rolltable(TBL["streets"], "Encounters: Korvosa Streets", "1d100", rows([
 (1, 5, "1d4 "+M("dream-spider", "dream spiders")), (6, 13, "1d6 "+M("giant-rat", "giant rats")),
 (14, 18, "2d4 "+L("drainspider", "drain spiders")), (19, 21, "1 "+M("rat-swarm")),
 (22, 26, "1 "+M("zebub", "accuser devil")+" (someone is being watched)"),
 (27, 29, "1 "+M("web-lurker", "web lurker")+" (ettercap)"),
 (30, 37, "1d4 feral "+M("riding-dog", "dogs")),
 (38, 49, "1d8 cutpurses — reuse "+L("rioter", "Korvosan Rioter")+" with Thievery +7"),
 (50, 52, "1 "+M("otyugh")+" (up from a sewer plug)"), (53, 57, "1d4 "+M("house-drake", "house drakes")),
 (58, 62, "1d4 "+M("imp", "imps")), (63, 67, "1d4 "+M("wererat", "wererats")),
 (68, 77, "1d4 charlatans — reuse "+L("lavthug", "Lavender Thug")+" with Deception +12"),
 (78, 87, "1d8 "+L("gmfoot", "Gray Maiden footsoldiers")), (88, 97, "1d8 "+L("physician", "Queen's Physicians")),
 (98, 102, "1d4 "+M("dandasuka", "dandasukas")), (103, 107, "1 "+M("erinys")),
 (108, 115, "1d4 veteran burglars — "+L("empthug", "Emperor's Thug")+" (Elite)"),
 (116, 123, "1d6 "+L("gmguard", "Gray Maiden guards")), (124, 130, "1d4 "+L("redmantis", "Red Mantis assassins")),
]), desc="<p>Street-level table (Appendix 7) — vermin shading into the queen's factions as the Danger modifier climbs."+DANGER_NOTE[3:], sort=300000))

TW("enc-korvosa-sewers", B.rolltable(TBL["sewers"], "Encounters: The Vaults (Sewers)", "1d100", rows([
 (1, 5, "1 "+M("spider-swarm")), (6, 8, "1d4 "+M("dream-spider", "dream spiders")),
 (9, 13, "2d4 "+L("drainspider", "drain spiders")), (14, 16, "1 "+M("crocodile")),
 (17, 23, "1 "+M("rat-swarm")), (24, 27, "1 "+M("violet-fungus")),
 (28, 32, "1d4 "+M("hunting-spider", "hunting spiders")), (33, 37, "1d4 "+M("reefclaw", "reefclaws")),
 (38, 42, "2d6 "+M("giant-rat", "giant rats")), (43, 45, "2d6 "+M("goblin-warrior", "goblin scavengers")),
 (46, 53, "1d8 cutpurses — reuse "+L("rioter", "Korvosan Rioter")+" with Thievery +7"),
 (54, 56, "1 "+M("centipede-swarm")), (57, 59, "1 "+M("gray-ooze")),
 (60, 62, "1d4 "+M("cave-fisher", "cave fishers")), (63, 65, "1d4 ratlings — "+M("giant-rat", "Giant Rat")+" (Elite) with speech"),
 (66, 70, "1d6 "+M("ghoul", "ghouls")), (71, 73, "1 "+M("gibbering-mouther")),
 (74, 76, "1 rat king — "+M("rat-swarm", "Rat Swarm")+" (Elite, crowned)"),
 (77, 79, "1d4 "+M("web-lurker", "web lurkers")), (80, 84, "1d6 "+M("wererat", "wererats")+" (Girrigz's kin)"),
 (85, 92, "1d4 charlatans — reuse "+L("lavthug", "Lavender Thug")), (93, 95, "1 "+L("cytillipede", "cytillipede")),
 (96, 98, "1d4 "+M("otyugh", "otyughs")), (99, 106, "1d6 "+L("derro", "derros")+" (Vreeg's kin)"),
 (107, 109, "1 "+M("chuul")), (110, 112, "1d4 "+M("barbazu", "bearded devils")),
 (113, 117, "1d4 veteran burglars — "+L("empthug", "Emperor's Thug")+" (Elite)"),
 (118, 120, "1 "+M("mohrg")), (121, 123, "1d4 ghoul stalkers — use "+M("ghast", "Ghast")),
 (124, 125, "1 "+M("vampire-count", "vampire")+" (Sorshen's leavings…)"),
 (126, 130, "1d4 "+L("redmantis", "Red Mantis assassins")),
]), desc="<p>The Vaults: Shoanti burial mounds, brick sewers, and Thassilonian deeps (Appendix 7)."+DANGER_NOTE[3:], sort=400000))

TW("enc-jeggare-river", B.rolltable(TBL["jeggare"], "Encounters: Jeggare River", "1d100", rows([
 (1, 20, "1 "+L("jigsaw", "jigsaw shark")), (21, 35, "2d4 "+L("drainspider", "drain spiders")+" (water-skating)"),
 (36, 50, "1 "+M("crocodile", "alligator")), (51, 55, "1 "+M("bunyip")),
 (56, 75, "1d4 "+M("reefclaw", "reefclaws")), (76, 95, "1d8 "+L("silteel", "silt eels")),
 (96, 100, "1 devilfish — use "+M("reef-octopus", "Reef Octopus")+" (Elite)"),
]), desc="<p>River and harbor travel (Appendix 7). 20% per day afloat.</p>", sort=500000))

TW("enc-cinderlands", B.rolltable(TBL["cinder"], "Encounters: The Cinderlands", "1d100", rows([
 (1, 5, "1d6 "+M("giant-viper", "giant vipers")), (6, 13, "1 "+M("basilisk")),
 (14, 18, "1d4 "+M("giant-scorpion", "giant scorpions")), (19, 26, "1d6 firepelt cougars — use "+M("leopard", "Leopard")),
 (27, 31, "1d6 "+M("hippogriff", "hippogriffs")), (32, 36, "1d6 spirestalkers — "+M("giant-gecko", "Giant Gecko")+" (Elite, horned)"),
 (37, 39, "1d6 "+L("ashwing", "Ashwing gargoyles")), (40, 47, "2d4 "+M("ankhrav", "ankhravs")+" (ankhegs)"),
 (48, 57, "2d6 aurochs — use "+M("bison", "Bison")), (58, 60, "1 "+M("roc")),
 (61, 65, "1d4 "+M("bulette", "bulettes")), (66, 68, "1d4 "+M("chimera", "chimeras")),
 (69, 73, "1 orc warband — "+M("orc-commander", "commander")+" with 2d6 "+M("orc-veteran", "veterans")),
 (74, 76, "1d6 dragonnes — use "+M("manticore-quill-tail", "Manticore")+" (Elite, leonine)"),
 (77, 79, "1d6 "+M("wyvern", "wyverns")), (80, 81, "1 ash giant — use "+M("cave-giant", "Cave Giant")),
 (82, 83, "1d6 "+M("stone-giant", "stone giants")), (84, 87, "1d8 "+M("hill-giant", "hill giants")),
 (88, 90, "2d4 "+M("cave-giant", "cave giants")), (91, 97, "4 "+L("thunder", "Sklar-Quah thundercallers")+" (talk — or burn)"),
 (98, 99, "1 "+M("cave-worm", "cave worm")+" (purple worm)"), (100, 100, "1 "+M("red-dragon-adult", "adult red dragon")),
]), desc="<p>Ch.4's badlands (Appendix 7). Pair with the Cinderlands travel hazards (emberstorm, cinder cones, heat). 20% per travel day.</p>", sort=600000))

TW("enc-hinterlands", B.rolltable(TBL["hinter"], "Encounters: Korvosan Hinterlands", "1d100", rows([
 (1, 5, "1 "+M("wolverine")), (6, 13, "1d4 "+M("giant-gecko", "giant geckos")),
 (14, 18, "1d8 "+L("stirge", "stirges")), (19, 28, "2d6 "+M("goblin-warrior", "goblins")),
 (29, 33, "1d4 "+M("bugbear-tormentor", "bugbears")), (34, 41, "1d4 firepelt cougars — use "+M("leopard", "Leopard")),
 (42, 46, "1d6 "+M("ghoul", "ghouls")), (47, 51, "1 "+M("manticore-quill-tail", "manticore")),
 (52, 59, "1d6 "+M("hippogriff", "hippogriffs")), (60, 69, "1d8 "+M("wolf", "wolves")),
 (70, 85, "1 bandit gang — 5 cutpurses (reuse "+L("rioter", "Korvosan Rioter")+") led by a poacher ("+L("lavthug", "Lavender Thug")+", Elite, longbow)"),
 (86, 88, "1 "+M("ettin")), (89, 91, "1d4 "+M("harpy", "harpies")),
 (92, 94, "1d6 "+M("ogre-warrior", "ogres")), (95, 96, "1 "+M("bulette")),
 (97, 98, "1d4 "+M("troll", "trolls")), (99, 100, "1d4 "+M("hill-giant", "hill giants")),
]), desc="<p>Farms, ferries, and the road to Harse (Appendix 7). 20% per travel day.</p>", sort=700000))

TW("enc-belkzen", B.rolltable(TBL["belkzen"], "Encounters: Hold of Belkzen", "1d100", rows([
 (1, 5, "1d6 "+M("cockatrice", "cockatrices")), (6, 10, "1 "+M("roc")),
 (11, 30, "1 orc warband — "+M("orc-commander", "commander")+" with 2d6 "+M("orc-veteran", "veterans")),
 (31, 35, "1d6 "+M("bulette", "bulettes")), (36, 38, "1 bhuta — use "+M("specter", "Specter")+" (Elite; a wronged wilderness ghost)"),
 (39, 58, "2d6 "+M("orc-scrapper", "orc scouts")), (59, 63, "1d6 yrthaks — use "+M("thunderbird", "Thunderbird")),
 (64, 68, "1d8 "+M("mastodon", "mastodons")), (69, 73, "2d6 "+M("woolly-rhinoceros", "woolly rhinoceroses")+" (arsinoitherium herd)"),
 (74, 78, "2d6 "+M("hill-giant", "hill giants")), (79, 83, "2d6 "+M("troll", "trolls")+" (Elite brutes)"),
 (84, 86, "1 "+M("red-dragon-adult", "adult red dragon")), (87, 91, "1d4 "+M("athach", "athachs")),
 (92, 96, "1d6 ash giants — use "+M("cave-giant", "Cave Giant")), (97, 100, "1 "+M("warsworn")+" (the battlefields remember)"),
]), desc="<p>Ch.5's overland road (Appendix 7) — the AP assumes magical travel; roll only if the party camps or forages. 20% per travel day.</p>", sort=800000))

TW("enc-mushfens", B.rolltable(TBL["mushfens"], "Encounters: The Mushfens", "1d100", rows([
 (1, 20, "1 "+M("goliath-spider")), (21, 35, "1d4 dire crocodiles — "+M("deinosuchus", "Deinosuchus")),
 (36, 40, "1d4 "+M("mobogo", "mobogos")), (41, 45, "1 "+M("froghemoth")),
 (46, 55, "1 "+M("viper-vine")), (56, 65, "1d4 "+M("hezrou", "hezrous")),
 (66, 80, "1d8 "+L("boggard", "boggard champions")+" (Beirawash's tithe-takers)"),
 (81, 90, "2d6 "+M("marsh-giant", "marsh giants")), (91, 95, "1d6 "+M("omox", "omox demons")),
 (96, 100, "1 "+M("black-dragon-ancient", "ancient black dragon")+" (the swamp's eldest terror)"),
]), desc="<p>Ch.6's swamp road to the Sunken Queen (Appendix 7) — a high-level band (L11-16). 20% per travel day.</p>", sort=900000))

# ---- the promised Rumor Mill scaffold (CHG-0012) — original paraphrase hooks ----
TW("korvosa-rumor-mill", B.rolltable(TBL["rumors"], "Korvosa — Rumor Mill", "1d20", rows([
 (1, 1, "The king kept his mistresses even after the wedding — <em>false</em> (he stopped at the altar; the gossips never did)."),
 (2, 2, "A deformed royal brother floats in a jar in the castle attic — <em>false, and the truth is sadder</em> (Venster lived; see Ch.6)."),
 (3, 4, "Eodred was murdered, and the seneschal fled because he did it — <em>half-true</em> (murdered, yes; wrong culprit — see Ch.3)."),
 (5, 6, "The king died of plain old age; the murder talk is anarchist slander — <em>false</em>."),
 (7, 7, "Blackjack is retired… or dead — <em>half-true</em> (watch the end of Ch.1)."),
 (8, 8, "The Key-Lock Killer — nine locked-room murders — was never caught — <em>true</em> (Ch.2 learns his name: Rolth Lamm)."),
 (9, 11, "No crowned monarch of Korvosa dies of old age or leaves an heir: the Curse of the Crimson Throne — <em>believed by everyone; the book itself shrugs</em>."),
 (12, 12, "A jilted paramour — that painter girl, Trinia Sabor — poisoned the king — <em>the queen's lie, repeated until it votes</em>."),
 (13, 14, "The Acadamae has barred its gates until the troubles end — <em>true</em>."),
 (15, 15, "Thieves, anarchists, wererats, and undeath-cultists are all plotting in the same shadows — <em>true, severally</em>."),
 (16, 16, "Otyugh attacks out of the sewers are getting worse — <em>true</em>."),
 (17, 20, "<strong>Chapter rumor:</strong> seed a hook from the current chapter (a site, a villain's calling-card, a mission the PCs could chase early — award full mission rewards if they do)."),
]), desc="<p><strong>The Rumor Mill (CHG-0012).</strong> One Gather Information beat per downtime: "
   + chk("type:diplomacy|dc:15") + " (raise the DC as the city tier slides, to "+chk("type:diplomacy|dc:25")+" under martial law) + 1d4 hours = one roll here. Duplicates: reroll or report the PCs' own deeds back to them, garbled.</p>", sort=1000000))

print(f"Appendix rolltables: {len(tables_built)} built ({len(HDOMT)} harrow draws).")

# =====================================================================
# JOURNAL — "7. Appendices & Beyond"
# =====================================================================
SRC = lambda what, p: f'<p class="source"><em>Source: CotCT (2016 HC), {what} — p.{p}.</em></p>'
def encx(levels, pl):
    e = B.encounter(levels, party_level=pl); return f"{e['band']} · {e['xp']} XP @ L{pl}"

PID = {k: nid() for k in ["arc", "artifacts", "items5", "harrowdeck", "dramatis", "gazetteer", "bestiary7"]}
pages = []
def PG(pid, name, html, level=2): pages.append(B.page(pid, name, html, level=level))

PG(PID["arc"], "Continuing the Campaign — the Post-Finale Arc",
  SRC("Appendix 1 (Continuing the Campaign)", "394-395")
  + B.s_milestone("<p><strong>Beyond the Crown (L17–20, optional).</strong> The approved postgame (CHG-0003): the main story closes at L17; these seven seeds — three of them developed into a playable arc — carry the table to 20 in the same world they saved.</p>")
  + "<p><strong>ARC I — Rulers of Korvosa (L17, intrigue):</strong> no monarch in a century of curses. Neolandus runs the restoration and asks the PCs to broker the succession; factions (the noble houses, the church of Abadar's schism, the surviving Arkonas' papers, the freed Gray Maidens) maneuver. Run it as Influence — and let a PC end it on the Crimson Throne, with everything that word now means.</p>"
  + "<p><strong>ARC II — Sorshen's Legacy &amp; the Everdawn Pool (L18, dungeon):</strong> the Pool's residue stirs what sleeps beneath the city — the pyramid under Castle Korvosa was <em>hers</em>. Destroying the artifact for good is a high-level expedition into Thassilonian deeps; using it, even once, invites Eurythnia's leftovers up the crystal veins.</p>"
  + "<p><strong>ARC III — Kazavon Rises (L19–20, the true endgame):</strong> the Crown was one relic of seven. Across Avistan the others begin to <em>converge</em>, carried by owners who dream the same dream. If they meet, the dragon is reborn whole. Serithtial knows it; she has been waiting five hundred years to finish this.</p>"
  + B.enc("ARC III FINALE — Kazavon Reborn", encx([23], 20),
     "<p>"+act(KAZAVON_ID, "KAZAVON")+" (L23), complete, with whatever army 2d6 weeks of regearing bought him — against one sword. The actor ships his draconic and human forms, the time-stop opening, and his rejuvenation/return logistics. A Severe solo budget at L20 — the regeared army is the dial that pushes the finale to Extreme <em>by design</em>.</p>",
     B.aside_token([act(KAZAVON_ID, "Kazavon (23)"), itm(SERITHTIAL_ID, "Serithtial")]))
  + SEC("<p><strong>Side-seeds</strong> (thread into the arcs): <strong>Ileosa's Revenge</strong> — her soul went to Hell under contract; she can bargain her way back (a devil-army vengeance, or a vampire-return via Pool blood-magic). <strong>Lorthact's Plot</strong> — the contract's hidden master is the exiled Infernal Duke ruling the Acadamae in secret; Ileosa's soul may be his ticket home, and his enemies pay well. <strong>A New Crimson Peril</strong> — the Red Mantis remember: the Crimson Citadel raid is 'harder than Scarwall' (and if Cinnabar lives redeemed, they remember her most of all).</p>")
  + B.s_conv("<p><strong>The six lost relics are dangling by design.</strong> The AP never places the Armor of Skulls, Bound Blade, Howling Horn, Shredskin, Staff of the Slain, or Throne of Nalt — they are Arc III's quest hooks, not an oversight. Seed one per region your table cares about; every owner shares the dream. This conversion deliberately leaves them locationless.</p>"))

PG(PID["artifacts"], "Campaign Artifacts",
  SRC("Appendix 5 (artifacts)", "432-436")
  + "<p>The campaign's three great objects, as items: "+itm(SERITHTIAL_ID, "Serithtial")+" · "+itm(CROWN_ID, "The Crown of Fangs")+" · and "+itm(ZELLARA_DECK_ID, "Zellara's Harrow Deck")+" (Ch.1 items folder), which in the endgame transcends into the <strong>Harrow Deck of Many Things</strong> — no longer GM hand-waving: the full 54-draw table ships as "+tbl(TBL["harrowdeck"], "a rolltable")+", with procedure on "+pg(PID["harrowdeck"], "its own page")+". Venster's ghost (Ch.6) may bestow the first draw.</p>"
  + B.s_conv("<p><strong>Item links at their recovery scenes:</strong> Serithtial is granted at the Sacred Lake islet (Ch.5, H4 — linked there); the Crown is sundered or claimed at the Everdawn Pool (Ch.6, B20 — linked there). Both chapter pages carry the drag-and-drop links.</p>")
  + SEC("<p><strong>The "+itm(CIT["everdawn"], "Everdawn Pool")+"</strong> (not lootable, mercifully — the item doc is a GM reference): a major artifact of stored life — each charge a day of stolen blood (max 25; 10 remain at the finale; bathing grants bleed-immunity and the Sunken Queen's all-seeing eyes; 5 charges spin up a taniniver; 100 charges in a year buy eternal youth over the donors' corpses). Its destruction wants five impossible bloods and a wish — Arc II's prize.</p>"))

PG(PID["items5"], "Appendix 5: Equipment & Magic (Item Docs)",
  SRC("Appendix 5 (Equipment and Magic)", "430-437")
  + "<p>Every Appendix 5 item the campaign actually hands out, converted (PF1e prices ÷10; magic items keep their identity as PF2e equivalents):</p>"
  + "<ul>"
  "<li>"+itm(IT["ringsplendid"], "Ring of Splendid Security")+" — Queen Ileosa's ring (now in her inventory).</li>"
  "<li>"+itm(IT["warpaint"], "Shoanti Warpaint")+" — all 8 colors with effects (Ch.4's 5-pot grant now has mechanics).</li>"
  "<li>"+itm(IT["mantismask"], "Mask of the Mantis")+" — Red Mantis issue (embedded in the assassin's gear).</li>"
  "<li>"+itm(IT["plaguemask"], "Plaguebringer's Mask")+" — why the Queen's Physicians never sicken (Ch.2 evidence).</li>"
  "<li>"+itm(IT["coffer"], "Death's Head Coffer")+" — the plague's coin-shipment vector (Ch.2).</li>"
  "<li>"+itm(IT["souljar"], "Soul Jar")+" — the cult's reliquary.</li>"
  "<li>"+itm(IT["ringimmolate"], "Ring of Immolation")+" — Cinderlands fire-wreath.</li>"
  "<li>"+itm(IT["smokebomb"], "Smoke Bomb")+" — Jolistina's signature (now in her inventory).</li>"
  "<li>"+itm(IT["ukwaraxe"], "Ukwar")+" — the Deadwatcher leader's spirit in her own battleaxe (Ch.5).</li>"
  "<li>"+itm(IT["foolslep"], "Fool's Leprosy")+" — the poison that killed a king, statted as an affliction.</li>"
  "</ul>"
  + B.s_treasure("<p><strong>Community statblock adoption also ships:</strong> the "+itm(CIT["thirdeye"], "Rakshasan Third Eye")+" (Bahor's, Ch.3), the "+itm(CIT["everdawn"], "Everdawn Pool")+" (filed under Campaign Artifacts), and the eight war-paint colors as individual pots in this folder (the combined doc above stays the Ch.4 grant's mechanics reference). <strong>Availability:</strong> none of these are on Korvosa's open market; fool's leprosy and the masks are villain-issue only.</p>"))

PG(PID["harrowdeck"], "The Harrow Deck of Many Things",
  SRC("Appendix 3 (harrow deck of many things)", "428-429")
  + B.s_milestone("<p><strong>Endgame artifact (CHG-0010).</strong> Near the campaign's end — traditionally after Venster's bestowal or Zellara's farewell — her deck wakes fully. Mechanics ship as "+tbl(TBL["harrowdeck"], "Harrow Deck of Many Things")+" (54 draws, 1d54).</p>")
  + "<p><strong>Procedure:</strong></p><ul>"
  "<li>Each PC <strong>declares up to 4 draws</strong> before touching the deck, then draws one at a time; effects bind only the drawer.</li>"
  "<li><strong>The spirit stacks the deck:</strong> on an unwanted card, any PC may spend 1 Harrow Point to discard it and redraw (doesn't count against the declared total).</li>"
  "<li>Reshuffle everything (including discards) when a new PC begins. After every PC has drawn, the deck is forever quiet — a keepsake, not an artifact.</li>"
  "</ul>"
  + B.s_skill("<p><strong>Table-safety notes:</strong> several draws are campaign-grade (The Crows, The Mute Hag, The Lost, The Waxworks); several interact with <em>Serithtial</em> (The Courtesan, The Paladin) or the finale itself (The Twin, The Locksmith, The Owl, The Teamster, The Tyrant). Read the table before offering the deck; the declared-draws rule is the players' only brake.</p>")
  + B.s_conv("<p>For the chapter-by-chapter Harrowing (suit draws, Harrow Points, the Chosen), see the Conversion Guide's <em>The Harrowing</em> page — it now carries the chapter→suit table the print sidebar lost.</p>"))

PG(PID["dramatis"], "Appendix 6: Dramatis Personae (Campaign Index)",
  SRC("Appendix 6 (NPC Codex)", "438-463")
  + '<p class="subhead"><strong>Allies & Patrons</strong></p>'
  + "<ul>"
    "<li>"+act(AKT["cressida"], "Cressida Kroft")+" — Field Marshal; patron from Ch.1, rebel leader by Ch.6 (the campaign's employer, now an actor)</li>"
    "<li>"+act("vencarloOrisini1", "Vencarlo Orisini")+" — swordmaster, mentor — and Blackjack (Ch.3+; the mantle-handoff mechanics live on the Conversion Guide's <em>Becoming Blackjack</em> page and in the Ch.3 journal)</li>"
    "<li>"+act("neolandusKalep01", "Neolandus Kalepopolis")+" — the missing seneschal; the lawful lever (Ch.3+)</li>"
    "<li>"+act("triniaSabor00001", "Trinia Sabor")+" — the framed painter (Ch.1-2) → "+act(AKT["trinia2"], "Trinia Returned")+" (L8, Ch.4+; her off-screen Craghawk/ghost-tomb arc and the <em>Training with Trinia</em> retrain ride on the new actor)</li>"
    "<li>"+act("grauSoldado00001", "Grau Soldado")+" — redeemed watch sergeant (Ch.1-2)</li>"
    "<li>"+act("ishaniDhatri0001", "Ishani Dhatri")+" — Abadaran healer of the plague (Ch.2+)</li>"
    "<li>"+act("aminJalento00001", "Amin Jalento")+" — rescued young noble (Ch.1, 3, 6)</li>"
    "<li>"+act(AKT["bones"], "Thousand Bones")+" — Skoan-Quah shaman; the Shoanti door (Ch.1, 4)</li>"
    "<li>"+act("krojunEatsWhat01", "Krojun Eats-What-He-Kills")+" — Sklar-Quah champion; rival, then nalharest (Ch.4)</li>"
    "<li>"+act("akramTruthspeak1", "Truthspeaker Akram")+" — the last truthspeaker (Ch.4)</li>"
    "<li>"+act("marcusEndrin0001", "Marcus Endrin")+" — Sable commandant; the great rescue (Ch.3, 4)</li>"
    "<li>"+act("laoriVaus0000001", "Laori Vaus")+" — cheerful Kuthite; the long redemption (Ch.3, 5)</li>"
    "<li>"+act("shadowcountSial1", "Shadowcount Sial")+" — Brotherhood of Bones; would-be curate (Ch.4-5) — never without "+act(AKT["asyra"], "Asyra")+", his kyton eidolon (fights to the death for him; banished, not slain)</li>"
    "<li>"+act("sabinaMerrin0001", "Sabina Merrin")+" — the queen's general; the great defection (Ch.6)</li>"
    "<li>"+act("vensterArabast01", "Venster's ghost")+" — the kindest informant (Ch.6)</li>"
    "<li><strong>Zellara</strong> — the harrow-spirit guide (whole campaign; guard her from Scarwall); her deck: "+itm(ZELLARA_DECK_ID, "Zellara's Harrow Deck")+"</li>"
   "</ul>"
  + '<p class="subhead"><strong>Villains, by Chapter</strong></p>'
  + "<ul>"
    "<li><strong>Ch.1</strong> — "+act("RKfT6vJ5guinSBjo", "Gaedren Lamm")+" · "+act("vreegDerroNec001", "Vreeg")+"</li>"
    "<li><strong>Ch.2</strong> — "+act("reinerDavaulus01", "Dr. Davaulus")+" · "+act("andaisinUrgath01", "Lady Andaisin")+" · "+act(ROLTH_ID, "Rolth Lamm")+" (the Key-Lock Killer; recurring if he escapes) · "+act("ramoskaArkminos1", "Ramoska Arkminos")+" · "+act("jolistinaSusp001", "Jolistina")+"</li>"
    "<li><strong>Ch.3</strong> — "+act("piltsSwastel0001", "Pilts Swastel")+" · "+act("bahorArkona00001", "Bahor")+" · "+act("vimandaArkona001", "Vimanda")+" · "+act("sivitDarksphinx1", "Sivit")+"</li>"
    "<li><strong>Ch.4</strong> — "+act("cinderlander0001", "the Cinderlander")+" · "+act("cinnabarRedMant1", "Cinnabar")+" · "+act("zenobiaZenderh01", "Zenobia Zenderholm")+" · "+act("kordaitraDesta01", "Kordaitra Destaid")+"</li>"
    "<li><strong>Ch.5</strong> — "+act("mithrodarChain01", "Mithrodar")+" · "+act("zevRavenkaDemi01", "Zev Ravenka")+" · "+act("belshallamUmbr01", "Belshallam")+" · "+act("kleestadPharma01", "Kleestad")+"</li>"
    "<li><strong>Ch.6</strong> — "+act("togomorBloatmg01", "Togomor")+" · "+act("sermignattoDvl01", "Sermignatto")+" · "+act("kayltanyaRedM001", "Mistress Kayltanya")+" · "+act("queenIleosa00001", "QUEEN ILEOSA")+"</li>"
   "</ul>"
  + '<p class="subhead"><strong>Contingencies & Engines</strong></p>'
  + "<ul>"
    "<li>"+act(KAZAVON_ID, "Kazavon")+" (L23) — the fail-state and Arc III finale; ships with return logistics (2d6 weeks to regear; an Everdawn restoration leaves only fangs on destruction).</li>"
    "<li>"+act(AKARUZUG_ID, "Akaruzug")+" (L15) — the soul-engine crucifix construct (Deathhead Vault arc / Scarwall).</li>"
   "</ul>"
  + B.s_conv("<p><strong>Module complete:</strong> Chapters 1–6, the subsystems (Harrowing · Reputation/City Tiers · Blood Veil/Epidemic Clock · Respect &amp; Rebellion Points · Becoming Blackjack · Korvosan Guard ranks), the campaign backgrounds, the Appendix 5 items, the Appendix 7 tables, and the postgame arc. Verbatim read-aloud renders only on the GM's machine (local AP.md injection); all mechanics are original PF2e conversion work. Run well.</p>"))

PG(PID["gazetteer"], "Korvosa & Beyond (Gazetteer Reference)",
  SRC("Appendix 2 (Korvosa and Beyond)", "396-415")
  + "<p><strong>The city</strong> (84 keyed locations, summarized for play): the Heights (Castle Korvosa, the Acadamae — Lorthact's secret), Old Korvosa (Endrin Isle, Old Dock, Fort Korvosa — the Arkonas), North Point (the Bank of Abadar, Citadel Volshyenek, the Longacre Building), Midland (the Shingles, Eel's End), Gray District (the Dead Warrens, the rebel ossuary), South Shore (Carowyn Manor, the noble estates), East Shore (Hellknight Citadel Vraid beyond).</p>"
  + '<p class="subhead"><strong>The Shingles & The Vaults</strong></p>'
  + "<p><strong>The Shingles:</strong> the rooftop shanty-ward — a criminal highway above the Guard's sightline, nested with "+B.mon("imp", "imps")+", the "+B.mon("house-drake", "house drakes")+" that hunt them (and cause nearly as much trouble), stirges in the gutters, and chokers no purge has ever cleared (locals in overshadowed blocks sleep below the second floor for a reason). Random table: "+tbl(TBL["shingles"], "The Shingles")+".</p>"
  + "<p><strong>The Vaults:</strong> Korvosa's underground has three strata — repurposed <em>Shoanti burial mounds</em> (the mainland's twisting dead-end 'sewers' were tombs first; the Skoan-Quah have not forgotten), purpose-built <em>brick sewage tunnels</em> (the newest, often joining older works behind barred walls — "+chk("type:athletics|dc:30")+" to Force Open a barrier), and the <em>Thassilonian deeps</em> — Eurythnia's bones, oldest and worst, with surviving Darklands links. Random table: "+tbl(TBL["sewers"], "The Vaults")+".</p>"
  + '<p class="subhead"><strong>Sites of Interest (V1–V13)</strong></p>'
  + "<ul>"
    "<li><strong>V1 Old City Hall</strong> ('the Charcoal Palace') — mostly abandoned; a caretaker skeleton crew.</li>"
    "<li><strong>V2 Exemplary Execrables</strong> — Pilts Swastel's gore-theater (volunteers went missing); burned in the quarantine; its manager re-crowns himself in Ch.3.</li>"
    "<li><strong>V3 Temple of Aroden</strong> — its three caretakers die of blood veil early; a brutal choker nest by Ch.3.</li>"
    "<li><strong>V4 Wreck of the Direption</strong> — the false plague ship's grave (Ch.2).</li>"
    "<li><strong>V5 Avenue of Arms</strong> — 127 identical stone arms along the riverfront, elbows bent away from shore, all sprouting from one buried basalt mass; dig at it and it <em>shrieks</em> and wells black brine. Thassilonian. Leave it alone.</li>"
    "<li><strong>V6 Jeggare Museum</strong> — curator <strong>Mercival Jeggare</strong> pays fair coin for Varisian finds (the party's best fence for antiquities).</li>"
    "<li><strong>V7 Marbledome</strong> — the money-losing opera house.</li>"
    "<li><strong>V8 The Gatefoot</strong> — a colossal stone foot, all that stands of a statue of <strong>Sorshen</strong> (rumors of a complex below were never substantiated… Arc II disagrees).</li>"
    "<li><strong>V9 Kendall Amphitheater</strong> — a sinkhole made a stage by Abadarans and dwarven masons.</li>"
    "<li><strong>V10 Eodred's Square</strong> — Midland's meeting-plaza (and a statue site for Ileosa's vanity project).</li>"
    "<li><strong>V11 Pillar Wall</strong> — the 100-foot Thassilonian pillar-row.</li>"
    "<li><strong>V12 Great Tomb of Leadership</strong> — Gray's guarded crypt of generals.</li>"
    "<li><strong>V13 Dead Warrens</strong> — the pauper-crypts (Ch.1 Part 3; the rebellion's cellar by Ch.4+).</li>"
   "</ul>"
  + '<p class="subhead"><strong>Proprietors the chapters meet</strong></p>'
  + "<p><strong>Eel's End</strong> — Devargo Barvasi, the King of Spiders (Ch.1) · <strong>Old Fishery</strong> — Gaedren Lamm (Ch.1) · <strong>All the World's Meat</strong> — the Cow Hammer Boys (Ch.1) · <strong>Lavender</strong> — Vendra Loaggri, the cure-fraud (Ch.2) · <strong>Carowyn Manor</strong> — the Carowyns, then Jolistina's puppet-show (Ch.2) · <strong>Hospice of the Blessed Maiden</strong> — Arkona warehouse turned Urgathoan front (Ch.2) · <strong>Arkona Palace</strong> — 'Glorio' (Ch.3) · <strong>Orisini Academy</strong> — Vencarlo, until the Red Mantis burn it (Ch.3) · <strong>Posh and Turtle</strong> — Thaviun Rigulus, wizard-restaurateur (glass floor over Old Tom the sea turtle) · <strong>Pestico's Dolls</strong> — old Vadid Pestico · <strong>Acadamae</strong> — headmaster Toff Ornelos (gates barred all campaign) · <strong>Bank of Abadar</strong> — Archbanker Darb Tuttle (fights the free-healing schism; Ishani's superior) · <strong>Grand Cathedral of Pharasma</strong> — Keppira d'Bear (secret rebel landlord under martial law) · <strong>Jeggare Light</strong> — a keeper who is no longer alive, exactly (the cult's penanggalen lamplighter).</p>"
  + '<p class="subhead"><strong>City state & markets</strong></p>'
  + "<p><strong>City state-tracking:</strong> run Korvosa's condition by the Conversion Guide's <strong>Reputation &amp; City Tiers</strong> page — it now ships the concrete tier table (Baseline L14 → Unrest L11 → Plagued L10 → Martial Law L8 → Anarchy/black-market L11, with purchase caps and hireling casting per tier), driven by the <strong>Epidemic Clock</strong> (Blood Veil page) and the chapters' events. <strong>The Rumor Mill</strong> ships as "+tbl(TBL["rumors"], "a scaffold rolltable")+" ("+chk("type:diplomacy|dc:15")+" to "+chk("type:diplomacy|dc:25")+" by tier).</p>"
  + '<p class="subhead"><strong>The hinterlands & beyond</strong></p>'
  + "<p><strong>Near:</strong> Harse (Blackbird Ranch; ferry-town where fugitive PCs are recognized fast — "+tbl(TBL["hinter"], "Hinterlands table")+"), Janderhoff (the dwarven Sky Citadel that shelters Vencarlo and Neolandus, start of Ch.4), Citadel Vraid (the Hellknights — mercenary allies who leave when the pay does, Ch.2), Kaer Maga (the cliff-city resupply), Veldraine and Palin's Cove (the navy and the siege-engine yards), Melfesh, Baslwief, Biston, Sirathu, Abken (the holdings).</p>"
  + "<p><strong>Far:</strong> the Cinderlands (Ch.4 — travel hazards now real: "+haz(HZ["emberstorm"], "Emberstorm")+" · "+haz(HZ["cindercone"], "Cinder Cone Bombardment")+" · "+haz(HZ["heat"], "Heat & Thirst")+"; encounters: "+tbl(TBL["cinder"], "Cinderlands table")+"; flora worth knowing: flask trees store water, galtroot becomes the Shoanti's 'barbarian chew,' ember poppies sprout after burns), Belkzen ("+tbl(TBL["belkzen"], "Belkzen table")+" — Ch.5 assumes magical transit), the Mushfens ("+tbl(TBL["mushfens"], "Mushfens table")+" — Ch.6's swamp road), the Jeggare River ("+tbl(TBL["jeggare"], "River table")+").</p>")

PG(PID["bestiary7"], "Appendix 7: Bestiary & Random Encounters",
  SRC("Appendix 7 (Bestiary)", "464-477")
  + B.s_skill("<p><strong>Random encounter rules:</strong> 20% chance per day of travel or night of rest (GM's dial). The three Korvosa tables add the city's current <strong>Danger modifier</strong> (+10 Unrest/Plagued · +20 Martial Law · +30 Anarchy) to the d% roll — the nasty results live above 100; halve the roll to skew safer. Scarwall (Ch.5) uses its own chapter rules.</p>")
  + "<p><strong>The eight tables:</strong> "+tbl(TBL["shingles"], "The Shingles")+" · "+tbl(TBL["streets"], "Korvosa Streets")+" · "+tbl(TBL["sewers"], "The Vaults (Sewers)")+" · "+tbl(TBL["jeggare"], "Jeggare River")+" · "+tbl(TBL["cinder"], "The Cinderlands")+" · "+tbl(TBL["hinter"], "Korvosan Hinterlands")+" · "+tbl(TBL["belkzen"], "Hold of Belkzen")+" · "+tbl(TBL["mushfens"], "The Mushfens")+" — plus "+tbl(TBL["rumors"], "the Rumor Mill")+".</p>"
  + '<p class="subhead"><strong>The nine new monsters → where they live now</strong></p>'
  + "<ul>"
    "<li><strong>House drake</strong> — official PF2e print: "+B.mon("house-drake")+" (a CG imp-hunter; 7th-level CG casters may take one as a familiar).</li>"
    "<li><strong>Dream spider</strong> — official PF2e print: "+B.mon("dream-spider")+" (its venom distills into the drug shiver — Ch.1's economy).</li>"
    "<li><strong>Drain spider / shingle spider</strong> — module actor: "+L("drainspider", "Drain Spider")+" (the shingle variant is the same beast in a chimney).</li>"
    "<li><strong>Chained spirit</strong> — module actor: "+L("mithrodar", "Mithrodar")+" (Ch.5's curse-heart; the anchor mechanics live on his sheet).</li>"
    "<li><strong>Danse macabre</strong> — community statblock (creature, L15): "+B.cmon("Danse Macabre")+" (Ch.5).</li>"
    "<li><strong>Red reaver</strong> — module actor: "+L("redreaver", "Red Reaver")+" (beauty-fascinated siege-beast).</li>"
    "<li><strong>Akaruzug</strong> — new appendix actor: "+act(AKARUZUG_ID, "Akaruzug")+" (the soul-engine crucifix).</li>"
    "<li><strong>Havero</strong> — <strong>tentacles only, by design:</strong> the full CR-21 horror is never fought; Ch.4/Ch.6 stage only its reaching limbs ("+L("havtentacle", "Havero Tentacle")+"). Severing tentacles buys passage — the body behind the wall is a reason to <em>leave</em>, and the conversion keeps it that way deliberately.</li>"
    "<li><strong>Pharmakos</strong> — the god-cursed apostate-guardian has no module actor (its one cameo is off the campaign's spine); improvise from "+B.mon("mobogo", "Mobogo")+" (Elite) with constant agony (immune to pain), an acid-blood breath cone, and Strength-sapping claws if your table goes looking.</li>"
   "</ul>"
  + B.s_conv("<p><strong>PF2e substitutions inside the tables</strong> (no official print exists): yrthak → Thunderbird · bhuta → Elite Specter · dragonne → Elite leonine Manticore · ash giant → Cave Giant · ratling → speaking Elite Giant Rat · rat king → crowned Elite Rat Swarm · devilfish → Elite Reef Octopus · arsinoitherium → Woolly Rhinoceros · NPC-Codex humans → reflavored module NPCs. Everything else links the official Bestiary/Monster Core.</p>"))

journal = B.journal_entry(JIDA, "7. Appendices & Beyond", pages, folder=ADV_FOLDER)
B.write("journals", "07-appendices-and-beyond", copy.deepcopy(journal), embed_pages=True)
print(f"Appendices journal: {len(pages)} pages.")

# =====================================================================
# INTRODUCTION — rebuilt with ORIGINAL summaries (policy fix: build_pilot's
# verbatim publisher-prose pages are replaced; the 'Atrip…' OCR artifact dies
# with them). Same journal id, so this overwrite is clean.
# =====================================================================
intro_pages = [
 B.page(nid(), "Long Live the Queen!",
  '<p class="source"><em>Source: CotCT (2016 HC), Introduction — pp.4-9. Original summary; the publisher\'s prose stays in your own book.</em></p>'
  + B.s_read("<p>Korvosa calls itself the Jewel of Varisia — a charter-bound Chelish colony of arbiters and academies, built on a flattened pyramid older than its gods. Its people prize order, wealth, and routine. They are about to lose all three.</p>")
  + "<p><strong>The premise.</strong> Korvosans whisper of a curse on their throne: no crowned ruler has died of old age, and none has produced an heir. King Eodred II is dying — faster than nature explains — and his young queen, Ileosa Arabasti, is about to inherit a city that despises her. What follows is an urban campaign about one city and the monster its crown makes: riots, a manufactured plague, a quarantined island, an exile among the Shoanti, a haunted castle at the edge of the world, and a final reckoning beneath a drowned pyramid.</p>"
  + "<p><strong>The engine.</strong> The PCs don't start as heroes of the realm — they start as people Gaedren Lamm has wronged. The crime-lord's downfall (Chapter 1) puts them on the streets the night the king dies, and Field Marshal Cressida Kroft turns survivors into agents. From there the campaign escalates by betrayal, not by dungeon-depth.</p>"
  + B.s_skill("<p><strong>What you need:</strong> the PF2e core rules; this module; your own copy of the AP for the boxed read-aloud (see the build note below); battle maps of your choosing (Racooze's free CotCT set fits). The Conversion Guide journal carries the campaign-wide subsystems: the Harrowing, Reputation &amp; City Tiers, the campaign backgrounds, Blood Veil &amp; the Epidemic Clock, and Becoming Blackjack.</p>")
  + B.s_conv("<p><strong>IP policy (how this module ships):</strong> boxed read-aloud is injected at build time from the GM's local AP markdown and is never committed or redistributed; every page of mechanics, encounter math, and summary prose is original PF2e conversion work. These introduction pages are original summaries by design.</p>"), level=1),
 B.page(nid(), "Campaign Synopsis",
  '<p class="source"><em>Source: CotCT (2016 HC), Introduction (synopsis) — pp.7-8. Original summary.</em></p>'
  + "<table><thead><tr><th>Chapter</th><th>Levels</th><th>One line</th></tr></thead><tbody>"
  "<tr><td><strong>1. Edge of Anarchy</strong></td><td>1 → 4</td><td>Gaedren Lamm's bill comes due; the king dies mid-chapter; the PCs hold a rioting city for its new queen — then watch her find a scapegoat.</td></tr>"
  "<tr><td><strong>2. Seven Days to the Grave</strong></td><td>4 → 8</td><td>Blood veil sweeps Korvosa. The 'Queen's Physicians' aren't doctors, the plague ship was staged, and the cure leads through a cathedral of Urgathoa.</td></tr>"
  "<tr><td><strong>3. Escape from Old Korvosa</strong></td><td>8 → 11</td><td>A journey into the quarantined island-district — mob emperors, Red Mantis assassins, the rakshasa lords of House Arkona — to retrieve the seneschal who can lawfully name the queen's crimes. Blackjack returns; the mantle looks for new shoulders.</td></tr>"
  "<tr><td><strong>4. A History of Ashes</strong></td><td>10/11 → 13</td><td>Exile in the Cinderlands: earning the Shoanti's trust, the history of the dragon whose fangs the queen wears, and the Red Mantis hunting party that follows.</td></tr>"
  "<tr><td><strong>5. Skeletons of Scarwall</strong></td><td>13 → 15</td><td>Across Belkzen to a chain-hung castle of the dead, for the one blade that can unmake the Crown of Fangs: <em>Serithtial</em>.</td></tr>"
  "<tr><td><strong>6. Crown of Fangs</strong></td><td>15 → 17</td><td>The rebellion, the assault on Castle Korvosa — and the Sunken Queen, where Ileosa bathes in her city's stolen blood. The campaign ends with a sword, a crown, and a choice of dawns.</td></tr>"
  "</tbody></table>"
  + SEC("<p><strong>The spine (GM only):</strong> Queen Ileosa's crown is set with the fangs of <strong>Kazavon</strong>, a dragon-warlord of Zon-Kuthon slain centuries ago; its seed-soul ripens in her as she feeds it. The plague, the Blooding, the blood-harvest — all of it fills the <strong>Everdawn Pool</strong>, the Thassilonian artifact that will make her (or what wears her) eternal. Only Serithtial, the blade that killed Kazavon the first time, can cut the knot — and the campaign is the long road to its hilt.</p>")
  + B.s_conv("<p><strong>After the finale:</strong> the optional L17–20 postgame (Rulers of Korvosa · Sorshen's Legacy · Kazavon Rises) lives in the <em>7. Appendices &amp; Beyond</em> journal, with the Harrow Deck of Many Things, the Appendix 5 item docs, the Appendix 7 encounter tables, and the campaign-wide NPC actors.</p>"), level=1),
 B.page(nid(), "Using This Module",
  '<p class="source"><em>Conversion notes — original to this module.</em></p>'
  + "<p><strong>What's in the box:</strong> one fat journal per chapter (section-block pages: read-aloud, GM-secret, skill, treasure, encounter cards with GMC XP math) · actors and hazards per chapter (officially-printed monsters link the PF2e Bestiary instead of being rebuilt) · items (campaign artifacts, backgrounds, Appendix 5 conversions) · rolltables (Harrowing, Rumor Mill, the eight Appendix 7 encounter tables, the Harrow Deck of Many Things) · the Ch.1 scene and Adventure bundle.</p>"
  + "<ul>"
  "<li><strong>Encounter cards</strong> show name | budget (e.g. 'Severe · 120 XP @ L4') — recomputed for PF2e, not transliterated.</li>"
  "<li><strong>DCs and damage</strong> are native PF2e enrichers — click to roll.</li>"
  "<li><strong>Treasure</strong> follows the PF1e-gp ÷ 10 anchor for valuables; named magic items keep their identity as PF2e equivalents with runes.</li>"
  "<li><strong>GM-secret blocks</strong> are hidden from players by Foundry's section.secret handling and badged for the GM.</li>"
  "<li><strong>Build order</strong> (for rebuilders): pilot → ch2…ch6 → appendix, last — the appendix script owns this introduction and stitches cross-chapter links.</li>"
  "</ul>"
  + B.s_skill("<p><strong>Subsystem map:</strong> Harrowing + chapter→suit table — Conversion Guide · Reputation, City Tiers, Korvosan Guard ranks — Conversion Guide · Blood Veil / Epidemic Clock — Conversion Guide · Becoming Blackjack — Conversion Guide + Ch.3 · Respect Points — Ch.4 · Rebellion Points — Ch.6 · the postgame — Appendices &amp; Beyond.</p>"), level=1),
]
intro_journal = B.journal_entry(INTRO_JID, "Introduction", intro_pages, folder=None)
B.write("journals", "00-introduction", copy.deepcopy(intro_journal), embed_pages=True)
print("Introduction journal: rebuilt with original prose (3 pages).")

# =====================================================================
# CROSS-CHAPTER PATCHES (idempotent; run appendix LAST)
# =====================================================================
print("Cross-chapter patches:")

# --- (1) Conversion Guide: The Harrowing — chapter→suit table (the lost sidebar) ---
patch_page("00-conversion-guide", "The Harrowing", "appHarrowChTbl",
  '<section class="conversion" id="appHarrowChTbl"><p><strong>Chapter → suit (the lost sidebar).</strong> '
  "The print sidebar mapping each chapter to a suit didn't survive OCR — these journals are now the carrier. "
  "Each chapter's Harrowing pulls its Choosing from this suit, and Harrow Points that chapter reroll the matching ability:</p>"
  "<table><thead><tr><th>Chapter</th><th>Suit</th><th>Ability</th><th>Alternate 1-point spends (free action)</th></tr></thead><tbody>"
  "<tr><td>1. Edge of Anarchy</td><td>Keys</td><td>Dexterity</td><td>+1 status AC <em>or</em> +10-ft Speed for one encounter</td></tr>"
  "<tr><td>2. Seven Days to the Grave</td><td>Shields</td><td>Constitution</td><td>resistance 3 to physical for one encounter; <em>or</em> after a fight, 1 minute's rest restores HP equal to your level</td></tr>"
  "<tr><td>3. Escape from Old Korvosa</td><td>Books</td><td>Intelligence</td><td>+1 status to one spell's DC; <em>or</em> attempt one trained-only action untrained</td></tr>"
  "<tr><td>4. A History of Ashes</td><td>Hammers</td><td>Strength</td><td>+5 status damage with melee Strikes for one combat; <em>or</em> ignore an object's Hardness for 1 round</td></tr>"
  "<tr><td>5. Skeletons of Scarwall</td><td>Stars</td><td>Wisdom</td><td>your next vitality/void spell gains +1 to its DC and +1 die</td></tr>"
  "<tr><td>6. Crown of Fangs</td><td>Crowns</td><td>Charisma</td><td>force the GM to reroll one d20 (you live with the result)</td></tr>"
  "</tbody></table>"
  "<p><strong>The Chosen:</strong> each PC's Choosing card silently keys ONE encounter that chapter — when it begins, that PC "
  "gains +1 status to rolls the chapter's ability drives, for the encounter (don't reveal it in advance). "
  "<strong>Endgame:</strong> the deck transcends — the full 54-draw <em>Harrow Deck of Many Things</em> rolltable and procedure "
  "live in the <em>7. Appendices &amp; Beyond</em> journal.</p></section>")

# --- (2) Conversion Guide: Reputation page — Guard rank-gates + concrete city tiers ---
patch_page("00-conversion-guide", "Reputation", "appGuardRanks",
  '<section class="skill" id="appGuardRanks"><p><strong>Korvosan Guard — ranks, gates &amp; benefits (Appendix 6, converted).</strong> '
  "Cressida inducts the PCs in Ch.1 (Event 9). Rank advances only at the gates below — deeds, not points:</p>"
  "<table><thead><tr><th>Rank</th><th>Gate</th><th>Benefits</th></tr></thead><tbody>"
  "<tr><td><strong>R1</strong></td><td>Induction (Ch.1, Event 9)</td><td>borrow up to 10 gp of gear per mission; +1 circumstance to Gather Information at guard posts</td></tr>"
  "<tr><td><strong>R2</strong></td><td>prove you're no crown agent — Trinia's escape (end Ch.1)</td><td>borrow 50 gp; <strong>Recovery 1</strong>; free retraining access (Citadel trainers)</td></tr>"
  "<tr><td><strong>R3</strong></td><td>a great service to the citizens — ending blood veil (end Ch.2)</td><td>borrow 100 gp; command a team (1d6 L3 guards, one mission); <strong>Recovery 2</strong></td></tr>"
  "<tr><td><strong>R4</strong></td><td>a personal, risky stand against the queen — rescuing Neolandus (end Ch.3; accusation without proof doesn't count)</td><td>borrow 250 gp; <strong>Recovery 3</strong></td></tr>"
  "</tbody></table>"
  "<p><strong>Recovery 1:</strong> an overnight at Citadel Volshyenek (Ch.1–3) or the Dead Warrens (Ch.4–6) restores all HP and grants one "
  "counteract attempt (+15) against a curse, disease, or blindness/deafness — <em>not available during Ch.2's plague peak</em>. "
  "<strong>Recovery 2:</strong> adds <em>restoration</em>-grade care and a <em>raise dead</em> (components covered or defrayed by the borrow limit). "
  "<strong>Recovery 3:</strong> adds <em>greater restoration</em>-grade care and <em>resurrection</em>-grade returns.</p></section>"
  + '<section class="conversion" id="appCityTiers"><p><strong>City Tiers — the concrete numbers (CHG-0012, shipped).</strong> '
  "Korvosa's five settlement states, converted (PF1e marketplace ÷10). Restock: 1d4 lesser (≤L8) / 1d2 mid (L9–12) / 1 high (L13+) new items per month of play; "
  "a wanted specific item is in stock on a "+chk("type:flat|dc:6")+" if at or under the tier's level cap.</p>"
  "<table><thead><tr><th>Tier</th><th>Typical trigger</th><th>Item level cap</th><th>Single-purchase cap</th><th>Hireling casting</th></tr></thead><tbody>"
  "<tr><td><strong>Baseline</strong> (L14 city)</td><td>Ch.1 start</td><td>L14</td><td>8,500 gp</td><td>7th rank</td></tr>"
  "<tr><td><strong>Unrest</strong></td><td>Ch.1 riots</td><td>L11</td><td>5,000 gp</td><td>5th rank</td></tr>"
  "<tr><td><strong>Plagued</strong></td><td>Ch.2 / Epidemic Clock ≥7</td><td>L10 — disease-cure consumables need a "+chk("type:flat|dc:11")+" to find at all</td><td>5,000 gp</td><td>5th rank</td></tr>"
  "<tr><td><strong>Martial Law</strong></td><td>Ch.3–5 (curfew dusk–dawn)</td><td>L8 lawful; black market L11 at +25% ("+chk("type:underworld-lore|dc:25")+" to reach)</td><td>2,500 gp</td><td>3rd rank (the crown keeps 7th)</td></tr>"
  "<tr><td><strong>Anarchy</strong></td><td>Ch.6 assault window</td><td>black market only, L11 at +50% ("+chk("type:underworld-lore|dc:20")+")</td><td>5,000 gp</td><td>5th rank</td></tr>"
  "</tbody></table>"
  "<p>Allied NPC casters (Ishani, the Pharasmins, Thousand Bones) serve regardless of tier — but if the queen learns of one, "
  "expect an arrest and a rescue hook (the Deathhead Vault holds more than rebels).</p></section>")

# --- (3) Conversion Guide: Campaign Backgrounds — goal→party-XP framework ---
patch_page("00-conversion-guide", "Campaign Backgrounds", "appBgGoals",
  '<section class="skill" id="appBgGoals"><p><strong>Background goals → party XP (stated once, here).</strong> '
  "Each campaign background implies a personal goal: unmask the one who <em>betrayed</em> you · bury the <em>addiction</em> and its supplier · "
  "clear your <em>framed</em> name in law · lay your <em>lost love</em> to rest · recover the <em>missing child</em> from the Lambs · "
  "outgrow the <em>unhappy childhood</em> by facing its author. When a PC resolves their goal on-screen, award the whole party a "
  "<strong>30 XP story award</strong> (or <strong>80 XP</strong> if it closes a chapter villain or thread) — once per background. "
  "Gaedren's fall usually pays the first; later chapters echo the rest (the betrayer can resurface in Ch.3's Old Korvosa, "
  "the framed PC's exoneration rides Ch.3's seneschal, the child's fate can thread all the way to the Gray Maidens).</p></section>")

# --- (4) Conversion Guide + Ch.3 journal: Becoming Blackjack made concrete ---
BLACKJACK_HTML = (
  '<p class="source"><em>Source: CotCT (2016 HC), Appendix 6 (Vencarlo Orisini / Becoming Blackjack) — pp.462-463.</em></p>'
  + B.s_milestone("<p><strong>Becoming Blackjack (subsystem).</strong> Blackjack is two hundred years of one mask — an identity handed to a single trainee per generation. Vencarlo Orisini is the current bearer; by campaign's end, a PC can be the next.</p>")
  + "<p><strong>The kit</strong> (hidden in Vencarlo's bag of holding): mask, cloak, gloves, boots, daggers, and his mother's keen rapier. <strong>Finding it:</strong> discoverable in Ch.3 Part 1 (his ransacked home); otherwise Vencarlo approaches a chosen PC between Ch.3 and Ch.4. He prefers a private heir but accepts party-wide knowledge if all swear secrecy.</p>"
  + B.s_skill("<p><strong>The mantle benefit:</strong> wearing the full kit and honoring the role, the bearer gains a <strong>+2 circumstance bonus to Deception, Diplomacy, and Intimidation against Korvosan citizens of non-noble station</strong> (explicitly including Pilts Swastel's court) — the city believes in Blackjack harder than it believes in itself. Blackjack is a true second identity for impersonation and renown purposes.</p>")
  + B.s_conv("<p><strong>The one-time rebuild:</strong> the inheritor may rebuild toward the role — reassign skill increases and feats (and, with GM blessing, class or subclass toward a swashbuckler/rogue silhouette). <strong>Deadline:</strong> the transition completes before the Deathhead Vault infiltration (Ch.4, Part 3). Vencarlo then retires (he keeps his stats; emergencies only). <strong>Ch.6 showcase:</strong> open the chapter with a beat built for the new Blackjack — the Trifaccia unmasking (Event 1) is tailor-made.</p>"))
add_page("00-conversion-guide", "appPgGuideBJ0001", "Becoming Blackjack (Mantle & Rebuild)", BLACKJACK_HTML)
add_page("03-escape-from-old-korvosa", "appPgBlackjack01", "Becoming Blackjack",
  BLACKJACK_HTML + "<p><strong>In this chapter:</strong> the kit can surface during Part 1 at "
  + "Vencarlo's ransacked home; if the PCs miss it, the offer comes after the Arkona rescue — the mantle should be settled before the party leaves for the Cinderlands.</p>", level=2)

# --- (5) Rumor Mill: CHG-0012 wording now true (we DO ship a scaffold table) ---
patch_replace("00-conversion-guide",
  "a rolltable to populate from your own Appendix 2 (we ship no rumor text)",
  "shipped as a scaffold rolltable (<em>Korvosa — Rumor Mill</em>: original paraphrase hooks with truth flags; chapter slots 17-20 are yours to seed)",
  "Korvosa — Rumor Mill")

# --- (6) Ch.4: the 5-pot warpaint grant now links real mechanics ---
patch_replace("04-a-history-of-ashes",
  "5 pots of Shoanti war paint",
  "5 pots of "+itm(IT["warpaint"], "Shoanti warpaint")+" (GM's pick of colors)",
  IT["warpaint"])

# --- (7) Ch.5: Serithtial item doc linked at its recovery scene (H4, the islet) ---
patch_page("05-skeletons-of-scarwall", "The Star Tower & the Sacred Lake", SERITHTIAL_ID,
  B.s_treasure("<p><strong>The prize (H4, the islet):</strong> the blade ships as an item doc — "
    + itm(SERITHTIAL_ID, "Serithtial")
    + " — drag it to the party when Kleestad falls. It stays a suppressed masterwork blade until the Scarwall curse breaks; the full awakened profile (and the only edge that can sunder the Crown) is on the item.</p>"))

# --- (8) Ch.6: Crown of Fangs item doc linked at the finale ---
patch_page("06-crown-of-fangs", "THE EVERDAWN POOL", CROWN_ID,
  B.s_treasure("<p><strong>The Crown itself:</strong> sundered or (unwisely) claimed, it ships as an item doc — "
    + itm(CROWN_ID, "The Crown of Fangs") + " — alongside " + itm(SERITHTIAL_ID, "Serithtial")
    + ". The wearer-corruption clock and the sunder profile (Hardness 20, HP 80 vs. Serithtial alone) live on the item.</p>"))

# --- (9) Inventory injections (Appendix 5 items into their bearers) ---
# Community Ileosa omits her AP-treasure ring — keep the injection, but embed the
# community item text so her copy matches the swapped items-pack doc.
ring_emb = B.community_doc("item", "Ring of Splendid Security") or copy.deepcopy(ring_splendid)
ring_emb["_id"] = EMB["ring"]; ring_emb.pop("_key", None); ring_emb["sort"] = 0
inject_item("queen-ileosa", ring_emb)

def remove_injected(actor_slug, item_id, why):
    """Strip a previously injected embedded copy (idempotent gear dedup)."""
    p = ASRC / f"{actor_slug}.json"
    if not p.exists():
        return
    d = _load(p)
    kept = [x for x in d["items"] if x["_id"] != item_id]
    if len(kept) != len(d["items"]):
        d["items"] = kept
        _save(p, d); print(f"  [inject] removed {item_id} from {actor_slug} ({why})")

# gear dedup vs community inventory: the swapped statblocks already carry these —
# Mask of the Mantis on the assassin, Smoke Bombs ×4 on Jolistina.
remove_injected("red-mantis-assassin", EMB["mask"], "community gear: Mask of the Mantis")
remove_injected("jolistina-susperio", EMB["smoke"], "community gear: Smoke Bomb ×4")

# --- (10) Havero: explicit 'tentacles-only by design' note on the ch4 actor ---
_hav = ASRC / "havero-tentacle.json"
if _hav.exists():
    _hd = _load(_hav)
    if "by design" not in _hd["system"]["details"]["publicNotes"]:
        _hd["system"]["details"]["publicNotes"] += ("<p><strong>Design note (Appendix 7):</strong> the full havero (CR 21) is "
          "deliberately not statted — the campaign only ever stages its reaching limbs. Severed tentacles buy passage; "
          "the body behind the wall is a reason to leave.</p>")
        _save(_hav, _hd); print("  [patch] havero-tentacle :: tentacles-only design note")

# --- (11) Adventure bundle: swap in the rebuilt (original-prose) Introduction ---
_advp = B.PACKS / "adventure" / "_source" / "cotct-edge-of-anarchy.json"
if _advp.exists():
    _adv = _load(_advp)
    _new = copy.deepcopy(intro_journal); _new.pop("_key", None)
    for _p in _new.get("pages", []): _p.pop("_key", None)
    _adv["journal"] = [(_new if j.get("_id") == INTRO_JID else j) for j in _adv["journal"]]
    _save(_advp, _adv); print("  [patch] adventure bundle :: Introduction replaced with original-prose version")
else:
    print("  [patch] SKIP adventure bundle (not built yet)")

print("Appendix build complete. (Run order matters: this script must run LAST.)")
