#!/usr/bin/env python3
"""Emit pf2e AUTOMATION docs (drag-and-drop effect items) into the items pack:
the Blood Veil disease + its Ch.2 suppressant, the eight Shoanti war-paint
effects, and three campaign marker effects (Ukwar's Drain, Whispers of the
Crown, Serithtial's Wrath). Runs after build_community.py (and before
build_adventure.py) in sync_to_foundry.sh, then idempotently patches the
Conversion Guide's Blood Veil page to link the new docs (same patch pattern
as build_appendix.py).

Schema provenance — copied EXACTLY from the installed pf2e 8.2.0 system
(scripts/extract_afflictions.mjs → scripts/affliction_samples.json):
  * "effect" item: Effect: Ghostbane Fulu (pf2e.equipment-effects), plus the
    badge shapes of Spell Effect: Touch of the Moon (counter + labels) and
    Effect: Remaining Air (counter + min/max).
  * "affliction" item: NO sample exists — pf2e 8.2.0 ships ZERO
    affliction-type compendium docs across all 97 packs AND deletes the
    subtype at init (`delete game.system.documentTypes.Item.affliction`,
    pf2e.mjs). Blood Veil therefore ships as a clearly-structured effect
    with the stages in the description; flagged on the doc itself."""
import json, pathlib, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import pf2e_build as B

FLD = "appItemFolder001"                     # Appendix: Equipment & Magic folder
# items shipped by earlier builders that these effects ride on (stable ids)
UKWAR_ITEM, CROWN_ITEM, SERITHTIAL_ITEM = "appUkwarAxe00001", "crownOfFangs0001", "serithtialSword1"
GUIDE_JID, GUIDE_BV_PAGE = "cotctGuide000001", "R96jUmyAvMxCISST"
CH2_JID, CH2_CURE_PAGE = "ch2SevenDaysJrn1", "iNq7BMF0o3J1WGli"

BLOODVEIL_ID, SUPPRESSANT_ID = "fxBloodVeil00001", "fxBVSuppressant1"

def itm(iid, label):
    return f"@UUID[Compendium.{B.MOD}.cotct-items.Item.{iid}]{{{label}}}"

def jpage(jid, pid, label):
    return f"@UUID[Compendium.{B.MOD}.cotct-journals.JournalEntry.{jid}.JournalEntryPage.{pid}]{{{label}}}"

def effect(_id, name, slug, img, level, desc, unit="unlimited", value=-1,
           rules=None, badge=None, traits=None, flags=None):
    """pf2e "effect" item — field set copied from Effect: Ghostbane Fulu
    (pf2e.equipment-effects, system 8.2.0). Unlimited durations use the
    official value=-1 / expiry=null convention."""
    assert len(_id) == 16 and _id.isalnum(), f"bad effect id: {_id!r}"
    system = {
        "description": {"value": desc},
        "duration": {"expiry": None if unit == "unlimited" else "turn-start",
                     "sustained": False, "unit": unit,
                     "value": -1 if unit == "unlimited" else value},
        "level": {"value": level},
        "publication": dict(B.PUB),
        "rules": rules or [],
        "start": {"initiative": None, "value": 0},
        "tokenIcon": {"show": True},
        "traits": {"value": traits or []},
        "slug": slug,
    }
    if badge:
        system["badge"] = badge
    return {"_id": _id, "img": img, "name": name, "type": "effect", "effects": [],
            "folder": FLD, "sort": 0, "ownership": {"default": 0},
            "flags": flags or {}, "_stats": dict(B.STATS), "system": system}

# ---------------------------------------------------------------------------
# 1) Blood Veil — the staged disease (affliction FALLBACK: see module docstring)
# ---------------------------------------------------------------------------
BV_DESC = (
    "<p><strong>Disease (manufactured)</strong> — Vorel's phage, weaponized by the cult of"
    " Urgathoa at Queen Ileosa's order (Ch.2). <strong>Saving Throw</strong>"
    " @Check[type:fortitude|dc:24] for ordinary exposure, rising to @Check[type:fortitude|dc:30]"
    " against concentrated sources (the cult's brewing vats and raw fluids); on a critical"
    " failure the victim <strong>skips the onset</strong> and immediately suffers Stage 1."
    " <strong>Onset</strong> 1 day.</p>"
    f"<p><strong>Stage 1</strong> {B.cond('enfeebled', 'Enfeebled 1')} (1 day);"
    f" <strong>Stage 2</strong> {B.cond('enfeebled', 'Enfeebled 2')} and {B.cond('drained', 'Drained 1')} (1 day);"
    f" <strong>Stage 3</strong> {B.cond('enfeebled', 'Enfeebled 2')} and {B.cond('drained', 'Drained 2')} (1 day);"
    f" <strong>Stage 4</strong> {B.cond('drained', 'Drained 3')} and {B.cond('enfeebled', 'Enfeebled 3')}.</p>"
    "<p><strong>Using this doc:</strong> apply the effect to an infected creature, set its"
    " badge to the current stage, and apply the linked conditions by hand (the PF1e Con+Cha"
    " damage becomes drained/enfeebled). The"
    f" {itm(SUPPRESSANT_ID, 'suppressant')} halts progression and steps the stage down one"
    " per day rather than curing outright; the epidemic itself runs on the"
    f" {jpage(GUIDE_JID, GUIDE_BV_PAGE, 'Epidemic Clock')}.</p>"
    "<p><em>Why not an affliction-type item: pf2e 8.2.0 ships no affliction-type compendium"
    " docs and disables the subtype at init, so this is a structured effect instead (see"
    " this doc's flags).</em></p>")

# ---------------------------------------------------------------------------
# 2) Effect items
# ---------------------------------------------------------------------------
SUPP_DESC = (
    f"<p>The Chapter 2 'cure', engineered from the researchers' note-sets — see"
    f" {jpage(CH2_JID, CH2_CURE_PAGE, 'Curing Blood Veil')} for crafting checks, time, and"
    " dose costs (~4 doses/day, or single doses at ~10 gp).</p>"
    f"<p><strong>On taking a dose:</strong> {itm(BLOODVEIL_ID, 'Blood Veil')} stops"
    " progressing, and its stage steps <strong>down</strong> by 1 each day until it ends —"
    " a suppression, not a cure. <strong>The mercy in its design:</strong> for 1 week after,"
    " the treated person <em>spreads the cure</em> by contact exactly as Blood Veil itself"
    " spread.</p>"
    "<p><strong>Suppresses, never cures:</strong> the cult keeps re-seeding the plague at a"
    " slow burn, and it only truly ends when Ileosa falls (Ch.6). Distributing doses"
    f" <strong>recedes the {jpage(GUIDE_JID, GUIDE_BV_PAGE, 'Epidemic Clock')} by 1</strong>."
    " (Removability hatch: at any chapter break the GM may rule this became a true cure.)</p>")

UKWAR_DESC = (
    f"<p>Once per day, the intelligent battleaxe {itm(UKWAR_ITEM, 'Ukwar')} drinks from her"
    " wielder: the first time each day she draws blood in anger, her wielder attempts"
    f" @Check[type:fortitude|dc:30] or becomes {B.cond('drained', 'Drained 1')}.</p>"
    "<p>Apply this effect to the wielder when the bite lands; it expires after a day,"
    " signalling that her thirst has returned. The drained condition itself recovers as"
    " normal (it is not tied to this marker).</p>")

CROWN_DESC = (
    f"<p>The corruption-clock carrier for {itm(CROWN_ITEM, 'The Crown of Fangs')}: a"
    " <strong>non-Ileosa wearer</strong> attempts @Check[type:will|dc:40] per week worn"
    " or the whispers take root — the soul-seed of Kazavon begins the campaign's horror"
    " over again in a new vessel.</p>"
    "<p>Apply this effect to any non-Ileosa creature that invests the crown; tick the badge"
    " up each week worn (it tracks failed saves at the GM's preference). The second soul"
    " grows with every day worn and every death defied. The crown's own"
    " @Check[type:will|dc:42] dominate (3/day) and its sunder profile live on the item"
    " doc.</p>")

SERITHTIAL_DESC = (
    f"<p>The anti-Ileosa rider of awakened {itm(SERITHTIAL_ITEM, 'Serithtial')}: while the"
    " blade has damaged a bearer of Kazavon's essence (Queen Ileosa, the taniniver, Kazavon"
    " himself) this round, that creature's <strong>regeneration is suppressed</strong> —"
    " and each hit forces @Check[type:fortitude|dc:35] or"
    f" {B.cond('drained', 'Drained 1')} (<strong>cumulative</strong>).</p>"
    "<p>Apply this marker to Ileosa when Serithtial first wounds her; use the badge to track"
    " the accumulated drained value across the fight. Only Serithtial can sunder the Crown"
    " of Fangs (Hardness 20, HP 80 against this blade alone).</p>")

# Shoanti war paints — mechanics from the community jar docs (community/items/
# shaonti-war-paint-*.json; jar = consumable with 10 uses, emitted by
# build_community.py). One color at a time; 1 hour. Rule elements where a simple
# RE is faithful; description-only where automation would be fragile.
WAR_PAINTS = {
    # color: (id, mechanics-html, rules, fragile-note)
    "black": ("fxWarPaintBlack1",
        "<p>You become cloaked in shadows and smoke, gaining the effects of a"
        " @UUID[Compendium.pf2e.spells-srd.Item.3JG1t3T4mWn6vTke]{Blur} spell.</p>"
        "<p><em>No rule element: concealment from blur is rolled per-attack by the GM"
        " (automation would be fragile).</em></p>", []),
    "blue": ("fxWarPaintBlue01",
        "<p>You gain a 10-foot item bonus to your base Speed.</p>",
        [{"key": "FlatModifier", "selector": "land-speed", "type": "item", "value": 10}]),
    "green": ("fxWarPaintGreen1",
        "<p>When you use the @UUID[Compendium.pf2e.spells-srd.Item.IAjvwqgiDr3qGYxY]{Inspire"
        " Courage} composition cantrip, the status bonus granted increases by 1.</p>"
        "<p><em>No rule element: the bonus rides on the bard's own aura effect"
        " (automation would be fragile).</em></p>", []),
    "orange": ("fxWarPaintOrang1",
        "<p>You gain resistance 5 to physical damage.</p>",
        [{"key": "Resistance", "type": "physical", "value": 5}]),
    "red": ("fxWarPaintRed001",
        "<p>You gain resistance 10 to fire damage.</p>",
        [{"key": "Resistance", "type": "fire", "value": 10}]),
    "silver": ("fxWarPaintSilvr1",
        "<p>You gain a +2 item bonus to your AC.</p>",
        [{"key": "FlatModifier", "selector": "ac", "type": "item", "value": 2}]),
    "white": ("fxWarPaintWhite1",
        "<p>You gain a +2 item bonus to all saving throws against spells with the negative"
        f" (void) trait. In addition, anytime you gain the {B.cond('drained', 'Drained')}"
        " condition, reduce its value by 1; the white war paint absorbs the energy and"
        " fades away, ending this effect immediately (remove it by hand — the absorption"
        " is once, then gone).</p>",
        [{"key": "FlatModifier", "selector": "saving-throw", "type": "item", "value": 2,
          "predicate": [{"or": ["item:trait:void", "item:trait:negative"]}]}]),
    "yellow": ("fxWarPaintYello1",
        "<p>You gain a +2 item bonus to your Perception checks. When you roll a success on"
        " a Perception check, you get a critical success instead.</p>",
        [{"key": "FlatModifier", "selector": "perception", "type": "item", "value": 2},
         {"key": "AdjustDegreeOfSuccess", "selector": "perception",
          "adjustment": {"success": "criticalSuccess"}}]),
}

# ---------------------------------------------------------------------------
# guide patch (idempotent — same pattern as build_appendix.py's patch_page)
# ---------------------------------------------------------------------------
def patch_guide():
    p = B.PACKS / "journals" / "_source" / "00-conversion-guide.json"
    if not p.exists():
        print("  [patch] SKIP 00-conversion-guide (not built yet — re-run after pilot/appendix)")
        return
    d = json.loads(p.read_text(encoding="utf-8"))
    for page in d["pages"]:
        if "Blood Veil" not in page["name"]:
            continue
        if BLOODVEIL_ID in page["text"]["content"]:        # marker: already patched
            return
        page["text"]["content"] += (
            '<section class="conversion"><p><strong>Automation docs (items compendium):</strong> '
            + itm(BLOODVEIL_ID, "Blood Veil (Affliction)")
            + " — the staged disease above as an applyable effect with a stage badge (1–4) — and "
            + itm(SUPPRESSANT_ID, "Effect: Blood Veil Suppressant")
            + " — the Ch.2 cure-that-suppresses. Apply the affliction to an infected creature,"
              " set the badge to its stage, and let the suppressant step it back down.</p></section>")
        p.write_text(json.dumps(d, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"  [patch] 00-conversion-guide :: {page['name']} (affliction + suppressant links)")
        return
    print("  [patch] Blood Veil page NOT FOUND in 00-conversion-guide")

# ---------------------------------------------------------------------------
def main():
    docs = []

    docs.append(("blood-veil-affliction", effect(
        BLOODVEIL_ID, "Blood Veil (Affliction)", "blood-veil-affliction",
        "systems/pf2e/icons/spells/abyssal-plague.webp", 7, BV_DESC,
        badge={"labels": ["Stage 1", "Stage 2", "Stage 3", "Stage 4"],
               "loop": False, "type": "counter", "value": 1},
        flags={B.MOD: {"afflictionFallback": True, "note":
               "pf2e 8.2.0 ships zero affliction-type compendium docs and deletes the "
               "'affliction' Item subtype at init (pf2e.mjs); shipped as a structured "
               "effect per scripts/extract_afflictions.mjs findings."}})))

    docs.append(("effect-blood-veil-suppressant", effect(
        SUPPRESSANT_ID, "Effect: Blood Veil Suppressant", "effect-blood-veil-suppressant",
        "systems/pf2e/icons/equipment/alchemical-items/alchemical-elixirs/antiplague.webp",
        7, SUPP_DESC)))

    for color, (cid, mech, rules) in WAR_PAINTS.items():
        jar = json.loads((B.ROOT / "community" / "items" /
                          f"shaonti-war-paint-{color}.json").read_text(encoding="utf-8"))
        desc = (f"<p>Granted by {itm(jar['_id'], f'Shoanti War Paint ({color.title()})')}"
                " — one application, lasting 1 hour. You can benefit from only one color of"
                " Shoanti war paint at a time; applying a different color replaces this"
                " effect.</p><hr />" + mech)
        docs.append((f"effect-war-paint-{color}", effect(
            cid, f"Effect: Shoanti War Paint ({color.title()})", f"effect-war-paint-{color}",
            jar["img"], jar["system"]["level"]["value"], desc,
            unit="hours", value=1, rules=rules)))

    docs.append(("effect-ukwars-drain", effect(
        "fxUkwarDrain0001", "Effect: Ukwar's Drain", "effect-ukwars-drain",
        "systems/pf2e/icons/equipment/weapons/battle-axe.webp", 12, UKWAR_DESC,
        unit="days", value=1)))

    docs.append(("effect-whispers-of-the-crown", effect(
        "fxCrownWhisper01", "Effect: Whispers of the Crown", "effect-whispers-of-the-crown",
        "systems/pf2e/icons/equipment/treasure/art-objects/major-art-object/jeweled-mithral-crown.webp",
        22, CROWN_DESC,
        badge={"max": 99, "min": 1, "type": "counter", "value": 1})))

    docs.append(("effect-serithtials-wrath", effect(
        "fxSerithtialWr01", "Effect: Serithtial's Wrath", "effect-serithtials-wrath",
        "systems/pf2e/icons/equipment/artifacts/serithtial.webp", 20, SERITHTIAL_DESC,
        badge={"max": 99, "min": 1, "type": "counter", "value": 1})))

    for slug, doc in docs:
        B.write("items", slug, doc)
    print(f"[build_effects] emitted {len(docs)} automation docs into the items pack")
    patch_guide()

if __name__ == "__main__":
    main()
