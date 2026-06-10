#!/usr/bin/env python3
"""QA: scan every rendered read-aloud / verbatim block in the built journals for
two-column OCR interleave symptoms (column-header fragments, ligature junk,
stranded stat tokens, garbled words) and report per page."""
import json, glob, re, sys

SYMPTOMS = [
    (r"\b(?:CHAPTER|BACKGROUND|CONCLUSION|APPENDIX)\b", "column-header fragment"),
    (r"\bPART \d\b|\bPART (?:ONE|TWO|THREE|1|2|3):", "part-header fragment"),
    (r"\b(?:rff|ftfl|fffi|flff|ffft|flffft)\b", "ligature junk"),
    (r"\b[bcdfghjklmnpqrstvwxz]{6,}\b", "consonant garble"),
    (r"\bCR \d+\b|\bXP [\d,]+\b|\bhp \d+\b", "stranded stat token"),
    (r"\b(?:[A-Za-z] ){4,}[A-Za-z]\b", "spaced-letter garble"),
    (r"<!--", "markdown comment leak"),
    (r"\b[A-Z][a-z]+ [A-Z]{4,}\b(?!\s*(?:Maiden|Mantis|Company|Guard|Throne|Veil|Pool|Fangs|Queen|Hall|Tower|Bones|Spider|Knife))", "caps-run (possible caption leak)"),
]

bad = 0
for f in sorted(glob.glob("packs/journals/_source/*.json")):
    d = json.load(open(f))
    for p in d.get("pages", []):
        html = p.get("text", {}).get("content", "")
        # read-aloud sections + all verbatim-derived content
        for m in re.finditer(r'<section class="description">(.*?)</section>', html, re.S):
            txt = re.sub(r"<[^>]+>", " ", m.group(1))
            txt = re.sub(r"@\w+\[[^\]]*\](\{[^}]*\})?", " ", txt)
            for pat, label in SYMPTOMS:
                for hit in re.finditer(pat, txt):
                    ctx = txt[max(0, hit.start()-40):hit.end()+40].strip()
                    print(f"  [{label}] {d['name']} › {p['name']}\n      …{ctx}…")
                    bad += 1
print(f"\n{bad} read-aloud symptom(s) found" if bad else "read-aloud clean ✅")
sys.exit(1 if bad else 0)
