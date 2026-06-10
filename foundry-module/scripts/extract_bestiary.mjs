// Extract official pf2e Bestiary creature index (name -> {pack,id,level}) from the
// installed pf2e system LevelDB packs. Reusable across the whole AP conversion:
// official monsters get @UUID links to the Bestiary instead of being rebuilt.
// Run: node scripts/extract_bestiary.mjs   (writes scripts/bestiary_index.json)
import { ClassicLevel } from "classic-level";
import { writeFileSync } from "node:fs";
import { join } from "node:path";

const PF = "/mnt/c/Users/maman/AppData/Local/FoundryVTT/Data/systems/pf2e/packs";
const PACKS = [
  "pathfinder-monster-core", "pathfinder-monster-core-2",
  "pathfinder-bestiary", "pathfinder-bestiary-2", "pathfinder-bestiary-3",
];

const index = {};   // slug -> {pack,id,level,name}  (first writer wins: monster-core preferred)
let total = 0;
for (const pack of PACKS) {
  const db = new ClassicLevel(join(PF, pack), { valueEncoding: "json" });
  for await (const [key, doc] of db.iterator()) {
    if (!doc || doc.type !== "npc") continue;
    const id = doc._id;
    const name = doc.name;
    if (!name || !id) continue;
    const slug = (doc.system?.details?.slug) ||
      name.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
    total++;
    if (!(slug in index)) {
      index[slug] = { pack, id, level: doc.system?.details?.level?.value ?? null, name };
    }
  }
  await db.close();
}
const sorted = {};
for (const k of Object.keys(index).sort()) sorted[k] = index[k];
writeFileSync(join(import.meta.dirname, "bestiary_index.json"),
  JSON.stringify(sorted, null, 2));
console.log(`indexed ${Object.keys(index).length} unique creatures from ${total} npc docs across ${PACKS.length} packs`);
