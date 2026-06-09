#!/usr/bin/env python3
"""Pilot journals (Old Fishery). Deterministic; live UUID links to actors/hazards/items."""
from __future__ import annotations
import json, pathlib, random
ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / "packs" / "journals" / "_source"
SRC.mkdir(parents=True, exist_ok=True)
MOD = "cotct-pf2e-conversion"

JID = {"overview":"PuUGEVunRqjIWFOj","fishery":"aO3z6QTqmYZCZYkw","npcs":"hnLhxaPI3vbCVFI2",
       "encounters":"WsefD5tDWGKzKU8x","treasure":"LAhqsOybawWEolxM","convnotes":"OmdAPBg10luB7GUr"}
A = {  # actor/hazard/item ids
 "gaedren":"RKfT6vJ5guinSBjo","yargin":"7uhbgkK2IOZOlJb3","hookshanks":"qH96VshE6CZqfajv","giggles":"mHUhxeaalWkTU1h4",
 "drainspider":"1M94tm3wnSRGcTG5","jigsawshark":"lsdWSvGJ81hDy4it","orphan":"UQr3ApF78GW7eghw",
 "boardwalk":"6y55S5DpXqnF40WL","rottendeck":"xMhIQZS6GokTsulZ",
 "brooch":"iNQaVcbkSM0VPXsa","harrowdeck":"DPDen8gco6rznX9Y","ledger":"I7HQNtjI9yPvQ4fA",
 "garnet":"dK4hnpH7s67RYnNI","coffer":"ymuRwMg6WfWIwkne","dagger":"b04PLWVkmm3RM4nm"}
# official monster-core actors
MC = {"crocodile":"2rMLYkUR47ZCQMUg","guarddog":"KHTYbQgR5hnFZdGL"}

def act(k, label=None): return f"@UUID[Compendium.{MOD}.cotct-actors.Actor.{A[k]}]" + (f"{{{label}}}" if label else "")
def haz(k, label=None): return f"@UUID[Compendium.{MOD}.cotct-hazards.Actor.{A[k]}]" + (f"{{{label}}}" if label else "")
def itm(k, label=None): return f"@UUID[Compendium.{MOD}.cotct-items.Item.{A[k]}]" + (f"{{{label}}}" if label else "")
def mc(k, label): return f"@UUID[Compendium.pf2e.pathfinder-monster-core.Actor.{MC[k]}]{{{label}}}"

_r = random.Random(20260610)
_ALPH = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
def pid(): return "".join(_r.choice(_ALPH) for _ in range(16))

def page(name, html, level=1, show_title=True):
    return {"_id": pid(), "name": name, "type": "text",
            "title": {"show": show_title, "level": level},
            "text": {"format": 1, "content": html}, "sort": 0,
            "ownership": {"default": -1}, "flags": {}, "system": {}}

def journal(idkey, name, pages):
    for i, p in enumerate(pages, 1):
        p["sort"] = i * 100000
    return {"_id": JID[idkey], "name": name, "pages": pages, "folder": None,
            "sort": 0, "ownership": {"default": 0}, "flags": {}}

def write(slug, doc):
    doc["_key"] = f"!journal!{doc['_id']}"
    # embedded pages are stored as separate leveldb entries with compound keys
    for p in doc.get("pages", []):
        p["_key"] = f"!journal.pages!{doc['_id']}.{p['_id']}"
    (SRC / f"{slug}.json").write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"  journals/{slug}.json  '{doc['name']}'  ({len(doc['pages'])} pages)")

SRCREF = "<p><em>Source: CotCT (2016 HC), Ch.1 'Edge of Anarchy', {area} — p.{pg}.</em></p>"

print("Building pilot journals...")

# =====================================================================
# 1) GM OVERVIEW & RUN SHEET
# =====================================================================
write("01-old-fishery-overview", journal("overview", "Old Fishery — GM Overview & Run Sheet", [
 page("Overview",
  "<p>This is the <strong>Phase-2 pilot</strong> conversion: the opening dungeon of Curse of the Crimson Throne — "
  "the hunt for crime-lord <strong>Gaedren Lamm</strong> in the <strong>Old Fishery</strong> (Westpier 17). It is "
  "the mandatory first dungeon and the emotional payoff for every PC's background hook.</p>"
  "<p><strong>Party:</strong> 4 PCs, <strong>level 1 → 2</strong> (milestone: level up to 2 on clearing the "
  "fishery). <strong>System:</strong> PF2e Remaster (Foundry v13 / pf2e 7.x).</p>"
  "<p><strong>Beat:</strong> the ghost-spirit Zellara draws the PCs together with a harrow reading and sends them "
  "to kill Gaedren, who hides in the fishery with his thugs, his pet crocodile <strong>Gobblegut</strong>, and his "
  "enslaved orphan pickpockets ('Lamm's Lambs'). The PCs recover Queen Ileosa's stolen brooch, Gaedren's coded "
  "ledger, and Zellara's haunted harrow deck — and, as they leave, the king dies and Korvosa erupts.</p>"
  "<p>Linked material: " + act("gaedren", "Gaedren Lamm") + " · "
  "Areas A1–A14 (this folder) · Encounters & balance journal · Treasure journal · Conversion Notes journal · "
  "and the project " + "<code>reports/</code> for exhaustive tables.</p>"),
 page("Zellara & the First Harrowing (lead-in)",
  SRCREF.format(area="Zellara's Home, 3 Lancet St.", pg="15–17") +
  "<p>The PCs each receive a personalized harrow card summoning them to Zellara's home at sunset. There they meet "
  "<strong>Zellara</strong>, a Varisian fortune-teller who asks them to bring Gaedren to justice — he murdered her "
  "son and stole her heirloom harrow deck. She performs a <strong>Harrowing</strong> to prepare them.</p>"
  "<p><strong>The twist:</strong> Zellara is already dead — a benign spirit. Her home is part illusion "
  "(see-through with <strong>Will DC 18</strong>); <em>detect magic</em> shows illusion, <em>detect undead</em> a "
  "faint aura. Discovering this early is fine (the AP says roll with it); the reveal lands fully in A14 when the PCs "
  "find her severed head and " + itm("harrowdeck", "her harrow deck") + ".</p>"
  "<p><strong>Harrowing (pilot stub, CHG-0010):</strong> run the reading as narrative foreshadowing — warn of "
  "coming unrest and that the PCs are fated to become heroes of Korvosa — then grant each PC a small pool of "
  "<strong>Harrow boons</strong> (extra Hero-Point-style rerolls themed by suit) for this chapter. Full Harrow "
  "rules are built with the Conversion Guide; the deck item carries the stub.</p>"),
 page("How to run it (pacing & tone)",
  "<p><strong>Korvosa = Gotham</strong> (community QoL consensus): splendor over crushing poverty, with a "
  "vigilante in the wings. Lean into the grime of the fishery and the plight of the orphans.</p>"
  "<ul>"
  "<li><strong>Tell players up front</strong> that Gaedren is a <em>connector</em>, not a final boss — this avoids "
  "the let-down of his quick defeat (the classic 'Lamm is a Lamb' problem). The campaign is about Korvosa, not "
  "just revenge.</li>"
  "<li><strong>Day vs night:</strong> by day, 9 orphans toil and the thugs patrol; doors to A7 are open, others "
  "locked. At night, all doors lock, 26 orphans sleep in A8, and " + mc("guarddog", "Bloo") + " roams A8 (alarm).</li>"
  "<li><strong>The alarm matters:</strong> Bloo's barks and a fleeing Yargin can forewarn Gaedren — reward stealth, "
  "but don't punish a loud party with an unwinnable boss (see Encounters journal).</li>"
  "<li><strong>The orphans are the heart.</strong> They are non-combatants; rescuing them — not killing through "
  "them — is the point. " + act("orphan", "Lamm's Lambs") + ".</li>"
  "</ul>"),
 page("Scene setup (maps & VTT) — no maps shipped",
  "<p><strong>No maps or art are shipped</strong> (copyright — CHG-0009). Supply your own legal copies.</p>"
  "<ul>"
  "<li><strong>Recommended map source:</strong> <em>Racooze's Curse of the Crimson Throne Battlemaps</em> (free "
  "Foundry module, Community Use) — use its <em>Old Fishery</em> scene. Otherwise drop your own image at "
  "<code>assets/maps/01-old-fishery.webp</code>.</li>"
  "<li><strong>Suggested scenes:</strong> (1) <em>Old Fishery — First Floor</em> (A1–A8) and (2) <em>Old Fishery — "
  "Lower Floor</em> (A9–A14), per the book's two-floor map. Grid 5 ft/square.</li>"
  "<li><strong>Token placements:</strong> Bloo in A4; Yargin A6; Hookshanks + 4 orphans A7; Giggles + 5 orphans "
  "A8; 1 drain spider A10, 4 in A11; jigsaw shark in the A12 water; Gaedren + Gobblegut at A13 (Gaedren across the "
  "pit, gator in the pool).</li>"
  "<li><strong>Walls/lighting:</strong> wall the boarded windows (vision-blocking, with the peer-slits as the "
  "AP notes); dim interior; the gator pool (A13) and underpier (A12) are deep water (difficult terrain / "
  "swimming). Pin the Slippery Boardwalk (A3) and Rotten Deck (A9) hazards as Foundry notes.</li>"
  "<li><strong>GM checklist:</strong> import maps → place tokens (drag the linked compendium actors; rename "
  "Crocodile→Gobblegut, Guard Dog→Bloo) → set the two hazards on their squares → pin this journal to the scene.</li>"
  "</ul>"),
 page("Advancement, XP & rewards",
  "<p><strong>Milestone:</strong> the party advances to <strong>level 2</strong> on clearing the fishery (defeating "
  "Gaedren / freeing the orphans). XP budgets are computed only for tuning (see Encounters journal & "
  "<code>reports/encounter_balance_report.md</code>).</p>"
  "<p><strong>Background payoffs</strong> (replacing PF1e campaign-trait XP): give a tangible beat to each PC whose "
  "hook resolves here — the 'Missing Child' PC finds their sibling among the orphans; 'Drug Addict' can destroy the "
  "shiver; 'Framed' decodes " + itm("ledger", "the ledger") + "; 'Betrayed/Love Lost' confront Gaedren directly.</p>"
  "<p><strong>Treasure</strong> is rebuilt to PF2e level 1→2 — see the Treasure journal. Don't restore PF1e gp.</p>"),
]))

# =====================================================================
# 2) AREAS A1–A14
# =====================================================================
areas = []
areas.append(("Fishery Features & Layout",
  SRCREF.format(area="A. Old Fishery", pg="17") +
  "<p>A decrepit but solid two-floor fishery on pilings over the Jeggare River, on a 13-ft embankment "
  "(Athletics DC 15 to climb the slick bank). Doors are wood (Hardness 5, low HP; Thievery DC 15 to pick, the "
  "brass key bypasses). Rendering rancid fish into slurry with orphan labor is the cover business.</p>"
  "<p><strong>Standing hazards:</strong> " + haz("boardwalk", "Slippery Boardwalk") + " (A3) and "
  + haz("rottendeck", "Rotten Ship Deck") + " (A9) — both can dump a PC into the water with "
  + act("jigsawshark", "the jigsaw shark") + " (A12).</p>"
  "<p><strong>Day/night:</strong> see the Run Sheet. Map: use Racooze's CotCT Battlemaps (Old Fishery) — none "
  "shipped (copyright). Scene-planning lives in the project scenes pack.</p>"))
areas.append(("A1 · Front Door",
  SRCREF.format(area="A1", pg="18") +
  "<p>Locked double doors (<strong>Thievery DC 15</strong>; knocking or a failed/loud pick brings "
  + act("yargin", "Yargin") + " from A6). A drooping signpost; brine-and-dead-fish reek.</p>"))
areas.append(("A2 · Loading Dock",
  SRCREF.format(area="A2", pg="18") +
  "<p>A 15-ft dock with tar-caked slurry barrels; stairs down to a riverside door near the water. Doors to A7 are "
  "open by day; the door to A8 is always locked (Thievery DC 15).</p>"))
areas.append(("A3 · Back Alley (hazard)",
  SRCREF.format(area="A3", pg="18–20") +
  "<p>The " + haz("boardwalk", "Slippery Boardwalk") + " clings to the south wall 13 ft above the river. Moving "
  "more than a Step (or fighting) on it risks a fall (Reflex/Acrobatics DC 15; crit fail → into the shark water). "
  "Heavy loads or two adjacent creatures can collapse a stretch. The A6 door is locked (Thievery DC 15).</p>"))
areas.append(("A4 · Front Room — Bloo (E1)",
  SRCREF.format(area="A4", pg="19") +
  "<p>A disused customer room; under the desk sleeps " + mc("guarddog", "Bloo") + ", Yargin's foul cur (use "
  "<strong>Guard Dog</strong>, rename the token). He attacks strangers on sight and his barks rouse the fishery. "
  "<strong>E1, Trivial (20 XP).</strong> Silence him fast (Stealth/Diplomacy to avoid, or a quick kill).</p>"))
areas.append(("A5 · Barracks",
  SRCREF.format(area="A5", pg="20") +
  "<p>The three thugs' bunkroom. They distrust each other and keep no valuables here.</p>"))
areas.append(("A6 · Yargin's Office (E2)",
  SRCREF.format(area="A6", pg="19–21") +
  "<p>" + act("yargin", "Yargin Balko") + ", Gaedren's acid-throwing fence, works here. <strong>E2, Low (40 XP).</strong> "
  "He opens with thrown Acid Flasks, then a light crossbow; <strong>if losing he flees down the hidden trapdoor to "
  "warn Gaedren.</strong></p>"
  "<p><strong>Hidden trapdoor</strong> (Perception DC 18 to spot; barred — Athletics DC 17 to force) drops to A13 — "
  "a flanking shortcut onto the boss. Yargin carries the <strong>brass key</strong> (all fishery doors).</p>"))
areas.append(("A7 · Upper Workroom — Hookshanks (E3)",
  SRCREF.format(area="A7", pg="20–22") +
  "<p>Slurry-prep room; 4 orphans toil under " + act("hookshanks", "Hookshanks Gruller") + ", a gnome who hides "
  "among the children (Perception DC 17 to pick him out). <strong>E3, Low (40 XP).</strong> He can surrender and "
  "inform. The 4 " + act("orphan", "orphans") + " are non-combatants — rally them (Diplomacy DC 15). Slippery floor "
  "(Acrobatics DC 15 if moving fast). Petty-cash cabinet locked (Thievery DC 15).</p>"))
areas.append(("A8 · Fishery Floor — Giggles (E4)",
  SRCREF.format(area="A8", pg="21–22") +
  "<p>The main slurry floor (8-ft tarred vat, catwalks, a hole to the river). " + act("giggles", "Giggles") +
  " oversees 5 orphans by day (26 sleep here at night). <strong>E4, Low (40 XP; 60 with Bloo at night).</strong> "
  "Giggles tries to <strong>capture</strong> PCs nonlethally for Gaedren, then fights to the death (Orc Ferocity). "
  "The hole in the floor drops to the underpier/water — beware feeding PCs to " + act("jigsawshark", "the shark") + ".</p>"))
areas.append(("A9 · Kraken's Folly (hazard)",
  SRCREF.format(area="A9", pg="23–24") +
  "<p>A derelict ship lashed to the pilings. The " + haz("rottendeck", "Rotten Ship Deck") + " (foredeck) collapses "
  "under Medium+ weight (Reflex DC 16 or fall to A11 for 1d6 + prone among the spiders); the stern is sound. "
  "Stairs down to the spider nest (A10/A11).</p>"))
areas.append(("A10 · Spider Nest (E5)",
  SRCREF.format(area="A10", pg="24") +
  "<p>Aft cabin lair of a single " + act("drainspider", "drain spider") + " that lunges at the first to enter. "
  "<strong>E5, Trivial (20 XP).</strong> Repelled by the vermin repellent looted in A13.</p>"))
areas.append(("A11 · Kraken's Hold (E6)",
  SRCREF.format(area="A11", pg="24") +
  "<p>Four more " + act("drainspider", "drain spiders") + " infest the hold. <strong>E6, Moderate (80 XP)</strong> — "
  "or <strong>trivialized</strong> if the PCs coat themselves in vermin repellent first. A hull secret door "
  "(Perception DC 17; +2 if Survival DC 15 tracked Gaedren's path) leads to A12 and the boss.</p>"))
areas.append(("A12 · Underpier (E7)",
  SRCREF.format(area="A12", pg="24–25") +
  "<p>A floating walkway under the fishery; Gaedren's skiffs (his escape route) are tied here. "
  + act("jigsawshark", "A jigsaw shark") + " patrols the water. <strong>E7, Low (40 XP), avoidable</strong> — it "
  "attacks anyone in the water but only leaps onto the walkway if attacked first. The small (2½-ft) locked door "
  "(Thievery DC 17) leads to A13.</p>"))
areas.append(("A13 · Gaedren's Playground — BOSS (E8)",
  SRCREF.format(area="A13", pg="24–26") +
  "<p><strong>The climax.</strong> A chamber over a water pit holding " + mc("crocodile", "Gobblegut") +
  " (use <strong>Crocodile</strong>, rename the token); two 5-ft walkways cross the pit. " + act("gaedren", "Gaedren Lamm") +
  " sorts loot here.</p>"
  "<p><strong>E8, SEVERE (120 XP) at level 1</strong> (Moderate at level 2): Gaedren (L2) + Gobblegut (L2). Gaedren "
  "opens with <em>Spur the Beast</em> — shooting Gobblegut to enrage it — then snipes from across the pit while the "
  "gator menaces anyone near the water. He flees toward the A12 skiffs at ≤8 HP. <strong>Reaching him means "
  "crossing the gator's water.</strong> Full tactics & party-size scaling: Encounters journal.</p>"
  "<p>Loot on the tables: " + itm("coffer", "a darkwood coffer + 20 shiver doses + 7 vermin repellent") + ".</p>"
  "<p><strong>⚠ Track:</strong> if the PCs leave Gaedren's body here, his son Rolth animates it as a zombie in the "
  "Dead Warrens (Ch.1 Part 3, area D13).</p>"))
areas.append(("A14 · Gaedren's Den (treasure & the reveal)",
  SRCREF.format(area="A14", pg="26–28") +
  "<p>Gaedren's filthy bedroom/study. A locked strongbox (rusty iron key on Gaedren; or Thievery DC 15) holds his "
  "hoard, including " + itm("brooch", "Queen Ileosa's Brooch") + " (launches the next beat). On the dresser, a "
  "hatbox holds <strong>Zellara's severed head</strong> (Medicine DC 14: dead for weeks — the reveal) and "
  + itm("harrowdeck", "her haunted harrow deck") + ". Atop the strongbox: " + itm("ledger", "Gaedren's coded ledger") +
  " (Society DC 17 to decode). Full parcel: Treasure journal.</p>"))
write("02-old-fishery-areas", journal("fishery", "Old Fishery — Areas (A1–A14)",
    [page(n, h) for n, h in areas]))

# =====================================================================
# 3) NPCs & CREATURES
# =====================================================================
write("03-old-fishery-npcs", journal("npcs", "Old Fishery — NPCs & Creatures", [
 page("Villains (custom builds)",
  "<ul>"
  "<li>" + act("gaedren", "Gaedren Lamm") + " (L2) — first villain; frail sniper who weaponizes Gobblegut. A13.</li>"
  "<li>" + act("yargin", "Yargin Balko") + " (L1) — acid-throwing fence; flees to warn Gaedren. A6.</li>"
  "<li>" + act("hookshanks", "Hookshanks Gruller") + " (L1) — gnome taskmaster hiding among orphans; can inform. A7.</li>"
  "<li>" + act("giggles", "Giggles") + " (L1) — half-orc bruiser; nonlethal capturer. A8.</li>"
  "</ul><p>Rationale & stat-design notes: <code>reports/npc_monster_conversion_report.md</code>.</p>"),
 page("Creatures",
  "<ul>"
  "<li>" + mc("crocodile", "Gobblegut") + " — <strong>use the official Crocodile</strong> (L2); rename the token. The real threat in E8.</li>"
  "<li>" + mc("guarddog", "Bloo") + " — <strong>use the official Guard Dog</strong> (L−1); the alarm dog. A4/A8.</li>"
  "<li>" + act("drainspider", "Drain Spider") + " (L−1) — nest vermin; repelled by vermin repellent. A10/A11.</li>"
  "<li>" + act("jigsawshark", "Jigsaw Shark") + " (L1) — under-fishery hazard-creature; avoidable. A12.</li>"
  "</ul>"),
 page("The Orphans (Lamm's Lambs)",
  act("orphan", "Lamm's Lambs") + " are <strong>non-combatants</strong> and the moral core of the dungeon. 9 by "
  "day, 26 at night (A8). <strong>Rally</strong> with Diplomacy DC 15 (Intimidation fails). They can Aid or reveal "
  "info; ignored, they may be forced to act for the thugs. <strong>Never an XP source for killing.</strong> "
  "Rescuing them is the chapter's heart (and a background payoff for 'Missing Child').</p>"),
 page("Allies — Zellara",
  "<p><strong>Zellara</strong> — the murdered fortune-teller, now a benign spirit bound to " +
  itm("harrowdeck", "her harrow deck") + ". She convenes the PCs and performs the recurring Harrowing. Run as a "
  "story NPC (no stat block). The deck is recovered in A14 and anchors the Harrow subsystem (CHG-0010).</p>"),
]))

# =====================================================================
# 4) ENCOUNTERS & BALANCE
# =====================================================================
write("04-old-fishery-encounters", journal("encounters", "Old Fishery — Encounters & Balance", [
 page("Encounter table (party level 1)",
  "<p>Budget (4 players): Trivial 40 / Low 60 / Moderate 80 / Severe 120 / Extreme 160. Full analysis & party-size "
  "scaling: <code>reports/encounter_balance_report.md</code>.</p>"
  "<table><thead><tr><th>#</th><th>Area</th><th>Foes</th><th>XP</th><th>Difficulty</th></tr></thead><tbody>"
  "<tr><td>E1</td><td>A4</td><td>Bloo (−1)</td><td>20</td><td>Trivial (alarm)</td></tr>"
  "<tr><td>E2</td><td>A6</td><td>Yargin (1)</td><td>40</td><td>Low</td></tr>"
  "<tr><td>E3</td><td>A7</td><td>Hookshanks (1) + orphans*</td><td>40</td><td>Low</td></tr>"
  "<tr><td>E4</td><td>A8</td><td>Giggles (1) [+Bloo]</td><td>40–60</td><td>Low</td></tr>"
  "<tr><td>E5</td><td>A10</td><td>Drain Spider (−1)</td><td>20</td><td>Trivial</td></tr>"
  "<tr><td>E6</td><td>A11</td><td>4× Drain Spider (−1)</td><td>80</td><td>Moderate**</td></tr>"
  "<tr><td>E7</td><td>A12</td><td>Jigsaw Shark (1)</td><td>40</td><td>Low (avoidable)</td></tr>"
  "<tr><td><strong>E8</strong></td><td>A13</td><td><strong>Gaedren (2) + Gobblegut/Crocodile (2)</strong></td><td><strong>120</strong></td><td><strong>SEVERE</strong></td></tr>"
  "</tbody></table>"
  "<p>*orphans non-combatant. **trivialized by vermin repellent.</p>"),
 page("E8 — Boss tactics & scaling",
  "<p><strong>The fix for 'Lamm is a Lamb':</strong> the danger is the crocodile, not the old man. " +
  act("gaedren", "Gaedren") + " opens with <em>Spur the Beast</em> (shoot " + mc("crocodile", "Gobblegut") +
  " to enrage it: +2 status to atk/dmg, forced to attack the nearest non-Gaedren creature), then snipes from across "
  "the pit and uses <em>Nimble Dodge</em>. Crossing the two 5-ft walkways to reach him means braving the gator's "
  "water (Grab → drag under). Gaedren flees to the A12 skiffs at ≤8 HP.</p>"
  "<table><thead><tr><th>PCs</th><th>Build</th></tr></thead><tbody>"
  "<tr><td>3</td><td>Gaedren (L2) + <strong>Weak</strong> Crocodile (≈90 XP)</td></tr>"
  "<tr><td>4</td><td><strong>As written</strong> (120 XP, Severe)</td></tr>"
  "<tr><td>5</td><td>+1 Drain Spider from the pool, or <strong>Elite</strong> Crocodile (≈150)</td></tr>"
  "<tr><td>6</td><td><strong>Elite</strong> Crocodile + Gaedren, or +2 Drain Spiders (≈160)</td></tr>"
  "</tbody></table>"
  "<p><strong>Alarm state:</strong> if Yargin reached Gaedren or Bloo's barks carried, start Gaedren in cover with "
  "Gobblegut pre-enraged (he acts round 1). Don't make a loud approach unwinnable — it just removes the surprise.</p>"),
]))

# =====================================================================
# 5) TREASURE
# =====================================================================
write("05-old-fishery-treasure", journal("treasure", "Old Fishery — Treasure", [
 page("Converted parcels (level 1 → 2)",
  "<p>Rebuilt to PF2e Treasure-by-Level — the community conversion omits treasure (CHG-0008). Do <strong>not</strong> "
  "restore PF1e gp. Full table & budget check: <code>reports/treasure_report.md</code>.</p><ul>"
  "<li>" + itm("dagger", "+1 Dagger (Gaedren's)") + " — boss loot; first permanent magic weapon.</li>"
  "<li>+1 armor potency (Gaedren's '+1 padded') — boss loot (or a level-2 minor item).</li>"
  "<li>A14 hoard → a 1st-rank scroll + ~50 gp re-priced gems.</li>"
  "<li>" + itm("garnet", "Garnet (Yargin)") + " (~8 gp) · " + itm("coffer", "Darkwood coffer + vermin repellent") + " (~12 gp).</li>"
  "<li>2× Acid Flask (lesser) + Thunderstone (Yargin's gear); 3× minor Healing Potion (Giggles); ~30 gp thug coin.</li>"
  "<li>" + itm("ledger", "Coded ledger") + " → Guard bounty 15 gp (30 w/ cipher key).</li>"
  "</ul>"),
 page("Story items",
  "<ul>"
  "<li>" + itm("brooch", "Queen Ileosa's Brooch") + " — returning it launches the queen's audience (Event 8) → "
  "recruitment + the queen's reward parcel (next section). Loot value trivial; narrative value high.</li>"
  "<li>" + itm("harrowdeck", "Zellara's Harrow Deck") + " — the recurring Harrow subsystem (CHG-0010); later "
  "becomes the Harrow Deck of Many Things (Ch.6).</li>"
  "<li>Shiver (in the coffer) — story drug, not loot; destroying it pays off a 'Drug Addict' hook.</li>"
  "</ul>"),
]))

# =====================================================================
# 6) CONVERSION NOTES (Changes from Original)
# =====================================================================
write("06-old-fishery-conversion-notes", journal("convnotes", "Old Fishery — Conversion Notes (Changes from Original)", [
 page("Changes from the original (GM-facing)",
  "<p>Per-area changes for the pilot; mirrors <code>conversion_change_log.md</code>. Format: <em>original → "
  "new → reason</em>.</p><ul>"
  "<li><strong>Gaedren rebuilt as a credible Severe (with Gobblegut)</strong> rather than a one-round pushover "
  "— <em>Reason:</em> the famous 'Lamm is a Lamb' anticlimax (community consensus) + PF2e solo-boss math. "
  "<em>Impact:</em> the emotional climax actually lands; the gator is the threat. <strong>Severity: Moderate.</strong> "
  "Added <em>Spur the Beast</em> + <em>Nimble Dodge</em>; kept Limping Gait. ⚠ Confirm Severe @L1 vs running at L2.</li>"
  "<li><strong>Gobblegut & Bloo referenced as official Crocodile / Guard Dog</strong> — <em>Reason:</em> clean "
  "PF2e equivalents (use-official-actor method). <em>Impact:</em> none narrative. Cosmetic.</li>"
  "<li><strong>Blood/save-or-X & ability-damage absent</strong> here — the only affliction is the rebuilt "
  "<strong>Drain Spider Venom</strong> (PF1e Con-drain → PF2e 1-stage poison + enfeebled). Minor.</li>"
  "<li><strong>All DCs re-derived</strong> from PF2e level-based/simple DCs (locked-door spam collapsed; see "
  "<code>reports/dc_skill_report.md</code>). Minor.</li>"
  "<li><strong>Treasure fully rebuilt</strong> to PF2e level 1→2; PF1e gp discarded (CHG-0008). Moderate (mechanical).</li>"
  "<li><strong>Harrowing → PF2e stub</strong> (Hero-Point-style boons via " + itm("harrowdeck", "the deck") + "; "
  "CHG-0010). Subsystem framework built with the Conversion Guide. Moderate.</li>"
  "<li><strong>Orphans = explicit non-combatants</strong> with Rally/Aid + Cower (PF1e already non-lethal-leaning) "
  "— <em>Reason:</em> make the moral framing mechanical & safe. Cosmetic/QoL.</li>"
  "<li><strong>QoL framing kept:</strong> 'Gaedren is a connector', day/night alarm logic, rescue-the-orphans as "
  "the heart — surfaced in the Run Sheet (community QoL consensus). Cosmetic.</li>"
  "</ul>"
  "<p><strong>Story preserved:</strong> plot, villain, location flow, and the king's-death cliffhanger are unchanged. "
  "<strong>No major (approval-gated) story changes in the pilot.</strong></p>"),
 page("Continuity hooks forward",
  "<ul>"
  "<li><strong>Leave Gaedren's body</strong> → Rolth animates it in the Dead Warrens (D13). Track party choice.</li>"
  "<li><strong>Queen's Brooch</strong> → Event 8 audience → recruitment by Cressida Kroft / the Korvosan Guard.</li>"
  "<li><strong>Zellara's deck</strong> → recurring Harrowings every chapter; Deck of Many Things in Ch.6.</li>"
  "<li><strong>If Gaedren escapes</strong> → recurs via Rolth (Ch.2). Note it in the campaign state.</li>"
  "</ul>"),
]))

print("Pilot journals built.")
