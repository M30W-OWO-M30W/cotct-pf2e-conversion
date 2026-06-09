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

echo "==> Validating links/ids..."
if ! npm run --silent validate | grep -q "problems=0"; then
  echo "!! validation reported problems — aborting sync:"
  npm run --silent validate | sed -n '/# Foundry/,/Problems/p'
  exit 1
fi

echo "==> Compiling packs to LevelDB..."
npm run --silent build >/dev/null || { echo "!! npm run build failed"; exit 1; }

echo "==> Syncing into Foundry: $DEST"
err=$(cp -rf packs/. "$DEST/packs/" 2>&1 >/dev/null)
cp -f module.json "$DEST/module.json"
cp -f styles/cotct-journal.css "$DEST/styles/cotct-journal.css"
cp -f scripts/*.py scripts/*.mjs "$DEST/scripts/" 2>/dev/null

if printf '%s' "$err" | grep -qiE "permission denied|resource busy|text file busy"; then
  echo
  echo "######################################################################"
  echo "#  FOUNDRY APPEARS TO BE RUNNING — the compendium database is locked,"
  echo "#  so the journal/actor packs were NOT fully updated."
  echo "#  --> Close Foundry completely, then run this again."
  echo "######################################################################"
  exit 2
fi

ver=$(grep -oE '"version": *"[^"]*"' module.json | head -1)
echo
echo "==> Done. Module synced ($ver)."
echo "    Reopen Foundry and open the journal from the COMPENDIUM"
echo "    (CotCT: Journals) — it is now up to date. No import needed."
echo "    (Only if you've imported the Adventure into a world do you"
echo "     also need to re-import to refresh that copy.)"
