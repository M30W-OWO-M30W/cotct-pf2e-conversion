// Find real "affliction"-type item docs in the installed pf2e system packs and
// dump schema samples for build_effects.py to copy EXACTLY. Also dumps one
// "effect"-type sample from equipment-effects (Effect: Aid) for the same reason.
// Run: node scripts/extract_afflictions.mjs   (writes scripts/affliction_samples.json)
import { ClassicLevel } from "classic-level";
import { writeFileSync, readdirSync, statSync } from "node:fs";
import { join } from "node:path";

const PF = "/mnt/c/Users/maman/AppData/Local/FoundryVTT/Data/systems/pf2e/packs";

// likely homes first, then every remaining item pack (afflictions are rare)
const LIKELY = ["campaign-effects", "other-effects", "equipment-effects",
                "bestiary-effects", "feat-effects", "spell-effects", "conditionitems"];
const all = readdirSync(PF).filter(d => statSync(join(PF, d)).isDirectory());
const order = [...LIKELY, ...all.filter(d => !LIKELY.includes(d))];

const afflictions = [];   // {pack, name, id}
let afflictionSample = null, effectSample = null;
for (const pack of order) {
  let db;
  try { db = new ClassicLevel(join(PF, pack), { valueEncoding: "json" }); }
  catch { continue; }
  try {
    for await (const [key, doc] of db.iterator()) {
      if (!doc || typeof doc !== "object") continue;
      if (doc.type === "affliction") {
        afflictions.push({ pack, name: doc.name, id: doc._id });
        if (!afflictionSample) afflictionSample = { pack, doc };
      }
      if (!effectSample && pack === "equipment-effects" && doc.type === "effect"
          && key.startsWith("!items!")) {
        effectSample = { pack, doc };
      }
    }
  } catch { /* non-item packs etc. */ }
  await db.close();
  if (afflictions.length && effectSample) break;  // got everything we need
}

writeFileSync(join(import.meta.dirname, "affliction_samples.json"), JSON.stringify({
  afflictionCount: afflictions.length,
  afflictionIndex: afflictions.slice(0, 50),
  afflictionSample, effectSample,
}, null, 2));
console.log(`afflictions found: ${afflictions.length}` +
  (afflictionSample ? ` (sample: ${afflictionSample.doc.name} from ${afflictionSample.pack})` : "") +
  (effectSample ? ` | effect sample: ${effectSample.doc.name}` : " | NO effect sample"));
