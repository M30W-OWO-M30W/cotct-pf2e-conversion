#!/usr/bin/env bash
# Rebuild the CotCT module from the current working tree and sync it into the
# local Foundry VTT install. Run this with FOUNDRY CLOSED — the compendium
# LevelDB is locked while Foundry runs, so packs can't be replaced otherwise.
#
# Normally invoked by the Windows launcher "Sync CotCT to Foundry.bat", but it
# is also fine to run directly:  bash scripts/sync_to_foundry.sh
set -uo pipefail

REPO="/home/saber/pf2e-conversion/curse-of-the-crimson-throne/foundry-module"
DEST="/mnt/c/Users/maman/AppData/Local/FoundryVTT/Data/modules/cotct-pf2e-conversion"

cd "$REPO" || { echo "!! repo not found: $REPO"; exit 1; }
[ -d "$DEST" ] || { echo "!! Foundry module folder not found: $DEST"; exit 1; }

echo "==> Building pilot (build_pilot.py)..."
python3 scripts/build_pilot.py || { echo "!! build_pilot.py failed"; exit 1; }
echo "==> Building Chapter 2 (build_ch2.py)..."
python3 scripts/build_ch2.py || { echo "!! build_ch2.py failed"; exit 1; }
echo "==> Building Chapter 3 (build_ch3.py)..."
python3 scripts/build_ch3.py || { echo "!! build_ch3.py failed"; exit 1; }
echo "==> Building Chapter 4 (build_ch4.py)..."
python3 scripts/build_ch4.py || { echo "!! build_ch4.py failed"; exit 1; }
echo "==> Building Chapter 5 (build_ch5.py)..."
python3 scripts/build_ch5.py || { echo "!! build_ch5.py failed"; exit 1; }
echo "==> Building Chapter 6 (build_ch6.py)..."
python3 scripts/build_ch6.py || { echo "!! build_ch6.py failed"; exit 1; }
echo "==> Building Appendices (build_appendix.py)..."
python3 scripts/build_appendix.py || { echo "!! build_appendix.py failed"; exit 1; }
echo "==> Emitting community-only Olliebird docs (build_community.py)..."
python3 scripts/build_community.py || { echo "!! build_community.py failed"; exit 1; }

echo "==> Checking read-aloud for OCR interleave..."
python3 scripts/check_readaloud.py || { echo "!! read-aloud OCR symptoms found"; exit 1; }

echo "==> Validating links/ids + content..."
vout=$(npm run --silent validate)
if ! printf '%s' "$vout" | grep -q "problems=0"; then
  echo "!! validation reported problems — aborting sync:"
  printf '%s\n' "$vout" | sed -n '/# Foundry/,/Problems/p'
  exit 1
fi
# surface the non-fatal content warnings (OCR splits / un-enriched DCs)
printf '%s\n' "$vout" | sed -n '/## Content warnings/,/## External/p' | sed '/## External/d'

echo "==> Compiling packs to LevelDB..."
npm run --silent build >/dev/null || { echo "!! npm run build failed"; exit 1; }

running_msg() {
  echo
  echo "######################################################################"
  echo "#  FOUNDRY IS RUNNING — its compendium database is locked, so NOTHING"
  echo "#  was changed (the module is left as-is, not half-updated)."
  echo "#  --> Close Foundry completely, then run this again."
  echo "######################################################################"
  exit 2
}

# Pre-flight: refuse to touch anything while Foundry is open, so the install can
# never end up half-synced (new module.json, stale packs).
if command -v tasklist.exe >/dev/null 2>&1 \
   && tasklist.exe 2>/dev/null | grep -qiE "FoundryVTT|Foundry Virtual"; then
  running_msg
fi

echo "==> Syncing into Foundry: $DEST"
err=$(cp -rf packs/. "$DEST/packs/" 2>&1 >/dev/null)
# Fallback lock detection (in case the process check missed it): abort BEFORE
# bumping module.json, so the version never lies about what's actually installed.
if printf '%s' "$err" | grep -qiE "permission denied|resource busy|text file busy"; then
  running_msg
fi
cp -f module.json "$DEST/module.json"
cp -f styles/cotct-journal.css "$DEST/styles/cotct-journal.css"
cp -f scripts/*.py scripts/*.mjs "$DEST/scripts/" 2>/dev/null

ver=$(grep -oE '"version": *"[^"]*"' module.json | head -1)
echo
echo "==> Done. Module synced ($ver)."
echo "    Reopen Foundry and open the journal from the COMPENDIUM"
echo "    (CotCT: Journals) — it is now up to date. No import needed."
echo "    (Only if you've imported the Adventure into a world do you"
echo "     also need to re-import to refresh that copy.)"
