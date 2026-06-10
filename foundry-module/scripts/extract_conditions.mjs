// Extract the full pf2e condition slug->id map (for cond() links) from the
// installed system's conditionitems pack. Writes scripts/conditions_index.json.
import { ClassicLevel } from "classic-level";
import { writeFileSync } from "node:fs";
import { join } from "node:path";

const candidates = ["conditionitems", "conditions"];
const PFROOT = "/mnt/c/Users/maman/AppData/Local/FoundryVTT/Data/systems/pf2e/packs";
let out = {};
for (const c of candidates) {
  try {
    const db = new ClassicLevel(join(PFROOT, c), { valueEncoding: "json" });
    for await (const [key, doc] of db.iterator()) {
      if (!doc?._id || !doc?.name) continue;
      const slug = doc.system?.slug || doc.name.toLowerCase().replace(/[^a-z0-9]+/g, "-");
      out[slug] = doc._id;
    }
    await db.close();
    if (Object.keys(out).length) break;
  } catch (e) { /* try next */ }
}
const sorted = {};
for (const k of Object.keys(out).sort()) sorted[k] = out[k];
writeFileSync(join(import.meta.dirname, "conditions_index.json"), JSON.stringify(sorted, null, 2));
console.log(`indexed ${Object.keys(out).length} conditions:`, Object.keys(sorted).join(", "));
