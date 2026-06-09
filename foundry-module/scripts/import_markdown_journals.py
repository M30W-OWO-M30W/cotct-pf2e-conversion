#!/usr/bin/env python3
"""Import rewritten AP Markdown into Kingmaker-style journal pages.

The source path is read from COTCT_AP_MD, or from the user's Downloads folder by
default. The script intentionally does not commit or copy the source Markdown;
it emits Foundry unpacked JSON journal entries derived from it.
"""
from __future__ import annotations

import copy
import hashlib
import html
import json
import os
import re
from pathlib import Path

import pf2e_build as B

SOURCE_ENV = "COTCT_AP_MD"
DEFAULT_SOURCE = Path.home() / "Downloads" / "Curse of the Crimson Throne AP.md"

CHAPTERS = [
    ("01", "Edge of Anarchy", "edge-of-anarchy"),
    ("02", "Seven Days to the Grave", "seven-days-to-the-grave"),
    ("03", "Escape from Old Korvosa", "escape-from-old-korvosa"),
    ("04", "A History of Ashes", "a-history-of-ashes"),
    ("05", "Skeletons of Scarwall", "skeletons-of-scarwall"),
    ("06", "Crown of Fangs", "crown-of-fangs"),
]

CHAPTER_IDS = {
    "01": "aO3z6QTqmYZCZYkw",  # preserve existing Old Fishery scene-note links
    "02": "j02SevenDays0000",
    "03": "j03OldKorvosa000",
    "04": "j04HistoryAshes0",
    "05": "j05Scarwall00000",
    "06": "j06CrownFangs000",
}

STAT_BLOCK_HEADINGS = {
    "DEFENSE",
    "OFFENSE",
    "TACTICS",
    "STATISTICS",
    "SPECIAL ABILITIES",
    "XP",
    "CR",
}

GLOBAL_PAGE_HEADINGS = {
    "CHAPTER BACKGROUND",
    "ADVANCEMENT TRACK",
    "NPC DEVELOPMENTS",
    "CHAPTER CONCLUSION",
    "HAUNTED FORTUNES",
    "A CITY GONE MAD",
    "BLOOD AND BONES",
    "INFECTION",
    "OUTBREAK",
    "CURING BLOOD VEIL",
    "FINAL SURVIVOR COUNT",
    "A CONSPIRACY REVEALED",
    "INTO THE DYING CITY",
    "THE ROAD NORTH",
    "THE FOURTH HARROWING",
    "BLACKBIRD RANCH",
    "THE KAZAVON SITUATION",
    "TRIALS OF RESPECT",
    "THE BLESSING OF THE ANCESTORS",
    "THE SPIRIT'S SONG",
    "OPTIONAL: A SWIFTER SCARWALL",
    "THE FINAL GOAL",
    "STREETS OF CHAOS",
    "THE FINAL HARROWING",
    "PREPARING FOR THE FINAL BATTLE",
}

LABEL_TO_SECTION = {
    "creature": "encounter",
    "creatures": "encounter",
    "trap": "encounter",
    "traps": "encounter",
    "hazard": "encounter",
    "hazards": "encounter",
    "haunt": "encounter",
    "haunts": "encounter",
    "encounter": "encounter",
    "treasure": "treasure",
    "reward": "treasure",
    "rewards": "treasure",
    "development": "gm",
    "developments": "gm",
    "story award": "gm",
    "story awards": "gm",
    "mission": "gm",
    "morale": "gm",
    "orphan": "gm",
    "orphans": "gm",
    "survivor count": "gm",
}

SKILL_MAP = {
    "acrobatics": "acrobatics",
    "appraise": "society",
    "bluff": "deception",
    "break": "athletics",
    "climb": "athletics",
    "craft": "crafting",
    "craft (alchemy)": "crafting",
    "diplomacy": "diplomacy",
    "disable device": "thievery",
    "escape artist": "acrobatics",
    "heal": "medicine",
    "intimidate": "intimidation",
    "knowledge": "society",
    "knowledge (arcana)": "arcana",
    "knowledge (engineering)": "crafting",
    "knowledge (history)": "society",
    "knowledge (local)": "society",
    "knowledge (nobility)": "society",
    "knowledge (religion)": "religion",
    "linguistics": "society",
    "perception": "perception",
    "sense motive": "perception",
    "spellcraft": "arcana",
    "strength": "athletics",
    "survival": "survival",
    "use magic device": "arcana",
}

PF2E_SKILLS = {
    "acrobatics",
    "arcana",
    "athletics",
    "crafting",
    "deception",
    "diplomacy",
    "intimidation",
    "medicine",
    "nature",
    "occultism",
    "perception",
    "performance",
    "religion",
    "society",
    "stealth",
    "survival",
    "thievery",
}


def stable_id(seed: str) -> str:
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    digest = hashlib.sha256(seed.encode("utf-8")).digest()
    return "".join(alphabet[b % len(alphabet)] for b in digest[:16])


def source_path() -> Path:
    return Path(os.environ.get(SOURCE_ENV, DEFAULT_SOURCE)).expanduser()


def clean_title(title: str) -> str:
    title = re.sub(r"\s+", " ", title.strip().strip("#").strip())
    title = title.replace("Â", "").replace("\xa0", " ")
    title = re.sub(r"\s+", " ", title)
    words = []
    for word in title.split(" "):
        if re.fullmatch(r"[A-Ha-h]\d{1,2}", word):
            words.append(word.upper())
        elif word.lower() in {"of", "the", "and", "to", "in", "on", "for", "a", "an"}:
            words.append(word.lower())
        elif word.isupper() and len(word) <= 4:
            words.append(word)
        else:
            words.append(word[:1].upper() + word[1:].lower())
    cleaned = " ".join(words)
    cleaned = re.sub(r"\bCr\b", "CR", cleaned)
    cleaned = re.sub(r"\bXp\b", "XP", cleaned)
    if cleaned and cleaned[0].islower():
        cleaned = cleaned[0].upper() + cleaned[1:]
    return cleaned


def clean_text(text: str) -> str:
    text = text.replace("\ufeff", "")
    text = text.replace("\xa0", " ").replace("Â", "")
    text = text.replace("Ã—", "x")
    text = text.replace("â€”", "-").replace("â€“", "-")
    text = text.replace("â€˜", "'").replace("â€™", "'").replace("â€œ", '"').replace("â€�", '"')
    text = re.sub(r"<!--\s*image\s*-->", "", text, flags=re.I)
    text = re.sub(r"<!--\s*pages?[^>]*-->", "", text, flags=re.I)
    text = re.sub(r"[ \t]+", " ", text)
    return text


def find_line(lines: list[str], needle: str, start: int = 0, heading: bool | None = None) -> int:
    needle_l = needle.lower()
    for idx in range(start, len(lines)):
        line = lines[idx].strip()
        if heading is True and not line.startswith("## "):
            continue
        if heading is False and line.startswith("## "):
            continue
        if needle_l in line.lower():
            return idx
    raise ValueError(f"Could not find chapter anchor: {needle}")


def first_heading_after(lines: list[str], needle: str, start: int) -> int:
    anchor = find_line(lines, needle, start)
    for idx in range(anchor, len(lines)):
        if lines[idx].strip().upper() == "## CHAPTER BACKGROUND":
            return idx
    raise ValueError(f"Could not find CHAPTER BACKGROUND after: {needle}")


def chapter_ranges(lines: list[str]) -> list[tuple[str, str, str, int, int]]:
    starts = {
        "01": find_line(lines, "## CHAPTER BACKGROUND"),
        "02": find_line(lines, "## SEVEN DAYS TO THE GRAVE"),
        "03": first_heading_after(lines, "ESCAPE FROM OLD KORVOSA", 5000),
        "04": first_heading_after(lines, "BY MICHAEL KORTES AND JAMES JACOBS", 7800),
        "05": find_line(lines, "## SKELETONS OF SCARWALL", 10000, heading=True),
        "06": find_line(lines, "## CHAPTER BACKGROUND", 14300, heading=True),
    }
    end = find_line(lines, "## APPENDIX", starts["06"], heading=True)
    ordered = []
    for idx, (num, name, slug) in enumerate(CHAPTERS):
        start = starts[num]
        stop = starts[CHAPTERS[idx + 1][0]] if idx + 1 < len(CHAPTERS) else end
        ordered.append((num, name, slug, start, stop))
    return ordered


def bare_heading(line: str) -> tuple[str, bool]:
    stripped = line.strip()
    if stripped.startswith("## "):
        return stripped[3:].strip(), True
    return stripped, False


def is_page_heading(title: str, markdown_heading: bool) -> bool:
    raw = re.sub(r"\s+", " ", title.strip())
    if not raw:
        return False
    upper = raw.upper()
    if upper in {"TABLE OF CONTENTS", "MAPS"}:
        return False
    if upper in STAT_BLOCK_HEADINGS:
        return False
    if re.match(r"(?i)^event\s+\d+\b", raw):
        return True
    if re.match(r"(?i)^[A-H]\d{1,2}\b", raw):
        return True
    if re.match(r"(?i)^[A-H]\s{1,3}[A-Z'\"].+", raw):
        return True
    if upper in GLOBAL_PAGE_HEADINGS:
        return True
    return False


def split_sections(lines: list[str], start: int, stop: int) -> list[dict[str, object]]:
    sections: list[dict[str, object]] = []
    current: dict[str, object] | None = None
    for line in lines[start:stop]:
        title, is_md = bare_heading(line)
        if is_page_heading(title, is_md):
            if current and current["lines"]:
                sections.append(current)
            current = {"title": clean_title(title), "raw_title": title, "lines": []}
        elif current is not None:
            current["lines"].append(line)
    if current and current["lines"]:
        sections.append(current)
    return sections


def para_html(text: str) -> str:
    return "<p>" + html.escape(text, quote=False) + "</p>"


def heading_html(text: str) -> str:
    return "<h4>" + html.escape(clean_title(text), quote=False) + "</h4>"


def paragraphs(raw_lines: list[str]) -> list[str]:
    text = clean_text("\n".join(raw_lines))
    out: list[str] = []
    buf: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            if buf:
                out.append(" ".join(buf).strip())
                buf = []
            continue
        if stripped.startswith("|") or re.fullmatch(r"[-| :]+", stripped):
            continue
        if stripped.startswith("## "):
            if buf:
                out.append(" ".join(buf).strip())
                buf = []
            out.append(stripped)
            continue
        buf.append(stripped)
    if buf:
        out.append(" ".join(buf).strip())
    return [p for p in out if p]


def section_kind(paragraph: str) -> str | None:
    if paragraph.startswith("## "):
        return "encounter"
    match = re.match(r"^([A-Za-z][A-Za-z ]{2,30})\s*:\s*", paragraph)
    if not match:
        return None
    return LABEL_TO_SECTION.get(match.group(1).strip().lower())


def strip_label(paragraph: str) -> tuple[str | None, str]:
    match = re.match(r"^([A-Za-z][A-Za-z ]{2,30})\s*:\s*(.*)$", paragraph)
    if not match:
        return None, paragraph
    return match.group(1).strip(), match.group(2).strip()


def infer_skill(name: str) -> str | None:
    key = re.sub(r"\s+", " ", name.lower().strip())
    key = key.split(" or ")[0].strip()
    if key.startswith("knowledge"):
        key = key if key in SKILL_MAP else "knowledge"
    inferred = SKILL_MAP.get(key, key.replace(" ", "-"))
    return inferred if inferred in PF2E_SKILLS else None


def dc_checks(text: str) -> list[str]:
    found: list[tuple[str, str]] = []
    patterns = [
        re.compile(r"(?i)\bDC\s*(\d+)\s+([A-Za-z]+(?:\s*\([^)]+\))?)\s+check"),
        re.compile(r"(?i)\b([A-Za-z]+(?:\s*\([^)]+\))?)\s+DC\s*(\d+)\b"),
    ]
    for match in patterns[0].finditer(text):
        found.append((match.group(2), match.group(1)))
    for match in patterns[1].finditer(text):
        found.append((match.group(1), match.group(2)))
    seen = set()
    checks = []
    for skill, dc in found:
        skill = re.sub(r"\s+", " ", skill).strip()
        key = (skill.lower(), dc)
        if key in seen:
            continue
        check_type = infer_skill(skill)
        if not check_type:
            continue
        seen.add(key)
        checks.append(f"<li>{html.escape(skill, quote=False)}: @Check[type:{check_type}|dc:{dc}]</li>")
    return checks


def page_level(title: str) -> int:
    if re.match(r"(?i)^[A-H]\d{1,2}\b|^event\s+\d+\b", title):
        return 3
    if re.match(r"(?i)^[A-H]\s{1,3}", title):
        return 2
    if title.upper() in {"CHAPTER BACKGROUND", "ADVANCEMENT TRACK", "NPC DEVELOPMENTS", "CHAPTER CONCLUSION"}:
        return 1
    return 2


def area_code(title: str) -> str | None:
    match = re.match(r"(?i)^([A-H]\d{1,2})\b", title)
    if match:
        return match.group(1).upper()
    return None


def build_page_html(title: str, raw_lines: list[str]) -> str:
    paras = paragraphs(raw_lines)
    read_aloud: list[str] = []
    gm: list[str] = []
    encounters: list[str] = []
    treasure: list[str] = []

    first_body = True
    active = "gm"
    for paragraph in paras:
        if paragraph.startswith("## "):
            active = "encounter"
            encounters.append(heading_html(paragraph[3:]))
            continue
        kind = section_kind(paragraph)
        if kind:
            active = kind
        label, body = strip_label(paragraph)
        rendered = para_html(f"{label}: {body}" if label else body)
        if first_body and not label and area_code(title):
            read_aloud.append(rendered)
            first_body = False
            continue
        first_body = False
        if active == "encounter":
            encounters.append(rendered)
        elif active == "treasure":
            treasure.append(rendered)
        else:
            gm.append(rendered)

    checks = dc_checks(" ".join(paras))
    html_parts: list[str] = []
    if read_aloud:
        html_parts.append(B.s_desc("".join(read_aloud)))
    if gm:
        html_parts.append(B.s_gm("".join(gm)))
    if checks:
        html_parts.append(B.s_skill("<h3>Checks</h3><ul>" + "".join(checks[:20]) + "</ul>"))
    if encounters:
        html_parts.append(B.s_encounter("<h3>Encounters</h3>" + "".join(encounters)))
    if treasure:
        html_parts.append(B.s_treasure("<h3>Treasure</h3>" + "".join(treasure)))
    html_parts.append(B.s_conv("<p>Imported from the supplied rewritten Markdown source. PF2e mechanics and balancing should be checked against the conversion reports before play.</p>"))
    return "".join(html_parts)


def extract_mechanics_sections(content: str) -> str:
    labels = {
        "skill": "PF2e Checks",
        "encounter": "PF2e Encounter",
        "treasure": "PF2e Treasure",
        "conversion": "Conversion Notes",
    }
    chunks = []
    for match in re.finditer(r'<section class="(skill|encounter|treasure|conversion)">(.*?)</section>', content, re.S):
        label = labels[match.group(1)]
        inner = re.sub(r"@UUID\[\.[A-Za-z0-9]+\]\{([^}]+)\}", r"\1", match.group(2))
        chunks.append(f"<h4>{label}</h4>{inner}")
    return "".join(chunks)


def existing_ch1_pages() -> dict[str, dict[str, str]]:
    path = B.PACKS / "journals" / "_source" / "01-edge-of-anarchy.json"
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    mapping = {}
    for page in data.get("pages", []):
        code = area_code(page.get("name", ""))
        if code:
            mapping[code] = {
                "id": page["_id"],
                "mechanics": extract_mechanics_sections(page.get("text", {}).get("content", "")),
            }
    return mapping


def journal_folder_id() -> str | None:
    folder_path = B.PACKS / "journals" / "_source" / "_folder_adventure-jou.json"
    if not folder_path.exists():
        return None
    return json.loads(folder_path.read_text(encoding="utf-8")).get("_id")


def strip_embedded(doc: dict) -> dict:
    stripped = copy.deepcopy(doc)
    stripped.pop("_key", None)
    for collection in ("items", "pages", "notes", "tokens"):
        for item in stripped.get(collection, []):
            item.pop("_key", None)
    return stripped


def generate(source: Path) -> list[dict]:
    raw = source.read_text(encoding="utf-8-sig")
    lines = raw.splitlines()
    ranges = chapter_ranges(lines)
    folder = journal_folder_id()
    ch1_existing = existing_ch1_pages()
    journals = []

    for num, chapter_name, slug, start, stop in ranges:
        sections = split_sections(lines, start, stop)
        pages = []
        title_counts: dict[str, int] = {}
        used_ch1_codes: set[str] = set()
        for section in sections:
            base_title = str(section["title"])
            title_counts[base_title] = title_counts.get(base_title, 0) + 1
            occurrence = title_counts[base_title]
            title = base_title if occurrence == 1 else f"{base_title} ({occurrence})"
            code = area_code(base_title)
            page_id = None
            if num == "01" and code and code not in used_ch1_codes:
                page_id = ch1_existing.get(code, {}).get("id")
                used_ch1_codes.add(code)
            page_id = page_id or stable_id(f"journal-page:{num}:{base_title}:{occurrence}")
            content = build_page_html(base_title, section["lines"])
            mechanics = ch1_existing.get(code, {}).get("mechanics") if num == "01" and code else None
            if mechanics:
                content += B.s_conv("<h3>PF2e Pilot Implementation</h3>" + mechanics)
            pages.append(B.page(page_id, title, content, level=page_level(base_title)))
        journal = B.journal_entry(
            CHAPTER_IDS[num],
            f"{int(num)}. {chapter_name}",
            pages,
            folder=folder,
            sort=int(num) * 100000,
            default_own=0,
        )
        B.write("journals", f"{num}-{slug}", journal, embed_pages=True)
        journals.append(journal)
    return journals


def patch_adventure(journals: list[dict]) -> None:
    path = B.PACKS / "adventure" / "_source" / "cotct-edge-of-anarchy.json"
    if not path.exists():
        return
    adventure = json.loads(path.read_text(encoding="utf-8"))
    adventure["name"] = "Curse of the Crimson Throne - Adventure Journals"
    adventure["caption"] = (
        "<p>Imports the Markdown-derived adventure journals, the Old Fishery scene "
        "(map-note pins + staged tokens), the converted pilot NPCs/hazards, and the pilot treasure.</p>"
    )
    adventure["description"] = adventure["caption"]
    adventure["journal"] = [strip_embedded(j) for j in journals]
    path.write_text(json.dumps(adventure, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def populate(source: Path | None = None) -> list[dict]:
    src = source or source_path()
    if not src.exists():
        raise FileNotFoundError(f"Markdown source not found: {src}")
    journals = generate(src)
    patch_adventure(journals)
    return journals


def main() -> None:
    journals = populate()
    pages = sum(len(j.get("pages", [])) for j in journals)
    print(f"Imported Markdown journals: {len(journals)} journals, {pages} pages")


if __name__ == "__main__":
    main()
