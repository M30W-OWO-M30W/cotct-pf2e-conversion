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
A2 = {"graymaiden": "grayMaidenFoot01"}
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

# =====================================================================
# JOURNAL — "2. Seven Days to the Grave" (front matter; missions follow)
# =====================================================================
SR = lambda area, p: f'<p class="source"><em>Source: CotCT (2016 HC), Ch.2, {area} — p.{p}.</em></p>'
def page(_id, name, html, level=2): return B.page(_id, name, html, level=level)
pages = []

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

journal = B.journal_entry(JID2, "2. Seven Days to the Grave", pages, folder=ADV_FOLDER)
B.write("journals", "02-seven-days-to-the-grave", copy.deepcopy(journal), embed_pages=True)

print(f"Chapter 2 (front matter) built: {len(folders)} folders, {len(actors)} actors, 1 journal ({len(pages)} pages).")
