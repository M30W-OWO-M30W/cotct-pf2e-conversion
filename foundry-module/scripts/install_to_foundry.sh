#!/usr/bin/env bash
# Refresh the LOCAL Foundry install of this private module.
# RUN WITH FOUNDRY CLOSED — Foundry locks the LevelDB pack files while running,
# which blocks overwriting them (you'll see "Permission denied" on LOCK/*.ldb).
#
# Copies the built module (incl. your git-ignored PDF in assets/private-source/)
# into the Foundry modules dir. Excludes node_modules.
set -euo pipefail

MODULE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEST="${1:-/mnt/c/Users/maman/AppData/Local/FoundryVTT/Data/modules/cotct-pf2e-conversion}"

# Heuristic running-check: a held LOCK we can't remove => Foundry is open.
if [ -e "$DEST/packs/journals/LOCK" ] && ! rm -f "$DEST/packs/journals/LOCK" 2>/dev/null; then
  echo "ERROR: '$DEST' packs are locked — close Foundry VTT completely, then re-run." >&2
  exit 1
fi

echo "Refreshing $DEST ..."
rm -rf "$DEST"
mkdir -p "$DEST"
cp -r "$MODULE_DIR"/module.json "$MODULE_DIR"/README.md "$MODULE_DIR"/CONVERSION_NOTES.md \
      "$MODULE_DIR"/package.json "$MODULE_DIR"/packs "$MODULE_DIR"/styles \
      "$MODULE_DIR"/assets "$MODULE_DIR"/scripts "$DEST"/
rm -rf "$DEST/node_modules"

echo "Installed. Checks:"
[ -f "$DEST/assets/private-source/curse-of-the-crimson-throne.pdf" ] && echo "  ✅ PDF present" || echo "  ⚠ PDF missing (drop your copy into assets/private-source/)"
for p in adventure journals actors hazards items scenes; do
  ls "$DEST/packs/$p/"*.ldb >/dev/null 2>&1 && echo "  ✅ pack: $p" || echo "  ⚠ pack empty: $p (run: npm run build)"
done
echo "Now start Foundry, enable the module, and import 'CotCT: Adventure (import this)'."
