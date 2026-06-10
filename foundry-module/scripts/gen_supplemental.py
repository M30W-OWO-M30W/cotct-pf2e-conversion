#!/usr/bin/env python3
"""Generate the Supplemental Conversion Rulings doc from research/supplemental_rulings.json
(the 7-agent classification of every live check: community-ruled vs module-authored).

Outputs:
  - SUPPLEMENTAL_RULINGS.md          (repo root — Olliebird-style reference doc)
  - scripts/supplemental_rulings.html (journal-page HTML; DCs enriched to @Check
    badges; build_appendix.py adds it to the Conversion Guide)

Re-run after editing the JSON. Both outputs are committed."""
import json, html as _html, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]          # foundry-module/
REPO = ROOT.parent
SRC = REPO / "research" / "supplemental_rulings.json"

OLLIEBIRD = [
    ("Intro / methodology", "1TR8s94mhT9N2yFUzVTeMLgrn4feAECYm2AMedq8s-KU"),
    ("Ch.1 Edge of Anarchy", "170X0H7rZH7dkgtANKF3k6gs_bQKm6sgNFW2PrpelBP4"),
    ("Ch.2 Seven Days to the Grave", "17YX2kyfz-mqPtK9lieFlPg63DHgO_IgEMN_3IKRwwaA"),
    ("Ch.3 Escape from Old Korvosa", "1CzybQx7hNVVK9IL4dPB2QZQHVYiCbZlsvDe-LNtS1wA"),
    ("Ch.4 A History of Ashes", "1vqrIpiCctLGcs5D49ffAL8ubDojcMiVJSTuMWrbGuNY"),
    ("Ch.5 Skeletons of Scarwall", "19WIQNAvwJcG9HHsZ9NXMRQWHfQyQSznI--NeP6wTbjA"),
    ("Ch.6 Crown of Fangs", "1X5OpUKSK_e4e3tBYrkjNteX05SIyWv5ms4AbYtl8GOA"),
]

CH_TITLES = {
    "ch1": "Chapter 1: Edge of Anarchy", "ch2": "Chapter 2: Seven Days to the Grave",
    "ch3": "Chapter 3: Escape from Old Korvosa", "ch4": "Chapter 4: A History of Ashes",
    "ch5": "Chapter 5: Skeletons of Scarwall", "ch6": "Chapter 6: Crown of Fangs",
    "app": "Appendices & Beyond (incl. Conversion-Guide subsystems)",
}

SKILLS = ("Perception|Acrobatics|Arcana|Athletics|Crafting|Deception|Diplomacy|Intimidation"
          "|Medicine|Nature|Occultism|Performance|Religion|Society|Stealth|Survival|Thievery")
SAVES = "Reflex|Fortitude|Will"

def chk(kind, dc, basic=False):
    p = f"type:{kind}|dc:{dc}" + ("|basic:true" if basic else "")
    return f"@Check[{p}]"

def enrich(text):
    """Wrap DC mentions in @Check enrichers for the journal-page version."""
    # basis tags keep plain numbers ("Lock (DC 39)" -> "Lock (39)") so the page
    # carries no un-enriched raw DCs
    def detag(m):
        return "[" + re.sub(r"DC\s*(\d+)", r"\1", m.group(1)) + "]"
    text = re.sub(r"\[([^\]]+)\]$", detag, text)
    text = re.sub(rf"DC (\d+) basic ({SAVES})",
                  lambda m: chk(m.group(2).lower(), m.group(1), basic=True), text)
    text = re.sub(rf"DC (\d+) ({SAVES}|{SKILLS})",
                  lambda m: chk(m.group(2).lower(), m.group(1)), text)
    text = re.sub(rf"({SAVES}|{SKILLS}) DC (\d+)",
                  lambda m: chk(m.group(1).lower(), m.group(2)), text)
    text = re.sub(r"DC (\d+) Underworld Lore", lambda m: chk("underworld-lore", m.group(1)), text)
    text = re.sub(r"(?:flat check, DC (\d+)|DC (\d+) flat check)",
                  lambda m: chk("flat", m.group(1) or m.group(2)), text)
    return text

def main():
    data = json.loads(SRC.read_text(encoding="utf-8"))
    for row in data:
        r = row["r"]
        r["chapterTitle"] = CH_TITLES[row["ch"]]   # normalize agent phrasing
        r["_unescaped"] = None
    tot_ours = sum(r["r"]["counts"]["ours"] for r in data)
    tot_comm = sum(r["r"]["counts"]["community"] for r in data)

    # ---------------- markdown ----------------
    md = []
    md.append("# Curse of the Crimson Throne — Supplemental Conversion Rulings")
    md.append("")
    md.append("*Module-authored checks, in the style of the community conversion documents.*")
    md.append("")
    md.append("**What this is.** The [Olliebird community conversion]"
              "(https://www.reddit.com/r/Pathfinder2e/comments/o34twp/) is this module's DC and "
              f"statblock authority wherever it speaks ({tot_comm} of its rulings are adopted "
              "verbatim and are **not** repeated here). This document lists the **other half**: "
              f"every check the module authors itself ({tot_ours} rulings) — hazard Disable "
              "entries the community docs don't model, locks/climbs/socials they never keyed, "
              "PF2e subsystem ladders (chases, the Epidemic Clock, City Tiers, Rise of the "
              "Dragon), and item riders. Each bullet carries a basis tag:")
    md.append("")
    md.append("- `[level-based — …]` GM Core level-based DC for the area/creature/item level")
    md.append("- `[simple DC — trained/expert/master/legendary]` GM Core simple DC tier")
    md.append("- `[convention — …]` matched to an adjacent community ruling for a like obstacle")
    md.append("- `[hazard Stealth/Disable — PF2e format]` required by the PF2e hazard statblock "
              "format (the community converts these spots as bare skill lines or not at all)")
    md.append("- `[subsystem — …]` part of a module-built subsystem ladder")
    md.append("- `[GM Core …]` a specific GM Core table (Climb DCs, Forcing Open, craft DCs…)")
    md.append("")
    md.append("**Community source docs** (archived in `research/olliebird/`):")
    for name, gid in OLLIEBIRD:
        md.append(f"- [{name}](https://docs.google.com/document/d/{gid})")
    md.append("")
    md.append("| Chapter | Community rulings adopted | Module-authored |")
    md.append("|---|---|---|")
    for row in data:
        c = row["r"]["counts"]
        md.append(f"| {CH_TITLES[row['ch']]} | {c['community']} | {c['ours']} |")
    md.append(f"| **Total** | **{tot_comm}** | **{tot_ours}** |")
    md.append("")
    for row in data:
        r = row["r"]
        md.append(f"\n## {r['chapterTitle']}\n")
        for sec in r["sections"]:
            md.append(f"### {_html.unescape(sec['heading'])}")
            md.append("")
            md.append("Skill Checks, Saves, Other:")
            for b in sec["bullets"]:
                md.append(f"* {_html.unescape(b)}")
            md.append("")
        if r.get("notes"):
            md.append("Notes:")
            for n in r["notes"]:
                md.append(f"- {_html.unescape(n)}")
            md.append("")
    (REPO / "SUPPLEMENTAL_RULINGS.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    # ---------------- journal-page HTML ----------------
    h = []
    h.append("<p><em>Module-authored checks, in the style of the community conversion "
             "documents. The Olliebird conversion is this module's DC authority wherever it "
             f"speaks ({tot_comm} rulings adopted verbatim, not repeated here); the "
             f"{tot_ours} rulings below are the module's own — hazard Disable entries, "
             "unkeyed locks and climbs, subsystem ladders, and item riders. Basis tags in "
             "brackets name each DC's derivation. The full reference (with links to the "
             "community docs) lives in <code>SUPPLEMENTAL_RULINGS.md</code>.</em></p>")
    for row in data:
        r = row["r"]
        c = r["counts"]
        h.append(f"<h2>{_html.escape(_html.unescape(r['chapterTitle']))}</h2>")
        h.append(f"<p><em>Community rulings adopted: {c['community']} · "
                 f"module-authored: {c['ours']}.</em></p>")
        for sec in r["sections"]:
            h.append(f"<h3>{_html.escape(_html.unescape(sec['heading']))}</h3>")
            h.append("<ul>")
            for b in sec["bullets"]:
                h.append(f"<li>{enrich(_html.escape(_html.unescape(b)))}</li>")
            h.append("</ul>")
        if r.get("notes"):
            h.append("<section class=\"gm-notes\"><h4>Notes</h4><ul>")
            for n in r["notes"]:
                h.append(f"<li>{enrich(_html.escape(_html.unescape(n)))}</li>")
            h.append("</ul></section>")
    (ROOT / "scripts" / "supplemental_rulings.html").write_text("\n".join(h) + "\n", encoding="utf-8")

    leftover = re.findall(r"DC\s*\d+[^<]{0,40}",
                          re.sub(r"@Check\[[^\]]*\]", "", "\n".join(h)))
    print(f"md: {tot_ours} rulings, {len(data)} chapters; html written")
    if leftover:
        print(f"[warn] {len(leftover)} un-enriched DC mentions remain in the HTML:")
        for x in leftover[:20]:
            print("   ", x)

if __name__ == "__main__":
    main()
